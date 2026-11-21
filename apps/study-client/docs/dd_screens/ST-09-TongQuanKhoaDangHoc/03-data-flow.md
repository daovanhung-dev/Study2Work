# ST-09 — Data Flow & State

## Current-source reconciliation — 2026-11-21

ST-09 reads paged ACTIVE-course data from #20 before requesting #37. For each
accepted page, the UI compares returned row count with the expected row count
derived from `page`, `size`, and COUNT's `total`. A matching ACTIVE row is
sufficient to continue to #37 even if the counts differ. When the target is
absent from a mismatched page, ST-09 preserves an unresolved state and offers
retry; it does not infer that enrollment is absent from an inconsistent list.
The design-time flow below does not override current caller evidence. The
full course tree, lesson selection and AC-18 aggregate remain unresolved.

## 1. Nguồn dữ liệu
| Field / object | Type | Source | Destination | Cập nhật khi |
|---|---|---|---|---|
| Chỉ liệt kê theo bằng chứng trong excerpt bên dưới | Theo DD/API source | API/inventory/design; status phải giữ nguyên | UI/state nêu ở DD nguồn | Theo event source |

## 2. State model

> Không tạo DTO/ViewModel mới khi chưa có contract. State, DTO và mapping được trích nguyên ngữ cảnh từ DD nguồn bên dưới.

## 3. API DTO → ViewModel mapping

### Trích từ DD nguồn: B. Mô tả luồng hoạt động tổng thể

### Expected flow khi đủ contract

1. Student đi vào route từ một course selection ở ST-08. Client cần nhận courseId từ URL; cách parse, invalid format và courseId không được trả về bởi ST-08 hiện chưa có contract hoàn chỉnh.
2. Yêu cầu auth/session Student theo AC-13 và API catalog được kiểm tra. Không có source cho Study Web route guard/session behavior, vì vậy không xác định redirect hoặc session-expiry UI.
3. Enrollment được xác minh trước khi nạp tài nguyên học riêng tư. Inventory chỉ ra #20; cần contract xác định membership response, status hợp lệ và lỗi không thuộc khóa. API #20 hiện không có route/module/query/test source và response type trong catalog không biểu diễn danh sách khóa.
4. Khi membership được xác nhận, thiết kế cần lấy progress #37 và curriculum. AC-18 cần aggregate lesson + quiz + assignment. #09 hiện có thể trả danh sách lesson public. Thứ tự/parallelism và cách xử lý partial failure chưa được duyệt.
5. Chỉ sau khi có access contract, UI mới có thể hiển thị curriculum/progress đã gắn với Student. Không dùng #09 làm enrollment/access check và không coi content/video_url trong response public là quyền phát media.
6. Khi người học chọn lesson, ST-10 cần lessonId và phải chạy access/start APIs #22/#23/#24. ST-09 asset CTA hiện không chọn lesson, nên chưa có đầu vào đủ để điều hướng.
7. ST-21 là inventory destination để xem chi tiết progress theo courseId. PNG/HTML không có link/control; trigger và handoff vẫn cần được thiết kế.
8. Mất mạng, session hết hạn, không có enrollment, không có published lesson, lỗi progress, khóa không tồn tại và lỗi access cần state contract/UI riêng. Asset hiện không mô tả các trạng thái này ngoài gated handoff copy.

### Current behavior đã kiểm chứng

- ST-09 route reacts to `courseId`; it validates the route ID before requesting ACTIVE membership pages from #20 and calls #37 only after an exact course match.
- The page renders source-backed course/progress fields, loading, errors with retry, count/list unresolved state, and the not-enrolled result after scanning consistent pages. It does not call public #09 as an access check or render a course tree/media URL.
- API #09 route hiện hành gọi get_course_curriculum. Path course_id được parse integer; invalid path trả 404. Query đầu tiên chỉ chấp nhận course PUBLISHED; query thứ hai chỉ lấy lesson PUBLISHED, sắp thứ tự sort_order rồi id. Response 200 envelope chứa Page<Lesson>, gồm id, course_id, title, nullable content, nullable video_url, order, status; page=1, size=count, total=count và total_pages là 1 nếu có lesson, ngược lại 0. Khi rỗng message là “No published lessons.” Lỗi query/mapping trả 500; lỗi SQL rollback. Endpoint không khai JWT/enrollment check.
- Test source cho #09 tồn tại, nhưng test không được chạy trong task này.
- Current #20 and #37 route/module/query/model sources and ST-09 callers are present. #22/#23/#24 are not found in current Study Server source. Deployed Study Web/API runtime remains unverified.

### Trích từ DD nguồn: E. Ma trận trạng thái và điều hướng

| State | Điều kiện vào dự kiến | Màn hình / hành động | Current evidence |
|---|---|---|---|
| Route unavailable | Study Web route chưa được nối | Implementation gap | Current ST-09 route/page are source-wired; deployed runtime is unverified. |
| Loading/auth pending | Route vào, session/course context đang xác minh | Loading treatment cần thiết kế | StudentLayout owns session setup; ST-09 shows loading while validating #20 membership and while loading #37. |
| Invalid/missing course | Path invalid, course không tồn tại/không public | #09 source maps non-integer path, missing course and unpublished course to 404; signed-int64 range handling is not explicit | ST-09 rejects an invalid/unsafe route ID locally before calling #20. Missing/non-enrolled IDs resolve through the validated #20 membership scan. |
| Enrollment unconfirmed | #20 chưa trả membership decision | Gated/error state; không gọi private learning flow | #20 projection and page are validated; request, response-shape and count/list mismatch states remain distinct and retryable. |
| Not enrolled | Membership contract xác nhận không thuộc Student | Deny/return state cần Product/API approval | After all validated, cardinality-consistent #20 pages are scanned, ST-09 shows the not-enrolled gate when no ACTIVE row matches. |
| Enrolled, loading | Enrollment verified, progress/curriculum loading | Loading layout cần thiết kế | A matching ACTIVE row triggers #37 and the page shows progress loading. |
| Enrolled, no lessons | #09 trả 200 empty public list | No-lessons content chỉ được hiển thị sau membership/access policy; không đồng nghĩa khóa có thể học | Current #37 `has_content=false` state displays no published lessons in its progress projection; public #09 is not called. |
| Enrolled, loaded | #20 gate + #37/#09 valid payloads + approved projection | Course outline/progress UI cần bổ sung | ST-09 renders validated #37 course-level totals/percentage; it has no course tree or lesson selection. |
| Partial failure | Một trong #09/#37 thất bại | Partial/error state và retry semantics chưa chốt | #20/#37 errors are shown with the existing retry action; public #09 is not called. |
| Session expired/forbidden | Auth/access layer trả 401/403 theo contract | Session/error handling cần thiết kế; không mặc định redirect | #20/#37 only declared codes |
| Lesson chosen | Lesson item + lessonId exists | Access handoff to ST-10 | Lesson item absent; #22–#24 NOT_FOUND |
| Progress detail requested | User selects ST-21 control | /student/progress/:courseId | ST-09 links to the course progress route; destination design and #37 aggregate discrepancies remain open. |

### Điều hướng

| From | Trigger/data | To | Gaps |
|---|---|---|---|
| ST-08 | Chọn course card; pass courseId | ST-09 | ST-08 asset không có loaded course card; #20/#21 schemas absent |
| ST-09 | Select lesson; pass lessonId (and context if approved) | ST-10 | ST-09 has no lesson row; CTA provides no ID; #22–#24 absent |
| ST-09 | Progress detail action; pass courseId | ST-21 | Inventory relation only; visual control and #37 contract absent |
| ST-09 | Return link | ST-08 | href=#; route state/history unverified |
| Header/footer | Labels/data-path for ST-01/ST-08/ST-20/ST-23/ST-26 | Corresponding screen | href=#; router/auth guard absent |

Không có bằng chứng về back-stack, query/path restoration, tab persistence hoặc session redirect. Những hành vi này vẫn là quyết định thiết kế mở.

## 4. Luồng đọc (Read)
- Orchestration từ inventory: Xác nhận course thuộc #20 → GET #37; GET #9 chỉ chứa phần public; lesson access #22 trước khi học.
- Chi tiết current/source mapping: xem [API Integration](04-api-integration.md) và DD nguồn.

## 5. Luồng ghi (Write)
- Chỉ mô tả mutation được DD/API source nêu; không thêm endpoint hoặc side effect.
- Source trace: [ST-09](../../screen_stitch/03_student/ST-09_tong-quan-khoa-dang-hoc/ST-09.md)

## 6. Cache / concurrency / lifecycle
- Cache, race, cleanup, pagination: xem các section source bên dưới; nếu không có bằng chứng thì để `CẦN_XÁC_NHẬN`.

## 7. Data errors & security
- Theo error/security/source-status section của DD nguồn; không coi state trong mockup là runtime behavior.

## 8. Trace
[Events](02-events.md) · [API](04-api-integration.md) · [Rules](05-business-rules.md)
