---
title: "Overview"
order: 2
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Overview"
format: markdown
dd_id: "API-IAM-024"
status: "PARTIALLY COMPLETED — SOURCE GAPS"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | `API-IAM-024` |
| Module | `Platform Identity` |
| Method | `GET` |
| Endpoint | `/.well-known/jwks.json` |
| Purpose | `Không input → active/public rollover keys` |
| Consumer/Actor | `Public` |
| Authentication | `Không yêu cầu access token.` |
| Authorization | `N/A — public/anonymous.` |
| Basis | `DIRECT cho endpoint-level contract; DERIVED/SOURCE_REQUIRED được gắn theo từng field` |
| Status | `PARTIALLY COMPLETED — SOURCE GAPS` |
| Transaction | `N/A — READ-ONLY API` |
| Side effects | `N/A — Không có side effect trong nguồn endpoint.` |

## Sources

- `PLAN_06_IAM_IAM_Quan_tri_user_global_role_va_JWKS.md`.
- `01_TONG_QUAN_DU_AN.md`.
- `02_BIEU_DO_HE_THONG.md`.
- `03_THIET_KE_CO_SO_DU_LIEU.md`.
- `04_DAC_TA_API.md`.
- `05_DAC_TA_MAN_HINH.md`.

## Tables read

- `TBL-IAM-011 — signing_keys`.

## Tables write

- `N/A — READ-ONLY API`.

## Mục chú ý

- Database owner: `identity_db`; cấm query/join xuyên database.
- Contract summary: Read signing-key metadata or config; chỉ public parameters; cache key cũ đến hết max token TTL.
- Vận hành: CDN 5 phút; ETag.

## Assumptions

- `N/A — Không dùng giả định âm thầm`; nội dung suy dẫn được ghi `DERIVED`.

## Conflicts

- [Q-16] Field-level JSON Schema request/response chưa đầy đủ cho toàn bộ API catalog.

## Security note

- Không log/response raw password, token, MFA secret, private key hoặc PII không cần thiết; cache theo contract.

## Performance note

- CDN 5 phút; ETag

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
