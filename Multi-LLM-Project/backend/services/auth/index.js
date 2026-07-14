import express from "express";
import dotenv from "dotenv";
dotenv.config();
import connectDB from "./config/db.js";

const app = express();
const PORT = process.env.PORT || 8000;

connectDB();

app.get("/", (req, res) => {
    res.send("Hello from the Auth Service!");
});

