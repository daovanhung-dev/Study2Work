# ME-15 — Theo dõi gửi thông báo · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `ME-15` |
| Module | Mentor |
| Route | `/mentor/notifications/:notificationId/status` — hiện đăng ký trong `mentor.route.ts`; browser/runtime chưa xác minh |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source reader cho #64 hiện WIRED/PARTIAL; chọn notification ID từ batch và status/report behaviors còn BLOCKED; browser/runtime NOT VERIFIED. |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
| Nguồn đối chiếu | [ME-15.md](../../screen_stitch/04_mentor/ME-15_theo-doi-gui-thong-bao/ME-15.md), [ME-15_PLAN.md](../../screen_stitch/04_mentor/ME-15_theo-doi-gui-thong-bao/ME-15_PLAN.md), [ME-15_markers.json](../../screen_stitch/04_mentor/ME-15_theo-doi-gui-thong-bao/ME-15_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Hiển thị status theo một notification ID do caller xác định; API #64 source-backed trả Operation-shaped status local cho notification đó, không phải tổng hợp cả batch. #63 trả một Operation UUID và nhiều notification IDs int64; selector/route handoff chưa chốt. Inventory `queued/sending/complete/failed` không khớp #64 source `QUEUED/FAILED/SENT`.
- In-scope: Current source calls #64 with one validated notification ID; it never sends Operation UUID `data.id` to the path. It does not call #18 because AC-25 has no #18 flow edge and operation tracking semantics remain separate. Prototype channel/report/ACK/real-time claims are not server evidence.
- Out-of-scope: Xem gate bên dưới; không kết luận Study Web route/UI đã wired hoặc runtime đã chạy.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-25 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Hiển thị status theo một notification ID do caller xác định; API #64 source-backed trả Operation-shaped status local cho notification đó, không phải tổng hợp cả batch. #63 trả một Operation UUID và nhiều notification IDs int64; selector/route handoff chưa chốt. Inventory `queued/sending/complete/failed` không khớp #64 source `QUEUED/FAILED/SENT`. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #18, #64
- Liên kết màn hình dự kiến: [ME-14](../ME-14-SoanThongBaoMentor/00-overview.md), [SH-07](../SH-07-TheoDoiTacVuBatDongBo/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | queued/sending/complete/failed |
| Current source/runtime | Current Study Client source | `SOURCE-WIRED / PARTIAL` · `BROWSER RUNTIME NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [ME-15 source screen.png](../../screen_stitch/04_mentor/ME-15_theo-doi-gui-thong-bao/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/04_mentor/ME-15_theo-doi-gui-thong-bao/screen_annotated.png))
- Luồng: Current source gọi #64 theo một validated `notificationId` path ID; nó không dùng UUID `data.id` làm path. Không gọi #18 vì AC-25 node #18 không nối flow và generic operation contract vẫn khác notification status. Producer selection, batch status mapping, channel/report/ACK/real-time claims chưa có bằng chứng.
- Priority: P2; Gate/source status: **M**; #64 có local route/module/query/model/test và current ME-15 caller; #18 D/UNWIRED. **SOURCE-WIRED / PARTIAL:** strict read/retry/route-change handling. **BLOCKED:** batch ID selection, status lifecycle mapping, per-channel/recipient report, polling cadence/destination links; live schema/provider/runtime chưa verified.

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

The source excerpt below describes the 2026-11-08 prototype/DD snapshot. Current source evidence from 2026-11-20 is appended after that excerpt.

# ME-15 — Theo dõi gửi thông báo

**Screen ID:** ME-15 · **Loại:** Trang · **AC:** AC-25 · **Actor dự kiến:** Mentor  
**Tài liệu:** DD READY · **Implementation:** IMPLEMENTATION BLOCKED · **Runtime:** NOT VERIFIED  
**Ảnh:** [screen.png](../../screen_stitch/04_mentor/ME-15_theo-doi-gui-thong-bao/screen.png) · [Ảnh đánh số](../../screen_stitch/04_mentor/ME-15_theo-doi-gui-thong-bao/screen_annotated.png) · [Marker map](../../screen_stitch/04_mentor/ME-15_theo-doi-gui-thong-bao/ME-15_markers.json) · [Kế hoạch](../../screen_stitch/04_mentor/ME-15_theo-doi-gui-thong-bao/ME-15_PLAN.md)

> `DD READY` nghĩa là tài liệu ghi nhận đủ bằng chứng hiện hành và các quyết định còn thiếu để chuyển giao review. Việc tích hợp trạng thái, luồng chọn ID và các nội dung báo cáo vẫn bị chặn; không có tuyên bố chức năng runtime đã hoạt động.

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: A. Tổng quan màn hình

### Mục tiêu và ranh giới

ME-15 được danh mục mô tả là trang theo dõi việc gửi thông báo sau ME-14. Route danh mục là `/mentor/notifications/:notificationId/status`; tham số này là một notification ID số nguyên. Màn hình dự kiến hiển thị trạng thái dispatch của notification mà Mentor sở hữu.

Ảnh và `code.html` hiện có là prototype tĩnh. HTML không đọc route param, không có Study Web router/API client, không tải dữ liệu và không xác thực người dùng. Vì vậy nội dung đang thấy trên ảnh không phải bằng chứng về trạng thái server.

### Điều kiện truy cập và dữ liệu

| Thuộc tính | Đặc tả / bằng chứng |
|---|---|
| Actor | Mentor. API #64 yêu cầu Bearer token và role `MENTOR`; kiểm tra này thuộc server. Profile Mentor trong HTML là text tĩnh, không phải session hiện hành. |
| Điều kiện trước — mục tiêu | Có một `notificationId` hợp lệ được xác định từ kết quả tạo thông báo/điều hướng trước đó và Mentor đã đăng nhập. Quy tắc chọn một ID từ một batch chưa có contract. |
| Điều kiện trước — prototype | Không cần tham số hoặc session; trang dựng toàn bộ text tĩnh khi HTML tải. |
| Dữ liệu đầu vào | Mục tiêu: `notification_id:int64` trên route API #64. API #63 trả `data.id:uuid` cho Operation batch và `meta.notification_ids:int64[]` cho từng notification. Hai ID không thể hoán đổi. |
| Kết quả sau | API #64 là GET read-only. Không có mutation hoặc thay đổi thông báo. Hành vi rời màn hình hiện chưa được nối route. |
| Route UI | Inventory: `/mentor/notifications/:notificationId/status`; current `mentor.route.ts` registers ME-15 and the #64 caller. Browser/runtime remains unverified. |
| Màn hình liên quan | ME-14 là producer/caller dự kiến. SH-07 là generic operation tracker; API #18 không thay thế API #64. Các anchor quay lại/hỗ trợ trong prototype chưa có destination. |
| API mục tiêu | #64 `GET /api/v1/mentor/notifications/{notification_id}/status`. #18 generic operation status is not called because AC-25 does not connect it to this flow. |
| Side effect | Không có trên #64. Current page's manual reload makes a read-only #64 request; prototype timer/toast behavior is historical. |
| Bảo mật | Client không tự quyết định ownership. #64 xác thực Bearer Mentor, so `notifications.sender_id` với Mentor hiện tại trước khi trả operation data. Không đưa UUID Operation vào path `notification_id`. |
| Trạng thái triển khai | Current Study Client route and #64 caller are source-wired; #18 is not used; live schema, worker/provider and browser runtime are unverified. |

### Expected behavior và current behavior

| Chủ đề | Expected / contract | Current source / prototype | Kết luận |
|---|---|---|---|
| ID | Inventory route nhận `notificationId`; #63 response có Operation UUID và nhiều notification IDs int64. | #64 nhận đúng một int64; không có quy tắc chọn recipient ID đại diện batch. | BLOCKER: producer-to-screen mapping và semantics batch. |
| Status | Inventory liệt kê `queued/sending/complete/failed`. | #64 source hiện trả `QUEUED`, `FAILED` hoặc `SENT` dựa trên local outbox. | DISCREPANCY: chưa được map `SENT` sang `complete`; `sending` không có trong source/API #64. |
| Refresh | Nút có nhãn “Tải lại trạng thái”. | Handler chờ 800 ms, bật toast rồi ẩn sau 3000 ms; không đọc server hoặc đổi dữ liệu. | Prototype mock; không mô tả là refresh thực. |
| Channels/report | UI hiển thị LMS Portal, Email, thảo luận và báo cáo từng người nhận. | Đây là các dòng/text tĩnh. Response #64 không có chi tiết kênh, count hoặc recipient. | BLOCKER: chưa có data/API contract cho các element này. |
| Real-time/ACK | Copy hứa trạng thái theo thời gian thực và tiến độ sau ACK. | Không có WebSocket/SSE/fetch/poll hoặc worker/provider evidence trong màn hình. | Claim chưa được chứng minh. |
| Generic operation | Catalog mô tả #18 cho operation tracking. | #18 chưa wired; path ID trong catalog `int64` nhưng convention/schema/AC khai báo UUID; node generic của AC-25 không nối flow. | ME-15 không gọi #18. |

### Nguồn truy vết chính

- Screen inventory: `apps/study-client/docs/list_screen.md`, dòng ME-15; kế hoạch tổng: `apps/study-client/docs/screen_stitch/dd_screens/PLAN.md`.
- Prototype: `screen.png`, `code.html` trong thư mục này. Original SHA-256 trước khi làm: PNG `6172c259a4dfca9a37a6652ebdae83d3f10831b63dd8b59b5e988a23ea534713`; HTML `ccd0151ae1352662dc006483ff0e00094d9317d35762e76515252c32b7dda70f`.
- Handoff #63: `apps/study-server/app/modules/mentor/api_63_mentor_notifications_create/{models.py,view.py,query.py}` và `apps/study-server/tests/modules/mentor/api_63_mentor_notifications_create/test_mentor_notifications_create.py`.
- API #64: `apps/study-server/app/api/v1.py`; `apps/study-server/app/modules/mentor/api_64_mentor_notification_status/{models.py,validate.py,query.py,view.py}`; API DD `apps/study-server/docs/dd/64_mentor_notifications_status/`.
- Generic #18: `apps/study-server/docs/dd/18_operations/` mô tả design-only; hiện không có route/module/query/test Study. Catalog tại `docs/lists/list_api.md`.
- Activity: `apps/study-server/docs/diagrams/AC_UNICA/AC_03_MENTOR_TEACHING.drawio`, trang AC-25; connected node `n8` là #64, còn `operation_status` (#18) không có incident edge. SH-07 cũng phân biệt generic #18 với notification-specific #64.

### Current Study Client source (2026-11-20)

- ME-15 is registered at `/mentor/notifications/:notificationId/status`. It follows route parameter changes and cancels stale #64 reads.
- The page rejects route IDs that are not positive int64-safe values, validates the exact `DESIGN_RESOURCE_RETRIEVED` envelope and Operation projection, and exposes loading, error/retry and ready states.
- The route `notificationId` is distinct from `data.id` Operation UUID. #64 returns `QUEUED`, `FAILED` or `SENT` for one notification; it does not return `sending`/`complete`, `completed_at`, per-channel results or a batch summary.
- Manual reload calls #64; there is no automatic polling. #63 does not yet select/pass a notification ID into ME-15, so direct route entry is the only current source handoff. Tests and browser/runtime were not run.
