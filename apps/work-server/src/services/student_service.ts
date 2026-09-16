import prisma from "../config/prisma.config.js";

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
      const student = await prisma.sinhVien.create({
        data: { hoten, email, matkhau, chuyennganh, avt },
      });
      console.log("Tạo sinh viên thành công:", student.id);
      return { success: true, data: student };
    } catch (err) {
      console.error("Lỗi tạo sinh viên:", err);
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

      if (!user) {
        console.log("Không tồn tại");
        return { success: false };
      }

      if (user.matkhau !== pass) {
        console.log("Mật khẩu sai");
        return { success: false };
      }

      const { matkhau, ...userData } = user;
      console.log("Đăng nhập thành công:", userData.id, userData.email);
      return { success: true, data: userData };
    } catch (err) {
      console.error(err);
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
      console.error(err);
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
      console.error(err);
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
      const updated = await prisma.sinhVien.update({
        where: { id: BigInt(id) },
        data,
      });
      return { success: true, data: updated };
    } catch (err) {
      console.error(err);
      return { success: false, error: "Không thể cập nhật sinh viên" };
    }
  }

  // Xóa sinh viên
  async deleteStudent(id: number | bigint) {
    try {
      await prisma.sinhVien.delete({ where: { id: BigInt(id) } });
      return { success: true };
    } catch (err) {
      console.error(err);
      return { success: false, error: "Không thể xóa sinh viên" };
    }
  }
}

export default new StudentService();
