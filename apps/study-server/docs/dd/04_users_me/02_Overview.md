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
| Purpose | `Nạp profile hiện tại theo user_id trong Bearer JWT` |
| Consumer/Actor | `Authenticated Student` |
| Authentication | `Bearer JWT bắt buộc` |
| Authorization | `Role = Student` |
| Basis | `DIRECT — list_api.md normative + AC-02 + AC-11 + ERD V1` |
| Status | `Draft — Needs Confirmation` |
| Transaction | `N/A — read-only API` |
| Side effects | `N/A — không có mutation hoặc external side effect được source xác nhận` |

## Sources

- [`docs/lists/list_api.md`](../../../docs/lists/list_api.md) — API #4 contract, auth, response và error codes.
- [`AC-02 Đăng nhập`](../../../docs/diagrams/AC_UNICA/AC_01_GUEST_ACCOUNT.drawio) — sau khi phát hành token, client nạp profile.
- [`AC-11 Quản lý hồ sơ cá nhân`](../../../docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) — Student mở hồ sơ và đọc user/profile.
- [`DB_UNICA_ERD.drawio`](../../../docs/diagrams/DB_UNICA_ERD.drawio) — bảng `users` và column-level design V1.
- [`createDD-markdown template`](../../../.agents/skills/create_dd/docs/dd/DD_API_Template_MD/) — cấu trúc 8 file DD.

## Tables read

- `users` — lookup theo `users.id` từ JWT claim `user_id`.

## Tables write

- `N/A — read-only API`.

## Mục chú ý

- `API #4 được gọi trong AC-02 sau login và trong AC-11 khi mở hồ sơ cá nhân.`
- `Nguồn lặp auth{bearer_jwt!} được chuẩn hóa thành một Authorization header.`
- `Không thêm permissions field vì response contract chỉ khai báo UserProfile.`

## Assumptions

- `JWT chứa claim user_id và role theo flow AC-02; exact JWT library/claim validation chưa được source xác nhận.`
- `Nếu token hợp lệ nhưng user record không tồn tại, dùng 401 vì contract không khai báo 404; đây là assumption design-only.`
- `meta = {}` vì API #4 không khai báo pagination/operation metadata.`

## Conflicts

- `DISCREPANCY/TBD: UserProfile.bio có trong contract nhưng ERD users không có column tương ứng; không tự tạo profile table/column.`
- `DISCREPANCY: diagram/list lặp auth{bearer_jwt!}; DD mô tả một header Authorization duy nhất.`

## Security note

- `Không trả hoặc log password_hash, token raw, secret, SQL hoặc DB detail.`
- `JWT phải được kiểm tra chữ ký, expiry và role trước khi truy vấn profile.`

## Performance note

- `Lookup theo primary key users.id; không pagination và không join được source xác nhận.`

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
