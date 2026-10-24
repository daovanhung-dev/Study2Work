# Báo cáo kiểm chứng — API #92 Lấy notification list

## Phạm vi

- DD: `apps/study-server/docs/dd/92_admin_notifications_list/`.
- Trạng thái tài liệu: `Draft — Needs Confirmation`; các câu hỏi về cardinality, schema, permission và filter vẫn mở.
- Current source: API #92 `UNWIRED / NOT_FOUND`; không có route, module hoặc test tương ứng trong Study source.
- Đây là kiểm tra tài liệu tĩnh. Application tests, runtime và live DB không được chạy/xác minh.

## Nguồn đã đối chiếu

- Catalog #92 và reusable `Notification`: giữ `GET /api/v1/admin/notifications`, Admin Bearer, query `status?:string`, `channel?:string`, `page?:int32`, `ApiEnvelope<Notification>`, HTTP 200 và đúng errors 401/403/503/500.
- AC-36 index và diagram: #92 query trước các nhánh #93–#96; list cardinality, filter mapping, pagination và trigger 503 chưa được xác định.
- DB table guide, ERD, legacy BIGINT DDL và V1-PILOT UUID DDL: hai notification models được giữ riêng; delivery channel/status không được đổi thành Notification-level fields.
- DD #43, #63 và #64: dùng làm precedent có giới hạn; Student ownership và Mentor operation semantics không được chuyển sang Admin #92.
- Current Study router, middleware, response helper và API Guidelines: không có route #92; middleware path allowlist chưa có Admin notifications; helper/error-envelope discrepancy chỉ là future wiring concern.

## Template và fingerprint

- Đã dùng đủ tám file trong `.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/`.
- Template manifest SHA-256: `541b6ea0c36c5781c1b62574e1aba4e2fab5fde2f949a54129a123c63b78b9c2` — SHA-256 của các dòng `filename:file_sha256`, sắp xếp theo filename.
- Output manifest SHA-256: `72d5ac23b4c67c6720904a57caad533b209cf525ab49b39544563f54d13187c8` — SHA-256 cùng cách tính trên tám sheet, `PLAN_RESULT.md` và `OPEN_QUESTIONS.md`; loại report này khỏi manifest để tránh tự tham chiếu.
- Study workflow giao thư mục Markdown; không tạo ZIP.

## Kiểm tra tĩnh

| Hạng mục | Kết quả | Trạng thái |
|---|---|---|
| Package | Đúng 11 file: 8 sheet và 3 report | PASS — 11/11 |
| Template appendix | Tám appendix khớp byte-for-byte với template | PASS — 8/8 |
| Front matter | Tám sheet có front matter và `dd_id: 92` | PASS — 8/8 |
| Catalog contract | Method/path/auth/query/response/status và exact error set được giữ | PASS — static |
| Notification projection | Tất cả field của schema `Notification` và envelope được liệt kê; Page proposal tách khỏi direct contract | PASS — static |
| JSON examples | Tất cả fenced JSON parse được | PASS — 4/4 |
| Markdown tables/fences | 34 bảng, 436 dòng bảng nhất quán; sáu cặp fence cân bằng | PASS — static |
| Relative links/anchors | 20 file/directory links và 5 anchor links đều resolve | PASS — 25/25 |
| Whitespace/newline | Không có trailing whitespace; mọi file có final newline | PASS |
| Read-only mapping | `07_table.md` ghi N/A, không có mutation giả | PASS |
| Source scan | Không có route/module/test API #92; design allowlist chưa chứa path | PASS — static |
| AC-36 macro-review | Đã rà #92–#96; xem [AC-36_MACRO_REVIEW.md](../96_admin_notifications_status/AC-36_MACRO_REVIEW.md) | VERIFIED_WITH_OPEN_QUESTIONS — document review |
| Application tests | Không chạy; task docs-only | NOT_RUN |

## Kết quả và giới hạn

- Direct contract vẫn là `ApiEnvelope<Notification>`; response Page chỉ là đề xuất `DERIVED`, không thay catalog.
- Legacy BIGINT notifications và V1-PILOT UUID notifications/deliveries không được gộp. Chưa có query hoặc schema hoàn chỉnh để map Notification cho Admin.
- Campaign-vs-recipient grain, enum/filter semantics, Admin permission, pagination, 503 trigger và #93 Notification-vs-Operation response vẫn là open questions.
- Không có claim về runtime, deployment, live schema hoặc owner approval. Các câu hỏi về cardinality, Admin schema, permission và #93 Operation bridge tiếp tục mở.
