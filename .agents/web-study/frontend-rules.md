# Bộ quy tắc bắt buộc cho Study Web

    SCOPE: apps/study-client/
    FRAMEWORK: ANGULAR 22
    AUTHORITY: REQUIRED_FOR_STUDY_WEB_IMPLEMENTATION

## 1. Phạm vi và mức độ bắt buộc

Áp dụng riêng cho Study Web Angular. Agent phải đọc trang này trước khi thực hiện coding, fix, test, review hoặc thay đổi tài liệu kiến trúc trong `apps/study-client/`. Các từ **BẮT BUỘC**, **KHÔNG ĐƯỢC** và **CHỈ KHI** là quy tắc phải tuân thủ. Ngoại lệ phải có yêu cầu được người dùng chấp thuận và ghi rõ trong task.

Luôn phân biệt yêu cầu với hiện trạng: DD, ảnh thiết kế và `design.md` mô tả mục tiêu; chúng không chứng minh màn hình, tuyến, API hoặc hành vi đã chạy. Trước khi nối giao diện với nghiệp vụ/API, kiểm tra mã nguồn và contract hiện hành. Không tự tạo route, field, validation, quyền truy cập hoặc phản hồi API để lấp chỗ trống.

## 2. Trách nhiệm từng lớp

| Phần | Trách nhiệm bắt buộc | Không được đặt tại đây |
|---|---|---|
| `app.ts`, `app.html`, `app.css` | Ghép khung gốc và vùng hiển thị tuyến; giữ thông báo scaffold cho đến khi có yêu cầu màn hình đã xác minh. | Quy tắc nghiệp vụ, truy vấn dữ liệu hoặc logic riêng của feature. |
| `app.routes.ts`, `<group>.route.ts` | `app.routes.ts` ghép route theo group/layout; mỗi group có đúng một `<group>.route.ts` khai báo các màn hình thuộc group đó. Chỉ đăng ký route đã được xác nhận đủ yêu cầu và dependency. | Xử lý nghiệp vụ, gọi API trực tiếp hoặc quyết định quyền truy cập thay server. |
| `layouts/` | Tạo khung giao diện, điều hướng và vùng chứa trang cho nhóm tuyến. | Quy tắc nghiệp vụ, truy vấn riêng màn hình hoặc sở hữu trạng thái dữ liệu của feature. |
| `features/<group>/<SCREEN_ID>/pages/` | Chứa component trang chính của screen, nhận tham số, điều phối event/luồng hiển thị và trạng thái của screen; gọi `data-access/` qua component/page boundary. | Gọi HTTP trực tiếp, chứa widget nhỏ dùng riêng lẻ hoặc tự quyết định policy chưa có trong DD/contract. |
| `features/<group>/<SCREEN_ID>/ui/` | Chứa UI nhỏ thuộc riêng screen như popup/dialog, hiển thị input và phát event cho page xử lý. | Gọi API, phụ thuộc router/data-access hoặc import screen khác. |
| `features/<group>/<SCREEN_ID>/data-access/` | Chứa `*.service.ts` lấy/gửi dữ liệu bên ngoài qua `core/` theo API/contract đã xác minh; giữ nguyên raw response tại ranh giới này. | Component UI, thao tác DOM, field/API tự suy đoán hoặc quy tắc quyền do client tự quyết. |
| `features/<group>/<SCREEN_ID>/models/` | Chứa kiểu dữ liệu của screen và logic lọc/chuyển đổi dữ liệu nhận từ `data-access/` theo contract đã xác minh; thường dùng `*.models.ts`. | Field, trạng thái, enum, lỗi hoặc ý nghĩa nghiệp vụ chưa có nguồn xác nhận. |
| `core/` | Cung cấp hạ tầng kỹ thuật dùng xuyên feature như cấu hình HTTP, xử lý lỗi dùng chung và tích hợp auth đã được xác minh. | API client, model, policy hoặc trạng thái riêng một feature. |
| `src/app/shared/` | Cung cấp component/tiện ích trung lập được nhiều screen tái sử dụng; kiểm tra và dùng lại nơi đây trước khi tạo bản sao. | Import screen/feature, API nghiệp vụ, model riêng một screen hoặc logic theo vai trò người dùng. |

Trong mỗi `features/<group>/<SCREEN_ID>/` phải có đúng bốn thư mục con trực tiếp: `data-access/`, `models/`, `pages/`, `ui/`. Không tạo thêm `domain/`, `components/`, `services/` hay folder thứ năm trong screen. Đặt file TypeScript component chính cùng template `.html` và stylesheet `.css` trong `pages/`, đặt tên nhất quán theo screen ID. Nếu yêu cầu không thể triển khai đúng trong bốn trách nhiệm này, ghi rõ design gap trong plan trước khi code; không tự mở rộng cấu trúc.

## 3. Nhóm screen, route và layout

Nhóm mã theo inventory Study Web hiện tại:

- `features/shared/`: nhóm Shared / Auth / System, gồm các screen mã `SH-*`.
- `features/guest/`: Guest / Discovery, gồm `GS-*`.
- `features/student/`: học viên, gồm `ST-*`.
- `features/mentor/`: mentor, gồm `ME-*`.
- `features/admin/`: quản trị, gồm `AD-*`.

Tên folder screen dùng mã compact như `SH02`, tương ứng screen ID `SH-02` trong catalog/DD. Trong từng group, mỗi screen có folder riêng theo mã này.

Mỗi group có một route file duy nhất đặt tại `features/<group>/<group>.route.ts` (đuôi `.route.ts` số ít), khai báo route của tất cả screen trong group. Mỗi group cũng có một layout riêng tại `layouts/<group>/`; layout là shell chung có vùng `RouterOutlet`, và các screen được nạp bên trong layout qua group route. `app.routes.ts` chỉ ghép các group layout/route đã được xác nhận.

Screen-local popup/component nằm trong folder `ui/` của screen. Component thật sự dùng lại giữa nhiều screen đặt tại `src/app/shared/`; trước khi tạo component mới phải tìm component có sẵn và nêu kết quả reuse trong implementation plan. Layout không sở hữu data-access hoặc business state riêng từng screen.

## 4. Chiều phụ thuộc

Tuân theo luồng sau; không đảo chiều để tiện triển khai:

    app.routes.ts -> layouts/<group>/ -> features/<group>/<group>.route.ts
                                      -> features/<group>/<SCREEN_ID>/pages/
                                         ├──> ui/ -> event về page
                                         ├──> models/ -> kiểu/lọc/chuyển đổi dữ liệu
                                         └──> data-access/ -> core HTTP -> API đã xác minh

- `pages/` có thể dùng `ui/`, `models/` và `data-access/` trong cùng screen; page không gọi HTTP trực tiếp.
- `ui/` chỉ trình bày dữ liệu và phát event; không phụ thuộc router, `data-access/`, `core/` hoặc screen khác.
- `data-access/` dùng hạ tầng `core/` và contract đã xác minh; `models/` chuyển đổi/filter dữ liệu theo contract.
- `layouts/`, `core/` và `src/app/shared/` không import mã nội bộ của feature/screen. Một screen không import trực tiếp implementation của screen khác.
- DD route là thiết kế. Chỉ đăng ký route khi yêu cầu, dependency và behavior cần thiết đã được xác minh; không xem route trong catalog là runtime route.

## 5. Quy tắc trước khi nối hành vi

1. Xác định screen/group/API scope; đọc source hiện tại, DD và design guide trước khi sửa.
2. Với route/API, truy dấu Study Server source/test và contract để xác minh method, path, request/response, auth, permission và mã lỗi. Nếu thiếu bằng chứng, ghi `SOURCE_REQUIRED`, `UNWIRED` hoặc `DISCREPANCY`; không lấp gap bằng giả định.
3. Screen orchestration thuộc `pages/`; child UI thuộc `ui/`; I/O thuộc `data-access/`; typing, filtering và data mapping thuộc `models/`. Không tạo folder thứ năm cho screen.
4. Đưa component dùng lại giữa nhiều screen vào `src/app/shared/`; không chuyển một component screen-local sang shared chỉ vì nó có thể được tổng quát hóa trong tương lai.
5. Viết/chạy kiểm thử theo DD khi coding screen. Nếu Angular test target chưa có, thêm cấu hình test phù hợp trong implementation scope hoặc ghi `DECLARED_NOT_RUNNABLE`; không tuyên bố đã test.
6. Cập nhật `gui/architech.md` và context liên quan trong task triển khai khi source thực sự áp dụng cấu trúc mới.

## 6. Workflow coding screen

Trước mọi coding/fix/test/demo theo một screen, agent phải làm theo workflow đã đăng ký `study-web-screen-coding`: [quy trình implement screen Study Web](../web-work/study/workflows/screen-implementation.md). Quy trình đó quy định việc đọc DD 8 phần và ảnh, đối chiếu HTML tham khảo, viết plan, kiểm tra reuse, xác minh event/API/data flow, chạy test/demo và dọn fixture.

## 7. Điều kiện chấp nhận khi review

- Mỗi screen chỉ có bốn folder con trực tiếp: `data-access/`, `models/`, `pages/`, `ui/`.
- Group route và layout được khai báo riêng cho `shared`, `guest`, `student`, `mentor`, `admin`; `shared` bao gồm Shared/Auth/System.
- Component UI không gọi API hoặc router; page điều phối event và gọi data-access qua ranh giới đã nêu.
- Không có dependency từ `src/app/shared/`, `core/` hoặc `layouts/` vào feature/screen.
- Các kiểu dữ liệu và hành vi API truy ngược được tới contract/source đã xác minh; nội dung DD/mockup vẫn được đánh dấu là yêu cầu khi runtime chưa có.
- Test case và demo của DD có bằng chứng; fixture database chỉ được tạo trong DB local/test cô lập và đã được dọn/xác minh sau demo.
