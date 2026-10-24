# Báo cáo kiểm chứng — API #77

- DD status: `Draft — Needs Confirmation`.
- Endpoint: `DELETE /api/v1/admin/courses/{course_id}`.
- Runtime status: `UNWIRED / NOT_FOUND` — route, module, Admin guard và focused test không có trong Study source.
- Direct contract: Bearer/Admin; `course_id:int64!`; không body/query; `ApiEnvelope<DeleteResult>`; HTTP 200 `DESIGN_RESOURCE_DELETED`; đúng năm error code catalog 401/403/404/422/500.
- DeleteResult fields: `id:int64`, `status:"deleted"`, `deleted_at:date-time`. Field `deleted_at` direct trong schema nhưng persistence source chưa xác định.
- Derived proposals: dependency block có thể trả catalog 422; dependency check + soft-delete transaction; visibility sau delete. Không chọn blocker set, physical marker, audit, repeat-delete/idempotency hoặc hard delete.
- Application tests: `NOT_RUN` — docs-only.

## Kiểm tra

| Check | Kết quả | Trạng thái |
|---|---|---|
| Worklog preflight | Deno selector chọn #48/#49/#50; cả ba worklog được đọc đầy đủ trước khi inspect sâu. | PASS |
| Plan trước folder | Requirement, Request Usage, Query, Mutation và Response Source matrices được ghi trong worklog trước authoring. | PASS |
| Catalog/diagram/source/schema | API #77/reusable DeleteResult, toàn bộ flow AC-32, current router/auth/middleware/response helpers và legacy/pilot DDL được đối chiếu. | PASS — STATIC |
| Direct contract/error set | DELETE path/auth/path/no-body/no-query/response/status được giữ; success + đúng 401/403/404/422/500 codes, không thêm code. | PASS |
| DeleteResult/mutation coverage | Cả ba response fields có mapping/gap; soft-delete intent tách khỏi physical persistence; không bịa column/cascade/audit. | PASS_WITH_OPEN_QUESTIONS |
| Exact package | Đúng 11 Markdown files: 8 template sheets + `OPEN_QUESTIONS.md`, `PLAN_RESULT.md`, `VERIFICATION_REPORT.md`; không có ZIP. | PASS — STATIC |
| Template appendices | 8/8 sheet có front matter và appendix suffix byte-match registered template. | PASS — STATIC |
| JSON/tables/fences | 2/2 JSON examples parse; 28 bảng và 7 code fences trong 8 core sheets được kiểm tra cấu trúc. | PASS — STATIC |
| Links/anchors/whitespace | 36 local Markdown links và 19 anchors trong package DD được kiểm tra; links resolve; newline cuối file có mặt; không trailing whitespace. | PASS — STATIC |
| Output fingerprints | Template pack và DD payload SHA-256 được ghi bên dưới. | RECORDED |
| AC-32 macro-review | Đã rà tài liệu #73–#77 và cập nhật Open Questions, Plan, Verification Report cùng worklogs. Các policy/schema/auth gaps vẫn được giữ mở. | COMPLETED_WITH_OPEN_QUESTIONS |
| Application tests | Không chạy; docs-only. | NOT_RUN |
| Context validator | Không sửa context page hoặc registry. | NOT_APPLICABLE |

## Kết quả macro-review AC-32 #73–#77

- Ranh giới chức năng: #73 list/filter; #74 detail; #75 metadata-only update; #76 status update + audit intent theo diagram; #77 soft-delete theo policy. Không đưa status/audit vào #75 hoặc #77, không hard-delete/cascade.
- Giữ response theo catalog: #73–#76 dùng `Page<Course>`; #77 dùng `DeleteResult`. Singleton Page cho #74–#76 và body của #75/#76 là proposal, không phải contract mới.
- Flow nhắc counters cho #74 nhưng Course contract không định nghĩa counter fields; category relation của #73–#75 cũng chưa có source. Không thêm field, query hoặc relation.
- Nếu #77 thành công, ẩn khỏi #73/#74 và từ chối/định nghĩa rõ #75/#76 trên deleted target là policy cần owner chốt; physical marker/filter hiện chưa xác định.
- Shared unresolved items: Admin/course-management guard, CourseStatus casing, legacy BIGINT vs V1-PILOT UUID model, audit persistence của #76, delete dependency/timestamp source, dynamic middleware path mapping và error `data:null` guideline so với helper `{}`.
- Đây là static document review. Nó không xác minh route/runtime, Admin permission, live DB/schema, audit persistence hoặc physical soft-delete.

## Fingerprints

| Fingerprint | Phạm vi | SHA-256 |
|---|---|---|
| Registered template pack | 8 template filenames đã sort + NUL + raw bytes + NUL | `3dc7fd2242dd1ed1bd9faba50aadad913a31b97ebf1392d6144bb905c5208137` |
| DD output payload | 8 sheets + `OPEN_QUESTIONS.md` + `PLAN_RESULT.md`; loại report này khỏi digest để tránh self-reference; cùng thuật toán | `500d56e1b57c70bd877f6122e0c9da5d6dff5b724652144c8452f293744c3615` |

## Giới hạn kết luận

Static verification xác nhận tính nhất quán của DD với catalog, AC-32 và source artifacts đã đọc. Nó không chứng minh chính sách xóa, Admin authorization, live schema, endpoint runtime hoặc database mutation.
