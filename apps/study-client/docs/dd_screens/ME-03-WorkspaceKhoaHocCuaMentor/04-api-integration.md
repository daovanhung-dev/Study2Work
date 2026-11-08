# ME-03 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `ME-03-API-001` | #49 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `ME-03-API-002` | #65 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #49, #65
- Orchestration/data notes: GET #49 và #65 sau khi course thuộc #46; render module theo permissions.
- BE/source status và gate: **D**
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: 2.1 API #49 — cây Content

| Thành phần | Contract/source hiện tại |
|---|---|
| Route | `GET /api/v1/mentor/courses/{course_id}/content` |
| Auth | `Authorization: Bearer <JWT>`; shared guard yêu cầu `MENTOR`, lấy numeric JWT `sub`, chạy trước truy vấn. |
| Input | `course_id` path theo signed-int64; không query/body. Sai định dạng/range hoặc course không tồn tại → 404. |
| Access | Đọc `courses.id`, so `courses.mentor_id` với JWT `sub`; khác owner → 403. Quan hệ assignment không được kiểm tra. |
| Read | `contents` cùng course, `deleted_at IS NULL`, không lọc `status`, không phân trang; order `parent_id NULLS FIRST, content_order ASC, id ASC`. Không ghi/commit. |
| Response 200 | `businessCode=DESIGN_RESOURCE_RETRIEVED`; `data` là mảng phẳng. Mỗi item có `id:int64`, `course_id:int64`, `content_type:string`, `title:string`, `payload:object`, `status:string`, `parent_id?:int64`, `order:int32`. Root có `parent_id=null` bị omit. Empty tree vẫn 200 với `data: []`. |
| Mapping guard | Payload phải là JSON object; ID phải unique; mọi parent phải nằm trong response; course ID phải khớp; cycle/invalid projection làm hỏng toàn response. |
| Errors | 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 404 `DESIGN_RESOURCE_NOT_FOUND`; 500 `DESIGN_INTERNAL_ERROR`. SQL/projection/tree detail không trả cho client. |
| Giới hạn dùng cho ME-03 | Flat Content nodes không tự chứng minh cấu trúc `chapter/module/lesson`. `content_type`, `status`, payload subtype, revision và publish rules chưa chốt. Không suy số bài giảng đã duyệt từ status mẫu. |

### Trích từ DD nguồn: 2.2 API #65 — tiến độ toàn lớp

| Thành phần | Catalog trực tiếp | Current source cục bộ |
|---|---|---|
| Route | `GET /api/v1/mentor/courses/{course_id}/progress` | Đã đăng ký tại router và gọi module #65. |
| Auth/input | Bearer JWT, role Mentor; `course_id:int64!`; không query/body. | Shared Mentor guard; signed-int64 parser; direct owner check. |
| Response | `ApiEnvelope<Page<Course>>` theo [catalog #65](../../../../../docs/lists/list_api.md#L175). | `ApiEnvelope<Page<MentorStudentProgress>>`; local shape là DERIVED và đang DISCREPANCY. |
| Roster | Không có progress schema trong `Page<Course>`. | Distinct Student thuộc enrollment ACTIVE; người dùng phải có role `STUDENT`. Một item/Student. |
| Denominator | Không có lesson/progress rule trong catalog. | Chỉ `lessons.status='PUBLISHED'`; chọn progress row mới nhất theo `last_accessed_at DESC NULLS LAST, id DESC`. |
| Tính toán | Chưa định nghĩa. | `completed_lessons` đếm status `COMPLETED`; `progress_percent = floor(sum(progress_percent)/total_published_lessons)`. Không có lesson thì bằng 0. Missing row/percent được tính 0; projection với status/range không hợp lệ trả safe 500. |
| Pagination | Catalog không khai báo page/size input. | Trả toàn bộ roster: `page=1`, `size=total`, `total=total`, `total_pages=1` khi có item, nếu rỗng thì `size=0`, `total_pages=0`. Không có bound. |
| Errors | 401/403/404/500 theo catalog. | Cùng status/business code; direct-owner mismatch 403, course/path không tồn tại/sai 404. |
| Giới hạn dùng cho ME-03 | Catalog chưa biểu diễn tiến độ. | Course-wide theo từng Student; không có tiến độ từng module, event feed, risk flag, quiz/lab score, review/rating hoặc thời điểm gần nhất. Response, eligibility, formula và full-roster page phải chờ owner/schema approval. |

API #65 và API #49 cùng dùng legacy BIGINT source artifacts; DDL/migrations đã kiểm tra tĩnh, live schema/deployment chưa xác minh. `#65` không gọi `#66`/`#67` phía server. AC-26 liệt kê #65, #67, #66 cho class progress, selected-Student detail và analytics riêng; inventory ME-03 chỉ chỉ định #65.

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/04_mentor/ME-03_workspace-khoa-hoc-cua-mentor/ME-03.md)
