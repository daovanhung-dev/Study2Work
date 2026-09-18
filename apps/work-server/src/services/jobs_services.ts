import prisma from "../config/prisma.config.js";
import { businessPublicSelect, jobPublicSelect } from "./public-selectors.js";
import type { Prisma } from "@prisma/client";

class JDService {
  // Tạo JD mới
  async insertJD(data: {
    ten_vi_tri: string;
    phong_ban?: string;
    cap_bac?: string;
    bao_cao_cho?: string;
    nhiem_vu?: string;
    trinh_do?: string;
    kinh_nghiem?: string;
    ky_nang?: string;
    ky_nang_mem?: string;
    uu_tien?: string;
    muc_luong?: string;
    phuc_loi?: string;
    moi_truong?: string;
    dia_diem?: string;
    thoi_gian?: string;
    han_nop?: string;
    cach_ung_tuyen?: string;
    mo_ta?: string;
    doanhnghiep_id?: number | bigint;
    ten_cong_ty?: string;
    nganh?: string;
    avt?: string;
  }) {
    try {
      const prismaData = {
        ...data,
        ...(data.doanhnghiep_id === undefined
          ? {}
          : { doanhnghiep_id: BigInt(data.doanhnghiep_id) }),
      };
      const jd = await prisma.jD.create({ data: prismaData, select: jobPublicSelect });
      return { success: true, data: jd };
    } catch (err) {
      console.error("Lỗi tạo JD.");
      return { success: false, error: "Không thể tạo JD" };
    }
  }

  // Lấy tất cả JD, sắp xếp theo ngày tạo mới nhất
  async getAllJD() {
    try {
      const jds = await prisma.jD.findMany({
        orderBy: { ngay_tao: "desc" }, // sắp xếp theo ngày tạo mới nhất
        select: jobPublicSelect,
      });
      return jds;
    } catch (error) {
      console.error("Lỗi khi lấy JD.");
      throw error;
    }
  }

  // Lấy tổng số job
  countJD = async () => {
    return await prisma.jD.count();
  };

  // Lấy jobs phân trang
  getJDWithLimit = async (skip: number, take: number) => {
    return await prisma.jD.findMany({
      skip,
      take,
      include: { DoanhNghiep: { select: businessPublicSelect } }, // join với doanh nghiệp nếu cần
    });
  };

  // Lấy JD theo ID
  async getJDById(id: number | bigint) {
    try {
      const jd = await prisma.jD.findUnique({ where: { id: BigInt(id) }, select: jobPublicSelect });
      if (!jd) return { success: false, error: "Không tìm thấy JD" };
      return { success: true, data: jd };
    } catch (err) {
      console.error("Lỗi lấy JD.");
      return { success: false, error: "Lỗi server" };
    }
  }


  // Xóa JD
  async deleteJD(id: number | bigint) {
    try {
      await prisma.jD.delete({ where: { id: BigInt(id) } });
      return { success: true };
    } catch (err) {
      console.error("Lỗi xóa JD.");
      return { success: false, error: "Không thể xóa JD" };
    }
  }

  //tim theo id doanh nghiep
  async getJDByCompany(doanhnghiep_id: number | bigint) {
    try {
      const data = await prisma.jD.findMany({
        where: { doanhnghiep_id: BigInt(doanhnghiep_id) },
        orderBy: { id: "desc" }, // sắp xếp mới nhất trước
        select: jobPublicSelect,
      });

      return data;
    } catch (error) {
      console.error("Lỗi lấy JD theo doanh nghiệp.");
      throw error;
    }
  }

  async updateJD(id: number | bigint, data: Prisma.JDUpdateInput) {
    const updated = await prisma.jD.update({
      where: { id: BigInt(id) },
      data,
      select: jobPublicSelect,
    });

    return updated;
  }

}

export default new JDService();
