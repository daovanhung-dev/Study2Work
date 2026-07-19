// src/controllers/adminController.ts

import { Request, Response } from "express";

/* ===========================
   1. Trang Home (Dashboard)
=========================== */
export const admin_home = (req: Request, res: Response) => {
  res.render("Admin/admin-home");
};

/* ===========================
   2. Trang Quản lý người dùng
=========================== */
export const admin_users = (req: Request, res: Response) => {
  res.render("Admin/admin-users");
};

/* ===========================
   3. Trang Quản lý Tin tuyển dụng
=========================== */
export const admin_jobs = (req: Request, res: Response) => {
  res.render("Admin/admin-jobs");
};

/* ===========================
   4. Trang Quản lý Ngành học
=========================== */
export const admin_majors = (req: Request, res: Response) => {
  res.render("Admin/admin-majors");
};

/* ===========================
   5. Trang Thống kê
=========================== */
export const admin_stats = (req: Request, res: Response) => {
  res.render("Admin/admin-stats");
};

/* ===========================
   6. Cài đặt hệ thống
=========================== */
export const admin_settings = (req: Request, res: Response) => {
  res.render("Admin/admin-settings");
};
