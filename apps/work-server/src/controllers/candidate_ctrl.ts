// controllers/ungvien_controller.ts
import { Request, Response } from "express";
import CandidateService from "../services/candidate_services.js";
import CVService from "../services/cv_services.js";
import JDService from "../services/jobs_services.js";
import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();

class UngVienController {
async CandidateJD(req: Request, res: Response) {
    try {
      // Lấy jdId từ params
      const jdID = Number(req.params.jdId); // convert sang number
      if (isNaN(jdID)) {
        return res.send(
          `<script>alert("Vị trí ứng tuyển không hợp lệ!"); window.location.href="/student/home";</script>`
        );
      }

      // Lấy studentID từ session/user
      const studentID = Number((req.user as any).id);

      // Lấy JD để lấy doanhnghiep_id
      const jd = await prisma.jD.findUnique({ where: { id: BigInt(jdID) } });
      if (!jd) {
        return res.send(
          `<script>alert("Vị trí ứng tuyển không tồn tại!"); window.location.href="/student/home";</script>`
        );
      }

      const businessID = jd.doanhnghiep_id ? Number(jd.doanhnghiep_id) : null;
      if (!businessID) {
        return res.send(
          `<script>alert("Vị trí này chưa gán doanh nghiệp!"); window.location.href="/student/home";</script>`
        );
      }

      // Kiểm tra đã ứng tuyển chưa
      const count = await CandidateService.count(studentID, businessID);
      if (count != 0) {
        return res.send(
          `<script>alert("Bạn đã ứng tuyển vị trí này rồi!"); window.location.href="/student/home";</script>`
        );
      }

      // Tạo ứng viên
      await CandidateService.create(studentID, businessID, jdID);
      return res.send(
        `<script>alert("Ứng tuyển thành công!"); window.location.href="/student/home";</script>`
      );
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
      const users = req.user as any; // giả sử session lưu id sinh viên
      const ketqua = await CandidateService.getKetQuaUngTuyen(users.id);
      
      res.render('student/Result', { ketqua });
    } catch (error) {
      console.error(error);
      res.status(500).send('Lỗi server');
    }
  }

}

export default new UngVienController();
