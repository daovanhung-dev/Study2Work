# GS-03 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `GS-03-TC-001` | Planning ref / not run | `AC-05` | See source acceptance section | P1 |

## 2. Test planning references

### GS-03-TC-001 — Acceptance planning reference (AC-05)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [GS-03](../../screen_stitch/02_guest_discovery/GS-03_chi-tiet-khoa-hoc/GS-03.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-05`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/02_guest_discovery/GS-03_chi-tiet-khoa-hoc/GS-03.md).

## 3. Source acceptance / test plan (not run)

### Trích từ DD nguồn: H. Tiêu chí nghiệm thu

### Tài liệu và asset

- [x] GS-03 plan tồn tại trước khi tạo ảnh đánh số và DD.
- [x] `screen.png`/`code.html` giữ nguyên hash; ảnh nguồn trắng được ghi nhận, có render thay thế rõ nguồn gốc.
- [x] `screen_annotated.png` có 10 marker tuần tự; marker JSON cùng 10 element ID và không đánh dấu UI vắng mặt.
- [x] Mỗi marker #1–#10 có đúng một mô tả ở mục C và đúng một mục trong bảng marker JSON.
- [x] Event có input, trình tự, API/code, output và ngoại lệ; hành vi không có source được đánh dấu expected/blocked.
- [x] #08/#09 current source và #10 declared-only được phân biệt; AC/F02 order conflict, 404/403 conflict và G-01 được ghi rõ.
- [ ] Loaded detail, tab active states, enrollment CTA, route/auth handoff và API #10 schema/orchestration được Product/BE xác nhận; điều kiện bắt buộc để chuyển DD sang READY.
- [ ] UI runtime/router được nối và xác minh; điều kiện để xem xét `RUNTIME VERIFIED`.

### Decision/blocker owner cần chốt

| Blocker | Quyết định cần có | Chủ sở hữu đề xuất theo nguồn |
|---|---|---|
| Loaded course detail/CTA design còn thiếu | Vị trí và nội dung course/mentor/price, CTA; loading/error/empty states; price formatting/currency; responsive/focus behavior | Product + Web |
| AC-05 call order khác F02 | Chọn eager #09/#10 trong AC hay lazy theo tab; cập nhật nguồn chuẩn sau duyệt | Product + Backend |
| API #10 absent và schema conflict | Nối route/module; xác nhận review fields/title, rating source/aggregate, query key/filter, pagination, visibility, error semantics | Backend + Product |
| Guest enrollment handoff / G-01 | Identity semantics cho #15 hoặc thay contract; auth/login flow, idempotency/eligibility và course ID handoff | Product + Auth/Backend |
| Study Web UNWIRED | Router/runtime/layout và link destinations | Web |

#### Kế hoạch kiểm chứng từ source PLAN

### Trích từ DD nguồn: 5. Thứ tự thực hiện và acceptance checklist

1. [x] Kế hoạch này được tạo trước khi tạo ảnh render, annotation hoặc DD.
2. [x] Render HTML nguyên trạng trong Firefox ra `screen_rendered.png`; đã kiểm tra kích thước, stylesheet và nội dung. Không ghi đè nguồn.
3. [x] Tạo `GS-03_markers.json`, SVG overlay và `screen_annotated.png` theo 10 nhóm trên; marker đúng vùng, thứ tự liên tục, không che nội dung.
4. [x] Viết `GS-03.md` tiếng Việt theo các phần: tổng quan; luồng; 10 element; từng event với đầu vào/xử lý/đầu ra và API status; state/navigation matrix; blocker; acceptance checklist và trace links.
5. [x] Static audit: JSON parse; marker IDs/số thứ tự khớp bảng DD; link tương đối tồn tại; hash `screen.png`/`code.html` không đổi; 83 inventory/tracker/folder IDs match; `git diff --check`. Không chạy test hay runtime.
6. [x] Cập nhật dòng GS-03 trong `dd_screens/PLAN.md` và worklog. Kết quả `DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED`, vì loaded state/CTA/tab orchestration/#10 contract/UI router chưa đủ căn cứ.

### Kết quả static audit

- PASS: `list_screen.md`, master tracker và 83 thư mục nguồn có cùng 83 ID; GS-03 có đủ source, render, annotated image, marker map, plan và DD.
- PASS: JSON marker có #1–#10 duy nhất; bảng element DD ánh xạ đủ 10 ID; event IDs liên tục #01–#06; mọi Markdown link tương đối trong DD resolve.
- PASS: source hashes giữ nguyên; PNG là 1280×1024 (source), 1440×1200 (rendered), 3040×2400 (annotated); SVG có 10 circle/leader và embed đúng ảnh render.
- PASS: master tracker cập nhật GS-03 và next screen GS-04; `git diff --check` không báo lỗi.
- Tests và Study runtime không chạy/không xác minh.

### Điều kiện DD READY chưa đạt

- Chưa có visual contract cho loaded course detail, mentor/price blocks, curriculum/review states hoặc enrollment CTA.
- AC-05 và inventory khác nhau về thứ tự eager/lazy API calls.
- API #10 chưa có runtime source; rating/title thiếu source/schema.
- Guest CTA sang ST-04 cần policy identity/authentication/route handoff giải quyết.
- Study Web/router chưa được nối.

- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
