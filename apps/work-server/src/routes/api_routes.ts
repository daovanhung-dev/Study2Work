import { Router, type Request, type Response } from "express";
import { randomUUID } from "node:crypto";

import { upload } from "../config/multer.js";
import CandidateService from "../services/candidate_services.js";
import BusinessService from "../services/business_services.js";
import CVService from "../services/cv_services.js";
import JDService from "../services/jobs_services.js";
import StudentService from "../services/student_service.js";
import prisma from "../config/prisma.config.js";
import { ensureAuthenticated, checkRole } from "../middleware/auth.middleware.js";
import { signToken } from "../utils/jwt.js";

const api_router = Router();

type ApiRequest = Request & {
  user: { id: number; email: string; role: string };
};

function traceId(req: Request): string {
  return req.get("X-Trace-Id") || randomUUID();
}

function jsonSafe(value: unknown): unknown {
  if (typeof value === "bigint") return Number(value);
  if (value instanceof Date) return value.toISOString();
  if (Array.isArray(value)) return value.map(jsonSafe);
  if (typeof value === "object" && value !== null) {
    return Object.fromEntries(
      Object.entries(value).map(([key, child]) => [key, jsonSafe(child)]),
    );
  }
  return value;
}

function reply(
  req: Request,
  res: Response,
  status: number,
  businessCode: string,
  message: string,
  data: unknown = null,
  meta: Record<string, unknown> = {},
) {
  const id = traceId(req);
  res.setHeader("X-Trace-Id", id);
  return res.status(status).json({
    success: status < 400,
    businessCode,
    message,
    data: status < 400 ? jsonSafe(data) : null,
    meta,
    traceId: id,
  });
}

function badRequest(req: Request, res: Response, message: string) {
  return reply(req, res, 400, "INVALID_REQUEST", message);
}

function serverError(req: Request, res: Response) {
  return reply(req, res, 500, "INTERNAL_SERVER_ERROR", "Lỗi máy chủ.");
}

function numericParam(value: string | string[] | undefined): number | null {
  if (typeof value !== "string" || !/^\d+$/.test(value)) return null;
  const result = Number(value);
  return Number.isSafeInteger(result) ? result : null;
}

function parseSocial(value: unknown): unknown {
  if (typeof value !== "string" || !value.trim()) return undefined;
  try {
    return JSON.parse(value);
  } catch {
    return value;
  }
}

const cvFieldNames = [
  "hoten", "ngaysinh", "gioitinh", "email", "sdt", "diachi", "vitri", "nganh",
  "muctieunghiep", "hocvan", "kinhnghiem", "kynang", "ngoaingu", "chungchi",
  "duan", "giaithuong", "hoatdong", "portfolio", "luongmongmuon",
] as const;

function cvData(body: Record<string, unknown>, fileName?: string) {
  const data: Record<string, unknown> = {};
  for (const field of cvFieldNames) {
    if (body[field] !== undefined) data[field] = body[field];
  }
  if (body.ngaysinh) data.ngaysinh = new Date(String(body.ngaysinh));
  else if ("ngaysinh" in body) data.ngaysinh = null;
  if (body.social !== undefined) data.social = parseSocial(body.social);
  if (fileName) data.avt = fileName;
  return data;
}

const jdFieldNames = [
  "ten_vi_tri", "phong_ban", "cap_bac", "bao_cao_cho", "nhiem_vu", "trinh_do",
  "kinh_nghiem", "ky_nang", "ky_nang_mem", "uu_tien", "muc_luong", "phuc_loi",
  "moi_truong", "dia_diem", "thoi_gian", "han_nop", "cach_ung_tuyen", "mo_ta",
  "ten_cong_ty", "nganh",
] as const;

function jdData(body: Record<string, unknown>, fileName?: string) {
  const data: Record<string, unknown> = {};
  for (const field of jdFieldNames) {
    if (body[field] !== undefined) data[field] = body[field];
  }
  if (fileName) data.avt = `/uploads/${fileName}`;
  return data;
}

async function loginStudent(req: Request, res: Response) {
  try {
    const { email, matkhau, password } = req.body as { email?: string; matkhau?: string; password?: string };
    const loginPassword = matkhau ?? password;
    if (!email || !loginPassword) return badRequest(req, res, "Email và mật khẩu bắt buộc.");

    const result = await StudentService.loginStudent(email, loginPassword);
    if (!result.success || !result.data) {
      return reply(req, res, 401, "INVALID_CREDENTIALS", "Email hoặc mật khẩu không đúng.");
    }

    const user = { id: Number(result.data.id), email: result.data.email || "", role: "student" };
    return reply(req, res, 200, "AUTH_LOGIN_SUCCESS", "Đăng nhập thành công.", {
      token: signToken(user),
      user,
    });
  } catch {
    return serverError(req, res);
  }
}

async function loginBusiness(req: Request, res: Response) {
  try {
    const { email, matkhau, password } = req.body as { email?: string; matkhau?: string; password?: string };
    const loginPassword = matkhau ?? password;
    if (!email || !loginPassword) return badRequest(req, res, "Email và mật khẩu bắt buộc.");

    const result = await BusinessService.loginDoanhNghiep(email, loginPassword);
    if (!result.success || !result.data) {
      return reply(req, res, 401, "INVALID_CREDENTIALS", "Email hoặc mật khẩu không đúng.");
    }

    const user = { id: Number(result.data.id), email: result.data.email || "", role: "business" };
    return reply(req, res, 200, "AUTH_LOGIN_SUCCESS", "Đăng nhập thành công.", {
      token: signToken(user),
      user,
    });
  } catch {
    return serverError(req, res);
  }
}

async function registerStudent(req: Request, res: Response) {
  try {
    const { hoten, email, matkhau, chuyennganh } = req.body as Record<string, string | undefined>;
    if (!hoten || !email || !matkhau) return badRequest(req, res, "Họ tên, email và mật khẩu bắt buộc.");
    const result = await StudentService.insertStudent(
      hoten,
      email,
      matkhau,
      chuyennganh || "",
      req.file?.filename || null,
    );
    if (!result.success) return reply(req, res, 409, "STUDENT_CREATE_FAILED", result.error || "Không thể tạo sinh viên.");
    return reply(req, res, 201, "STUDENT_CREATED", "Bạn đã tạo tài khoản thành công.", result.data);
  } catch {
    return serverError(req, res);
  }
}

async function listJobs(req: Request, res: Response) {
  try {
    const requestedPage = Number(req.query.page || 1);
    const requestedLimit = Number(req.query.limit || 6);
    const page = Number.isInteger(requestedPage) && requestedPage > 0 ? requestedPage : 1;
    const limit = Number.isInteger(requestedLimit) && requestedLimit > 0 && requestedLimit <= 50 ? requestedLimit : 6;
    const allJobs = await JDService.getAllJD();
    const total = allJobs.length;
    const items = allJobs.slice((page - 1) * limit, page * limit);
    return reply(req, res, 200, "JOBS_LOADED", "Đã tải danh sách việc làm.", items, {
      page,
      limit,
      total,
      totalPages: Math.ceil(total / limit),
    });
  } catch {
    return serverError(req, res);
  }
}

async function getJob(req: Request, res: Response) {
  try {
    const id = numericParam(req.params.id);
    if (id === null) return badRequest(req, res, "ID việc làm không hợp lệ.");
    const result = await JDService.getJDById(id);
    if (!result.success) return reply(req, res, 404, "JOB_NOT_FOUND", result.error || "Không tìm thấy việc làm.");
    return reply(req, res, 200, "JOB_LOADED", "Đã tải chi tiết việc làm.", result.data);
  } catch {
    return serverError(req, res);
  }
}

async function getMe(req: Request, res: Response) {
  const user = (req as ApiRequest).user;
  const result = user.role === "student"
    ? await StudentService.getStudentById(user.id)
    : await BusinessService.getDoanhNghiepById(user.id);
  if (!result.success || !result.data) return reply(req, res, 404, "USER_NOT_FOUND", "Không tìm thấy tài khoản.");
  return reply(req, res, 200, "ME_LOADED", "Đã tải thông tin tài khoản.", { ...result.data, role: user.role });
}

async function createCv(req: Request, res: Response) {
  const user = (req as ApiRequest).user;
  try {
    const count = await CVService.countCV(user.id);
    if (typeof count !== "number") return serverError(req, res);
    if (count > 0) return reply(req, res, 409, "CV_ALREADY_EXISTS", "Tài khoản đã có CV.");
    const data = cvData(req.body as Record<string, unknown>, req.file?.filename);
    if (!data.hoten || !data.email) return badRequest(req, res, "Họ tên và email CV bắt buộc.");
    data.sinhvien_id = user.id;
    const result = await CVService.insertCv(data as never);
    if (!result.success) return serverError(req, res);
    return reply(req, res, 201, "CV_CREATED", "Tạo CV thành công.", result.data);
  } catch {
    return serverError(req, res);
  }
}

async function getMyCv(req: Request, res: Response) {
  const user = (req as ApiRequest).user;
  const result = await CVService.getCvById(user.id);
  if (!result.success || !result.data) return reply(req, res, 404, "CV_NOT_FOUND", "Chưa tìm thấy CV.");
  return reply(req, res, 200, "CV_LOADED", "Đã tải CV.", result.data);
}

async function updateCv(req: Request, res: Response) {
  const user = (req as ApiRequest).user;
  const cvId = numericParam(req.params.cvId);
  if (cvId === null) return badRequest(req, res, "ID CV không hợp lệ.");
  try {
    const current = await prisma.cv.findFirst({ where: { id: BigInt(cvId), sinhvien_id: BigInt(user.id) } });
    if (!current) return reply(req, res, 404, "CV_NOT_FOUND", "Không tìm thấy CV của tài khoản.");
    const data = cvData(req.body as Record<string, unknown>, req.file?.filename);
    const result = await CVService.updateCv(cvId, data as never);
    if (!result.success) return serverError(req, res);
    return reply(req, res, 200, "CV_UPDATED", "Cập nhật CV thành công.", result.data);
  } catch {
    return serverError(req, res);
  }
}

async function applyToJob(req: Request, res: Response) {
  const user = (req as ApiRequest).user;
  const jobId = numericParam(req.params.jobId);
  if (jobId === null) return badRequest(req, res, "ID việc làm không hợp lệ.");
  try {
    const job = await prisma.jD.findUnique({ where: { id: BigInt(jobId) } });
    if (!job) return reply(req, res, 404, "JOB_NOT_FOUND", "Vị trí ứng tuyển không tồn tại.");
    if (!job.doanhnghiep_id) return badRequest(req, res, "Vị trí chưa gán doanh nghiệp.");
    const businessId = Number(job.doanhnghiep_id);
    const count = await CandidateService.count(user.id, businessId, jobId);
    if (typeof count !== "number") return serverError(req, res);
    if (count > 0) return reply(req, res, 409, "APPLICATION_ALREADY_EXISTS", "Bạn đã ứng tuyển vị trí này rồi.");
    const application = await CandidateService.create(user.id, businessId, jobId);
    return reply(req, res, 201, "APPLICATION_CREATED", "Ứng tuyển thành công.", application);
  } catch {
    return serverError(req, res);
  }
}

async function getStudentApplications(req: Request, res: Response) {
  try {
    const data = await CandidateService.getKetQuaUngTuyen((req as ApiRequest).user.id);
    return reply(req, res, 200, "APPLICATIONS_LOADED", "Đã tải kết quả ứng tuyển.", data);
  } catch {
    return serverError(req, res);
  }
}

async function listBusinessJobs(req: Request, res: Response) {
  try {
    const data = await JDService.getJDByCompany((req as ApiRequest).user.id);
    return reply(req, res, 200, "BUSINESS_JOBS_LOADED", "Đã tải tin tuyển dụng.", data);
  } catch {
    return serverError(req, res);
  }
}

async function createBusinessJob(req: Request, res: Response) {
  try {
    const user = (req as ApiRequest).user;
    const data = jdData(req.body as Record<string, unknown>, req.file?.filename);
    if (!data.ten_vi_tri || !data.dia_diem) return badRequest(req, res, "Tên vị trí và địa điểm bắt buộc.");
    const business = await BusinessService.getDoanhNghiepById(user.id);
    data.doanhnghiep_id = user.id;
    if (!data.ten_cong_ty && business.success && business.data) data.ten_cong_ty = business.data.hoten || undefined;
    const result = await JDService.insertJD(data as never);
    if (!result.success) return serverError(req, res);
    return reply(req, res, 201, "JOB_CREATED", "Tạo tin tuyển dụng thành công.", result.data);
  } catch {
    return serverError(req, res);
  }
}

async function updateBusinessJob(req: Request, res: Response) {
  const jobId = numericParam(req.params.jobId);
  if (jobId === null) return badRequest(req, res, "ID việc làm không hợp lệ.");
  try {
    const owner = await prisma.jD.findFirst({ where: { id: BigInt(jobId), doanhnghiep_id: BigInt((req as ApiRequest).user.id) } });
    if (!owner) return reply(req, res, 404, "JOB_NOT_FOUND", "Không tìm thấy tin tuyển dụng của tài khoản.");
    const data = jdData(req.body as Record<string, unknown>, req.file?.filename);
    const result = await JDService.updateJD(jobId, data);
    return reply(req, res, 200, "JOB_UPDATED", "Cập nhật tin tuyển dụng thành công.", result);
  } catch {
    return serverError(req, res);
  }
}

async function deleteBusinessJob(req: Request, res: Response) {
  const jobId = numericParam(req.params.jobId);
  if (jobId === null) return badRequest(req, res, "ID việc làm không hợp lệ.");
  try {
    const owner = await prisma.jD.findFirst({ where: { id: BigInt(jobId), doanhnghiep_id: BigInt((req as ApiRequest).user.id) } });
    if (!owner) return reply(req, res, 404, "JOB_NOT_FOUND", "Không tìm thấy tin tuyển dụng của tài khoản.");
    await prisma.jD.delete({ where: { id: BigInt(jobId) } });
    return reply(req, res, 200, "JOB_DELETED", "Đã xóa tin tuyển dụng.", { id: jobId });
  } catch {
    return serverError(req, res);
  }
}

async function listBusinessApplications(req: Request, res: Response) {
  try {
    const data = await CandidateService.getStudentIdByBusinessId((req as ApiRequest).user.id);
    return reply(req, res, 200, "BUSINESS_APPLICATIONS_LOADED", "Đã tải danh sách ứng viên.", data);
  } catch {
    return serverError(req, res);
  }
}

async function getStudentCv(req: Request, res: Response) {
  const studentId = numericParam(req.params.studentId);
  if (studentId === null) return badRequest(req, res, "ID sinh viên không hợp lệ.");
  const result = await CVService.getCvById(studentId);
  if (!result.success || !result.data) return reply(req, res, 404, "CV_NOT_FOUND", "Không tìm thấy CV.");
  return reply(req, res, 200, "CV_LOADED", "Đã tải CV ứng viên.", result.data);
}

api_router.post("/auth/student/login", loginStudent);
api_router.post("/auth/business/login", loginBusiness);
api_router.post("/auth/logout", ensureAuthenticated, (req, res) =>
  reply(req, res, 200, "AUTH_LOGOUT_SUCCESS", "Đăng xuất thành công."));
api_router.post("/students", upload.single("avt"), registerStudent);
api_router.get("/jobs", listJobs);
api_router.get("/jobs/:id", getJob);

api_router.use(ensureAuthenticated);
api_router.get("/me", getMe);

api_router.get("/students/me/cv", checkRole("student"), getMyCv);
api_router.post("/students/me/cv", checkRole("student"), upload.single("avt"), createCv);
api_router.put("/students/me/cv/:cvId", checkRole("student"), upload.single("avt"), updateCv);
api_router.get("/students/me/applications", checkRole("student"), getStudentApplications);
api_router.post("/jobs/:jobId/applications", checkRole("student"), applyToJob);

api_router.get("/businesses/me/jobs", checkRole("business"), listBusinessJobs);
api_router.post("/businesses/me/jobs", checkRole("business"), upload.single("avt"), createBusinessJob);
api_router.put("/businesses/me/jobs/:jobId", checkRole("business"), upload.single("avt"), updateBusinessJob);
api_router.delete("/businesses/me/jobs/:jobId", checkRole("business"), deleteBusinessJob);
api_router.get("/businesses/me/applications", checkRole("business"), listBusinessApplications);
api_router.get("/students/:studentId/cv", checkRole("business"), getStudentCv);

export default api_router;
