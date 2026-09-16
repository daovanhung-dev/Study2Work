import prisma from "../config/prisma.config.js";

class DoanhNghiepService {
  // Tạo doanh nghiệp mới
  async insertDoanhNghiep(
    hoten: string,
    email: string,
    matkhau: string,
    diachi: string | null,
    sodienthoai: string | null,
    avt: string | null
  ) {
    try {
      const doanhNghiep = await prisma.doanhNghiep.create({
        data: {
          hoten,
          email,
          matkhau,
          diachi,
          sodienthoai,
          avt,
        },
      });
      console.log("Tạo doanh nghiệp thành công:", doanhNghiep.id);
      return { success: true, data: doanhNghiep };
    } catch (err) {
      console.error("Lỗi tạo doanh nghiệp:", err);
      return { success: false, error: "Không thể tạo doanh nghiệp" };
    }
  }

  // Đăng nhập doanh nghiệp
  async loginDoanhNghiep(email: string, matkhau: string) {
    try {
      const doanhNghiep = await prisma.doanhNghiep.findUnique({
        where: { email },
        select: { id: true, email: true, matkhau: true },
      });

      if (!doanhNghiep) {
        console.log("Doanh nghiệp không tồn tại");
        return { success: false };
      }

      if (doanhNghiep.matkhau !== matkhau) {
        console.log("Mật khẩu sai");
        return { success: false };
      }

      const { matkhau: _, ...data } = doanhNghiep;
      console.log("Đăng nhập thành công:", data.id, data.email);

      return { success: true, data };
    } catch (err) {
      console.error("Lỗi login doanh nghiệp:", err);
      return { success: false, error: "Lỗi server" };
    }
  }

  // Lấy tất cả doanh nghiệp
  async getAllDoanhNghiep() {
    try {
      const list = await prisma.doanhNghiep.findMany();
      return { success: true, data: list };
    } catch (err) {
      console.error(err);
      return { success: false, error: "Lỗi server" };
    }
  }

  // Lấy doanh nghiệp theo id
  async getDoanhNghiepById(id: bigint | number) {
    try {
      const doanhNghiep = await prisma.doanhNghiep.findUnique({
        where: { id: BigInt(id) },
      });
      if (!doanhNghiep) return { success: false, error: "Không tìm thấy" };
      return { success: true, data: doanhNghiep };
    } catch (err) {
      console.error(err);
      return { success: false, error: "Lỗi server" };
    }
  }

  // Cập nhật doanh nghiệp
  async updateDoanhNghiep(
    id: bigint | number,
    data: {
      hoten?: string;
      email?: string;
      matkhau?: string;
      diachi?: string;
      sodienthoai?: string;
      avt?: string;
    }
  ) {
    try {
      const updated = await prisma.doanhNghiep.update({
        where: { id: BigInt(id) },
        data,
      });
      return { success: true, data: updated };
    } catch (err) {
      console.error(err);
      return { success: false, error: "Không thể cập nhật" };
    }
  }

  // Xóa doanh nghiệp
  async deleteDoanhNghiep(id: bigint | number) {
    try {
      await prisma.doanhNghiep.delete({ where: { id: BigInt(id) } });
      return { success: true };
    } catch (err) {
      console.error(err);
      return { success: false, error: "Không thể xóa" };
    }
  }
}

export default new DoanhNghiepService();
