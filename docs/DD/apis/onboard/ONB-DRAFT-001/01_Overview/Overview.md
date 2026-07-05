# Overview — ONB-DRAFT-001

## 1. Business intent

**Lưu nháp onboarding** thuộc module **03. Onboarding**.

## 2. Authorization

- Yêu cầu `Bearer JWT`.
- Actor/role hợp lệ: **Learner**.
- Authorization thực hiện tại backend, không tin trạng thái guard của frontend.

## 3. Main flow

1. API gateway/controller nhận `PATCH /api/v1/onboarding/draft` và gắn `traceId`.
2. Xác thực caller, kiểm tra permission/scope và validate request.
3. Load aggregate hoặc projection liên quan.
4. Áp dụng rule nghiệp vụ, cập nhật/truy vấn dữ liệu.
5. Ghi event/audit nếu có mutation; trả envelope chuẩn.

## 4. Business rules

- Dự thảo có thể lưu nhiều lần; xác nhận chỉ hợp lệ khi dữ liệu bắt buộc đầy đủ và contact đã VERIFIED.
- Ghi chú endpoint: Partial update, schema phụ thuộc step.
- Không trả dữ liệu ngoài scope của caller; `404` có thể được dùng thay `403` để tránh lộ resource.

## 5. Source traceability

- BD: `03. Study2Work_Study_BasicDesign_Onboarding.md`
- AC: `diagram/AC/04. Study2Work_Study_AC_Onboarding.md`
- Sequence: `diagram/SEQUENCE/04. Study2Work_Study_SEQ_Onboarding_Goi_Y_Lo_Trinh.md`
- Class model dùng chung: `diagram/CLASS/01. Study2Work_Study_Diagram_CLASS_Mo_Hinh_Nghiep_Vu.md`
