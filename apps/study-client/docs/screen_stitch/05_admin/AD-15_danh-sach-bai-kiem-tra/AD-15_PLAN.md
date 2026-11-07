# AD-15 PLAN — Danh sách bài kiểm tra

## 1. Phạm vi phiên

- Hoàn thiện **chỉ AD-15** theo inventory row 73, AC-35 và goal objective; dừng trước AD-16.
- Tạo screen DD A–F, marker JSON/SVG, `screen_annotated.png`, cập nhật inventory/API reverse index, global plan và worklog.
- Giữ nguyên `screen.png` và `code.html`; không sửa Study Web hay Study Server. API #87 source được mô tả như hiện trạng, không đổi API DD.
- UI-only DD không có skill canonical trong registry; `createDD-markdown` áp dụng cho Web/API DD và loại trừ `web-ui-only-dd`.

## 2. Expected behavior và luồng AC-35

- Inventory đề xuất route `/admin/quizzes`, actor Admin, AC-35, GET #87; các nhánh tới AD-16 (create/update), AD-18 (delete) và AD-17 (statistics).
- AC-35 nêu Admin có `quiz management permission`; postcondition là quiz được tạo/cập nhật/xóa hoặc có thể xem statistics. Diagram: mở màn hình → GET #87 → query quizzes → chọn Create (#88), Update (#89), Delete (#90) hoặc Statistics (#91) → hiển thị kết quả. Đây là expected flow; route/UI wiring chưa được chứng minh.
- Direct catalog #87: `GET /api/v1/admin/quizzes`, Bearer JWT / role Admin, không body, query `course?:int64`, `status?:string`, `page?:int32`, direct `ApiEnvelope<Quiz>`, 200/401/403/500. API #87 DD còn `Draft — Needs Confirmation`.

## 3. Current source, asset và discrepancy cần giữ rõ

- Folder hiện có `screen.png` (1600×1394; SHA-256 `a58cc4433342fe13441b337f2ca287a8b6fde354180ff73ff488f9d8d235401a`) và `code.html` (20,852 bytes; SHA-256 `d8b6e43ee2e9832bb5bbfd13ae6a7bd802877ecc2207ad3fb43db6ced7878473`). HTML là prototype tĩnh; giữ nguyên cả hai file.
- Study Web có `docs/`, `dist/index.html`, `node_modules/` và build metadata nhưng không có editable source, package manifest, router hoặc API client. `dist` không cho thấy `/admin/quizzes`/API #87. Trạng thái UI `UNWIRED`; không xác nhận route hay runtime.
- API #87 route/module/query/model/test source được compose cục bộ. Shared `ADMIN` auth chạy trước query parse/DB; AC-35 permission riêng chưa có policy. Local query đếm và đọc page với cùng exact optional filters `course`/`status`, loại `DELETED`, page mặc định 1, size cố định 20, `id ASC`; local response `ApiEnvelope<Page<Quiz>>` có `items`, `pagination`, metadata-only `questions=[]`. Các fallback này là DERIVED; catalog trực tiếp vẫn là `ApiEnvelope<Quiz>`. Invalid `course`/`page` trả local 422 ngoài catalog; query/mapping lỗi 500 + rollback; list rỗng hoặc page vượt total trả 200; GET không commit.
- Local Quiz projection chỉ có `id`, `course_id`, `title`, nullable `duration_minutes`, `passing_score`, `questions=[]`. Ảnh yêu cầu thêm mã bài thi/code, tên khóa, số câu hỏi và status; #87 không trả các trường đó. Không dùng `len(questions)` để hiện số câu hỏi vì danh sách luôn chưa hydrate.
- Prototype search theo tên/mã đề không được #87 hỗ trợ; course option dùng slug trong khi query `course` là int64; status options `draft/active/closed` không có enum/normalization mapping (server so khớp raw text). Toolbar refresh và empty-state refresh chỉ xoay icon 800 ms, không tải dữ liệu; advanced filter, create và pagination đang disabled. Nội dung “chưa đồng bộ”, scoring engine `Sẵn sàng`, security V3 và RBAC/system badges đều là static copy.
- Legacy `quizzes` BIGINT DDL là candidate, cho phép `course_id`/`passing_score` nullable; V1-PILOT dùng UUID `assessments`/versioned quiz tables. DDL và fake DB tests không xác nhận live schema/deployment. Screenshot dùng full-width/cobalt/Plus Jakarta-style; `.agents/web-study/design.md` là target ocean-blue, Inter/system, centered/responsive.

## 4. Events cần mô tả trong DD

| Event | Trigger | Boundary cần ghi |
|---|---|---|
| EV-01 Open/load list | Vào `/admin/quizzes` | Candidate GET #87; auth; query/body; source Page vs catalog Quiz; loading/ready/empty/auth/error; không claim client wiring. |
| EV-02 Search | Nhập tên/mã đề | HTML không gắn listener; #87 không có search/code query; không tự thêm param/API. |
| EV-03 Select course | Đổi course filter | Option slug không map được sang `course:int64`; chỉ gọi #87 khi mapping/option source được duyệt. |
| EV-04 Select status | Đổi status filter | Giữ discrepancy `draft/active/closed` vs exact raw backend status; enum/casing cần owner chốt. |
| EV-05 Refresh | Toolbar hoặc empty-state button | Current chỉ animation 800 ms; candidate GET #87 nếu được wire; retry/dedup/cache policy chưa có. |
| EV-06 Advanced filters | Click disabled button | Hiện disabled, không event handler; không phát sinh query #87 chưa khai báo. |
| EV-07 Create | CTA `Tạo bài kiểm tra mới` | Hiện disabled; expected handoff AD-16; #88 thuộc screen khác, không gọi từ AD-15 khi route chưa duyệt. |
| EV-08 Pagination | Previous/next | Current disabled/0-of-0; local #87 nhận page 1-based, size 20; cách cập nhật query/URL và page reset cần chốt. |
| EV-09 Update | Chọn action trên quiz row | Row actions không hiện ở empty screenshot; AC-35 #89 → AD-16, numeric quiz ID là candidate; body/route policy chưa thuộc AD-15. |
| EV-10 Delete | Chọn action trên quiz row | AC-35 #90 → AD-18; list row action và confirmation thuộc design liên quan; không suy diễn từ table header. |
| EV-11 Statistics | Chọn action trên quiz row | AC-35 #91 → AD-17; local response #91 khác catalog, nên chỉ ghi handoff/contract blocker. |
| EV-12 Admin shell/navigation | Nav, notification, breadcrumbs, footer | Anchors `#`/static controls; không có route, profile, health, RBAC, support handler. |

## 5. Marker plan

Tạo 50 marker theo thứ tự thị giác, tọa độ pixel trên ảnh gốc 1600×1394; mỗi marker khớp duy nhất một dòng §C:

| Range | Nhóm | Số lượng |
|---|---|---:|
| #1 | Brand block | 1 |
| #2–#6 | Năm Admin navigation links | 5 |
| #7–#9 | System badge, notification, Admin identity | 3 |
| #10–#13 | Global breadcrumbs và RBAC copy | 4 |
| #14–#16 | Breadcrumb cục bộ và trạng thái scoring-engine tĩnh | 3 |
| #17–#21 | Badge, Screen ID, title, subtitle, Create CTA | 5 |
| #22–#26 | Search, course/status filters, refresh, advanced filter | 5 |
| #27–#33 | Bảy table column headers | 7 |
| #34–#37 | Empty-state icon, heading, copy, refresh | 4 |
| #38–#41 | Result summary, page indicator, previous/next | 4 |
| #42–#45 | Policy icon, heading, copy, security V3 badge | 4 |
| #46–#50 | Footer copyright, descriptor và ba links | 5 |

Gộp icon trang trí vào control tương ứng; không đánh số nền/card/separator không mang nghĩa độc lập. Đặt marker trong gutter/whitespace, tránh che label; render 2× và xem ảnh cuối.

## 6. Blocker register

- Response cardinality `ApiEnvelope<Quiz>` vs local `ApiEnvelope<Page<Quiz>>`.
- Required table fields không có trong #87; không fabricate Quiz code, course title, question count hoặc status.
- Search by name/code không có query contract; course slug cần nguồn ID; status enum/casing không được xác nhận.
- AC-35 quiz-management permission vs shared `ADMIN`; legacy BIGINT vs V1-PILOT UUID/live schema; required projection có thể gặp nullable DDL values.
- No Study Web source/router/client; disabled/static controls, unsupported refresh/empty-sync/system/security claims và screenshot/design-target discrepancy.
- Local page/error/tombstone behavior khác direct API catalog và chưa được owner duyệt.

## 7. Work order và checklist

1. [x] Đọc objective/router/context/worklog preflight; docs selector READY 3/220; đọc AD-01/02/03 và handoff AD-14.
2. [x] Đọc registry/scopes, AC-35, inventory, API catalog/#87 Draft DD, server route/module/query/model/test/DDL, Study Web assets/tree và design target.
3. [x] Lưu plan này trước marker JSON/SVG, annotated image hoặc AD-15 DD.
4. [x] Tạo 50 JSON/SVG marker; render PNG 3200×2788; kiểm tra order/coords/bounds/overlap/1:1 mapping và xem trực tiếp.
5. [x] Viết DD A–F với 50 §C rows, EV-01…EV-12, API/error/state/navigation và blocker/source trace.
6. [x] Cập nhật inventory/API #087 reverse index, global AD-15 checkpoint/core artifact count và worklog; giữ API #87 DD Draft.
7. [x] Audit source hashes, dimensions, JSON/XML, links, 83 folders/IDs, core artifact count, whitespace và `git diff --check`; không chạy application tests/runtime.
8. [x] Chốt AD-15 only; trạng thái màn hình `DD BLOCKED`, `IMPLEMENTATION BLOCKED`, `RUNTIME NOT VERIFIED`; dừng trước AD-16.
