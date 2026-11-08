# ST-21 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `ST-21-TC-001` | Planning ref / not run | `AC-18` | See source acceptance section | P2 |

## 2. Test planning references

### ST-21-TC-001 — Acceptance planning reference (AC-18)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [ST-21](../../screen_stitch/03_student/ST-21_tien-do-theo-khoa-hoc/ST-21.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-18`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/03_student/ST-21_tien-do-theo-khoa-hoc/ST-21.md).

## 3. Source acceptance / test plan (not run)

### Trích từ DD nguồn: F. Tiêu chí nghiệm thu và blockers

### F.1. Checklist

- [x] 11 nhóm element đang thấy trong HTML-derived image được đánh số và ánh xạ một-một tới DD.
- [x] PNG gốc và HTML gốc được giữ nguyên; HTML render bổ sung ghi provenance/hash/dimensions và giới hạn static-only.
- [x] Expected inventory/AC/API design được tách khỏi current source; API #37 là `DECLARED_NOT_RUNNABLE`.
- [x] API #37 method/path/auth/query/body/response/statuses được ghi theo catalog, không thêm 400/422.
- [x] 9 event mô tả trigger, input, xử lý, output và ngoại lệ; không tự tạo schema/aggregate/rule.
- [x] State matrix, ST-20/ST-10/ST-11 navigation và security constraints được ghi.
- [ ] API #37 response DTO có fields tiến độ được duyệt và đồng bộ catalog/API DD.
- [ ] AC-18 aggregate lesson/quiz/assignment, quiz attempt/submission selection, denominator/weight/rounding/timestamp policies được duyệt.
- [ ] Course enrollment/access/403-vs-404/JWT identity/empty and invalid-path behavior được chốt.
- [ ] Chọn schema/migration generation và xác minh live DB trước khi implementation.
- [ ] Loaded progress UI/lesson controls và route/data handoff được thiết kế; Study Web app source/runtime được wire.

### F.2. Blockers

1. API #37 response `ApiEnvelope<UserProfile>` không biểu diễn course/lesson/quiz/assignment progress; API DD Draft và Student route/module/query/test NOT_FOUND.
2. AC-18 chỉ nêu aggregate lesson + quiz + assignment; formula, dataset, attempt/submission selection, status inclusion, denominator, weight, rounding, timestamps và no-progress response đều mở.
3. Enrollment/course access, JWT user mapping, course visibility, 403/404 masking và `course_id` parse/range policy chưa chốt.
4. Legacy `lesson_progress` candidate khác V1-PILOT `lesson_progress_facts`/`progress_snapshots`; live schema/deployment chưa chứng minh API #37 query source.
5. Original PNG thiếu UI; HTML chỉ có static empty fallback, không có loaded course/lesson/metric design. Study Web route/runtime chưa có.
6. Lesson link phải qua ST-10/ST-11 gate; lesson-level access/handoff chưa được implement hoặc verify.

**Kết luận:** DD BLOCKED vì thiếu response/business/access contract và loaded-state design; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED. Không chạy tests/runtime trong phiên tài liệu này.

#### Kế hoạch kiểm chứng từ source PLAN

### Trích từ DD nguồn: 6. Verification plan

- Keep original screenshot/HTML hashes unchanged; record render provenance, dimensions and hash if Chromium render works.
- Validate marker JSON, ordered unique markers, in-bounds coordinates and exact DD element mapping; inspect annotated image visually for correct targets and unobscured content.
- Validate DD A–F, events, API statuses/fields, relative links, tracker row/count/pointers, source hashes and `git diff --check`.
- No tests or runtime API check unless requested. Run context validator only if a context page/manifest changes.

- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
