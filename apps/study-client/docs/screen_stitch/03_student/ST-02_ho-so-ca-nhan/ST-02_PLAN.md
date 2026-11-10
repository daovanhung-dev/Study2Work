# ST-02 — Kế hoạch chi tiết

> Ngày rà soát: 2026-11-06
>
> Trạng thái: `PLAN COMPLETE; DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED`

## 1. Phạm vi và phân loại

```text
primary_task_type: docs
secondary_task_types: []
project_scopes: [web-work, server-study]
cross_scope_dependencies: [ST-02 GET API #04; auth/session handoff from SH-02; navigation to ST-03]
```

- Chỉ xử lý **ST-02 — Hồ sơ cá nhân (Page)** trong phiên này.
- Inventory: route đề xuất `/student/profile`; AC-11; API #04; actor Student; link ST-03. Expected states `loading/ready/401/403`; cache profile theo dòng màn hình.
- Theo `list_screen.md` §8.1, ST-02 là P0 trong W0 và chưa có artifact DD; ST-01 thuộc W3 vì dashboard APIs chưa nối. Guest group chỉ có GS-01..GS-07; không tồn tại GS-08. Sửa handoff pointer cũ trong global tracker sau khi hoàn thành ST-02.

## 2. Nguồn và baseline

- Source folder ban đầu chỉ có `screen.png` và `code.html`; giữ nguyên cả hai.
- `screen.png` là PNG hợp lệ 1280×1078, SHA-256 `d708cf38575a9ef14352ea5937379e191448bdb62341f7b1fc90f5e50144f379`. Ảnh cho thấy header và footer; phần nội dung giữa trống.
- `code.html` SHA-256 `9969e179da65352894ac2eead28147f341b47b5fb226c6047c7b62345a265cc1`. HTML có tiêu đề “Hồ sơ cá nhân”, empty/sign-in card, login CTA và disabled edit button; nội dung này không xuất hiện trong `screen.png`.
- Kế hoạch: render HTML nguyên trạng thành `screen_rendered.png` bằng Firefox headless và giữ `screen.png` làm ảnh gốc. Sau render phải xem trực tiếp; nếu render không hoàn chỉnh thì không dùng làm ảnh chú thích và ghi rõ giới hạn.
- Firefox chụp đúng viewport 1280×1078, nhưng HTML đặt `main` tối thiểu bằng chiều cao viewport trừ header nên footer nằm ngoài ảnh. Vì PNG gốc giữ footer đầy đủ nhưng body trống, tạo thêm `screen_composite.png`: giữ toàn bộ PNG gốc, chèn phần body từ `screen_rendered.png` tại vị trí gốc. Giữ nguyên `screen.png`, `code.html` và bản render HTML thuần; ghi rõ hai nguồn trong marker map. Ảnh composite là review asset, không phải runtime capture.

## 3. Expected behavior và current evidence

| Chủ đề | Expected/design source | Current evidence | Tác động |
|---|---|---|---|
| Actor/access | AC-11 Student đã đăng nhập; route `/student/profile`. #04 chỉ cho JWT role STUDENT. | Screenshot body trống; HTML cho thấy nội dung sign-in dù inventory gọi đây là màn Student. Không có Study Web source/router/session. | Actor/state mismatch và `UNWIRED`; không tuyên bố auth redirect. |
| Profile data | API #04 GET Bearer; avatar/email/role/status; current screen flow có cache profile. AC-02/AC-11 gọi #04. | Current source route/view/query/model có thật; SELECT theo numeric JWT `sub`; trả id/full_name/email/role/avatar_url/phone/status/created_at/updated_at. | Source-backed backend nhưng chưa được UI gọi. Không tạo UI field/layout cho loaded profile khi chưa có design. |
| Authorization | Catalog/AC yêu cầu Bearer JWT, Student role; 401/403/500. | Shared guard parse `sub` positive numeric ID và `roles` list; yêu cầu `STUDENT` trước DB. Không so role JWT với `users.role`, không lọc `users.status`. | Token role/status freshness và account-locked behavior còn mở. |
| Response | `ApiEnvelope<UserProfile>`; AC-02 còn nói profile/role/permissions. Catalog có optional bio. | Current response không có permissions hoặc bio; extra model fields bị ignore. `avatar_url` và `phone` nullable; `status` bắt buộc trong model. | Contract/source/UI mapping discrepancy. |
| Profile edit | ST-03 owns edit; AC-11 also references APIs #13/#14. | HTML button “Chỉnh sửa hồ sơ (Tạm khóa)” is disabled; API #13/#14 have separate contracts and remain ST-03 scope. | Không enable hoặc kéo upload/save behavior vào ST-02. |
| Navigation | Login/role handoff to Student route; current Student can visit ST-02 and continue to ST-03. | All anchors use `href="#"` and `data-path`; app router absent. | Route/history/return-to behavior `UNWIRED`. |

### API #04 current source trace

1. `/api/v1/users/me` route accepts one optional `Authorization` header at FastAPI boundary, DB session and trace ID, then calls `get_current_user`.
2. View calls shared `validate_current_user_request(..., role="STUDENT")` before database access. Missing/malformed/invalid JWT or invalid `sub`/`roles` → 401; valid token without Student role → 403.
3. Parsed positive numeric `sub` becomes `user_id`; `CURRENT_USER_PROFILE` performs read-only `SELECT` from `users` by `id=:user_id`, `LIMIT 1`. It reads only safe profile columns and does not query `password_hash`.
4. Missing user row maps to 401 `DESIGN_AUTHENTICATION_REQUIRED` in current source; no 404 branch. SQLAlchemy failure rolls back and maps to 500; invalid `UserProfile` mapping maps to 500. No DB mutation or external side effect.
5. Success is HTTP 200 `DESIGN_RESOURCE_RETRIEVED`; current data excludes `bio`/permissions. Test source confirms these branches but will not be run in this docs task.

### Known contract gaps

- API #04 DD is `Draft — Needs Confirmation`. Catalog repeats auth notation; route has one Authorization header. AC-02 says claims `user_id`/`role`, current #03/#04 use `sub`/`roles`.
- AC-02 mentions permissions but #04 has no permission query/model/field. AC-11 expects `bio` in edit flow; catalog marks it optional but #04 does not select or serialize it.
- API #03 login currently already returns a base profile with its token; design says #04 is then called for Student. Purpose/freshness/cache policy of the second read is unresolved.
- Query reads DB `role/status` for display but authorization trusts JWT `roles`; it does not compare them or reject a locked DB account. Checked-in `DB.sql` lets `users.status` be nullable despite `UserProfile.status` being required. Live schema is `NOT_VERIFIED`.

## 4. Planned annotation and event coverage

Create 10 ordered component markers, with one DD row per marker, using side gutters on `screen_composite.png`:

1. Header brand anchor.
2. Header primary navigation group (Home, Courses, My Courses, Profile; static active style).
3. Header login link.
4. Page title and supporting description.
5. Profile card surface/icon.
6. Profile card heading and sign-in explanation.
7. Card login CTA.
8. Disabled edit-profile button.
9. Footer brand link.
10. Footer navigation group.

Planned events: `ST02-EV-01` direct entry/profile load and API #04 expected flow; `ST02-EV-02` header navigation; `ST02-EV-03` header/card login anchors; `ST02-EV-04` disabled edit action; `ST02-EV-05` footer links. All current anchors are static `href="#"`; disabled edit has no click action.

## 5. Planned output and acceptance

- Preserve the two original assets and record hashes.
- Add `ST-02_PLAN.md` before rendering/annotation/DD; render and visually inspect `screen_rendered.png` from `code.html`. Keep it as evidence of the HTML-only render; use documented `screen_composite.png` for annotation because the provided screenshot omits the body and the viewport capture omits footer text.
- Add 10 ordered marker records, SVG overlay and `screen_annotated.png`; map 1:1 to DD element rows.
- Add `ST-02.md` with overview, expected/current flow, each element, event inputs/preconditions/sequence/outcomes, #04 response/errors, state/access/navigation, conflicts and references.
- Update global tracker: ST-02 separate statuses, full artifact count 15/83, remaining incomplete count 68, and ST-03 next by the dependency wave in `list_screen.md` §8.1. ST-01 remains in W3 because its dashboard APIs are not wired. Never write GS-08.
- `DD BLOCKED` while the profile-ready design, permission/bio contract and token role/status policy remain unresolved. Keep `IMPLEMENTATION BLOCKED` and `RUNTIME NOT VERIFIED` separate. Do not run tests.

## 6. Kết quả kiểm tra tĩnh

- `screen.png` (`d708cf38575a9ef14352ea5937379e191448bdb62341f7b1fc90f5e50144f379`) và `code.html` (`9969e179da65352894ac2eead28147f341b47b5fb226c6047c7b62345a265cc1`) giữ nguyên hash gốc; `screen_rendered.png` (`162a7647579ba911783cc8975c71bea57a1d54595ec4f5e2951e1187f7b56e43`) giữ nguyên capture HTML thuần 1280×1078.
- `screen_composite.png` (`62b0f97f48582bf9941b352f7e98f4c33bdfaf774608204cc2978ee001060c7c`) giữ header/footer từ PNG gốc, chèn body crop (x=0, y=64, 1280×536) từ HTML render và vẫn ở 1280×1078. PNG đã được xem trực tiếp; footer cùng body đều thấy.
- `ST-02_markers.json` có 10 marker có thứ tự; 10 phần tử khớp 10 hàng element trong DD; overlay SVG và PNG chú thích được dựng từ composite; các link tương đối trong DD resolve.
- Không chạy test. API test source chỉ được đọc; UI/runtime và live schema chưa xác minh.

## 7. Preflight record

- `.agents/AGENTS.md`, `.agents/context-map.md`, `.agents/worklog/README.md`, `.agents/worklog/TEMPLATE.md` read.
- Exact-type selector: `node scripts/select-worklogs.mjs --type docs --limit 3`; result `READY`, 167 available, no shortage. Read GS-01, GS-02 and GS-03 worklogs individually before deep inspection.
- Cross-scope context read: `.agents/project/INDEX.md`, architecture/dependencies; web-work and Study Web entry/index/design; server-study entry/index/route/runtime/auth/database/tests; skill registry and `.agents/context-manifest.json`.
- Registry excludes `web-ui-only-dd` from `createDD-markdown`; no canonical skill applies to this UI-only screen DD. Do not load API DD authoring skill as if it were the UI contract.
