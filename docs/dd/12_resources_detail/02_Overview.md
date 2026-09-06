---
title: "Overview"
order: 2
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Overview"
format: markdown
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | `12` |
| Module | `GUEST / ACCOUNT & DISCOVERY` |
| Method | `GET` |
| Endpoint | `/api/v1/resources/{resource_id}` |
| Purpose | `Lấy metadata của một resource và URL có thể mở/tải; URL có thể là URL trực tiếp hoặc signed URL theo access rule.` |
| Consumer/Actor | `Guest / resource viewer` |
| Authentication | `Public; không yêu cầu Bearer token theo list_api.md` |
| Authorization | `Public theo contract; visibility/access check trong AC-06 là phần cần xác nhận.` |
| Basis | `DIRECT — approved API contract + AC-06; parent-course gate và storage signing là DERIVED/TBD.` |
| Status | `Draft — Needs Confirmation` |
| Transaction | `N/A — read-only API` |
| Side effects | `Không mutation DB; có thể gọi Object Storage signer khi resource private.` |

## Sources

- [`docs/lists/list_api.md`](../../../docs/lists/list_api.md) — API #12, path `resource_id`, `ApiEnvelope<Resource>` và status/error contract.
- [`AC_01_GUEST_ACCOUNT.drawio`](../../../docs/diagrams/AC_UNICA/AC_01_GUEST_ACCOUNT.drawio) — AC-06, access decision và Object Storage signed URL.
- [`00_AC_API_INDEX.md`](../../../docs/diagrams/AC_UNICA/00_AC_API_INDEX.md) — resource public hoặc user có quyền truy cập.
- [`DB_UNICA_ERD.drawio`](../../../docs/diagrams/DB_UNICA_ERD.drawio) — `resources.lesson_id → lessons.id → courses.id`.
- [`createDD_MARKDOWN_SKILL.md`](../../../.agents/skills/create_dd/docs/dd/createDD_MARKDOWN_SKILL.md) — template và traceability rules.

## Tables read

- `resources` — đọc metadata và URL theo `resource_id`.
- `lessons` — xác định course sở hữu resource.
- `courses` — kiểm tra trạng thái public của parent course theo giả định design.

## Tables write

- `N/A — READ-ONLY API; không có DB mutation.`

## Mục chú ý

- API #12 được gọi sau khi client chọn một resource từ API #11.
- Contract chỉ có field `data.url`; không tạo field `signed_url` riêng.
- API #12 không nhận query hoặc request body.
- Contract hiện chỉ khai báo `404` và `500`; không tự thêm `403` hoặc `503`.

## Assumptions

- `resource_id` map trực tiếp tới `resources.id`.
- Resource chỉ được expose qua flow public khi parent course được xác nhận `PUBLISHED`; đây là derived rule cần xác nhận.
- Resource public trả `resources.url`; resource private cần Object Storage signer và kết quả signer được map vào `data.url`.
- `Resource.visibility` là field bắt buộc của contract nhưng chưa có cột nguồn trong ERD; giữ `TBD`, không tạo cột mới.
- `resources.url` và `resources.lesson_id` được ERD ghi `NOT NULL`, trong khi contract cho phép optional; giữ discrepancy ở Response.

## Conflicts

- `DISCREPANCY: list_api.md khai báo Public/no Bearer token và chỉ có 404/500, nhưng AC-06/diagram mô tả public-or-authorized access và nhánh 403.`
- `DISCREPANCY: contract yêu cầu Resource.visibility nhưng ERD resources không có cột visibility.`
- `DISCREPANCY/TBD: diagram có Object Storage signer nhưng không có adapter/API, request, expiry hoặc error contract.`
- `RUNTIME_STATUS: Study server DECLARED_NOT_RUNNABLE; DD không phải bằng chứng runtime.`

## Security note

- Không trả object key nội bộ, credential, token, raw SQL hoặc stack trace.
- Không decode Bearer token trong nhánh public hiện tại của contract.
- Không expose resource private khi access policy chưa được approved; behavior 403/404 cần chốt trước implementation.
- Signed URL phải có giới hạn thời gian theo storage policy, nhưng expiry chưa có source.

## Performance note

- Lookup theo `resources.id`; parent scope đi qua `lessons` và `courses`.
- Không thêm pagination, cache, index hoặc retry policy ngoài source hiện có.
- Storage signer là external dependency tùy nhánh; timeout/failure mapping chưa được đặc tả và hiện quy về contract `500` nếu cần trả lỗi.

---
## Phụ lục đối chiếu template Markdown

- Template: `../../../.agents/skills/create_dd/docs/dd/DD_API_Template_MD/02_Overview.md`.
- Sheet logic: `Overview`.
