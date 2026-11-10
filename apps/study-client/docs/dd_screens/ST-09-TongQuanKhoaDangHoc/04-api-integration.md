# ST-09 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `ST-09-API-001` | #09 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `ST-09-API-002` | #20 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `ST-09-API-003` | #37 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #09, #20, #37
- Orchestration/data notes: Xác nhận course thuộc #20 → GET #37; GET #9 chỉ chứa phần public; lesson access #22 trước khi học.
- BE/source status và gate: **D**; #09 local source-backed/public (API DD Draft, int64 range check absent); #20/#37 and #22–#24 not source-backed; **BLOCK:** Chưa có contract course-learning tree đầy đủ
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: Expected flow khi đủ contract

1. Student đi vào route từ một course selection ở ST-08. Client cần nhận courseId từ URL; cách parse, invalid format và courseId không được trả về bởi ST-08 hiện chưa có contract hoàn chỉnh.
2. Yêu cầu auth/session Student theo AC-13 và API catalog được kiểm tra. Không có source cho Study Web route guard/session behavior, vì vậy không xác định redirect hoặc session-expiry UI.
3. Enrollment được xác minh trước khi nạp tài nguyên học riêng tư. Inventory chỉ ra #20; cần contract xác định membership response, status hợp lệ và lỗi không thuộc khóa. API #20 hiện không có route/module/query/test source và response type trong catalog không biểu diễn danh sách khóa.
4. Khi membership được xác nhận, thiết kế cần lấy progress #37 và curriculum. AC-18 cần aggregate lesson + quiz + assignment. #09 hiện có thể trả danh sách lesson public. Thứ tự/parallelism và cách xử lý partial failure chưa được duyệt.
5. Chỉ sau khi có access contract, UI mới có thể hiển thị curriculum/progress đã gắn với Student. Không dùng #09 làm enrollment/access check và không coi content/video_url trong response public là quyền phát media.
6. Khi người học chọn lesson, ST-10 cần lessonId và phải chạy access/start APIs #22/#23/#24. ST-09 asset CTA hiện không chọn lesson, nên chưa có đầu vào đủ để điều hướng.
7. ST-21 là inventory destination để xem chi tiết progress theo courseId. PNG/HTML không có link/control; trigger và handoff vẫn cần được thiết kế.
8. Mất mạng, session hết hạn, không có enrollment, không có published lesson, lỗi progress, khóa không tồn tại và lỗi access cần state contract/UI riêng. Asset hiện không mô tả các trạng thái này ngoài gated handoff copy.

### Trích từ DD nguồn: D.1 API và bảo mật

| API | Contract được khai báo | Current source | Dùng trong ST-09 |
|---|---|---|---|
| #09 | Public GET curriculum; course_id int64; response ApiEnvelope<Page<Lesson>>; 200/404/500. | SOURCE_BACKED_LOCAL: registered route/view/validator/query/model/test source; reverse API index corrected to R. API DD is still Draft. | Chỉ public outline projection; không chứng minh enrollment hoặc quyền phát nội dung/media. |
| #20 | Student GET /users/me/courses; optional status/page; Bearer JWT; response ApiEnvelope<UserProfile>; 200/401/403/422/500. | NOT_FOUND route/module/query/test. | Intended enrollment gate nhưng response schema không mô tả course membership. |
| #37 | Student GET /users/me/progress/{course_id}; Bearer JWT; response ApiEnvelope<UserProfile>; 200/401/403/404/500. | NOT_FOUND route/module/query/test; API DD Draft. | Intended aggregate progress; formula, payload, empty/error semantics chưa quyết định. |
| #22–#24 | Inventory uses lesson access/start/content flow. | NOT_FOUND route/module/test in current source. | Required before protected lesson access. |

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/03_student/ST-09_tong-quan-khoa-dang-hoc/ST-09.md)
