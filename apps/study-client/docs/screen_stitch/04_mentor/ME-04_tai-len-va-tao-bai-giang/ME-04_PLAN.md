# ME-04 — Kế hoạch Detailed Design: Tải lên và tạo bài giảng

> **Plan status:** COMPLETE — lập trước marker map, ảnh chú thích và DD lúc `2026-11-06T19:54:00+07:00`.
> **Screen status dự kiến sau audit:** `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`.

## 1. Phạm vi và bằng chứng

- Chỉ xử lý Screen ID **ME-04**, route đề xuất `/mentor/courses/:courseId/lectures/new`.
- Expected từ [`list_screen.md`](../../../list_screen.md#L164): AC-21; GET #46 xác minh course context → POST #34 upload asset → POST #47 tạo lecture; liên kết ME-05 và ME-03; states `draft/uploading/creating/422/error`. Inventory cảnh báo không nhận `content:int64` như rich-text nếu chưa chốt.
- Đọc mục tiêu phiên bản đầy đủ tại `/home/daovh/.codex/attachments/f6127670-d01c-46c9-b22a-2adfcbe78641/goal-objective.md`; mỗi phiên chỉ một Screen ID.
- **Original assets:** `screen.png` 1175×1600, SHA-256 `5c95672f8912580f0dc932bccb233075cab6a29f5ea1ff789c93ea03abb960eb`; `code.html` 42,754 bytes, SHA-256 `489fb9dae33dc172d2d11375ac60da2a2f5341fe4cabb11a622729ba26f5f925`. Giữ nguyên hai file.
- `code.html` là mockup tĩnh: 7 anchors `href="#"`, 22 buttons, 11 inputs, 1 select; không có form, textarea, `contenteditable`, file input, fetch/XHR hoặc API call. Có một click handler cho CTA tạo bài giảng; handler chỉ giả lập success sau 900 ms, không kiểm tra hay gửi dữ liệu. Label auto-save chỉ là text tĩnh.
- Study Web được kiểm tra lại: root chỉ có `dist/`, `docs/`, `node_modules/`, `tsconfig.tsbuildinfo`; không có `src/`, package manifest hoặc router có thể sửa. Bundle/serving không chứng minh route/runtime.

## 2. Source/API trace trước khi viết DD

### API #46 — xác nhận course context

- Route source `GET /api/v1/mentor/courses`; Bearer JWT role `MENTOR`; query `status?`, `page=1`, `size=20` (size tối đa 100); success `200 DESIGN_RESOURCE_RETRIEVED` với `Page<Course>` và empty page hợp lệ.
- Current SQL chỉ lọc `courses.mentor_id = JWT sub`, sắp `created_at DESC, id ASC`; không có assigned-course relation hoặc endpoint lấy riêng course bằng path. Course projection gồm `id/title/description/thumbnail_url/price/status/mentor`, không có module, course code, lesson count hay course-specific detail fields.
- AC-21 cho phép course do Mentor sở hữu **hoặc được phân công**. Inventory cũng nói “course thuộc #46”, nhưng #46 chỉ direct owner. Ghi discrepancy; không coi course code mẫu trong screenshot là `courseId`.

### API #34 — upload file

- Registered route `POST /api/v1/uploads`, `multipart/form-data`: required `file`, `purpose`, optional `course_id`; Mentor phải dùng `purpose=LECTURE` và cung cấp course ID int64 trực tiếp sở hữu.
- Shared JWT guard accepts STUDENT or MENTOR, then purpose/role guard; direct-owner query runs before storage write. Source accepts any bytes/MIME and has no application file-size cap; it measures bytes, uses fallback filename `upload` and MIME `application/octet-stream`, generates `uploads/<UUID>`, calls injectable S3-compatible provider, then commits an `uploads` metadata row with status `UPLOADED`.
- Success `201 DESIGN_RESOURCE_CREATED`, response `UploadAsset{id,name,url,content_type,size_bytes,status}`. Errors source-backed: 401; 403 role/scope; 422 multipart/purpose/course validation; 503 storage unavailable; 500 metadata/DB failure. Storage failure or metadata failure attempts best-effort object cleanup; live provider/schema is unverified.

### API #47 — tạo lecture

- Registered `POST /api/v1/mentor/courses/{course_id}/lectures`, Bearer JWT role MENTOR, JSON strict body `{title:string<=200, content:int64, asset_refs:string, order:int32}`; extra fields are rejected.
- Current route/view validates signed-int64 course ID and the JSON-text asset ID array (`[]` allowed; duplicate IDs rejected), checks direct course owner with no course-status filter, then resolves every asset under same Mentor + `LECTURE` + same course. It inserts `lessons` with `content = str(request.content)`, status fixed to `PUBLISHED`, and `order` into `sort_order`; when refs exist it inserts ordered `lesson_uploads` rows in the same transaction. Success `201 DESIGN_RESOURCE_CREATED` returns `Lecture{id,course_id,title,content:string,assets,order,status}`.
- Errors source-backed: 401; 403 non-owner; 404 missing course or generic unresolved/cross-scope assets; 422 type/range/title/asset_refs validation; 500 query/mapping/transaction failure with rollback. No Draft create mode, rich-text encoding, duration/type/preview/prerequisite/stream URL, or request idempotency key is present in the body/source.
- API #47 local DD remains `Draft — Needs Confirmation` because live schema/migration is not verified. Its Q1/Q2 decision record resolves the local `content:int64` and `asset_refs` wire shapes; it does not make the screenshot's rich-text editor compatible with `content:int64`. API #34 historical `PLAN_RESULT.md` says #47 is UNWIRED, but current route/source/tests are present; current source takes precedence and that old note is stale.

### API #48 — post-create destination

- Registered `GET /api/v1/mentor/lectures/{lecture_id}` is the API for ME-05. It uses MENTOR Bearer auth, parses the ID, enforces direct course owner, then returns lecture plus linked ordered UploadAssets. Success `200`; source errors 401/403/404/500. It does not create or repair the lecture and does not prove browser navigation.

### Persistence/runtime boundary

- Current checked-in candidates: legacy BIGINT `lessons`, `uploads`, `lesson_uploads`; migrations `004_uploads.sql` and `005_lesson_uploads.sql`. No live DB or migration deployment inspected. API #34/#47 tests use fake DB/provider seams; test source and historical reports were read, tests were not run in this session.
- API #34 commits each uploaded object/metadata before #47 runs. A later #47 failure does not roll back successful uploads. Search found no upload delete endpoint; removing a mockup attachment cannot be specified as remote deletion.

## 3. Marker inventory and coordinate plan

Coordinates use original screenshot pixels, origin `(0,0)` at top-left, bounds `1175×1600`; annotation export is planned at 2× (`2350×3200`). Markers sit on component edges/gutters where possible; rich-text toolbar and editor content are grouped to keep the controls readable. After visual review, marker #3 and #25 were shifted away from nearby elements and JSON/SVG/PNG were regenerated from this final coordinate table. Every numbered marker must map once to JSON, SVG and one DD element row.

| # | Element dự kiến | Điểm đặt `(x,y)` |
|---:|---|---:|
| 1 | Brand/logo Mentor Portal | 157,22 |
| 2 | Điều hướng Mentor toàn cục | 700,22 |
| 3 | Tìm kiếm header | 704,50 |
| 4 | Notification button và badge | 969,48 |
| 5 | Tài khoản Mentor hiện tại | 1161,6 |
| 6 | Quay lại Workspace ME-03 | 14,58 |
| 7 | Breadcrumb course | 300,58 |
| 8 | Course code mẫu trên breadcrumb | 650,58 |
| 9 | Tiêu đề trang tạo bài giảng | 14,118 |
| 10 | Badge “ME-04 Authoring” | 510,119 |
| 11 | Nhãn auto-save mẫu | 847,67 |
| 12 | CTA xem trước (Preview) | 1002,95 |
| 13 | Header khối định vị lecture | 14,164 |
| 14 | Select chương/module | 14,236 |
| 15 | Badge Bloom-Tech level | 650,206 |
| 16 | Select thứ tự/vị trí bài | 668,236 |
| 17 | Input tiêu đề lecture | 14,304 |
| 18 | Bộ đếm ký tự tiêu đề | 660,277 |
| 19 | Input thời lượng ước tính | 14,369 |
| 20 | Hiển thị khung độ khó | 668,369 |
| 21 | Header khối media/video | 14,443 |
| 22 | Chip API #34 | 649,451 |
| 23 | Card file video đã tải | 14,520 |
| 24 | Thumbnail video | 44,518 |
| 25 | Tên và metadata file | 648,480 |
| 26 | Progress/status “100% Hoàn tất” | 665,528 |
| 27 | Nút xem phát thử media | 552,561 |
| 28 | Nút thay thế/retry media | 584,561 |
| 29 | Nút xóa media khỏi danh sách | 616,561 |
| 30 | Vùng kéo/thả/chọn tệp | 665,620 |
| 31 | Hướng dẫn MIME/dung lượng mẫu | 665,682 |
| 32 | Input URL stream HLS/Vimeo | 14,725 |
| 33 | Header tóm tắt và code sample | 14,807 |
| 34 | Chọn chế độ Markdown | 668,808 |
| 35 | Chọn chế độ WYSIWYG | 668,834 |
| 36 | Thanh công cụ định dạng: B/I/U/H2/H3/list/quote/code/image | 668,863 |
| 37 | Vùng nội dung Markdown/WYSIWYG gồm văn bản và code mẫu | 14,950 |
| 38 | Header attachments/source code | 14,1262 |
| 39 | Nút thêm attachment | 668,1263 |
| 40 | Card attachment PDF | 14,1305 |
| 41 | Nút gỡ attachment PDF | 363,1354 |
| 42 | Card attachment ZIP | 665,1305 |
| 43 | Nút gỡ attachment ZIP | 623,1354 |
| 44 | Header cấu hình phân phối/publish | 668,168 |
| 45 | Radio Video bài giảng chính | 1000,271 |
| 46 | Radio Bài đọc chuyên sâu | 1000,322 |
| 47 | Radio Hướng dẫn thực hành Lab | 1000,373 |
| 48 | Toggle Guest Preview | 1000,410 |
| 49 | Toggle khóa điều kiện tiên quyết | 1000,457 |
| 50 | Radio Lưu nháp | 668,501 |
| 51 | Radio Gửi duyệt/Publish | 1000,501 |
| 52 | Header kiểm định QA | 668,576 |
| 53 | Badge điểm QA 100% | 1000,570 |
| 54 | Giải thích QA | 1000,625 |
| 55 | Danh sách checklist QA | 1000,760 |
| 56 | CTA tạo bài giảng & gửi duyệt | 1000,882 |
| 57 | CTA lưu bản nháp | 668,920 |
| 58 | CTA hủy bỏ | 1000,920 |
| 59 | Chú thích ISO/EduTrust/AC | 1000,956 |
| 60 | Footer Study2Work và các nhóm liên kết | 14,1474 |
## 4. Kế hoạch sự kiện

| Event | Kích hoạt | Nguồn/hành động dự kiến | Bằng chứng hoặc blocker |
|---|---|---|---|
| ME04-EV-01 | Enter route / quay lại từ ME-03 | Đọc `courseId`, kiểm tra MENTOR session và xác minh course qua #46; không render như authorized trước khi có kết quả. | #46 là page direct-owner, không có detail-by-ID; assignment và deep-link policy chưa khớp. |
| ME04-EV-02 | Chọn module hoặc thứ tự | Đọc selection đã được server cấp; cập nhật metadata draft local. | Không có API/module source trong ME-04 contract; không dùng option mẫu hoặc tự tính order. |
| ME04-EV-03 | Nhập title/duration/content | Cập nhật form state, trim/limit theo rule đã duyệt. | #47 chỉ có `title<=200`, `content:int64`; duration không có field; title không có min/trim rule. |
| ME04-EV-04 | Chọn/kéo thả file | Gửi #34 multipart `file`, `purpose=LECTURE`, `course_id=<path int64>` tuần tự cho từng file. | Role/direct-owner, binary/MIME/size contract và side effect cần giữ rõ. |
| ME04-EV-05 | #34 success/progress | Map `UploadAsset.id/name/url/content_type/size_bytes/status`; giữ IDs theo thứ tự để chuyển vào `asset_refs`; hiển thị lỗi từng file. | Current source chỉ trả completion response; progress UI hiện chưa được wire. |
| ME04-EV-06 | Thay file/retry | Chọn và upload file mới; quản lý ID mới local. | Không có idempotency key hoặc delete asset API; không giả định thay thế/xóa remote file. |
| ME04-EV-07 | Xóa file attachment | Bỏ ID khỏi client draft nếu chưa submit. | Upload đã commit vẫn tồn tại; cleanup/retention policy chưa có contract. |
| ME04-EV-08 | Nhập URL stream | Validate URL theo policy được phê duyệt và liên kết với content/media. | #47 không nhận `video_url`; không có API resource binding cho field này. |
| ME04-EV-09 | Chọn Markdown/WYSIWYG/toolbar, sửa nội dung | Chỉnh rich-text local state và serialize theo contract. | #47 `content:int64` được lưu thành số thập phân dạng string; không tương thích text/code editor nếu chưa có mapping. |
| ME04-EV-10 | Thêm/gỡ attachment | Upload qua #34 rồi giữ UploadAsset IDs cho #47; không gửi URL/metadata tự nhập. | #47 `asset_refs` JSON string chứa ordered unique int64 IDs; deletion ngoài scope. |
| ME04-EV-11 | Xem trước | Tạo preview của unsaved draft hoặc điều hướng theo đích đã duyệt. | Không có preview API/state/route được xác nhận. |
| ME04-EV-12 | Chọn loại Video/Paper/Lab | Giữ lựa chọn trong form state sau khi có schema. | #47 không có `type` field; choices không được persist. |
| ME04-EV-13 | Bật/tắt Guest Preview | Lưu policy cho bài giảng. | #47 không có preview/access field hoặc policy. |
| ME04-EV-14 | Bật/tắt prerequisites | Lưu quan hệ điều kiện tiên quyết. | #47 không có prerequisite field/relationship. |
| ME04-EV-15 | Chọn Draft/Publish | Xác nhận lifecycle trước khi submit. | #47 luôn insert status `PUBLISHED`; không có Draft endpoint/body. |
| ME04-EV-16 | Lưu nháp | Persist draft và giữ route/state. | Không có API draft; không thể dùng #47 mà không publish. |
| ME04-EV-17 | Tạo bài giảng & gửi duyệt | Validate approved body; POST #47; map returned lecture ID/assets/status. | Current endpoint creates PUBLISHED immediately; cannot claim “gửi duyệt” or use rich-text body. |
| ME04-EV-18 | Tạo thành công | Navigate `/mentor/lectures/:lectureId` (ME-05); ME-05 calls #48 and shows server result. | #47 response has ID; #48 is read-only. Navigation remains proposed, Web route UNWIRED. |
| ME04-EV-19 | Validation/network/API error or repeated submit | Keep local input; prevent accidental repeat while request pending; reconcile ambiguous result before retry. | #34/#47 don't declare client idempotency; second POST may create a duplicate. |
| ME04-EV-20 | Hủy/quay lại ME-03 | Detect dirty state, request discard decision, route back with course context. | Confirmation, upload cleanup, browser history and draft persistence are undefined. |
| ME04-EV-21 | Header nav/search/notification/footer | Navigate only to inventory-defined screens/routes. | Mockup anchors are `#`; destinations and data contracts are not established here. |

## 5. Blocker và điều kiện nghiệm thu

- **ME04-B01 — access scope:** AC-21 allows owned/assigned courses; #46/#34/#47 current source only direct owner. Decide assignment semantics and manage permission.
- **ME04-B02 — course context:** #46 is paginated list, not an ID detail route; direct-entry behavior, route `courseId` mapping, course code and module/course context source are unresolved.
- **ME04-B03 — editor content mapping:** screenshot accepts markdown/WYSIWYG/code, while #47 requires signed int64 and stores its decimal text. Approve the meaning/representation or change the server contract before implementation.
- **ME04-B04 — lecture lifecycle:** #47 always creates `PUBLISHED`, while UI offers `DRAFT`, “Gửi duyệt”, preview and publish mode. Decide state machine and review lifecycle.
- **ME04-B05 — curriculum/order:** module hierarchy and lesson order source/rules are absent; #47 only accepts int32 `order`, with no range/next-order policy.
- **ME04-B06 — unsupported fields:** duration, lesson type, streaming URL, guest preview, prerequisites and QA result have no #47 request/response source.
- **ME04-B07 — upload policy:** screenshot claims accepted media types/2 GB max; API #34 source has no MIME allowlist or application max size. Approve client/provider policy and feedback.
- **ME04-B08 — upload lifecycle:** each #34 upload commits before #47; no upload delete/cleanup endpoint or idempotency contract. Draft/cancel/remove/retry and post-create failure can leave unlinked uploads.
- **ME04-B09 — client/runtime:** Study Web route/session/API client is absent; HTML handler only simulates success.
- **ME04-B10 — persistence deployment:** #47 DD still Draft until legacy BIGINT schema and migrations 004/005 are verified in the target database.
- **ME04-B11 — design/accessibility:** supplied mockup uses remote Plus Jakarta Sans/Tailwind and compact 28–42 px controls; Study design guide calls for local Inter/system font, min 44 px controls and responsive/focus behavior.

Plan acceptance: preserve both originals; 60 numbered markers match JSON/SVG/image/DD; every visible actionable control is represented by an element/event; API fields/errors and side effects trace to current source; unsupported behavior is blocked rather than guessed; source links and tracker/worklog resolve; no test or runtime claim without execution.

## 6. Source references to use in DD

- Inventory/AC: [`list_screen.md` ME-04](../../../list_screen.md#L164), `../../../../../../apps/study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md` AC-21 and `AC_03_MENTOR_TEACHING.drawio`.
- API catalog: `../../../../../../docs/lists/list_api.md` rows #34/#46/#47/#48 and upload decisions.
- Routes: `../../../../../../apps/study-server/app/api/v1.py` (#34 around `upload_file`, #46, #47, #48).
- Modules: `../../../../../../apps/study-server/app/modules/student/api_34_uploads/`; `../../../../../../apps/study-server/app/modules/mentor/api_46_mentor_courses/`, `api_47_mentor_lectures_create/`, `api_48_mentor_lecture_detail/`.
- Tests: corresponding `../../../../../../apps/study-server/tests/modules/student/api_34_uploads/` and Mentor API #46–#48 test directories; source review only.
- API DD: `../../../../../../apps/study-server/docs/dd/34_uploads/`, `46_mentor_courses/`, `47_mentor_lectures_create/`, `48_mentor_lecture_detail/`; treat DD status separately from runtime source.
- Persistence artifacts: `../../../../../../infra/postgres/study-server/DB.sql`, `migrations/004_uploads.sql`, `migrations/005_lesson_uploads.sql`.
- Study UI target: `../../../../../../.agents/web-study/design.md`; ME-03 entry: `../ME-03_workspace-khoa-hoc-cua-mentor/ME-03.md`.
