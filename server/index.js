const express = require("express");

const PORT = process.env.PORT || 3001;

const app = express();

app.get("/weather", (req, res) => {
  res.json({ message: "sunny" });
});

app.listen(PORT, () => {
  console.log(`Server listening on ${PORT}`);
});

