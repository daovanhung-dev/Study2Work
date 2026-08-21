---
title: "Overview"
order: 2
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Overview"
format: "markdown"
dd_id: "API-INT-011"
api_name: "GET wss://work-api.study2work.vn/api/v1/realtime"
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
| ---: | --- |
| API ID | `API-INT-011` |
| Module | `Integration and Realtime` |
| Method | `GET` |
| Endpoint | `wss://work-api.study2work.vn/api/v1/realtime` |
| Purpose | SOURCE_REQUIRED — endpoint row does not split input and output fields. |
| Consumer/Actor | Ứng viên/thành viên Work đã xác thực |
| Authentication | WebSocket protocol authentication |
| Authorization | Ứng viên/thành viên Work đã xác thực |
| Basis | `DIRECT` for catalog facts; `SOURCE_REQUIRED` for missing field detail. |
| Status | `Draft — Needs Confirmation` |
| Transaction | N/A — no source-confirmed business mutation. |
| Side effects | N/A — WebSocket lifecycle is part of the protocol contract. |

## Sources

- [04_DAC_TA_API.md](../../../../BD/04_DAC_TA_API.md): `L493` — endpoint contract.
- [01_TONG_QUAN_DU_AN.md](../../../../BD/01_TONG_QUAN_DU_AN.md) — business rules, authorization and service boundaries.
- [03_THIET_KE_CO_SO_DU_LIEU.md](../../../../BD/03_THIET_KE_CO_SO_DU_LIEU.md) — physical terminology when a table is explicitly named.
- [02_BIEU_DO_HE_THONG.md](../../../../BD/02_BIEU_DO_HE_THONG.md) — flow/concurrency context only.
- [05_DAC_TA_MAN_HINH.md](../../../../BD/05_DAC_TA_MAN_HINH.md) — screen coverage only.

## Tables read

N/A — no read table is independently materialized from this endpoint row.

## Tables write

N/A — READ-ONLY API.

## Mục chú ý

- Transport: `websocket`.
- WebSocket delivery is not modeled as a REST response envelope.

## Assumptions

- None. Missing physical keys, types, locations, columns and value sources remain `SOURCE_REQUIRED`.

## Conflicts

N/A — no official review gap matched automatically; endpoint field detail may still be SOURCE_REQUIRED.

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
