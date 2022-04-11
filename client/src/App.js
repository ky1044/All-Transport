import React, { useEffect, useState } from "react";
import './App.css';

function App() {

  const [lat, setLat] = useState([]);
  const [long, setLong] = useState([]);

  useEffect(() => {
    navigator.geolocation.getCurrentPosition(function(position) {
      setLat(position.coords.latitude);
      setLong(position.coords.longitude);
    });

    console.log("Latitude is:", lat)
    console.log("Longitude is:", long)
  }, [lat, long]);

  return (
    <div className="App">
      <h1>Manttan Transit</h1>
      <Weather lat = {lat} long = {long}/>
    </div>
  );

}

function Weather(props){

  const [weatherData, setData] = useState(null);

  useEffect(() => {
    props.lat && props.long &&
    fetch(`/weather?lat=${props.lat}&long=${props.long}`)
      .then((res) => res.json())
      .then((data) => {
        setData(data.message);
      });
  }, []);

  return (
    <div>
      {
        !weatherData || !weatherData.weather || !weatherData.weather[0]?
        <p>Getting Current Weather...</p>:
        <p>Current Weather for {weatherData.name}: {weatherData.weather[0].main} at {Math.floor(weatherData.main.temp-273.15)} Celcius</p>
      }
    </div>
  );

}

export default App;
