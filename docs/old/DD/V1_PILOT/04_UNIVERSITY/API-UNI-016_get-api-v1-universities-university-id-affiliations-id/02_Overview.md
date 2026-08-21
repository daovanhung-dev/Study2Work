---
title: "Overview"
order: 2
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Overview"
format: "markdown"
dd_id: "API-UNI-016"
api_name: "GET /api/v1/universities/{universityId}/affiliations/{id}"
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
| ---: | --- |
| API ID | `API-UNI-016` |
| Module | `University` |
| Method | `GET` |
| Endpoint | `/api/v1/universities/{universityId}/affiliations/{id}` |
| Purpose | trạng thái người học thuộc danh sách cho phép cho mục đích đã chấp thuận |
| Consumer/Actor | `PERM-UNI-031` + đồng ý cụ thể đang hoạt động |
| Authentication | `PERM-UNI-031` + đồng ý cụ thể đang hoạt động |
| Authorization | `PERM-UNI-031` + đồng ý cụ thể đang hoạt động |
| Basis | `DIRECT` for catalog facts; `SOURCE_REQUIRED` for missing field detail. |
| Status | `Draft — Needs Confirmation` |
| Transaction | N/A — no source-confirmed business mutation. |
| Side effects | Mọi truy cập được kiểm toán riêng tư; không lưu |

## Sources

- [04_DAC_TA_API.md](../../../../BD/04_DAC_TA_API.md): `L360` — endpoint contract.
- [01_TONG_QUAN_DU_AN.md](../../../../BD/01_TONG_QUAN_DU_AN.md) — business rules, authorization and service boundaries.
- [03_THIET_KE_CO_SO_DU_LIEU.md](../../../../BD/03_THIET_KE_CO_SO_DU_LIEU.md) — physical terminology when a table is explicitly named.
- [02_BIEU_DO_HE_THONG.md](../../../../BD/02_BIEU_DO_HE_THONG.md) — flow/concurrency context only.
- [05_DAC_TA_MAN_HINH.md](../../../../BD/05_DAC_TA_MAN_HINH.md) — screen coverage only.

## Tables read

N/A — no read table is independently materialized from this endpoint row.

## Tables write

N/A — READ-ONLY API.

## Mục chú ý

- Transport: `public_http`.

## Assumptions

- None. Missing physical keys, types, locations, columns and value sources remain `SOURCE_REQUIRED`.

## Conflicts

- [OQ-UNI-INCOMPLETE-FLOWS](../../OPEN_QUESTIONS.md#oq-uni-incomplete-flows).

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
