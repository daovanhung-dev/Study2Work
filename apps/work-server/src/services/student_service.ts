import prisma from "../config/prisma.config.js";
import { studentPublicSelect } from "./public-selectors.js";
import { hashPassword, verifyPassword } from "../utils/password.js";
import { isUniqueConstraintError } from "../utils/prisma-errors.js";

class StudentService {
  // Tạo sinh viên mới
  async insertStudent(
    hoten: string,
    email: string,
    matkhau: string,
    chuyennganh: string,
    avt: string | null
  ) {
    try {
      const passwordHash = await hashPassword(matkhau);
      const student = await prisma.sinhVien.create({
        data: { hoten, email, matkhau: passwordHash, chuyennganh, avt },
        select: studentPublicSelect,
      });
      return { success: true, data: student };
    } catch (err) {
      if (isUniqueConstraintError(err)) return { success: false, error: "DUPLICATE_EMAIL" };
      console.error("Lỗi tạo sinh viên.");
      return { success: false, error: "Không thể tạo sinh viên" };
    }
  }

  // Đăng nhập sinh viên
  async loginStudent(email: string, pass: string) {
    try {
      const user = await prisma.sinhVien.findUnique({
        where: { email },
        select: { id: true, email: true, matkhau: true },
      });

      if (!user) return { success: false };

      const verification = await verifyPassword(pass, user.matkhau);
      if (!verification.valid) return { success: false };

      if (verification.needsRehash) {
        await prisma.sinhVien.update({
          where: { id: user.id },
          data: { matkhau: await hashPassword(pass) },
        }).catch(() => undefined);
      }

      const { matkhau: _matkhau, ...userData } = user;
      return { success: true, data: userData };
    } catch (err) {
      console.error("Lỗi đăng nhập sinh viên.");
      return { success: false, error: "Lỗi server" };
    }
  }

  // Lấy tất cả sinh viên
  async getAllStudents() {
    try {
      const list = await prisma.sinhVien.findMany({
        select: { id: true, hoten: true, email: true, chuyennganh: true, avt: true },
      });
      return { success: true, data: list };
    } catch (err) {
      console.error("Lỗi lấy danh sách sinh viên.");
      return { success: false, error: "Lỗi server" };
    }
  }

  // Lấy sinh viên theo ID
  async getStudentById(id: number | bigint) {
    try {
      const student = await prisma.sinhVien.findUnique({
        where: { id: BigInt(id) },
        select: { id: true, hoten: true, email: true, chuyennganh: true, avt: true },
      });
      if (!student) return { success: false, error: "Không tìm thấy" };
      return { success: true, data: student };
    } catch (err) {
      console.error("Lỗi lấy sinh viên.");
      return { success: false, error: "Lỗi server" };
    }
  }

  // Cập nhật sinh viên
  async updateStudent(
    id: number | bigint,
    data: {
      hoten?: string;
      email?: string;
      matkhau?: string;
      chuyennganh?: string;
      avt?: string;
    }
  ) {
    try {
      const nextData = {
        ...data,
        ...(data.matkhau ? { matkhau: await hashPassword(data.matkhau) } : {}),
      };
      const updated = await prisma.sinhVien.update({
        where: { id: BigInt(id) },
        data: nextData,
        select: studentPublicSelect,
      });
      return { success: true, data: updated };
    } catch (err) {
      console.error("Lỗi cập nhật sinh viên.");
      return { success: false, error: "Không thể cập nhật sinh viên" };
    }
  }

  // Xóa sinh viên
  async deleteStudent(id: number | bigint) {
    try {
      await prisma.sinhVien.delete({ where: { id: BigInt(id) } });
      return { success: true };
    } catch (err) {
      console.error("Lỗi xóa sinh viên.");
      return { success: false, error: "Không thể xóa sinh viên" };
    }
  }
}

export default new StudentService();
