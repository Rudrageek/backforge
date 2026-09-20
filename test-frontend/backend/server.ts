import express from "express";

const app = express();

app.get(
  "/api/bookings",
  (req, res) => {
    res.json([]);
  }
);