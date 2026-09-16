// src/controllers/business_ctrl.ts

import { Request, Response } from "express";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

/* ===========================
   2. Trang cài đặt doanh nghiệp
=========================== */
export const business_setting = (req: Request, res: Response) => {
  res.render("Business/business_setting");
};

/* ===========================
   3. Trang cập nhật thông tin doanh nghiệp
=========================== */
export const business_update_information = (req: Request, res: Response) => {
  res.render("Business/business_update_information");
};

export const business_update_information_post = (
  req: Request,
  res: Response
) => {
  console.log("Update info:", req.body);
  res.redirect("/Business/Setting");
};

/* ===========================
   4. Trang đăng tin tuyển dụng
=========================== */
export const business_post_job = (req: Request, res: Response) => {
  res.render("Business/business_post_job");
};

export const business_post_job_post = (req: Request, res: Response) => {
  console.log("Job posted:", req.body);
  res.redirect("/Business/PostJob");
};

/* ===========================
   5. Danh sách ứng viên đã apply
=========================== */
export const business_apply_list = (req: Request, res: Response) => {
  res.render("Business/business_apply_list");
};

/* ===========================
   6. Sửa thông tin ứng viên đã apply
=========================== */
export const business_edit_info_apply = (req: Request, res: Response) => {
  res.render("Business/business_edit_Info_apply");
};

export const business_edit_info_apply_post = (req: Request, res: Response) => {
  console.log("Update applicant:", req.body);
  res.redirect("/Business/ApplyList");
};

/* ===========================
   7. Kết nối với nhà trường
=========================== */
export const business_link_with_university = (req: Request, res: Response) => {
  res.render("Business/business_link_with_university");
};

/* ===========================
   8. Trang thông báo
=========================== */
export const business_notification = (req: Request, res: Response) => {
  res.render("Business/business_notification");
};

/* ===========================
   9. Trang chat với ứng viên / trường
=========================== */
export const business_chat = (req: Request, res: Response) => {
  res.render("Business/business_chat");
};

/* ===========================
   10. Trang Home doanh nghiệp
=========================== */
export const business_home = (req: Request, res: Response) => {
  if (req.user && "role" in req.user) {
    const role = req.user.role;
    console.log(role);
  }
  res.render("Business/business_home");
};

export const business_logOut = (req: Request, res: Response) => {
  req.logout({ keepSessionInfo: false }, (err) => {
    if (err) {
      console.error("Logout error:", err);
      return res.status(500).send("Lỗi khi logout");
    }
    // Redirect về trang chính
    res.redirect("/");
  });
};
