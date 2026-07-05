# Overview — CNT-COURSE-OUTLINE-001

## 1. Business intent

**Lấy outline khóa học theo learner** thuộc module **05. Khóa học và nội dung học**.

## 2. Authorization

- Yêu cầu `Bearer JWT cho nội dung học; catalog công khai tách riêng`.
- Actor/role hợp lệ: **Learner, Content Admin, Admin**.
- Authorization thực hiện tại backend, không tin trạng thái guard của frontend.

## 3. Main flow

1. API gateway/controller nhận `GET /api/v1/courses/{courseId}/outline` và gắn `traceId`.
2. Xác thực caller, kiểm tra permission/scope và validate request.
3. Load aggregate hoặc projection liên quan.
4. Áp dụng rule nghiệp vụ, cập nhật/truy vấn dữ liệu.
5. Ghi event/audit nếu có mutation; trả envelope chuẩn.

## 4. Business rules

- Chỉ học nội dung thuộc lộ trình đã kích hoạt và được mở khóa; media dùng signed URL ngắn hạn, không trả URL lưu trữ gốc.
- Ghi chú endpoint: Chỉ lộ nội dung learner được phép xem.
- Không trả dữ liệu ngoài scope của caller; `404` có thể được dùng thay `403` để tránh lộ resource.

## 5. Source traceability

- BD: `05. Study2Work_Study_BasicDesign_Khoa_Hoc_Noi_Dung_Hoc.md`
- AC: `diagram/AC/06. Study2Work_Study_AC_Khoa_Hoc_Noi_Dung_Hoc.md`
- Sequence: `diagram/SEQUENCE/06. Study2Work_Study_SEQ_Hoc_Bai_Cap_Nhat_Tien_Do.md`
- Class model dùng chung: `diagram/CLASS/01. Study2Work_Study_Diagram_CLASS_Mo_Hinh_Nghiep_Vu.md`
