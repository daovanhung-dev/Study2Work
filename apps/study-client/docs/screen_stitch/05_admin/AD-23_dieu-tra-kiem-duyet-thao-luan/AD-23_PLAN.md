# AD-23 — Detailed Design Plan

## 1. Scope and order

- Screen: AD-23, “Điều tra/kiểm duyệt thảo luận” (inventory row 81).
- Scope: document the static investigation/moderation placeholder, expected AC-37 flow, catalog APIs #98–#100, local #98 source behavior, current source gaps for #99/#100, and the AD-22/#97 return handoff.
- Boundary: AD-23 only. Do not start AD-24. Do not define missing report, moderation, audit, permission, or delete rules.
- Required order: source/contract review → this plan → markers/overlay and annotated image → A–F DD → inventory/API reverse index/global plan/worklog → static audit.
- No application tests or runtime verification are planned.

## 2. Evidence and source hashes

| Evidence | Use | Status |
|---|---|---|
| [`screen.png`](./screen.png), 1505×1600 | Original visual source; preserve unchanged. | Source asset |
| [`code.html`](./code.html) | Placeholder DOM, disabled controls, anchor targets, absence of handlers/API calls. | Static prototype only |
| Inventory row 81 in [`list_screen.md`](../../../list_screen.md) | Candidate route, AC/API links, expected states, and current blocker. | Design requirement |
| AC-37 in [`AC_04_ADMIN_MANAGEMENT.drawio`](../../../../../study-server/docs/diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio) | Expected queue → detail → moderation/audit → optional delete → queue flow. | Expected flow; open branch contract |
| [`list_api.md`](../../../../../../docs/lists/list_api.md), #98–#100 | Direct catalog method, path/body, auth role, response and business codes. | Approved design catalog; not runtime by itself |
| Study Server router and `api_98_admin_discussions_detail` module/tests | Local #98 route, `ADMIN` guard, validation, query, projection, side effects, errors, characterization tests. | Current local source; test source inspected, not run |
| API DD #98–#100 and candidate migration/DDL | Existing status and unresolved action/audit/delete/report persistence mapping. | Draft/open questions; DDL is not live-schema proof |
| [Study Web design context](../../../../../../.agents/web-study/design.md) and Study client tree | UI conventions and editable client/runtime availability. | Design context; Study Web is UNWIRED |

Original hashes captured before edits:

- `screen.png`: `2f3787dfdaab4a82b7ddf31a266f3dc0dadb3abe17eb696bfe6790c7c91070bf`
- `code.html`: `8e8d8fe38bbd6f5c9e5e0cd0a184acc0988a9c90732dda199e4ae2d9fd13d74b`

## 3. Expected flow and current boundary

- Expected: AD-22 supplies a valid Discussion ID; #98 returns thread and report context; an Admin evaluates the report; #99 applies an approved action and reason with audit; optional #100 soft-deletes while preserving audit; the queue is refreshed through #97 or AD-22 is revisited.
- Current local #98: route/module/query/test source is registered. It checks local role `ADMIN`, validates positive int64 `discussion_id`, reads the Discussion and direct child comments, and returns a one-item `Page<Discussion>`. It does not query reports or mutate state. Its API DD still says `UNWIRED / NOT_FOUND`, a source/DD discrepancy.
- Current #99/#100: catalog and Draft API DDs exist; no local route/module/query/model/test source was found. Their behavior is not runtime verified.
- Current Study Web: no tracked editable `src` route/client exists; the HTML is a static placeholder, all moderation controls are disabled, and no handler/API call is present.
- AC-37 says “dismiss report” on the no-violation branch, but no dismissal endpoint is listed. The prototype’s permanent-delete choice sits in the #99 radio group even though AC separates optional deletion to #100 and describes soft delete with audit preservation.

## 4. Plan for element coverage and annotation

Create 45 sequential markers, each mapped one-to-one to a row in `AD-23.md` §C. Coordinates are circle centers in original 1505×1600 screenshot pixels. Render the annotation at 2× (3010×3200), keep the original aspect ratio, and put markers on component edges/whitespace where practical. JSON and SVG use the same source-pixel coordinates and IDs.

| # | Planned component | Marker center (x,y) |
|---:|---|---:|
| 1 | Study2Work brand / portal mark | 16, 32 |
| 2 | Navigation: Tổng quan | 280, 33 |
| 3 | Navigation: Người dùng | 404, 33 |
| 4 | Navigation: Khóa học & Nội dung | 540, 33 |
| 5 | Navigation: Kiểm duyệt | 740, 33 |
| 6 | Navigation: Báo cáo | 870, 33 |
| 7 | System Normal status | 996, 33 |
| 8 | Notifications bell | 1180, 33 |
| 9 | Admin identity/avatar | 1260, 33 |
| 10 | Global breadcrumb | 17, 89 |
| 11 | RBAC verification badge | 1290, 89 |
| 12 | Local moderation breadcrumb | 23, 160 |
| 13 | Return-to-AD-22 header button | 1121, 170 |
| 14 | Screen title | 18, 196 |
| 15 | Target discussion panel heading/icon | 48, 286 |
| 16 | Target load-status badge | 1153, 286 |
| 17 | Discussion ID summary card | 80, 313 |
| 18 | Course summary card | 430, 313 |
| 19 | Author summary card | 780, 313 |
| 20 | Discussion status summary card | 1130, 313 |
| 21 | Audit/policy banner icon | 44, 496 |
| 22 | Audit/policy banner heading | 103, 494 |
| 23 | Audit/policy banner copy | 103, 553 |
| 24 | Thread panel heading/icon | 56, 662 |
| 25 | Thread display-mode badge | 835, 664 |
| 26 | Empty-thread icon | 510, 854 |
| 27 | Empty-thread title | 630, 930 |
| 28 | Empty-thread explanatory copy | 750, 984 |
| 29 | Empty-thread return-to-AD-22 CTA | 620, 1048 |
| 30 | Moderation action panel heading/icon | 908, 664 |
| 31 | Safety-lock badge | 1262, 663 |
| 32 | Action-group label | 909, 721 |
| 33 | Hide-temporarily option card | 913, 787 |
| 34 | Lock-comments option card | 913, 881 |
| 35 | Warn-author option card | 913, 972 |
| 36 | Permanent-delete option card | 913, 1063 |
| 37 | Reason input label | 911, 1142 |
| 38 | Disabled reason textarea | 1438, 1197 |
| 39 | Audit-note copy | 1438, 1300 |
| 40 | Disabled apply-decision button | 1438, 1375 |
| 41 | Cancel/return link | 1438, 1440 |
| 42 | Footer copyright | 18, 1572 |
| 43 | Footer privacy link | 830, 1572 |
| 44 | Footer RBAC standards link | 1029, 1572 |
| 45 | Footer support link | 1288, 1572 |

## 5. Event inventory to specify

| Event | Trigger | Planned treatment |
|---|---|---|
| EV-01 — Load moderation detail | Screen entry / future `Load` | Separate expected #98 contract from current local source and static placeholder. Record unresolved ID handoff, missing report projection, response/error behavior and auth distinction. |
| EV-02 — Return from header | Header button click | Inventory/AC link to AD-22; prototype anchor is `#ad-22`, with no router/history behavior. No refresh/cache semantics are specified. |
| EV-03 — Return from empty thread | Empty-state CTA click | Same AD-22 link. Do not infer a report ID or which previous filters/page are restored. |
| EV-04 — Select moderation action | Radio change | Four radios are disabled and have no values. #99 accepts generic `action:string`, but exact tokens and transitions are unresolved; delete belongs to separate optional #100 per AC. |
| EV-05 — Enter reason | Text input | Textarea disabled. Catalog #99 requires string `reason`; length/blank rules and audit persistence are unspecified. No validation is invented. |
| EV-06 — Apply decision | Button submit/click | Button is disabled and has no handler. Describe only the conditional catalog #99 PATCH envelope/auth/body/errors; no success or retry behavior is claimed. |
| EV-07 — Optional delete | Future action flow | AC/catalog place deletion on separate #100 DELETE, not #99 radio submission; soft-delete/audit mapping and confirmation/eligibility are unresolved. No confirmation UI is added from inference. |
| EV-08 — Cancel/return | Link click | Prototype fragment `#ad-22`; expected screen link AD-22. No decision state exists to discard in current HTML. |
| EV-09 — Shell, notifications and footer navigation | Anchor/button interaction | Static fragment links / no bell handler; target routes are not wired. |

## 6. DD authoring and static verification

1. Write `AD-23.md` sections A–F with 45 element rows and EV-01…EV-09.
2. Keep expected AC/catalog behavior, prototype behavior, local #98 source, and unresolved #99/#100 behavior separate. Include success and errors only where the direct contract/local source supports them.
3. Explain that #98 currently maps Discussion and direct comments only; do not fabricate report reasons, severity, reporter, report count, or audit fields. Distinguish catalog response from current local projection and note API DD #98’s stale runtime label.
4. Record the #99 delete-radio mismatch, AC no-violation dismissal without an endpoint, Admin vs local `ADMIN`, root/reply grain, and missing Study Web source as blockers.
5. Create `AD-23_markers.json`, `AD-23_markers_overlay.svg`, and `screen_annotated.png` after this plan. Review full-size annotation visually and move any marker obscuring meaningful copy.
6. Update inventory row 81 and API reverse-index #098–#100 using separate source-status and DD/runtime-status labels. Append the AD-23 checkpoint to the global plan; do not start AD-24.
7. Static audit: IDs 1–45 unique/sequential, in bounds, aligned across plan/JSON/SVG/DD; all A–F and events present; relative links resolve; JSON/SVG parse; annotated dimensions 3010×3200; source image/HTML hashes unchanged; 83 inventory IDs/folders remain; core artifact count updated; `git diff --check` passes.

## 7. Known blockers to carry into the DD

- #98 current source omits reports even though AC-37 expects report context; #97 report persistence/writer and live schema remain unverified.
- API #98 DD still labels its implementation `UNWIRED / NOT_FOUND` despite current registered local route/module/test source.
- #99/#100 are catalog/Draft-only with no current local routes/tests; action tokens, transitions, reason validation, audit persistence/actor/atomicity, delete state/timestamp/eligibility/retention and concurrency policy remain open.
- AC-37 no-violation dismissal branch has no listed endpoint.
- Discussion root/reply report target and thread visibility rules are unresolved.
- AC/catalog Admin actor and permission mapping do not establish the local `ADMIN` authorization rule for #99/#100.
- The prototype claims warning delivery, automatic audit logging and complete permanent deletion without source-backed behavior; delete radio also conflicts with the separate #100 flow.
- Study Web route/client is UNWIRED; no runtime verification is available.
