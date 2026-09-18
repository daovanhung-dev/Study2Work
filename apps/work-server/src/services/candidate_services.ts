// services/ungvien_service.ts
import prisma from "../config/prisma.config.js";
import { businessPublicSelect, jobPublicSelect, studentPublicSelect } from "./public-selectors.js";

class CandidateService {
  /**
   * Tạo mới một ứng viên
   * @param sinhvien_id ID sinh viên from the authenticated JWT principal
   * @param doanhnghiep_id ID doanh nghiệp
   */
  async create(sinhvien_id: number, doanhnghiep_id: number, jd_id?: number) {
    const newUngVien = await prisma.ungVien.create({
      data: {
        sinhvien_id: BigInt(sinhvien_id),
        doanhnghiep_id: BigInt(doanhnghiep_id),
        ...(jd_id === undefined ? {} : { jd_id: BigInt(jd_id) }),
        // trangthai và created_at dùng default value trong model
      },
      include: {
        JD: { select: jobPublicSelect },
      },
    });
    return newUngVien;
  }

  //kiem tra ton tai
  async count(studentID: number, businessID: number, jdID?: number) {
    try {
      const total = await prisma.ungVien.count({
        where: {
          sinhvien_id: BigInt(studentID),
          doanhnghiep_id: BigInt(businessID),
          ...(jdID === undefined ? {} : { jd_id: BigInt(jdID) }),
        },
      });
      return total;
    } catch (err) {
      return { success: false, error: "Lỗi server" };
    }
  }

  //lay ung vien theo id doanh nghiep
  async getStudentIdByBusinessId(businessID: number) {
    return prisma.ungVien.findMany({
      where: {
        doanhnghiep_id: BigInt(businessID),
      },
      include: {
        SinhVien: { select: studentPublicSelect },
        JD: { select: jobPublicSelect },
      },
    });
  }

  async getKetQuaUngTuyen(sinhvien_id: number) {
    return prisma.ungVien.findMany({
      where: { sinhvien_id: BigInt(sinhvien_id) },
      include: {
        JD: { select: jobPublicSelect },
        DoanhNghiep: { select: businessPublicSelect },
      },
      orderBy: { created_at: "desc" },
    });
  }
}

export default new CandidateService();
