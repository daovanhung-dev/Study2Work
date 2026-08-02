---
title: "Overview"
order: 2
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Overview"
format: markdown
dd_id: "API-STU-004"
status: "PARTIALLY COMPLETED — SOURCE GAPS"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | `API-STU-004` |
| Module | `Study` |
| Method | `GET` |
| Endpoint | `/api/v1/catalog/courses/{slug}` |
| Purpose | `Slug → course/version curriculum preview and learner state` |
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
- `TBL-STU-014 — chapters`.
- `TBL-STU-015 — lessons`.
- `TBL-STU-027 — course_enrollments`.
- `TBL-STU-030 — progress_snapshots`.

## Tables write

- `N/A — READ-ONLY API`.

## Mục chú ý

- Database owner: `study_db`; cấm query/join xuyên database.
- Contract summary: Join current version/chapter/lesson summary; learner state pinned separately by user/course.
- Vận hành: CDN public fragment 60s; private fragment no-store.

## Assumptions

- `N/A — Không dùng giả định âm thầm`; nội dung suy dẫn được ghi `DERIVED`.

## Conflicts

- [Q-16] Field-level JSON Schema request/response chưa đầy đủ cho toàn bộ API catalog.
- [Q-14] Catalog cần bổ sung taxonomy/prerequisite/file candidate tables theo response thực tế.

## Security note

- Không log/response raw password, token, MFA secret, private key hoặc PII không cần thiết; cache theo contract.

## Performance note

- CDN public fragment 60s; private fragment no-store

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
