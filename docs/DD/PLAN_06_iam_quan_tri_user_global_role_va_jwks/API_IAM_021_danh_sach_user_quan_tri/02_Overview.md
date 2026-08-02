---
title: "Overview"
order: 2
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Overview"
format: markdown
dd_id: "API-IAM-021"
status: "PARTIALLY COMPLETED — SOURCE GAPS"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | `API-IAM-021` |
| Module | `Platform Identity` |
| Method | `GET` |
| Endpoint | `/api/v1/admin/users` |
| Purpose | `Page/filter status/email hash/role → redacted users` |
| Consumer/Actor | ``PERM-IAM-001`` |
| Authentication | `Bearer access token ES256; kiểm iss, aud, exp, nbf, jti, sid, authVersion theo quy ước chung.` |
| Authorization | ``PERM-IAM-001`` |
| Basis | `DIRECT cho endpoint-level contract; DERIVED/SOURCE_REQUIRED được gắn theo từng field` |
| Status | `PARTIALLY COMPLETED — SOURCE GAPS` |
| Transaction | `Một database transaction; không gọi HTTP dependency trong transaction; rollback toàn bộ mutation cùng boundary.` |
| Side effects | `Audit theo nguồn endpoint; payload phải redact PII/secret.` |

## Sources

- `PLAN_06_IAM_IAM_Quan_tri_user_global_role_va_JWKS.md`.
- `01_TONG_QUAN_DU_AN.md`.
- `02_BIEU_DO_HE_THONG.md`.
- `03_THIET_KE_CO_SO_DU_LIEU.md`.
- `04_DAC_TA_API.md`.
- `05_DAC_TA_MAN_HINH.md`.

## Tables read

- `TBL-IAM-001 — users`.
- `TBL-IAM-002 — user_emails`.
- `TBL-IAM-015 — user_role_assignments`.
- `TBL-IAM-012 — roles`.

## Tables write

- `TBL-IAM-017 — security_audit_events`.

## Mục chú ý

- Database owner: `identity_db`; cấm query/join xuyên database.
- Contract summary: Query`(status,created_at,id)` or normalized email exact index; PII view requires separate permission.
- Vận hành: No shared cache; audit search; 60/phút.

## Assumptions

- `N/A — Không dùng giả định âm thầm`; nội dung suy dẫn được ghi `DERIVED`.

## Conflicts

- [Q-16] Field-level JSON Schema request/response chưa đầy đủ cho toàn bộ API catalog.

## Security note

- Không log/response raw password, token, MFA secret, private key hoặc PII không cần thiết; cache theo contract.

## Performance note

- No shared cache; audit search; 60/phút

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
