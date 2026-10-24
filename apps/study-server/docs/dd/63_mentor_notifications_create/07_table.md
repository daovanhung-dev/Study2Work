---
title: "Định nghĩa table"
order: 7
dd_id: "63"
api_name: "Tạo và phát thông báo"
source_sheet: "table"
status: "Draft — Needs Confirmation"
---

# Định nghĩa table — Notification, recipients và Operation

## Thông tin mapping

| Thuộc tính | Giá trị |
|---|---|
| Physical target | `SOURCE_REQUIRED`; chưa chọn legacy BIGINT hay V1-PILOT UUID model. |
| Logical entities | Notification, recipient association, Operation/delivery job. |
| Operation | Logical INSERT Notification + recipients; create/queue Operation. |
| Data Mapping step | 3–5 |
| Evidence | AC-25 nodes n6/n7; catalog #63/#64; Notification/Operation schemas; DB guide/legacy/Pilot comparison. |
| Runtime | API #63 `UNWIRED / NOT_FOUND`. |

## Mapping ghi logic — Notification

| STT | Field logic | Kiểu/yêu cầu | Nguồn giá trị | Mapping candidate | Bằng chứng/trạng thái |
|---:|---|---|---|---|---|
| 1 | Notification ID | Catalog domain int64 | Persistence | Legacy `BIGSERIAL`; pilot UUID | Conflict; no canonical ID source. |
| 2 | Title | string! | Request `title` | Legacy/pilot title VARCHAR(200) | Field trực tiếp; giới hạn 200 chỉ là candidate. |
| 3 | Content | int64! direct | Request `content` | Legacy TEXT / pilot body VARCHAR(4000) | DISCREPANCY; không tự ép kiểu hoặc tạo lookup. |
| 4 | Sender | Mentor identity | Bearer principal | Legacy `sender_id BIGINT`; pilot has no sender field | Identity mapping/model conflict. |
| 5 | Channels | string! direct | Request `channels` | Legacy không có channel; pilot delivery cho phép `IN_APP` hoặc `EMAIL` | Encoding/token và mapping Push là SOURCE_REQUIRED. |
| 6 | Created time | Notification.created_at | Persistence clock | Legacy TIMESTAMP; pilot timestamptz | Timezone/clock policy SOURCE_REQUIRED. |

## Mapping ghi logic — recipients

| STT | Field logic | Kiểu/yêu cầu | Nguồn giá trị | Mapping candidate | Bằng chứng/trạng thái |
|---:|---|---|---|---|---|
| 1 | Recipient IDs | `recipients:string!` direct | Body | Đề xuất CSV Student ID int64 dạng thập phân | Chỉ là DERIVED; cần duyệt user/enrollment key và parser. |
| 2 | Course association | Cần để kiểm tra quyền | Đề xuất `course_id:int64!` | Không có trong request trực tiếp | Đề xuất sửa contract, chưa phải input hiện tại. |
| 3 | Recipient relation | Notification × từng Student được chọn | AC-25 select/insert | Legacy `notifications.user_id` lưu một recipient mỗi row; không có bảng recipient. | Chưa thể biểu diễn nhóm notification/status nếu thiếu relation được duyệt. |
| 4 | Eligibility | Enrollment active trong course được cấp quyền | #62 roster + DB enrollment relation | Legacy/pilot schemas khác nhau | Server phải kiểm tra lại; status và identity mapping chính xác là SOURCE_REQUIRED. |

## Mapping Operation logic và queue

| STT | Field logic/effect | Nguồn giá trị | Rule/trạng thái |
|---:|---|---|---|
| 1 | Operation ID | Async job layer | Reusable schema UUID; API #18 row type discrepancy remains. |
| 2 | Operation owner | Authenticated Mentor | Reusable `owner_id:int64`; principal mapping SOURCE_REQUIRED. |
| 3 | Initial status/kind | Job được API #63 chấp nhận | Enum và lifecycle chưa định nghĩa; không tự gán token. |
| 4 | Notification ID handoff | Notification persistence | API #64 yêu cầu int64; Operation schema không có notification reference. SOURCE_REQUIRED. |
| 5 | Queue/outbox record | Dispatch bất đồng bộ | Chưa có bảng/provider/transaction Study được duyệt; không tự tạo physical target. |
| 6 | Phát ra bên ngoài | Push/Email provider | Diagram xác nhận ý định dùng channel; provider, retry và aggregation là SOURCE_REQUIRED. |

## SQL mapping

Không có câu INSERT vật lý được duyệt. Legacy `notifications` và V1-PILOT `notifications`/`notification_deliveries` không tương thích về ID, recipient relation, sender, channels và delivery fields. Không viết SQL giả hoặc gộp hai schema.

## Tính nhất quán giữa các API

- #62 cần trả recipient key; response trực tiếp `Page<Course>` đang lệch với learner roster.
- #63 cần course scope và phải trả notification ID để gọi #64; request/response hiện tại chưa cung cấp đủ dữ liệu.
- API #18 theo dõi Operation nhưng không thay thế delivery status #64; hai ID/type cần phân biệt.
---
## Phụ lục đối chiếu nguồn Excel
- Workbook nguồn: `DD_API_Template(1).xlsx`
- Sheet nguồn: `table`
- Dimension: `A1:BA35`
- Trạng thái: `visible`
- Số ô có dữ liệu/công thức: `19`
- Số vùng merge: `5`

<details>
<summary>Danh sách vùng merge</summary>

- `W34:BA34`
- `W14:BA14`
- `W15:BA15`
- `W19:BA19`
- `W32:BA32`

</details>

<details>
<summary>Bản ghi từng ô có dữ liệu hoặc công thức</summary>

| Hàng | Ô | Giá trị nguồn | Công thức nguồn |
|---:|---|---|---|
| 2 | `A2` | № |  |
| 2 | `B2` | Tên table |  |
| 3 | `B3` | SB |  |
| 3 | `S3` | Độ dài |  |
| 3 | `T3` | Dấu phẩy thập phân |  |
| 3 | `U3` | Bắt buộc |  |
| 3 | `V3` | Main key |  |
| 3 | `W3` | Nội dung setting |  |
| 4 | `B4` | № |  |
| 4 | `C4` | Item ID |  |
| 4 | `I4` | Item name |  |
| 4 | `O4` | Kiểu |  |
| 5 | `A5` | 1 |  |
| 5 | `B5` | table id |  |
| 5 | `I5` | table name |  |
| 6 | `B6` | Update |  |
| 6 | `I6` | Trường hợp số record get được từ xử lý 3. của sheet [３．Data mapping]  > 0 |  |
| 21 | `B21` | Insert |  |
| 21 | `I21` | Trường hợp số record get được từ xử lý 3. của sheet [３．Data mapping]  = 0 |  |

</details>
