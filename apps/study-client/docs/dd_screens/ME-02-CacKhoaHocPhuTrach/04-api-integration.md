# ME-02 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `ME-02-API-001` | #46 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #46
- Orchestration/data notes: GET #46; mentor chỉ thao tác course hợp quyền từ server, không tự suy ownership ở client.
- BE/source status và gate: **D**
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: 5. API contract và response mapping

### API #46 — `GET /api/v1/mentor/courses`

| Thuộc tính | Current source |
|---|---|
| Authentication | Header `Authorization: Bearer <JWT>`; shared `validate_current_user_request(..., role="MENTOR")`. Missing/invalid token → 401; valid token without MENTOR role → 403, trước DB query. JWT `sub` hiện được parse thành numeric user ID dương. |
| Query | `status?: string` enum source `DRAFT|PUBLISHED`; `page?: int` default 1/min 1; `size?: int` default 20/min 1/max 100. No request body. |
| Query effect | `status` absent → no status predicate; provided → exact equality. Both count/page predicate direct `courses.mentor_id = :mentor_id`. Fixed order `created_at DESC, id ASC`; limit/offset from page/size. GET read-only. |
| Success | HTTP 200, `businessCode=DESIGN_RESOURCE_RETRIEVED`, envelope `success/businessCode/message/data/meta/traceId`. Empty page message “No courses found.”; data still `items:[]` plus pagination. |
| `data.items[]` | `id:int`, `title:string`, `description?:string|null`, `thumbnail_url?:string|null`, `price:decimal string`, `status:string` (current output constrained to DRAFT/PUBLISHED), `mentor:{id:int, full_name:string, avatar_url?:string|null}`. No `course_code`, level/category, rating, count or progress fields. |
| `data.pagination` | `page`, `size`, `total`, `total_pages`; `total_pages=0` if total=0. Out-of-range page may have `items=[]` while `total` remains positive. |
| Errors | 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 422 `DESIGN_VALIDATION_ERROR` for status/page/size; 500 `DESIGN_INTERNAL_ERROR` for DB/integrity/mapping failures. Trace ID is preserved by shared response helpers. |

#### Response-to-UI allowlist

| API field | UI use | Restriction |
|---|---|---|
| `id` | Route context for card actions, only after destination approval. | Do not display as course code without product definition. |
| `title` | Course heading. | Text sample replaced by current field after success. |
| `description` | Supporting text. | Nullable; fallback/truncation rules need UI design. |
| `thumbnail_url` | Course image. | Nullable URL; loading/failed-image state not designed. HTML remote image URLs are sample assets. |
| `status` | Raw status text or approved translation. | Do not map to active/upcoming/archived without approved mapping. |
| `price` | Not visibly required by screenshot. | Preserve decimal string if later displayed; no currency symbol/currency field supplied. |
| `mentor` | Not needed within each owned course card. | Does not provide Mentor job title, availability or profile record. |
| `pagination.*` | Result count/page controls/page-size state. | Count reflects current direct-owner/status query; it does not mean “eligible/assigned/active” until scope is resolved. |

### API #62/#65/#66 — not part of ME-02 request orchestration

These source-backed routes are listed only to trace possible visible metrics/CTA destinations. Their existence does not authorize new calls from ME-02. #62 returns active Student summaries for one direct-owner course; #65 returns per-Student progress for one direct-owner course; #66 returns activity proxy for one direct-owner course. They do not supply sample ratings, Capstone status, course codes, course-level completion average, lecture/lab counters or global report output. Current `list_api.md` still lists #65/#66 as `ApiEnvelope<Page<Course>>`, which differs from current route/module response models; document that discrepancy at the downstream screen/API owner before relying on those fields.

### Trích từ DD nguồn: Source trace — API #46

```text
GET /api/v1/mentor/courses
  -> apps/study-server/app/api/v1.py:mentor_courses
  -> MentorCourseQuery(status, page, size)
  -> app.modules.mentor.api_46_mentor_courses.view.get_mentor_courses
  -> validate_current_user_request(role="MENTOR")
  -> validate status DRAFT|PUBLISHED, page>=1, size 1..100
  -> count_owned_courses / find_owned_courses
       -> COUNT + LIST SQL; courses.mentor_id = JWT sub; optional exact status
       -> LEFT JOIN users; ORDER BY created_at DESC, id ASC; LIMIT/OFFSET
  -> map_course -> CoursePage(items, pagination)
  -> ApiEnvelope success DESIGN_RESOURCE_RETRIEVED or safe error response
  -> test source covers auth/query/page/empty/error branches (read, not run)
```

`find_owned_courses` và `count_owned_courses` dùng cùng direct-owner predicate và status nếu có. GET không ghi dữ liệu, không commit và không có external side effect. Query/status validation diễn ra sau auth guard; sai role trả 403 trước query. Test source dùng fake DB session/rows, vì vậy không xác minh live schema, deployment hay PostgreSQL query execution. DB context ghi live schema là `NOT_VERIFIED`.

### Trích từ DD nguồn: API liên quan tới các chỉ số trong mockup

- **#62 `GET /api/v1/mentor/courses/{course_id}/students`:** current source kiểm tra trực tiếp `courses.mentor_id`, rồi trả danh sách `StudentSummary` distinct từ enrollment `ACTIVE`; response không có aggregate total, không pagination. Không chứng minh KPI tổng học viên toàn bộ course hoặc dedup giữa các course.
- **#65 `GET /api/v1/mentor/courses/{course_id}/progress`:** current source trả một row cho mỗi active Student gồm `completed_lessons`, `total_lessons`, `progress_percent` theo lesson `PUBLISHED`. `progress_percent` là per-Student; contract source không trả average course completion. Tự average/dedup thêm ở ME-02 chưa được duyệt.
- **#66 `GET /api/v1/mentor/courses/{course_id}/analytics`:** current source trả `tracked_lesson_accesses`, `students_with_activity`, `last_activity_at`; đây là activity proxy, không phải rating, Capstone pass rate hay completion KPI. API catalog/DD snapshot còn mô tả #65/#66 response là `Page<Course>`, khác model runtime source.
- Các API trên cần `course_id`; chúng không nằm trong API list của ME-02 row ngoại trừ CTA/ME-16 handoff. Không gọi chúng để tạo KPI mới nếu màn hình/API orchestration chưa được phê duyệt.

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/04_mentor/ME-02_cac-khoa-hoc-phu-trach/ME-02.md)
