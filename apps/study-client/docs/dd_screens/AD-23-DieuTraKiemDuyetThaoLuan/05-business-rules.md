# AD-23 — Business Rules

## 1. Rule index
| Rule ID (package alias) | Tên / source ID | Áp dụng | Thực thi | Tests |
|---|---|---|---|---|
| `AD-23-BR-001` | Source rules/gates bundle (alias only) | See source DD | Not re-inferred | See source acceptance |

## 2. Rules, security, discrepancy và gate từ source
- Inventory purpose: Đọc full thread/report, action hide/lock/warn/delete có lý do.
- Gate/status (giữ nguyên): **R #98** local route/module/query/model/validator/view/test source; API DD #98 stale `UNWIRED`; #99/#100 **D** catalog/Draft only, no local route. **DD BLOCKED; IMPLEMENTATION BLOCKED:** #98 report projection, #99 action/audit, #100 soft-delete policy, dismissal branch, target grain, Admin permission mapping and Study Web remain unresolved/unwired
- BR IDs trong file này chỉ là alias trỏ tới source rule/gate bundles; không thêm business rule. Không khẳng định rule FE/BE mới khi source chưa xác nhận.

### Trích từ DD nguồn: F. Tiêu chí nghiệm thu và quyết định còn mở

### Static DD acceptance checklist

- [x] 45 numbered markers map to 45 unique element rows in §C.
- [x] Nine identified events distinguish static prototype, expected contract and current server source.
- [x] #98 method/path/auth/params/response/catalog codes are recorded; local source projection/query/auth/side effects/errors are separated.
- [x] #99 and #100 request/response/error contracts are recorded as catalog-only, not runtime behavior.
- [x] AC-37 navigation, optional delete, dismissal branch and AD-22 handoff are represented with unresolveds visible.
- [x] Source image and HTML are kept as original files; annotation is separate.
- [ ] Full DD READY: **not met**; the blockers below affect implementability.
- [ ] IMPLEMENTATION READY: **not met**; Study Web is UNWIRED and mutation APIs are absent locally.
- [ ] RUNTIME VERIFIED: **not met**; no app/runtime verification was performed.

### Blockers requiring contract decisions

1. Specify report persistence/writer and a #98 response that includes the report context AC-37 requires; decide report grain, reason/severity/reporter/count/time fields, and live-schema/deployment evidence.
2. Reconcile API #98 DD's stale `UNWIRED / NOT_FOUND` label with registered local route/module/test source; approve catalog/direct response mapping and whether local projection satisfies the final API contract.
3. Define #99 action tokens, allowed state transitions, target scope, validation for reason, authorization, audit actor/table/fields/retention and transaction atomicity; implement and test the route before enabling controls.
4. Define the no-violation dismissal behavior and endpoint, or revise AC-37 through its owner. Do not overload #99 without a contract.
5. Define #100 eligibility, soft-delete representation/timestamp, `DeleteResult` mapping, audit preservation/linkage, child/reply/report retention and visibility, repeat/concurrency/idempotency behavior, plus its UI trigger/confirmation.
6. Resolve whether a report targets a root Discussion or a reply and which comments are visible; confirm how AD-22 hands the correct ID/context to AD-23.
7. Approve mapping between AC Admin permission and local `ADMIN`, actor identity, tenant scope, and policies for #99/#100.
8. Implement the Study Web route/client, including response/error mapping, loading states and return/refresh behavior, then verify with runtime tests.

Until those decisions are source-backed, keep moderation/delete controls locked, preserve the prototype discrepancy, and retain `DD BLOCKED`, `IMPLEMENTATION BLOCKED`, `RUNTIME NOT VERIFIED`.

## 3. Quy tắc chưa xác nhận
- `CẦN_XÁC_NHẬN`: các quyết định/blocker trong inventory và DD nguồn chưa được giải quyết.
- Related IDs/source refs: Không có BR ID nguồn được chuẩn hóa.; xem [API](04-api-integration.md), [Events](02-events.md), [Tests](07-test-cases.md).
