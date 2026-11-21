# AD-13 — Navigation

## 1. Route definition
- Current route in inventory: `/admin/lessons/:lessonId`
- Status: Angular route is registered at `lessons/:lessonId`; AD-12 navigation is emitted only for IDs safe to represent as JavaScript numbers; AD-13 validates raw `lessonId` as full signed-int64 before GET #83.
- Route params/types: `lessonId` stays a raw string; missing/malformed/out-of-range values stop locally without a request; valid strings are passed unchanged.
- Query params/defaults: preserve the inventory route string; detailed parsing rules only from source DD.
- Route guards: see source DD/API contract; do not create role policy.

## 2. Điểm vào
| From screen/route | Trigger | Params | Guard / fallback |
|---|---|---|---|
| [AD-12](../AD-12-DanhSachBaiHocQuanTri/00-overview.md), [AD-14](../AD-14-SuaDoiTrangThaiXoaBaiHoc/00-overview.md) | Theo DD nguồn/inventory | Theo source; không suy diễn | Xem source DD; route chưa xác nhận runtime |

## 3. Điểm ra
| Destination | Trigger | Params | Điều kiện |
|---|---|---|---|
| [AD-14](../AD-14-SuaDoiTrangThaiXoaBaiHoc/00-overview.md) | Source event/inventory navigation | Theo source DD | Expected links; runtime chưa verify |

## 4. Back / refresh / deep link
- Back behavior: xem source DD; không mặc định browser history.
- Preserve filters/scroll/form state: chỉ nếu source có nêu, nếu không `CẦN_XÁC_NHẬN`.
- Refresh/direct URL: route trong inventory không chứng minh runtime.
- Invalid/missing ID: `adminRouteState` renders a local error for a missing parameter; `isSignedInt64RouteId` blocks malformed/out-of-range values before #83. Valid raw IDs remain unchanged.
- Not authenticated/authorized: theo source role guard; xem [Business Rules](05-business-rules.md).

## 5. Diagram
```mermaid
flowchart LR
  S0["AD-13 Chi tiết bài học quản trị"] --> S1["AD-14"]
```

## Source navigation and flow detail

### Trích từ DD nguồn: E. Ma trận trạng thái và điều hướng

| Trạng thái | Điều kiện vào | Dữ liệu/UI | Chuyển tiếp và giới hạn |
|---|---|---|---|
| `wired-source` | Current Angular router registers AD-13, AD-12 passes safe IDs and AD13Page has a raw signed-int64 guard | Invalid route IDs stop locally; valid IDs call GET #83 and render only the Lesson projection | Tests were not run for this continuation; browser/live DB remain unverified. |
| `loading` | Valid raw `lessonId` passes the local guard and AD13Page sends #83 | Loading notice shown | 200→`loaded`; HTTP failures enter `error`. |
| `loaded` | #83 returns valid `Lesson` | Seven API fields only; optional content/video may be null | AD-14 action remains disabled; no dependency/metric counts. |
| `selection-required` | Prototype no-selection state | Static empty prompt | Direct route with missing `lessonId` renders a local error and skips #83; a valid detail request requires `lesson_id`. |
| `invalid-route-id` | Raw `lessonId` is malformed or outside signed-int64 bounds | Local route error; no HTTP request | Error recovery link returns to AD-12. |
| `not-found` | #83 returns 404 for no matching row or `DELETED` tombstone | 404 `DESIGN_RESOURCE_NOT_FOUND` | Return-to-list behavior is a client policy; API does not redirect. |
| `unauthorized` | Missing/invalid/expired Bearer token | 401 `DESIGN_AUTHENTICATION_REQUIRED` | Session recovery/login route is not defined for Study Web. |
| `forbidden` | Authenticated principal lacks `ADMIN` | 403 `DESIGN_ACCESS_DENIED` | AC-34 fine-grained lesson permission is not enforced by current source. |
| `service-error` | Query/required-field/mapping failure or transport issue | Safe 500 for backend failures; network UX unspecified | Source rolls back read transaction; retry policy is absent. |
| `dependencies-unknown` | #83 returns Lesson with no dependency projection | Do not infer 0 references | #86 performs its own current dependency check at delete time; 422 conflict maps in AD-14. |
| `metrics-unavailable` | No #83 metrics/SSE payload | Screenshot values are static placeholders | No subscription/refresh transition exists. |

**Navigation:** AD-12 safe numeric row ID → `/admin/lessons/{lessonId}` → GET #83 → AD-14 with the same ID only after its separate flow is approved. Angular back links return to AD-12. Browser history, filter preservation, stale detail, dependency refresh, route guard and #84/#85/#86 policy remain open.

**Accessibility/design:** `.agents/web-study/design.md` remains the design target. Angular has semantic links/buttons and explicit disabled/loading/error states; keyboard/focus-visible behavior, responsive browser rendering and contrast have not been verified in a browser.

### Trích từ DD nguồn: B. Luồng hoạt động tổng thể

1. **Đi vào từ AD-12:** current #82 rows pass `Lesson.id` into `/admin/lessons/:lessonId` only when it is a JavaScript safe integer. Unsafe IDs show a precision warning and have no detail link. The Angular route and AD-13 page are registered. Do not pass a course slug/title as the lesson ID.
2. **Kiểm tra phiên/quyền:** target client cần session Admin. Request #83 hiện xác thực Bearer/JWT + claim `ADMIN` trước khi parse raw path hay truy vấn DB. AC-34 yêu cầu lesson-management permission riêng nhưng source chỉ có role guard; không để UI badge thay quyền server.
3. **Chuẩn bị request:** tạo `GET /api/v1/admin/lessons/{lesson_id}` với Bearer token; không body/query. Giữ numeric ID; client không tự đặt positive constraint ngoài nguồn. API raw parser chấp nhận signed int64 text và leading zero trong giới hạn parser.
4. **Lookup:** server bind ID vào `FIND_ADMIN_LESSON_DETAIL`; đọc một row từ candidate legacy `lessons`; loại `status='DELETED'`; không lọc `PUBLISHED`, không join course/resources/progress và không gọi metric API.
5. **Xử lý response:** success trả `ApiEnvelope<Lesson>` trực tiếp; map `id`, `course_id`, `title`, `content`, `video_url`, `order`, `status`. `content` và `video_url` có thể null. `course_id/order/status` required ở model nhưng legacy DDL có thể NULL; lỗi map hiện thành 500 + rollback.
6. **Render:** prototype hiện luôn hiển thị no-selection placeholders. Target UI chỉ render fields response-backed sau khi contract/schema được giải quyết; `course_id` là ID, không phải course title; status cần giữ raw hoặc chờ enum mapping. No resource/progress/metrics fields are present in #83.
7. **Media/resources:** `content` là nullable string, không có HTML sanitization/rendering contract trong #83; `video_url` là nullable string, không có signed URL/player policy. Resources/quiz/discussion cards và số liệu không thể bind từ response.
8. **Hành động:** button tới AD-14 hiện disabled. Khi workflow được wire, chuyển cùng `lessonId` đến AD-14; không gọi #84/#85/#86 từ AD-13. API #86 tự kiểm tra progress/resources/uploads khi thực hiện delete.
9. **Rời màn hình:** expected back-to-AD-12 link. Current anchors là `#`; browser history, query preservation, refetch sau AD-14 và chọn lại row chưa được định nghĩa.

### Response và lỗi

- **Request:** `GET /api/v1/admin/lessons/{lesson_id}`, `Authorization: Bearer <token>`; optional `X-Trace-Id` theo middleware; no query/body.
- **Success:** HTTP 200; `success`, `businessCode=DESIGN_RESOURCE_RETRIEVED`, message, `data: Lesson`, `meta:{}`, `traceId`. Local message hiện là “Lesson retrieved.”.
- **Errors:** 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 404 `DESIGN_RESOURCE_NOT_FOUND` cho invalid/overflow/overlength ID hoặc missing/DELETED row; 500 `DESIGN_INTERNAL_ERROR` cho DB/mapping/required projection error.
- **Rollback/commit:** no commit on success. Missing row and error projection/query paths call rollback. Test source checks safe envelope and no raw database details.
- **Retry/cache/timeouts:** không có Study Web client policy; chưa được thiết kế. Không khẳng định stale response, request cancellation, retry hoặc cache invalidation.
