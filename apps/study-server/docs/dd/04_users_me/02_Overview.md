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
| API ID | `4` |
| Module | `GUEST / ACCOUNT & DISCOVERY` |
| Method | `GET` |
| Endpoint | `/api/v1/users/me` |
| Purpose | `Đọc hồ sơ user hiện tại theo identity trong Bearer JWT` |
| Consumer/Actor | `Authenticated Student` |
| Authentication | `Bearer JWT bắt buộc` |
| Authorization | `Role = Student` |
| Basis | `DIRECT — list_api.md normative + AC-02 + AC-11 + ERD V1` |
| Status | `Draft — Needs Confirmation` |
| Transaction | `N/A — read-only API` |
| Side effects | `N/A — không có mutation hoặc external side effect được source xác nhận` |

## Sources

- [`docs/lists/list_api.md`](../../../../../docs/lists/list_api.md) — API #4 contract, auth, response và error codes.
- [`AC-02 Đăng nhập`](../../../docs/diagrams/AC_UNICA/AC_01_GUEST_ACCOUNT.drawio) — sau khi phát hành token, client nạp profile.
- [`AC-11 Quản lý hồ sơ cá nhân`](../../../docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) — Student mở hồ sơ và đọc user/profile.
- [`DB_UNICA_ERD.drawio`](../../../docs/diagrams/DB_UNICA_ERD.drawio) — bảng `users` và column-level design V1.
- [`API #04 route`](../../../app/api/v1.py), [view](../../../app/modules/guest/api_04_users_me/view.py), [query](../../../app/modules/guest/api_04_users_me/query.py), [model](../../../app/modules/guest/api_04_users_me/models.py), [auth helper](../../../app/utils/auth.py), [test source](../../../tests/modules/guest/api_04_users_me/test_users_me.py).
- [`createDD-markdown template`](../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/) — cấu trúc 8 file DD.
- [`DB.sql candidate`](../../../../../infra/postgres/study-server/DB.sql) — DDL artifact, không xác nhận live schema.

## Tables read

- `users` — current source lookup theo `users.id` lấy từ numeric JWT `sub`.

## Tables write

- `N/A — read-only API`.

## Mục chú ý

- `API #4 được gọi trong AC-02 sau login và trong AC-11 khi mở hồ sơ cá nhân.`
- `Catalog lặp auth{bearer_jwt!}; route và diagram yêu cầu một Authorization header duy nhất.`
- `AC-02 nói đọc profile/role/permissions; response contract là UserProfile và current source không trả permissions.`
- `API #04 được gọi từ AC-02 sau #03 và từ AC-11 khi mở hồ sơ. AC-11 tiếp tục #13 upload avatar, #14 lưu URL vào users; #04 vẫn là GET read-only.`
- `AC-11/API #14 yêu cầu bio trong update flow, nhưng API #14 current model/query bỏ qua bio và API #04 không đọc/trả field này.`

## Boundary notes

- `Expected AC-02 wording dùng claims user_id/role; current #03/#04 dùng sub/roles. Catalog #04 không khóa claim keys.`
- `Current source map user record missing thành 401; catalog có 401 nhưng chưa nêu condition cụ thể.`
- `meta = {}` theo response helper cho request không có pagination/operation metadata.`

## Conflicts

- `DISCREPANCY: AC-02 claim names user_id/role khác current source sub/roles; catalog không định nghĩa claim keys.`
- `DISCREPANCY: AC-02 yêu cầu đọc permissions nhưng UserProfile/current API #04 response không có permissions field.`
- `SOURCE GAP: UserProfile.bio là optional; current #04 query/model không có source nên field bị omit.`
- `SOURCE/DDL GAP: current model yêu cầu users.status không null; DB.sql candidate chỉ khai báo DEFAULT, không có NOT NULL; NULL sẽ làm model mapping trả 500. Live schema chưa xác minh.`
- `POLICY OPEN: current guard dùng role trong token; query không đối chiếu users.role hoặc lọc users.status.`
- `API #14 route/module/test source tồn tại; report macro-review được cập nhật sang SOURCE_PRESENT, nhưng không có test/runtime pass claim mới.`

## Security note

- `Không trả hoặc log password_hash, token raw, secret, SQL hoặc DB detail.`
- `Current helper kiểm tra Bearer/JWT, signature/algorithm/issuer/audience/expiry, claims và Student role trước khi query; token-role freshness/status policy còn mở.`

## Performance note

- `Lookup một row theo users.id; không pagination/join. Source không lọc status và không đổi dữ liệu.`

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
