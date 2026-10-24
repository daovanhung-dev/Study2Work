# Plan Result — API #46

## Kết quả

Đã lập DD thiết kế cho `GET /api/v1/mentor/courses` theo contract catalog và flow AC-21. Tài liệu giữ riêng expected contract, candidate mapping, current source và các quyết định chưa có nguồn. API vẫn `UNWIRED / NOT_FOUND`; không có thay đổi runtime, catalog, DB hay diagram.

## API Requirement Matrix

| API ID | Method / endpoint | Actor/auth | Request field | Response/status | Basis |
|---|---|---|---|---|---|
| #46 | GET /api/v1/mentor/courses | Mentor / Bearer JWT | Authorization | `ApiEnvelope<Page<Course>>`; 200; errors 401/403/422/500 đúng catalog | Catalog + AC-21 |
| #46 | GET /api/v1/mentor/courses | Mentor / Bearer JWT | `status?:CourseStatus` | Giữ nguyên response/status | Catalog |
| #46 | GET /api/v1/mentor/courses | Mentor / Bearer JWT | `page?:int32=1` | Giữ nguyên response/status | Catalog |
| #46 | GET /api/v1/mentor/courses | Mentor / Bearer JWT | `size?:int32=20` | Giữ nguyên response/status | Catalog |

## Request Usage Matrix

| Request field | Source | Validation/use | Response use | Evidence/gap |
|---|---|---|---|---|
| Authorization | HTTP header | Xác thực Bearer/JWT và role Mentor; principal không lấy từ query | Scope Q1/Q2 | Contract direct; Mentor guard chưa có trong current helper. |
| `status` | Query | Nếu có, thêm equality predicate; member list chưa biết | Lọc `Course.status` | Field direct; enum `SOURCE_REQUIRED`. |
| `page` | Query hoặc default 1 | Đề xuất int32 `>=1` | `PageMeta.page` và offset | Default direct; range `DERIVED`. |
| `size` | Query hoặc default 20 | Đề xuất int32 `1..100` | `PageMeta.size` và limit | Default direct; max theo API #6 `DERIVED`. |

## Query Matrix

Mỗi output field, predicate, sort key và pagination expression nằm trên một dòng riêng.

| Query | Type | Candidate source | Query item | Rule | Evidence status |
|---|---|---|---|---|---|
| Q1 | SELECT | `courses AS c` | `c.id` | Course ID. | Legacy DDL candidate; pilot UUID conflict. |
| Q1 | SELECT | `courses AS c` | `c.name AS title` | Physical `name` sang logical `title`. | API #6 precedent. |
| Q1 | SELECT | `courses AS c` | `c.description` | Nullable description. | Legacy candidate. |
| Q1 | SELECT | `courses AS c` | `c.thumbnail_url` | Nullable thumbnail. | Legacy candidate. |
| Q1 | SELECT | `courses AS c` | `c.price` | Decimal-string; NULL là integrity gap. | Legacy nullable column. |
| Q1 | SELECT | `courses AS c` | `c.status` | Giữ raw status, enum chưa được định nghĩa. | SOURCE_REQUIRED enum. |
| Q1 | JOIN | `users AS m` | `m.id = c.mentor_id` | Candidate Mentor summary join. | API #6 + legacy DDL; assignment unresolved. |
| Q1 | SELECT | `users AS m` | `m.id` | Required Mentor ID. | API #6 precedent. |
| Q1 | SELECT | `users AS m` | `m.full_name` | Required Mentor name. | API #6 precedent. |
| Q1 | SELECT | `users AS m` | `m.avatar_url` | Optional Mentor avatar. | API #6 precedent. |
| Q1 | WHERE | `courses AS c` | `c.mentor_id = :mentor_id` | Luôn giới hạn candidate direct owner. | DERIVED; assignment relation chưa có. |
| Q1 | WHERE | `courses AS c` | `c.status = :status` | Chỉ thêm khi query status có giá trị. | Filter direct; predicate DERIVED. |
| Q1 | ORDER BY | `courses AS c` | `c.created_at DESC` | Mới nhất trước. | DERIVED theo API #6. |
| Q1 | ORDER BY | `courses AS c` | `c.id ASC` | Tie-breaker ổn định. | DERIVED theo API #6. |
| Q1 | LIMIT | N/A | `:size` | Số item tối đa. | Default direct; max DERIVED. |
| Q1 | OFFSET | N/A | `(:page - 1) * :size` | Chọn trang. | DERIVED. |
| Q2 | COUNT | `courses AS c` | `COUNT(*)` | Đếm cùng scope/predicate như Q1. | API #6 pattern. |
| Q2 | JOIN | `users AS m` | `m.id = c.mentor_id` | Integrity projection check. | API #6 pattern. |
| Q2 | COUNT | `users AS m` | `COUNT(*) FILTER (WHERE m.id IS NULL)` | Phát hiện Mentor projection thiếu. | API #6 precedent. |
| Q2 | WHERE | `courses AS c` | `c.mentor_id = :mentor_id` | Cùng owner predicate với Q1. | DERIVED. |
| Q2 | WHERE | `courses AS c` | `c.status = :status` | Chỉ thêm khi query status có giá trị. | DERIVED. |

## Mutation Matrix

| Operation | Target | Field/condition | Status |
|---|---|---|---|
| INSERT | N/A | Không tạo record | N/A — READ-ONLY API |
| UPDATE | N/A | Không cập nhật record | N/A — READ-ONLY API |
| DELETE | N/A | Không xóa record | N/A — READ-ONLY API |

## Response Source Matrix

| Response field | Contract/source | Candidate mapping | Rule/status |
|---|---|---|---|
| `success` | ApiEnvelope | Branch constant | DIRECT contract. |
| `businessCode` | Catalog | `DESIGN_RESOURCE_RETRIEVED` | DIRECT. |
| `data.items[].id` | Course | `courses.id` | Legacy candidate; UUID pilot conflict. |
| `data.items[].title` | Course | `courses.name` | API #6 precedent. |
| `data.items[].description` | Course? | `courses.description` | Null khi nguồn NULL. |
| `data.items[].thumbnail_url` | Course? | `courses.thumbnail_url` | Null khi nguồn NULL. |
| `data.items[].price` | Course | `courses.price` | Decimal-string; NULL integrity gap. |
| `data.items[].status` | Course | `courses.status` | Enum/source unresolved. |
| `data.items[].mentor.id` | UserSummary | `users.id` | Required projection. |
| `data.items[].mentor.full_name` | UserSummary | `users.full_name` | Required projection. |
| `data.items[].mentor.avatar_url` | UserSummary? | `users.avatar_url` | Null khi nguồn NULL. |
| `data.items[].category` | Course? | No mapping | Omit optional field; category relation absent. |
| `data.pagination.page` | PageMeta | Effective query/default | Default 1 direct. |
| `data.pagination.size` | PageMeta | Effective query/default | Default 20 direct; max DERIVED. |
| `data.pagination.total` | PageMeta | Q2 `COUNT(*)` | Same filters as Q1. |
| `data.pagination.total_pages` | PageMeta | `ceil(total / size)` | 0 if total=0; DERIVED. |
| `meta` | ApiEnvelope | Empty object candidate | Error details unresolved. |
| `traceId` | ApiEnvelope | Request trace | Contract direct; runtime API absent. |

## Phạm vi AC-21 và API liên quan

1. AC-21 gọi API #46 để Mentor xem/chọn course.
2. Sau lựa chọn, flow upload và API #47 tạo lecture.
3. API #48 tải lại lecture mới tạo.
4. #46 read-only; không thay thế validation ownership của #47. #47 cần dùng cùng định nghĩa course scope sau khi owner/assignment được quyết định.
5. Macro-review #46–#48 sau khi DD #48 tồn tại: cùng direct-owner candidate; assignment và Mentor ID mapping còn mở; #48 không lọc PUBLISHED nên có thể đọc candidate DRAFT từ #47; legacy BIGINT và V1-PILOT UUID vẫn tách riêng; assets[] còn SOURCE_REQUIRED từ #34/#47/#48; error envelope discrepancy được giữ nguyên. Chi tiết nằm tại [API #48 PLAN_RESULT](../48_mentor_lecture_detail/PLAN_RESULT.md).

## Source status

- `EXPECTED_BEHAVIOR`: API catalog #46 và AC-21.
- `CURRENT_BEHAVIOR`: router `app/api/v1.py` không khai báo route #46; không có module `view.py` hoặc focused test.
- `DISCREPANCY`: Hai course schema artifacts không tương thích; live schema chưa xác minh.
- Candidate SQL/projection là design proposal, không khẳng định đang chạy.

## Validation plan

- Kiểm tra đủ 8 sheet template và 3 report.
- So sánh API ID, method/path, auth/query fields, response/status/error set với catalog.
- Kiểm tra JSON examples, code fences, Markdown tables và relative links.
- Đối chiếu template appendix; không chạy application tests cho DD-only task.

