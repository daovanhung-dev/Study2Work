# Review / nghiệm thu DD Screen

## A. Nguồn và phạm vi
- [ ] ID, tên, route, owner, phiên bản, trạng thái được xác định.
- [ ] UI & yêu cầu nghiệp vụ đối chiếu bằng chứng; API đối chiếu contract thực tế.
- [ ] Không có secret/PII thật, không lẫn giả định vào dữ liệu đã xác nhận.

## B. UI và state
- [ ] 2 ảnh screen-clean/numbered cùng bố cục; mọi marker có EL ID.
- [ ] Mỗi element mô tả type, binding/source, visibility, enabled/disabled, event nếu tương tác.
- [ ] Có loading, success, empty, error, unauthorized, responsive nếu áp dụng.

## C. Event & dữ liệu
- [ ] Mọi thao tác & lifecycle đều được mô tả bằng Event ID.
- [ ] Mỗi event đủ input, guard, xử lý theo bước, output, ngoại lệ, retry.
- [ ] Mọi API call có request/response status mapping cụ thể.
- [ ] Có biện pháp chống double-submit/race/stale data khi thích hợp.
- [ ] State/DTO/ViewModel/derived values có nguồn và kiểu dữ liệu.

## D. Logic & navigation
- [ ] Business rules có ID, thứ tự ưu tiên, scope FE/BE.
- [ ] Route params, auth guard, navigation source/destination, back, deep link đầy đủ.
- [ ] Cross references đến screen đích đã tồn tại hoặc được ghi rõ là ngoài phạm vi.

## E. Test & tính nhất quán
- [ ] Happy path + negative + boundary + network/auth failure.
- [ ] Mỗi event/rule quan trọng có test ID.
- [ ] Không trùng ID, không hỏng đường dẫn Markdown/ảnh, không placeholder.
- [ ] Chạy `python3 03-TOOLS/validate_dd.py <folder>` và giải quyết mọi lỗi.

**Lưu ý:** validator tự động chỉ kiểm tra một tập con của checklist; review con người/đối chiếu repo vẫn là bắt buộc.
