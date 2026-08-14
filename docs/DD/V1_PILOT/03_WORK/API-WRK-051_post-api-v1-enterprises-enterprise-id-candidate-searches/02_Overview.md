---
title: "Overview"
order: 2
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Overview"
format: "markdown"
dd_id: "API-WRK-051"
api_name: "POST /api/v1/enterprises/{enterpriseId}/candidate-searches"
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
| ---: | --- |
| API ID | `API-WRK-051` |
| Module | `Work` |
| Method | `POST` |
| Endpoint | `/api/v1/enterprises/{enterpriseId}/candidate-searches` |
| Purpose | ứng viên đã che dữ liệu + giải thích đối sánh tự nhiên; hồ sơ tài trợ riêng/gắn nhãn |
| Consumer/Actor | `PERM-WRK-020` + quyền tìm kiếm đang hoạt động |
| Authentication | `PERM-WRK-020` + quyền tìm kiếm đang hoạt động |
| Authorization | `PERM-WRK-020` + quyền tìm kiếm đang hoạt động |
| Basis | `DIRECT` for catalog facts; `SOURCE_REQUIRED` for missing field detail. |
| Status | `Draft — Needs Confirmation` |
| Transaction | TBD — mutation candidate has no complete transaction boundary at endpoint detail. |
| Side effects | Kiểm toán ID truy vấn/bộ lọc/kết quả; 60/phút; không dùng bộ nhớ đệm chung |

## Sources

- [04_DAC_TA_API.md](../../../../BD/04_DAC_TA_API.md): `L319` — endpoint contract.
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

- [OQ-WRK-SEARCH-CONSENT](../../OPEN_QUESTIONS.md#oq-wrk-search-consent).

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
