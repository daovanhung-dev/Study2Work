import prisma from "../config/prisma.config.js";
import { hashPassword, verifyPassword } from "../utils/password.js";
import { isUniqueConstraintError } from "../utils/prisma-errors.js";
import { businessPublicSelect } from "./public-selectors.js";

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
      const passwordHash = await hashPassword(matkhau);
      const doanhNghiep = await prisma.doanhNghiep.create({
        data: {
          hoten,
          email,
          matkhau: passwordHash,
          diachi,
          sodienthoai,
          avt,
        },
        select: businessPublicSelect,
      });
      return { success: true, data: doanhNghiep };
    } catch (err) {
      if (isUniqueConstraintError(err)) return { success: false, error: "DUPLICATE_EMAIL" };
      console.error("Lỗi tạo doanh nghiệp.");
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

      if (!doanhNghiep) return { success: false };

      const verification = await verifyPassword(matkhau, doanhNghiep.matkhau);
      if (!verification.valid) return { success: false };

      if (verification.needsRehash) {
        await prisma.doanhNghiep.update({
          where: { id: doanhNghiep.id },
          data: { matkhau: await hashPassword(matkhau) },
        }).catch(() => undefined);
      }

      const { matkhau: _matkhau, ...data } = doanhNghiep;
      return { success: true, data };
    } catch (err) {
      console.error("Lỗi đăng nhập doanh nghiệp.");
      return { success: false, error: "Lỗi server" };
    }
  }

  // Lấy tất cả doanh nghiệp
  async getAllDoanhNghiep() {
    try {
      const list = await prisma.doanhNghiep.findMany({ select: businessPublicSelect });
      return { success: true, data: list };
    } catch (err) {
      console.error("Lỗi lấy danh sách doanh nghiệp.");
      return { success: false, error: "Lỗi server" };
    }
  }

  // Lấy doanh nghiệp theo id
  async getDoanhNghiepById(id: bigint | number) {
    try {
      const doanhNghiep = await prisma.doanhNghiep.findUnique({
        where: { id: BigInt(id) },
        select: businessPublicSelect,
      });
      if (!doanhNghiep) return { success: false, error: "Không tìm thấy" };
      return { success: true, data: doanhNghiep };
    } catch (err) {
      console.error("Lỗi lấy doanh nghiệp.");
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
      const nextData = {
        ...data,
        ...(data.matkhau ? { matkhau: await hashPassword(data.matkhau) } : {}),
      };
      const updated = await prisma.doanhNghiep.update({
        where: { id: BigInt(id) },
        data: nextData,
        select: businessPublicSelect,
      });
      return { success: true, data: updated };
    } catch (err) {
      console.error("Lỗi cập nhật doanh nghiệp.");
      return { success: false, error: "Không thể cập nhật" };
    }
  }

  // Xóa doanh nghiệp
  async deleteDoanhNghiep(id: bigint | number) {
    try {
      await prisma.doanhNghiep.delete({ where: { id: BigInt(id) } });
      return { success: true };
    } catch (err) {
      console.error("Lỗi xóa doanh nghiệp.");
      return { success: false, error: "Không thể xóa" };
    }
  }
}

export default new DoanhNghiepService();
