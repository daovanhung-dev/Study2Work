# ST-02 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `ST-02-TC-001` | Planning ref / not run | `AC-11` | See source acceptance section | P0 |

## 2. Test planning references

### ST-02-TC-001 — Acceptance planning reference (AC-11)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [ST-02](../../screen_stitch/03_student/ST-02_ho-so-ca-nhan/ST-02.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-11`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/03_student/ST-02_ho-so-ca-nhan/ST-02.md).

## 3. Source acceptance / test plan (not run)

### Trích từ DD nguồn: G. Tiêu chí nghiệm thu và nguồn

### Acceptance checklist

- [x] Original `screen.png` and `code.html` remain unchanged; their mismatch is recorded.
- [x] Every visible HTML-rendered component/control has an ordered marker and one DD element row.
- [x] Current #04 endpoint/auth/claims/query/data/errors/effects are traced to source and separated from AC/catalog/DD.
- [x] Login links, disabled edit, header/footer anchors, state/error branches and downstream ST-03 boundary are documented.
- [x] `bio`, permissions, cache, role/status freshness, null status/live schema and missing-user semantics remain explicit blockers.
- [ ] Authenticated profile-ready UI and runtime navigation verified — unavailable; implementation remains blocked.

### Nguồn

- Inventory/system flow: [`list_screen.md`](../../list_screen.md) ST-02, AC-02/AC-11, F01, G-02/G-03, waves W0/W1/W3 and global state/accessibility rules.
- AC sources: `apps/study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md` and `AC_02_STUDENT_LEARNING.drawio`.
- Assets: same-directory `screen.png` (original), `code.html`, `screen_rendered.png` (Firefox headless HTML render; not runtime), `screen_composite.png` (original header/footer plus HTML-rendered body, provenance in marker JSON; not runtime), `ST-02_markers.json`, `ST-02_markers_overlay.svg`, and `screen_annotated.png`.
- API declaration/DD: `docs/lists/list_api.md`; `apps/study-server/docs/dd/04_users_me/` including `OPEN_QUESTIONS.md`.
- Current route/auth/response: `apps/study-server/app/api/v1.py`; `app/modules/guest/api_04_users_me/{view,query,models}.py`; `app/utils/auth.py`; `app/core/security/access_token.py`; `app/core/responses.py`; upstream `app/modules/guest/api_03_auth_login/view.py`.
- Test source read only: `apps/study-server/tests/modules/guest/api_04_users_me/test_users_me.py`.
- Database candidate/status: `infra/postgres/study-server/DB.sql` and `.agents/server-study/database.md`; live schema `NOT_VERIFIED`.
- Context/guide: `.agents/web-work/study/INDEX.md`, `.agents/web-study/design.md`; current app source absent.

#### Kế hoạch kiểm chứng từ source PLAN

### Trích từ DD nguồn: 5. Planned output and acceptance

- Preserve the two original assets and record hashes.
- Add `ST-02_PLAN.md` before rendering/annotation/DD; render and visually inspect `screen_rendered.png` from `code.html`. Keep it as evidence of the HTML-only render; use documented `screen_composite.png` for annotation because the provided screenshot omits the body and the viewport capture omits footer text.
- Add 10 ordered marker records, SVG overlay and `screen_annotated.png`; map 1:1 to DD element rows.
- Add `ST-02.md` with overview, expected/current flow, each element, event inputs/preconditions/sequence/outcomes, #04 response/errors, state/access/navigation, conflicts and references.
- Update global tracker: ST-02 separate statuses, full artifact count 15/83, remaining incomplete count 68, and ST-03 next by the dependency wave in `list_screen.md` §8.1. ST-01 remains in W3 because its dashboard APIs are not wired. Never write GS-08.
- `DD BLOCKED` while the profile-ready design, permission/bio contract and token role/status policy remain unresolved. Keep `IMPLEMENTATION BLOCKED` and `RUNTIME NOT VERIFIED` separate. Do not run tests.

- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
