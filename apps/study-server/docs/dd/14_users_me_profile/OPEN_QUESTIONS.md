# OPEN_QUESTIONS

## Q-14-01 — Persistence của `bio`

**Bằng chứng**

- `list_api.md`: request có `bio:string!`; response `UserProfile` có `bio?:string`.
- `infra/postgres/study-server/DB.sql`: bảng `users` không có column `bio`.
- `DB_UNICA_ERD.drawio`: entity `USERS` không có field `bio`.
- Current API #4 profile model/query không có `bio`.

**Vấn đề**

- Chưa biết `bio` sẽ được lưu ở column mới, bảng khác hay không persistence.

**Ảnh hưởng**

- Request validation, `UPDATE users`, response `UserProfile`, migration và backward compatibility.

**Quyết định tạm thời**

- Giữ `bio` trong contract.
- Đánh dấu `SOURCE_REQUIRED`.
- Không tạo column, migration, shadow field hoặc JSON fallback.

## Q-14-02 — Requiredness và nullable semantics của `avatar_url`

**Bằng chứng**

- `list_api.md`: literal `avatar_url...:uri!`.
- Reusable `UserProfile`: `avatar_url?:uri`.
- Current `users.avatar_url`: `TEXT NULL`.

**Vấn đề**

- Dấu `...` không phải field syntax chuẩn và không xác định field có bắt buộc hay nullable.

**Ảnh hưởng**

- Request validation, PUT replacement semantics, DB null handling và response example.

**Quyết định tạm thời**

- Dùng physical field `avatar_url` trong DD.
- Giữ requiredness/nullable/blank policy là `TBD`.

## Q-14-03 — `phone` required trong contract nhưng nullable trong schema

**Bằng chứng**

- `list_api.md`: `phone:string!`.
- `DB.sql`: `phone VARCHAR(20) NULL`.

**Vấn đề**

- Chưa biết request bắt buộc có giá trị non-blank hay cho phép clear về `NULL`.

**Ảnh hưởng**

- Validation, SQL parameter binding, PUT full replacement và response nullability.

**Quyết định tạm thời**

- Ghi `phone` là required theo contract.
- Ghi max length `20` theo schema.
- Không tự chọn null/blank/clear semantics.

## Q-14-04 — Response source cho `UserProfile.bio`

**Bằng chứng**

- AC-11 yêu cầu reload profile sau update.
- Current API #4 chỉ select các public columns không gồm `bio`.

**Vấn đề**

- Không thể tạo response source đầy đủ cho `data.bio` từ current schema/source.

**Ảnh hưởng**

- Response contract, frontend rendering và khả năng chuyển DD thành implementation-ready.

**Quyết định tạm thời**

- Giữ `data.bio` ở `SOURCE_REQUIRED`.
- Không tự lấy `bio` từ request nếu không có persistence.

## Q-14-05 — Missing user mapping và PUT semantics

**Bằng chứng**

- API #14 contract không khai báo `404`.
- Current API #4 map user record không tồn tại thành `401`.
- Method là `PUT`, nhưng null/blank/clear policy cho profile fields chưa có source.

**Vấn đề**

- Cần xác nhận `401` có được giữ cho identity inconsistency và PUT có phải full replacement hay không.

**Ảnh hưởng**

- Error contract, retry/client behavior và data clearing semantics.

**Quyết định tạm thời**

- DD dùng `401 DESIGN_AUTHENTICATION_REQUIRED` theo current API #4 pattern.
- Ghi PUT replacement/clear behavior là `TBD`.

