# Báo cáo kiểm chứng — API #70

- DD status: Draft — Needs Confirmation.
- Endpoint: PUT /api/v1/admin/users/{user_id}.
- Runtime status: UNWIRED / NOT_FOUND — route, module, Admin guard và focused test không có trong Study source.
- Direct contract: Bearer JWT/Admin, path `user_id:int64!`, `ApiEnvelope<UserProfile>`, HTTP 200 `DESIGN_RESOURCE_UPDATED`; đúng direct errors 401/403/404/422/500.
- Request body và UPDATE SQL: chưa được catalog/diagram đặc tả; các candidate được gắn nhãn DERIVED.
- Application tests: NOT_RUN — task docs-only.

## Kiểm tra

| Check | Kết quả | Trạng thái |
|---|---|---|
| Worklog preflight | Selector chọn #48/#49/#50; đã đọc đủ cả ba. | PASS |
| Plan trước khi tạo DD | Requirement/request/query/mutation/response-source matrices có trong worklog trước khi tạo folder DD. | PASS |
| Catalog và diagram | API #70 row, UserProfile, AC-31 update branch và ranh giới #71/#72 đã đối chiếu. | PASS — STATIC |
| Source/Admin/auth | Không có route/module/focused test API #70; current shared guard chỉ cho Student. | PASS — STATIC SOURCE REVIEW |
| Schema/profile | API #14 mutation, legacy BIGINT users và V1-PILOT UUID boundary đã đối chiếu; live schema không xác minh. | PASS — STATIC |
| Contract/error | Method/path/auth/path type/response/status/error set giữ đúng catalog; không thêm code/status. | PASS |
| DERIVED/SOURCE_REQUIRED labels | Body fields, query/mutation, no-row mapping và open decisions được đánh dấu; bio không được bịa source. | PASS |
| Template/package | Exact 11-file manifest; 8/8 core appendix suffixes byte-equal với registered template. | PASS |
| Markdown/JSON/links | Fences/tables cân bằng; JSON parse; relative links/anchors resolve. | PASS — STATIC |
| AC-31 macro-review | Rà document-level #68–#72; update/status/delete boundaries được tách, chính sách và schema còn mở. | VERIFIED_WITH_OPEN_QUESTIONS |
| Inventory | Catalog 103 IDs; 72 DD folders, 60 full 11-file packages, 31 missing DD; 12 route-plus-view pairs and 91 without a pair. | PASS — STATIC |
| git diff --check | Không có diagnostics. | PASS |
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

Các câu hỏi về Admin authorization, body/role policy, live schema, bio/null, PII/audit, session effects, deleted-user behavior và error envelope còn trong [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md). Macro-review là document-level, không xác nhận runtime.
