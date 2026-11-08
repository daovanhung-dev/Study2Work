# ST-21 — Business Rules

## 1. Rule index
| Rule ID (package alias) | Tên / source ID | Áp dụng | Thực thi | Tests |
|---|---|---|---|---|
| `ST-21-BR-001` | Source rules/gates bundle (alias only) | See source DD | Not re-inferred | See source acceptance |

## 2. Rules, security, discrepancy và gate từ source
- Inventory purpose: Các bài đã/đang/chưa học, tỷ lệ hoàn thành, mốc thời gian có chứng cứ.
- Gate/status (giữ nguyên): **D**
- BR IDs trong file này chỉ là alias trỏ tới source rule/gate bundles; không thêm business rule. Không khẳng định rule FE/BE mới khi source chưa xác nhận.

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

## 3. Quy tắc chưa xác nhận
- `CẦN_XÁC_NHẬN`: các quyết định/blocker trong inventory và DD nguồn chưa được giải quyết.
- Related IDs/source refs: Không có BR ID nguồn được chuẩn hóa.; xem [API](04-api-integration.md), [Events](02-events.md), [Tests](07-test-cases.md).
