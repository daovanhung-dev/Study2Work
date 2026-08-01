# Review API DD — S2W-STUDY-API-047

- DD nguồn: `docs/DD/Study2Work_DD_API/05_Khoa_hoc_chuong_bai_hoc_va_tai_nguyen/S2W-STUDY-API-047_GET_me_content_issues.xlsx`
- Endpoint: `GET /api/v1/me/content-issues`
- Verdict: **CẦN SỬA**

## Findings

| Mức | Sheet/cell | Finding | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P0 | `2.Response!A15:H22`, `3.Data mapping!A12:H12`, `A20` | `study.content_issues` không tồn tại; issue ID/content ref/response/resolved lifecycle đều chưa có schema/BD contract nhưng bị trình bày như cột thật. | `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:235-732`; `docs/BD/05. Study2Work_Study_BasicDesign_Khoa_Hoc_Noi_Dung_Hoc.md:170-180` | Chốt model/lifecycle và field visibility trước khi định nghĩa list. |
| P0 | `3.Data mapping!A12:H12` | DD có owner predicate `content_issues.user_id`, nhưng API046 không ghi `user_id` và schema không tồn tại; ownership không thể được bảo đảm. | `docs/BD/13. Study2Work_Study_BasicDesign_Vai_Tro_Phan_Quyen_Audit_Log.md:57-76` | Dùng reporter/creator column thống nhất và negative ownership test. |
| P1 | `1.Request!A21:J23`, `2.Response!A19:H22` | Status là free text; response `response/resolved_at` không có enum/nullability/redaction. Admin response có thể chứa nội dung nội bộ/PII. | `docs/BD/05. Study2Work_Study_BasicDesign_Khoa_Hoc_Noi_Dung_Hoc.md:170-180`; `docs/BD/13. Study2Work_Study_BasicDesign_Vai_Tro_Phan_Quyen_Audit_Log.md:187-209` | Canonical status transition và learner-safe response projection. |
| P1 | `3.Data mapping!A12:H12` | Không có deterministic paging tie-breaker và page validation min ghi 0; concurrent inserts có thể lặp/mất dòng. | `docs/BD/base/0. Study2Work_System_Architecture.md:702-721` | Sort `(createdAt DESC,id DESC)`, page min 1/cap hoặc cursor. |
| P0 | `2.Response!A9:E11`, `A23:H26` | Envelope/pagination snake_case không canonical. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-721` | Canonical list response với `meta.pagination`. |

## Điều kiện duyệt lại

- [ ] Schema/lifecycle/learner visibility được phê duyệt.
- [ ] Ownership nối được với API046 và có test.
- [ ] Status/nullability/redaction/paging rõ.
- [ ] Envelope canonical và endpoint suy dẫn được duyệt.
