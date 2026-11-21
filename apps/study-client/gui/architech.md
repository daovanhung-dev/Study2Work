# Kiến trúc Study Web

    STATUS: SHARED_SH06_GUEST_STUDENT_MENTOR_ADMIN
    FRAMEWORK: ANGULAR 22
    RENDERING: CLIENT-SIDE SPA

## Mục đích và ranh giới hiện tại

SH-02 hiện được wire tại `/login`, SH-03 tại `/register` và SH-04 tại
`/register/verification` qua `layouts/shared/SharedLayout` và
`features/shared/`. SH-02 render presentation với submit disabled. SH-03 gọi
API #01; sau phản hồi 201 hợp lệ, trang hiển thị trạng thái tạo tài khoản và
link do người dùng chủ động mở SH-04. SH-04 là trang thông tin tĩnh, không
nhận ID/email và không gọi API #02. Handoff email, trigger/feature gate và
account lifecycle chưa được chốt; browser runtime/deployment chưa xác minh.

StudentLayout owns a Student-only login through API #03; tokens stay in tab
memory and `StudentApiService` attaches Bearer tokens to protected calls.
ST-01 calls #20/#38, ST-08 calls #20, ST-09 checks ACTIVE membership with #20
before #37, and ST-10 calls #22 followed by explicit #23 only for a PUBLISHED
lesson. ST-11 calls #24 after handoff. #21 returns UserProfile and is not used
for progress; #43–#45 remain SOURCE_ONLY. ST-09 keeps curriculum/media gated
because public #09 cannot prove entitlement. ST-06/ST-07 payment/result flows
remain gated. Browser runtime is unverified.

Guest routes `/courses`, `/courses/search` and `/courses/:courseId` to GS-01,
GS-02 and GS-03. The pages call #05/#06, #07 and #08 respectively. GS03 owns a
`?tab=curriculum` panel that calls #09 after #08 succeeds and projects
title/order only; reviews remain unavailable. Browser loaded-state and live
API/DB runtime remain unverified. Shared SH-06 has an explicit `/not-found`
route and the root wildcard clears an unknown Angular path/query before routing
there. GS-03 sends API #08 detail 404 to this generic page; #08 500 and #09
curriculum 404 remain separate. Static-host rewriting and deployment remain
unverified, and inventory prototype sections still require content/route review.

The root `/resources/:resourceId` route mounts GS-07 as a contract-blocked gate
only. It does not consume the route ID, call API #12, or render resource
actions. AC-06 access/URL policy remains blocked; browser and deployment
runtime are unverified.

Tài liệu này mô tả bộ khung Angular của Study Web và cấu trúc triển khai màn hình. App root chỉ chứa `RouterOutlet`; `/` lazy-load `SharedLayout` và SH-01, còn các route AD-01 đến AD-25 dùng chung `AdminLayout`. Readiness scaffold còn trong source nhưng không mounted. Mỗi màn hình có bốn thư mục `data-access/`, `models/`, `pages/`, `ui/`. Mười chín caller theo màn hình dùng 14 API GET Admin có route/source Study Server hiện tại thông qua `AdminApiService`; AD-01 và AD-02 giữ page riêng: AD-01 không có dữ liệu dashboard vì API #101 chưa có source; AD-02 đọc danh sách UserProfile qua #68 và chỉ ánh xạ keyword/role/status/page. AD-03 đến AD-25 cũng có layout riêng. Không routed Admin page nào import `AdminScreenSurface`; import hiện tại của component chỉ nằm trong unit spec riêng. AD-04 đọc #69 UserProfile và khóa các field/Save trong khi body, role và PII policy của #70 chưa được duyệt. AD-09 chỉ đọc Course qua #74; #76/#77 vẫn disabled vì contract body/transition và lifecycle policy chưa được duyệt. AD-05 chỉ đọc user qua #69; #71/#72 và audit reason vẫn disabled vì status/session, deletion/retention, permission và audit policy chưa được duyệt. `AdminSessionService` dùng API #3 cho login, refresh bằng route nguồn R-X01, giữ token trong bộ nhớ tab và chỉ chấp nhận role `ADMIN`; không dùng API #4 hoặc lưu token qua `localStorage`/`sessionStorage`. API wrapper gắn Bearer và kết thúc phiên local khi protected request trả 401. Đây là tích hợp source-backed ở client; chưa chứng minh deployment/API acceptance. API #99–#103 và #18 export/operation thiếu hoặc chưa thống nhất. Action có policy/request body chưa rõ được disabled. Router và điều hướng không thay thế quyền server. `core/http/StudyApiService` cung cấp transport generic tới `/api/v1`; Angular dev server proxy chuyển tiếp local request tới Study API `127.0.0.1:3003`.

`core/constant/api.constants.ts` chứa registry descriptor Study API theo catalog; `core/http/StudyApiService` dùng registry này để gửi request generic tới `/api/v1`. `AdminApiService` chỉ nhận descriptor GET `WIRED`, lấy Bearer token từ `AdminSessionService`, rồi gửi request qua `StudyApiService`. Registry/source không tự chứng minh deployment hoặc runtime acceptance.

`core/localStorage/local-storage.service.ts` cung cấp `LocalStorageService` để lưu/đọc giá trị JSON trong browser `localStorage`. Service giữ nguyên key, trả `null` khi key chưa có và truyền lỗi serialize/parse/storage cho caller. Utility này không được dùng cho auth; token Admin chỉ tồn tại trong bộ nhớ tab.

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
            ├── app.routes.ts        # Lazy-load route groups system, shared, student và admin
            ├── core/                # Hạ tầng toàn ứng dụng, dịch vụ dùng chung và phần liên miền
            │   ├── auth/
            │   │   └── admin-session.service.ts # Phiên Admin trong bộ nhớ tab, dùng API #3/R-X01
            │   ├── constant/
            │   │   └── api.constants.ts      # Registry descriptor Study API
            │   ├── http/
            │   │   ├── api-envelope.ts       # Kiểu envelope Study API dùng chung
            │   │   ├── study-api.service.ts  # HTTP transport generic cho /api/v1
            │   │   └── admin-api.service.ts # Bearer GET wrapper cho Admin source-backed APIs
            │   └── localStorage/
            │       └── local-storage.service.ts # Browser localStorage JSON utility
            ├── layouts/             # Khung giao diện dùng chung cho một nhóm trang
            │   ├── shared/          # Outlet shell cho Shared/Auth pages
            │   ├── admin/           # Outlet shell cho các route Admin
            │   └── system/          # Legacy outlet shell cho readiness; hiện không mounted
            ├── shared/              # Thành phần trình bày dùng lại, không chứa quy tắc nghiệp vụ
            │   └── ui/              # study-icon.*, admin-screen-surface.* và admin-detail-page.css
            └── features/            # Nhóm màn hình Study
                ├── shared/          # SH-* / Auth / System screens theo inventory
                │   ├── shared.route.ts
                │   ├── SH02/        # Login presentation; submit/session chưa nối
                │   ├── SH03/        # Registration API #01; SH-04 link after valid 201
                │   ├── SH04/        # Static information gate; API #02 remains unwired
                │   └── SH06/        # Explicit /not-found page
                ├── guest/           # GS-*
                ├── student/         # ST-*
                ├── mentor/          # ME-*
                ├── system/          # Readiness scaffold còn trong source; không mounted
                │   ├── system.routes.ts
                │   └── pages/system-readiness-page.*
                └── admin/           # AD-*
                    ├── admin.routes.ts
                    ├── AD01/ … AD25/ # Mỗi screen có data-access/, models/, pages/, ui/
                    └── admin.routes.ts # Các route Admin AD-01…AD-25

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
| src/styles.css | Chứa token CSS toàn cục, kiểu cơ sở/focus/reduced motion, container `.page-width` giới hạn trong Admin (AD-01 1540px desktop; các trang khác 1520px) và style bảng/trạng thái rỗng AD-02 được prefix theo component. |
| src/app/layouts/admin/admin-layout.* | Chứa khung Admin đăng nhập, breadcrumb workspace cố định, năm nhóm điều hướng, chuông thông báo, hồ sơ phiên và bảng màu xanh chỉ áp dụng trong Admin host; trạng thái vận hành không có nguồn phải giữ trung tính. |
| README.md | Hướng dẫn nhà phát triển cài gói phụ thuộc, chạy và biên dịch ứng dụng. |

### Ranh giới trong src/app/

- app.ts, app.html và app.css ghép thành phần gốc của ứng dụng. App root chỉ render `RouterOutlet`; `/` mount SharedLayout và SH-01. Readiness page còn trong source nhưng không được route.
- app.config.ts đăng ký provider Angular dùng toàn ứng dụng, gồm `provideHttpClient()` cho API transport. Chỉ thêm provider tại đây khi toàn ứng dụng cần dùng.
- app.routes.ts mounts `shared.route.ts` at `/` (SH-01), `guest.route.ts` at `/courses`, `student.route.ts` at `/student` and `admin.routes.ts` at `/admin`; `system.routes.ts` is not mounted. Shared routes include SH-02 `/login`, SH-03 `/register`, SH-04 `/register/verification` and SH-06 `/not-found`. The root wildcard sends unknown Angular routes to SH-06 and clears their original path/query; GS-03 #08 detail 404 uses the same generic state. Guest route group maps GS-01–GS-03; in GS-03, `?tab=curriculum` mounts panel GS04 and calls #09 after #08 confirms the course. There is no standalone GS04 route/page or GS05 review caller. `/forbidden` SH-05 has no route/error-context integration. Admin has no router guard; `AdminLayout` only renders after local login, while the API wrapper requires a Bearer token. Server guards own authorization.
- core/ quản lý hạ tầng toàn ứng dụng như registry descriptor trong `constant/api.constants.ts`, auth session, cấu hình HTTP và transport API generic trong `http/`, tiện ích JSON browser storage trong `localStorage/`, xử lý lỗi toàn cục và bộ chặn tuyến. `AdminSessionService` xác thực API #3, kiểm tra role `ADMIN`, giữ token trong memory và refresh qua R-X01. `AdminApiService` chỉ gửi GET descriptor `WIRED` có Bearer; 401 kết thúc phiên local. Không đặt truy vấn hay chính sách riêng của nhóm tính năng trong core/. Utility `LocalStorageService` chưa có caller auth.
- layouts/ quản lý khung giao diện dùng chung cho các tuyến, chẳng hạn khung công khai, đã xác thực, student, mentor hoặc admin. Khung giao diện sắp xếp điều hướng và vùng hiển thị trang; không sở hữu quy tắc nghiệp vụ hay truy cập dữ liệu của nhóm tính năng.
- shared/ quản lý thành phần trình bày tổng quát, chỉ thị, bộ biến đổi và tiện ích định dạng được nhiều miền dùng lại. `AdminScreenSurface` là renderer dùng chung cho các mẫu trình bày Admin; không gọi API nghiệp vụ hoặc chứa quy tắc nghiệp vụ Study. `admin-screen-surface.css`, `admin-detail-page.css`, stylesheet host-scoped của ST-02/ST-03/ST-04/ST-05 và CSS riêng của AD-06/08/10/11/12/14/15/16/17/18/19/20/21/22/23/24/25 được đăng ký toàn cục qua `angular.json`; selector của AD-06/07/08/10/11/12/13/14/15/16/17/18/19/20/21/22/23/24/25 được scope theo custom-element host để tránh ảnh hưởng ngoài màn hình.
- features/ quản lý screen theo nhóm `shared`, `guest`, `student`, `mentor` và `admin`. `features/system` giữ readiness scaffold cũ nhưng hiện không mounted; các SH-* screen thuộc group `shared`. SH-04 có đúng bốn thư mục con trực tiếp: `data-access/`, `models/`, `pages/` và `ui/`; hiện chỉ có static page component và test trong package này.
- pages/ chứa page component; ui/ chứa cấu hình/presentation riêng của screen; data-access/ ghi boundary và chỉ chứa I/O khi API, xác thực và contract đã xác minh; models/ chứa kiểu/chuyển đổi bám theo contract đã xác minh. Không tạo `domain/` hoặc folder thứ năm trong screen.
- Mỗi nhóm có một route file và một layout. Theo yêu cầu cụ thể của task, route files ở đây dùng tên `admin.routes.ts` và `system.routes.ts`; các tên SH-* khác vẫn theo cấu trúc canonical. `AdminLayout` sở hữu header, điều hướng, breadcrumb, footer, login gate theo in-memory session và outlet cho AD-01…AD-25. Source-backed reads hiển thị loading/error/empty/data theo response; đây không phải dữ liệu runtime/deployment đã xác minh. Route và điều hướng không xác thực quyền server.

### Mẫu cấu trúc feature

Dùng cấu trúc sau khi triển khai một nhóm màn hình; chỉ tạo những thư mục mà nhóm tính năng thực sự cần:

    features/<group>/<SCREEN_ID>/
    ├── data-access/    # I/O theo contract hiện hành; có thể chưa cần khi chưa có API
    ├── models/         # Kiểu/chuyển đổi theo contract đã xác minh
    ├── pages/          # Component trang chính và stylesheet/template cạnh nó
    └── ui/             # Component UI chỉ dùng trong screen

Tên thư mục screen dùng mã compact như `AD01` cho screen ID `AD-01`. Tuyến trong catalog/DD vẫn là đề xuất cho đến khi requirements, dependencies và runtime behavior được xác minh. Không tạo service/model/API riêng cho màn hình chỉ để lấp contract gap.

## Luồng dữ liệu và cách ứng dụng vận hành

    main.ts -> app.config.ts -> app.routes.ts -> AdminLayout -> page -> ui
    AdminLayout -> AdminSessionService -> StudyApiService -> API #3 / R-X01
    Screen page -> data-access -> AdminApiService -> AdminSessionService (Bearer)
              -> StudyApiService -> HttpClient -> /api/v1 -> Study API
    AdminApiService chỉ nhận GET descriptor WIRED; writes và API thiếu source không được gọi.

`StudyApiService`, `HttpClient` và proxy local đã được cấu hình. Mười chín caller theo màn hình dùng 14 Admin GET API hiện có trong source Study Server. Mỗi callsite cần phiên in-memory hợp lệ; token refresh dùng R-X01 theo source hiện tại và session bị xóa khi protected API trả 401. API #101/#102 và export worker/API #103/#18 chưa có local implementation, vì vậy dashboard/report/export hiển thị unavailable state. Production cần định tuyến cùng origin `/api/v1`, hiện chưa được xác minh. Với từng màn hình, xác minh tuyến Study Server hiện tại, request/response, xác thực, mã lỗi và test liên quan. Không suy ra behavior từ mockup hoặc tự tạo contract để lấp chỗ trống.

Dùng Angular Signals cho trạng thái giao diện đồng bộ tại chỗ và RxJS cho luồng bất đồng bộ khi đã bổ sung tích hợp API có căn cứ. Chưa thêm thư viện quản lý trạng thái toàn cục nếu chưa có nhu cầu cụ thể giữa nhiều nhóm tính năng. Bộ chặn tuyến phía trình duyệt chỉ phục vụ trải nghiệm điều hướng; quyền truy cập do máy chủ quyết định.

## Trạng thái source ST-02

`/student/profile` is registered inside the Student route group and uses
`StudentLayout`'s `custom` shell mode. `ST02ProfileService` calls API #04 through
the Student Bearer adapter; the page renders loading/error/retry and only the
response-backed `full_name` and `email`. Avatar rendering, `role`/`status`
authorization claims and edit behavior remain gated. The host-scoped page
stylesheet is registered in `angular.json`; this does not prove browser, live
API or database runtime.

## Trạng thái source ST-03

`/student/profile/edit` is registered inside the Student route group and renders
the G-03 mutation gate. `ST03ProfileService` calls API #04 through the Student
Bearer adapter and binds only `full_name`/`email` as read-only values. APIs #13
and #14 have route metadata only; upload/save, phone/bio and form submission
remain disabled. The page uses host-scoped CSS registered in `angular.json`;
source wiring does not establish authenticated browser or live API runtime.

## Trạng thái source ST-04

`/student/enroll/:courseId` loads public course detail through the existing
`GS03CourseDetailService` (#08). A published course leads to the Stitch-derived
enrollment gate; #08 404 and other errors map to not-found and generic error
states. Route metadata assigns #08/#15, but no #15 request is made: current
server code falls back to any course enrollment when Authorization is absent
or invalid. The Student guard/session and enrollment/payment branches remain
unresolved. Host-scoped CSS is registered in `angular.json`; authenticated and
live runtime are unverified.

## Trạng thái source ST-05

`/student/checkout/:courseId` reuses the public #08 course detail caller. A
published course renders the unavailable checkout state from Stitch; #08 404
and other errors map to separate not-found/error states. Route metadata assigns
#08/#16, but no order request is sent: the #16 descriptor remains `UNWIRED`,
the checked-in database has no `orders` table, and focused #16 tests were not
found. Student auth and order/payment contracts remain unresolved.

## Trạng thái source ST-11

Route `/student/lessons/:lessonId` hiện được đăng ký qua `app.routes.ts` và
`features/student/student.route.ts`, dùng `StudentLayout` cùng trang
`features/student/ST11/pages/`. Trang chỉ trình bày trạng thái fallback theo
ảnh ST-11; không đọc `lessonId`, gọi API, phát media hay lưu tiến độ. Các link
Student khác vẫn là href tĩnh và route đích chưa được xác minh. DD chức năng
Lesson Player tiếp tục blocked.

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
