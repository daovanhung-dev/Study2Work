# Review S2W-STUDY-API-129 — GET learner support profile

- DD nguồn: `docs/DD/Study2Work_DD_API/11_Admin_quan_ly_hoc_vien_va_ho_tro_ngoai_le/S2W-STUDY-API-129_GET_admin_learners_learner_id_support_profile.xlsx`
- Endpoint: `GET /api/v1/admin/learners/{learner_id}/support-profile`
- Kết luận: **CẦN SỬA — chưa đủ điều kiện VERIFIED**

## Các điểm cần sửa

| ID | Mức độ | Vị trí DD | Nhận xét và căn cứ BD | Cách sửa |
|---|---|---|---|---|
| 129-01 | P0 | `2.Response!A9:E11`, `A15:H25` | Response dùng envelope cũ và snake_case, trái chuẩn thay thế tại `System_Architecture.md:632-700`. Ví dụ còn chèn pagination cho response singleton. | Dùng envelope chuẩn camelCase; bỏ `page/page_size`; thêm businessCode cụ thể và `traceId`. |
| 129-02 | P0 | `3.Data mapping!A12:H20` | Điều kiện `users.user_id = :learner_id` sai với PK `users.id` (`schema_seed.sql:239-249`). SQL còn SELECT các “cột” tổng hợp như `basic_account`, `path_history`, `pending_assignments` và để `<FK condition>`, nên không thể triển khai. | Viết query/JOIN hoặc repository composition thật, nêu khóa nối và nguồn từng phần hồ sơ. |
| 129-03 | P1 | `2.Response!A16:H24` | Hầu hết section lồng nhau bị khai báo `String` và gán nguồn `users`, trong khi SEQ-12 yêu cầu tải account, onboarding, progress và history từ nhiều nguồn (`SEQ-12:25-28`). | Định nghĩa object/array con, cardinality, enum, nullable và nguồn cụ thể; không dùng `_value` trong sample. |
| 129-04 | P0 | `Overview!A12`, `3.Data mapping!A16:H16` | Dòng “không trả dữ liệu nhạy cảm” chưa thành field policy. BD cấm Admin xem mật khẩu, OTP và dữ liệu xác thực nhạy cảm (`BD-11:58-72`); kiến trúc còn yêu cầu minimize PII (`System_Architecture.md:980-1042`). | Lập allowlist field trả về, mask email/phone theo vai trò; cấm join/serialize `auth_credentials`; thêm test chống lộ secret. |
| 129-05 | P1 | `00.Hướng dẫn!A4:B18`, `Lịch sử!A4:F4` | Checklist ghi đã hết placeholder và đã review nguồn trong khi mapping vẫn giả lập; trạng thái VERIFIED không có người review/approve. | Chuyển NEEDS_REVIEW và chỉ VERIFIED sau review schema, privacy và contract. |

## Điều kiện duyệt lại

- Contract support profile có schema lồng nhau đầy đủ và mapping chạy được.
- Có kiểm thử field-level authorization và negative test không lộ credential/OTP/token.
