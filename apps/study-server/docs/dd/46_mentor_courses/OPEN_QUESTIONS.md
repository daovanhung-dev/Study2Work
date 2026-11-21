# Open Questions — API #46

Trạng thái tài liệu: `Draft — Needs Confirmation`. Các câu hỏi sau chặn việc coi candidate mapping là implementation contract.

| ID | Câu hỏi | Bằng chứng hiện có | Ảnh hưởng | Trạng thái |
|---|---|---|---|---|
| Q1 | Schema course thực tế là legacy BIGINT hay V1-PILOT UUID/versioned owner? | Hai DDL khác nhau; live schema chưa xác minh. | ID binding, join và response. | `SOURCE_REQUIRED` |
| Q2 | “Course được quản lý” gồm course do Mentor sở hữu, được phân công, hay cả hai? | AC-21 nói owns/assigned; legacy DDL chỉ có `mentor_id`; không thấy assignment relation. | Q1/Q2 predicate và API #47 authorization. | `NEEDS_CONFIRMATION` |
| Q3 | JWT Mentor principal có numeric `users.id` hay UUID subject? | Current Study helper hỗ trợ JWT source shape nhưng guard Student-specific; pilot schema dùng UUID subject. | `mentor_id` binding/identity. | `DISCREPANCY` |
| Q4 | Các member hợp lệ của `CourseStatus` là gì? Có cho phép status NULL không? | Catalog chỉ nêu type; legacy DDL cho phép NULL; runtime Course model không có enum. | Query validation và response mapping. | `SOURCE_REQUIRED` |
| Q5 | Nếu `price`, `status`, `mentor_id` hoặc joined Mentor field NULL/missing, API phải 500, bỏ course hay sửa schema? | Legacy DDL nullable; Course/UserSummary yêu cầu các field chính. | Record integrity và count/page consistency. | `NEEDS_CONFIRMATION` |
| Q6 | Khi không có category relation, API có tiếp tục omit optional `Course.category` không? | API #6 precedent omit; catalog đánh dấu category optional. | Response projection. | `DERIVED` |
| Q7 | `page >= 1`, `size` range 1..100 và sort `created_at DESC, id ASC` có được áp dụng như API #6 không? | API #46 chỉ định default page=1,size=20; không có max/sort contract. | 422 behavior, ordering và pagination. | `DERIVED / NEEDS_CONFIRMATION` |
| Q8 | Course.status có predicate nào mặc định (ví dụ mọi trạng thái hay chỉ một số trạng thái)? | AC-21 là Mentor management; API #46 có filter status; API #6 public route chỉ PUBLISHED. | Danh sách course Mentor có thể chọn. | `NEEDS_CONFIRMATION` |
| Q9 | Error envelope thực tế phải dùng `data:null` theo guideline hay `{}` theo helper hiện tại? | `contracts/api-guidelines` và `app/core/responses.py` khác nhau. | Expected/current response contract. | `DISCREPANCY` |
| Q10 | Course được phân công có dùng cùng một access rule cho #46/#47/#48 và được biểu diễn bằng relation nào? | AC-21 nối #46 → #47 → #48; macro-review thấy cả ba DD dùng cùng direct-owner candidate, nhưng không có assignment relation nguồn. | Nhất quán authorization xuyên suốt AC-21; candidate chưa hỗ trợ assigned course. | `SOURCE_REQUIRED` |
| Q11 | Live DB có index/query constraints phù hợp cho owner/status/page không? | Chỉ có DDL artifact; live DB và query plan chưa kiểm tra. | Hiệu năng và rollout. | `NOT_VERIFIED` |

## Cách xử lý trong DD

- Giữ candidate `courses.mentor_id = current numeric Mentor ID` ở nhãn `DERIVED`; không dùng làm xác nhận assignment semantics.
- Không hợp nhất legacy `courses` với pilot `course_versions`.
- Không tạo enum values, assignment table, category relation, migration hoặc runtime behavior từ suy luận.
- Các defaults `page=1`, `size=20` giữ theo catalog; mọi giới hạn và sort ngoài đó cần owner xác nhận.

