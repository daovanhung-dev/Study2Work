# Báo cáo kiểm chứng — API #92 Lấy notification list

## Phạm vi và trạng thái

- DD: `apps/study-server/docs/dd/92_admin_notifications_list/`.
- Tài liệu vẫn `Draft — Needs Confirmation`; các câu hỏi về cardinality, schema, permission, filter và phân trang chưa được owner xác nhận.
- API #92 hiện được wire trong local Study source. Các response/schema/permission fallback được đánh dấu `DERIVED`; kiểm thử fake DB không chứng minh live database hoặc deployment.

## Nguồn đã đối chiếu

- Catalog #92 và reusable `Notification`: giữ `GET /api/v1/admin/notifications`, Bearer/Admin, query `status?:string`, `channel?:string`, `page?:int32`, direct `ApiEnvelope<Notification>`, HTTP 200 và errors 401/403/503/500.
- AC-36 index/diagram: #92 query trước các nhánh #93–#96; không định nghĩa list cardinality, filter mapping, pagination hoặc trigger 503.
- DB table guide, ERD, legacy BIGINT DDL và V1-PILOT UUID DDL: hai notification models được giữ riêng; legacy outbox channel/status không được xem là owner-approved Notification enums.
- APIs #63/#64: local notification/outbox write model và aggregate precedence là implementation precedent; Mentor sender ownership không được chuyển sang Admin.
- Study router, middleware, response helper và API Guidelines: route, module, tests, OpenAPI schema và middleware contract path đã được wire cục bộ.

## Template và fingerprint

- Đã dùng đủ tám file trong `.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/`.
- Template manifest SHA-256: `1f327f751e000139cd5174b1de64e074a23ee2e398234828e94c3a398261c4b9` — SHA-256 các dòng `filename:file_sha256`, sắp xếp theo filename.
- Output manifest SHA-256: `51a387d7533ec12e8384a888f80b65e8935784e8cb1a2a8ab6e54ab5c8e82332` — cùng cách tính trên tám sheet, `PLAN_RESULT.md` và `OPEN_QUESTIONS.md`; không đưa report này vào manifest.
- Study giao DD dạng Markdown; không tạo ZIP.

## Kiểm tra DD và source

| Hạng mục | Kết quả | Trạng thái |
|---|---|---|
| Package | 11 file: 8 sheet và 3 report | PASS |
| Template appendix | Tám appendix trùng byte-for-byte với template | PASS — 8/8 |
| Front matter | Tám sheet có `dd_id: 92` và trạng thái Draft | PASS — 8/8 |
| Catalog contract | Method/path/auth/query/response/status và exact error set được giữ | PASS — static |
| Notification projection | Các field reusable `Notification` và envelope được ghi; Page fallback tách khỏi direct contract | PASS — static |
| JSON examples | Cả 3 fenced JSON parse được | PASS — 3/3 |
| Markdown tables/fences | 33 bảng, 449 dòng bảng; 5 code fences cân bằng | PASS — static |
| Relative links/anchors | 23 file/directory links và 5 anchors resolve | PASS — 28/28 |
| Whitespace/newline | Không trailing whitespace; 11/11 file có final newline | PASS |
| Read-only mapping | `07_table.md` đánh dấu N/A; không mô tả mutation | PASS |
| Source/OpenAPI | Route và module có mặt; 54 `/api/v1` path templates / 63 operations | PASS — local source |
| AC-36 macro-review | Rà #92–#96; group còn open questions | `VERIFIED_WITH_OPEN_QUESTIONS` — document review |

## Kiểm tra ứng dụng

- API #92 focused HTTP suite: 20 passed.
- Linked API #63/#64/#87/#92 regression: 85 passed.
- Full Study suite: 1217 passed; một upstream Starlette/httpx `TestClient` deprecation warning.
- `ruff check app tests`: passed.
- Scoped Ruff format check: passed.
- Fake sessions không kiểm tra PostgreSQL execution, live schema, migration deployment, worker delivery, fine-grained permission hoặc owner approval.

## Kết quả và giới hạn

- Direct catalog response vẫn là `ApiEnvelope<Notification>`; runtime hiện trả `ApiEnvelope<Page<Notification>>` theo fallback `DERIVED`.
- Local query dùng legacy BIGINT notifications cùng migration-009 delivery candidates; không gộp với V1-PILOT UUID notification model.
- Campaign-vs-recipient grain, channel/status enum semantics, Admin permission/scope, pagination, 503 trigger và #93 Notification-vs-Operation response còn là open questions.
- Không có claim về live schema, migration deployment, worker behavior hoặc owner approval. API #93–#96 vẫn là scope riêng.
