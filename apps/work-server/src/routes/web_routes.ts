import { Router } from "express";
import * as web_ctrl from "../controllers/web_ctrl.js";
import multer from "multer"; // import multer
import passport from "passport";
import * as student_ctrl from "../controllers/student_ctrl.js";
const web_router = Router();

// cấu hình multer
const storage = multer.diskStorage({
  destination: (req, file, cb) => cb(null, "uploads/"),
  filename: (req, file, cb) => cb(null, Date.now() + "-" + file.originalname),
});
const upload = multer({ storage }); // tạo upload middleware

// Route cho trang home
web_router.get("/", web_ctrl.homePage);

// Route đăng nhập
web_router.get("/SignInStudent", student_ctrl.student_signIn);
web_router.get("/signInBusiness", web_ctrl.signInBusinessCtrl);
web_router.get("/signInRole", web_ctrl.signInRole);
web_router.post(
  "/signInStudent",
  passport.authenticate("student-local", {
    successRedirect: "/student/home",
    failureRedirect: "/signInStudent",
    failureMessage: true,
  })
);

web_router.post(
  "/signInBusiness",
  passport.authenticate("business-local", {
    successRedirect: "/business/home",
    failureRedirect: "/signInBusiness",
    failureMessage: true,
  })
);

// Route đăng ký
web_router.get("/signUpStudent", web_ctrl.signUpStudentCtrl);
web_router.get("/signUpBusiness", web_ctrl.signUpBusinessCtrl);
web_router.get("/signUpRole", web_ctrl.signUpRole);
web_router.post("/signUpStudent", upload.single("avt"), web_ctrl.createStudent);

// Route coming-soon
web_router.get("/coming-soon", web_ctrl.comingSoon);

//errors
web_router.get("/errorRole", web_ctrl.errorRole);

export default web_router;
