import express from "express";
import path from "path";
import { fileURLToPath } from "url";
import dotenv from "dotenv";

import student_router from "./routes/student_route.js";
import business_router from "./routes/business_route.js";
import web_router from "./routes/web_routes.js";

import cookieParser from "cookie-parser";
import session from "express-session";
import passport from "passport";

// Passport configs
import configPassportCore from "./middleware/passport.js";        // <-- thêm file core
import configPassportStudent from "./middleware/passportStudent.js";
import configPassportBusiness from "./middleware/passportBusiness.js";



dotenv.config();

const app = express();

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const sessionSecret = process.env.SESSION_SECRET || process.env.JWT_SECRET;

if (!sessionSecret) {
  throw new Error("SESSION_SECRET or JWT_SECRET must be configured.");
}

// ---------------------- SESSION ----------------------
app.use(
  session({
    secret: sessionSecret,
    resave: false,
    saveUninitialized: false,
    cookie: { maxAge: 1000 * 60 * 60 }, // 1h
  })
);

// ---------------------- PASSPORT ----------------------
// 1) serialize/deserialize (quan trọng)
configPassportCore();

// 2) các strategy cho từng loại user
configPassportStudent();
configPassportBusiness();

// 3) chạy passport middleware
app.use(passport.initialize());
app.use(passport.session());

// ------------------------------------------------------

app.set("view engine", "ejs");
app.set("views", path.join(__dirname, "views"));

app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use(express.static(path.join(__dirname, "../public")));
app.use(cookieParser());

// ROUTES
app.use("/", web_router);
app.use("/business", business_router);
app.use("/student", student_router);

export default app;
