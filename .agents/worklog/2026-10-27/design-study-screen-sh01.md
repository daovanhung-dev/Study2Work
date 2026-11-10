---
task_id: "2026-10-27-design-study-screen-sh01"
date: "2026-10-27"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["Study Web SH-01 -> Study API #05 categories and #06 courses"]
status: "VERIFIED"
---

# Worklog: Thiết kế Study Web screen SH-01

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-27/study-web-design-guide.md`
    - carry_forward: Theo ocean-blue design tokens; đây là intended target, không phải current runtime. Study client source từng vắng trong checkout; mọi UI route vẫn là proposed nếu source chưa wire.
  - path: `.agents/worklog/2026-10-25/load-study-server-context.md`
    - carry_forward: Không xem test lịch sử hoặc DDL là bằng chứng live DB/deployment; task Study server phải kiểm tra source hiện tại.
  - path: `.agents/worklog/2026-10-24/commit-push-study-dd.md`
    - carry_forward: Kết quả Git delivery cũ không xác định trạng thái hiện tại; chỉ sửa artifact trong scope đã chốt.
- shortage: `none` (132 worklog docs khả dụng; đã đọc đủ 3 được chọn)

## EXPECTED_BEHAVIOR

- Requirement: Thiết kế đúng một screen trong phiên này; theo inventory, screen đầu là SH-01 Trang giới thiệu Study. Tạo plan, ảnh có marker đánh số từng element, và Markdown bảng đặc tả từng element trong `apps/study-client/docs/dd_screens/resource/SH-01/`. Nếu có screen con thật thì đặt trong subfolder cùng screen.
- Canonical contract/approved DD: `.agents/web-study/design.md` là intended visual target; `apps/study-client/docs/dd_screens/list_screen.md` là inventory/design baseline, chưa phải implementation confirmation. Source API #05/#06 hiện hành quyết định field/response evidence.

## CURRENT_BEHAVIOR

- Source/config: Worktree bắt đầu sạch. `apps/study-client/` hiện chỉ có `docs/dd_screens/list_screen.md`; không có FE source/router, nên SH-01 và các route liên kết là design target. API #05 là public `GET /api/v1/categories`, locale mặc định `vi-VN`, exact locale, chỉ ACTIVE, fields `id/name/slug/description`. API #06 là public `GET /api/v1/courses`, page 1/size 20 mặc định (size 1..100), sort allowlist; query chỉ PUBLISHED và trả `id/title/description?/thumbnail_url?/price(decimal string)/status/mentor{id/full_name/avatar_url?}`. API #06 loại `category` bằng 422; course response không có `category`, còn source không định nghĩa đơn vị tiền tệ.
- Runnable tests: Không chạy. Đã đọc test source #05/#06; chúng dùng FakeSession/fake rows, bao phủ envelope/mapping/empty/error/category rejection nhưng không xác minh PostgreSQL, live DB hay deployment.
- Runtime wiring: Route source #05/#06 được đăng ký trong `app/api/v1.py` và delegate vào view. Live DB/schema/deployment chưa xác minh. API DD #05/#06 còn `Draft — Needs Confirmation`; current source được ưu tiên khi có khác biệt.

## SOURCE_TRACE

```text
SH-01 / -> categories #05 + courses #06 -> display published course cards -> GS-01/GS-02 or SH-02/SH-03
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Study Web current implementation | `find apps/study-client -maxdepth 4 -type f` chỉ có `docs/dd_screens/list_screen.md`. | `SOURCE_REQUIRED` | Artifact được đánh dấu design target; không tuyên bố UI đã wired. |
| Categories filter/relation | API #06 validator trả 422 khi `category` được gửi; `Course` model không có `category`, DDL relation chưa source-backed. | `CURRENT_SOURCE / DISCREPANCY` | Category chỉ trình bày metadata; không thiết kế filter theo category hoặc quan hệ course-category. |
| Course price unit and ratings | #06 price là decimal string, không có currency field; course model không có rating. | `SOURCE_REQUIRED` | Không đưa currency, rating hoặc review count vào card. |

## CHANGES

- Files changed: `apps/study-client/docs/dd_screens/resource/SH-01/` gồm `PLAN.md`, `SCREEN.md`, hai PNG 1440×1320, SVG, build.py, ZIP V4 (superseded) và ZIP V5 (latest); worklog này.
- CONTEXT_UPDATES: Không đổi architecture/route; không sửa context page.
- Context pages changed: None.
- Assumptions: `SH-01` là screen đầu tiên theo STT global 01; một lượt chỉ hoàn tất screen này, không design các screen liên kết. Các category/course/mentor trên ảnh là VISUAL_SAMPLE.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `git status --short --branch` | `develop...origin/develop`, worktree sạch trước khi bắt đầu. | VERIFIED |
| `deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3` | Chọn và đọc đủ 3 worklog docs cùng loại trong 132 log khả dụng. | VERIFIED |
| `.agents/web-study/design.md`, `apps/study-client/docs/dd_screens/list_screen.md`, scope/manifest context | Đã đọc; inventory có 83 surfaces, SH-01 là STT 01, AC-03, route `/`, links GS-01/SH-02/SH-03, states loading/empty/error; global journey F02 mô tả tiếp tục tới GS-02/GS-03. | VERIFIED_STATIC_ONLY |
| `.agents/project/INDEX.md`, `architecture.md`, `dependencies.md`, `contracts.md` | Đã đọc boundary Study Web → Study API; Study OpenAPI là placeholder. | VERIFIED_STATIC_ONLY |
| API #05/#06 source, route declarations, API DD and test source | Đã đọc models/validate/query/view/shared mapping, route declarations, API DD #05/#06 and focused test source; tests not executed. | VERIFIED_STATIC_ONLY |
| `python3` zipfile extract + archive inspection (V4) | ZIP có đúng 5 file; không có đường dẫn archive bất thường. Hai PNG là 1440×1320; SCREEN.md có 41 row, 41 ID duy nhất; marker list trong build.py có 41 tọa độ duy nhất. | VERIFIED_STATIC_ONLY |
| `sha256sum` trên V3/V4 clean PNG, SVG và SCREEN.md | Ba SHA-256 khớp hoàn toàn; V4 chỉ đổi vị trí badge trong ảnh annotated và tên ZIP/source output. | VERIFIED_STATIC_ONLY |
| Visual review qua `view_image` (clean và annotated V4) | Đã rà toàn màn hình; hero H1 48px, artwork course khác nhau; 41 badge nhìn rõ, card gutter 24px, không còn badge đè text/avatar/logo. #12 chỉ kính lúp; các badge card nằm đúng khe. | VERIFIED_VISUAL |
| V5 archive/source/Markdown inspection | ZIP tải từ ChatGPT có đúng 5 file; `testzip()` trả `None`; clean/annotated đều PNG 1440×1320. SCREEN.md có đúng 41 row với ID liên tục 1–41; build.py AST hợp lệ. Chỉ thay category capsules bằng static labels và đổi vị trí marker #18; bảng/spec đi cùng. | VERIFIED_STATIC_ONLY |
| Visual review qua `view_image` (clean và annotated V5) | Cả hai ảnh 1440×1320 đã được xem ở độ phân giải gốc. Nhãn taxonomy có accent mảnh, không còn hình dáng nút; marker #17/#18 đứng ngoài chữ. 41 badge hiện đủ, card artwork/title/description/avatar/mentor name không bị che; course cards vẫn đọc là nội dung tĩnh. | VERIFIED_VISUAL |
| Diff V4 → V5 | SVG/source chỉ đổi hai label tĩnh; SCREEN.md đồng bộ tọa độ/semantics/state/responsive và category loading; không đổi hero, course art, card geometry, copy hoặc API logic. | VERIFIED_STATIC_ONLY |
| Kiểm tra local `build.py` | Không chạy vì môi trường thiếu module `PIL` (ModuleNotFoundError); artifact PNG được lấy từ ZIP V5 và xác minh độc lập. | DECLARED_NOT_RUNNABLE |

## HANDOFF

- Remaining blockers: Không còn blocker cho gói design SH-01 V5. Giới hạn: chỉ xuất ảnh desktop 1440×1320; tablet/mobile có rule trong SCREEN.md nhưng chưa có ảnh render. Study Web runtime/router vẫn không có trong checkout nên đây không phải bằng chứng implementation.
- Next owner/action: Tiếp tục screen SH-02 ở một phiên riêng theo yêu cầu one-screen-per-session; thực hiện context preflight của phiên đó trước khi thiết kế.
