# AD-23 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `AD-23-TC-001` | Planning ref / not run | `AC-37` | See source acceptance section | P1 |

## 2. Test planning references

### AD-23-TC-001 — Acceptance planning reference (AC-37)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [AD-23](../../screen_stitch/05_admin/AD-23_dieu-tra-kiem-duyet-thao-luan/AD-23.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-37`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/05_admin/AD-23_dieu-tra-kiem-duyet-thao-luan/AD-23.md).

## 3. Source acceptance / test plan (not run)

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

#### Kế hoạch kiểm chứng từ source PLAN

### Trích từ DD nguồn: 6. DD authoring and static verification

1. Write `AD-23.md` sections A–F with 45 element rows and EV-01…EV-09.
2. Keep expected AC/catalog behavior, prototype behavior, local #98 source, and unresolved #99/#100 behavior separate. Include success and errors only where the direct contract/local source supports them.
3. Explain that #98 currently maps Discussion and direct comments only; do not fabricate report reasons, severity, reporter, report count, or audit fields. Distinguish catalog response from current local projection and note API DD #98’s stale runtime label.
4. Record the #99 delete-radio mismatch, AC no-violation dismissal without an endpoint, Admin vs local `ADMIN`, root/reply grain, and missing Study Web source as blockers.
5. Create `AD-23_markers.json`, `AD-23_markers_overlay.svg`, and `screen_annotated.png` after this plan. Review full-size annotation visually and move any marker obscuring meaningful copy.
6. Update inventory row 81 and API reverse-index #098–#100 using separate source-status and DD/runtime-status labels. Append the AD-23 checkpoint to the global plan; do not start AD-24.
7. Static audit: IDs 1–45 unique/sequential, in bounds, aligned across plan/JSON/SVG/DD; all A–F and events present; relative links resolve; JSON/SVG parse; annotated dimensions 3010×3200; source image/HTML hashes unchanged; 83 inventory IDs/folders remain; core artifact count updated; `git diff --check` passes.

- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
