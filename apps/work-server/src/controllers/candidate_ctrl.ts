// controllers/ungvien_controller.ts
import { Request, Response } from "express";
import CandidateService from "../services/candidate_services.js";
import CVService from "../services/cv_services.js";
import JDService from "../services/jobs_services.js";
import prisma from "../config/prisma.config.js";

class UngVienController {
async CandidateJD(req: Request, res: Response) {
    try {
      // Lấy jdId từ params
      const jdID = Number(req.params.jdId); // convert sang number
      if (isNaN(jdID)) {
        return res.status(400).json({ message: "Vị trí ứng tuyển không hợp lệ!" });
      }

      // Lấy studentID từ JWT principal
      const studentID = Number((req.user as any).id);

      // Lấy JD để lấy doanhnghiep_id
      const jd = await prisma.jD.findUnique({ where: { id: BigInt(jdID) } });
      if (!jd) {
        return res.status(404).json({ message: "Vị trí ứng tuyển không tồn tại!" });
      }

      const businessID = jd.doanhnghiep_id ? Number(jd.doanhnghiep_id) : null;
      if (!businessID) {
        return res.status(400).json({ message: "Vị trí này chưa gán doanh nghiệp!" });
      }

      // Kiểm tra đã ứng tuyển chưa
      const count = await CandidateService.count(studentID, businessID);
      if (count != 0) {
        return res.status(409).json({ message: "Bạn đã ứng tuyển vị trí này rồi!" });
      }

      // Tạo ứng viên
      await CandidateService.create(studentID, businessID, jdID);
      return res.status(201).json({ message: "Ứng tuyển thành công!" });
    } catch (error) {
      console.error("Lỗi tạo ứng viên:", error);
      res.status(500).json({ error: "Lỗi server" });
    }
  }


  async showCandidate(req: Request, res: Response) {
    try {
      const users = req.user as any;
      const businessID = users.id;
      const data = await CandidateService.getStudentIdByBusinessId(businessID);
      if (!data || data.length === 0) {
        return res.render("Business/business_apply_list", {
          title: "Danh sách ứng viên",
          applicants: [],
          message: "Hiện chưa có ứng viên nào ứng tuyển!",
        });
      }
      return res.render("Business/business_apply_list", {
        title: "Danh sách ứng viên",
        applicants: data,
        message: null,
      });
    } catch (err) {
      console.error(err);
      return res.status(500).send("Lỗi server khi lấy danh sách ứng viên");
    }
  }

  async ketQuaUngTuyen(req: Request, res: Response) {
    try {
      const users = req.user as any; // JWT principal chứa id sinh viên
      const ketqua = await CandidateService.getKetQuaUngTuyen(users.id);
      
      res.render('student/Result', { ketqua });
    } catch (error) {
      console.error(error);
      res.status(500).send('Lỗi server');
    }
  }

}

export default new UngVienController();
