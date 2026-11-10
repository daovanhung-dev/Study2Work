# AD-14 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `AD-14-EV-001` | `Source heading` / Response and validation mapping for implementation handoff | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: D. Đặc tả chi tiết sự kiện

Mọi API flow dưới đây phân biệt **direct catalog/AC**, **local source behavior**, và **DERIVED/open policy**. Không có sự kiện nào hiện được frontend thực thi.

| Event ID | Tên / trigger | Input và điều kiện | Xử lý tuần tự | Output / exception |
|---|---|---|---|---|
| EV-01 | Mở AD-14, tải lesson | Route `lessonId` đề xuất từ AD-13; selected ID phải candidate numeric `Lesson.id`. | Route/auth policy → GET #83 → đọc `ApiEnvelope<Lesson>` → map đúng Lesson fields; không tải dependency/course/type/metrics ngoài contract. | Loading → ready; 401/403/404/500; current Study Web `UNWIRED`; invalid ID của #83 local là 404. |
| EV-02 | Sửa local metadata | Input từ title/content/order; các controls hiện disabled. | Sau #83 success mới cho phép edit nếu được duyệt → chuẩn hóa theo API/body contract đã chốt → giữ state local dirty. Không gửi course/type; không tự giữ/clear `video_url` hoặc gán enum. | `dirty` hoặc input error chỉ là target states; actual validation/persistence chưa được xác nhận. |
| EV-03 | Lưu thông tin (#84) | Button form/action-card; expected một Lesson ID và body full replacement. | Current source body: required strict `title`, `content`, `video_url`, `order`; FastAPI parse body trước auth; sau đó ADMIN guard → raw int64 path → UPDATE excluding DELETED → map Lesson → commit. | 200 Lesson / #82 reload candidate; 401/403/404/422/500. Hidden video_url, extra form fields, retry/version policy là BLOCKER. |
| EV-04 | Đổi status (#85) | Button status; target `{status}` hiện chưa có UI control. | Body parse trước handler/auth → ADMIN guard → path int64 → lock current Lesson → same-status no-op hoặc update status+timestamp and audit old/new/actor atomically → commit. | 200 Lesson / #82 reload candidate; 401/403/404/422/500. Enum, Archived mapping, transition/readiness/confirm rules và live audit schema còn BLOCKER. |
| EV-05 | Xóa (#86) | Button delete; dialog/confirmation policy chưa có trong ảnh. | ADMIN guard → raw int64 path → lock active Lesson → check progress/resources/uploads → 422+rollback if any → otherwise tombstone + DB timestamp → map DeleteResult → commit. | 200 DeleteResult / #82 reload; 401/403/404/422/500. Dependency set completeness, confirmation UX and live locks/schema are BLOCKER. |
| EV-06 | Cancel/back/breadcrumb | Click cancel, local crumb, or AD-12 back link. | Current anchors `#` have no handler. Target back label names AD-12; cancel target, unsaved guard and filter/history persistence are unresolved. | No current route transition or API call. |
| EV-07 | Shell/footer/static claims | Nav, Notification, identity, status badges, RBAC, support, policy copy. | Render static HTML only; no health/profile/notification/audit/API request or link handler. | No server result; mark all claims static/unmapped. |

### Response and validation mapping for implementation handoff

- #84 success is direct Lesson with `id`, `course_id`, `title`, nullable `content`, nullable `video_url`, `order`, `status`; `meta:{}` and trace ID follow current helper. Errors use catalog codes 401/403/404/422/500 and current `data:null` error envelope. The body fields and validator rules remain DERIVED.
- #85 success is direct Lesson; audit row is not in response. Current error set is 401/403/404/422/500. Local no-op and audit behavior are DERIVED.
- #86 success is direct DeleteResult `{id:int64, status:"deleted", deleted_at:datetime}`. Local dependency conflict uses 422 `DESIGN_VALIDATION_ERROR`; response intentionally carries no dependency counts/details. Current error set is 401/403/404/422/500.
- Do not add client retry, optimistic concurrency, idempotency, conflict code, toast wording or success persistence claims without an approved source.

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
