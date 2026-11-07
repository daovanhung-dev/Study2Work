# Kế hoạch rà soát màn hình — SH-01 Trang giới thiệu Study

> **Trạng thái:** PLAN REVIEWED / STATIC AUDIT PASSED; scope của phiên chỉ SH-01. **Đợt/ưu tiên:** W0 / P0.

## 1. Phạm vi, actor và nguồn

- **Actor / route / AC:** Guest; route `/` là đề xuất; AC-03; API #05 và #06. Screens liên kết theo inventory: GS-01, SH-02, SH-03. F02 còn mô tả GS-02/GS-03 ở luồng khám phá nhưng danh sách next-screen của SH-01 không liệt kê GS-02/GS-03.
- **Mục tiêu:** trang public giới thiệu Study, cho phép mở danh sách khóa học, tìm kiếm, đăng nhập/đăng ký và xem một trang khóa học đã xuất bản. Không thêm API marketing, form thu email, bộ lọc category hoặc dữ liệu không có trong DTO.
- **Inventory/expected:** [SH-01 trong list_screen.md](../../../list_screen.md); [AC-03 index](../../../../../../apps/study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md); [AC-03 activity](../../../../../../apps/study-server/docs/diagrams/AC_UNICA/AC_01_GUEST_ACCOUNT.drawio); [API catalog](../../../../../../docs/lists/list_api.md); [global DD tracker](../../dd_screens/PLAN.md).
- **UI target:** [Study Web design guide](../../../../../../.agents/web-study/design.md) là intended target. `apps/study-client/src/`, `package.json` và `.agents/web-work/study/` không có trong checkout; route/UI runtime chưa được xác minh. Study OpenAPI hiện chỉ là placeholder.
- **UI-only DD skill:** manifest đăng ký `createDD-markdown` cho Web/API DD và loại trừ `web-ui-only-dd`; không có skill canonical cho màn hình UI-only. Không load API DD template cho SH-01.
- **Tài sản hiện hành:** thư mục này là biến thể SH-01 duy nhất trong cây hiện tại; chưa có source variant-2. `screen.png` 559×1600 SHA-256 `777f11eafd87807524c99ac6c21d402519311f3c9ff48f54c0781b543bc0d64f`; `code.html` SHA-256 `d22ed5ee5000b49f6c4b69297b460ed0d2841938b04887f5b3882b8582d3e5b8`. Giữ nguyên hai file.
- **Schema evidence:** current source/API module sử dụng các bảng legacy `categories`, `courses`, `users` với BIGINT candidates trong [DB.sql](../../../../../../infra/postgres/study-server/DB.sql); file này không chứng minh schema live. `02_study_db.sql` là V1-PILOT riêng, không trộn schema/ID của nó với API runtime. Không thấy quan hệ course-category trong legacy DDL.

## 2. Expected behavior và current behavior cần giữ tách biệt

| Hạng mục | Expected theo inventory/AC/API design | Current source hoặc tài sản | Cách ghi trong DD |
|---|---|---|---|
| Entry | Public landing `/`; AC-03 Guest; route liên kết tới GS-01, SH-02, SH-03 | Không có Study Web router/client | `DESIGN_ONLY / ROUTE_UNWIRED`; không tuyên bố route chạy |
| Category #05 | `GET /api/v1/categories`, public, `locale?`, Category page/envelope | Route được đăng ký; default `vi-VN`, match locale chính xác, lấy `ACTIVE` theo `id ASC`; empty trả 200, page `{page:1,size:total,total,total_pages:1}` | `SOURCE_BACKED / TEST_SOURCE_ONLY`; chỉ map ID/name/slug/description |
| Courses #06 | `GET /api/v1/courses`, public, category/page/size/sort theo catalog; Page<Course> | Route được đăng ký; page default 1, size default 20, size 1–100, sort allowlist; chỉ `PUBLISHED`; category bất kỳ nếu được gửi trả 422 trước DB; price là decimal string; mentor projection bắt buộc | Ghi discrepancy catalog category-vs-source; SH-01 gọi page=1,size=6 không category/sort |
| API data | API #05/#06 là thiết kế và backend contract | Module/view/query/models/tests hiện có; tests dùng FakeSession/fake rows, chưa chạy ở phiên này; live DB/deployment không xác minh | Không dùng test source làm bằng chứng runtime production |
| Visual fidelity | Hình ảnh là tham chiếu asset; UI target theo Study design guide | Ảnh có hero/KPI/5 category chips/6 course cards/benefits/testimonials/logos/email/footer; HTML nhỏ hơn, có 4 category labels, 2 mock course cards, login/register links và empty-state sample cùng lúc. 16 href đều là fragment: 5 trỏ tới section IDs có thật, 5 là `#` quay đầu trang, 6 (`#dang-nhap`, `#dang-ky`, `#dieu-khoan`) không có target; không link nào chứng minh router Study. | Ghi discrepancy theo section; không hợp nhất thành một runtime UI đã duyệt |
| Dữ liệu ngoài DTO | Không có contract riêng trong SH-01 cho KPI/review/logo/newsletter | Ảnh/HTML chứa số, rating, duration, lesson counts, discount, category badge, testimonial/logo, email CTA | Ẩn/không gửi/không lưu cho tới khi nguồn và phê duyệt được cung cấp |

## 3. API / data flow cần đặc tả

### API #05 — categories

- `GET /api/v1/categories`; no auth; optional query `locale` (string). Bỏ locale dùng `vi-VN`; nếu có giá trị thì lọc exact-match, không trim/normalize.
- Query chỉ đọc `id,name,slug,description` từ `categories`, `status='ACTIVE'`, `locale=:locale`, `ORDER BY id ASC`.
- 200 `DESIGN_RESOURCE_RETRIEVED`; `data.items[]` + pagination ngầm định `{page:1,size:total,total,total_pages:1}`, kể cả empty `{size:0,total:0,total_pages:1}`. Request type lỗi: 422 `DESIGN_VALIDATION_ERROR`; SQL/mapping failure: 500 `DESIGN_INTERNAL_ERROR`, trace ID; SQL failure rollback.
- Không trả course count, icon, featured flag, localized UI copy hoặc filter relation.

### API #06 — published courses

- `GET /api/v1/courses?page=1&size=6`; no auth/body. `page=1,size=6` là lựa chọn hiển thị của SH-01; API defaults 1/20, size range 1–100. Không gửi `category` hoặc `sort`; default stable order `created_at DESC,id ASC`.
- Catalog #6 khai báo `category?:int64`; current validator từ chối mọi category với 422 `DESIGN_VALIDATION_ERROR` trước DB. Query dùng count query rồi list query, lọc `courses.status='PUBLISHED'`, join mentor projection qua `users`.
- 200 `DESIGN_RESOURCE_RETRIEVED`, data `items[]` + `pagination{page,size,total,total_pages}`. DTO: `id:int`, `title`, `description?`, `thumbnail_url?`, `price:string` dạng decimal, `status`, `mentor{id,full_name,avatar_url?}`. No currency/rating/duration/lesson count/discount/category/popularity field.
- `page<1`, `size<1 || >100`, sort sai hoặc category được truyền: 422 `DESIGN_VALIDATION_ERROR`; empty/out-of-range page: 200 với items rỗng; SQL/mapping/orphan mentor: safe 500 `DESIGN_INTERNAL_ERROR`, SQL/orphan branches rollback. Không biến 500/network thành empty.
- API #05/#06 DD đang `Draft — Needs Confirmation`; current route/source/test là bằng chứng current behavior, không thay approval/live schema.

## 4. Kế hoạch đánh số element và ảnh

Đánh dấu 26 component/element groups nhìn thấy trong `screen.png`; các control/field lặp được liệt kê rõ trong DD và marker map. Marker number 1–26 duy nhất, map tới `SH01-EL-01…26`. Không đánh dấu modal/hover state không có trong asset.

| # | Element ID | Element/component group | Target trong ảnh nguồn (x,y) | Ghi chú |
|---:|---|---|---:|---|
| 1 | `SH01-EL-01` | Header: brand/logo, nav, search summary, utility icons và account/auth area | 278,16 | Screenshot/HTML khác nhau; prototype có section fragments, top fragments và auth fragments không có target; chưa có route Study |
| 2 | `SH01-EL-02` | Hero campaign/scholarship badge | 280,52 | Ngày/số liệu campaign chưa có nguồn |
| 3 | `SH01-EL-03` | Hero title và supporting copy | 278,101 | Nội dung biên tập; cần Product duyệt |
| 4 | `SH01-EL-04` | Hero search input | 260,151 | Không có API từ SH-01; submit chuyển GS-02 |
| 5 | `SH01-EL-05` | Hero search submit button | 399,151 | Không gọi #07 tại SH-01 |
| 6 | `SH01-EL-06` | Hero CTA pair: khám phá / đăng ký lộ trình | 278,184 | Route CTA thứ hai phụ thuộc ý nghĩa câu chữ |
| 7 | `SH01-EL-07` | KPI row (10.000+, 120+, 94%) | 278,235 | Unsupported marketing metrics |
| 8 | `SH01-EL-08` | Category section heading/eyebrow | 170,294 | Static title/copy |
| 9 | `SH01-EL-09` | Category chip row (5 visible labels/counts/icons) | 278,336 | #05 only supplies name/id/slug/description |
| 10 | `SH01-EL-10` | Category carousel previous/next controls | 538,327 | No carousel source/behavior in HTML/API |
| 11 | `SH01-EL-11` | Published-course section title and subtitle | 190,397 | No featured/popularity field |
| 12 | `SH01-EL-12` | Sort/filter/view-all controls | 460,399 | Only “Tất cả” can map GS-01; other sort values unsupported |
| 13 | `SH01-EL-13` | Course-card grid (6 repeated card components) | 278,620 | Card fields listed separately in DD; sample-only metadata excluded |
| 14 | `SH01-EL-14` | Benefits section heading/intro | 278,860 | Editorial content requires approval |
| 15 | `SH01-EL-15` | Benefit cards (3 repeated cards) | 278,957 | No feature API |
| 16 | `SH01-EL-16` | Testimonial section heading and supporting metric | 278,1053 | Metric/testimonials unsupported |
| 17 | `SH01-EL-17` | Testimonial cards (3 repeated cards with rating/profile) | 278,1150 | No testimonial/rating endpoint used by SH-01 |
| 18 | `SH01-EL-18` | Employer/company logo strip (5 labels) | 278,1237 | Logo/affiliation asset and claims need approval |
| 19 | `SH01-EL-19` | Email CTA heading and supporting copy | 278,1364 | No lead/newsletter endpoint |
| 20 | `SH01-EL-20` | Email input | 165,1424 | Do not collect/store/log |
| 21 | `SH01-EL-21` | Email submit action | 306,1424 | Keep disabled/hidden absent approved API |
| 22 | `SH01-EL-22` | Trust/privacy/reassurance labels below form | 280,1454 | Claims need policy/source approval |
| 23 | `SH01-EL-23` | Footer brand and service description | 115,1530 | Static brand copy |
| 24 | `SH01-EL-24` | Footer navigation columns (Learning, Study2Work, Support/Legal) | 385,1534 | Links are not functional routes by themselves |
| 25 | `SH01-EL-25` | Accreditation/certification badges | 155,1566 | No source/credential evidence |
| 26 | `SH01-EL-26` | Copyright and platform tagline | 280,1590 | Copyright year/content need owner confirmation |

**Annotation layout:** center the source screenshot unchanged on a white canvas with 28 source-pixel equivalent gutter each side; render at 2×; place blue/white numbered badges and short gutter connector lines. Store original-image target coordinates and output badge side/center in `SH-01_markers.json`. This keeps badges off text and card content while retaining the source aspect inside the annotation canvas.

## 5. Event plan

| Event ID | Element(s) | Trigger / input | Processing and result |
|---|---|---|---|
| `SH01-EV-01` | #1–#3 | Entry to proposed `/` | Render only approved static copy; request #05 and #06 independently in parallel after client/router exists. No UI runtime currently. |
| `SH01-EV-02` | #05 | Hero search submit; q string | Trim leading/trailing whitespace; if empty, stay on SH-01/no request; otherwise URL-encode q and navigate to GS-02 proposal. SH-01 does not call #07. |
| `SH01-EV-03` | #1 header search (screenshot-only control) | q string, if retained after design choice | Same target GS-02 only after Product confirms it is a real input. Not present as an input in `code.html`; no runtime handler. |
| `SH01-EV-04` | #2/#6 | Click explore CTA | Navigate to proposed GS-01 `/courses`; no API side effect at SH-01. |
| `SH01-EV-05` | #1/#6 | Click login/register CTA | Navigate to SH-02/SH-03 only when target/CTA meaning is approved; no auth API call here. |
| `SH01-EV-06` | #07 | #05 response | Validate envelope/model; render name only; empty is 200; failure/422/500 is local to category region; no category count or icon synthesis. |
| `SH01-EV-07` | #13 | #06 response | Validate envelope and DTO; render up to requested six items in server order; optional description/thumbnail/avatar may be absent/null; do not add currency or unsupported fields. |
| `SH01-EV-08` | #09 | Select category chip | Keep informational/disabled: no #06 call while category relation/filter is unsupported; do not derive category ID from slug. |
| `SH01-EV-09` | #10/#12 | Click carousel/sort/filter | No current handler/contract. “Tất cả” may route to GS-01; other controls remain disabled/hidden pending decision. |
| `SH01-EV-10` | #13 | Click course card/detail | F02 target GS-03 with returned course ID conflicts with SH-01 next-screen list; current #08 route/module/test source exists while the catalog still labels it D. Keep card non-navigating or route only after Product approves. |
| `SH01-EV-11` | #07/#13 | Retry in one failed data region | Repeat only the corresponding public GET with unchanged validated params; do not retry validation errors automatically or blank the successful other region. |
| `SH01-EV-12` | #20/#21 | Enter/submit email | No endpoint/consent/retention contract. Do not send, store or log value; hide or disable the complete lead-capture form. |
| `SH01-EV-13` | #1/#24 | Click header/footer link | Use only a route confirmed by the cross-screen inventory and future Study router. `#khoa-hoc` / `#tim-kiem` are in-page anchors in the HTML; bare `#` returns to the top; `#dang-nhap`, `#dang-ky` and `#dieu-khoan` have no matching target. None establishes an app route. |
| `SH01-EV-14` | #23/#25/#26 | Footer static content | No API. Keep only approved brand/legal/certification claims; do not present unverified accreditation as fact. |

## 6. States, blockers and review gates

- **Static/design state:** current `screen.png` and `code.html` do not have a shared runtime state or API binding. HTML shows hard-coded examples and an empty-state block simultaneously. Do not equate this with current application behavior.
- **Future independently loaded regions:** categories `INITIAL → LOADING → READY/EMPTY/ERROR`; courses `INITIAL → LOADING → READY/EMPTY/ERROR`. A failure in one region must not erase a success in the other. 401/403 from public GET is unexpected; 422/500/network remain errors and must not become empty success.
- **Navigation/input:** blank search does not request; nonblank search transfers trimmed/encoded q to GS-02; auth/catalog routes remain proposals; invalid/unknown destinations are not fabricated.
- **Blockers:** (1) Study Web source/router absent; (2) no decision selecting screenshot versus HTML as authoritative; (3) API #06 contract lists category while current source rejects it and no legacy course-category relation exists; (4) direct course-card target GS-03/#08 conflicts with SH-01 next-screen list; (5) KPI, ratings, price currency, durations, testimonials, logos, certification and email collection lack source/approval; (6) variant-2 not found; (7) API DD approval and live DB/schema/deployment are not verified; (8) image/design guide drift needs frontend implementation decision.

## 7. Static acceptance checklist

- [x] This revised plan precedes marker map, annotation and DD update.
- [x] 26 unique ordered markers map one-to-one to 26 DD Element IDs and describe every visible component group.
- [x] Annotated image retains original screenshot content/aspect within the annotation canvas; badges do not cover text or controls.
- [x] PNG/HTML source hashes are unchanged; only current `variant-1` is documented.
- [x] API #05/#06 current route, source, test source, catalog and DDL evidence are cross-linked; unsupported category/marketing data are explicit blockers.
- [x] DD includes API request/response/error mapping, 14 event paths, states, navigation, privacy, accessibility and design drift.
- [x] Thêm bảng đối chiếu tường minh các yêu cầu A–F của objective với section tương ứng trong DD để dễ nghiệm thu.
- [x] Relative Markdown links, marker numbering, image dimensions/hash and whitespace audit pass.
- [x] Tracker/worklog updated; status distinguishes `DD READY`/`DD BLOCKED`, `IMPLEMENTATION BLOCKED` and `RUNTIME NOT VERIFIED`.

## 8. Session result

- Result: SH-01 DD, 26-marker annotation and source trace completed; static artifact audit passed.
- DD / implementation / runtime status: DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED.
- Next Screen ID: SH-02 in a separate session, following W0 order. No other Screen ID is in scope here.

## 9. Kế hoạch rà soát bổ sung (2026-11-07)

- **Scope:** chỉ re-audit SH-01 trong worktree hiện tại; không đổi contract, backend source, UI behavior hoặc assets gốc.
- **Đối chiếu:** kiểm tra lại inventory/AC-03, API #05/#06 route-module-query-model-test source, DDL candidate, Study Web source status, 26 marker↔element IDs, 14 event descriptions, fragment-link targets, source hashes và kích thước PNG.
- **Cải thiện dự kiến:** thêm bảng cross-reference A–F vào DD để chứng minh các deliverable của objective được đặt ở đâu; không thêm nghiệp vụ mới.
- **Gate:** giữ nguyên các discrepancy/blocker và ba trạng thái `DD BLOCKED`, `IMPLEMENTATION BLOCKED`, `RUNTIME NOT VERIFIED`; sau chỉnh sửa chạy lại static artifact/link/whitespace audit và `git diff --check` theo phạm vi.
- **Finding từ HTML:** có 16 fragment href, trong đó chỉ 5 trỏ tới section ID có thật; 5 `#` quay lên đầu trang và 6 auth/legal fragment không resolve. DD phải mô tả đúng các nhóm này, không gọi toàn bộ là `href="#"`.
- **Finding từ event audit:** EV-06/07 đã nêu mapping và nhánh rỗng trong phần xử lý nhưng chưa tách output/result thành trường dễ nghiệm thu; cần thêm kết quả thành công/rỗng riêng cho từng vùng. Dọn whitespace ở metadata DD để static check sạch.

### Kết quả re-audit

- Current API/source trace giữ nguyên: #05/#06 public routes, #06 category filter trả 422; DDL legacy không có course-category relation; Study Web source/router/package manifest không có trong checkout.
- Đã thêm cross-reference A–F trong DD §1.3; EV-06/07 có kết quả thành công/rỗng tách riêng; mô tả prototype fragment được sửa theo đúng target hiện có; metadata whitespace đã dọn.
- Static audit đạt: 26 marker tuần tự/duy nhất khớp 26 element rows và SVG labels; target nằm trong ảnh nguồn; 14 event tuần tự có trigger/điều kiện, input, process, result/output và exception/error; JSON/SVG parse; local Markdown links resolve; 16 fragment links được phân loại 5 section-target, 5 bare `#`, 6 unresolved.
- `screen.png` 559×1600 và `screen_annotated.png` 1230×3200; ảnh chú thích được xem trực tiếp; source `screen.png`/`code.html` hashes không đổi; authored whitespace scan và scoped `git diff --check` sạch.
- Không chạy application tests, Study Web runtime hay live DB. Status vẫn `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`. Screen tiếp theo W0 là SH-02 trong phiên riêng.
