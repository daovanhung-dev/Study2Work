# ME-08 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `ME-08-API-001` | #52 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `ME-08-API-002` | #53 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `ME-08-API-003` | #49 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #52, #53, #49
- Orchestration/data notes: PATCH #52 hay DELETE #53 theo action → GET #49 refresh; không tự đặt soft-delete policy.
- BE/source status và gate: **D**; **BLOCK:** Publish state machine và delete dependency cần chốt
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: 2. Current API/data trace

### Hydrate và refresh — API #49

`GET /api/v1/mentor/courses/{course_id}/content` không có body/query. Shared guard kiểm tra Bearer/JWT và role `MENTOR` trước DB; sau đó parse signed int64, đọc course, so sánh numeric JWT subject với `courses.mentor_id`, rồi lấy các dòng `contents` có `deleted_at IS NULL`, sắp theo `parent_id NULLS FIRST`, `content_order`, `id`.

Response success là `ApiEnvelope<Content[]>` với mỗi item `{id:int64, course_id:int64, content_type:string, title:string, payload:object, status:string, parent_id:int64|null, order:int32}`. Response là collection phẳng để client dựng cây; không có endpoint Content detail hoặc `canPublish/canDelete` field. #49 trả mọi status đang hoạt động để Mentor quản lý; `data:[]` hợp lệ.

Lỗi hiện tại: 401 auth; 403 role/direct-owner mismatch; 404 course path sai/không có course; 500 query, projection, duplicate/missing-parent/cycle integrity. Không có partial-tree response. Client edit flow phải tìm chính xác `data[].id == contentId` và xác nhận cùng `course_id`; không dùng giá trị mẫu của screenshot nếu không tìm thấy.

### Publish/unpublish — API #52 current source và contract

| Hạng mục | Current route/module source | Catalog/AC/API DD |
|---|---|---|
| Method/path | `PATCH /api/v1/mentor/content/{content_id}/publish` | Cùng route. |
| Request | Strict JSON `{published:boolean}`; bool strict, field thừa bị cấm. | Catalog #52 và AC-22 chỉ nêu path, không có body/action. Body là `DERIVED`; #52 DD vẫn `Draft — Needs Confirmation`. |
| Auth/access | Bearer + role `MENTOR`; khóa Content/Course rồi yêu cầu JWT numeric `sub == courses.mentor_id`. | AC-22 nói có quyền quản lý course; assignment/co-owner mapping chưa được source xác nhận. |
| Local transition fallback | `APPROVED → PUBLISHED` khi `published=true`; `PUBLISHED → APPROVED` khi `published=false`. Target giống trạng thái hiện tại là no-op và vẫn trả 200. Các trạng thái khác trả 422. | Catalog chỉ nói validate readiness; không định nghĩa enum, readiness, publish vs approval hay unpublish target. |
| Side effect | Chỉ đổi `contents.status`; không đổi payload/order/parent, không ghi `content_versions` hay audit row. | AC-22 nói update publication status; AC-33 gộp `APPROVED/PUBLISHED` khi Admin approve nên lifecycle đang mâu thuẫn/mở. |
| Success | HTTP 200 `DESIGN_RESOURCE_UPDATED`, `data` là Content projection. | `ApiEnvelope<Content>`. |

View trace: route → `publish_content` → shared Mentor guard → parse signed-int64 Content ID → `LOCK_MENTOR_CONTENT` (`FOR UPDATE OF content, course`, active row) → owner check → so sánh current/target status → conditional `UPDATE_PUBLICATION_STATUS` với expected status hoặc giữ row hiện tại cho same-target → validate Content projection → commit → response. Lookup/update/mapping/commit lỗi rollback an toàn và trả 500. Body/path/current state không hợp lệ trả 422 hoặc 404 theo nhánh; owner mismatch 403. Không có 409/version token.

`APPROVED` hiện chỉ là gate theo status, không kiểm tra payload completeness, asset, ContentType, revision, child readiness hoặc permission flag. Không suy ra rằng đổi status sẽ làm nội dung “hiển thị cho tất cả học viên”: API DD ghi rõ readiness/current revision và tác động tới public reader chưa được định nghĩa. `#52` source có target-idempotency cho retry cùng body, nhưng body và state machine chưa được duyệt.

### Xóa — API #53 current source và contract

| Hạng mục | Current route/module source | Catalog/AC/API DD |
|---|---|---|
| Method/path | `DELETE /api/v1/mentor/content/{content_id}` | Cùng route; path int64, không body/query. |
| Auth/access | Bearer + role `MENTOR`; khóa active Content/Course rồi so sánh JWT subject với `courses.mentor_id`. | AC-22 yêu cầu quyền quản lý course; direct owner là current fallback, không phải policy được duyệt. |
| Guards | Current `status == PUBLISHED` trả 422 trước khi truy vấn dependency. Nếu không PUBLISHED, query chỉ kiểm tra **direct child** có cùng course, `parent_id=content_id`, `deleted_at IS NULL`; có child thì 422. Các status không phải PUBLISHED khác được source cho phép qua guards này. | Catalog yêu cầu “nếu được phép; kiểm tra dependency”, nhưng không liệt kê dependency hoặc status eligibility. Child/PUBLISHED rules là `DERIVED`. |
| Mutation | `UPDATE contents SET deleted_at=CURRENT_TIMESTAMP`; không hard-delete, cascade, reparent, đổi status, ghi audit/version hoặc kiểm tra submission/asset/progress. | AC-22 chỉ mô tả DELETE/soft delete rồi reload tree; retention, audit, dependency ngoài cây và queue withdrawal còn mở. |
| Success | HTTP 200 `DESIGN_RESOURCE_DELETED`; `data={id:int64, status:"deleted", deleted_at:datetime}`. | `ApiEnvelope<DeleteResult>`. Response không trả `course_id`. |

View trace: route → `delete_content` → shared Mentor guard → parse signed-int64 ID → lock Content/Course where active → owner check → reject PUBLISHED → query active direct child → soft-delete timestamp → validate `DeleteResult` → commit → success envelope. Missing/already deleted/invalid ID 404; role/auth 401/403; owner mismatch 403; PUBLISHED/active child 422; query/projection/commit failure 500 with rollback. Vì #53 không thay `status`, response literal `deleted` là DeleteResult status, không phải ContentStatus.

Sau khi `deleted_at` được ghi, #49 loại target khỏi collection. Lặp DELETE lên tombstone trả 404 từ active-row lookup. Nếu request timeout sau commit, client không thể coi lần DELETE kế tiếp là cùng success; retry policy chưa có contract. Candidate reconciliation là GET #49 bằng `courseId` đã giữ lại, không gửi lại action tự động.

### Persistence boundary và cây Content

- Local `contents` được khai báo trong legacy `DB.sql` và migration 006; migration 007 thêm `content_versions`. Đây là checked-in schema evidence, không xác nhận live database/deployment. Không dùng UUID V1-PILOT `content_blocks` thay cho legacy BIGINT Content.
- #52 cập nhật status của row hiện tại, không chọn version từ `content_versions`. #53 chỉ cập nhật `deleted_at`, giữ row và mọi snapshot; không xóa lịch sử.
- #53 guard chỉ nhìn active direct children. Đây không phải kiểm tra dependency toàn hệ thống: không thấy query với lesson/assessment/asset/submission/progress/review queue hoặc các tham chiếu JSON payload. Ngoài ra #49 loại mọi tombstone rồi từ chối cây có parent không hiện diện; source #53 không kiểm tra descendant sâu bị tách bởi một child đã soft-delete. Đây là khoảng trống suy ra từ hai source path, cần owner xác nhận trước khi tuyên bố cây luôn hợp lệ sau delete.
- API #52/#53 test files hiện có là fake-session HTTP tests. Context Study Server ghi nhận focused suites trước đó lần lượt 27 và 18 tests pass; phiên này chỉ đọc test source/context, không chạy test. Fake rows không xác nhận PostgreSQL lock/FK, migration live hoặc runtime deployment.

### Trích từ DD nguồn: 3. Data mapping và quy tắc field

| Field/context | Source/format | Dùng tại ME-08 | Validation/limit hiện có |
|---|---|---|---|
| `contentId` | Proposed route path, int64 Content ID | Tìm node trong #49; path của #52/#53. Không nhầm với Lecture ID. | API #52/#53 parse signed int64; sai format/range → 404. Client route/parser chưa tồn tại. |
| `courseId` | ME-06 route/context; #49 response `course_id` | GET #49 ban đầu và refresh sau #52/#53. | Required cho #49; absent trong ME-08 proposed route và DeleteResult. Handoff chưa được định nghĩa. |
| `status` | `Content.status:string` trong #49/#52 | Hiển thị trạng thái thật chỉ sau khi load exact Content. | Enum chưa approved; không map mặc định sang “Bản nháp”. Local #52 chỉ cho APPROVED/PUBLISHED transition; #53 chỉ chặn exact PUBLISHED. |
| `title`, `content_type`, `payload` | #49 Content fields | Target card/impact decision context. | `payload` object không có subtype schema. Screenshot title/status/sample content không phải response. |
| `parent_id`, `order` | #49 response (`int64|null`, `int32`) | Có thể xác định target nằm ở đâu; không được đổi ở ME-08. | #52 trả Content; #53 không trả Content/cây mới. Refresh #49 để dựng lại. |
| `published` | #52 body strict bool (current source only) | Target state true/false; không phải toggle mơ hồ. | Catalog/AC body absent, DERIVED. Không gửi cho #53 hoặc field `status` tự tạo. |
| `deleted_at` | #53 DeleteResult datetime; DB `CURRENT_TIMESTAMP` | Chỉ hiển thị server result/audit nếu UI có quyết định. | API trả timestamp; timezone semantics của legacy `TIMESTAMP` chưa xác nhận. |
| Impact/audit/environment | Static mockup copy | Không bind thành server metric hoặc authorization. | #49/#52/#53 không có field/source. |

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/04_mentor/ME-08_xuat-ban-xoa-noi-dung/ME-08.md)
