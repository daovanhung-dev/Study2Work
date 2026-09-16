// services/ungvien_service.ts
import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();

class CandidateService {
  /**
   * Tạo mới một ứng viên
   * @param sinhvien_id ID sinh viên (lấy từ session)
   * @param doanhnghiep_id ID doanh nghiệp
   */
  async create(sinhvien_id: number, doanhnghiep_id: number, jd_id?: number) {
  try {
    const newUngVien = await prisma.ungVien.create({
      data: {
        sinhvien_id,
        doanhnghiep_id,
        jd_id,  // liên kết với JD nếu có
        // trangthai và created_at dùng default value trong model
      },
    });
    return newUngVien;
  } catch (error) {
    console.error("Lỗi khi tạo ứng viên:", error);
    throw error;
  }
}


  //kiem tra ton tai
  async count(studentID: number, businessID: number) {
    try {
      const total = await prisma.ungVien.count({
        where: {
          sinhvien_id: studentID,
          doanhnghiep_id: businessID,
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
        doanhnghiep_id: businessID,
      },
      include: {
        SinhVien: true, // lấy full thông tin sinh viên
        JD: true, // lấy full thông tin Job
      },
    });
  }

  async getKetQuaUngTuyen(sinhvien_id: number) {
    return prisma.ungVien.findMany({
      where: { sinhvien_id },
      include: {
        JD: true, // Lấy tất cả thông tin vị trí
        DoanhNghiep: true, // Lấy thông tin doanh nghiệp
      },
      orderBy: { created_at: "desc" },
    });
  }
}

export default new CandidateService();
