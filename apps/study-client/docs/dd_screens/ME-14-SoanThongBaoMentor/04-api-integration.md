# ME-14 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `ME-14-API-001` | #62 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `ME-14-API-002` | #63 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

### Current Study Web integration — 2026-11-21

- ME-14 receives course and selected Student IDs from ME-13 history state, validates a non-empty unique positive safe-ID list, then calls Mentor API #63 with CSV `recipients`, trimmed `title`/text `content`, and explicitly selected `PUSH`/`EMAIL` channels.
- The page accepts only HTTP 202 `DESIGN_OPERATION_ACCEPTED` with `data.kind=NOTIFICATION_DISPATCH`, `data.status=QUEUED`, and a valid UUID in `data.id`; it routes that UUID to SH-07. API #18 later enforces owner matching for the authenticated caller.
- Current API #63 contract/model/OpenAPI treats `content` as text. The server still cannot bind selected recipients to the exact `courseId` in UI state because #63 has no `course_id` request field; its existing common ACTIVE roster rule remains the server rule. 202 means outbox acceptance, not provider delivery.
- Focused Mentor verification in the ME-01–ME-18 completion task: 6 spec files / 12 tests passed, including ME-14 safety cases. Live API/DB/provider/browser runtime is not verified.

- API refs: #62 is used by ME-13 to choose recipients; ME-14 does not refetch it. ME-14 posts to #63. SH-07 reads the accepted UUID through #18; #64 remains a separate per-notification-ID API.
- Current producer slice: ME-13 passes course context and selected Student IDs in router state; ME-14 validates the selection, sends trimmed text and explicit `PUSH`/`EMAIL` values, then routes a valid accepted UUID to SH-07. API #63 does not accept `course_id`, so the server cannot bind this request to the exact selected course.
- API DDs remain Draft/derived for broader semantics. Attachment, draft persistence, exact course binding, provider delivery and browser runtime remain unresolved or unverified; they do not block the implemented text/recipient/channel submit slice.
- Contract/design excerpts below preserve the earlier DD snapshot; current source behavior is summarized above.

### Trích từ DD nguồn: Nguồn truy vết

- Inventory/route/API/dependencies: [list_screen.md](../../list_screen.md), [global DD screen plan](../../screen_stitch/dd_screens/PLAN.md).
- Trước màn hình này: [ME-13.md](../../screen_stitch/04_mentor/ME-13_chon-nguoi-nhan-thong-bao/ME-13.md).
- Expected flow AC-25: `apps/study-server/docs/diagrams/AC_UNICA/AC_03_MENTOR_TEACHING.drawio` (page AC-25).
- #63 local source: `apps/study-server/app/api/v1.py`; `apps/study-server/app/modules/mentor/api_63_mentor_notifications_create/`; DD `apps/study-server/docs/dd/63_mentor_notifications_create/`; tests `apps/study-server/tests/modules/mentor/api_63_mentor_notifications_create/`.
- #64 local source: `apps/study-server/app/api/v1.py`; `apps/study-server/app/modules/mentor/api_64_mentor_notification_status/`; DD `apps/study-server/docs/dd/64_mentor_notifications_status/`; tests `apps/study-server/tests/modules/mentor/api_64_mentor_notification_status/`.
- #18 design/current-source status: `apps/study-server/docs/dd/18_operations/`; notification-only UUID route/module/query/tests are present, and current SH-07 calls it with owner-bound behavior. Generic operation kinds remain outside the implementation.
- #34 upload source: `apps/study-server/app/modules/shared/api_34_uploads/`; DD `apps/study-server/docs/dd/34_uploads/`.
- Screen prototype: `code.html`, `screen.png`; the `UNWIRED` note in the 2026-11-08 source snapshot is historical. Current Study Client route/composer source is summarized below; browser/runtime remains unverified.

### Earlier client source snapshot (superseded 2026-11-21)

The following source notes described the pre-implementation state. Current ME-14 calls #63 with text `content`, selected recipients and explicit channels, then routes the accepted UUID to SH-07. The #63 request still has no `course_id` or idempotency key; provider delivery and browser runtime remain unverified.

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/04_mentor/ME-14_soan-thong-bao-mentor/ME-14.md)
