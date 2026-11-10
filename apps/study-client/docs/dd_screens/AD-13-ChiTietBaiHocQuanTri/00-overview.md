# AD-13 — Chi tiết bài học quản trị · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `AD-13` |
| Module | Admin |
| Route | `/admin/lessons/:lessonId` — route trong inventory, không phải xác nhận router runtime |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source status: **Detailed Design:** `DD BLOCKED` · **Implementation:** `IMPLEMENTATION BLOCKED` · **Study Web runtime:** `NOT VERIFIED` (`UNWIRED` trong checkout)<br> |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
| Nguồn đối chiếu | [AD-13.md](../../screen_stitch/05_admin/AD-13_chi-tiet-bai-hoc-quan-tri/AD-13.md), [AD-13_PLAN.md](../../screen_stitch/05_admin/AD-13_chi-tiet-bai-hoc-quan-tri/AD-13_PLAN.md), [AD-13_markers.json](../../screen_stitch/05_admin/AD-13_chi-tiet-bai-hoc-quan-tri/AD-13_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Hiển thị đúng Lesson fields từ #83; linked progress/resources/metrics chỉ sau khi có contract riêng. Mở AD-14 bằng cùng numeric `Lesson.id`.
- In-scope: AD-12 numeric `Lesson.id` → GET #83 `ApiEnvelope<Lesson>`; local #83 trả 7 fields, loại `DELETED`, không đọc dependencies/metrics; API #86 tự kiểm tra progress/resources/uploads khi delete. Không gọi Student #24 thay API Admin.
- Out-of-scope: Xem gate bên dưới; không kết luận Study Web route/UI đã wired hoặc runtime đã chạy.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-34 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Hiển thị đúng Lesson fields từ #83; linked progress/resources/metrics chỉ sau khi có contract riêng. Mở AD-14 bằng cùng numeric `Lesson.id`. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #83
- Liên kết màn hình dự kiến: [AD-14](../AD-14-SuaDoiTrangThaiXoaBaiHoc/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | loading/ready/404/error |
| Current runtime | Worklog/context Study Web | `UNWIRED` / `RUNTIME NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [AD-13 source screen.png](../../screen_stitch/05_admin/AD-13_chi-tiet-bai-hoc-quan-tri/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/05_admin/AD-13_chi-tiet-bai-hoc-quan-tri/screen_annotated.png))
- Luồng: AD-12 numeric `Lesson.id` → GET #83 `ApiEnvelope<Lesson>`; local #83 trả 7 fields, loại `DELETED`, không đọc dependencies/metrics; API #86 tự kiểm tra progress/resources/uploads khi delete. Không gọi Student #24 thay API Admin.
- Priority: P1; Gate/source status: **R** local #83 route/module/query/model/test source; API DD Draft. **DD BLOCKED; IMPLEMENTATION BLOCKED:** AC dependencies chưa có output rule; course title/type/resource/progress/metrics/SSE fields thiếu; ADMIN vs lesson-management permission, legacy/V1-PILOT schema, nullable required fields/status enum và Study Web `UNWIRED` còn mở; **RUNTIME NOT VERIFIED**

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

# AD-13 — Chi tiết bài học quản trị

> **Detailed Design:** `DD BLOCKED` · **Implementation:** `IMPLEMENTATION BLOCKED` · **Study Web runtime:** `NOT VERIFIED` (`UNWIRED` trong checkout)<br>
> **Screen:** AD-13 · **Actor expected:** Admin có lesson-management permission theo AC-34 · **Route đề xuất:** `/admin/lessons/:lessonId` · **API:** #83 · **Trước:** AD-12/#82 · **Sau:** AD-14/#84–#86<br>
> **Assets:** [screen nguồn](../../screen_stitch/05_admin/AD-13_chi-tiet-bai-hoc-quan-tri/screen.png) · [screen có marker](../../screen_stitch/05_admin/AD-13_chi-tiet-bai-hoc-quan-tri/screen_annotated.png) · [marker map](../../screen_stitch/05_admin/AD-13_chi-tiet-bai-hoc-quan-tri/AD-13_markers.json) · [kế hoạch](../../screen_stitch/05_admin/AD-13_chi-tiet-bai-hoc-quan-tri/AD-13_PLAN.md) · [inventory](../../list_screen.md)

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: A. Tổng quan màn hình

### Mục tiêu và expected behavior

AD-13 là trang Admin xem chi tiết một lesson đã chọn từ AD-12. Inventory row 71 đề xuất route `/admin/lessons/:lessonId`, GET #83 và xem lesson content/status/linked progress theo contract; AC-34 mô tả AD-12 list → AD-13 detail → một nhánh tại AD-14 (update #84, status #85 hoặc delete #86) → reload AD-12. Path #83 yêu cầu `lesson_id:int64`; dữ liệu handoff ứng viên là numeric `Lesson.id` từ row list. API #82 catalog hiện ghi một `Lesson`, còn local #82 trả collection; cần giữ discrepancy từ AD-12 khi chốt client mapping.

AC-34 node n5 ghi “Đọc lesson + dependencies”, nhưng không xác định dependency fields, counts, schema hay vị trí response. API #83 catalog trả `ApiEnvelope<Lesson>` trực tiếp, không khai báo dependencies. Đây là blocker để màn hình không tự trình bày progress/resource counts.

### Current behavior đã xác minh

- **Study Web:** thư mục hiện có `docs`, ignored `dist`, `node_modules` và `tsconfig.tsbuildinfo`; không có editable `src`, `package.json`, router hoặc API client. `code.html` không có route param/data binding, request, `EventSource`, WebSocket, timer hay listener. Anchors dùng `href="#"`; action tới AD-14 là button disabled. Study Web `UNWIRED`; không có runtime verification.
- **API #83:** local route `GET /api/v1/admin/lessons/{lesson_id}`, `GetAdminLessonEnvelope`, direct `Lesson` response. Bearer/JWT shared guard yêu cầu role `ADMIN` trước custom raw-path parsing và DB. AC-34 lesson-management permission chưa được enforce bởi route source đã rà soát.
- `lesson_id` custom parser nhận signed int64 trong bounds; malformed, overflow hoặc raw path dài hơn 20 ký tự trả 404 `DESIGN_RESOURCE_NOT_FOUND` (local DERIVED choice để khớp error set; không gọi DB). Parser không tạo 422.
- Bound query lấy tối đa một row từ candidate legacy `lessons` theo `id`, loại `status='DELETED'`; không áp dụng public `PUBLISHED` filter. Không join `courses`, không đọc `resources`/`lesson_progress`, không trả pagination/dependency data, không ghi hoặc commit.
- Mapping dùng reusable API #09 `Lesson`: `id`, `course_id`, `name→title`, nullable `content`, nullable `video_url`, `sort_order→order`, `status`. Success HTTP 200 trả direct `data` object, `meta:{}` và trace ID. Row thiếu/mismatch hoặc required projection không hợp lệ→safe 500 + rollback; row vắng mặt/tombstone→404 + rollback; query error→safe 500 + rollback. Optional `content`/`video_url` null serialize thành JSON `null`.
- Test source API #83 đã đọc, không chạy trong phiên này. Source tests dùng fake DB; historical API DD report ghi 15 focused passes nhưng không chứng minh live PostgreSQL/schema/deployment.
- API #83 DD là `Draft — Needs Confirmation`. Legacy `lessons` DDL dùng BIGINT và cho phép nullable `course_id`, `sort_order`, `status`, trong khi Lesson response yêu cầu các field đó. V1-PILOT DDL dùng UUID/versioned lesson model với field khác; live schema chưa được xác minh.

### Tác nhân, điều kiện và quyền

- **Actor expected:** Admin có lesson-management permission theo AC-34. **Current API:** chỉ shared role guard `ADMIN`; fine-grained permission và ownership scope chưa được source-backed cho #83.
- **Entry condition:** AD-12 selection truyền numeric lesson ID vào `lessonId` route param; route/API client chưa được triển khai. Nếu thiếu param, client route behavior chưa được định nghĩa; API path bắt buộc.
- **Postcondition:** render một Lesson response nếu #83 thành công; không thay đổi dữ liệu. AD-14 là nơi tiếp tục các mutation #84–#86.
- Không dùng copy “Chế độ phân quyền Admin”, “RBAC”, “cách ly khỏi học viên”, “khóa ghi đồng thời” hoặc “Audit Log Level 1” làm bằng chứng runtime/access/audit guarantee.

### API #83 contract và local behavior

| Thuộc tính | Catalog / AC | Current source |
|---|---|---|
| Method/path | `GET /api/v1/admin/lessons/{lesson_id}` | Route wired cùng path; raw `lesson_id` chuyển sang module |
| Authentication | Bearer JWT; role Admin | Shared guard `role="ADMIN"`; chạy trước path parse/DB |
| Permission | AC-34 yêu cầu lesson-management permission | Fine-grained permission chưa có source |
| Input | Required path `lesson_id:int64`; không body/query | Custom signed-int64 parser; malformed/overflow/overlength→404 locally (DERIVED) |
| Success | 200 `ApiEnvelope<Lesson>` | 200 direct `Lesson` object trong `data` |
| Error | 401, 403, 404, 500 | Cùng catalog error set; no 422 trong OpenAPI #83 |
| Data | Lesson theo reusable schema | Legacy BIGINT lookup candidate, loại `DELETED`; không join dependencies |
| Side effect | GET / read-only | Không mutate, không commit; rollback nhánh missing/error |

### Discrepancies và blocker

| Chủ đề | Expected/design hoặc mockup | Current source | Trạng thái / ảnh hưởng |
|---|---|---|---|
| Dependencies / linked progress | Inventory và AC-34 nói xem linked progress/đọc lesson + dependencies; mockup có resource/quiz/discussion tiles. | #83 trả Lesson בלבד, không đọc dependencies. #86 rechecks `lesson_progress`, `resources`, `lesson_uploads` lúc delete và trả 422 nếu còn liên kết. | `DISCREPANCY / BLOCKER`: không hiển thị counts hoặc dùng detail snapshot để quyết định xóa. Cần owner xác định output #83. |
| Metadata | Mockup có title, lesson identifier, course, content type, order, publication status. | #83 có `id`, `course_id`, `title`, `order`, `status`, nullable `content`/`video_url`; không có course title/type/slug. | `DISCREPANCY`: map numeric IDs/raw fields có điều kiện; không tự dựng tên khóa, type hoặc status label. |
| Content/media | Mockup nói kỹ thuật và media stream được trích xuất tự động. | API chỉ trả string content và nullable `video_url`; không có content-block/resource schema, signer/player/DRM, expiry hoặc media authorization. | `BLOCKER`: không tự render raw URL hoặc coi content là trusted HTML. |
| Metrics/SSE | Mockup có learners, completion/submission/rating, progress bars, Realtime SSE. | #83 không có metrics, stream, counts, filter hay SSE. | `STATIC_ONLY / UNMAPPED`: không dùng endpoint khác nếu không có AC/contract handoff. |
| Audit/concurrency/sync | Mockup tuyên bố auto lock, Audit Log Level 1, sync state. | #83 là GET read-only; không lock row, ghi audit hoặc lấy sync status. | `STATIC_ONLY`: không đưa ra guarantee hoặc trạng thái hoạt động. |
| Authorization/schema/status | AC-34 lesson-management permission; screen status field. | Source chỉ check `ADMIN`; legacy schema nullable và khác V1-PILOT; status enum/casing mở. | `OPEN / BLOCKER`: cần policy, live schema/nullability và enum xác nhận. |
| Study Web/design | Mockup cobalt/Plus Jakarta Sans/full-width; anchors/static button. | UI source absent; guide yêu cầu ocean tokens, Inter/system, content width khoảng 1120px. | `UNWIRED / DESIGN DISCREPANCY`: không coi asset là implementation; theo guide khi frontend tồn tại. |
