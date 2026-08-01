# Review API DD — S2W-STUDY-API-046

- DD nguồn: `docs/DD/Study2Work_DD_API/05_Khoa_hoc_chuong_bai_hoc_va_tai_nguyen/S2W-STUDY-API-046_POST_content_issues.xlsx`
- Endpoint: `POST /api/v1/content-issues`
- Verdict: **CẦN SỬA**

## Findings

| Mức | Sheet/cell | Finding | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P0 | `3.Data mapping!A12:H14`, `7.DB_Insert_Main!A6:I14` | Target `study.content_issues` không tồn tại trong SQL; toàn bộ insert/status lifecycle chỉ là suy diễn nhưng workbook ghi VERIFIED. | `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:235-732`; `docs/BD/05. Study2Work_Study_BasicDesign_Khoa_Hoc_Noi_Dung_Hoc.md:170-180` | Chốt schema/migration và Admin handling lifecycle trước coding/approval. |
| P0 | `1.Request!A21:J25` | `content_type`/`issue_type` là free text (max tới 2000), không có enum theo các loại lỗi BD; không validate actor có quyền xem content ID được báo. | `docs/BD/05. Study2Work_Study_BasicDesign_Khoa_Hoc_Noi_Dung_Hoc.md:170-180,209-219` | Enum target/issue canonical, verify referenced content + learner access, giới hạn description hợp lý. |
| P0 | `7.DB_Insert_Main!A8:I14` | Mapping không có actor/user ownership theo tên canonical (`created_by` là field suy diễn), không có anti-spam/dedup/idempotency; POST retry có thể tạo report trùng. | `docs/BD/base/0. Study2Work_System_Architecture.md:723-736`; BD05 `:170-180` | Lưu reporter ID, fingerprint/status/timestamps; idempotency/rate limit/dedup rõ. |
| P1 | `1.Request!A25:J25` | Nhận arbitrary `evidence_url` nhưng không có allowlist/upload ownership/malware/SSRF policy. | `docs/BD/base/0. Study2Work_System_Architecture.md:975-1042` | Dùng upload reference do platform cấp hoặc strict URL validation; không fetch URL tùy ý. |
| P0 | `2.Response!A9:E11`, `A15:H19` | Envelope cũ; response `issue_id/submitted_at` cũng dựa relation/cột chưa tồn tại. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Canonical `CONTENT_ISSUE_CREATED` contract sau khi schema/lifecycle được duyệt. |

## Điều kiện duyệt lại

- [ ] Có schema/lifecycle/admin queue được phê duyệt.
- [ ] Enum/reference access/reporter/idempotency/rate limit đầy đủ.
- [ ] Evidence handling an toàn.
- [ ] Contract canonical và endpoint suy dẫn được PO/API owner duyệt.
