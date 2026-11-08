# Quy trình tạo mới DD screen — chuẩn thực thi

## 0. Chuẩn bị nguồn dữ liệu

**Input bắt buộc:** (1) Screen ID/tên/mục tiêu; (2) ảnh thiết kế hoặc màn hình thực tế; (3) các luồng người dùng; (4) nguồn API/schema hoặc ghi rõ chưa xác nhận; (5) màn hình trước/sau, route và quyền truy cập.

**Nếu có repository:** khảo sát entrypoint, router, components, state store, services/API client, types/schema, authentication, permissions, test, những DD screen có liên quan. Ghi **đường dẫn file, symbol, version/commit** làm chứng cứ. Không coi tên endpoint trong mockup là API thật.

## 1. Đăng ký screen

- Đối chiếu `screen-index.md`, đảm bảo Screen ID chưa trùng.
- Đặt tên folder `SH-XX-FeatureName`; route có thể chứa params, ví dụ `/courses/:courseId`.
- Ghi Screen ID, tên, module, thiết bị/viewport, phiên bản, trạng thái DD (Draft / Review / Approved), owner, nguồn.

## 2. Chuẩn hóa ảnh

- Lưu `images/screen-clean.png` (ảnh nguyên trạng), `images/screen-numbered.png` (cùng ảnh, thêm marker rõ ràng).
- Đánh số các thành phần **nhìn thấy trong trạng thái ảnh** theo thứ tự trái→phải, trên→dưới, có thể nhóm vùng hợp lý.
- Ảnh một trạng thái không đủ để thể hiện loading/error/modal: bổ sung ảnh state tùy chọn `state-*.png` và mô tả trạng thái ở UI file.
- Viết mapping: `#1 → SH-XX-EL-001`, `#2 → SH-XX-EL-002`... Không đánh số riêng cho từng card cùng một loại, trừ khi hành vi khác nhau.

## 3. Điền 8 file theo thứ tự phù hợp

1. `00-overview.md`: mục tiêu, actor, điều kiện, use cases, nguồn thông tin.
2. `01-ui-elements.md`: đi từng marker trên ảnh; thêm phần tử ẩn có điều kiện; phân biệt visible/conditional.
3. `05-business-rules.md`: chốt các quyết định nghiệp vụ, phạm vi áp dụng, chỗ thực thi FE/BE.
4. `04-api-integration.md`: trích hợp đồng thật từ OpenAPI/backend; request/response/error, auth, mapping; không tự phỏng đoán.
5. `03-data-flow.md`: state, DTO/ViewModel, luồng load và mutate, cache, race condition, pagination.
6. `02-events.md`: **cho mỗi Event**: trigger → guard → input source → validation → từng bước → API/data processing → UI/state → navigation → lỗi/ngoại lệ; link BR/API.
7. `06-navigation.md`: entry/exit, params, guard, back behavior, invalid deep-link.
8. `07-test-cases.md`: bao phủ mọi event, rule, trạng thái, lỗi quan trọng, request đồng thời.

**Lý do thứ tự này:** viết rule/contract/state trước rồi mới chi tiết từng event, tránh để event phải tự phát minh nghiệp vụ.

## 4. Mẫu traceability (truy xuất)

```text
Ảnh #3 → EL-003 (Search Input)
           → EV-002 (On keyword change)
               → BR-001 (Normalize keyword)
               → API-001 (GET /courses)
               → Data Flow (update items/total)
           → TC-002, TC-003 (success/empty), TC-004 (race condition)
```

Quy tắc: mỗi UI tương tác phải có Event ID; mỗi event gọi API phải có API ID; mỗi BR quan trọng phải có test; mỗi điều hướng phải có destination được xác định.

## 5. Rà soát 3 vòng

- **Vòng UI:** đối chiếu từng marker với ảnh; responsive, loading, empty, error, disabled.
- **Vòng kỹ thuật:** đối chiếu route/response/DTO/authorization với source/contract; toàn bộ event đủ input, handling, output, race condition.
- **Vòng QA:** happy path + negative + boundary + permissions + network failure + retry + stale results.

Chạy script `validate_dd.py`, giải quyết lỗi trước khi review. Chỉ đánh trạng thái `Approved` khi các quyết định quan trọng đã được xác nhận, bằng chứng đã rà soát, checklist đạt.

## 6. Cập nhật sau khi code thay đổi

- Một thay đổi API contract: cập nhật API, data-flow, events và test liên quan.
- Một thay đổi UI: cập nhật ảnh và elements, soát lại events.
- Một thay đổi rule: cập nhật business-rules, events, test.
- Ghi changelog ngắn trong `00-overview.md`: ngày, thay đổi, người/nguồn xác nhận.

## 7. Khi còn thiếu thông tin

Sử dụng khối rõ ràng:

```md
> CẦN_XÁC_NHẬN [Q-01]: API đăng ký khóa học có idempotency key hay không?
> Nguồn cần đối chiếu: backend/routes/enrollments.py, OpenAPI.
> Tác động: EV-004 / API-002 / TC-006.
> Người phụ trách: Backend.
```

Không viết phỏng đoán thành đặc tả chính thức. Nếu nhiều luồng chưa rõ, DD có thể tiếp tục ở trạng thái Draft.

## 8. Điều kiện hoàn thành (Definition of Done)

- [ ] Đúng 8 file với nội dung hợp lệ, không còn dấu placeholder `{{...}}`.
- [ ] Có ảnh clean và numbered, marker khớp với element.
- [ ] Event bao phủ mọi tương tác, lifecycle và lỗi cần thiết.
- [ ] API, rule, navigation, data mapping truy xuất hai chiều được.
- [ ] Có test cho main flow, error, empty, auth, boundary/race nếu áp dụng.
- [ ] Không còn `CẦN_XÁC_NHẬN` nghiêm trọng khi chuyển Approved.
- [ ] Source references đã được kiểm chứng, version/commit được ghi.
