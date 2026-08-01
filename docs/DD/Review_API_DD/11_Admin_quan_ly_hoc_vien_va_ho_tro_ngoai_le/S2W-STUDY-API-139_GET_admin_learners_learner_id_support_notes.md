# Review S2W-STUDY-API-139 — GET learner support notes

- DD nguồn: `docs/DD/Study2Work_DD_API/11_Admin_quan_ly_hoc_vien_va_ho_tro_ngoai_le/S2W-STUDY-API-139_GET_admin_learners_learner_id_support_notes.xlsx`
- Endpoint: `GET /api/v1/admin/learners/{learner_id}/support-notes`
- Kết luận: **CẦN SỬA — thiếu persistence model cho support note**

## Các điểm cần sửa

| ID | Mức độ | Vị trí DD | Nhận xét và căn cứ BD | Cách sửa |
|---|---|---|---|---|
| 139-01 | P0 | `2.Response!A15:H23`, `3.Data mapping!A12:H20` | DD dựa vào `study.support_notes`, nhưng schema hiện hành không có bảng này; SQL còn dùng `note_id/author` như cột chưa được định nghĩa. | Bổ sung migration/table/FK/index/retention hoặc quyết định ánh xạ sang model khác; không để bảng giả ở trạng thái VERIFIED. |
| 139-02 | P0 | `3.Data mapping!A13:H17` | Visibility `INTERNAL|OFFICIAL_RESPONSE` xuất hiện ở response nhưng chưa có policy đọc theo vai trò. BD nói note nội bộ chỉ hiện theo quyền và không cho learner xem trừ phản hồi chính thức (`BD-11:157-166`, `170-181`). | Định nghĩa permission riêng, row/field policy, author snapshot và đường public riêng cho official response. |
| 139-03 | P1 | `1.Request!A22:J23`, `3.Data mapping!A12:H12` | Sort ghi `ORDER BY order_index ASC, created_at DESC` dù note không có `order_index`; pagination thiếu stable tie-breaker. | Sort `createdAt DESC, id DESC`; định nghĩa cursor/page total và index `(learner_id, created_at, id)`. |
| 139-04 | P0 | `2.Response!A9:E11` | Envelope, snake_case và pagination phẳng trái `System_Architecture.md:632-721`. | Dùng camelCase và `meta.pagination`; traceId ở top-level. |
| 139-05 | P1 | `00.Hướng dẫn!A4:B18`, `Lịch sử!A4:F4` | Checklist ghi đã review schema/không placeholder dù target table chưa tồn tại. | Chuyển DRAFT/NEEDS_REVIEW và chỉ verify sau migration + authorization tests. |

## Điều kiện duyệt lại

- Persistence/retention/visibility của note được chốt.
- Có negative test learner/Content Admin không đọc note nội bộ.
