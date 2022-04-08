import React, { useEffect, useState } from "react";
import './App.css';

function App() {

  const location = {
    "cityName":"New York",
    "lat":40.733662,
    "long":-73.986496
  }

  return (
    <div className="App">
      <h1>Manttan Transit</h1>
      <Weather location = {location}/>
    </div>
  );

}

function Weather(props){

  const [weatherData, setData] = React.useState(null);

  React.useEffect(() => {
    fetch(`/weather?lat=${props.location.lat}&long=${props.location.long}`)
      .then((res) => res.json())
      .then((data) => setData(data.message));
  }, []);

  return (
    <div>
      <p>current weather in {props.location.cityName}: {!weatherData ? "Loading..." : weatherData}</p>
    </div>
  );

}

export default App;
