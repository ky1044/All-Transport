const express = require("express");
const bodyParser = require("body-parser");
const request = require("request");
const app = express();

require("dotenv").config();

const weatherApiKey = `${process.env.WEATHER_API_KEY}`;
const weatherApiUrl = `${process.env.WEATHER_API_URL}`;

const PORT = process.env.PORT || 3001;


app.get("/weather", (req, res) => {
  console.log(`weather request for lat: ${req.query.lat}, long: ${req.query.long}`)

  let url = `${weatherApiUrl}/weather?lat=${req.query.lat}&lon=${req.query.long}&appid=${weatherApiKey}`;
  console.log(url);

  request(url, function(err, response, body) {

    // On return, check the json data fetched
    if (err) {
      console.log("ERROR")
        // res.render('index', { weather: null, error: 'Error, please try again' });
        res.json({ message: "error getting weather data" });
    } else {
        console.log(body)
        let data = JSON.parse(body);

        console.log(data);
        res.json({ message: data });
    };
  });

  

});

app.listen(PORT, () => {
  console.log(`Server listening on ${PORT}`);
});

