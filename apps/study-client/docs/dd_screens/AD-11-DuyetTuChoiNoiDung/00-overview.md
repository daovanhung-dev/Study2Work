# AD-11 — Duyệt/từ chối nội dung · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `AD-11` |
| Module | Admin |
| Route | `/admin/content/:contentId/review` — đăng ký trong Angular router; runtime chưa xác minh |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source status: **Detailed Design:** `DD BLOCKED` · **Implementation:** `PARTIAL SOURCE; DECISION FLOW BLOCKED` · **Study Web runtime:** `NOT VERIFIED` |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.2 / 2026-11-20 (signed-int64 route guard) |
| Nguồn đối chiếu | [AD-11.md](../../screen_stitch/05_admin/AD-11_duyet-tu-choi-noi-dung/AD-11.md), [AD-11_PLAN.md](../../screen_stitch/05_admin/AD-11_duyet-tu-choi-noi-dung/AD-11_PLAN.md), [AD-11_markers.json](../../screen_stitch/05_admin/AD-11_duyet-tu-choi-noi-dung/AD-11_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Preview Content được chọn; metadata chỉ hiển thị field có contract; form reason theo #81 sau khi thống nhất validation.
- In-scope: AD-10 link chuyển `Content.id` sang route AD-11; AD11Page validates the raw signed-int64 route ID before GET #79 and preserves valid raw text. UI hiển thị field có contract và payload dưới dạng JSON text. PATCH #80/#81 được tham chiếu trong expected flow nhưng hiện không có caller Web và controls vẫn khóa. #80 local đặt `APPROVED`, không publish; #79 không trả author/version.
- Out-of-scope: Xem gate bên dưới; không tuyên bố quyết định kiểm duyệt, publish, media preview, rubric hoặc runtime đã được xác minh.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-33 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Preview Content được chọn; metadata chỉ hiển thị field có contract; form reason theo #81 sau khi thống nhất validation. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #79, #80, #81
- Liên kết màn hình dự kiến: [AD-10](../AD-10-HangDoiKiemDuyetNoiDung/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | loading/ready/approving/rejecting/stale/error |
| Current source/runtime | Angular route, AD11Page, #79 caller/spec | `WIRED SOURCE` / `RUNTIME NOT VERIFIED`; loading/loaded/error states exist |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [AD-11 source screen.png](../../screen_stitch/05_admin/AD-11_duyet-tu-choi-noi-dung/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/05_admin/AD-11_duyet-tu-choi-noi-dung/screen_annotated.png))
- Luồng: Candidate `Content.id` từ AD-10 → GET #79 → PATCH #80 hoặc PATCH #81 với `{reason}` → reload #78. #80 local đặt `APPROVED`, không publish; #79 không trả author/version.
- Priority: P1; Gate/source status: **R** local route/module/test source #79–#81 and Angular route/page/#79 caller; API DD Draft. **DD BLOCKED; IMPLEMENTATION PARTIAL SOURCE; DECISION FLOW BLOCKED:** AC `APPROVED/PUBLISHED` vs #80 `APPROVED`; reason required vs optional/disabled in prototype; author/version/media/rubric source thiếu; revision/stale policy, moderation permission và live schema/migration còn mở; **RUNTIME NOT VERIFIED**

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.
- 2026-11-16 — Reconcile trạng thái theo checkout hiện tại: Angular route/page/GET #79 caller và tests tồn tại; controls #80/#81 vẫn disabled. Không xác minh browser runtime hoặc đóng các gate contract.

## Trạng thái và ranh giới bằng chứng

# AD-11 — Thẩm định và phê duyệt nội dung bài giảng

> **Detailed Design:** `DD BLOCKED` · **Implementation:** `PARTIAL SOURCE; DECISION FLOW BLOCKED` · **Study Web runtime:** `NOT VERIFIED`<br>
> **Screen:** AD-11 · **Actor expected:** Admin theo AC-33; moderation-specific permission chưa xác nhận · **Route:** `/admin/content/:contentId/review` (Angular router source-present) · **AC:** AC-33 · **APIs:** #79, #80, #81<br>
> **Assets:** [screen nguồn](../../screen_stitch/05_admin/AD-11_duyet-tu-choi-noi-dung/screen.png) · [screen có marker](../../screen_stitch/05_admin/AD-11_duyet-tu-choi-noi-dung/screen_annotated.png) · [marker map](../../screen_stitch/05_admin/AD-11_duyet-tu-choi-noi-dung/AD-11_markers.json) · [kế hoạch](../../screen_stitch/05_admin/AD-11_duyet-tu-choi-noi-dung/AD-11_PLAN.md) · [inventory](../../list_screen.md)

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: A. Tổng quan màn hình

### Expected behavior

Inventory row 69 mô tả AD-11 là màn hình thẩm định nội dung được chọn từ AD-10. Luồng AC-33 dự kiến lấy chi tiết qua #79, chọn một nhánh quyết định: #80 approve hoặc #81 reject với lý do, rồi làm mới queue #78. AC-33 gọi tới metadata tác giả/phiên bản; các quy tắc duyệt và publish cần được giải quyết trước khi UI/BE được triển khai.

API catalog `docs/lists/list_api.md` quy định:

| API | Request contract | Success | Catalog errors |
|---|---|---|---|
| #79 `GET /api/v1/admin/content/{content_id}` | Bearer/Admin; path `content_id:int64!`; không body/query | 200 `ApiEnvelope<Content>` | 401, 403, 404, 500 |
| #80 `PATCH /api/v1/admin/content/{content_id}/approve` | Bearer/Admin; path `content_id:int64!`; không body/query | 200 `ApiEnvelope<Content>` | 401, 403, 404, 422, 500 |
| #81 `PATCH /api/v1/admin/content/{content_id}/reject` | Bearer/Admin; path `content_id:int64!`; body `{reason:string!}` | 200 `ApiEnvelope<Content>` | 401, 403, 404, 422, 500 |

### Current behavior theo asset và source

- **Angular source:** `admin.routes.ts` đăng ký `/admin/content/:contentId/review` → `AD11Page`; AD-10 tạo link an toàn từ `Content.id`; `AD11ApiService` gọi GET #79 bằng `AdminApiService`/Admin session. Page validates the complete raw `contentId` against #79 signed-int64 path rules before GET; invalid/missing/out-of-range values show an error without a request, while valid IDs are passed unchanged. It has loading/loaded/error state and displays fields supported by #79 và render `payload` thành JSON text trong `<pre>`. Spec xác nhận payload không được tạo thành HTML. Source tồn tại không chứng minh browser/runtime hoặc deployment; runtime vẫn `NOT VERIFIED`.
- **Stitch prototype:** `code.html` là trang tĩnh. Back link, navigation và footer anchors dùng `href="#"`; notification không có handler. Approve/reject buttons và textarea `#review-comments` disabled. Preview/metadata là placeholder; không có request/API client hoặc media decoder trong prototype.
- **Preview và metadata trong Angular:** Content title và các field được contract hỗ trợ được lấy từ #79. Payload hiển thị như JSON text, không có video/SCORM/PDF renderer. Author, course title, submitted date, version/revision vẫn unavailable vì không có trong response.
- **Decision panel:** Angular hiện khóa reason và cả hai decision buttons, không gọi #80/#81. CTA hiện ghi “Phê duyệt nội dung (Approve)” để không hàm ý publish. Stitch prototype vẫn ghi reason “Tùy chọn” và “Phê duyệt xuất bản”, trái với #81 field `reason` và #80 chỉ chuyển Content sang `APPROVED`, không `PUBLISHED`.
- **Rubric:** Stitch prototype có ba criterion được đánh dấu check nhưng progress `0/3`; Angular hiển thị “Chưa có nguồn” và không kết luận tiêu chí đã được nạp. Không có API/model/rubric state được tìm thấy.
- **API #79 local source:** đọc active logical Content row và trả direct projection đúng tám field: `id`, `course_id`, `content_type`, `title`, object `payload`, `status`, nullable `parent_id`, `order`. Không có author, course title, submitted date, revision/version hay signed media locator. Detail không lọc trạng thái `PENDING_REVIEW` và không đọc `content_versions`.
- **API #80 local source:** shared `ADMIN` guard; khóa active Content row; chỉ cho phép `PENDING_REVIEW → APPROVED`; ghi một decision/audit candidate với actor JWT `sub`, trạng thái cũ/mới và reason `NULL`; commit sau khi response projection hợp lệ. Không ghi version, không phát notification, không publish.
- **API #81 local source:** strict JSON body `{reason:string}`; shared `ADMIN` guard; khóa active pending row; chuyển `PENDING_REVIEW → REJECTED`; ghi một decision row với actor, trạng thái cũ/mới và reason nguyên văn; response Content không trả reason. Empty string hiện được chấp nhận; không có trim/min/max/blank-only rule trong catalog/source.
- **Error behavior local:** #79 sai định dạng/overflow path → 404; missing/soft-deleted → 404. #80/#81 sai/overflow path → 422; missing/deleted → 404; current status khác pending → 422; query/update/audit/projection/commit error → safe 500 + rollback. #81 body schema errors xảy ra tại FastAPI trước khi handler chạy.
- **Persistence/auth limits:** Migration 011 là checked-in BIGINT audit candidate, không phải bằng chứng schema đã deploy. Legacy BIGINT `contents` và V1-PILOT UUID content/review model khác nhau; live DB chưa xác minh. Shared `ADMIN` không chứng minh moderation-specific permission. Local tests dùng fake DB và không xác nhận PostgreSQL hoặc live policy.

### Expected và current discrepancy

| Chủ đề | Expected / design | Current source/prototype | Trạng thái và ảnh hưởng |
|---|---|---|---|
| Trạng thái sau approve | AC-33 diagram node #9 ghi `APPROVED/PUBLISHED + audit`; mockup nói “phê duyệt xuất bản”. | #80 catalog/source chuyển sang `APPROVED`; Angular CTA chỉ ghi “Phê duyệt nội dung” và đang disabled. | `DISCREPANCY` giữa AC/prototype và #80 vẫn mở; không được hiển thị success như đã publish nếu chỉ gọi #80. |
| Reason từ chối | #81 yêu cầu field `reason:string!`. | Stitch ghi “Tùy chọn”; Angular textarea disabled. Local schema cho phép empty string, giữ nguyên whitespace. | `DISCREPANCY`: form chưa thể đáp ứng contract; required/blank/length/copy chưa thống nhất. |
| Author/version và nội dung preview | AC #79 yêu cầu review metadata; preview cần render Content. | #79 chỉ có tám Content field, không author/version/course title/submitted time hoặc media URL. | `BLOCKER`: không dựng metadata, revision hoặc secure renderer từ placeholder. |
| Revision/stale item | Handoff queue → detail → decision cần nhất quán. | #79/#80/#81 chỉ dùng logical `content_id`; không request version/expected-row token; #79 không lọc pending. | `OPEN`: quyết định có thể tác động logical row hiện hành, không bảo đảm revision Admin vừa xem; stale behavior chưa có 409 contract. |
| Permission | AC actor Admin. | Current APIs kiểm tra role `ADMIN`. | Shared role chưa chứng minh permission kiểm duyệt cụ thể; owner cần chốt scope. |
| Audit/schema | AC yêu cầu audit decision. | #80/#81 dùng migration 011 như local candidate; fake DB tests. | `DERIVED`; live schema, migration deployment, grants và retention/access chưa xác minh. |
| Rubric/renderer/runtime | Mockup thể hiện rubric và secure player. | Angular route/page tồn tại; rubric báo “Chưa có nguồn”, payload chỉ là JSON text; không có secure renderer. | `UNWIRED` cho rubric/media; runtime chưa xác minh; không có scoring/publish gate. |

### Tác nhân, điều kiện vào và dữ liệu sở hữu

- **Actor expected:** Admin theo AC-33/catalog. Request phải có Bearer JWT với role `ADMIN` theo current source. Không suy ra vai trò này cho phép mọi hành động moderation.
- **Điều kiện vào expected/current:** AD-10 có link tới route AD-11 bằng `Content.id` an toàn; `AD11Page` validates the complete raw route ID as signed-int64 before #79 and passes valid strings unchanged; invalid IDs stop locally without a request. #79 local có thể trả một Content active ở status bất kỳ; không có status gate phía Web.
- **Dữ liệu canonical local:** #79 `data` là Content hiện tại, các field mapping nằm trong C. `payload` là object nhưng không có media-specific schema/URL trong response contract dùng ở màn này.
- **Dữ liệu không có:** author identity/display name, course name, submitted timestamp, review version, audit history, preview token/asset URL, rubric, rubric result, ownership grant hay moderator permission details.
- **Source of truth:** AC/index + API catalog cho expected flow; direct router/modules/query/models/tests cho current local behavior; screenshot/HTML chỉ cho presentation. API DD #79–#81 đều còn Draft/Needs Confirmation.
