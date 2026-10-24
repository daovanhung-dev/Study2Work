# Báo cáo kiểm chứng — API #71

- DD status: Draft — Needs Confirmation.
- Endpoint: PATCH /api/v1/admin/users/{user_id}/status.
- Runtime status: UNWIRED / NOT_FOUND — route, module, Admin guard và focused test không có trong Study source.
- Direct contract: Bearer JWT/Admin, path `user_id:int64!`, `ApiEnvelope<UserProfile>`, HTTP 200 `DESIGN_RESOURCE_UPDATED`; direct errors 401/403/404/422/500.
- Body/status values và database/session mutations: catalog/diagram chưa định nghĩa đầy đủ; candidate được gắn DERIVED.
- Session boundary: source cho thấy login/refresh kiểm tra ACTIVE và access JWT guard không tra account status; refresh-token revoke không đồng nghĩa access-token revoke.
- Application tests: NOT_RUN — task docs-only.

## Kiểm tra

| Check | Kết quả | Trạng thái |
|---|---|---|
| Worklog preflight | Selector chọn #48/#49/#50; cả ba đã được đọc đầy đủ. | PASS |
| Plan trước khi tạo DD | Requirement/request/query/mutation/response-source matrices có trong worklog trước khi tạo folder. | PASS |
| Catalog và diagram | API #71 row, UserProfile/UserStatus, AC-31 STATUS branch, conditional revoke và reload path đã đối chiếu. | PASS — STATIC |
| Current source/session | Không có route/module/test #71; API #3 login/refresh, token queries, API #4/auth guard và legacy/pilot status DDL đã đối chiếu. | PASS — STATIC SOURCE REVIEW |
| Contract/error | Method/path/auth/path type/response/status/errors giữ đúng catalog; không thêm code/status. | PASS |
| DERIVED/source gaps | Body/status values, legacy UPDATE, conditional refresh-token revoke và access JWT limitation được phân biệt; không gộp #70/#72. | PASS |
| Template/package | Exact 11-file manifest; 8/8 appendix tails byte-equal registered templates. | PASS |
| Markdown/JSON/links | JSON parse; tables/fences balanced; relative links/anchors resolve; no trailing whitespace. | PASS — STATIC |
| AC-31 macro-review | Rà document-level #68–#72; status/session và delete policy còn mở. | VERIFIED_WITH_OPEN_QUESTIONS |
| Inventory | Catalog 103 IDs; 72 DD folders, 60 full 11-file packages, 31 missing DD; 12 route-plus-view pairs and 91 without a pair. | PASS — STATIC |
| git diff --check | Không có diagnostics. | PASS |
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

Body/status enum, Admin guard, live schema, conditional session revoke, access JWT invalidation, no-op/self-lock, delete policy và error envelope còn trong [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md). Macro-review là document-level, không xác nhận runtime.
