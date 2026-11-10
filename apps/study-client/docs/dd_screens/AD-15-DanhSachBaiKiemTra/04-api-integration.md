# AD-15 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `AD-15-API-001` | #87 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #87
- Orchestration/data notes: Candidate GET #87; catalog `ApiEnvelope<Quiz>` khác local `ApiEnvelope<Page<Quiz>>`; local fields thiếu code/course title/question count/status, không có search, course cần int64, status exact raw.
- BE/source status và gate: **R** local #87 route/module/query/model/test source; API DD Draft. **DD BLOCKED; IMPLEMENTATION BLOCKED:** response cardinality/projection, search/course/status mapping, AC-35 permission vs `ADMIN`, legacy BIGINT vs V1-PILOT UUID/live schema, Study Web UNWIRED; **RUNTIME NOT VERIFIED**
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: API #87 — contract đối chiếu

| Thành phần | Catalog/API DD trực tiếp | Local source #87 | Quyết định cho AD-15 |
|---|---|---|---|
| Request | `GET /api/v1/admin/quizzes`; Bearer JWT/Admin; query tùy chọn `course:int64`, `status:string`, `page:int32`; không body. | Route chuyển raw query đến module. Shared `ADMIN` guard chạy trước query validation và truy vấn DB. | Chỉ các query có nguồn và mapping được owner xác nhận mới được gửi. Không tự thêm search/code/size/sort. |
| Response | Catalog khai báo `ApiEnvelope<Quiz>`; API DD #87 còn `Draft — Needs Confirmation`. | Envelope thành công gồm `success`, `businessCode`, `message`, `data`, `meta`, `traceId`; `data` là `Page<Quiz>` với `items` và `pagination`. `businessCode=DESIGN_RESOURCE_RETRIEVED`; message phụ thuộc có item hay rỗng. | Cardinality catalog/AC và source chưa thống nhất; client không được chốt mapping list trước khi có quyết định. |
| Local query | Không nêu page size/default/order hay status enum trong catalog. | `course` là signed int64; `page` signed int32 >=1, mặc định 1; `status` giữ nguyên chuỗi; count và list dùng cùng exact filters; loại `DELETED`; size cố định 20; `id ASC`; không commit. | Đây là hành vi local source, chưa được coi là API contract đã duyệt. |
| Local projection | Catalog gọi kiểu `Quiz` nhưng chưa giải quyết yêu cầu page/list. | Mỗi item có `id`, `course_id`, `title`, nullable `duration_minutes`, `passing_score` dạng decimal string, `questions=[]`. | Không có quiz code, course title, question count, status; không suy ra các giá trị này. |
| Lỗi | Catalog: 401/403/500. | 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, lỗi query/projection 500 `DESIGN_INTERNAL_ERROR`; invalid `course`/`page` local trả 422 `DESIGN_VALIDATION_ERROR` trước DB. | 422 là local derived behavior chưa có trong catalog; UI mapping vẫn chờ contract. |
| Empty/page | Catalog không quy định chi tiết. | Empty hoặc page vượt tổng trả 200; `total_pages=0` khi total=0; message `No quizzes found.` | Không đồng nhất `0/0` của prototype với trạng thái lỗi hoặc “chưa đồng bộ”. |

### Trích từ DD nguồn: Nguồn truy vết chính

- `apps/study-client/docs/list_screen.md` row 73, §8.1 và reverse index #087.
- AC-35: `apps/study-server/docs/diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio` và `apps/study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md`.
- API catalog: `docs/lists/list_api.md`, API #87. API DD #87 hiện `Draft — Needs Confirmation`.
- Local API: `apps/study-server/app/api/v1.py`; `apps/study-server/app/modules/admin/api_87_admin_quizzes_list/` (view, models, query, validate) và `apps/study-server/tests/modules/admin/api_87_admin_quizzes_list/test_admin_quizzes_list.py`.
- Candidate schema: `infra/postgres/study-server/DB.sql`; source này không xác nhận live schema/deployment. Study Web design target: `.agents/web-study/design.md`.

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/05_admin/AD-15_danh-sach-bai-kiem-tra/AD-15.md)
