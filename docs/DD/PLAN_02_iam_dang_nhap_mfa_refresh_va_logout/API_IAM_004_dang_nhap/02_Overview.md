---
title: "Overview"
order: 2
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Overview"
format: markdown
dd_id: "API-IAM-004"
status: "PARTIALLY COMPLETED — SOURCE GAPS"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | `API-IAM-004` |
| Module | `Platform Identity` |
| Method | `POST` |
| Endpoint | `/api/v1/auth/login` |
| Purpose | ``email`, `password`, device label → token hoặc MFA challenge` |
| Consumer/Actor | `Anonymous` |
| Authentication | `Anonymous; endpoint vẫn áp dụng rate limit và anti-enumeration khi có nguồn.` |
| Authorization | `N/A — public/anonymous.` |
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

- `TBL-IAM-002 — user_emails`.
- `TBL-IAM-003 — password_credentials`.
- `TBL-IAM-001 — users`.
- `TBL-IAM-015 — user_role_assignments`.
- `TBL-IAM-012 — roles`.
- `TBL-IAM-006 — mfa_methods`.

## Tables write

- `TBL-IAM-009 — auth_sessions`.
- `TBL-IAM-008 — mfa_challenges`.
- `TBL-IAM-018 — outbox_events`.
- `TBL-IAM-003 — password_credentials`.
- `TBL-IAM-010 — refresh_tokens`.
- `TBL-IAM-017 — security_audit_events`.

## Mục chú ý

- Database owner: `identity_db`; cấm query/join xuyên database.
- Contract summary: R credential/user bằng normalized-email unique index; constant-time verify; TX cập nhật failure/lock; nếu privileged tạo one-use challenge, nếu không tạo session + rotating refresh.
- Vận hành: Security audit cả success/failure; rate như mục 2.3; event login-risk nếu bất thường.

## Assumptions

- `N/A — Không dùng giả định âm thầm`; nội dung suy dẫn được ghi `DERIVED`.

## Conflicts

- [Q-16] Field-level JSON Schema request/response chưa đầy đủ cho toàn bộ API catalog.
- [Q-15] Event payload/version chưa có schema đầy đủ cho nhiều endpoint.

## Security note

- Không log/response raw password, token, MFA secret, private key hoặc PII không cần thiết; cache theo contract.

## Performance note

- Security audit cả success/failure; rate như mục 2.3; event login-risk nếu bất thường

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
