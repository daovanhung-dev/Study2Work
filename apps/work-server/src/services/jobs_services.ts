import prisma from "../config/prisma.config.js";

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
      const jd = await prisma.jD.create({ data });
      console.log("Tạo JD thành công:", jd.id);
      return { success: true, data: jd };
    } catch (err) {
      console.error("Lỗi tạo JD:", err);
      return { success: false, error: "Không thể tạo JD" };
    }
  }

  // Lấy tất cả JD, sắp xếp theo ngày tạo mới nhất
  async getAllJD() {
    try {
      const jds = await prisma.jD.findMany({
        orderBy: { ngay_tao: "desc" }, // sắp xếp theo ngày tạo mới nhất
      });
      return jds;
    } catch (error) {
      console.error("Lỗi khi lấy JD:", error);
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
      include: { DoanhNghiep: true }, // join với doanh nghiệp nếu cần
    });
  };

  // Lấy JD theo ID
  async getJDById(id: number | bigint) {
    try {
      const jd = await prisma.jD.findUnique({ where: { id: BigInt(id) } });
      if (!jd) return { success: false, error: "Không tìm thấy JD" };
      return { success: true, data: jd };
    } catch (err) {
      console.error(err);
      return { success: false, error: "Lỗi server" };
    }
  }


  // Xóa JD
  async deleteJD(id: number | bigint) {
    try {
      await prisma.jD.delete({ where: { id: BigInt(id) } });
      return { success: true };
    } catch (err) {
      console.error(err);
      return { success: false, error: "Không thể xóa JD" };
    }
  }

  //tim theo id doanh nghiep
  async getJDByCompany(doanhnghiep_id: number) {
    try {
      const data = await prisma.jD.findMany({
        where: { doanhnghiep_id: doanhnghiep_id },
        orderBy: { id: "desc" }   // sắp xếp mới nhất trước
      });

      return data;
    } catch (error) {
      console.error("Lỗi lấy JD theo doanh nghiệp:", error);
      throw error;
    }
  }

  async updateJD(id: number, data: any) {
    // Chuyển hạn nộp sang Date nếu có
    if (data.han_nop) {
      data.han_nop = new Date(data.han_nop);
    }

    const updated = await prisma.jD.update({
      where: { id },
      data
    });

    return updated;
  }

}

export default new JDService();
