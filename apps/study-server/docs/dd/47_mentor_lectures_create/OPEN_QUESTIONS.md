# Open Questions — API #47 Tạo lecture

Trạng thái: API decision đã chốt cho implementation local. DD vẫn `Draft — Needs Confirmation` đến khi xác nhận target schema/migration trên live database.

| ID | Câu hỏi | Bằng chứng hiện có | Ảnh hưởng | Trạng thái |
|---|---|---|---|---|
| Q1 | `content:int64` được chuyển thành kiểu nào khi lưu/trả? | Người dùng chốt request giữ int64, lưu `str(content)` trong `lessons.content TEXT` và response `content:string`; test HTTP xác minh giá trị thập phân. | Request, persistence và response mapping. | RESOLVED_BY_USER; SOURCE_BACKED |
| Q2 | `asset_refs` wire key/format và order là gì? | JSON string chứa ordered array signed int64 IDs; `[]` hợp lệ; duplicate reject; response giữ request order. | Parse, query và response assets. | RESOLVED_BY_USER; SOURCE_BACKED |
| Q3 | API #34 lưu metadata UploadAsset ở đâu? | Source API #34 và migration artifact dùng BIGINT `uploads`, status `UPLOADED`; live DB chưa xác minh. | API #47 metadata resolver. | SOURCE_BACKED; LIVE_SCHEMA_NOT_VERIFIED |
| Q4 | API #47 có ghi `resources` hoặc thay đổi `uploads` không? | Người dùng chốt chỉ resolve `uploads` metadata, không ghi resources hoặc mutate uploads. | Asset persistence boundary. | RESOLVED_BY_USER; SOURCE_BACKED |
| Q5 | Mentor được phân công course có được tạo lecture không? | Người dùng chốt chỉ Mentor trực tiếp sở hữu course qua `courses.mentor_id`; không dùng assignment relation. | Authorization và course lookup. | RESOLVED_BY_USER; SOURCE_BACKED |
| Q6 | JWT Mentor principal được map vào owner thế nào? | Shared access-JWT guard xác minh role `MENTOR` và trả numeric user ID; API #46 cùng dùng `courses.mentor_id`. | Bind owner query. | SOURCE_BACKED |
| Q7 | Target schema đang chạy là legacy BIGINT hay V1-PILOT UUID/versioned? | Legacy `DB.sql`/migration 004 có `courses`, `lessons`, `uploads` BIGINT; V1-PILOT khác cấu trúc; không có live metadata trong task. | Runtime database compatibility/deployment. | NOT_VERIFIED; KEEPS_DD_DRAFT |
| Q8 | Lesson mới dùng trạng thái nào? | Người dùng chốt `PUBLISHED`; source INSERT ghi trạng thái tường minh và response lấy từ returned row. | INSERT và response. | RESOLVED_BY_USER; SOURCE_BACKED |
| Q9 | Course cần status cụ thể không? | Người dùng chốt không lọc status; test xác minh course `DRAFT` được phép nếu thuộc Mentor. | Predicate/validation. | RESOLVED_BY_USER; SOURCE_BACKED |
| Q10 | Response `content` có thể null/omit không? | Request content là required signed int64; runtime chuyển thành decimal string và response model yêu cầu string. | Response nullability. | RESOLVED_BY_USER; SOURCE_BACKED |
| Q11 | Timestamp có timezone semantics nào? | Runtime truyền `CURRENT_TIMESTAMP` cho cả hai cột bắt buộc theo legacy DDL; live database/session timezone chưa kiểm tra. | Database timestamp interpretation. | SOURCE_BACKED_EXPRESSION; LIVE_BEHAVIOR_NOT_VERIFIED |
| Q12 | Error envelope dùng `data:null` hay object rỗng? | `app.core.responses.error_response` hiện serialize `data:null`; API #47 dùng helper hiện hành. | Error response shape. | SOURCE_BACKED |
| Q13 | Asset thiếu/ngoài scope map về lỗi nào? | Người dùng chốt cùng generic 404; source trả `DESIGN_RESOURCE_NOT_FOUND` và không phân biệt nguyên nhân. | Asset enumeration/privacy behavior. | RESOLVED_BY_USER; SOURCE_BACKED |

## Remaining verification boundary

- Không còn quyết định nghiệp vụ/API nào chặn implementation local.
- Live schema, migration application và runtime database behavior chưa được kiểm tra; tài liệu vẫn ở trạng thái Draft.
- Các test dùng fake DB session/query và không chứng minh schema hoặc deployment trên môi trường thật.
