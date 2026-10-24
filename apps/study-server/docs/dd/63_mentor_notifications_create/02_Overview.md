---
title: "Overview"
order: 2
dd_id: "63"
api_name: "Tạo và phát thông báo"
source_sheet: "Overview"
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | #63 |
| Module | MENTOR / TEACHING & SUPPORT — AC-25 |
| Method | `POST` |
| Endpoint | `/api/v1/mentor/notifications` |
| Purpose | Tạo thông báo cho nhóm học viên Mentor đã chọn và chấp nhận yêu cầu phát bất đồng bộ. |
| Consumer/Actor | Mentor |
| Authentication | Bearer JWT |
| Authorization | Role Mentor; quyền trên course và từng recipient cần được xác thực. Body trực tiếp hiện không có `course_id`, nên chưa đủ dữ liệu để ràng buộc danh sách người nhận vào course đã chọn. |
| Basis | Method/path/body/response/status/errors lấy trực tiếp từ catalog; bước ghi Notification + recipients và Push/Email DIRECT từ AC-25 diagram; phần encoding, identity và persistence chưa được xác nhận. |
| Status | `Draft — Needs Confirmation` |
| Current runtime state | `UNWIRED / NOT_FOUND` — chưa có route, module, provider hoặc test cho API #63 trong Study source. |
| Transaction | Ranh giới giao dịch DB/queue chưa được nguồn chốt; không coi provider delivery là đồng bộ trong transaction. |
| Side effects | Tạo Notification và recipients, sau đó yêu cầu Push/Email theo channel; API trả 202 chỉ xác nhận đã nhận/chấp nhận xử lý, không chứng minh đã phát thành công. |

## Sources

- [API catalog và reusable schemas](../../../../../docs/lists/list_api.md) — #18, #62–#64, #93, Notification, NotificationDelivery, Operation và Payment.
- [AC/API index, AC-25](../../diagrams/AC_UNICA/00_AC_API_INDEX.md).
- [AC-25 activity diagram](../../diagrams/AC_UNICA/AC_03_MENTOR_TEACHING.drawio) — node/edge #62 → chọn recipient → #63 → ghi Notification + recipients → Push/Email → #64; node #18 đứng riêng, không có edge.
- [API #62 overview](../62_mentor_course_students/02_Overview.md) và [Open Questions #62](../62_mentor_course_students/OPEN_QUESTIONS.md) — roster contract conflict và recipient key chưa chốt.
- [API #64 catalog row](../../../../../docs/lists/list_api.md) — trạng thái delivery theo `notification_id:int64`.
- [API #18 overview](../18_operations/02_Overview.md) và [Open Questions #18](../18_operations/OPEN_QUESTIONS.md) — Định danh Operation, persistence và kiểu result chưa chốt.
- [API #43 overview](../43_users_me_notifications/02_Overview.md), [API #45 overview](../45_notifications_read_all/02_Overview.md) — Notification schema/read-state không đồng nhất với delivery status.
- [API #50 logical mapping precedent](../50_mentor_content_create/07_table.md) — ghi logical operation khi physical persistence chưa có bằng chứng.
- [DB table guide](../../diagrams/DB_UNICA_TABLES.md) và [legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql) — mô hình notification BIGINT candidate; không có recipient table riêng.
- [V1-PILOT DDL](../../../../../infra/postgres/02_study_db.sql) — mô hình UUID learner/notification/delivery thay thế; không coi là live schema.
- [Study router](../../../app/api/v1.py), [middleware](../../../app/core/middleware.py), [API Guidelines](../../../../../contracts/api-guidelines/README.md).
- [Canonical DD Markdown template](../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/) — tám sheet; fingerprint trong [PLAN_RESULT](./PLAN_RESULT.md).

## Tables/entities đọc

- `notifications` — physical candidate trong legacy BIGINT schema; fields không đủ để lưu channels, delivery lifecycle hoặc group notification.
- `notification_deliveries` — chỉ có ở V1-PILOT UUID model; channel/status không tương thích đầy đủ với catalog/diagram.
- `NotificationRecipient` — logical entity theo AC flow; không có bảng cùng tên trong legacy DB guide/DDL.
- `Operation` — logical response/job; Study physical table, enum và lifecycle chưa có nguồn.

## Tables/entities ghi

- `Notification` và associations tới người nhận — yêu cầu logic DIRECT từ diagram; physical target chưa được chọn.
- Delivery work và `Operation` — cần cho 202/tracking; queue/persistence chưa được chốt.

## Mục chú ý

- Giữ nguyên body trực tiếp theo catalog: `recipients:string!`, `title:string!`, `content:int64!`, `channels:string!`.
- AC-25 cùng Notification schema dùng nội dung dạng text; `content:int64` là `DISCREPANCY`, không tự đổi kiểu trực tiếp thành string.
- UI chọn người nhận trong một course; #63 body không nhận `course_id`. Đề xuất DERIVED là thêm `course_id:int64!` để server kiểm tra toàn bộ recipients thuộc course Mentor có quyền quản lý.
- `recipients`/`channels` là string nhưng không có format; chuỗi CSV là khuyến nghị đơn giản, chưa phải contract đã duyệt.
- Response `Operation` chưa chỉ ra `notification_id:int64` cần cho API #64; `Operation.result?:Payment` không biểu diễn delivery.
- Không khẳng định `202` có nghĩa provider đã gửi; trạng thái và retry phải đọc qua API theo dõi sau khi thống nhất ID bàn giao.

## Đề xuất DERIVED cần xác nhận

| Chủ đề | Đề xuất tối giản | Cơ sở | Trạng thái |
|---|---|---|---|
| Course scope | Thêm `course_id:int64!` vào body; xác thực Mentor quản lý course đó và từng recipient là Student đang đủ điều kiện trong course. | AC-25 chọn course trước roster; giảm nguy cơ gửi ngoài scope. | DERIVED — đổi catalog trước khi code. |
| Recipients | Giữ string tạm thời nhưng quy ước CSV các `Student.id` int64 duy nhất, ví dụ `101,202`; server parse và kiểm tra lại toàn bộ. | #62 chọn từng learner; catalog domain ID int64. | DERIVED — cần thống nhất với #62 và schema ID. |
| Content | Đổi `content` sang string không rỗng. | UI nhập nội dung; `Notification.content` là string/TEXT. | DERIVED — catalog hiện khai báo int64. |
| Channels | Dùng CSV tên channel được contract duyệt; giới hạn ở channel đã được cấu hình. | Diagram nêu Push/Email; không có machine enum chung. | DERIVED — chưa chốt token hay mapping Push/IN_APP. |
| Retry | Bảo đảm POST idempotent bằng `Idempotency-Key` và lưu kết quả accepted trước khi dispatch. | API Guidelines khuyến nghị key cho mutation có retry; delivery bên ngoài có thể bị lặp. | DERIVED — persistence/key contract SOURCE_REQUIRED. |
| Tracking bridge | Trả Operation ID cho job; đồng thời công bố notification ID để API #64 truy vấn delivery. | #63 Operation response và #64 notification_id là hai định danh khác nhau. | SOURCE_REQUIRED — result schema chưa đủ. |

## Conflicts

| Nguồn A | Nguồn B | Xung đột | Ảnh hưởng |
|---|---|---|---|
| Catalog #63 | AC-25 diagram + Notification schema | Request `content:int64`; UI nhập nội dung và Notification.content là text. | Không thể xác nhận mapping body khi chưa sửa contract. |
| #62 → #63 | API #63 body | #62 chọn học viên theo course; #63 không nhận course ID. | Không thể kiểm tra recipient thuộc đúng course đã chọn bằng request hiện tại. |
| #63 response | #64 path | #63 trả `Operation` (id UUID theo schema); #64 nhận `notification_id:int64`. | Client thiếu ID đúng loại để gọi #64. |
| Operation schema | Notification job | `Operation.result?:Payment`; không có delivery result type gắn với Operation. | Không thể trả notification_id/counts qua result hiện tại. |
| AC-25 diagram | AC/API index | Diagram có node API #18 nhưng không nối; index liệt kê #18 cùng #62–#64. | Chưa rõ generic operation polling là nhánh bắt buộc hay song song với #64. |
| Legacy schema | V1-PILOT schema | Legacy có `notifications.user_id` BIGINT cho từng người nhận nhưng không có bảng recipients; pilot dùng UUID theo learner và bảng delivery, với channel `IN_APP` hoặc `EMAIL`. | Không ghép model hoặc khẳng định schema live. |
| Catalog #93 | Operation tracking summary | Admin create trả `Notification` ở row nhưng phần tổng quan nói trả `Operation`. | Không dùng Admin row để tự sửa Mentor contract. |
| API Guidelines | Current response helper | Guideline yêu cầu error `data:null`; helper hiện serialize `{}` khi không có data. | Future wiring discrepancy; #63 hiện chưa chạy. |

## Security note

- Chỉ lấy sender identity từ Bearer principal, không nhận sender ID từ body.
- Không chấp nhận recipient chỉ vì client gửi ID; server cần đối chiếu role, enrollment hiện hành và quyền Mentor trên đúng course.
- Không gửi nội dung/recipient tới Push hoặc Email trước khi authorization và toàn bộ input được kiểm tra.
- Không trả token, raw provider error, SQL, stack trace hoặc thông tin cá nhân không cần thiết.

## Performance/reliability note

- Fan-out có thể tăng theo số recipients × channels; catalog không có giới hạn batch. Giới hạn phải được bổ sung vào contract trước khi chọn một con số.
- 202 nên chỉ trả sau khi yêu cầu đã được chấp nhận bền vững; queue/outbox hoặc Operation storage hiện `SOURCE_REQUIRED`.
- Không kết luận retry count, backoff, partial-success status hoặc timeout khi chưa có nguồn được duyệt.
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
