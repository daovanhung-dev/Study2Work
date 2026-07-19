import { Request, Response } from "express"; // import type Express
import path from "path";
import { fileURLToPath } from "url";
import JDService from "../services/jobs_services.js";
import StudentService from "../services/student_service.js";
import student_router from "../routes/student_route.js";
import { Sign } from "crypto";
import { signToken } from "../utils/jwt.js";

import passport from "passport";

const __filename = fileURLToPath(import.meta.url); // lấy đường dẫn file hiện tại
const __dirname = path.dirname(__filename);
// Route Home
export const homePage = async (req: Request, res: Response) => {
  if (req.user && "role" in req.user) {
    const role = req.user.role;
    if (role == "business") {
      return res.redirect("/business/home");
    } else return res.redirect("/student/home");
  }

  const jobs = await JDService.getAllJD();
  return res.render("home", { jobs });
};

// Route Sign In ================================================================================================================================================
export const signInStudentCtrl = (req: Request, res: Response) => {
  res.render("Student/signIn");
};
export const signInBusinessCtrl = (req: Request, res: Response) => {
  const { session } = req as any;

  // Passport lưu lỗi vào session.messages (mảng)
  const errors: string[] = session?.messages ?? [];

  // xóa sau khi lấy để không hiển thị lại lần sau
  if (session?.messages) session.messages = [];
  res.render("Business/signIn", { errors });
};

export const loginStudentCtrl = async (req: Request, res: Response) => {
  console.log("➡️ loginStudentCtrl");

  try {
    const { email, password } = req.body;

    // 1. Kiểm tra input
    if (!email || !password) {
      console.log("❌ Thiếu dữ liệu đầu vào");
      return res.status(400).render("signIn", {
        error: "Email và mật khẩu bắt buộc",
      });
    }

    // 2. Gọi service xử lý đăng nhập
    const result = await StudentService.loginStudent(email, password);

    if (!result || !result.success) {
      console.log("❌ Sai email hoặc mật khẩu");
      return res.render("signIn", {
        error: "Email hoặc mật khẩu sai",
      });
    }

    const student = result.data; // Lấy thông tin sinh viên
    if (!student) {
      console.log("❌ Student không tồn tại sau khi login");
      return res.status(400).render("signIn", {
        error: "Email hoặc mật khẩu sai",
      });
    }

    // 3. Tạo JWT token
    const token = signToken({
      id: Number(student.id), // chuyển BigInt sang Number
      email: student.email || "", // đảm bảo không null
      role: "student", // hoặc lấy từ student.role nếu có
    });

    // 4. Lưu token vào cookie
    res.cookie("jwt", token, {
      httpOnly: true, // cookie không đọc được bởi JS client
      secure: false, // true nếu dùng HTTPS
      maxAge: 7 * 24 * 60 * 60 * 1000, // 7 ngày
    });

    console.log("🎉 Đăng nhập thành công → Token đã lưu vào cookie!");

    // 5. Redirect sang trang chính của sinh viên
    return res.redirect("/student/Home");
  } catch (error) {
    console.error("💥 Lỗi login:", error);
    return res.status(500).render("signIn", {
      error: "Lỗi hệ thống",
    });
  }
};
export const signInRole = (req: Request, res: Response) => {
  res.render("signInRole");
};

// Route Sign Up ================================================================================================================================================
export const signUpStudentCtrl = (req: Request, res: Response) => {
  res.render("Student/signUp");
};
export const signUpBusinessCtrl = (req: Request, res: Response) => {
  res.render("Business/signUp");
};
export const signUpRole = (req: Request, res: Response) => {
  res.render("signUpRole");
};

//create
export const createStudent = async (req: Request, res: Response) => {
  try {
    const { hoten, email, matkhau, chuyennganh } = req.body;
    const avt = req.file ? req.file.filename : null;

    if (!hoten || !email || !matkhau) {
      return res.status(400).send("Họ tên, email và mật khẩu bắt buộc");
    }
    console.log("create user");
    await StudentService.insertStudent(
      hoten,
      email,
      matkhau,
      chuyennganh || null,
      avt
    );

    return res.send(
      `<script>alert("Bạn đã tạo tài khoản thành công!"); window.location.href="/";</script>`
    );
  } catch (err: any) {
    res.status(500).send(err.message);
  }
};

//coming-soon
export const comingSoon = (req: Request, res: Response) => {
  res.render("coming-soon");
};

//error role
export const errorRole = (req: Request, res: Response) => {
  res.render("errorRole");
};
