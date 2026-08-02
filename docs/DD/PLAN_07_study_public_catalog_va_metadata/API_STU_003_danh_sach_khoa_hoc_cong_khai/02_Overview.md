---
title: "Overview"
order: 2
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Overview"
format: markdown
dd_id: "API-STU-003"
status: "PARTIALLY COMPLETED — SOURCE GAPS"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | `API-STU-003` |
| Module | `Study` |
| Method | `GET` |
| Endpoint | `/api/v1/catalog/courses` |
| Purpose | `Page, q, skill, level → standalone published courses` |
| Consumer/Actor | `Public` |
| Authentication | `Không yêu cầu access token.` |
| Authorization | `N/A — public/anonymous.` |
| Basis | `DIRECT cho endpoint-level contract; DERIVED/SOURCE_REQUIRED được gắn theo từng field` |
| Status | `PARTIALLY COMPLETED — SOURCE GAPS` |
| Transaction | `N/A — READ-ONLY API` |
| Side effects | `N/A — Không có side effect trong nguồn endpoint.` |

## Sources

- `PLAN_07_STU_Study_Public_catalog_va_metadata.md`.
- `01_TONG_QUAN_DU_AN.md`.
- `02_BIEU_DO_HE_THONG.md`.
- `03_THIET_KE_CO_SO_DU_LIEU.md`.
- `04_DAC_TA_API.md`.
- `05_DAC_TA_MAN_HINH.md`.

## Tables read

- `TBL-STU-011 — courses`.
- `TBL-STU-012 — course_versions`.
- `TBL-STU-057 — course_skill_outcomes`.
- `TBL-STU-056 — study_skills`.

## Tables write

- `N/A — READ-ONLY API`.

## Mục chú ý

- Database owner: `study_db`; cấm query/join xuyên database.
- Contract summary: Current published course version only; FTS/trigram; independently enrollable flag always true V1.
- Vận hành: CDN 60s.

## Assumptions

- `N/A — Không dùng giả định âm thầm`; nội dung suy dẫn được ghi `DERIVED`.

## Conflicts

- [Q-16] Field-level JSON Schema request/response chưa đầy đủ cho toàn bộ API catalog.
- [Q-14] Catalog cần bổ sung taxonomy/prerequisite/file candidate tables theo response thực tế.

## Security note

- Không log/response raw password, token, MFA secret, private key hoặc PII không cần thiết; cache theo contract.

## Performance note

- CDN 60s

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
