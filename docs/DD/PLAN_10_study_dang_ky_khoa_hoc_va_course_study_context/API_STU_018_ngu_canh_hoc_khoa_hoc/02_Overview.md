---
title: "Overview"
order: 2
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Overview"
format: markdown
dd_id: "API-STU-018"
status: "PARTIALLY COMPLETED — SOURCE GAPS"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | `API-STU-018` |
| Module | `Study` |
| Method | `GET` |
| Endpoint | `/api/v1/courses/{courseId}/study` |
| Purpose | `Optional enrollment ID → pinned curriculum, access/progress` |
| Consumer/Actor | `Enrolled learner` |
| Authentication | `Bearer access token ES256; kiểm iss, aud, exp, nbf, jti, sid, authVersion theo quy ước chung.` |
| Authorization | `Enrolled learner` |
| Basis | `DIRECT cho endpoint-level contract; DERIVED/SOURCE_REQUIRED được gắn theo từng field` |
| Status | `PARTIALLY COMPLETED — SOURCE GAPS` |
| Transaction | `N/A — READ-ONLY API` |
| Side effects | `N/A — Không có side effect trong nguồn endpoint.` |

## Sources

- `PLAN_10_STU_Study_ang_ky_khoa_hoc_va_course_study_context.md`.
- `01_TONG_QUAN_DU_AN.md`.
- `02_BIEU_DO_HE_THONG.md`.
- `03_THIET_KE_CO_SO_DU_LIEU.md`.
- `04_DAC_TA_API.md`.
- `05_DAC_TA_MAN_HINH.md`.

## Tables read

- `TBL-STU-002 — learner_profiles`.
- `TBL-STU-027 — course_enrollments`.
- `TBL-STU-011 — courses`.
- `TBL-STU-012 — course_versions`.
- `TBL-STU-014 — chapters`.
- `TBL-STU-015 — lessons`.
- `TBL-STU-016 — content_blocks`.
- `TBL-STU-030 — progress_snapshots`.

## Tables write

- `N/A — READ-ONLY API`.

## Mục chú ý

- Database owner: `study_db`; cấm query/join xuyên database.
- Contract summary: Predicate enrollment owner + course; join pinned immutable version, chapters, lessons, snapshots.
- Vận hành: Private; conditional ETag on content version.

## Assumptions

- `N/A — Không dùng giả định âm thầm`; nội dung suy dẫn được ghi `DERIVED`.

## Conflicts

- [Q-16] Field-level JSON Schema request/response chưa đầy đủ cho toàn bộ API catalog.

## Security note

- Không log/response raw password, token, MFA secret, private key hoặc PII không cần thiết; cache theo contract.

## Performance note

- Private; conditional ETag on content version

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
