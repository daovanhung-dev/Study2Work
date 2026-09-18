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
import { isUniqueConstraintError } from "../utils/prisma-errors.js";

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
  if (typeof value !== "string" || !/^\d+$/.test(value) || value === "0") return null;
  const result = Number(value);
  return Number.isSafeInteger(result) && result > 0 ? result : null;
}

function textValue(value: unknown): string | undefined {
  return typeof value === "string" ? value.trim() : undefined;
}

function requestBody(req: Request): Record<string, unknown> {
  return typeof req.body === "object" && req.body !== null && !Array.isArray(req.body)
    ? req.body as Record<string, unknown>
    : {};
}

function isValidEmail(value: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
}

function positiveIntegerQuery(value: unknown, fallback: number, maximum?: number): number | null {
  if (value === undefined) return fallback;
  if (typeof value !== "string" || !/^\d+$/.test(value)) return null;
  const parsed = Number(value);
  if (!Number.isSafeInteger(parsed) || parsed < 1) return null;
  if (maximum !== undefined && parsed > maximum) return null;
  return parsed;
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

function cvData(body: Record<string, unknown>, fileName?: string): { data?: Record<string, unknown>; error?: string } {
  const data: Record<string, unknown> = {};
  for (const field of cvFieldNames) {
    if (body[field] !== undefined) data[field] = body[field];
  }
  if (body.ngaysinh) {
    const parsedDate = new Date(String(body.ngaysinh));
    if (Number.isNaN(parsedDate.getTime())) return { error: "Ngày sinh không hợp lệ." };
    data.ngaysinh = parsedDate;
  } else if ("ngaysinh" in body) data.ngaysinh = null;
  if (body.social !== undefined) data.social = parseSocial(body.social);
  if (fileName) data.avt = fileName;
  return { data };
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
    if (body[field] !== undefined) {
      data[field] = typeof body[field] === "string" ? body[field].trim() : body[field];
    }
  }
  if (fileName) data.avt = `/uploads/${fileName}`;
  return data;
}

function validateCvData(data: Record<string, unknown>, partial: boolean): string | null {
  if (!partial || data.hoten !== undefined) {
    if (!textValue(data.hoten)) return "Họ tên CV bắt buộc.";
  }
  if (!partial || data.email !== undefined) {
    const email = textValue(data.email);
    if (!email) return "Email CV bắt buộc.";
    if (!isValidEmail(email)) return "Email CV không hợp lệ.";
  }
  if (data.hoten !== undefined) data.hoten = textValue(data.hoten);
  if (data.email !== undefined) data.email = textValue(data.email);
  return null;
}

async function loginStudent(req: Request, res: Response) {
  try {
    const body = requestBody(req);
    const normalizedEmail = textValue(body.email);
    const loginPassword = typeof body.password === "string"
      ? body.password
      : typeof body.matkhau === "string" ? body.matkhau : undefined;
    if (!normalizedEmail || !loginPassword) return badRequest(req, res, "Email và mật khẩu bắt buộc.");
    if (!isValidEmail(normalizedEmail)) return badRequest(req, res, "Email không hợp lệ.");

    const result = await StudentService.loginStudent(normalizedEmail, loginPassword);
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
    const body = requestBody(req);
    const normalizedEmail = textValue(body.email);
    const loginPassword = typeof body.password === "string"
      ? body.password
      : typeof body.matkhau === "string" ? body.matkhau : undefined;
    if (!normalizedEmail || !loginPassword) return badRequest(req, res, "Email và mật khẩu bắt buộc.");
    if (!isValidEmail(normalizedEmail)) return badRequest(req, res, "Email không hợp lệ.");

    const result = await BusinessService.loginDoanhNghiep(normalizedEmail, loginPassword);
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
    const body = requestBody(req);
    const normalizedName = textValue(body.hoten);
    const normalizedEmail = textValue(body.email);
    const password = typeof body.matkhau === "string" ? body.matkhau : undefined;
    if (!normalizedName || !normalizedEmail || !password) return badRequest(req, res, "Họ tên, email và mật khẩu bắt buộc.");
    if (!isValidEmail(normalizedEmail)) return badRequest(req, res, "Email không hợp lệ.");
    if (password.length < 6) return badRequest(req, res, "Mật khẩu phải có ít nhất 6 ký tự.");
    const result = await StudentService.insertStudent(
      normalizedName,
      normalizedEmail,
      password,
      textValue(body.chuyennganh) || "",
      req.file?.filename || null,
    );
    if (!result.success) {
      if (result.error === "DUPLICATE_EMAIL") return reply(req, res, 409, "STUDENT_CREATE_FAILED", "Email đã được đăng ký.");
      return serverError(req, res);
    }
    return reply(req, res, 201, "STUDENT_CREATED", "Bạn đã tạo tài khoản thành công.", result.data);
  } catch {
    return serverError(req, res);
  }
}

async function listJobs(req: Request, res: Response) {
  try {
    const page = positiveIntegerQuery(req.query.page, 1);
    const limit = positiveIntegerQuery(req.query.limit, 6, 50);
    if (page === null || limit === null) return badRequest(req, res, "Page hoặc limit không hợp lệ.");
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
  try {
    const user = (req as ApiRequest).user;
    const result = user.role === "student"
      ? await StudentService.getStudentById(user.id)
      : await BusinessService.getDoanhNghiepById(user.id);
    if (!result.success || !result.data) return reply(req, res, 404, "USER_NOT_FOUND", "Không tìm thấy tài khoản.");
    return reply(req, res, 200, "ME_LOADED", "Đã tải thông tin tài khoản.", { ...result.data, role: user.role });
  } catch {
    return serverError(req, res);
  }
}

async function createCv(req: Request, res: Response) {
  const user = (req as ApiRequest).user;
  try {
    const count = await CVService.countCV(user.id);
    if (typeof count !== "number") return serverError(req, res);
    if (count > 0) return reply(req, res, 409, "CV_ALREADY_EXISTS", "Tài khoản đã có CV.");
    const prepared = cvData(requestBody(req), req.file?.filename);
    if (prepared.error || !prepared.data) return badRequest(req, res, prepared.error || "Dữ liệu CV không hợp lệ.");
    const validationError = validateCvData(prepared.data, false);
    if (validationError) return badRequest(req, res, validationError);
    prepared.data.sinhvien_id = user.id;
    const result = await CVService.insertCv(prepared.data as never);
    if (!result.success) {
      if (result.error === "CV_ALREADY_EXISTS") return reply(req, res, 409, "CV_ALREADY_EXISTS", "Tài khoản đã có CV.");
      return serverError(req, res);
    }
    return reply(req, res, 201, "CV_CREATED", "Tạo CV thành công.", result.data);
  } catch {
    return serverError(req, res);
  }
}

async function getMyCv(req: Request, res: Response) {
  try {
    const user = (req as ApiRequest).user;
    const result = await CVService.getCvById(user.id);
    if (!result.success || !result.data) return reply(req, res, 404, "CV_NOT_FOUND", "Chưa tìm thấy CV.");
    return reply(req, res, 200, "CV_LOADED", "Đã tải CV.", result.data);
  } catch {
    return serverError(req, res);
  }
}

async function updateCv(req: Request, res: Response) {
  const user = (req as ApiRequest).user;
  const cvId = numericParam(req.params.cvId);
  if (cvId === null) return badRequest(req, res, "ID CV không hợp lệ.");
  try {
    const current = await prisma.cv.findFirst({ where: { id: BigInt(cvId), sinhvien_id: BigInt(user.id) } });
    if (!current) return reply(req, res, 404, "CV_NOT_FOUND", "Không tìm thấy CV của tài khoản.");
    const prepared = cvData(requestBody(req), req.file?.filename);
    if (prepared.error || !prepared.data) return badRequest(req, res, prepared.error || "Dữ liệu CV không hợp lệ.");
    const validationError = validateCvData(prepared.data, true);
    if (validationError) return badRequest(req, res, validationError);
    if (Object.keys(prepared.data).length === 0) return badRequest(req, res, "Cần ít nhất một trường để cập nhật CV.");
    const result = await CVService.updateCv(cvId, prepared.data as never);
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
    if (!Number.isSafeInteger(businessId) || businessId < 1) return serverError(req, res);
    const count = await CandidateService.count(user.id, businessId, jobId);
    if (typeof count !== "number") return serverError(req, res);
    if (count > 0) return reply(req, res, 409, "APPLICATION_ALREADY_EXISTS", "Bạn đã ứng tuyển vị trí này rồi.");
    const application = await CandidateService.create(user.id, businessId, jobId);
    return reply(req, res, 201, "APPLICATION_CREATED", "Ứng tuyển thành công.", application);
  } catch (error) {
    if (isUniqueConstraintError(error)) return reply(req, res, 409, "APPLICATION_ALREADY_EXISTS", "Bạn đã ứng tuyển vị trí này rồi.");
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
    const data = jdData(requestBody(req), req.file?.filename);
    if (!textValue(data.ten_vi_tri) || !textValue(data.dia_diem)) return badRequest(req, res, "Tên vị trí và địa điểm bắt buộc.");
    const business = await BusinessService.getDoanhNghiepById(user.id);
    if (!business.success || !business.data) return reply(req, res, 404, "USER_NOT_FOUND", "Không tìm thấy tài khoản doanh nghiệp.");
    data.doanhnghiep_id = user.id;
    if (!data.ten_cong_ty) data.ten_cong_ty = business.data.hoten || undefined;
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
    const data = jdData(requestBody(req), req.file?.filename);
    if (Object.keys(data).length === 0) return badRequest(req, res, "Cần ít nhất một trường để cập nhật tin tuyển dụng.");
    const result = await JDService.updateJD(jobId, data as never);
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
  try {
    const studentId = numericParam(req.params.studentId);
    if (studentId === null) return badRequest(req, res, "ID sinh viên không hợp lệ.");
    const result = await CVService.getCvById(studentId);
    if (!result.success || !result.data) return reply(req, res, 404, "CV_NOT_FOUND", "Không tìm thấy CV.");
    return reply(req, res, 200, "CV_LOADED", "Đã tải CV ứng viên.", result.data);
  } catch {
    return serverError(req, res);
  }
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
