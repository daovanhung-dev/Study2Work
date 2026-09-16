import { Router } from "express";
import * as studentCtrl from "../controllers/student_ctrl.js";
import { ensureAuthenticated, checkRole } from "../middleware/auth.middleware.js";
import jd_ctrl from "../controllers/jd_ctrl.js";
import CVCtrl from "../controllers/cv_ctrl.js";
import cv_ctrl from "../controllers/cv_ctrl.js";
import {upload} from "../config/multer.js";
import candidate_ctrl from "../controllers/candidate_ctrl.js";
const student_router = Router();

student_router.use(ensureAuthenticated, checkRole("student"));
student_router.get("/Home", studentCtrl.student_homeSV);
student_router.get("/Setting", studentCtrl.student_setting);
student_router.get("/Profile", studentCtrl.student_profile);
student_router.get("/Update-Profile", studentCtrl.student_updateProfile);
student_router.get("/CreateCV", studentCtrl.student_createCV);
student_router.get("/UpdateCV", cv_ctrl.getCV);
student_router.get("/PostJobs", studentCtrl.student_posts_jobs);
student_router.get("/Apply", studentCtrl.student_apply);
student_router.get("/Noti", studentCtrl.student_noti);
student_router.get("/Chat", studentCtrl.student_chat);
student_router.get("/TopCV", studentCtrl.student_view_topcv);
student_router.get("/Interview", studentCtrl.student_interview_schedule);
student_router.get("/Logout", studentCtrl.student_logOut);
student_router.get("/JobDescription/:id", jd_ctrl.showDetail);
student_router.get("/CV", CVCtrl.CV);
student_router.get("/Result",candidate_ctrl.ketQuaUngTuyen);

//post
student_router.post("/CreateCV",upload.single("avt"), cv_ctrl.createCV);
student_router.post("/UpdateCV/:id",upload.single("avt"), cv_ctrl.updateCV);
student_router.post("/CandidateJD/:id",candidate_ctrl.CandidateJD);


export default student_router;
