# Kiến trúc Study Web

    STATUS: ROOT_READINESS_AND_ROUTED_ADMIN_PRESENTATION_UI
    FRAMEWORK: ANGULAR 22
    RENDERING: CLIENT-SIDE SPA

## Mục đích và ranh giới hiện tại

Tài liệu này mô tả bộ khung Angular của Study Web và cấu trúc triển khai màn hình. App root chỉ chứa `RouterOutlet`; `/` lazy-load route readiness scaffold trong `features/system`, còn `/admin` và `/admin/users` dùng chung `AdminLayout` lần lượt hiển thị AD-01 và AD-02. Cả hai trang Admin đều presentation-only; AD-02 có bảng rỗng và điều khiển tìm kiếm/lọc/phân trang disabled. API #68, dữ liệu người dùng, enum role/status, auth guard và quyền Admin chưa được nối hoặc xác minh; DD/API #68 vẫn blocked. Điều hướng UI không phải access control. System root scaffold không phải SH-01. Chưa triển khai luồng xác thực, lưu trữ dữ liệu hoặc hành vi phát hành ứng dụng. `core/http/StudyApiService` cung cấp transport generic tới `/api/v1`; Angular dev server proxy chuyển tiếp local request tới Study API `127.0.0.1:3003`. Transport này không xác nhận endpoint nghiệp vụ hoặc deployment đã được nối.

`core/constant/api.constants.ts` chứa registry descriptor Study API theo catalog; `core/http/StudyApiService` dùng registry này để gửi request generic tới `/api/v1`. Registry ghi trạng thái đối chiếu source hiện tại, không tự chứng minh feature callsite hoặc deployment đã được nối.

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
            ├── app.html             # Chỉ chứa vùng hiển thị của bộ định tuyến
            ├── app.css              # Chỉ chứa kiểu của thành phần gốc
            ├── app.config.ts        # Provider Angular dùng chung toàn ứng dụng
            ├── app.routes.ts        # Lazy-load route groups system và admin
            ├── core/                # Hạ tầng toàn ứng dụng, dịch vụ dùng chung và phần liên miền
            │   ├── constant/
            │   │   └── api.constants.ts      # Registry descriptor Study API
            │   └── http/
            │       ├── api-envelope.ts       # Kiểu envelope Study API dùng chung
            │       └── study-api.service.ts  # HTTP transport generic cho /api/v1
            ├── layouts/             # Khung giao diện dùng chung cho một nhóm trang
            │   ├── admin/           # Outlet shell cho các route Admin
            │   └── system/          # Outlet shell cho route readiness ở /
            ├── shared/              # Thành phần trình bày dùng lại, không chứa quy tắc nghiệp vụ
            │   └── ui/study-icon.*  # Icon trung lập dùng trong Admin shell và AD-02
            └── features/            # Nhóm màn hình Study
                ├── shared/          # SH-* / Auth / System screens theo inventory
                ├── guest/           # GS-*
                ├── student/         # ST-*
                ├── mentor/          # ME-*
                ├── system/          # Route readiness tại /; không đại diện SH-01
                │   ├── system.routes.ts
                │   └── pages/system-readiness-page.*
                └── admin/           # AD-*
                    ├── admin.routes.ts
                    ├── AD01/        # data-access/, models/, pages/, ui/
                    └── AD02/        # data-access/, models/, pages/, ui/; presentation-only

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

- app.ts, app.html và app.css ghép thành phần gốc của ứng dụng. App root chỉ render `RouterOutlet`; readiness page được route riêng tại `/`, không phải màn hình SH-01.
- app.config.ts đăng ký provider Angular dùng toàn ứng dụng, gồm `provideHttpClient()` cho API transport. Chỉ thêm provider tại đây khi toàn ứng dụng cần dùng.
- app.routes.ts lazy-load `system.routes.ts` cho `/` và `admin.routes.ts` cho `/admin`; `admin.routes.ts` hiển thị AD-01 ở `/admin` và AD-02 ở `/admin/users`. Không có wildcard, route SH-05/SH-06, auth guard hoặc API route.
- core/ quản lý hạ tầng toàn ứng dụng như registry descriptor trong `constant/api.constants.ts`, cấu hình HTTP, transport API generic trong `http/`, tích hợp xác thực đã được xác minh, xử lý lỗi toàn cục và bộ chặn tuyến. Không đặt truy vấn hay chính sách riêng của nhóm tính năng trong core/. Hiện chưa có token store hoặc tích hợp xác thực Study Web.
- layouts/ quản lý khung giao diện dùng chung cho các tuyến, chẳng hạn khung công khai, đã xác thực, student, mentor hoặc admin. Khung giao diện sắp xếp điều hướng và vùng hiển thị trang; không sở hữu quy tắc nghiệp vụ hay truy cập dữ liệu của nhóm tính năng.
- shared/ quản lý thành phần trình bày tổng quát, chỉ thị, bộ biến đổi và tiện ích định dạng được nhiều miền dùng lại. Không được phụ thuộc vào nhóm tính năng, gọi API nghiệp vụ hoặc chứa quy tắc nghiệp vụ Study.
- features/ quản lý screen theo nhóm `shared`, `guest`, `student`, `mentor` và `admin`. `features/system` chỉ giữ route readiness root được yêu cầu cho scaffold; các SH-* screen vẫn thuộc group `shared`. Mỗi screen có đúng bốn thư mục con trực tiếp: `data-access/`, `models/`, `pages/` và `ui/`.
- pages/ chứa page component; ui/ chứa widget riêng của screen; data-access/ chỉ chứa I/O theo API đã xác minh; models/ chứa kiểu/chuyển đổi bám theo contract đã xác minh. Không tạo `domain/` hoặc folder thứ năm trong screen.
- Mỗi nhóm có một route file và một layout. Theo yêu cầu cụ thể của task, route files ở đây dùng tên `admin.routes.ts` và `system.routes.ts`; các tên SH-* khác vẫn theo cấu trúc canonical. `AdminLayout` sở hữu header, điều hướng, breadcrumb, footer và outlet cho AD01Page/AD02Page. `/admin/users` là route presentation-only: không gọi API #68, không có bản ghi hoặc enum lọc, không thêm auth; route không xác thực quyền.

### Mẫu cấu trúc feature

Dùng cấu trúc sau khi triển khai một nhóm màn hình; chỉ tạo những thư mục mà nhóm tính năng thực sự cần:

    features/<group>/<SCREEN_ID>/
    ├── data-access/    # I/O theo contract hiện hành; có thể chưa cần khi chưa có API
    ├── models/         # Kiểu/chuyển đổi theo contract đã xác minh
    ├── pages/          # Component trang chính và stylesheet/template cạnh nó
    └── ui/             # Component UI chỉ dùng trong screen

Tên thư mục screen dùng mã compact như `AD01` cho screen ID `AD-01`. Tuyến trong catalog/DD vẫn là đề xuất cho đến khi requirements, dependencies và runtime behavior được xác minh. Không tạo service/model/API riêng cho màn hình chỉ để lấp contract gap.

## Luồng dữ liệu và cách ứng dụng vận hành

    main.ts -> app.config.ts -> app.routes.ts -> layout/group route -> page -> ui
                                                                   -> models (nếu có contract)
                                                                   -> data-access -> StudyApiService -> HttpClient -> /api/v1 -> Study API
    StudyApiService nhận descriptor từ core/constant/api.constants.ts

`StudyApiService`, `HttpClient` và proxy local đã được cấu hình; AD-01 và AD-02 không có feature API call. AD-02 chỉ trình bày trạng thái dữ liệu chưa kết nối; API #68 và functional DD vẫn blocked, không tạo service/model để lấp contract gap. API #101 chưa có current route/module/query/model/test; không ánh xạ KPI draft thành card. Proxy chỉ áp dụng cho `ng serve`; production cần định tuyến cùng origin `/api/v1`, hiện chưa được xác minh. Với từng màn hình, trước tiên xác minh tuyến Study Server hiện tại, cấu trúc yêu cầu/phản hồi, xác thực, mã lỗi và các kiểm thử liên quan. Không suy ra hành vi điểm cuối API từ bản phác giao diện, cũng không tự tạo trường dữ liệu hoặc tuyến API để lấp chỗ trống.

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
- Angular `@angular/build:unit-test` với Vitest được cấu hình cho `ng test`; test `*.spec.ts` đặt cạnh code được kiểm tra. Đây là test runner của frontend, không xác minh API/runtime backend.
- Dùng npm start để chạy môi trường phát triển cục bộ và npm run build để biên dịch bản phát hành. Đầu ra Angular trong dist/ là sản phẩm được tạo tự động, không phải mã nguồn.
