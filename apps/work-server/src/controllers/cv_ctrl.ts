import { Request, Response } from "express";
import CVService from "../services/cv_services.js";


class CVCtrl {
  async CV(req: Request, res: Response) {
    //kiem tra xem da co cv chua
    const id = (req.user as any).id;
    const count = await CVService.countCV(id);
    console.log("Id: ", id);
    console.log("count: ", count);
    if (count == 0) {
      console.log("Chua tao cv");
      res.redirect("/Student/CreateCV");
    } else {
      console.log("Da co CV roi!!");
      res.redirect("/Student/UpdateCV");
    }
  }

  async createCV(req: Request, res: Response) {
    try {
      console.log("Tạo CV");

      const user = req.user as any;
      if (!user) return res.status(400).send("Không xác thực được người dùng");

      const sinhvien_id = Number(user.id);

      // Kiểm tra đã có CV chưa
      const count = await CVService.countCV(sinhvien_id);
      if (typeof count === "number" && count >= 1) {
        return res.status(400).send("Bạn đã có CV rồi, không thể tạo thêm.");
      }

      // Nếu có file upload, lấy tên file
      let avtFile = undefined;
      if (req.file) {
        avtFile = req.file.filename;
      }

      const {
        hoten,
        ngaysinh,
        gioitinh,
        email,
        sdt,
        diachi,
        vitri,
        nganh,
        muctieunghiep,
        hocvan,
        kinhnghiem,
        kynang,
        ngoaingu,
        chungchi,
        duan,
        giaithuong,
        hoatdong,
        social,
        portfolio,
        luongmongmuon,
      } = req.body;

      // Parse social an toàn
      let socialData = undefined;
      if (social) {
        try {
          socialData = JSON.parse(social);
        } catch {
          socialData = social;
        }
      }

      const data = {
        avt: avtFile, // lưu tên file
        hoten,
        ngaysinh: ngaysinh ? new Date(ngaysinh) : undefined,
        gioitinh,
        email,
        sdt,
        diachi,
        vitri,
        nganh,
        muctieunghiep,
        hocvan,
        kinhnghiem,
        kynang,
        ngoaingu,
        chungchi,
        duan,
        giaithuong,
        hoatdong,
        social: socialData,
        portfolio,
        luongmongmuon,
        sinhvien_id,
      };

      const result = await CVService.insertCv(data);

      if (!result.success) {
        return res.status(500).send("Lỗi khi tạo CV");
      }

      console.log("Tạo CV thành công!");
      return res.redirect("/Student/CV");
    } catch (err) {
      console.error("Lỗi tạo CV:", err);
      return res.status(500).send("Lỗi server");
    }
  }

  async getCV(req: Request, res: Response) {
    const users = req.user as any;
    const id = users.id;
    const cv = await CVService.getCvById(id);

    // chuẩn hoá avatar
    let avatarUrl = "/public/images/default-avatar.png"; // ảnh mặc định
    if (cv.data && cv.data.avt) {
      // nếu chỉ lưu tên file trong folder uploads
      avatarUrl = `/uploads/${cv.data.avt}`;
    }

    res.render("Student/student_update_CV", { cv: cv.data, avatarUrl });
  }

  async updateCV(req: Request, res: Response) {
    try {
      //khai bao user
      const id = Number(req.params.id);
      const updateData = req.body;
      if (updateData.ngaysinh) {
        updateData.ngaysinh = new Date(updateData.ngaysinh);
      }
      await CVService.updateCv(id, updateData);
      res.redirect("/student/UpdateCV");
    } catch (err) {
      console.error(err);
      return res.status(500).json({ success: false, error: "Lỗi server" });
    }
  }

  async detail(req: Request, res: Response) {
  try {
    const id = Number(req.params.id);

    if (!id) {
      return res.status(400).send("ID CV không hợp lệ");
    }

    const result = await CVService.getCvById(id);

    if (!result.success) {
      return res.status(404).send(result.error || "Không tìm thấy CV");
    }

    // Lấy thẳng dữ liệu CV để render
    const cvData = result.data;

    res.render("business/detailCV", { cv: cvData });
  } catch (error) {
    console.error("Lỗi xem chi tiết CV:", error);
    res.status(500).send("Lỗi máy chủ");
  }
}


}

export default new CVCtrl();
