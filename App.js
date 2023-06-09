import React, {useState, useEffect} from 'react'

function App(){
  const[data, setData] = useState([{}])

  useEffect(()=> { 
    console.log('UseEffect called')
    fetch ("/members").then(
        res => res.json()
          ).then (
              data => {
                  setData(data)
                  console.log(data)
                }
              )
  },[]) 
console.log("this is hos data",data.hospital)

  return (
   /*<div>
    
    <h1>Hospital Data</h1>
    
    {data.hospital.map((hospital, index) => (
  <div key={index}>
    <h2>{hospital.Name}</h2>
    <p>Address: {hospital.Address}</p>
    <p>Bed Count: {hospital['Bed Count']}</p>
    <p>Bed Prediction: {hospital['Bed Predi']}</p>
    <p>City: {hospital.City}</p>
    <p>Miles Away: {hospital['Miles Away']}</p>
    <p>State: {hospital.State}</p>
  </div>
))}
*/
<div>
<h1>Hospital Data</h1>
{

(typeof data.hospital === 'undefined')?(<p>Loading...</p>):(data.hospital.map((hospital,index) => (
  <div key={index}>
    <h2>{hospital.Name}</h2>
    <p>Address: {hospital.Address}</p>
    <p>Bed Count: {hospital['Bed Count']}</p>
    <p>Bed Prediction: {hospital['Bed Predi']}%</p>
    <p>City: {hospital.City}</p>
    <p>Miles Away: {hospital['Miles Away']}</p>
    <p>State: {hospital.State}</p>

</div>
      )))
}

</div>
  

) 

}


export default App