import prisma from "../config/prisma.config.js";
import { isUniqueConstraintError } from "../utils/prisma-errors.js";

class CVService {
  // Tạo CV mới
  async insertCv(data: {
    avt?: string;
    hoten: string;
    ngaysinh?: Date;
    gioitinh?: string;
    email: string;
    sdt?: string;
    diachi?: string;
    vitri?: string;
    nganh?: string;
    muctieunghiep?: string;
    hocvan?: string;
    kinhnghiem?: string;
    kynang?: string;
    ngoaingu?: string;
    chungchi?: string;
    duan?: string;
    giaithuong?: string;
    hoatdong?: string;
    social?: object;
    portfolio?: string;
    luongmongmuon?: string;
    sinhvien_id?: number | bigint;
  }) {
    try {
      const cv = await prisma.cv.create({
        data: {
          ...data,
          ...(data.sinhvien_id === undefined ? {} : { sinhvien_id: BigInt(data.sinhvien_id) }),
        },
      });
      return { success: true, data: cv };
    } catch (err) {
      if (isUniqueConstraintError(err)) return { success: false, error: "CV_ALREADY_EXISTS" };
      console.error("Lỗi tạo CV.");
      return { success: false, error: "Không thể tạo CV" };
    }
  }

  // Lấy tất cả CV
  async getAllCv() {
    try {
      const list = await prisma.cv.findMany();
      return { success: true, data: list };
    } catch (err) {
      console.error("Lỗi lấy danh sách CV.");
      return { success: false, error: "Lỗi server" };
    }
  }

  // Lấy CV theo ID
  async getCvById(id: number | bigint) {
    try {
      const cv = await prisma.cv.findFirst({ where: { sinhvien_id: BigInt(id) } });
      
      if (!cv) return { success: false, error: "Không tìm thấy CV" };
      return { success: true, data: cv };
    } catch (err) {
      console.error("Lỗi lấy CV.");
      return { success: false, error: "Lỗi server" };
    }
  }

  // Cập nhật CV
  async updateCv(
    id: number | bigint,
    data: Partial<{
      avt: string;
      hoten: string;
      ngaysinh: Date;
      gioitinh: string;
      email: string;
      sdt: string;
      diachi: string;
      vitri: string;
      nganh: string;
      muctieunghiep: string;
      hocvan: string;
      kinhnghiem: string;
      kynang: string;
      ngoaingu: string;
      chungchi: string;
      duan: string;
      giaithuong: string;
      hoatdong: string;
      social: object;
      portfolio: string;
      luongmongmuon: string;
      sinhvien_id: number | bigint;
    }>
  ) {
    try {
      const updated = await prisma.cv.update({
        where: { id: BigInt(id) },
        data,
      });

      return { success: true, data: updated };
    } catch (err) {
      console.error("Lỗi cập nhật CV.");
      return { success: false, error: "Không thể cập nhật CV" };
    }
  }

  // Xóa CV
  async deleteCv(id: number | bigint) {
    try {
      await prisma.cv.delete({ where: { id: BigInt(id) } });
      return { success: true };
    } catch (err) {
      console.error("Lỗi xóa CV.");
      return { success: false, error: "Không thể xóa CV" };
    }
  }

  //kiem tra so luong row theo id
  async countCV(student_id: number){
    try {
      const total = await prisma.cv.count(
        {
          where:{
            sinhvien_id: BigInt(student_id)
          }
        }
      );
      return total;
    }
    catch(err){
      return { success: false, error: "Lỗi server" };
    }
  }
}

export default new CVService();
