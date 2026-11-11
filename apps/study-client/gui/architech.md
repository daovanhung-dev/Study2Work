# Kiến trúc Study Web

    STATUS: SKELETON_ONLY
    FRAMEWORK: ANGULAR 22
    RENDERING: CLIENT-SIDE SPA

## Mục đích và ranh giới hiện tại

Tài liệu này mô tả bộ khung Angular của Study Web và cấu trúc sẽ dùng khi triển khai các màn hình. Ứng dụng hiện chỉ hiển thị thông báo tạm thời cho biết bộ khung đã sẵn sàng. Chưa triển khai SH-01 hay màn hình nghiệp vụ, luồng xác thực, lời gọi API theo feature, lưu trữ dữ liệu hoặc hành vi phát hành ứng dụng. `core/http/StudyApiService` cung cấp transport generic tới `/api/v1`; Angular dev server proxy chuyển tiếp local request tới Study API `127.0.0.1:3003`. Transport này không xác nhận endpoint nghiệp vụ hoặc deployment đã được nối.

83 gói màn hình và các tài nguyên trong screen_stitch dưới docs/ là bằng chứng về yêu cầu và thiết kế. Các tuyến được đề xuất trong đó không chứng minh rằng tuyến đã được đăng ký khi ứng dụng chạy. Trước khi triển khai màn hình, hãy đối chiếu DD và các tham chiếu API với mã nguồn Study Server hiện tại cùng các hợp đồng có thể kiểm chứng. Ghi rõ những hành vi chưa được xác nhận.

Quy tắc bắt buộc về ranh giới giao diện, nghiệp vụ và truy cập dữ liệu nằm trong [agent context Study Web](../../../.agents/web-study/frontend-rules.md). Tài liệu này mô tả cấu trúc; rule trong agent context quy định cách triển khai và chiều phụ thuộc.

## Cấu trúc dự án

    apps/study-client/
    ├── angular.json                 # Cấu hình biên dịch, máy chủ phát triển và tài nguyên Angular CLI
    ├── proxy.conf.json              # Proxy local /api/v1 tới Study API
    ├── package.json                 # Các lệnh npm và gói phụ thuộc trực tiếp
    ├── package-lock.json            # Khóa cây gói phụ thuộc để các lần cài npm có kết quả nhất quán
    ├── tsconfig.json                # Tùy chọn TypeScript nghiêm ngặt dùng chung
    ├── tsconfig.app.json            # Cấu hình entry và phạm vi file TypeScript của ứng dụng
    ├── .editorconfig                # Quy tắc khoảng trắng và xuống dòng cho trình soạn thảo
    ├── .gitignore                   # Loại node_modules, bộ nhớ đệm Angular và sản phẩm biên dịch khỏi Git
    ├── .prettierrc                  # Quy ước định dạng mã
    ├── README.md                    # Lệnh chạy/biên dịch cục bộ và liên kết tới tài liệu này
    ├── public/                      # Tệp tĩnh được chép nguyên trạng vào đầu ra ứng dụng
    ├── gui/
    │   └── architech.md             # Kiến trúc, trách nhiệm thư mục và ranh giới
    └── src/
        ├── index.html               # Metadata tài liệu, ngôn ngữ tiếng Việt và phần tử gốc
        ├── main.ts                  # Khởi chạy thành phần gốc Angular độc lập
        ├── styles.css               # Token thiết kế Study, kiểu cơ sở và quy tắc nhận focus toàn cục
        └── app/
            ├── app.ts               # Thành phần gốc; nơi ghép vùng hiển thị của bộ định tuyến
            ├── app.html             # Thông báo bộ khung tạm thời và vùng hiển thị của bộ định tuyến
            ├── app.css              # Chỉ chứa kiểu của thành phần gốc
            ├── app.config.ts        # Provider Angular dùng chung toàn ứng dụng
            ├── app.routes.ts        # Tuyến cấp cao nhất; hiện để trống có chủ đích
            ├── core/                # Hạ tầng toàn ứng dụng, dịch vụ dùng chung và phần liên miền
            │   └── http/
            │       ├── api-envelope.ts       # Kiểu envelope Study API dùng chung
            │       └── study-api.service.ts  # HTTP transport generic cho /api/v1
            ├── layouts/             # Khung giao diện dùng chung cho một nhóm trang
            ├── shared/              # Thành phần trình bày dùng lại, không chứa quy tắc nghiệp vụ
            └── features/            # Năng lực nghiệp vụ, tách theo miền màn hình Study
                ├── auth/            # SH-02…SH-04
                ├── guest/           # SH-01 và GS-01…GS-07
                ├── system/          # SH-05…SH-07
                ├── student/         # ST-01…ST-26
                ├── mentor/          # ME-01…ME-18
                └── admin/           # AD-01…AD-25

Các tệp .gitkeep trong những thư mục kiến trúc còn trống chỉ giúp Git giữ lại cấu trúc dự kiến. Xóa từng tệp giữ chỗ khi thêm mã nguồn thật. Chỉ tạo thư mục con cho một tính năng khi bắt đầu triển khai năng lực tương ứng; không tạo module rỗng hoặc tệp API chỉ dựa trên suy đoán.

## Trách nhiệm

### Tệp cấu hình dự án và khởi chạy ứng dụng

| Đường dẫn | Trách nhiệm |
|---|---|
| angular.json | Khai báo ứng dụng Angular cùng các cấu hình biên dịch, chạy máy chủ phát triển và kiểm thử dự kiến. |
| package.json / package-lock.json | Khai báo lệnh npm, gói phụ thuộc và khóa chính xác cây gói. Giữ các gói phụ thuộc trong phạm vi ứng dụng; không tạo Git repository lồng nhau. |
| tsconfig*.json | Bật kiểm tra nghiêm ngặt cho TypeScript và khuôn mẫu Angular. Chỉ thêm cấu hình kiểm thử khi phạm vi công việc có kiểm thử. |
| public/ | Chứa tệp tĩnh dùng khi ứng dụng chạy, chẳng hạn favicon. Giữ ảnh chụp DD và bản xuất thiết kế trong docs/. |
| src/index.html | Khai báo tiêu đề tài liệu, ngôn ngữ, thông tin viewport và điểm gắn ứng dụng &lt;study-root&gt;. |
| src/main.ts | Gọi bootstrapApplication để khởi chạy thành phần gốc độc lập cùng cấu hình ứng dụng. |
| src/styles.css | Chứa token CSS toàn cục, đặt lại kiểu mặc định, kiểu chữ cơ sở, chỉ báo nhận focus và hành vi giảm chuyển động. Kiểu riêng của thành phần đặt cạnh thành phần đó. |
| README.md | Hướng dẫn nhà phát triển cài gói phụ thuộc, chạy và biên dịch ứng dụng. |

### Ranh giới trong src/app/

- app.ts, app.html và app.css ghép thành phần gốc của ứng dụng. Thông báo sẵn sàng chỉ là tạm thời, không phải màn hình SH-01.
- app.config.ts đăng ký provider Angular dùng toàn ứng dụng, gồm `provideHttpClient()` cho API transport. Chỉ thêm provider tại đây khi toàn ứng dụng cần dùng.
- app.routes.ts là danh sách đăng ký tuyến gốc. Hiện tệp này để trống; chỉ thêm tuyến cho màn hình đã triển khai và có bằng chứng từ mã nguồn. Khi bổ sung nhóm tính năng, nạp tệp tuyến của nhóm đó theo cách tải trễ.
- core/ quản lý hạ tầng toàn ứng dụng như cấu hình HTTP, transport API generic, tích hợp xác thực đã được xác minh, xử lý lỗi toàn cục và bộ chặn tuyến. Không đặt truy vấn hay chính sách riêng của nhóm tính năng trong core/. Hiện chưa có token store hoặc tích hợp xác thực Study Web.
- layouts/ quản lý khung giao diện dùng chung cho các tuyến, chẳng hạn khung công khai, đã xác thực, student, mentor hoặc admin. Khung giao diện sắp xếp điều hướng và vùng hiển thị trang; không sở hữu quy tắc nghiệp vụ hay truy cập dữ liệu của nhóm tính năng.
- shared/ quản lý thành phần trình bày tổng quát, chỉ thị, bộ biến đổi và tiện ích định dạng được nhiều miền dùng lại. Không được phụ thuộc vào nhóm tính năng, gọi API nghiệp vụ hoặc chứa quy tắc nghiệp vụ Study.
- features/ quản lý các năng lực Study. Đặt trang theo tuyến, giao diện miền, logic nghiệp vụ, truy cập dữ liệu và mô hình dữ liệu bên trong ranh giới của nhóm tính năng tương ứng.
- features/&lt;domain&gt;/&lt;capability&gt;/domain/ chỉ được tạo khi nhóm tính năng có quy tắc nghiệp vụ thuần cần tách khỏi giao diện và truy cập dữ liệu.

### Mẫu cấu trúc feature

Dùng cấu trúc sau khi triển khai một nhóm màn hình; chỉ tạo những thư mục mà nhóm tính năng thực sự cần:

    features/<domain>/<capability>/
    ├── pages/          # Thành phần trang độc lập gắn với tuyến
    ├── ui/             # Thành phần trình bày riêng của miền nghiệp vụ
    ├── domain/         # Quy tắc nghiệp vụ thuần; chỉ tạo khi feature cần
    ├── data-access/    # Lời gọi API và trạng thái dữ liệu từ server
    ├── models/         # Kiểu dữ liệu suy ra từ hợp đồng feature đã xác minh
    └── <capability>.routes.ts

Ánh xạ nhóm màn hình theo danh mục hiện tại: auth dành cho đăng ký và xác minh; guest dành cho Study công khai và khám phá nội dung; system dành cho trạng thái quyền truy cập, lỗi và vận hành; tiếp theo là student, mentor và admin. Chỉ tách miền thành các năng lực như courses, lessons, submissions hoặc reports khi bắt đầu công việc DD tương ứng. Tuyến xuất hiện trong danh mục vẫn chỉ là đề xuất cho đến khi phần triển khai và các gói phụ thuộc được xác minh.

## Luồng dữ liệu và cách ứng dụng vận hành

    main.ts -> app.config.ts -> app.routes.ts -> trang feature -> ui của feature
                                                         -> domain (khi feature có quy tắc nghiệp vụ)
                                                         -> data-access -> StudyApiService -> HttpClient -> /api/v1 -> Study API

`StudyApiService`, `HttpClient` và proxy local đã được cấu hình; chưa có feature `data-access` nào gọi endpoint. Proxy chỉ áp dụng cho `ng serve`; production cần định tuyến cùng origin `/api/v1`, hiện chưa được xác minh. Với từng màn hình, trước tiên xác minh tuyến Study Server hiện tại, cấu trúc yêu cầu/phản hồi, xác thực, mã lỗi và các kiểm thử liên quan. Không suy ra hành vi điểm cuối API từ bản phác giao diện, cũng không tự tạo trường dữ liệu hoặc tuyến API để lấp chỗ trống. Giữ mô hình dữ liệu bên trong nhóm tính năng đó, trừ khi có hợp đồng đã xác minh thực sự được dùng chung.

Dùng Angular Signals cho trạng thái giao diện đồng bộ tại chỗ và RxJS cho luồng bất đồng bộ khi đã bổ sung tích hợp API có căn cứ. Chưa thêm thư viện quản lý trạng thái toàn cục nếu chưa có nhu cầu cụ thể giữa nhiều nhóm tính năng. Bộ chặn tuyến phía trình duyệt chỉ phục vụ trải nghiệm điều hướng; quyền truy cập do máy chủ quyết định.

## Quy tắc giao diện và khả năng tiếp cận của Study Web

Dùng [hướng dẫn thiết kế Study Web](../../../.agents/web-study/design.md) làm nguồn chuẩn. Bộ token toàn cục:

| Token | Giá trị | Quy tắc |
|---|---|---|
| --ocean-primary | #0B5F8A | Nút hành động chính, điều hướng đang chọn, liên kết và vòng focus |
| --ocean-hover | #084968 | Trạng thái hover và nhấn của điều khiển chính |
| --ocean-deep | #073B57 | Tiêu đề nhấn mạnh và điểm màu tối |
| --sky-accent | #43A5C5 | Chỉ dùng làm điểm trang trí; không dùng làm dấu hiệu duy nhất truyền đạt ý nghĩa |
| --ocean-soft | #E8F4FA | Nền cho vùng được chọn và thông tin |
| --page-background | #F6FAFC | Nền chính của ứng dụng |
| --surface | #FFFFFF | Thẻ, biểu mẫu, menu và hộp thoại |
| --text-primary | #17324D | Tiêu đề và nội dung chính |
| --text-muted | #536A7A | Nội dung phụ và metadata |
| --border | #D4E2E9 | Đường phân cách nhẹ và ranh giới bề mặt |
| --success / --warning / --danger | #18794E / #8A4B08 / #B42318 | Mỗi màu trạng thái phải đi kèm chữ hoặc biểu tượng |

Lấy giao diện sáng làm nền tảng. Chỉ dùng Inter nếu font này đã có sẵn; nếu không, dùng chuỗi sans-serif của hệ thống. Không tải font từ xa hoặc thêm thư viện thành phần giao diện trong scaffold này. Dùng nhịp khoảng cách 4px, chiều rộng nội dung khoảng 1120px và lề co giãn 16px / 24px / 32px. Điều chỉnh bố cục tại các ngưỡng <768px, 768–1023px và >=1024px; không ẩn nội dung chính.

Điều khiển phải cao ít nhất 44px; điều khiển chỉ có biểu tượng phải đạt ít nhất 44×44px. Luôn hiển thị dấu nhận biết khi dùng bàn phím, dùng nút/liên kết đúng ngữ nghĩa, gắn nhãn với trường biểu mẫu, cung cấp văn bản thay thế có ý nghĩa và đạt tương phản WCAG AA. Không dùng riêng màu sắc để giải thích trạng thái. Tôn trọng tùy chọn prefers-reduced-motion; phản hồi thao tác cần tức thời và tránh chuyển động trang trí.

## Quy ước phát triển và xác minh

- Tạo thành phần và tuyến độc lập theo quy ước tên tệp Angular ngắn gọn năm 2025: thing.ts, thing.html, thing.css.
- Đặt kiểu của thành phần cạnh mã thành phần; chỉ dùng kiểu toàn cục cho token và hành vi thực sự áp dụng toàn ứng dụng.
- Khi công việc có phạm vi kiểm thử, cấu hình mục tiêu kiểm thử Angular và đặt các tệp *.spec.ts tập trung cạnh mã nguồn. Bộ khung này cố ý chưa có mục tiêu kiểm thử, tệp đặc tả kiểm thử hoặc nghiệp vụ.
- Dùng npm start để chạy môi trường phát triển cục bộ và npm run build để biên dịch bản phát hành. Đầu ra Angular trong dist/ là sản phẩm được tạo tự động, không phải mã nguồn.
