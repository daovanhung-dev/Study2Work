import express from "express";
import path from "path";
import { fileURLToPath } from "url";

import student_router from "./routes/student_route.js";
import business_router from "./routes/business_route.js";
import web_router from "./routes/web_routes.js";

import { authenticateToken } from "./middleware/auth.middleware.js";

const app = express();

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

app.set("view engine", "ejs");
app.set("views", path.join(__dirname, "views"));

app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use(express.static(path.join(__dirname, "../public")));
app.use(authenticateToken);

// ROUTES
app.use("/", web_router);
app.use("/business", business_router);
app.use("/student", student_router);

export default app;
