// src/controllers/jdController.ts
import { Request, Response } from "express";
import JDService from "../services/jobs_services.js";
import multer from "multer";

// Cấu hình multer để upload ảnh
const storage = multer.memoryStorage(); // lưu tạm trong memory, service sẽ ghi ra file
export const upload = multer({ storage });

class JDController {
  // Hiển thị chi tiết JD
  async showDetail(req: Request, res: Response) {
    try {
      console.log("show Detail");
      const id = Number(req.params.id);
      if (isNaN(id)) return res.status(400).send("ID không hợp lệ");

      const result = await JDService.getJDById(id);
      if (!result.success)
        return res.status(404).render("404", { message: result.error });

      // Render EJS hiển thị chi tiết
      res.render("JD_Descrition", { jd: result.data });
    } catch (err) {
      console.log("error Detail");
      console.error(err);
      res.status(500).send("Lỗi server");
    }
  }

  async PostJOB(req: Request, res: Response) {
    try {
      const data: any = req.body;

      // Validate trường bắt buộc
      if (!data.ten_vi_tri || !data.dia_diem) {
        return res.send(
          `<script>alert("Tên vị trí và Địa điểm không được để trống!"); window.history.back();</script>`
        );
      }

      // Nếu có file, lưu đường dẫn string
      if (req.file) {
        data.avt = "/uploads/" + req.file.filename; // string lưu DB
      } else {
        data.avt = null; // nếu không upload
      }

      if (req.user) {
        data.doanhnghiep_id = BigInt((req.user as any).id);
        data.ten_cong_ty = (req.user as any).ten_cong_ty;
      }

      const result = await JDService.insertJD(data);

      if (result.success)
        return res.send(
          `<script>alert("Tạo Job thành công!"); window.location.href="/";</script>`
        );
      else
        return res.send(
          `<script>alert("Tạo Job thất bại!"); window.history.back();</script>`
        );
    } catch (err) {
      console.error(err);
      return res.send(
        `<script>alert("Lỗi hệ thống!"); window.location.href="/";</script>`
      );
    }
  }
  async manageJD(req: Request, res: Response): Promise<void> {
    try {
      const user = req.user as any;

      if (!user) {
        res.status(401).send("Không xác thực được doanh nghiệp");
        return;
      }

      const doanhnghiep_id = Number(user.id);

      if (isNaN(doanhnghiep_id)) {
        res.status(400).send("ID doanh nghiệp không hợp lệ");
        return;
      }

      const jds = await JDService.getJDByCompany(doanhnghiep_id);

      // ⭐ FIX BIGINT → NUMBER để không lỗi JSON.stringify trong EJS
      const safeJDs = jds.map((jd) => ({
        ...jd,
        id: Number(jd.id),
        doanhnghiep_id: jd.doanhnghiep_id ? Number(jd.doanhnghiep_id) : null,
      }));

      res.render("business/business_manager_job", {
        jds: safeJDs,
        doanhnghiep_id,
      });
    } catch (error) {
      console.error("Lỗi controller manageJD:", error);
      res.status(500).send("Lỗi server");
    }
  }

  async deleteJD(req: Request, res: Response) {
    try {
      const id = Number(req.params.id);
      const result = await JDService.deleteJD(id);

      if (!result)
        return res
          .status(404)
          .send("Không tìm thấy JD hoặc không thuộc doanh nghiệp");

      return res.redirect("/business/ManganerJD");
    } catch (error) {
      console.error(error);
      return res.status(500).send("Lỗi server");
    }
  }

  async updateJD(req: Request, res: Response): Promise<void> {
    try {
      const jd_id = Number(req.params.id);

      if (isNaN(jd_id)) {
        res.status(400).send("ID JD không hợp lệ");
        return;
      }

      const result = await JDService.updateJD(jd_id, req.body);

      res.redirect("/doanhnghiep/manage-jd");
    } catch (error) {
      console.error("Lỗi updateJD:", error);
      res.status(500).send("Lỗi server");
    }
  }

  async showUpdatePage(req: Request, res: Response): Promise<void> {
    try {
      const jd_id = Number(req.params.id);

      if (isNaN(jd_id)) {
        res.status(400).send("ID JD không hợp lệ");
        return;
      }

      const jd = await JDService.getJDById(jd_id);

      if (!jd) {
        res.status(404).send("Không tìm thấy JD");
        return;
      }

      // Render EJS và truyền dữ liệu ra
      res.render("business/business_update_jd", { jd });

    } catch (error) {
      console.error("Lỗi showUpdatePage:", error);
      res.status(500).send("Lỗi server");
    }
  }

}

export default new JDController();
