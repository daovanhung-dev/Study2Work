# Báo cáo kiểm chứng — API #69

- DD status: Draft — Needs Confirmation.
- Endpoint: GET /api/v1/admin/users/{user_id}.
- Runtime status: UNWIRED / NOT_FOUND — route, module, Admin guard và focused test không có trong Study source.
- Direct contract: ApiEnvelope<UserProfile>, HTTP 200 DESIGN_RESOURCE_RETRIEVED; đúng direct errors 401/403/404/500.
- Candidate query/no-row mapping: DERIVED trên legacy users; không phải runtime SQL.
- Application tests: NOT_RUN — task docs-only.

## Kiểm tra

| Check | Kết quả | Trạng thái |
|---|---|---|
| Worklog preflight | Selector chọn #48/#49/#50; đã đọc đủ cả ba. | PASS |
| Plan trước khi tạo DD | Requirement/request/query/mutation/response-source matrices có trong worklog trước khi tạo DD folder. | PASS |
| Catalog và diagram | API #69 row, UserProfile reusable schema, AC-31 index và toàn bộ page nodes/edges đã đối chiếu. | PASS — STATIC |
| Source/Admin/auth | Không có route/module/test API #69; current shared guard chỉ cho Student; Admin path chưa có trong middleware allowlist. | PASS — STATIC SOURCE REVIEW |
| Schema/profile | Legacy BIGINT users, V1-PILOT UUID relations và API #4/#14 profile projection đối chiếu; live schema không xác minh. | PASS — STATIC |
| Contract/error | Method/path/auth/path type/response/status/error set giữ đúng catalog; không thêm 422. | PASS |
| UserProfile fields | Đủ field id/full_name/email/role/avatar_url/bio/phone/status/created_at/updated_at; bio source gap và enum/null rules nêu rõ. | PASS |
| Data safety | Query candidate chỉ chọn safe profile fields; không lấy password_hash; PII và Admin boundary được nêu. | PASS |
| Template/package | 11-file package; 8 sheet dùng đúng front matter/appendix từ registered template pack. | PASS |
| Markdown/JSON/links | 2 ví dụ JSON parse; relative links và explicit anchors, table cell counts, fences và trailing whitespace đã pass. | PASS — STATIC |
| AC-31 macro-review | Rà document-level #68–#72; delete visibility, profile gaps, Admin policy và error consistency còn mở. | VERIFIED_WITH_OPEN_QUESTIONS |
| Inventory | Catalog 103 IDs; 72 DD folders, 60 full 11-file packages, 31 missing DD; 12 route-plus-view pairs and 91 without a pair. | PASS — STATIC |
| git diff --check | Chạy sau DD, inventory, report và worklog update; không có diagnostics. | PASS |
| Application tests | Không chạy; docs-only. | NOT_RUN |
| Context validator | Không áp dụng vì không sửa context page/manifest. | NOT_APPLICABLE |

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

Các câu hỏi về Admin authorization, schema, bio/enum/null, PII/audit, deletion visibility và error envelope còn trong [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md). Macro-review là document-level, không xác nhận runtime.
