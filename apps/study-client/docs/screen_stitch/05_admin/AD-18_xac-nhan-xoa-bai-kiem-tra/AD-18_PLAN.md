# AD-18 — Kế hoạch đặc tả màn hình xác nhận xóa bài kiểm tra

## Mục tiêu và phạm vi

Hoàn thiện riêng màn hình AD-18 theo inventory row 76, AC-35 và API #90. Giữ nguyên `screen.png`/`code.html`; lập bản đồ marker một-một, tạo ảnh đánh số 2× và viết DD A–F có truy vết expected/current tách biệt. Không xử lý AD-19 trong phiên này.

| Thuộc tính | Expected / nguồn thiết kế | Current evidence |
|---|---|---|
| Actor/permission | AC-35: Admin có quyền quản lý quiz. | Local #90 chỉ kiểm tra role `ADMIN`; fine-grained quiz-management policy chưa có nguồn. |
| Route | Inventory: `/admin/quizzes/:quizId/delete`; AD-15 là entry point và màn quay lại. | Study Web không có source/router/API client; các anchor HTML đều `href="#"`. Route chỉ là candidate. |
| Target record | Admin kiểm tra tác động tới attempts rồi xác nhận. | HTML/PNG hiện “Chưa chọn bản ghi”, `--`; #87 chỉ có ID, course_id, title, duration, passing score, `questions=[]`; không có GET quiz detail. Course title và history count không map được. |
| Delete | AC-35 n10 yêu cầu soft delete nếu có attempts. Catalog #90: path-only DELETE, DeleteResult; 200/401/403/404/422/500. | Local #90 soft-deletes khi attempts hoặc answers tham chiếu tồn tại; hard-deletes child/quiz khi không có history. Đây là local `DERIVED`, chưa được owner duyệt. |
| UI state | Inventory: `confirm/deleting/conflict/deleted`; #87 invalidate sau xóa. | Prototype confirm button và audit textarea disabled; không có listener/request. Catalog #90 không khai báo 409/conflict. |
| Data/history | Giữ history nếu attempts tồn tại theo AC-35. | API #87 ẩn tombstone; #89 từ chối sửa quiz có history/tombstone; #91 vẫn tính thống kê quiz tombstone. Attempt-create #29 chưa có route/module local để chứng minh race safety. |
| Runtime | — | `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`. |

## Nguồn và thứ tự xử lý

1. `apps/study-client/docs/list_screen.md` row 76, API reverse index #090 và G-11; global screen plan AD-18 row/checkpoint.
2. `apps/study-server/docs/diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio` (AC-35 nodes n9/n10), `docs/lists/list_api.md` #90, API #90 Draft DD / OPEN_QUESTIONS.
3. AD-15 DD và API #87 source để xác định data handoff; API #89/#91 current lifecycle; API #90 route, validator, query, model, view, test source và verification report.
4. Current Study Web file tree; original AD-18 PNG and HTML. Preserve asset hashes.
5. Save this plan before creating marker JSON/SVG, annotated PNG, or DD.

## Sơ đồ khu vực và marker map (source image 1600×1442)

| Marker | Element/region | Planned target |
|---:|---|---|
| 1 | Study2Work LMS/Admin brand | Shell header left |
| 2–6 | Shell navigation: Overview, Users, Courses/Content, Moderation, Reports | Header navigation |
| 7 | System Normal status copy (static) | Header right |
| 8 | Notifications button (no handler) | Header right |
| 9 | Admin identity/avatar (static) | Header right |
| 10 | Global breadcrumb | Shell second row |
| 11 | RBAC assurance copy (static) | Shell second row right |
| 12–14 | Local breadcrumb: quiz admin, AD-15 list, current delete label | Local navigation card |
| 15 | Return-to-AD-15 link (anchor is `#`) | Local navigation card right |
| 16–18 | Danger icon, risk label, confirmation title | Main panel header |
| 19 | Target record section heading | Record card |
| 20 | Selected-record status pill (placeholder) | Record card right |
| 21 | Quiz title field/value (`--`) | Record card, first column |
| 22 | Quiz identifier field/value (not selected) | Record card, second column |
| 23 | Linked course field/value (`--`) | Record card, third column |
| 24–28 | Safety icon, policy heading, warning text, unresolved-attempt rule copy, read-only status copy | Warning card |
| 29–32 | Audit reason label, ISO claim, disabled textarea, disabled-field hint | Audit input region |
| 33 | Safe return link (anchor is `#`) | Bottom actions |
| 34 | Permanent delete button (disabled; no handler) | Bottom actions |
| 35–36 | Data-protection banner copy and compliance badge (static claims) | Main panel footer |
| 37–40 | Copyright/system label, privacy link, RBAC standards link, support link | Global footer |

All markers will use integer source-pixel coordinates with origin at top-left. The Markdown element table and JSON/SVG marker numbers must be exactly 1–40 in order. Markers describe visible groups/controls; decorative divider, glyphs, and repeated text within each group do not become separate interactive controls.

## Event/data plan

1. **EV-01 — Open candidate route / identify target:** accept `quizId` from route candidate. No detail GET exists in inventory. AD-15 local #87 can provide only `id`, `course_id`, `title`, `duration_minutes`, `passing_score`; it cannot supply course display name or attempts/history. Do not invent a second API or claim the target is loaded. Check approved Admin permission before showing actionable content once a route guard exists.
2. **EV-02 — Return to AD-15:** top back link and list breadcrumb indicate return, but HTML anchors are `#`. Route/history behavior and filter/page handoff are not wired. Specify intended return as AD-15 only as design expectation.
3. **EV-03 — Safe cancel:** safe-return anchor is `#`; no handler. Candidate cancel returns to AD-15 or previous safe page after route owner selects a rule. No mutation.
4. **EV-04 — Confirm deletion:** current button is disabled and has no handler. If policy/permission/data contract is approved and control is enabled: validate a positive signed-int64 `quizId` (local source behavior), send exactly one `DELETE /api/v1/admin/quizzes/{quiz_id}` with Bearer JWT, no query/body, map catalog success/error envelope. 200 `DESIGN_RESOURCE_DELETED` returns `{id,status:"deleted",deleted_at}`. 401/403/404/422/500 map to auth/access/not-found/invalid-ID/service-error. Do not create a 409 branch; inventory `conflict` state has no API support. On success, inventory expects #87 invalidation; exact success navigation and cache mechanism remain open because no client exists.
5. **EV-05 — Audit reason field:** disabled in HTML; #90 catalog has no body and local route deliberately reads no body. Do not enable/send the text until a new approved request contract exists.
6. **EV-06 — Shell notification/navigation controls:** prototype contains notification button without handler and `#` shell/footer anchors. Document them as static/no-op; do not infer destinations or data.

## Required source decisions / blockers

- Approve behavior when no attempt exists; AC-35 is silent while local code physically deletes.
- Confirm whether answer-only references trigger tombstone, accepted status value `DELETED`, `updated_at`→`deleted_at` mapping, timezone, and repeated DELETE result.
- Resolve API #29 concurrent attempt creation and ensure #90 locking is compatible; local #29 route/module was not found.
- Confirm post-delete visibility in #87, edit restrictions in #89, and history/statistics access in #91; current local behavior is not approved policy.
- Resolve AC-35 quiz-management permission vs shared `ADMIN` role guard.
- Decide how route receives target Quiz and course name; no detail API is present and #87 omits course title/history count.
- Resolve inventory `conflict` state vs #90 catalog without 409; HTTP 422 means request validation in the current source, not dependency conflict.
- Study Web runtime, live DB schema/deployment and client cache behavior are unverified.

## Acceptance audit

- [x] Original `screen.png` 1600×1442 and `code.html` hashes stay unchanged.
- [x] Marker IDs 1–40 are sequential, unique, in-bounds, visually legible and map one-to-one to DD element rows.
- [x] SVG and JSON coordinates match DD; annotated PNG renders at 3200×2884 and has been visually reviewed.
- [x] DD includes A–F, detailed EV-01…EV-06, API #90 direct catalog vs local source, route/data mapping, error/status matrix and blockers.
- [x] Relative links resolve; screen inventory remains 83 IDs/folders; core artifact count increases by one (70/83 → 71/83).
- [x] Reverse API index #090, G-11, global AD-18 status/checkpoint and worklog reflect current evidence.
- [x] `git diff --check` and static artifact audit pass. App tests/runtime were not run for this documentation task.
