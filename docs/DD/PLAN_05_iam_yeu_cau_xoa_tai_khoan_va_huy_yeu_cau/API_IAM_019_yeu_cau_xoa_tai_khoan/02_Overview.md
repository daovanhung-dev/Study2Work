---
title: "Overview"
order: 2
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Overview"
format: markdown
dd_id: "API-IAM-019"
status: "NEEDS USER DECISION — Draft"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | `API-IAM-019` |
| Module | `Platform Identity` |
| Method | `POST` |
| Endpoint | `/api/v1/me/deletion-requests` |
| Purpose | `Confirm text, reason optional →`graceEndsAt`` |
| Consumer/Actor | `Authenticated + step-up` |
| Authentication | `Bearer access token ES256; kiểm iss, aud, exp, nbf, jti, sid, authVersion theo quy ước chung.` |
| Authorization | `Authenticated + step-up` |
| Basis | `DIRECT cho endpoint-level contract; DERIVED/SOURCE_REQUIRED được gắn theo từng field` |
| Status | `NEEDS USER DECISION — Draft` |
| Transaction | `Một database transaction; không gọi HTTP dependency trong transaction; rollback toàn bộ mutation cùng boundary.` |
| Side effects | `Audit theo nguồn endpoint; payload phải redact PII/secret.; Outbox/event `identity.deletion.requested`; payload/version còn Q-15 nếu chưa có schema.` |

## Sources

- `PLAN_05_IAM_IAM_Yeu_cau_xoa_tai_khoan_va_huy_yeu_cau.md`.
- `01_TONG_QUAN_DU_AN.md`.
- `02_BIEU_DO_HE_THONG.md`.
- `03_THIET_KE_CO_SO_DU_LIEU.md`.
- `04_DAC_TA_API.md`.
- `05_DAC_TA_MAN_HINH.md`.

## Tables read

- `TBL-IAM-001 — users`.
- `TBL-IAM-009 — auth_sessions`.
- `TBL-IAM-010 — refresh_tokens`.

## Tables write

- `TBL-IAM-009 — auth_sessions`.
- `TBL-IAM-016 — idempotency_keys`.
- `TBL-IAM-018 — outbox_events`.
- `TBL-IAM-010 — refresh_tokens`.
- `TBL-IAM-017 — security_audit_events`.
- `TBL-IAM-001 — users`.

## Mục chú ý

- Database owner: `identity_db`; cấm query/join xuyên database.
- Contract summary: TX L user; status`DELETION_PENDING`; revoke sessions; create outbox for Study/Work; retain 30-day cancel window.
- Vận hành: Idempotency;`identity.deletion.requested`; audit.

## Assumptions

- `N/A — Không dùng giả định âm thầm`; nội dung suy dẫn được ghi `DERIVED`.

## Conflicts

- [Q-16] Field-level JSON Schema request/response chưa đầy đủ cho toàn bộ API catalog.
- [Q-01] `authVersion` được yêu cầu bởi API/rule nhưng không có cột vật lý canonical; không ánh xạ ngầm sang `session_epoch`.
- [Q-05] Chưa có legal-hold registry account-level đầy đủ.
- [Q-15] Event payload/version chưa có schema đầy đủ cho nhiều endpoint.

## Security note

- Không log/response raw password, token, MFA secret, private key hoặc PII không cần thiết; cache theo contract.

## Performance note

- Idempotency;`identity.deletion.requested`; audit

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
