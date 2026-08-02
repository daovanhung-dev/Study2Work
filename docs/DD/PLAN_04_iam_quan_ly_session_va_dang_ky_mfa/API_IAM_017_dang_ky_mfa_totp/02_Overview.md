---
title: "Overview"
order: 2
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Overview"
format: markdown
dd_id: "API-IAM-017"
status: "NEEDS USER DECISION — Draft"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | `API-IAM-017` |
| Module | `Platform Identity` |
| Method | `POST` |
| Endpoint | `/api/v1/me/mfa/enrollments` |
| Purpose | `Method`TOTP`; device label → secret once + QR payload, recovery codes once` |
| Consumer/Actor | `Privileged user + step-up` |
| Authentication | `Bearer access token ES256; kiểm iss, aud, exp, nbf, jti, sid, authVersion theo quy ước chung.` |
| Authorization | `Privileged user + step-up` |
| Basis | `DIRECT cho endpoint-level contract; DERIVED/SOURCE_REQUIRED được gắn theo từng field` |
| Status | `NEEDS USER DECISION — Draft` |
| Transaction | `Một database transaction; không gọi HTTP dependency trong transaction; rollback toàn bộ mutation cùng boundary.` |
| Side effects | `Audit theo nguồn endpoint; payload phải redact PII/secret.` |

## Sources

- `PLAN_04_IAM_IAM_Quan_ly_session_va_ang_ky_MFA.md`.
- `01_TONG_QUAN_DU_AN.md`.
- `02_BIEU_DO_HE_THONG.md`.
- `03_THIET_KE_CO_SO_DU_LIEU.md`.
- `04_DAC_TA_API.md`.
- `05_DAC_TA_MAN_HINH.md`.

## Tables read

- `TBL-IAM-006 — mfa_methods`.
- `TBL-IAM-001 — users`.

## Tables write

- `TBL-IAM-016 — idempotency_keys`.
- `TBL-IAM-006 — mfa_methods`.
- `TBL-IAM-017 — security_audit_events`.

## Mục chú ý

- Database owner: `identity_db`; cấm query/join xuyên database.
- Contract summary: Encrypt pending secret with KMS envelope; create enrollment not active until verify.
- Vận hành: Idempotency;`no-store`; audit.

## Assumptions

- `N/A — Không dùng giả định âm thầm`; nội dung suy dẫn được ghi `DERIVED`.

## Conflicts

- [Q-16] Field-level JSON Schema request/response chưa đầy đủ cho toàn bộ API catalog.
- [Q-04] Thời điểm API trả recovery codes giữa enroll và confirm MFA chưa thống nhất.
- [Q-15] Event payload/version chưa có schema đầy đủ cho nhiều endpoint.

## Security note

- Không log/response raw password, token, MFA secret, private key hoặc PII không cần thiết; cache theo contract.

## Performance note

- Idempotency;`no-store`; audit

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
