const express = require("express");

const PORT = process.env.PORT || 3001;

const app = express();

app.get("/weather", (req, res) => {
  console.log(`weather request for lat: ${req.query.lat}, long: ${req.query.long}`)
  res.json({ message: "sunny" });
});

app.listen(PORT, () => {
  console.log(`Server listening on ${PORT}`);
});

