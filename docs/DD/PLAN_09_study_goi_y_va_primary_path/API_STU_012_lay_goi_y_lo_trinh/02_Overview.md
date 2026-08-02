---
title: "Overview"
order: 2
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Overview"
format: markdown
dd_id: "API-STU-012"
status: "PARTIALLY COMPLETED — SOURCE GAPS"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | `API-STU-012` |
| Module | `Study` |
| Method | `GET` |
| Endpoint | `/api/v1/me/path-recommendations` |
| Purpose | `→ top 3 path versions, score bands/reasons/run version` |
| Consumer/Actor | `Learner active + onboarding completed` |
| Authentication | `Bearer access token ES256; kiểm iss, aud, exp, nbf, jti, sid, authVersion theo quy ước chung.` |
| Authorization | `Learner active + onboarding completed` |
| Basis | `DIRECT cho endpoint-level contract; DERIVED/SOURCE_REQUIRED được gắn theo từng field` |
| Status | `PARTIALLY COMPLETED — SOURCE GAPS` |
| Transaction | `N/A — READ-ONLY API` |
| Side effects | `N/A — Không có side effect trong nguồn endpoint.` |

## Sources

- `PLAN_09_STU_Study_Goi_y_va_primary_path.md`.
- `01_TONG_QUAN_DU_AN.md`.
- `02_BIEU_DO_HE_THONG.md`.
- `03_THIET_KE_CO_SO_DU_LIEU.md`.
- `04_DAC_TA_API.md`.
- `05_DAC_TA_MAN_HINH.md`.

## Tables read

- `TBL-STU-002 — learner_profiles`.
- `TBL-STU-007 — onboarding_submissions`.
- `TBL-STU-008 — path_recommendation_runs`.
- `TBL-STU-010 — learning_path_versions`.
- `TBL-STU-009 — learning_paths`.

## Tables write

- `N/A — READ-ONLY API`.

## Mục chú ý

- Database owner: `study_db`; cấm query/join xuyên database.
- Contract summary: R latest immutable recommendation run/items; omit unpublished path and mark stale if catalog changed.
- Vận hành: Private no-store.

## Assumptions

- `N/A — Không dùng giả định âm thầm`; nội dung suy dẫn được ghi `DERIVED`.

## Conflicts

- [Q-16] Field-level JSON Schema request/response chưa đầy đủ cho toàn bộ API catalog.
- [Q-10] Recommendation item/score-band schema chưa được định nghĩa ngoài arrays/JSON snapshot.

## Security note

- Không log/response raw password, token, MFA secret, private key hoặc PII không cần thiết; cache theo contract.

## Performance note

- Private no-store

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
