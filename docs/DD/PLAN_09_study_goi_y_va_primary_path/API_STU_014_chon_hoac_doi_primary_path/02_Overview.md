---
title: "Overview"
order: 2
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Overview"
format: markdown
dd_id: "API-STU-014"
status: "NEEDS USER DECISION — Draft"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | `API-STU-014` |
| Module | `Study` |
| Method | `PUT` |
| Endpoint | `/api/v1/me/primary-path` |
| Purpose | ``pathVersionId`, expected current period/version, reason optional → new active period` |
| Consumer/Actor | `Learner active + onboarding complete` |
| Authentication | `Bearer access token ES256; kiểm iss, aud, exp, nbf, jti, sid, authVersion theo quy ước chung.` |
| Authorization | `Learner active + onboarding complete` |
| Basis | `DIRECT cho endpoint-level contract; DERIVED/SOURCE_REQUIRED được gắn theo từng field` |
| Status | `NEEDS USER DECISION — Draft` |
| Transaction | `Một database transaction; không gọi HTTP dependency trong transaction; rollback toàn bộ mutation cùng boundary.` |
| Side effects | `Audit theo nguồn endpoint; payload phải redact PII/secret.; Outbox/event `study.primary_path.changed`; payload/version còn Q-15 nếu chưa có schema.` |

## Sources

- `PLAN_09_STU_Study_Goi_y_va_primary_path.md`.
- `01_TONG_QUAN_DU_AN.md`.
- `02_BIEU_DO_HE_THONG.md`.
- `03_THIET_KE_CO_SO_DU_LIEU.md`.
- `04_DAC_TA_API.md`.
- `05_DAC_TA_MAN_HINH.md`.

## Tables read

- `TBL-STU-002 — learner_profiles`.
- `TBL-STU-007 — onboarding_submissions`.
- `TBL-STU-026 — primary_path_periods`.
- `TBL-STU-010 — learning_path_versions`.

## Tables write

- `TBL-STU-050 — audit_events`.
- `TBL-STU-051 — idempotency_keys`.
- `TBL-STU-052 — outbox_events`.
- `TBL-STU-026 — primary_path_periods`.

## Mục chú ý

- Database owner: `study_db`; cấm query/join xuyên database.
- Contract summary: TX advisory lock user; idempotency; validate published; initial select or enforce UTC 168h cooldown; close old as SWITCHED_OUT; insert new ACTIVE; preserve all enrollment/progress.
- Vận hành: Idempotency required;`study.primary_path.changed`; audit; no cache.

## Assumptions

- `N/A — Không dùng giả định âm thầm`; nội dung suy dẫn được ghi `DERIVED`.

## Conflicts

- [Q-16] Field-level JSON Schema request/response chưa đầy đủ cho toàn bộ API catalog.
- [Q-12] Chưa chốt chọn primary path có tự động tạo course enrollment hay không.
- [Q-15] Event payload/version chưa có schema đầy đủ cho nhiều endpoint.

## Security note

- Không log/response raw password, token, MFA secret, private key hoặc PII không cần thiết; cache theo contract.

## Performance note

- Idempotency required;`study.primary_path.changed`; audit; no cache

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
