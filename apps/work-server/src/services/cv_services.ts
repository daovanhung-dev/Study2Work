import { request } from "http";
import prisma from "../config/prisma.config.js";
import { Request, Response } from "express";

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
      const cv = await prisma.cv.create({ data });
      console.log("Tạo CV thành công:", cv.id);
      return { success: true, data: cv };
    } catch (err) {
      console.error("Lỗi tạo CV:", err);
      return { success: false, error: "Không thể tạo CV" };
    }
  }

  // Lấy tất cả CV
  async getAllCv() {
    try {
      const list = await prisma.cv.findMany();
      return { success: true, data: list };
    } catch (err) {
      console.error(err);
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
      console.error(err);
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
      console.log("cap nhat cv")
      const updated = await prisma.cv.update({
        where: { id: BigInt(id) },
        data,
      });

      return { success: true, data: updated };
    } catch (err) {
      console.error(err);
      return { success: false, error: "Không thể cập nhật CV" };
    }
  }

  // Xóa CV
  async deleteCv(id: number | bigint) {
    try {
      await prisma.cv.delete({ where: { id: BigInt(id) } });
      return { success: true };
    } catch (err) {
      console.error(err);
      return { success: false, error: "Không thể xóa CV" };
    }
  }

  //kiem tra so luong row theo id
  async countCV(student_id: number){
    try {
      const total = await prisma.cv.count(
        {
          where:{
            sinhvien_id: student_id
          }
        }
      );
      return total;
    }
    catch(err){
      return {success: false, error:"Lỗi server"};
    }
  }
}

export default new CVService();
