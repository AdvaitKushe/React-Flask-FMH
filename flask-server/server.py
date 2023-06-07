from flask import Flask, request
import pandas as pd
import haversine as hs
from haversine import Unit
import geopy
import geocoder
from geopy.geocoders import Nominatim
import geopandas
import json

app = Flask(__name__)


@app.route("/members")
def members():
    global user_input
    df = pd.read_csv('Hospital_Data.csv')
    df1 = pd.read_csv('Discharge_Data.csv')
    #cleaning first dataset
    
    s1=input("enter state 1")
    s2 = input("enter state 2")
    s3= input("enter state 3")
    discharge_to_hos = []
    curr = -1
    for i in df1.index:
        if df1['Rndrng_Prvdr_State_Abrvtn'][i] == s1 or df1['Rndrng_Prvdr_State_Abrvtn'][i] == s2 or df1['Rndrng_Prvdr_State_Abrvtn'][i] == s3:
            if i != 0 and (df1['Rndrng_Prvdr_Org_Name'][i-1] == df1['Rndrng_Prvdr_Org_Name'][i]):
                discharge_to_hos[curr][1] = discharge_to_hos[curr][1] + \
                    df1["Tot_Dschrgs"][i]
            else:
                curr = curr + 1
                discharge_to_hos.append([
                    str.lower(df1['Rndrng_Prvdr_Org_Name'][i]), df1['Tot_Dschrgs'][i]])


    hos_dis = pd.DataFrame(discharge_to_hos)

    hos_dis = hos_dis.rename(columns={0: "Hospital", 1: "Total Discharge"})

    locator = Nominatim(user_agent='My_agent')


    g = geocoder.ip('me')
    g = g.latlng

    # Current GeoLocation
    myLoc = (g[0], g[1])

    #Cleaning and filtering data, and calculating information, merging two datasets into one
    newData = []
    inp = 50
    for i in df.index:
        if df['State'][i] == 'VA' :#or df['State'][i] == 'DC' or df['State'][i] == 'MD':
            addr = str.lower(df['Street Address'][i])
            city = str.lower(df['City'][i])
            state = str.lower(df['State'][i])
            hos = str.lower(df['Facility Name'][i])

            beds = df['Certified Bed Count'][i]
            location = locator.geocode(
                addr+", " + city + ", " + state, timeout=None)

            if location != None and not hos_dis.loc[hos_dis["Hospital"] == hos].empty:
                temp = hos_dis.loc[hos_dis["Hospital"] == hos].iloc[0]
                dis = temp['Total Discharge']

                admi = (df['inpatient_beds_used'][i])
                # Available Beds = Total Beds - (Admissions x Length of Stay) + Discharges
                availBeds_Predi = beds - ((admi) * 5.5) + (dis/360)

                miles = hs.haversine(
                    myLoc, (location.latitude, location.longitude), unit=Unit.MILES)
                if miles <= float(inp):

                    allgeo = [state, hos, addr, city,
                            beds, int(100*(availBeds_Predi/beds)), miles]

                    newData.append(allgeo)


    df = pd.DataFrame(newData)
    df = df.rename(columns={0: "State", 1: "Facility Name", 2: "Address",
                            3: "City", 4: "Bed Count", 5: "Available Beds Predi", 6: "Miles_Away"})


    # Sort Data
    df= df.sort_values(by=['Available Beds Predi'],kind='quicksort')
    json_data = df.to_json()

# Load the JSON data as a dictionary
    data = json.loads(json_data)

    # Create a new list to store the grouped data
    hospital_data = []

    # Iterate over the keys in the "State" dictionary
    for key in data["State"].keys():
        # Create a new dictionary for each hospital
        hospital = {
            "State": data["State"][key],
            "Name": data["Facility Name"][key],
            "Address": data["Address"][key],
            "City": data["City"][key],
            "Bed Count": data["Bed Count"][key],
            "Bed Predi": data["Available Beds Predi"][key],
            "Miles Away": data["Miles_Away"][key]
        }
        # Add the hospital to the list
        hospital_data.append(hospital)

    # Create a new dictionary with the hospital data
    output_data = {"hospital": hospital_data}

    return output_data
if __name__ == "__main__":
    app.run(debug=True, port=8080)
