# ST-03 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `ST-03-TC-001` | Planning ref / not run | `AC-11` | See source acceptance section | P1 |

## 2. Test planning references

### ST-03-TC-001 — Acceptance planning reference (AC-11)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [ST-03](../../screen_stitch/03_student/ST-03_chinh-sua-ho-so-avatar/ST-03.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-11`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/03_student/ST-03_chinh-sua-ho-so-avatar/ST-03.md).

## 3. Source acceptance / test plan (not run)

### Trích từ DD nguồn: H. Tiêu chí nghiệm thu

- [x] Một hàng element cho từng marker 1–26; bản đồ marker ghi đúng ST03-EL-01…ST03-EL-26.
- [x] Bao quát các tương tác/nội dung tĩnh theo source HTML và phân biệt disabled/readonly.
- [x] Event có input, precondition, sequence, API/business code khi áp dụng, output và giới hạn hiện tại.
- [x] Đối chiếu API #04/#13/#14 với router/module/model/validator/query/backend contract.
- [x] Ghi rõ khác nhau giữa inventory/AC/API contract và current source; không tự hòa giải.
- [x] Ghi trạng thái DD, implementation và runtime riêng.
- [ ] Contract bio/phone/avatar, refresh-after-save và partial upload failure được quyết định.
- [ ] Study Web loaded/error/route/session behavior được triển khai và xác minh.
- [ ] Live schema/Object Storage và runtime end-to-end được xác minh.
- [ ] Không còn blocker để lập trình viên triển khai theo một contract duy nhất.

#### Kế hoạch kiểm chứng từ source PLAN

### Trích từ DD nguồn: 5. Output, acceptance và verification

- Đã tạo `ST-03_PLAN.md` trước DD/annotation; giữ nguyên hai source assets và đối chiếu hash trước/sau.
- Đã tạo `ST-03_markers.json`, SVG overlay, `screen_annotated.png`, và `ST-03.md`; marker order/Element ID ánh xạ 1:1. Không đánh dấu data-only text thành event hoặc disabled controls thành hoạt động.
- `ST-03.md` bao gồm overview, expected/current flow, 26 elements, 9 events, current API #04/#13/#14 mapping/errors/effects, state/navigation matrix, security/privacy, discrepancies và acceptance checklist.
- Đã đọc test source #13/#14 nhưng không chạy test theo yêu cầu; ghi rõ test fake storage/session và DDL không chứng minh live S3, DB schema/deployment hay Study Web runtime.
- Đã cập nhật global tracker: ST-03 có trạng thái DD/implementation/runtime riêng; 16/83 artifact bundles, còn 67; điểm tiếp tục W1 là ST-08. Không bắt đầu Screen ID tiếp theo trong phiên này.
- Giữ `DD BLOCKED` vì bio/phone/avatar mapping và reload contract chưa khóa; `IMPLEMENTATION BLOCKED` vì Study Web không có app runtime và thiết kế gate giữ thao tác save/upload disabled; `RUNTIME NOT VERIFIED` vì không chạy client/live S3/production DB.

- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
