# ST-19 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `ST-19-TC-001` | Planning ref / not run | `AC-17` | See source acceptance section | P1 |

## 2. Test planning references

### ST-19-TC-001 — Acceptance planning reference (AC-17)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [ST-19](../../screen_stitch/03_student/ST-19_bai-da-nop-va-phan-hoi/ST-19.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-17`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/03_student/ST-19_bai-da-nop-va-phan-hoi/ST-19.md).

## 3. Source acceptance / test plan (not run)

### Trích từ DD nguồn: F. Tiêu chí nghiệm thu và blockers

### F.1. Checklist

- [x] 58 visible element groups are numbered and mapped one-to-one to DD rows.
- [x] Screen, HTML, design contract, API catalog/DD and current route/source status are distinguished; Tailwind scripts are not described as application/API wiring.
- [x] API #36 method/path/auth/request/response/success/error set are recorded; no undocumented status is added.
- [x] Events document trigger element/type, preconditions, inputs, processing, outputs and unresolved policies; no write/API is invented.
- [x] Submitted/pending/graded/denied, auth/access/not-found/system/transport states and navigation dependencies are recorded.
- [ ] API #36 Student runtime route/query/test and Student Web route are implemented and verified.
- [ ] Ownership predicate, 403/404 masking, score/feedback release and status lifecycle are approved.
- [ ] Asset association, `files[]` mapping, URL security and timestamp/schema semantics are confirmed.
- [ ] API #35 response ID is aligned with inventory handoff and ST-19 route parameter.
- [ ] Comments, booking, next assignment, rubric and skill-index source/destination contracts are approved or removed from the implementation scope.
- [ ] PNG/HTML visual and actor-state discrepancy with the Study Web design target is resolved or approved before implementation.

### F.2. Blockers

1. API #36 remains `Draft — Needs Confirmation`, with no current Student route/module/query/test.
2. Study Web route/source/runtime for ST-19 is absent.
3. Student access predicate and 403/404 masking are unresolved.
4. Score/feedback disclosure and full status lifecycle are unresolved.
5. Logical `files[]` cannot be mapped to candidate single `file_url`; API #34 asset relation/security is unresolved.
6. API #35 draft `data.id` and inventory `submission_id` disagree; route handoff is unresolved.
7. Screenshot-only rubric, cohort stats, skill trend, mentor identity, comments, meeting and next assignment lack data/API contracts.
8. Timestamp timezone/format, candidate DDL nullability and live schema remain unverified.
9. PNG/HTML visual, typography, route and actor-state differences from the Study Web target remain unresolved.

**Kết luận:** DD BLOCKED; chưa đủ contract để chuyển triển khai. IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED. Không có tests hoặc runtime checks được chạy trong phiên docs này.

#### Kế hoạch kiểm chứng từ source PLAN

> CẦN_XÁC_NHẬN: Plan nguồn không có section verification/test được nhận diện.


- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
