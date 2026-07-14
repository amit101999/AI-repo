import express from "express";
import dotenv from "dotenv";
dotenv.config();
import proxy from 'express-http-proxy'

const app = express();
const PORT = process.env.PORT || 8000;

app.use("/auth", proxy(process.env.AUTH_SERVICE));

app.get("/", (req, res) => {
    res.send("Hello from the Gateway!");
});

