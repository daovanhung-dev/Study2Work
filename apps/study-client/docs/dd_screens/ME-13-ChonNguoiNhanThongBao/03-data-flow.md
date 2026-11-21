# ME-13 — Data Flow & State

## 1. Nguồn dữ liệu
| Field / object | Type | Source | Destination | Cập nhật khi |
|---|---|---|---|---|
| Chỉ liệt kê theo bằng chứng trong excerpt bên dưới | Theo DD/API source | API/inventory/design; status phải giữ nguyên | UI/state nêu ở DD nguồn | Theo event source |

## 2. State model

> Không tạo DTO/ViewModel mới khi chưa có contract. State, DTO và mapping được trích nguyên ngữ cảnh từ DD nguồn bên dưới.

## 3. API DTO → ViewModel mapping

### Trích từ DD nguồn: B. Mô tả luồng hoạt động tổng thể

1. **Entry/auth.** Khi Study Web được triển khai, route đề xuất phải nằm trong Mentor-authenticated shell. Nếu chưa có session/role MENTOR, không gọi #46/#62/#63. Current source chỉ chứng minh backend Bearer/role guards; client redirect và session refresh chưa có contract.
2. **Khởi tạo.** Đặt course selection rỗng, roster rỗng, selected IDs rỗng, loading/error state phù hợp. Ảnh tĩnh cho thấy radio all được chọn trực quan nhưng chưa chọn course; xác nhận đây là default nghiệp vụ trước khi dùng làm runtime default.
3. **Tải course.** Gọi #46. Dùng data.items để render course title và gắn value bằng data.items[].id int64. Theo data.pagination tải thêm page nếu cần để danh sách đủ. Không chuyển HTML slug sang int64 bằng suy luận. #46 rỗng → course-empty state; response lỗi → giữ retry/leave action theo app-wide policy.
4. **Chọn course và tải roster.** Khi chọn một course ID hợp lệ, reset roster/selection thuộc course cũ rồi gọi #62 theo path course_id. Chỉ áp dụng response nếu nó thuộc course selection mới nhất; tránh response chậm của course cũ thay state hiện tại. 200 [] → roster-empty state. 200 data[] → map id, full_name, avatar_url; không tự tạo các cột/email/progress.
5. **Chọn recipients.** all chọn toàn bộ IDs từ response #62; specific yêu cầu chọn từng ID trên UI đã được thiết kế; support-needed không thể tính từ #62. Giữ IDs unique; đổi course thì xóa lựa chọn của course trước. Cách giữ/tạo selection khi chuyển giữa radio scopes cần product xác nhận.
6. **Continue.** Không gọi API #63 tại ME-13. Chỉ chuyển ME-14 khi có course context hợp lệ và tập recipients khác rỗng; API #63 hiện từ chối recipients rỗng. Truyền IDs nguyên dạng numeric int64 qua cơ chế được xác nhận. Route state, query, persistence, selection all expansion và serial hóa sang CSV ở ME-14 chưa chốt.
7. **Rời màn hình.** Cancel, breadcrumb, header/footer destinations hiện là href="#". Không tuyên bố navigation hiện hành. AC-25 tiếp tục qua ME-14; ME-14 mới soạn title/content/channels và gọi #63 nếu payload contract được duyệt. Operation UUID, notification_ids, #18 polling và #64 status không thuộc state của ME-13.
8. **Lỗi và ngoại lệ.** 401 cần chuyển vào auth/session flow đã được xác nhận; 403 course/recipient denied; 404 course/path không tồn tại hoặc slug sai; 422 query/body validation; 500 internal; transport/offline xử lý theo shared client policy. Không tự retry POST #63. API #46/#62 là GET nhưng retry/backoff vẫn theo app-wide policy chưa được xác minh.

### Trích từ DD nguồn: E. Ma trận trạng thái và điều hướng

| State | Entry/condition | UI/data | Allowed transitions |
|---|---|---|---|
| session-check | Enter proposed route | No protected request until Mentor auth is known | authenticated → courses-loading; unauthenticated/role denied → app auth state |
| courses-loading | E01 #46 pending | Course selector loading; Continue disabled | success-nonempty → course-ready; success-empty → courses-empty; error → courses-error |
| courses-empty | #46 returns items=[] | No course option; empty copy needs design | reload → courses-loading; leave → confirmed destination |
| courses-ready | #46 returns one or more pages | Course options with source IDs/titles | select → roster-loading |
| roster-loading | E02 #62 pending | Selected course; clear previous roster/IDs; Continue disabled | data[] → roster-ready; [] → roster-empty; 401/403/404/500/network → roster-error |
| roster-empty | #62 data=[] | Empty roster; count 0; Continue disabled | choose another course → roster-loading; leave → confirmed destination |
| roster-ready-none | Roster loaded, no selected IDs | Show approved rows; count 0 | all → selected-all; specific row toggles → selected-some; support scope remains blocked |
| selected-all | IDs equal all loaded roster IDs | Count equals roster length; specific only after explicit product decision | deselect/scope change → roster-ready-none or selected-some; continue → handoff-pending |
| selected-some | Explicit subset selected | Count equals unique selected IDs | select/deselect → selected-some/none; continue → handoff-pending |
| support-scope-blocked | support_needed selected | No derived IDs; explain only approved blocker | choose all/specific → roster-ready state |
| courses-error / roster-error | API/network failure | Keep safe course context; no stale rows; show shared error state | retry under shared client policy; choose other course; leave |
| handoff-pending | E05 after validated nonempty IDs | Disable repeated activation while transition occurs | success → ME-14; failure → selected state with error |

### Navigation/data handoff

- Entry: `/mentor/notifications/new/recipients` is registered under the Mentor layout. Global session/role behavior is owned by that layout and has not been browser-verified here.
- Next: ME-14 at `/mentor/notifications/new`. Current source navigates with selected course ID and recipient summaries in in-memory `history.state`; IDs are validated against the loaded roster. Persistence, reload/back restoration and product approval of the carrier remain unresolved.
- Back/cancel: browser back can return to ME-13, but router-state restore semantics are not verified; no local/session storage is used. Cancel destination remains unspecified.
- #63 sends only in ME-14; #63 returns operation UUID and notification IDs, neither should be introduced as ME-13 selection state. #18 and #64 belong downstream to ME-15.
- Session expiry and denied access must use approved global auth/error routes. No redirect target is specified here.

## 4. Luồng đọc (Read)
- Orchestration từ inventory: GET #46 → GET #62 theo numeric course_id → giữ unique Student IDs int64 cho ME-14; handoff carrier chưa được duyệt.
- Chi tiết current/source mapping: xem [API Integration](04-api-integration.md) và DD nguồn.

## 5. Luồng ghi (Write)
- Chỉ mô tả mutation được DD/API source nêu; không thêm endpoint hoặc side effect.
- Source trace: [ME-13](../../screen_stitch/04_mentor/ME-13_chon-nguoi-nhan-thong-bao/ME-13.md)

## 6. Cache / concurrency / lifecycle
- Cache, race, cleanup, pagination: xem các section source bên dưới; nếu không có bằng chứng thì để `CẦN_XÁC_NHẬN`.

## 7. Data errors & security
- Theo error/security/source-status section của DD nguồn; không coi state trong mockup là runtime behavior.

## 8. Trace
[Events](02-events.md) · [API](04-api-integration.md) · [Rules](05-business-rules.md)

## Current Study Client source (2026-11-21)

- `mentor.route.ts` registers `/mentor/notifications/new/recipients` as ME-13 and `/mentor/notifications/new` as ME-14.
- ME-13 calls #46 with `page` and supported `size=100`, then #62 only for a validated nonempty int64-safe course ID. Clearing/changing the course cancels a pending roster read without sending an empty path value. It rejects malformed/duplicate response IDs, distinguishes #62 access denied, and offers retry/empty/loading states.
- Continue is enabled only while the course remains in the current validated #46 page, a successful #62 roster is loaded, no roster error/access denial is present, and every selected ID still belongs to that roster. Optional #62 avatars render only from HTTPS or same-origin HTTP with `no-referrer`; a failed/missing/unsafe avatar falls back to initials.
- The user can select individual roster rows or all currently returned rows. The prototype's support-needed scope cannot be implemented from #62 and no progress/attendance filter is derived.
- Continue sends the selected course ID and recipient summaries through Angular router `history.state`; ME-14 consumes this state. This is current source behavior only. Persistence, reload/back restoration and product approval of the carrier remain unresolved.
- #63 is not called by ME-13 or ME-14; send controls stay disabled while its request/body and course-scoping contract remain unresolved. No browser/runtime verification or tests were run.
