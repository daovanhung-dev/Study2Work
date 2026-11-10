# ME-14 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `ME-14-TC-001` | Planning ref / not run | `AC-25` | See source acceptance section | P2 |

## 2. Test planning references

### ME-14-TC-001 — Acceptance planning reference (AC-25)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [ME-14](../../screen_stitch/04_mentor/ME-14_soan-thong-bao-mentor/ME-14.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-25`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/04_mentor/ME-14_soan-thong-bao-mentor/ME-14.md).

## 3. Source acceptance / test plan (not run)

### Trích từ DD nguồn: F. Tiêu chí nghiệm thu và traceability

### Checklist tài liệu

- [x] A–F có mặt; expected behavior và current behavior phân tách.
- [x] 68 marker liên tục, mỗi ID ánh xạ một element record.
- [x] Prototype interactions, điều kiện, input, xử lý, output và lỗi/unavailable behavior được mô tả tại D.
- [x] API #63 request/auth/scope/transaction/response/error được đối chiếu source và DD; trạng thái `Draft`/`DERIVED` được giữ rõ.
- [x] #62 được giới hạn vào roster step ME-13; không tự thêm fetch ở ME-14.
- [x] API #64 notification ID và API #18 Operation ID không bị nhập làm một.
- [x] Attachment, draft, channel mapping, rich text, recipient course binding và retry được đánh dấu blocker.
- [x] Metric/compliance/visibility claims tĩnh không được nâng thành behavior requirement.
- [x] Asset gốc được giữ lại; annotation là file riêng.

### Điều kiện chặn triển khai

1. Chốt course-bound recipient handoff giữa ME-13 và #63; `#63` hiện không nhận `course_id`.
2. Chốt body content contract thay cho `content:int64` hoặc chỉ định nguồn content ID hợp lệ.
3. Chốt title required/blank rule và giới hạn 120 hay 200.
4. Chốt In-app↔`PUSH` mapping, Email availability và delivery worker/provider.
5. Quyết định có notification attachment không; nếu có, định nghĩa upload purpose/scope/size/type, ID persistence và link vào #63.
6. Định nghĩa draft persistence/restore và retry/idempotency behavior.
7. Chốt Study Web route/auth/state plumbing; #18 không khả dụng và không nối trong AC-25.

### Nguồn truy vết

- Inventory/route/API/dependencies: [list_screen.md](../../list_screen.md), [global DD screen plan](../../screen_stitch/dd_screens/PLAN.md).
- Trước màn hình này: [ME-13.md](../../screen_stitch/04_mentor/ME-13_chon-nguoi-nhan-thong-bao/ME-13.md).
- Expected flow AC-25: `apps/study-server/docs/diagrams/AC_UNICA/AC_03_MENTOR_TEACHING.drawio` (page AC-25).
- #63 local source: `apps/study-server/app/api/v1.py`; `apps/study-server/app/modules/mentor/api_63_mentor_notifications_create/`; DD `apps/study-server/docs/dd/63_mentor_notifications_create/`; tests `apps/study-server/tests/modules/mentor/api_63_mentor_notifications_create/`.
- #64 local source: `apps/study-server/app/api/v1.py`; `apps/study-server/app/modules/mentor/api_64_mentor_notification_status/`; DD `apps/study-server/docs/dd/64_mentor_notifications_status/`; tests `apps/study-server/tests/modules/mentor/api_64_mentor_notification_status/`.
- #18 design/current-source status: `apps/study-server/docs/dd/18_operations/`; source route/module/test scan found no Study implementation.
- #34 upload source: `apps/study-server/app/modules/student/api_34_uploads/`; DD `apps/study-server/docs/dd/34_uploads/`.
- Screen prototype: `code.html`, `screen.png`; web status `UNWIRED` in `.agents/context-manifest.json` and `.agents/web-study/`.

### Kiểm tra cuối

- [ ] Source image/HTML hashes không đổi.
- [ ] Marker JSON parse, ID đúng `1..68`, không trùng, trong bounds 1267×1600.
- [ ] 68 marker khớp 68 dòng element; annotated image là 2534×3200 và không che text quan trọng.
- [ ] Links nội bộ tồn tại; `git diff --check` sạch.
- [ ] Không chạy application tests và không gắn `RUNTIME VERIFIED` cho task tài liệu này.

#### Kế hoạch kiểm chứng từ source PLAN

### Trích từ DD nguồn: 8. Review and static verification gate

- Confirm source hashes remain unchanged.
- Confirm markers are contiguous from 1 through N, unique, in image bounds, and match exactly N DD element records.
- Confirm the annotated PNG is readable at full resolution and markers avoid important text.
- Confirm every identified control and meaningful static claim has a DD element record and relevant event(s).
- Confirm every API statement cites the exact catalog/DD/source boundary and keeps Draft/DERIVED/UNWIRED/RUNTIME NOT VERIFIED labels separate.
- Check local links, image paths, Markdown structure, JSON parse, and `git diff --check`.
- Do not run application tests or claim runtime verification for this docs-only task.

- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
