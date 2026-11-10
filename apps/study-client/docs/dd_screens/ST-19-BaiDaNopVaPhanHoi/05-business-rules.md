# ST-19 — Business Rules

## 1. Rule index
| Rule ID (package alias) | Tên / source ID | Áp dụng | Thực thi | Tests |
|---|---|---|---|---|
| `ST-19-BR-001` | Source rules/gates bundle (alias only) | See source DD | Not re-inferred | See source acceptance |

## 2. Rules, security, discrepancy và gate từ source
- Inventory purpose: Hiển thị timestamp, file, trạng thái chấm, score/feedback khi có.
- Gate/status (giữ nguyên): **D; DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED:** API #36 chỉ có catalog/Draft DD, Student route/module/query/test NOT_FOUND; ownership/access predicate, 403-vs-404, score/feedback release, SubmissionStatus/timezone/path parsing còn mở; logical `files[]` không map được vào legacy scalar `file_url`, assignment/user nullability và live schema chưa xác minh; API #35 `data.id` vs inventory `submission_id` handoff chưa chốt; rubric/cohort/mentor/PR/booking/skill/next-assignment fields thiếu API contract; loaded graded PNG khác Guest fallback HTML (Tailwind CDN/config, remote fonts, max-width 1440px) và Study Web design target; Study Web UNWIRED
- BR IDs trong file này chỉ là alias trỏ tới source rule/gate bundles; không thêm business rule. Không khẳng định rule FE/BE mới khi source chưa xác nhận.

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

## 3. Quy tắc chưa xác nhận
- `CẦN_XÁC_NHẬN`: các quyết định/blocker trong inventory và DD nguồn chưa được giải quyết.
- Related IDs/source refs: Không có BR ID nguồn được chuẩn hóa.; xem [API](04-api-integration.md), [Events](02-events.md), [Tests](07-test-cases.md).
