# Câu hỏi còn mở — API #74

Trạng thái tài liệu: `Draft — Needs Confirmation`. API #74 đã có local route, module và focused tests. Các fallback bên dưới mô tả source hiện tại; chúng chưa được xem là quyết định product/schema đã duyệt.

## Fallback đã triển khai (`DERIVED`)

- Shared JWT guard yêu cầu role `ADMIN`; chưa có dedicated course-management permission policy.
- Query legacy BIGINT candidate `courses LEFT JOIN users` theo ID; không lọc status, không query counter và không map `category`.
- Response giữ `ApiEnvelope<Page<Course>>` với một item và pagination `1/1/1/1` theo catalog cùng API #08 precedent.
- Malformed/out-of-int64 path ID trả 404; course/mentor/price projection hoặc DB failure trả safe 500 theo catalog.
- Middleware nhận diện dynamic endpoint qua FastAPI route template; `error_response` hiện trả `data:null`.

## Cần chủ sở hữu/schema xác nhận

1. **Admin permission:** Role `ADMIN` có đủ quyền đọc course management hay cần policy/permission riêng? Scope/tenant boundary là gì?
2. **Counters trong AC-32:** Counter nào cần đọc, định nghĩa/cách đếm là gì, và thuộc `Course`, `meta` hay response riêng? Catalog hiện không khai báo trường counter.
3. **Response detail wrapper:** Có giữ `ApiEnvelope<Page<Course>>` singleton hay cập nhật catalog/reusable contract thành `ApiEnvelope<Course>`?
4. **Schema/live DB:** API dùng legacy BIGINT `courses/users` hay V1-PILOT UUID `courses/course_versions`? Migration và live schema chưa được xác minh.
5. **Mentor integrity:** Course thiếu mentor hoặc price thì Admin cần thấy/sửa dữ liệu mồ côi hay nhận 500?
6. **Category mapping:** Có source/schema được duyệt để trả `Course.category` không?
7. **CourseStatus:** Các giá trị hợp lệ và casing là gì? #76, legacy DDL và API #08 chưa thống nhất.
8. **Nullable fields:** `description`, `thumbnail_url`, `mentor.avatar_url` serialize null hay omit theo contract cuối?
9. **Path error boundary:** Giữ fallback malformed/out-of-range int64 → 404 hay catalog cần khai báo 422?
10. **AC-32 macro-review:** Visibility sau soft-delete và cách #75/#76 xử lý deleted target cần thống nhất với #73/#77.

## Ranh giới bằng chứng

- Local route/tests không xác minh deployment, live DB schema/grants hoặc policy ngoài role `ADMIN`.
- Diagram yêu cầu owner/counters nhưng không định nghĩa counter schema; không tự thêm field/query.
- `07_table.md` tiếp tục mô tả mapping schema là candidate, không phải live-schema evidence.
