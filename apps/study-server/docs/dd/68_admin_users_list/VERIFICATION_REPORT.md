# Báo cáo kiểm chứng — API #68

- DD status: Draft — Needs Confirmation.
- Endpoint: GET /api/v1/admin/users.
- Runtime status: UNWIRED / NOT_FOUND — route, module, Admin guard và focused test không có trong source Study hiện tại.
- Direct contract: ApiEnvelope<UserProfile>, HTTP 200 DESIGN_RESOURCE_RETRIEVED; đúng direct errors 401/403/500.
- Candidate Page<UserProfile> và pagination/filter semantics: DERIVED; chưa được contract owner duyệt.
- Runtime/application tests: NOT_RUN — task docs-only.

## Kiểm tra

| Check | Kết quả | Trạng thái |
|---|---|---|
| Worklog preflight | Selector chọn #48/#49/#50; đã đọc đủ cả ba. | PASS |
| Plan trước khi tạo DD | Requirement/request/query/mutation/response matrices có trong worklog trước lúc tạo DD folder. | PASS |
| Catalog và diagram | API #68 row, AC-31 index/full diagram page và users entity trong DB ERD đối chiếu; list/pagination mismatch được ghi rõ. | PASS — STATIC |
| Source/admin/auth | Không có route/module/test API #68 hoặc Admin guard; path chưa có trong middleware allowlist. | PASS — STATIC SOURCE REVIEW |
| Schema/profile | Legacy BIGINT users, V1-PILOT UUID model, API #4/#14 profile projection và API #07 pagination precedent đối chiếu; live schema không xác minh. | PASS — STATIC |
| Contract/error | Direct response và đúng 3 error code 401/403/500 được giữ; không thêm 404/422. | PASS |
| UserProfile fields | Tất cả field kể cả UserRole/UserStatus và bio? được ghi theo reusable schema; enum members/bio source gap được nêu. | PASS |
| Data safety | Candidate query chỉ chọn safe profile fields; không lấy password_hash; PII và bio gap được nêu. | PASS |
| Template/package | Exact 11-file package; front matter và appendix template 8/8 khớp byte-for-byte. | PASS |
| Markdown/JSON/links | JSON parse; relative links/anchors, table widths, fences và whitespace đều pass. | PASS |
| AC-31 macro-review | Rà document-level #68–#72; list response mismatch và policy/schema/security gaps còn mở. | VERIFIED_WITH_OPEN_QUESTIONS |
| Inventory | Catalog 103 IDs; 72 DD folders, 60 full 11-file packages, 31 missing DD; 12 route-plus-view pairs and 91 without a pair. | PASS — STATIC |
| git diff --check | Chạy sau final report/worklog/inventory update; không có diagnostics. | PASS |
| Application tests | Không chạy; docs-only. | NOT_RUN |
| Context validator | Không áp dụng nếu không sửa context page/manifest. | NOT_APPLICABLE |

## AC-31 group macro-review

Status: VERIFIED_WITH_OPEN_QUESTIONS — document-level review of APIs #68–#72.

- #68 catalog response remains ApiEnvelope<UserProfile>, while AC-31 describes a list/pagination flow; the discrepancy is still open and #72 does not change it.
- #69 detail, #68 list and #70/#71 UserProfile responses share the UserProfile schema, but bio has no legacy/source mapping; role/status enum members, optional null behavior, PII access and audit policy remain unresolved.
- #70 owns candidate profile/role updates; #71 owns candidate account ACTIVE/SUSPENDED transitions and conditional refresh-token revocation; #72 owns the delete/anonymization intent. Do not overlap these writes.
- #72 keeps DeleteResult and the diagram's soft-delete/anonymize intent. Physical policy/schema, dependency rules, deleted_at source and repeat-delete behavior remain SOURCE_REQUIRED.
- List/detail visibility after suspend/delete/anonymization, Admin authorization, live schema and error data null-versus-empty remain shared implementation questions.
- Legacy user-linked relations are DDL context only; no blanket dependency block, cascade or hard-delete rule was inferred.
- No route/runtime or application-test claim is made; all five APIs remain UNWIRED / NOT_FOUND.

## Open status

Các câu hỏi về response list, pagination, filters, Admin authorization, live schema, bio/null, PII và visibility sau delete được giữ trong [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md). Macro-review chỉ xác nhận độ nhất quán tài liệu; không xác nhận runtime.
