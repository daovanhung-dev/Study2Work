import express from "express";
import path from "path";
import { fileURLToPath } from "url";

import student_router from "./routes/student_route.js";
import business_router from "./routes/business_route.js";
import web_router from "./routes/web_routes.js";
import { env } from "./config/env.js";
import { errorHandler } from "./middleware/error.middleware.js";

import cookieParser from "cookie-parser";
import session from "express-session";
import passport from "passport";

// Passport configs
import configPassportCore from "./middleware/passport.js";        // <-- thêm file core
import configPassportStudent from "./middleware/passportStudent.js";
import configPassportBusiness from "./middleware/passportBusiness.js";

const app = express();

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// ---------------------- SESSION ----------------------
app.use(
  session({
    secret: env.sessionSecret,
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
app.use(errorHandler);

export default app;
