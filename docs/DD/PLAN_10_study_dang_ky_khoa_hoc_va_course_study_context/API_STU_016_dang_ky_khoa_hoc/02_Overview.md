---
title: "Overview"
order: 2
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Overview"
format: markdown
dd_id: "API-STU-016"
status: "NEEDS USER DECISION — Draft"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | `API-STU-016` |
| Module | `Study` |
| Method | `POST` |
| Endpoint | `/api/v1/courses/{courseId}/enrollments` |
| Purpose | `Stable course ID hoặc explicit published version → enrollment pinned version` |
| Consumer/Actor | `Learner active; onboarding không bắt buộc` |
| Authentication | `Bearer access token ES256; kiểm iss, aud, exp, nbf, jti, sid, authVersion theo quy ước chung.` |
| Authorization | `Learner active; onboarding không bắt buộc` |
| Basis | `DIRECT cho endpoint-level contract; DERIVED/SOURCE_REQUIRED được gắn theo từng field` |
| Status | `NEEDS USER DECISION — Draft` |
| Transaction | `Một database transaction; không gọi HTTP dependency trong transaction; rollback toàn bộ mutation cùng boundary.` |
| Side effects | `Audit theo nguồn endpoint; payload phải redact PII/secret.; Outbox/event `study.course.enrolled`; payload/version còn Q-15 nếu chưa có schema.` |

## Sources

- `PLAN_10_STU_Study_ang_ky_khoa_hoc_va_course_study_context.md`.
- `01_TONG_QUAN_DU_AN.md`.
- `02_BIEU_DO_HE_THONG.md`.
- `03_THIET_KE_CO_SO_DU_LIEU.md`.
- `04_DAC_TA_API.md`.
- `05_DAC_TA_MAN_HINH.md`.

## Tables read

- `TBL-STU-001 — identity_projections`.
- `TBL-STU-002 — learner_profiles`.
- `TBL-STU-011 — courses`.
- `TBL-STU-012 — course_versions`.
- `TBL-STU-027 — course_enrollments`.
- `TBL-STU-026 — primary_path_periods`.

## Tables write

- `TBL-STU-050 — audit_events`.
- `TBL-STU-027 — course_enrollments`.
- `TBL-STU-051 — idempotency_keys`.
- `TBL-STU-052 — outbox_events`.

## Mục chú ý

- Database owner: `study_db`; cấm query/join xuyên database.
- Contract summary: TX idempotency; select current published version; insert unique`(user,course_version)` or return existing; source standalone/path.
- Vận hành: Idempotency required;`study.course.enrolled`; audit.

## Assumptions

- `N/A — Không dùng giả định âm thầm`; nội dung suy dẫn được ghi `DERIVED`.

## Conflicts

- [Q-16] Field-level JSON Schema request/response chưa đầy đủ cho toàn bộ API catalog.
- [Q-13] Vị trí `courseVersionId` và nguồn `source_type` của enrollment chưa được chốt.
- [Q-15] Event payload/version chưa có schema đầy đủ cho nhiều endpoint.

## Security note

- Không log/response raw password, token, MFA secret, private key hoặc PII không cần thiết; cache theo contract.

## Performance note

- Idempotency required;`study.course.enrolled`; audit

---
## Phụ lục đối chiếu nguồn Excel
- Workbook nguồn: `DD_API_Template(1).xlsx`
- Sheet nguồn: `Overview`
- Dimension: `A1:BA10`
- Trạng thái: `visible`
- Số ô có dữ liệu/công thức: `4`
- Số vùng merge: `0`

<details>
<summary>Bản ghi từng ô có dữ liệu hoặc công thức</summary>

| Hàng | Ô | Giá trị nguồn | Công thức nguồn |
|---:|---|---|---|
| 1 | `A1` | 【Khái quát】 |  |
| 3 | `B3` | Get thông tin…. |  |
| 5 | `A5` | 【Mục chú ý】 |  |
| 7 | `B7` | Không có |  |

</details>
