// src/controllers/student_ctrl.ts
import { Request, Response } from "express";
import JDService from "../services/jobs_services.js";

// Trang chính và các trang render
export const student_homeSV = async (req: Request, res: Response) => {
  if (req.user && "role" in req.user) {
    const role = req.user.role;
    const id = (req.user as any).id; // lấy id từ user
    console.log("Role:", role, " - User ID:", id);
  }
  
  const page = parseInt(req.query.page as string) || 1;
  const limit = 6; // số jobs mỗi trang

  const allJobs = await JDService.getAllJD(); // lấy tất cả công việc
  const totalJobs = allJobs.length; // tổng số job
  const totalPages = Math.ceil(totalJobs / limit); // tổng số trang

  const jobs = allJobs.slice((page - 1) * limit, page * limit); // jobs của trang hiện tại

  // Truyền tất cả biến cần thiết cho EJS
  res.render("Student/student_home", { jobs, page, totalPages, totalJobs });
};

export const student_setting = (req: Request, res: Response) =>
  res.render("Student/student_setting");
export const student_profile = (req: Request, res: Response) =>
  res.render("Student/student_profile");
export const student_updateProfile = (req: Request, res: Response) =>
  res.render("Student/student_update_SV");
export const student_createCV = (req: Request, res: Response) =>
  res.render("Student/student_create_CV");
export const student_updateCV = (req: Request, res: Response) =>
  res.render("Student/student_update_CV");
export const student_posts_jobs = (req: Request, res: Response) =>
  res.render("Student/student_post");
export const student_apply = (req: Request, res: Response) =>
  res.render("Student/student_apply");
export const student_noti = (req: Request, res: Response) =>
  res.render("Student/student_noti");
export const student_chat = (req: Request, res: Response) =>
  res.render("Student/student_chat");
export const student_view_topcv = (req: Request, res: Response) =>
  res.render("Student/student_view_TopCV");
export const student_interview_schedule = (req: Request, res: Response) =>
  res.render("Student/student_interview_schedule");
export const student_signIn = (req: Request, res: Response) => {
  const { session } = req as any;

  // Passport lưu lỗi vào session.messages (mảng)
  const errors: string[] = session?.messages ?? [];

  // xóa sau khi lấy để không hiển thị lại lần sau
  if (session?.messages) session.messages = [];

  res.render("Student/signIn", { errors });
};


// POST xử lý form
export const student_updateProfile_post = (req: Request, res: Response) => {
  console.log("Dữ liệu update:", req.body);
  res.redirect("/student/profile");
};

export const student_createCV_post = (req: Request, res: Response) => {
  console.log("Dữ liệu tạo CV:", req.body);
  res.redirect("/student/create-cv");
};

// Logout
//logout
export const student_logOut = (req: Request, res: Response) => {
  req.logout({ keepSessionInfo: false }, (err) => {
    if (err) {
      console.error("Logout error:", err);
      return res.status(500).send("Lỗi khi logout");
    }
    // Redirect về trang chính
    res.redirect("/");
  });
};
