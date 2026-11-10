# ME-15 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `ME-15-TC-001` | Planning ref / not run | `AC-25` | See source acceptance section | P2 |

## 2. Test planning references

### ME-15-TC-001 — Acceptance planning reference (AC-25)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [ME-15](../../screen_stitch/04_mentor/ME-15_theo-doi-gui-thong-bao/ME-15.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-25`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/04_mentor/ME-15_theo-doi-gui-thong-bao/ME-15.md).

## 3. Source acceptance / test plan (not run)

### Trích từ DD nguồn: F. Tiêu chí nghiệm thu

- [x] Plan được lập trước marker map/annotated image/DD.
- [x] 54 marker tuần tự được lưu trong `ME-15_markers.json`; mỗi marker có một element row trong mục C.
- [x] Original `screen.png` và `code.html` được giữ nguyên; hash gốc được ghi ở mục A và plan.
- [x] UI static claims được tách khỏi current backend behavior.
- [x] API #64 được đối chiếu với route, model, parser, view, query, API design và AC-25; status/error mapping có nguồn.
- [x] API #63 handoff phân biệt Operation UUID với notification ID list.
- [x] API #18 được đánh dấu unwired và không được thay thế bằng #64.
- [x] Mọi anchor, refresh timer/toast, static step/channel/report, auth/error/session, empty state và navigation gap được mô tả.
- [x] Đã ghi unresolved states, channel receipts, polling/retry policy, batch selection và UI routing là blocker; không tự tạo contract.
- [ ] Product/API owner chốt một ID cho ME-15 hoặc batch semantics.
- [ ] Product/API owner thống nhất `queued/sending/complete/failed` với `QUEUED/FAILED/SENT`.
- [ ] Có contract/API cho channel/recipient report, ACK và real-time nếu các vùng này phải phản ánh runtime.
- [ ] Study Web router/auth/API client và destination links được triển khai; cần runtime verification riêng.

**Trạng thái cuối:** `DD READY`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`. Đây là ba đánh giá độc lập. Local source/tests của API #64 không chứng minh production schema, delivery worker/provider hoặc frontend end-to-end.

#### Kế hoạch kiểm chứng từ source PLAN

### Trích từ DD nguồn: 8. Tiêu chí kết thúc phiên

- Đủ bốn artifact cốt lõi: `screen_annotated.png`, `ME-15.md`, `ME-15_PLAN.md`, `ME-15_markers.json`; giữ nguyên `screen.png` và `code.html`.
- 100% marker map có mô tả chính xác trong DD; event/API/ID/state discrepancies được truy vết.
- Cập nhật tracker/worklog sau kiểm tra.
- Không bắt đầu `ME-16`.
- Chỉ ghi `DD READY` nếu tài liệu đủ implementable và các unresolved requirement được phân định rõ; ghi riêng `IMPLEMENTATION BLOCKED` và `RUNTIME NOT VERIFIED` khi tương ứng.

- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
