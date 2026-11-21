# AD-09 — Business Rules

## 1. Rule index
| Rule ID (package alias) | Tên / source ID | Áp dụng | Thực thi | Tests |
|---|---|---|---|---|
| `AD-09-BR-001` | Source rules/gates bundle (alias only) | See source DD | Not re-inferred | See source acceptance |

## 2. Rules, security, discrepancy và gate từ source
- Inventory purpose: Confirmation đổi trạng thái và cảnh báo enrollment/content phụ thuộc.
- Gate/status: **R** local source #74/#76/#77 route/module/test; Angular route/page/#74 read caller exists and write actions remain gated. API DDs Draft. **DD BLOCKED; IMPLEMENTATION PARTIAL SOURCE; WRITE FLOW BLOCKED:** #76 body/enum/transition DERIVED; `archive` has no mapping; #77 dependency/repeat/restore/audit policy, AC-32 permission vs `ADMIN`, and live schema remain open; post-write reload is undecided. **RUNTIME NOT VERIFIED**
- BR IDs trong file này chỉ là alias trỏ tới source rule/gate bundles; không thêm business rule. Không khẳng định rule FE/BE mới khi source chưa xác nhận.

### Trích từ DD nguồn: F. Tiêu chí nghiệm thu và blocker

### Checklist

- [x] Original screenshot and HTML preserved; hashes recorded.
- [x] 38 ordered markers and matching DD rows cover the visible screen elements/options/actions.
- [x] Native radio-only behavior, disabled textarea/Confirm, static claims and broken back/cancel destination are documented separately from runtime.
- [x] AC-32 and #74/#76/#77 catalog, DD/open questions, route/model/validator/view/query/test source and candidate DDL were reviewed.
- [x] Status and delete branches, auth/path/body/effects/response/errors and transaction boundaries traced.
- [x] API body/enum, archive mapping, hard-vs-soft delete, dependency coverage, audit reason, permission/schema, deleted visibility/restore and Study Web wiring remain explicit.
- [ ] Owner approves #76 enum/body/transitions/learner effects and AC-32 permission mapping.
- [ ] Owner approves #77 deletion marker/dependencies/repeat/audit/lifecycle policy and confirms live schema/deployment.
- [ ] Study Web route/client/navigation/error/loading/reload flow is implemented and runtime verified.

### Blockers

1. Catalog/AC omit #76 body and status enum; local values/transition behavior are `DERIVED`; mockup `archive` cannot map.
2. Local #77 soft-deletes while the mockup claims permanent irreversible deletion. Dependency set, repeat-delete 404, restore/visibility and delete audit remain open.
3. Mockup reason/ISO-27001 requirement is not in #76/#77 body or local audit data model.
4. AC-32 fine-grained course-management permission is not implemented by local shared `ADMIN` guard. Legacy BIGINT and V1-PILOT UUID/versioned schema differ; live DB/deployment unverified.
5. Angular route/page/#74 caller and loading/loaded/error states exist; status/delete/reason controls remain disabled and there is no #76/#77 Web caller. API error/session handling and post-mutation GET/revalidation remain gated/open.
6. Mockup enrollment/RBAC/protection/lifetime-retention claims are static. #74 counters are absent; #77's dependency check does not define a complete owner-approved policy.

**Completion decision:** The screen DD records the evidence and open decisions, but cannot be `DD READY` while body/enum, delete policy, permission, persistence and write-navigation decisions remain unresolved. Final screen status: **DD BLOCKED** · **IMPLEMENTATION PARTIAL SOURCE; WRITE FLOW BLOCKED** · **RUNTIME NOT VERIFIED**. Local API #76/#77 source status can be `R`; their API DDs remain Draft.

## 3. Quy tắc chưa xác nhận
- `CẦN_XÁC_NHẬN`: các quyết định/blocker trong inventory và DD nguồn chưa được giải quyết.
- Related IDs/source refs: Không có BR ID nguồn được chuẩn hóa.; xem [API](04-api-integration.md), [Events](02-events.md), [Tests](07-test-cases.md).
