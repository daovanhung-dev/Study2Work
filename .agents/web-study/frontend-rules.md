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
| `app.routes.ts`, `<capability>.routes.ts` | Khai báo tuyến; nạp route của feature theo cách tải trễ khi phù hợp. Chỉ đăng ký màn hình đã được xác nhận đủ yêu cầu và dependency. | Xử lý nghiệp vụ, gọi API trực tiếp hoặc quyết định quyền truy cập thay server. |
| `layouts/` | Tạo khung giao diện, điều hướng và vùng chứa trang cho nhóm tuyến. | Quy tắc nghiệp vụ, truy vấn riêng màn hình hoặc sở hữu trạng thái dữ liệu của feature. |
| `features/<domain>/<capability>/pages/` | Nhận tham số tuyến, ghép các thành phần UI, điều phối tương tác và trạng thái hiển thị của trang; chuyển thao tác sang `domain/` hoặc `data-access/`. | Tự viết quyết định nghiệp vụ, tính toán chính sách, gọi HTTP hoặc chứa toàn bộ giao diện của một màn hình lớn. |
| `features/<domain>/<capability>/ui/` | Hiển thị dữ liệu nhận vào, giữ trạng thái trình bày cục bộ và phát sự kiện người dùng để page xử lý. | Gọi API, phụ thuộc router/data-access, quyết định nghiệp vụ hoặc truy cập feature khác. |
| `features/<domain>/<capability>/domain/` | Khi có nhu cầu, chứa quy tắc nghiệp vụ thuần như tính toán, chính sách, validation nghiệp vụ và chuyển trạng thái. Giữ logic có thể kiểm thử độc lập. | HTTP, database, router, DOM, trạng thái Angular hoặc side effect bên ngoài. Không tạo thư mục này khi feature chưa có quy tắc nghiệp vụ cần tách. |
| `features/<domain>/<capability>/data-access/` | Thực hiện truy cập API của feature qua hạ tầng `core/`, điều phối tác vụ bất đồng bộ, quản lý trạng thái dữ liệu từ server và chuyển đổi DTO theo contract đã xác minh. | Thành phần giao diện, thao tác DOM hoặc quyết định chính sách nghiệp vụ. |
| `features/<domain>/<capability>/models/` | Khai báo kiểu dữ liệu dựa trên API contract hoặc DD đã được xác nhận. Tách kiểu truyền tải khỏi kiểu miền nếu hình dạng khác nhau. | Field, trạng thái, mã lỗi hoặc ý nghĩa nghiệp vụ được suy đoán. |
| `core/` | Cung cấp hạ tầng kỹ thuật dùng xuyên feature như cấu hình HTTP, xử lý lỗi dùng chung và tích hợp auth đã được xác minh. | API client, model, policy hoặc trạng thái riêng một feature. |
| `shared/` | Cung cấp UI primitive và tiện ích trung lập được ít nhất hai miền dùng chung. Giữ thành phần trình bày độc lập với nghiệp vụ Study. | Import feature, API nghiệp vụ, model miền hoặc logic theo vai trò người dùng. |

Kiểm tra dữ liệu biểu mẫu ở `ui/` chỉ được phục vụ cách nhập và cách hiển thị lỗi. Validation quyết định một thao tác nghiệp vụ có hợp lệ hay không thuộc `domain/`, dựa trên yêu cầu đã xác minh.

## 3. Chiều phụ thuộc

Tuân theo luồng sau; không đảo chiều để tiện triển khai:

    app.routes.ts -> feature routes -> pages -> ui
                                      ├──> domain -> kiểu miền trong models
                                      └──> data-access -> core HTTP -> API đã xác minh

- `pages/` được dùng các lớp trong cùng capability và UI dùng chung từ `shared/`; page không gọi HTTP trực tiếp.
- `ui/` chỉ nhận dữ liệu và phát sự kiện; không phụ thuộc `domain/`, `data-access/`, `core/` hoặc router.
- `domain/` chỉ phụ thuộc kiểu miền trung lập và mã TypeScript thuần; không phụ thuộc Angular hay I/O.
- `data-access/` được dùng hạ tầng `core/` và các kiểu contract của feature; chuyển đổi dữ liệu tại ranh giới API khi cần.
- `layouts/`, `core/` và `shared/` không import mã nội bộ từ `features/`. Một feature không import trực tiếp implementation của feature khác.
- Chỉ chuyển phần dùng chung ra khỏi feature khi có nhu cầu thật và ranh giới trung lập đã được xác định; không dùng `shared/` làm nơi chứa nghiệp vụ chung cho tiện.

## 4. Trách nhiệm các feature Study

Các thư mục dưới đây nhóm phạm vi theo inventory DD hiện tại. Đây là ranh giới tổ chức mã, không xác nhận tính năng đã được triển khai hoặc route đã hoạt động.

| Feature | Phạm vi dự kiến theo inventory |
|---|---|
| `auth/` | Đăng ký và xác minh, tham chiếu SH-02…SH-04. |
| `guest/` | Study công khai và khám phá nội dung, tham chiếu SH-01, GS-01…GS-07. |
| `system/` | Trạng thái truy cập, lỗi và vận hành, tham chiếu SH-05…SH-07. |
| `student/` | Năng lực dành cho học viên, tham chiếu ST-01…ST-26. |
| `mentor/` | Năng lực dành cho mentor, tham chiếu ME-01…ME-18. |
| `admin/` | Năng lực dành cho quản trị viên, tham chiếu AD-01…AD-25. |

Chỉ tạo capability con khi bắt đầu triển khai DD tương ứng. Giữ page, UI, domain, data access và models trong cùng feature; không gom chúng thành một thư mục toàn cục theo loại màn hình.

## 5. Quy tắc trước khi nối hành vi

1. Xác định feature, capability và DD liên quan; kiểm tra source hiện tại trước khi sửa.
2. Với route/API, truy dấu Study Server source và contract để xác minh method, path, request/response, auth và mã lỗi. Nếu thiếu bằng chứng, ghi `SOURCE_REQUIRED` hoặc `UNWIRED` và dừng ở placeholder phù hợp.
3. Đặt UI theo đúng lớp; đặt quy tắc nghiệp vụ trong `domain/` và I/O trong `data-access/`. Không để component quyết định policy.
4. Bổ sung kiểm thử phù hợp khi thay đổi logic nghiệp vụ hoặc chuyển đổi dữ liệu API trong phạm vi có thể kiểm thử. Hiện scaffold chưa có test target; không tuyên bố đã kiểm thử nếu chưa có cấu hình chạy được.
5. Cập nhật `gui/architech.md` và context liên quan trong cùng task nếu thay đổi ranh giới kiến trúc hoặc cách tổ chức thư mục.

## 6. Điều kiện chấp nhận khi review

- Component trình bày không gọi API, router hoặc service nghiệp vụ.
- Page chỉ điều phối màn hình; quyết định nghiệp vụ nằm trong `domain/`, I/O nằm trong `data-access/`.
- Không có dependency từ `shared/`, `core/` hoặc `layouts/` vào feature.
- Các kiểu dữ liệu và hành vi API truy ngược được tới contract/source đã xác minh; nội dung DD/mockup vẫn được đánh dấu là yêu cầu khi runtime chưa có.
- Mỗi thư mục mới có trách nhiệm cụ thể; không tạo thư mục hoặc module rỗng ngoài nhu cầu đã xác định.
