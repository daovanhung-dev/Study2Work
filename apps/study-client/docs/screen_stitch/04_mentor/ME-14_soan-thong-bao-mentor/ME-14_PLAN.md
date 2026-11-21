# ME-14 Detailed Design Plan

## 1. Scope and result target

- Screen ID: `ME-14` — Soạn thông báo mentor (Step 2: compose notification content).
- Session scope: ME-14 only. Do not start ME-15 in this session.
- Deliverables: `ME-14_PLAN.md` (this file), `ME-14_markers.json`, `screen_annotated.png`, and `ME-14.md` with sections A–F.
- Preserve the source `screen.png` and `code.html` byte-for-byte.
- Use the screen image's top-left pixel coordinate system. Each independent visible element gets one sequential marker and exactly one corresponding element record.
- Statuses are tracked separately: document readiness, implementation blockers, and runtime verification.

## 2. Source inventory and preservation baseline

| Asset | Initial evidence | Handling |
|---|---|---|
| `screen.png` | 1267×1600; SHA-256 `bc6d536347650aaa8ab357da960fe14753b4b261b5c77657af0e90072f9b2324` | Preserve unchanged; annotate a scaled copy only. |
| `code.html` | 31,875 bytes; SHA-256 `ebb83dd43389906390a57bd16895311fca1a12c5ff8c1b02b0b0078f5af2c6de` | Preserve unchanged; use only as static prototype evidence. |
| Existing ME-14 DD/plan/markers | None before this plan | Create the three remaining artifacts after this plan is saved. |

## 3. Expected behavior and current behavior

### Expected behavior

- `list_screen.md` describes ME-14 at `/mentor/notifications/new`, AC-25, APIs #62/#63, next ME-15, and draft/validation/send/accept/error states.
- ME-13 precedes this screen and supplies selected recipient identity. ME-13's exact state carrier and course identity are unresolved; do not invent route state, query parameters, browser storage, or serialization.
- AC-25 describes course and active-student selection, then notice title/content/recipients/channels, POST #63, queued dispatch, and later #64 status reads.

### Current local source

- Study Web is `UNWIRED`; this HTML is a static mockup. Its only script mirrors title/body into the preview and updates counters. It has no application route, authentication/session logic, API call, save handler, send handler, upload input, or persistent state.
- API #63 is present in local Study Server source with a strict body: `recipients:string`, `title:string` (max 200), `content:int64`, `channels:string`. It validates Mentor auth, CSV input, and that recipients are ACTIVE students in at least one common course directly owned by the Mentor. It has no `course_id`, attachment, or idempotency key.
- API #63 writes one legacy notification per recipient and queued delivery rows per channel in a transaction, returning 202 only after commit. It returns an Operation UUID as `data.id` and notification int64 IDs in `meta.notification_ids`; queued acceptance does not prove delivery. The OpenAPI/API DD remains Draft and parts of request/scope/projection are DERIVED.
- API #64 reads an individual notification status by int64 notification ID and reconstructs an Operation response from notification/outbox rows. It is a local read-only route; worker/provider delivery is not wired or runtime verified.
- API #18 has a design DD/catalog row but no Study route, module, query, or test. Its ID type and lifecycle are unresolved. AC-25 does not connect #18 to the notification flow; the ME-14 send path must not poll it by inference.
- API #34 uploads only `SUBMISSION` or `LECTURE` purpose, with no application MIME allowlist or size cap. It has no notification-purpose attachment relationship; its current contract cannot satisfy this screen's claimed PDF/DOCX/ZIP ≤25MB attachment behavior.

## 4. Planned marker and element coverage

Annotate visible, independently meaningful controls/content in reading order, including:

1. Mentor header brand, navigation items, notification icon, identity.
2. Breadcrumbs, stepper, editor heading/introduction, missing-recipient warning, and link back to ME-13.
3. Recipient summary/lock state; title label/input/count; in-app and disabled email channel controls; editor label/formatting toolbar/body/word count.
4. Attachment copy/button; security warning; back, save-draft, and disabled-send actions.
5. Preview header, channel/author/title/body placeholders, static visibility/product labels, and response-rate metric.
6. Message-standard guidance/image, help link, footer brand/compliance copy, and footer navigation.

The final marker list is the source of truth for section C. Decorative backgrounds and repeated glyphs are grouped with their owning card/control; visible claims with implementation or contract implications receive distinct records.

## 5. Planned event coverage

Document each trigger with preconditions, exact input, ordered processing, output/UI state, and error or unavailable-state behavior. Include:

- E01 initial screen load and ME-13 recipient/course context availability (currently unresolved; no inferred fetch).
- E02 title input and preview/count synchronization; UI limit 120 versus #63 max 200.
- E03 channel change; prototype defaults In-app and disables Email; backend token/channel mapping is not approved and provider delivery is absent.
- E04 body input, word count and preview; toolbar buttons are inert; backend `content:int64` conflicts with free-form rich text.
- E05 attachment selection; button has no file input, and #34 purpose/relationship does not support notification attachments.
- E06 save draft; no draft endpoint, local storage, or handler exists.
- E07 send; the prototype button is disabled. If an approved flow later enables it, document #63's exact request/response/errors and transaction effects while preserving unresolved field mappings and blockers.
- E08 back to ME-13; prototype links use `href="#"`; recipient-state preservation is not specified.
- E09 header, breadcrumb, help and footer navigation; all are prototype placeholders, with destinations not established.
- E10 form validation/focus and preview empty/default behavior only to the extent present in HTML; do not claim client validation not implemented by the artifact.

## 6. Sources to trace in the DD

- Screen inventory and cross-screen link: `apps/study-client/docs/list_screen.md`.
- Prior screen handoff: `04_mentor/ME-13_chon-nguoi-nhan-thong-bao/ME-13.md`.
- API flow: `apps/study-server/docs/diagrams/AC_UNICA/AC_03_MENTOR_TEACHING.drawio`, page AC-25.
- API #63: router, `api_63_mentor_notifications_create` module, API #63 DD and tests.
- API #64: router, `api_64_mentor_notification_status` module, API #64 DD and tests.
- API #18: catalog/DD plus current route/module scan (expected `UNWIRED`/`NOT_FOUND`).
- API #34: route, upload module, DD, and current purpose/metadata model.
- Study Web registry/context: `.agents/context-manifest.json`, `.agents/web-study/` and `.agents/web-work/`.

## 7. Known blockers and discrepancy handling

| Topic | Evidence | Design disposition |
|---|---|---|
| Recipient handoff/course binding | ME-13 selected int64 IDs; #63 takes only CSV recipients and infers any common Mentor-owned course. | Mark as BLOCKER; do not prescribe a carrier or claim course-bound send. |
| Free text vs API `content:int64` | Prototype is a free-text body; #63 requires signed int64. | Mark as BLOCKER; do not cast, truncate, or invent a content ID. |
| Title bounds | HTML max 120; local #63 max 200. | Preserve the visible limit as prototype evidence and report discrepancy; do not choose a new UI rule. |
| Channel names and delivery | Prototype says In-app/Email; #63 uses PUSH/EMAIL; no worker/provider is wired. | Mapping and actual delivery claims remain blocked. |
| Attachment | Prototype claims PDF/DOCX/ZIP ≤25MB; HTML has no file input; #34 has only SUBMISSION/LECTURE and no attachment link in #63. | Mark unsupported and blocked; do not cite #34 as a usable notification upload path. |
| Save draft | Button exists without endpoint or persistence. | Prototype affordance only; blocked until a draft contract exists. |
| Generic operation tracking | API #18 is unwired; UUID/int64 and lifecycle issues remain; AC-25 has no #18 edge. | Do not call #18 from ME-14. Keep operation ID distinct from notification IDs; #64 is the local notification-status path. |
| Static metrics/compliance copy | Preview rate, channel visibility and WCAG claim are static prototype copy, not verified source behavior. | Identify as unverified content; do not turn into requirements. |

## 8. Review and static verification gate

- Confirm source hashes remain unchanged.
- Confirm markers are contiguous from 1 through N, unique, in image bounds, and match exactly N DD element records.
- Confirm the annotated PNG is readable at full resolution and markers avoid important text.
- Confirm every identified control and meaningful static claim has a DD element record and relevant event(s).
- Confirm every API statement cites the exact catalog/DD/source boundary and keeps Draft/DERIVED/UNWIRED/RUNTIME NOT VERIFIED labels separate.
- Check local links, image paths, Markdown structure, JSON parse, and `git diff --check`.
- Do not run application tests or claim runtime verification for this docs-only task.
