# PLAN_RESULT — Study API #62

## Trạng thái kế hoạch

- Kế hoạch và các ma trận request/query/mutation/response đã được ghi trong worklog trước khi tạo thư mục DD.
- API: #62 — Lấy tập người nhận; trạng thái `Draft — Needs Confirmation`.
- Giao phẩm Study: 8 sheets và 3 report Markdown; không tạo ZIP.

## Danh mục nguồn

| Nguồn | Bằng chứng sử dụng | Trạng thái |
|---|---|---|
| Catalog #62 | GET path, Bearer Mentor, course_id int64, Page<Course>, 200 và đúng 401/403/404/500 | DIRECT |
| Reusable schemas | Page/PageMeta/Course/Category/Enrollment/UserSummary | Shape DIRECT; enum/status còn thiếu |
| AC/API index và diagram AC25 | Đọc active enrollments → chọn người nhận → #63 notification → #64 trạng thái gửi | DIRECT; predicate/projection còn mở |
| Legacy guide và DDL | courses/users/enrollments BIGINT; status VARCHAR default ACTIVE; DDL cho phép FK NULL | Candidate; chưa có live proof; guide và DDL lệch nhau |
| V1-PILOT DDL | courses/course_versions/course_enrollments/learner_profiles UUID; enrollment enum khác | Candidate; model và ID không tương thích |
| Router/modules/tests hiện tại | Không có route/module/test #62 | `UNWIRED / NOT_FOUND` |
| Auth/response/middleware hiện tại | Guard Student-only; helper trả `{}` khi data lỗi vắng; path chưa allowlist | Source dùng chung; discrepancy khi wiring sau này |
| DD #46/#54/#61 | Tham khảo owner/Page, gap pagination và package gần nhất | Chỉ làm precedent, không thay contract #62 |

## API Requirement Matrix

| API ID | Method/path | Auth | Request | Success | Errors | Bằng chứng |
|---|---|---|---|---|---|---|
| #62 | `GET /api/v1/mentor/courses/{course_id}/students` | Bearer JWT; Mentor | `course_id:int64!`; không query/body | 200 `DESIGN_RESOURCE_RETRIEVED`; `ApiEnvelope<Page<Course>>` | 401 authentication required; 403 access denied; 404 not found; 500 internal error | Catalog DIRECT; ý nghĩa roster còn xung đột |

## Luồng AC-25 và ranh giới API

```text
Mentor chọn course → #62 đọc active enrollments → UI chọn người nhận
→ #63 thêm Notification + recipients và gọi Push/Email
→ #64 đọc trạng thái gửi
```

#62 chỉ đọc. API #63 nhận `recipients:string!` nhưng không quy định ID/encoding; #62 không tự chọn cách serialize để bàn giao.

## Ma trận và quyết định mapping

| Ma trận | Kết quả |
|---|---|
| Request Usage | Bearer Mentor principal giới hạn course_id int64; không body/query; không thêm page/size. |
| Query | Q1 kiểm tra course/scope theo legacy candidate; Q2 đọc active enrollment qua users; Q3 chỉ đếm unique nếu response recipient/pagination được duyệt. |
| Mutation | N/A — chỉ đọc; #63 sở hữu ghi Notification/recipients và gửi đi. |
| Response Source | Giữ `Page<Course>` theo catalog nhưng không biểu diễn học viên; `Page<UserSummary>` là đề xuất cần owner/catalog duyệt; PageMeta chưa có pagination input. |

## Discrepancy và blocker

- `Page<Course>` trong catalog lệch endpoint `/students` và AC-25 recipient flow: `DISCREPANCY`; không tạo Course mapping giả.
- PageMeta nhưng request không có page/size: `SOURCE_REQUIRED`; default/order/grain đếm chưa biết.
- Legacy BIGINT enrollment khác V1-PILOT UUID/versioned enrollment; live schema chưa xác minh.
- Active status, duplicate recipient, Mentor claim/assignment và privacy rule cần xác nhận.
- API #63 `recipients:string!` chưa có encoding.
- Guideline yêu cầu error `data:null`, helper hiện tại trả `{}`; route #62 chưa allowlist và chưa wired.

## Fingerprint template

| Template | SHA-256 |
|---|---|
| `00_Cover.md` | `fd5f568c5329d3069fbaff617a6f4ed3b5ffaf050e042c95b7c9100a05f79e63` |
| `01_Lich_su.md` | `d1cec6573433a9551812bf47552f8a44d7c533d790341941047c410e1d57771e` |
| `02_Overview.md` | `c2879c2f0e007395558dfee4167484786c5aadb3fdd63ab135ca111e7c5f8aa6` |
| `03_Request.md` | `37aaa1e9d7f3e83329e81ab38d922c9dff959284d5b7b3ae353878798dd4b7aa` |
| `04_Response.md` | `5bcb43ba5eb487302dd5d5efde4383b9f452f9fed2149f55315d64ff78a19ab8` |
| `05_Data_Mapping.md` | `11bc77bc0522d3af27b9499114991c8819046ac32bde5c1efdc841be088dcc5b` |
| `06_Error.md` | `e0160ea07fdbc74f2cafebd6ed3b21e60029662d28d67f5f6a0b4d95ba72be9b` |
| `07_table.md` | `4c9a0e037872333210aaf44ba9fbf00a0e63343a69d55250e537d2c3c5e2d356` |

## Cổng kế hoạch

- Contract catalog được giữ nguyên trong Requirement Matrix: PASS.
- Luồng AC-25 và ranh giới chỉ đọc được truy vết: PASS.
- Candidate được tách khỏi nguồn đã xác nhận: PASS.
- Bốn ma trận được ghi trước khi tạo DD: PASS.
- Open question được ghi trước khi kết luận sẵn sàng triển khai: PASS.
