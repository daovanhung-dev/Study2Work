# ME-17 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `ME-17-API-001` | #67 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #67
- Orchestration/data notes: Chỉ gọi #67 với course_id + student_id numeric sau khi ME-16 handoff được chốt; không gộp #65/#66. Catalog ApiEnvelope<Page<Course>> khác local ApiEnvelope<StudentCourseProgress>; AC-26 đặt #66 trước chọn Student/#67, khác inventory; loaded timeline và mockup metrics chưa có field mapping.
- BE/source status và gate: **R**; #67 route/module/query/model/focused test source có local implementation. **DD BLOCKED; IMPLEMENTATION BLOCKED:** catalog/local response mismatch, AC-26 ordering, selected-row carrier, loaded timeline/metrics, owner/ACTIVE-roster/privacy and live-schema confirmation; Study Web UNWIRED; RUNTIME NOT VERIFIED
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: B2. Current API #67 source flow

1. GET route nhận raw course_id, student_id và Authorization header. OpenAPI khai báo hai path parameter bắt buộc signed int64; không có query/body/page-size.
2. Shared Bearer/JWT guard yêu cầu role MENTOR trước DB.
3. Validator parse cả hai ID thành signed int64. Giá trị malformed hoặc ngoài range trả 404 DESIGN_RESOURCE_NOT_FOUND.
4. Query kiểm course trước. Course không tồn tại trả 404; course không thuộc direct owner trả 403 DESIGN_ACCESS_DENIED.
5. Student phải có users.role=STUDENT và ACTIVE enrollment trong course; nếu không thì 404 DESIGN_RESOURCE_NOT_FOUND.
6. Query lấy lesson PUBLISHED theo sort_order ASC, id ASC. Khi có duplicate progress rows cho cùng user/lesson, giữ row có last_accessed_at DESC NULLS LAST, tie-break id DESC.
7. Lesson không có row progress được chiếu thành NOT_STARTED, percent 0, timestamps null. Model/view chấp nhận progress_status NOT_STARTED, IN_PROGRESS hoặc COMPLETED. Summary gồm completed_lesson count, số PUBLISHED lessons và floor(sum(progress_percent)/total lessons); mẫu số 0 cho percent 0.
8. Success source trả ApiEnvelope<StudentCourseProgress> với course_id; student{id,full_name,avatar_url}; summary{completed_lessons,total_lessons,progress_percent}; lessons[]{lesson_id,title,order,progress_status,progress_percent,last_accessed_at,completed_at}. Không có pagination hoặc DB write.
9. Local errors: 401 DESIGN_AUTHENTICATION_REQUIRED, 403 DESIGN_ACCESS_DENIED, 404 DESIGN_RESOURCE_NOT_FOUND, 500 DESIGN_INTERNAL_ERROR. Error body dùng envelope an toàn/data null theo local source.
10. Đọc test source cho thấy fake DB cases cho auth, IDs, owner/roster, empty curriculum, projection/error/OpenAPI/trace; test chưa chạy. Đây không phải bằng chứng live DB/deployment.

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/04_mentor/ME-17_tien-do-tung-hoc-vien/ME-17.md)
