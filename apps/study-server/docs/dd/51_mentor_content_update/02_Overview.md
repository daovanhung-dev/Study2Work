---
title: "Overview"
order: 2
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Overview"
format: markdown
dd_id: "51"
api_name: "Cập nhật nội dung Mentor"
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | #51 |
| Module | MENTOR / TEACHING |
| Method | PUT |
| Endpoint | `/api/v1/mentor/content/{content_id}` |
| Purpose | Cập nhật Content và lưu snapshot phiên bản trước đó theo AC-22. |
| Consumer/Actor | Mentor |
| Authentication | Bearer JWT; shared guard yêu cầu role `MENTOR`. |
| Authorization | Direct owner `courses.mentor_id` của course chứa Content; fallback từ API #49, chưa xác nhận assigned Mentor. |
| Basis | Path/response/errors/`UPDATE Content + version` là DIRECT; body/history DDL/lifecycle là DERIVED. |
| Status | Runtime local wired; DD Draft — Needs Confirmation. |
| Transaction | Lock Content và Course, insert snapshot, update `contents`, commit cùng transaction; query/view không tự commit. |
| Side effects | Tạo snapshot trong `content_versions`, thay `content_type/title/payload`, set current `status=PENDING_REVIEW`; giữ nguyên course, parent và order. |

## Sources

- [API catalog #51](../../../../../docs/lists/list_api.md) — path-only request, `ApiEnvelope<Content>`, exact response/error codes.
- [AC-22](../../diagrams/AC_UNICA/AC_03_MENTOR_TEACHING.drawio) — Mentor cập nhật `Content + version`.
- [AC-33](../../diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio) — review queue đọc `PENDING_REVIEW`; reviewer đọc content/version/author.
- [API #49 current source](../../../app/modules/mentor/api_49_mentor_content_list/) và [API #50 DD](../50_mentor_content_create/02_Overview.md) — direct-owner pattern và body fields `content_type/title/payload`.
- [Legacy DB guide](../../diagrams/DB_UNICA_TABLES.md), [migration 006](../../../../../infra/postgres/study-server/migrations/006_contents.sql), [migration 007](../../../../../infra/postgres/study-server/migrations/007_content_versions.sql) — checked-in BIGINT schema artifacts; không chứng minh live migration.
- [V1-PILOT DDL](../../../../../infra/postgres/02_study_db.sql) — model `content_blocks` khác boundary, không được dùng cho Content này.

## Tables read

- `contents` joined với `courses` để khóa target, tree placement và direct owner.
- `content_versions` để cấp `version_no` kế tiếp khi lưu snapshot.

## Tables write

- `content_versions`: insert toàn bộ trạng thái Content trước update; `archived_by` là Mentor tạo thay đổi kế tiếp, không xác nhận tác giả gốc.
- `contents`: update ba body fields và `status='PENDING_REVIEW'`; giữ `course_id`, `parent_id`, `content_order`.

## Mục chú ý

- Catalog và diagram không định nghĩa body. Runtime dùng full replacement `{content_type, title, payload}` từ API #50 dưới dạng `DERIVED`; body bắt buộc, field thừa bị từ chối.
- `content_type` giữ open string; `payload` phải là JSON object. Enum member, title bounds/normalization và payload subtype chưa có nguồn.
- Mỗi PUT archive trạng thái hiện tại rồi cập nhật projection mới trong một transaction. Version của current row là implicit `MAX(content_versions.version_no)+1`.
- API response không thêm version field và giữ shared `Content` shape cùng exact catalog codes.
- Snapshot bảo toàn trạng thái cũ trong bảng history nhưng API #51 không xác định public reader dùng phiên bản nào sau update.

## Assumptions

- Direct course owner authorization được suy từ API #49; assigned/co-owner access chưa hỗ trợ.
- Body fields, requiredness, full replacement, `PENDING_REVIEW`, status snapshot và `content_versions` schema/sequence là `DERIVED`, chưa được approve.
- `archived_by` ghi Mentor thực hiện lần update kế tiếp; không được gọi là tác giả ban đầu.

## Conflicts

- Catalog/diagram không khai báo body nhưng PUT phải mang dữ liệu; implementation body là `DERIVED`.
- AC-22 yêu cầu version; legacy `contents` không có lịch sử. Migration 007 thêm legacy snapshot table nhưng live schema/deployment chưa xác minh.
- AC-33 đề cập author nhưng Content source không có tác giả gốc. AC-33 approval `APPROVED/PUBLISHED` và API #52 publish/unpublish chưa được nối bằng revision selector.
- Snapshot lưu bản published trước đó nhưng current `contents` row chuyển sang `PENDING_REVIEW`; không khẳng định published snapshot tiếp tục được serve.

## Security note

Xác thực Mentor trước DB; lấy course scope từ Content trong DB; khóa Content và Course khi kiểm tra owner/update. Không nhận owner, course, status hoặc tree placement từ body.

## Performance note

Một locked target lookup, một insert snapshot có `MAX(version_no)` trên PK index, một update và một commit. Row lock theo Content serialize PUT cạnh tranh; không có optimistic version token hoặc 409 trong catalog.

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
