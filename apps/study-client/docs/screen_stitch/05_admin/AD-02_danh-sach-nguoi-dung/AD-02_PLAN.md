# AD-02 — Kế hoạch Detailed Design

**Trạng thái:** `COMPLETED WITH BLOCKERS` — kế hoạch được viết trước marker, ảnh chú thích và DD; blocker còn lại được ghi tại §5 và trong DD.
**Phạm vi phiên:** chỉ Screen ID `AD-02`.

## 1. Mục tiêu và ranh giới

- Hoàn thiện kế hoạch, marker map, ảnh `screen_annotated.png` và DD A–F cho `/admin/users`, dựa trên inventory row 60, AC-31, catalog/API DD #68, PNG/HTML gốc, Study Web design guide và Study Server source/test hiện hành.
- Tách expected behavior khỏi current behavior. Không coi placeholder, filter copy, security notice, API/RBAC badge, empty-state sync message, Add hoặc Export trong mockup là hành vi runtime.
- Truy vết handoff theo AC-31 từ #68 list tới #69 detail và các nhánh #70 update, #71 status, #72 delete; chỉ author DD cho AD-02.
- Bảo toàn `screen.png` và `code.html`; ảnh chú thích chỉ render từ ảnh gốc.

## 2. Bằng chứng đã kiểm tra

### Expected behavior

- Inventory row 60: AD-02 “Danh sách người dùng”, route đề xuất `/admin/users`, AC-31, API #68; bảng có keyword/status/role/pagination/hành động Admin; giữ filter trong query URL; links AD-03/AD-04; states `loading/empty/ready/filter-error`; P1.
- AC-31: Actor Admin; precondition Admin đăng nhập và có quyền user management; mở danh sách → #68 truy vấn users + pagination → chọn user → #69 detail → nhánh #70 update, #71 status, hoặc #72 delete → reload list/detail. AC-31 và catalog khai báo #68 trả `ApiEnvelope<Page<UserProfile>>`, query `role`, `status`, `keyword`, `page`, và lỗi 401/403/422/500.
- API #68 DD hiện `Draft — Needs Confirmation`. Page default/size/order, literal keyword normalization, role/status exact-match values, permission mapping, PII/audit policy, lifecycle visibility và live schema còn DERIVED/open.

### Current behavior

- `screen.png` 1600×1425 RGB, SHA-256 `444e6530086a14607ff097d39a5133c55e6f637146a09ee9ebc8c0e61d61a6e0`; `code.html` SHA-256 `af8433bd009b3e7e2309631b17841488746a26d62edca6420d5d98782f89a57d`.
- Prototype dùng keyword copy có “mã người dùng”, option role `student/instructor/admin`, status `active/locked/pending`; API #68 chỉ tìm `full_name/email`, exact-match string role/status và chưa có danh sách enum được duyệt. Không tự map `instructor→MENTOR` hoặc `locked→SUSPENDED`.
- HTML có 8 anchor `href="#"`, không form/fetch/XHR/client route. Reset chỉ clear keyword/role/status và focus search. Refresh và pagination disabled; Add, Export, guide không có handler. Prototype empty-state nói chờ đồng bộ từ auth server; API #68 không trả sync state. Footer/security copy khẳng định access được audit nhưng API #68 không cung cấp audit data.
- Study Web hiện chỉ có docs/assets, ignored `dist/` và `node_modules/`; editable source, package manifest và `/admin/users` route absent. Status `UNWIRED`; serving/deployment chưa xác minh.
- Current API #68 route/module/test source tồn tại; shared `ADMIN` JWT guard chạy trước query; list read-only trên legacy BIGINT `users` candidate, không chọn password hash, trả safe `Page<UserProfile>`, page size 20/order `id ASC`; tests dùng fake DB rows. Live schema/deploy và user-management permission policy chưa xác minh.
- Prototype palette/typeface khác Study Web guide (ocean-blue semantic tokens; Inter nếu có, nếu không system sans-serif). Ghi nhận discrepancy, không đổi canonical tokens.

## 3. Kế hoạch sự kiện

| Event dự kiến | Element | Expected flow | Current prototype |
|---|---|---|---|
| EV-01 — Mở danh sách | Route/page | Admin permission đã được xác nhận; đọc `role/status/keyword/page` từ URL theo inventory; gọi #68; map Page<UserProfile>. | Không có Study Web route/client. |
| EV-02 — Tìm kiếm | Search input | Gửi keyword; backend chỉ match substring literal trên tên/email; giữ query URL. ID search chưa được #68 hỗ trợ. Debounce/submit policy còn mở. | Input chưa gửi request; copy nói có tìm user ID. |
| EV-03 — Lọc role/status | Hai select | Gửi string exact-match theo enum được owner duyệt; page/filter URL policy cần chốt. | Select value lowercase không khớp semantics được phê duyệt; không có listener/request. |
| EV-04 — Đặt lại | Reset | Xóa filter và cập nhật URL/refetch #68 theo policy đã chốt. | Local handler chỉ xóa ba control và focus search; URL/query không đổi. |
| EV-05 — Phân trang | Prev/current/next | Dùng `page`; size cố định 20; render `total/total_pages`. Empty Page là 200 với `page=1,total_pages=0`; hiển thị `0/0` trong mockup cần thống nhất. | Nút pagination disabled, không có dữ liệu/page state. |
| EV-06 — Mở user / chỉnh sửa | Row action | Dùng `id` → AD-03/#69; vào AD-04/#70 theo quyền và contract. AD-05/#71/#72 là nhánh riêng, không mutation trong #68. | Không có row/action implementation vì mockup chỉ empty state. |
| EV-07 — Thêm người dùng | Add button | Chưa có create-user API/AC-31 endpoint; yêu cầu owner quyết định đích/feature trước khi enable. | Button tĩnh, không handler. |
| EV-08 — Export | Export button | Chưa có user-list export contract/API; không tải giả hoặc đổi sang report API khác. | Button tĩnh, không handler. |
| EV-09 — Refresh / help | Refresh và guide | Refresh refetch #68; guide destination cần xác định. | Refresh disabled; guide không có handler. |
| EV-10 — Navigation/profile/security notice | Header, badge, notification, footer | Mở route/destination chỉ khi inventory/contract có đích; không xác nhận health/RBAC/audit bằng static copy. | Navigation/footer đều `href="#"`; notification không có handler; claims là static. |

## 4. Kế hoạch marker và DD

- Tạo 38 element rows theo thứ tự đọc: brand; primary nav group/status/profile; global/local breadcrumbs và badges; page heading/actions; filters/sync summary; table header; empty state/help/pagination; security notice; footer.
- Mỗi marker đại diện một component/control; năm primary nav anchors được gom trong một group row; icon/label cùng một control ghi chung trong row. Các cột của table header là một vùng semantic; trạng thái từng filter và pagination được ghi riêng. Marker không che text/control.
- Tạo `AD-02_markers.json`, `AD-02_markers.svg` và render `screen_annotated.png` ở 2× (3200×2850), marker `1..38` theo tọa độ ảnh gốc 1600×1425.
- DD A–F: overview + expected/current; AC-31/API flow; 38 element rows; event/API/error mapping; states/navigation; acceptance checklist và blocker.
- Chỉ ghi API fields/actions được catalog/AC/source hỗ trợ. Không thêm `size/sort`, search-by-ID, enum mapping, create/export/audit/sync endpoint hoặc mutation vào #68.

## 5. Blocker cần giữ rõ

1. API #68 claim `ADMIN` được dùng làm fallback cho user-management permission; owner chưa duyệt permission/tenant policy.
2. Prototype `student/instructor/admin` và `active/locked/pending` không được API #68 whitelist; giá trị role/status và mapping chưa chốt.
3. Keyword copy có user ID nhưng backend chỉ tìm full_name/email.
4. Email/phone là PII trong response; audit/visibility policy và lifecycle (suspended/deleted/anonymized) chưa chốt.
5. Add user, export, guide, audit và server-sync claims không có mapping trong #68/AC-31; không enable khi chưa có contract/route.
6. Legacy BIGINT `users` là local query candidate; live schema/deployment chưa xác minh.
7. Study Web route/runtime chưa có; prototype behavior không được wire.
8. Screenshot dùng palette/typeface khác canonical Study Web guide.

## 6. Thứ tự thực hiện và kiểm chứng

1. [x] Reread goal objective/router/context/worklog instructions; run exact-type docs selector and review all three selected worklogs.
2. [x] Compare inventory, AC-31, API #68 catalog/DD, current route/module/query/model/auth/database/test source, Study Web tree and source assets.
3. [x] Write this plan before creating any AD-02 marker, annotation, or DD artifact.
4. [x] Create marker JSON/SVG and 2× annotation; inspect dimensions, IDs, bounds and visual placement.
5. [x] Author `AD-02.md` A–F with one row per marker, source-backed events/response/errors, state and handoff map, open decisions.
6. [x] Update AD-02 inventory/API #68 runtime-source status and `dd_screens/PLAN.md`; preserve unrelated worktree changes.
7. [x] Check original asset hashes, marker/DD 1:1, JSON/XML/local links, 83-screen inventory count and `git diff --check`; do not run application tests/runtime.

## 7. Tiêu chí kết thúc phiên

- `screen.png` and `code.html` hashes unchanged; original plus annotated PNG present.
- 38 ordered unique markers are in bounds and match exactly 38 DD element rows.
- DD has A–F, source trace, events, API/error mapping, states/navigation, and unresolved decisions clearly separated from approved behavior.
- Inventory/tracker/worklog agree on `R` for source-backed API #68 while screen result remains `DD BLOCKED`, `IMPLEMENTATION BLOCKED`, `RUNTIME NOT VERIFIED` where blockers remain.
- This session handles only AD-02; no other Screen ID is started.

## Kết quả phiên

- Plan, A–F DD, 38 marker JSON/SVG and 2× annotated PNG are complete; original `screen.png` and `code.html` hashes are unchanged.
- Static audit: 38 ordered/unique/in-bounds markers match 38 DD rows; JSON/XML and local links are valid; image and tracker checks pass; 55/83 screen folders have the four core artifacts.
- API #68 source classification updated `D→R`; DD remains `BLOCKED`, implementation `BLOCKED`, runtime `NOT VERIFIED` pending policy/schema and Study Web decisions.
- Application tests/runtime were not run. This session covers only AD-02.
