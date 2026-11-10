# ST-18 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `ST-18-TC-001` | Planning ref / not run | `AC-17` | See source acceptance section | P1 |

## 2. Test planning references

### ST-18-TC-001 — Acceptance planning reference (AC-17)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [ST-18](../../screen_stitch/03_student/ST-18_soan-va-nop-bai-tap/ST-18.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-17`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/03_student/ST-18_soan-va-nop-bai-tap/ST-18.md).

## 3. Source acceptance / test plan (not run)

### Trích từ DD nguồn: F. Tiêu chí nghiệm thu

- [x] 60 markers are sequential and map one-to-one to 60 rows in this table.
- [x] Original screen.png and code.html bytes are preserved; annotated image retains original screen content and is visually readable.
- [x] Every field/action shown in the design is described; sample data is not treated as live.
- [x] Events document trigger, input, preconditions, sequence, API/envelope/status/business code, output, error behavior and persistence boundary, with unconfirmed behavior left open.
- [x] #34 behavior matches current route/view/provider source and clearly separates current server behavior from unrun tests/live deployment.
- [x] #33/#35 are not described as implemented; #36 remains a ST-19 follow-on with its current missing-source status.
- [x] File size/MIME, optional course_id, public URL access, file-ref encoding, draft persistence/retention, URL mapping, consent, retry/idempotency and submission response ID discrepancies remain explicit.
- [x] State machine never treats successful upload as successful submission or local countdown as authorization.
- [ ] Navigation and payload handoffs agree with linked screens after the open ID/cache/API decisions are resolved.
- [x] No unresolved assumption is silently promoted to an approved contract.

#### Kế hoạch kiểm chứng từ source PLAN

### Trích từ DD nguồn: 5. Blockers and discrepancy checklist

- Screenshot loaded form vs HTML unavailable fallback; actor/state differ.
- Screenshot's GitHub/deployment/checklist/draft/autosave/consent details have no source mapping in #33/#35.
- Screenshot says 50 MB and advertises PDF/DOCX/ZIP/PNG/WEBP; current #34 source has no application size/MIME restriction.
- #34 `course_id` is optional; omitting it skips Student enrollment query. The assignment/course context and client behavior are not approved.
- #34 returns an asset ID and a public URL, but #35's required `file refs:string!` has no key/encoding/cardinality contract; physical `file_url` cannot represent logical `files[]` without a schema decision.
- API #35 and Student #33/#36 are not wired; #35 response ID naming (`data.id` vs inventory `submission_id`) and state transition/idempotency are open.
- Inventory assigns GET #33 to ST-17 and ST-18 while AC-17 depicts one read before entering the submission form; cache/refetch ownership is unresolved.
- Study Web route/runtime and real database/object-storage deployment are not verified.

### Trích từ DD nguồn: 6. Verification plan

- Preserve original PNG/HTML hashes/dimensions.
- Produce ordered marker JSON and side-gutter SVG/PNG; ensure 60 IDs map exactly once to the DD table, coordinates are in bounds, labels don't overlap or cover screenshot content, then visually inspect the rendered result.
- Check DD sections A–F, sequential event IDs and complete API/error/state/navigation trace; verify local links and tracker row/counters/next pointers.
- Run `git diff --check` and a focused static artifact/whitespace audit. No tests or runtime are run under current task instructions.

- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
