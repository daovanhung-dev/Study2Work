# Overview — EXE-REVIEW-001

## 1. Business intent

**Chấm hoặc phản hồi thủ công** thuộc module **06. Bài tập và đánh giá**.

## 2. Authorization

- Yêu cầu `Bearer JWT`.
- Actor/role hợp lệ: **Learner, Content Admin, Learner Support, Admin; quyền cụ thể được kiểm tra theo permission code.**.
- Authorization thực hiện tại backend, không tin trạng thái guard của frontend.

## 3. Main flow

1. API gateway/controller nhận `PATCH /api/v1/admin/exercise-submissions/{submissionId}/review` và gắn `traceId`.
2. Xác thực caller, kiểm tra permission/scope và validate request.
3. Load aggregate hoặc projection liên quan.
4. Áp dụng rule nghiệp vụ, cập nhật/truy vấn dữ liệu.
5. Ghi event/audit nếu có mutation; trả envelope chuẩn.

## 4. Business rules

- Điểm và trạng thái nộp do server tính; thời hạn, số lần nộp và điều kiện nộp lại được kiểm tra server-side.
- Ghi chú endpoint: Reviewer có scope; audit bắt buộc.
- Không trả dữ liệu ngoài scope của caller; `404` có thể được dùng thay `403` để tránh lộ resource.

## 5. Source traceability

- BD: `06. Study2Work_Study_BasicDesign_Bai_Tap_Danh_Gia.md`
- AC: `diagram/AC/07. Study2Work_Study_AC_Bai_Tap_Danh_Gia.md`
- Sequence: `diagram/SEQUENCE/07. Study2Work_Study_SEQ_Bai_Tap_Nop_Cham_Nop_Lai.md`
- Class model dùng chung: `diagram/CLASS/01. Study2Work_Study_Diagram_CLASS_Mo_Hinh_Nghiep_Vu.md`
