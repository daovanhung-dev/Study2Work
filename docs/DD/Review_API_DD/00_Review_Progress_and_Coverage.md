# Tiến độ và Coverage Review API DD

## Task Definition

- Yêu cầu: đọc toàn bộ BD, đọc toàn bộ DD, đánh giá tính hợp lý của từng API DD và tạo một file Markdown ghi các điểm cần sửa cho mỗi API.
- Phạm vi: toàn bộ nội dung trong `docs.zip`.
- Không thực hiện: sửa trực tiếp 157 workbook DD hoặc thay đổi nghiệp vụ.
- Nguồn ưu tiên: BD/sequence, kiến trúc hệ thống và schema SQL trong gói tài liệu.

## Input và độ phủ

| Nhóm | Số lượng | Đã đọc | Chưa đọc | Lỗi | Coverage |
|---|---:|---:|---:|---:|---:|
| BD Markdown | 47 | 47 | 0 | 0 | 100% |
| BD SQL schema | 1 | 1 | 0 | 0 | 100% |
| API DD workbook | 157 | 157 | 0 | 0 | 100% |
| DD index workbook | 1 | 1 | 0 | 0 | 100% |
| Review Markdown có sẵn | 138 | 138 | 0 | 0 | 100% |
| **Tổng file đầu vào** | **344** | **344** | **0** | **0** | **100%** |

Kiểm chứng workbook: **158 workbook, 1.731 sheet, 131.447 cell/formula có nội dung, 42 formula**; không phát hiện sheet ẩn, comment hoặc chart. Mỗi API workbook có 11 sheet theo cùng template.

## Xác định tiến độ ban đầu

- Tổng API DD: **157**.
- Note review đã có: **137**, tương ứng API-021…API-157.
- Note còn thiếu: **20**, tương ứng API-001…API-020.
- Tiến độ ban đầu: **137/157 = 87,3%**.
- Phần còn lại: **12,7%**.

| Module | API DD | Note trước khi xử lý | Note sau khi xử lý | Tiến độ ban đầu |
|---|---:|---:|---:|---:|
| `01_Public_Catalog` | 6 | 0 | 6 | 0.0% |
| `02_Tai_khoan_xac_thuc_va_ho_so` | 14 | 0 | 14 | 0.0% |
| `03_Onboarding` | 7 | 7 | 7 | 100.0% |
| `04_Lo_trinh_hoc` | 11 | 11 | 11 | 100.0% |
| `05_Khoa_hoc_chuong_bai_hoc_va_tai_nguyen` | 9 | 9 | 9 | 100.0% |
| `06_Bai_tap_va_danh_gia` | 13 | 13 | 13 | 100.0% |
| `07_Tien_do_va_hoan_thanh` | 9 | 9 | 9 | 100.0% |
| `08_Cong_dong_Zalo` | 13 | 13 | 13 | 100.0% |
| `09_Thong_bao` | 11 | 11 | 11 | 100.0% |
| `10_Admin_quan_tri_noi_dung` | 34 | 34 | 34 | 100.0% |
| `11_Admin_quan_ly_hoc_vien_va_ho_tro_ngoai_le` | 14 | 14 | 14 | 100.0% |
| `12_Bao_cao_van_hanh` | 8 | 8 | 8 | 100.0% |
| `13_Vai_tro_phan_quyen_va_audit` | 8 | 8 | 8 | 100.0% |

## Kết quả thực hiện

- Đã tạo đủ **20 note review** cho API-001…API-020.
- Sau xử lý: **157/157 API có đúng một note Markdown**, không thiếu ID và không trùng ID.
- Toàn bộ 157 note hiện có verdict bắt đầu bằng **“CẦN SỬA”**. Điều này có nghĩa coverage review đã hoàn thành, nhưng các DD nguồn chưa đủ điều kiện phê duyệt.
- Không chỉnh sửa workbook DD nguồn; chỉ bổ sung review note và báo cáo kiểm kê/coverage.

### Nhóm vấn đề chính trong API-001…API-020

1. Contract request/response lệch BD sequence, dùng snake_case và envelope `{
data, meta
}`/`{error}` thay vì canonical envelope.
2. Mapping tới view, bảng hoặc cột không tồn tại trong schema; nhiều SQL còn placeholder.
3. API đăng ký, login, session, verification và password đặt ownership ở Study trong khi kiến trúc quy định Platform Identity sở hữu credential/session/token.
4. Thiếu rule bảo mật quan trọng: anti-enumeration, rate limit, OTP/token TTL, one-time use, session revocation và step-up authentication.
5. Nhiều workbook ghi `VERIFIED` dù reviewer/approver chưa chỉ định và source inventory trong template đã lỗi thời.

## Quality Gate

| Gate | Kết quả | Ghi chú |
|---|---|---|
| Coverage Gate | PASS | 344/344 file in-scope đã đọc; 157/157 API có note. |
| ID/Uniqueness Gate | PASS | Không thiếu và không trùng API review ID. |
| Traceability Gate cho note mới | PASS | Mỗi finding có sheet/cell, căn cứ BD/schema và cách sửa. |
| Consistency/Design Gate của DD nguồn | FAILED VALIDATION | Contract, ownership và mapping DB còn nhiều P0/P1. |
| Delivery Gate | PASS | Mỗi API DD có một Markdown review; source workbook không bị ghi đè. |

## Trạng thái

- **Task review:** `DONE`.
- **Tình trạng DD nguồn:** `FAILED VALIDATION — NEEDS REVISION`.
- **Lưu ý:** 137 note cũ được giữ nguyên; đã kiểm tra sự hiện diện, ID, nguồn và verdict, nhưng không tái biên tập toàn bộ nội dung của các note đó.

## File mới tạo

- `DD/Review_API_DD/01_Public_Catalog/S2W-STUDY-API-001_GET_catalog_overview.md`
- `DD/Review_API_DD/01_Public_Catalog/S2W-STUDY-API-002_GET_catalog_learning_paths.md`
- `DD/Review_API_DD/01_Public_Catalog/S2W-STUDY-API-003_GET_catalog_learning_paths_slug.md`
- `DD/Review_API_DD/01_Public_Catalog/S2W-STUDY-API-004_GET_catalog_courses.md`
- `DD/Review_API_DD/01_Public_Catalog/S2W-STUDY-API-005_GET_catalog_courses_slug.md`
- `DD/Review_API_DD/01_Public_Catalog/S2W-STUDY-API-006_GET_catalog_sample_lessons_lesson_id.md`
- `DD/Review_API_DD/02_Tai_khoan_xac_thuc_va_ho_so/S2W-STUDY-API-007_POST_auth_register.md`
- `DD/Review_API_DD/02_Tai_khoan_xac_thuc_va_ho_so/S2W-STUDY-API-008_POST_auth_login.md`
- `DD/Review_API_DD/02_Tai_khoan_xac_thuc_va_ho_so/S2W-STUDY-API-009_POST_auth_logout.md`
- `DD/Review_API_DD/02_Tai_khoan_xac_thuc_va_ho_so/S2W-STUDY-API-010_POST_auth_verification_send.md`
- `DD/Review_API_DD/02_Tai_khoan_xac_thuc_va_ho_so/S2W-STUDY-API-011_POST_auth_verify_contact.md`
- `DD/Review_API_DD/02_Tai_khoan_xac_thuc_va_ho_so/S2W-STUDY-API-012_GET_auth_account_status.md`
- `DD/Review_API_DD/02_Tai_khoan_xac_thuc_va_ho_so/S2W-STUDY-API-013_POST_auth_password_forgot.md`
- `DD/Review_API_DD/02_Tai_khoan_xac_thuc_va_ho_so/S2W-STUDY-API-014_POST_auth_password_reset.md`
- `DD/Review_API_DD/02_Tai_khoan_xac_thuc_va_ho_so/S2W-STUDY-API-015_PUT_auth_password.md`
- `DD/Review_API_DD/02_Tai_khoan_xac_thuc_va_ho_so/S2W-STUDY-API-016_GET_me_profile.md`
- `DD/Review_API_DD/02_Tai_khoan_xac_thuc_va_ho_so/S2W-STUDY-API-017_PATCH_me_profile.md`
- `DD/Review_API_DD/02_Tai_khoan_xac_thuc_va_ho_so/S2W-STUDY-API-018_POST_me_contact_change.md`
- `DD/Review_API_DD/02_Tai_khoan_xac_thuc_va_ho_so/S2W-STUDY-API-019_POST_me_contact_change_confirm.md`
- `DD/Review_API_DD/02_Tai_khoan_xac_thuc_va_ho_so/S2W-STUDY-API-020_GET_me_navigation_context.md`
