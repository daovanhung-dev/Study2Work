---
title: "Overview"
order: 2
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Overview"
format: "markdown"
dd_id: "API-IAM-022"
api_name: "PUT /api/v1/admin/users/{userId}/status"
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
| ---: | --- |
| API ID | `API-IAM-022` |
| Module | `Platform Identity` |
| Method | `PUT` |
| Endpoint | `/api/v1/admin/users/{userId}/status` |
| Purpose | người dùng |
| Consumer/Actor | `PERM-IAM-002` + MFA |
| Authentication | `PERM-IAM-002` + MFA |
| Authorization | `PERM-IAM-002` + MFA |
| Basis | `DIRECT` for catalog facts; `SOURCE_REQUIRED` for missing field detail. |
| Status | `Draft — Needs Confirmation` |
| Transaction | TBD — mutation candidate has no complete transaction boundary at endpoint detail. |
| Side effects | Khóa lặp; kiểm toán trước/sau; sự kiện đổi trạng thái |

## Sources

- [04_DAC_TA_API.md](../../../../BD/04_DAC_TA_API.md): `L108` — endpoint contract.
- [01_TONG_QUAN_DU_AN.md](../../../../BD/01_TONG_QUAN_DU_AN.md) — business rules, authorization and service boundaries.
- [03_THIET_KE_CO_SO_DU_LIEU.md](../../../../BD/03_THIET_KE_CO_SO_DU_LIEU.md) — physical terminology when a table is explicitly named.
- [02_BIEU_DO_HE_THONG.md](../../../../BD/02_BIEU_DO_HE_THONG.md) — flow/concurrency context only.
- [05_DAC_TA_MAN_HINH.md](../../../../BD/05_DAC_TA_MAN_HINH.md) — screen coverage only.

## Tables read

N/A — no read table is independently materialized from this endpoint row.

## Tables write

SOURCE_REQUIRED — catalog describes a mutation candidate without a certain physical target table.

## Mục chú ý

- Transport: `public_http`.

## Assumptions

- None. Missing physical keys, types, locations, columns and value sources remain `SOURCE_REQUIRED`.

## Conflicts

- [OQ-IAM-AUTHVERSION](../../OPEN_QUESTIONS.md#oq-iam-authversion).

## Security note

- Apply the global BD prohibition on logging or returning secrets, tokens, raw sensitive content, SQL and stack traces.
- Authorization, tenant and ownership checks are server-authoritative.

## Performance note

- Apply pagination, cache, rate-limit and retry behavior only where the API catalog or BD §2.3–§2.4 states it.

---
## Phụ lục đối chiếu template Markdown

- Template Markdown: `.agent/docs/dd/DD_API_Template_MD/02_Overview.md`.
- Workbook/sheet prototype: `DD_API_Template(1).xlsx` / `Overview`.
- Nội dung nghiệp vụ được sinh từ Basic Design hiện hành; đây không phải khẳng định về chuyển đổi lossless từ Excel.
