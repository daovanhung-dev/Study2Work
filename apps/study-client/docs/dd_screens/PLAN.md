# Kế hoạch chuyển 83 screen DD sang skill create_dd_screen

**Phạm vi đã chốt với người dùng:** dùng đúng 83 screen folder đang có dưới `screen_stitch/`; không tạo screen thứ 84. `list_screen.md` cũng công bố 83 mã duy nhất.

## Nguồn và trạng thái

- Inventory: [list_screen.md](../list_screen.md), §2 (83 mã).
- Mỗi màn: thư mục nguồn chứa `<ID>.md`, `<ID>_PLAN.md`, `screen.png`, `screen_annotated.png`, `<ID>_markers.json`; nội dung DD/plan nguồn là bằng chứng chi tiết và phải giữ nguyên.
- UI Web hiện được ghi nhận `UNWIRED`; route trong inventory là route thiết kế/đề xuất, không phải runtime đã xác minh. API references kế thừa status, discrepancy và blockers từ DD nguồn; không suy diễn từ ví dụ SH-01/SH-02 trong skill.
- Output theo 8 file của `.agents/skills/create_dd_screen/01-TEMPLATES/SCREEN_ID/`; mỗi package có `images/screen-clean.png` và `images/screen-numbered.png`.

## Quy tắc chuyển đổi

1. Dùng ID, tên, route, AC, API reference, orchestration, navigation, UI states, priority và gate đúng từ inventory hiện hành. Route giữ nhãn đề xuất khi inventory/source chưa xác minh runtime.
2. Chuyển section tương ứng từ `<ID>.md` sang 8 trách nhiệm của skill: overview, elements, events, data/state, API, business rules/gates, navigation, acceptance/test plan. Các ID nguồn và cách đánh dấu được giữ nguyên; không bịa contract hay test đã chạy.
3. Ảnh clean và numbered là bản sao byte-for-byte từ `screen.png` và `screen_annotated.png`. Mapping element/marker tham chiếu `<ID>_markers.json` và DD nguồn; không vẽ lại marker trong lần chuyển đổi này.
4. Mỗi tài liệu ghi links tương đối tới DD/plan/asset nguồn. Source excerpts được chuyển link tương đối theo vị trí output. Draft status là trạng thái package mới; trạng thái DD/implementation/runtime gốc được nêu riêng.
5. Không sửa source assets hoặc source DD. Không chạy app tests; chỉ chạy structural validator của skill và kiểm tra tĩnh số lượng/file/link/ảnh.

## Kết quả theo nhóm

| Nhóm | Mã | Số screen |
|---|---|---:|
| Shared/Auth/System | SH-01…SH-07 | 7 |
| Guest/Discovery | GS-01…GS-07 | 7 |
| Student | ST-01…ST-26 | 26 |
| Mentor | ME-01…ME-18 | 18 |
| Admin | AD-01…AD-25 | 25 |
| **Tổng** | **83 mã duy nhất** | **83** |

## Acceptance cho lần chuyển đổi

- [x] 83 package folder, mỗi folder đủ 8 Markdown + 2 ảnh; không có `{{...}}` chưa điền.
- [x] Source links tồn tại và đường dẫn Markdown nội bộ kiểm tra được.
- [x] 2 ảnh output khớp hash với 2 ảnh source; source tree không bị sửa bởi chuyển đổi.
- [x] Validator skill chạy trên 83 package; 83 PASS, 0 error, 0 warning sau khi mở rộng ID theo inventory.
- [x] Worklog cập nhật verification và context validator đã chạy; global validator drift được ghi rõ, không sửa ngoài phạm vi.
