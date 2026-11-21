# AD-13 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `AD-13-EV-001` | `Source heading` / EV-01 — Mở route và tải lesson detail | See source event detail below |
| `AD-13-EV-002` | `Source heading` / EV-02 — Ánh xạ và hiển thị Lesson | See source event detail below |
| `AD-13-EV-003` | `Source heading` / EV-03 — Render content or video/media preview | See source event detail below |
| `AD-13-EV-004` | `Source heading` / EV-04 — Hiển thị resources, quizzes, discussion và progress dependencies | See source event detail below |
| `AD-13-EV-005` | `Source heading` / EV-05 — Hiển thị engagement metrics và SSE | See source event detail below |
| `AD-13-EV-006` | `Source heading` / EV-06 — Mở thao tác quản trị ở AD-14 | See source event detail below |
| `AD-13-EV-007` | `Source heading` / EV-07 — Quay lại danh sách AD-12 | See source event detail below |
| `AD-13-EV-008` | `Source heading` / EV-08 — Admin shell, status badges, standards and footer | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: D. Đặc tả chi tiết sự kiện

Prototype không implement các event sau; đây là target flow và source trace. Không có client retry/cache/timeout policy để ghi thành current behavior.

### EV-01 — Mở route và tải lesson detail

- **Trigger / element:** điều hướng từ row selection AD-12 tới route `/admin/lessons/:lessonId`; #16/#25/#44. **Type:** Load/navigation.
- **Precondition:** Admin session; expected lesson-management permission. Current server only enforces role `ADMIN`.
- **Input:** numeric `Lesson.id` từ response #82 → route param `lessonId` → path `lesson_id:int64!`; Bearer JWT; optional trace header. No body/query.
- **Processing:** (1) Shared Angular route-state helper checks the parameter exists and AD13Page validates the complete raw string against signed-int64 bounds; missing/malformed/out-of-range values show a local error and skip HTTP. (2) Valid raw ID is sent unchanged in GET #83; it is not replaced with course ID/slug or converted through `Number`. (3) Shared server guard validates Bearer/JWT/`ADMIN` before parse/DB. (4) Custom parser chấp nhận signed int64 string có dấu/leading zeros trong bounds; invalid/overflow/length>20→404 catalog code, no query. (5) Bind numeric ID vào query. (6) Select một lesson từ legacy candidate, `status IS DISTINCT FROM 'DELETED'`; không public `PUBLISHED` filter/dependency joins. (7) Validate returned identity/required Lesson fields. (8) Trả 200 direct Lesson hoặc exact errors.
- **Success:** `ApiEnvelope<Lesson>`; UI target nhận `data.id`, `course_id`, `title`, `content`, `video_url`, `order`, `status`. #83 không cập nhật DB/commit.
- **Errors:** 401, 403, 404 invalid/missing/deleted, 500 safe query/projection. Query/mapping/missing branches rollback per source.
- **UI state:** Angular AD-13 implements local missing/invalid-ID error without request, plus `loading`→`loaded` and API `error`; shared mapping distinguishes 401, 403 and 404 messages, while 500/network errors use a generic safe message. Focused page specs cover successful API field rendering and the AD-12 safe-ID handoff; tests were not run for this continuation and browser runtime remains unverified.

### EV-02 — Ánh xạ và hiển thị Lesson

- **Trigger / element:** successful EV-01 response; #22–#33.
- **Input:** exact `Lesson` object from #83. `course_id/order/status` are required in response model; `content`/`video_url` may be JSON null.
- **Processing:** map `id→lesson identifier`, `title→title`, `course_id→course ID`, `order→chapter order`, `status→raw status`. Do not map course name or content type because the fields are absent. Null content/video remains null; do not display static `--` as server value. If required projection fails server returns 500, rather than dropping the row or filling defaults.
- **Output:** target ready view may show only fields and labels approved by product. Status vocabulary/casing and course display rules need confirmation. Legacy DDL nullability mismatch remains open.

### EV-03 — Render content or video/media preview

- **Trigger / element:** content/video cards #24–#26 and #38 after a successful detail response.
- **Input:** nullable `data.content:string` and `data.video_url:string`; no other payload or signed locator.
- **Processing:** #83 only reads/returns string fields. It has no content-block schema, HTML sanitization contract, resource mapping, object-storage signer, URL allowlist, media proxy, expiry, DRM or playback authorization. Do not insert raw HTML or automatically open raw `video_url`. The mockup’s “technical parameters/media flow automatically extracted” is static, not supported processing.
- **Output/exceptions:** if either value is null, preserve null and show an approved empty state only after design decision. Safe preview/loading/unsupported-media UX and access rules require a media/content contract. No viewer events are wired.

### EV-04 — Hiển thị resources, quizzes, discussion và progress dependencies

- **Trigger / element:** linked-resource section #34–#41.
- **Input:** screenshot’s `Payload: Void`, 0 quizzes, 0 files, discussion “Khóa”; #83 returns none of these values.
- **Processing:** do not query relations client-side from inferred table names. AC-34 n5 says “lesson + dependencies” without defining fields/location; #83 has no relation collection/count. Current #86 independently locks the lesson and checks existence of `lesson_progress`, `resources`, `lesson_uploads` during delete; if any exists, it returns 422. It does not use an earlier #83 response, and it does not provide those counts to AD-13. Quiz/discussion dependencies are not among those #86 checks.
- **Output:** relationship tiles remain explicitly `STATIC_ONLY` until an owner supplies response/API semantics. Do not treat displayed zeros as safe-delete signal or claim delete eligibility.

### EV-05 — Hiển thị engagement metrics và SSE

- **Trigger / element:** #49–#55.
- **Input:** mockup has learner count, completion/submission rates, rating and an SSE connection label; API #83 has none.
- **Processing:** no metrics/SSE request, timer, `EventSource` or subscription exists in HTML or #83. Do not substitute a Mentor progress/analytics API without a contract connecting it to Admin AC-34; do not compute rates from a single Lesson object. Current `--`, zero-width bars, “waiting service” and “Disconnected” are authored static values.
- **Output:** no dynamic metric state can be claimed. Metric definitions, time window, aggregation grain, permissions and stream lifecycle are open.

### EV-06 — Mở thao tác quản trị ở AD-14

- **Trigger / element:** button #44, currently disabled.
- **Expected handoff:** carry the same numeric `lessonId` to AD-14. AC-34 branches to PUT #84 update, PATCH #85 status, or DELETE #86; those APIs/screens have separate request and confirmation rules.
- **Current behavior:** Stitch and Angular AD-13 both show a disabled action button; the Angular button has no mutation handler. AD-13 does not call a mutation. Do not enable the button or place mutation forms here based on its combined label.
- **Output/errors:** no navigation/action currently occurs. AD-14 route, access policy, editing state, confirmations, response refresh and `#86` dependency conflict UX belong to the separate AD-14 DD.

### EV-07 — Quay lại danh sách AD-12

- **Trigger / element:** back CTA #16, inline link #27, breadcrumb #13.
- **Current:** the Stitch prototype still uses `href="#"`. Angular AD-12 now links safe numeric lesson IDs to `/admin/lessons/:lessonId`; AD-13 back links use `RouterLink` to `/admin/lessons`. AD-14 remains disabled; filter/query/current-page preservation is not implemented.
- **Expected:** return to AD-12; the AC-34 workflow later reloads #82 after a successful downstream mutation. Whether normal back preserves filters/selection or refetches is not specified. Do not claim that the static links perform that navigation.

### EV-08 — Admin shell, status badges, standards and footer

- **Trigger / element:** shell/nav/notification #1–#11, page labels #15/#17–#21, standards/footer #56–#61.
- **Current:** static text and anchors; no Admin profile, health-check, notification, audit, sync, RBAC policy or compliance request. No active-page route source.
- **Expected UX boundary:** current Angular uses the shared host-scoped detail stylesheet and semantic route links/loading/error states. Continue following `.agents/web-study/design.md` for ocean tokens, typography, responsive reflow, keyboard/focus-visible and contrast. Browser comparison and accessibility verification remain open; the static mockup does not prove runtime behavior.
- **Output:** labels remain presentation-only; do not report a healthy endpoint, permission outcome, audit guarantee or student-isolation boundary from them.

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
