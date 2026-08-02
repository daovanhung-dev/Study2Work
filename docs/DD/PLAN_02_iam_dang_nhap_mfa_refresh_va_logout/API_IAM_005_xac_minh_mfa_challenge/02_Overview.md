---
title: "Overview"
order: 2
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Overview"
format: markdown
dd_id: "API-IAM-005"
status: "PARTIALLY COMPLETED — SOURCE GAPS"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | `API-IAM-005` |
| Module | `Platform Identity` |
| Method | `POST` |
| Endpoint | `/api/v1/auth/mfa/challenges/{challengeId}/verify` |
| Purpose | `TOTP 6 số hoặc recovery code → access/refresh token` |
| Consumer/Actor | `User có challenge` |
| Authentication | `Bearer access token ES256; kiểm iss, aud, exp, nbf, jti, sid, authVersion theo quy ước chung.` |
| Authorization | `User có challenge` |
| Basis | `DIRECT cho endpoint-level contract; DERIVED/SOURCE_REQUIRED được gắn theo từng field` |
| Status | `PARTIALLY COMPLETED — SOURCE GAPS` |
| Transaction | `Một database transaction; không gọi HTTP dependency trong transaction; rollback toàn bộ mutation cùng boundary.` |
| Side effects | `Audit theo nguồn endpoint; payload phải redact PII/secret.` |

## Sources

- `PLAN_02_IAM_IAM_ang_nhap_MFA_refresh_va_logout.md`.
- `01_TONG_QUAN_DU_AN.md`.
- `02_BIEU_DO_HE_THONG.md`.
- `03_THIET_KE_CO_SO_DU_LIEU.md`.
- `04_DAC_TA_API.md`.
- `05_DAC_TA_MAN_HINH.md`.

## Tables read

- `TBL-IAM-008 — mfa_challenges`.
- `TBL-IAM-006 — mfa_methods`.
- `TBL-IAM-007 — mfa_recovery_codes`.
- `TBL-IAM-001 — users`.

## Tables write

- `TBL-IAM-009 — auth_sessions`.
- `TBL-IAM-016 — idempotency_keys`.
- `TBL-IAM-008 — mfa_challenges`.
- `TBL-IAM-007 — mfa_recovery_codes`.
- `TBL-IAM-010 — refresh_tokens`.
- `TBL-IAM-017 — security_audit_events`.

## Mục chú ý

- Database owner: `identity_db`; cấm query/join xuyên database.
- Contract summary: L challenge; hash compare; max 5 lần; consume; create session, refresh family; recovery code one-use.
- Vận hành: Idempotency bắt buộc; audit; 10/15 phút/challenge.

## Assumptions

- `N/A — Không dùng giả định âm thầm`; nội dung suy dẫn được ghi `DERIVED`.

## Conflicts

- [Q-16] Field-level JSON Schema request/response chưa đầy đủ cho toàn bộ API catalog.
- [Q-15] Event payload/version chưa có schema đầy đủ cho nhiều endpoint.

## Security note

- Không log/response raw password, token, MFA secret, private key hoặc PII không cần thiết; cache theo contract.

## Performance note

- Idempotency bắt buộc; audit; 10/15 phút/challenge

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
