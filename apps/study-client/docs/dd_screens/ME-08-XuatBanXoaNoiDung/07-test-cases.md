# ME-08 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `ME-08-TC-001` | Planning ref / not run | `AC-22` | See source acceptance section | P2 |

## 2. Test planning references

### ME-08-TC-001 — Acceptance planning reference (AC-22)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [ME-08](../../screen_stitch/04_mentor/ME-08_xuat-ban-xoa-noi-dung/ME-08.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-22`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/04_mentor/ME-08_xuat-ban-xoa-noi-dung/ME-08.md).

## 3. Source acceptance / test plan (not run)

### Trích từ DD nguồn: 8. Acceptance criteria

1. ME-08 obtains `contentId` plus course context from an approved ME-06 handoff and hydrates only the matching Content from #49; it does not invent a detail endpoint or trust sample data.
2. Publish and unpublish intent are explicit target actions. #52 body/state/readiness contract is approved before implementation; supported response/errors are mapped as documented.
3. Delete confirmation accurately states the approved dependency policy. Current #53 source facts (PUBLISHED guard, active direct-child guard, soft-delete result) stay distinct from unapproved effects and missing dependency checks.
4. Mutations remain separate. If product requires unpublish then delete, intermediate success and later delete failure are represented; no assumption of atomicity.
5. After mutation, #49 is reloaded with preserved `courseId`; #53 response is not expected to provide it. Mutation success and refresh error are separate states.
6. 46 marker IDs match one DD element each and the JSON/SVG/image. Every visible link/button is either source-backed or explicitly static/blocked.
7. Current server auth, request, side effects, response, errors and test-source limits are traced; there is no claim of Study Web, deployed API or live DB runtime verification.

#### Kế hoạch kiểm chứng từ source PLAN

### Trích từ DD nguồn: 5. Session acceptance checklist

- Original PNG/HTML hashes remain unchanged; screenshot and HTML discrepancies are recorded.
- `ME-08_PLAN.md` predates marker JSON/SVG, annotated PNG and DD.
- 46 ordered unique in-bounds markers; JSON↔SVG↔DD one-to-one; no marker obscures content; image dimensions preserve 2× aspect ratio.
- Every action/event traces to inventory/AC/current route/module/query/view/test source or is labeled open/DERIVED/blocked.
- #52 catalog/body/state discrepancy and #53 derived guards are explicit; no unapproved transition, dependency policy or audit effect is presented as canonical.
- Local API tests are inspected only; no test, runtime, deployed DB or live API claim is made.
- Update global ME-08 row/checkpoint and this worklog; run static link/marker/hash audit and `git diff --check`.

- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
