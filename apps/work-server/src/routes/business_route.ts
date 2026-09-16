// src/routes/business_route.ts
import { Router } from "express";
import * as businessCtrl from "../controllers/business_ctrl.js";
import { ensureAuthenticated, checkRole } from "../middleware/auth.middleware.js";
import JDController from "../controllers/jd_ctrl.js";
import {upload} from "../config/multer.js";
import UngVienController from "../controllers/candidate_ctrl.js";
import CVCtrl from "../controllers/cv_ctrl.js";


const business_router = Router();

/* ---------------------------- BUSINESS ROUTES ---------------------------- */

business_router.use(ensureAuthenticated, checkRole("business"));
// Trang chính
business_router.get("/Home", businessCtrl.business_home);

// Cài đặt doanh nghiệp
business_router.get("/Setting", businessCtrl.business_setting);

// Update thông tin doanh nghiệp
business_router
  .route("/UpdateInformation")
  .get(businessCtrl.business_update_information)
  .post(businessCtrl.business_update_information_post);

// Quản lý tin tuyển dụng
business_router
  .route("/PostJob")
  .get(businessCtrl.business_post_job);

// Danh sách ứng viên apply
business_router.get("/ApplyList", UngVienController.showCandidate);

// Chỉnh sửa thông tin ứng viên
business_router
  .route("/EditInfoApply")
  .get(businessCtrl.business_edit_info_apply)
  .post(businessCtrl.business_edit_info_apply_post);

// Kết nối với trường đại học
business_router.get(
  "/LinkUniversity",
  businessCtrl.business_link_with_university
);

business_router.get("/Notification", businessCtrl.business_notification);

// Tin nhắn
business_router.get("/Chat", businessCtrl.business_chat);

business_router.get("/ManganerJD", JDController.manageJD);

//xoa jd
business_router.get("/DeleteJD/:id", JDController.deleteJD);

//update jd
business_router.get("/UpdateJD/:id", JDController.showUpdatePage);

business_router.get("/Logout", businessCtrl.business_logOut);


/* ------------------------------------------------------------------------ */

//post
business_router.post("/PostJob", upload.single('avt'),JDController.PostJOB);
business_router.post("/UpdateJD/:id", JDController.updateJD);
business_router.get("/CVDetail/:id", CVCtrl.detail);

export default business_router;
