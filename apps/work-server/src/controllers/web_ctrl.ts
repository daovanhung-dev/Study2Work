import { Request, Response } from "express";
import JDService from "../services/jobs_services.js";
import StudentService from "../services/student_service.js";
import BusinessService from "../services/business_services.js";
import { signToken } from "../utils/jwt.js";

// Route Home
export const homePage = async (req: Request, res: Response) => {
  if (req.user && "role" in req.user) {
    const role = req.user.role;
    if (role === "business") {
      return res.redirect("/business/home");
    }
    return res.redirect("/student/home");
  }

  const jobs = await JDService.getAllJD();
  return res.render("home", { jobs });
};

// Route Sign In
export const signInStudentCtrl = (_req: Request, res: Response) => {
  res.render("Student/signIn", { errors: [] });
};

export const signInBusinessCtrl = (_req: Request, res: Response) => {
  res.render("Business/signIn", { errors: [] });
};

export const loginStudentCtrl = async (req: Request, res: Response) => {
  try {
    const { email, matkhau, password } = req.body as {
      email?: string;
      matkhau?: string;
      password?: string;
    };
    const loginPassword = matkhau ?? password;

    if (!email || !loginPassword) {
      return res.status(400).json({ error: "EMAIL_AND_PASSWORD_REQUIRED" });
    }

    const result = await StudentService.loginStudent(email, loginPassword);
    if (!result || !result.success || !result.data) {
      return res.status(401).json({ error: "INVALID_CREDENTIALS" });
    }

    const student = result.data;
    const user = {
      id: Number(student.id),
      email: student.email || "",
      role: "student" as const,
    };

    return res.json({ token: signToken(user), user });
  } catch (error) {
    console.error("Student login error:", error);
    return res.status(500).json({ error: "INTERNAL_SERVER_ERROR" });
  }
};

export const loginBusinessCtrl = async (req: Request, res: Response) => {
  try {
    const { email, matkhau, password } = req.body as {
      email?: string;
      matkhau?: string;
      password?: string;
    };
    const loginPassword = matkhau ?? password;

    if (!email || !loginPassword) {
      return res.status(400).json({ error: "EMAIL_AND_PASSWORD_REQUIRED" });
    }

    const result = await BusinessService.loginDoanhNghiep(email, loginPassword);
    if (!result || !result.success || !result.data) {
      return res.status(401).json({ error: "INVALID_CREDENTIALS" });
    }

    const business = result.data;
    const user = {
      id: Number(business.id),
      email: business.email || "",
      role: "business" as const,
    };

    return res.json({ token: signToken(user), user });
  } catch (error) {
    console.error("Business login error:", error);
    return res.status(500).json({ error: "INTERNAL_SERVER_ERROR" });
  }
};

export const signInRole = (_req: Request, res: Response) => {
  res.render("signInRole");
};

// Route Sign Up
export const signUpStudentCtrl = (_req: Request, res: Response) => {
  res.render("Student/signUp");
};

export const signUpBusinessCtrl = (_req: Request, res: Response) => {
  res.render("Business/signUp");
};

export const signUpRole = (_req: Request, res: Response) => {
  res.render("signUpRole");
};

export const createStudent = async (req: Request, res: Response) => {
  try {
    const { hoten, email, matkhau, chuyennganh } = req.body;
    const avt = req.file ? req.file.filename : null;

    if (!hoten || !email || !matkhau) {
      return res.status(400).send("Họ tên, email và mật khẩu bắt buộc");
    }

    await StudentService.insertStudent(
      hoten,
      email,
      matkhau,
      chuyennganh || null,
      avt
    );

    return res.json({
      message: "Bạn đã tạo tài khoản thành công!",
      redirect: "/",
    });
  } catch (err: any) {
    return res.status(500).send(err.message);
  }
};

export const comingSoon = (_req: Request, res: Response) => {
  res.render("coming-soon");
};

export const errorRole = (_req: Request, res: Response) => {
  res.render("errorRole");
};
