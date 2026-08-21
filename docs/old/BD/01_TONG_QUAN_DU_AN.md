# Study2Work — Tổng quan dự án và thiết kế mục tiêu V1-PILOT

| Thuộc tính | Giá trị |
|---|---|
| Trạng thái | Tài liệu chuẩn — đã được phê duyệt cho V1-PILOT |
| Phạm vi | Danh tính nền tảng, Study, Work và các tích hợp dùng chung |
| Đối tượng đọc | Sản phẩm, BA, UX/UI, kiến trúc sư, lập trình viên, QA, DevOps, vận hành và bảo mật |
| Múi giờ nghiệp vụ | `Asia/Ho_Chi_Minh`; mọi thời điểm lưu trữ và trao đổi qua API là UTC |
| Ngôn ngữ dữ liệu | Giao diện bằng tiếng Việt; mã, enum và hợp đồng kỹ thuật dùng tiếng Anh |
| Quy mô thử nghiệm | 5.000 tài khoản, 500 DAU, đỉnh 50 RPS |

## 1. Quản trị bộ tài liệu

### 1.1. Vai trò của tài liệu

Tài liệu này là nguồn chuẩn cho **ý định sản phẩm và mọi quyết định xuyên hệ thống**. Bốn tài liệu còn lại cụ thể hóa nhưng không được thay đổi các quyết định tại đây:

| Tài liệu | Nội dung sở hữu |
|---|---|
| `01_TONG_QUAN_DU_AN.md` | Phạm vi, năng lực, trường hợp sử dụng, quyền, quy tắc nghiệp vụ, kiến trúc, NFR và kiểm thử chấp nhận |
| `02_BIEU_DO_HE_THONG.md` | Định nghĩa `AC`, `CLS`, `SEQ` và biểu đồ trường hợp sử dụng dùng các `UC` tại đây |
| `03_THIET_KE_CO_SO_DU_LIEU.md` | Định nghĩa enum và `TBL`, ràng buộc, chỉ mục, giao dịch và lưu giữ vật lý |
| `04_DAC_TA_API.md` | Định nghĩa `API`, `EVT`, `ERR`, hợp đồng HTTP/WebSocket/webhook và lô-gic truy vấn |
| `05_DAC_TA_MAN_HINH.md` | Định nghĩa `SCR`, đường dẫn, trường hiển thị, trạng thái và luồng tương tác |

Thứ tự ưu tiên khi có sai khác là: quyết định nghiệp vụ tại tài liệu này → hợp đồng API/sự kiện → mô hình dữ liệu → biểu đồ → mô tả màn hình. `OpenAPI`, `migration` và lược đồ sự kiện là các hợp đồng thực thi dẫn xuất; yêu cầu hợp nhất làm thay đổi hành vi phải cập nhật tài liệu sở hữu và các hợp đồng liên quan trong cùng thay đổi.

### 1.2. Quy ước định danh và thay đổi

- ID có dạng `TYPE-CTX-NNN`; `CTX` thuộc `IAM`, `STU`, `WRK`, `PAY`, `UNI`, `AIX`, `INT`, `OPS`.
- Tài liệu này sở hữu `CAP`, `UC`, `BR`, `PERM`, `NFR`, `TC`. ID đã phát hành không được tái sử dụng cho nghĩa khác; mục bị loại phải được đánh dấu ngừng dùng trong lịch sử thay đổi.
- Mọi thay đổi trạng thái, quyền truy cập, dữ liệu cá nhân, thanh toán hoặc quyết định AI cần ít nhất một quy tắc nghiệp vụ, một kiểm thử chấp nhận và một dòng truy vết.
- Nội dung đã khóa cho V1-PILOT chỉ được thay đổi qua ADR hoặc quyết định sản phẩm có người chịu trách nhiệm, tác động tương thích và kế hoạch chuyển đổi rõ ràng.
- Không lấy bản nguyên mẫu Work cũ, tài liệu BD cũ hoặc mã nguồn đang chạy làm căn cứ để ghi đè đặc tả đích này.

### 1.3. Trách nhiệm phê duyệt

| Nhóm thay đổi | Người chịu trách nhiệm cuối | Bên bắt buộc rà soát |
|---|---|---|
| Phạm vi, hành trình, quy tắc nghiệp vụ | Chủ sở hữu sản phẩm | BA, Trưởng nhóm kỹ thuật, QA |
| Danh tính, quyền, không gian dữ liệu, quyền riêng tư | Chủ sở hữu Bảo mật/Nền tảng | Sản phẩm, Trưởng nhóm kỹ thuật, DPO/người phụ trách dữ liệu |
| Miền Study và Work | Chủ sở hữu miền tương ứng | Sản phẩm, Dữ liệu, QA |
| Thanh toán, hoàn tiền | Chủ sở hữu Tài chính | Sản phẩm, Bảo mật, Chủ sở hữu Work |
| AI và ghép nối | Chủ sở hữu Quản trị AI | Sản phẩm, Bảo mật, Chủ sở hữu miền Tuyển dụng |
| NFR, vận hành, khôi phục | Chủ sở hữu Nền tảng/Vận hành | Các chủ sở hữu miền, Bảo mật |

## 2. Tầm nhìn, mục tiêu và phạm vi

### 2.1. Tầm nhìn

Study2Work là hệ sinh thái công nghệ giáo dục và công nghệ nhân sự, giúp người học xây dựng năng lực có cấu trúc trong Study, chủ động dùng minh chứng đã chọn để ứng tuyển trong Work, đồng thời giúp doanh nghiệp và trường đại học vận hành tuyển dụng thực tập một cách minh bạch. Hệ thống ưu tiên sự đồng ý, khả năng kiểm toán và các quyết định có con người chịu trách nhiệm.

### 2.2. Mục tiêu V1-PILOT

1. Cung cấp một danh tính email/mật khẩu an toàn cho toàn nền tảng; không sao chép thông tin xác thực vào Study hoặc Work.
2. Cho phép học độc lập mọi khóa đã xuất bản; quy trình làm quen chỉ phục vụ việc lựa chọn lộ trình chính.
3. Bảo toàn lịch sử học và phiên bản nội dung, phát hành minh chứng có thể thu hồi.
4. Cung cấp hồ sơ nghề nghiệp, CV, việc làm, ứng tuyển, ATS, phỏng vấn và trò chuyện 1–1 theo hồ sơ ứng tuyển.
5. Chỉ cho phép doanh nghiệp tìm ứng viên khi ứng viên chủ động bật tính năng tìm kiếm; kết quả tìm kiếm không lộ thông tin liên hệ, CV hoặc minh chứng.
6. Hỗ trợ không gian dữ liệu cho doanh nghiệp và trường đại học, có phân quyền, sự đồng ý và cách ly dữ liệu.
7. Bán gói/tín dụng trả trước bằng VND qua VNPAY và MoMo; kích hoạt quyền lợi chính xác một lần theo xác nhận từ nhà cung cấp.
8. Dùng AI để soạn thảo và giải thích/đề xuất, không tự ra quyết định tuyển dụng hoặc thay đổi trạng thái ATS.

### 2.3. Trong phạm vi

- Ứng dụng web thích ứng cho khách, người học/ứng viên, doanh nghiệp, trường đại học và đội vận hành.
- Danh tính nền tảng: đăng ký email/mật khẩu, xác minh email, đăng nhập, đặt lại mật khẩu, phiên làm việc, mã làm mới xoay vòng, TOTP MFA, quản trị trạng thái và vai trò nền tảng.
- Study: danh mục, quy trình làm quen, đề xuất lộ trình, lộ trình chính, khóa học độc lập, nội dung có phiên bản, tiến độ, bài đánh giá, quét tệp, minh chứng, thông báo, cộng đồng, hỗ trợ và quản trị nội dung.
- Work: hồ sơ nghề nghiệp, CV/hồ sơ năng lực, tìm kiếm ứng viên, không gian dữ liệu doanh nghiệp, bản sửa đổi việc làm, ATS, minh chứng khi ứng tuyển, phỏng vấn, trò chuyện, thông báo và kiểm duyệt.
- Trường đại học: liên kết, nhóm khóa, chương trình thực tập, phân phối việc làm trong trường, hợp tác/giới thiệu và báo cáo tổng hợp.
- TopCV/TopJD: mẫu cao cấp, hỗ trợ viết bằng AI, hồ sơ/việc làm được tài trợ có nhãn và quyền lợi trả trước.
- Thanh toán: VNPAY, MoMo, đối soát, hoàn tiền, tranh chấp thanh toán ngược và quyền lợi sử dụng.
- AI xử lý bất đồng bộ qua bộ điều hợp nhà cung cấp; mặc định dùng Ollama cho đợt thử nghiệm.
- Kiểm toán, yêu cầu về quyền riêng tư, lưu giữ, quan sát vận hành, sao lưu và khôi phục sau thảm họa.

### 2.4. Ngoài phạm vi

- Đăng nhập mạng xã hội, số điện thoại/OTP, SSO doanh nghiệp và định danh điện tử.
- Ứng dụng di động gốc, thanh toán trong ứng dụng và thông báo đẩy gốc.
- Chợ giảng viên, lớp học trực tiếp, giám sát thi, môi trường chạy mã và chấm mã nguồn tự động.
- Trò chuyện nhóm, gọi thoại/cuộc gọi có hình, gửi tệp trong trò chuyện; V1 chỉ có tin nhắn văn bản và tin nhắn hệ thống 1–1 theo hồ sơ ứng tuyển.
- Đồng bộ lịch Google/Microsoft hoặc nền tảng họp; V1 dùng lịch nội bộ và tệp/liên kết ICS.
- Tự động gia hạn thuê bao, lưu thẻ, ví nội bộ, ký quỹ trung gian, chi trả, trả lương hoặc hoa hồng chợ dịch vụ.
- AI tự động ứng tuyển, tự động đổi ATS, xếp hạng bằng thuộc tính nhạy cảm, tự từ chối/tuyển dụng hoặc thay con người phê duyệt.
- Cụm tìm kiếm, kho dữ liệu, vi dịch vụ theo từng mô-đun và truy vấn cơ sở dữ liệu chéo.
- Trường đại học theo dõi cá nhân khi chưa có sự đồng ý còn hiệu lực; nhóm báo cáo dưới 10 người.

## 3. Thuật ngữ chuẩn

| Thuật ngữ | Định nghĩa chuẩn |
|---|---|
| Danh tính nền tảng | Dịch vụ triển khai dùng chung, sở hữu người dùng, thông tin xác thực, xác minh, phiên làm việc, mã thông báo, vai trò toàn cục và kiểm toán bảo mật. |
| Người dùng nền tảng | Danh tính toàn cục có `platformUserId` là UUID bất biến. |
| Bản sao chiếu | Bản sao tối thiểu, nhất quán sau cùng của danh tính hoặc hệ phân loại trong cơ sở dữ liệu của miền; không phải thông tin xác thực. |
| Người học | Người dùng nền tảng sử dụng Study. |
| Ứng viên | Người dùng nền tảng sở hữu hồ sơ nghề nghiệp trong Work; một người có thể đồng thời là người học. |
| Không gian dữ liệu | Biên dữ liệu của doanh nghiệp hoặc trường đại học; mọi truy vấn phải lấy không gian dữ liệu từ tư cách thành viên đã được máy chủ xác thực. |
| Tư cách thành viên | Quan hệ người dùng–không gian dữ liệu có vai trò, trạng thái và thời hạn; không phải vai trò toàn cục. |
| Lộ trình chính | Một lộ trình chính đang `ACTIVE`; không hạn chế việc học các khóa độc lập. |
| Thực thể ổn định | Danh tính bền vững của lộ trình/khóa học/việc làm; nội dung đã xuất bản nằm trong bản sửa đổi/phiên bản bất biến. |
| Minh chứng | Minh chứng do Study phát hành cho một kết quả học tập, có phiên bản, chủ sở hữu và trạng thái thu hồi. |
| Bản chụp minh chứng | Bản chụp tối thiểu Work lưu theo hồ sơ ứng tuyển sau khi ứng viên chọn minh chứng và đồng ý xuất dữ liệu. |
| Sự đồng ý | Bản ghi chủ thể, mục đích, phạm vi, phiên bản điều khoản, thời điểm cấp, hết hạn và thu hồi. |
| ATS | Luồng xử lý hồ sơ ứng tuyển của doanh nghiệp; mọi thay đổi trạng thái có tác nhân và kiểm toán. |
| Chủ động cho phép tìm kiếm ứng viên | Sự đồng ý riêng để hồ sơ được lập chỉ mục và tìm thấy; mặc định tắt. |
| Điểm tự nhiên | Điểm phù hợp không chịu ảnh hưởng của thanh toán hoặc vị trí tài trợ. |
| Vị trí tài trợ | Vị trí quảng bá trả phí, luôn có nhãn và được xếp riêng khỏi điểm tự nhiên. |
| Quyền lợi sử dụng | Quyền sử dụng/tín dụng phát sinh từ đơn hàng đã `SETTLED`; có số dư, hạn dùng và sổ cái. |
| Tính bất biến theo yêu cầu | Cùng chủ thể, thao tác và `Idempotency-Key` với cùng dữ liệu đầu vào phải trả cùng kết quả, không tạo tác dụng phụ lần hai. |
| Hộp gửi sự kiện | Sự kiện được ghi cùng giao dịch với thay đổi của miền rồi được tiến trình nền phát đi ít nhất một lần. |
| Trạng thái kết thúc | Trạng thái không thể chuyển tiếp qua API nghiệp vụ thông thường. |
| Người dùng đặc quyền | Mọi nhân sự vận hành nội bộ hoặc thành viên không gian dữ liệu có quyền xem dữ liệu của người khác, xuất bản, tuyển dụng, tài chính, phân quyền hoặc kiểm toán. |
| PII | Dữ liệu có thể nhận diện cá nhân như email, tên, thông tin liên hệ, CV, địa chỉ, tệp và lịch sử ứng tuyển. |

## 4. Tác nhân, không gian dữ liệu, vai trò và quyền

### 4.1. Tác nhân

| Tác nhân | Phạm vi hành động |
|---|---|
| Khách | Xem trang giới thiệu/danh mục/việc làm công khai; đăng ký, xác minh và đăng nhập. |
| Người học/Ứng viên | Quản lý dữ liệu của chính mình, học tập, ứng tuyển, đồng ý xử lý dữ liệu, thanh toán và gửi yêu cầu về quyền riêng tư. |
| Tác giả/Nhà xuất bản nội dung | Soạn nội dung, kiểm tra và xuất bản phiên bản Study. |
| Người chấm bài đánh giá | Chấm bài văn bản/liên kết/tệp theo thang điểm; không sửa bài đã nộp. |
| Hỗ trợ người học/Người kiểm duyệt cộng đồng | Xử lý hỗ trợ hoặc kiểm duyệt trong đúng phạm vi được giao. |
| Chủ sở hữu/Quản trị viên doanh nghiệp | Quản lý không gian dữ liệu, tư cách thành viên, thanh toán, việc làm và chính sách tuyển dụng. |
| Nhà tuyển dụng/Người phỏng vấn | Nhà tuyển dụng vận hành tìm nguồn/ATS; người phỏng vấn chỉ xem hồ sơ và buổi phỏng vấn được phân công, cùng phản hồi được phép. |
| Chủ sở hữu/Điều phối viên/Người xem của trường đại học | Quản lý không gian dữ liệu, liên kết/nhóm khóa/chương trình/giới thiệu hoặc chỉ xem báo cáo tổng hợp theo vai trò. |
| Nhân sự tài chính | Đối soát, xử lý hoàn tiền/tranh chấp thanh toán ngược; không được tự cấp vai trò hoặc sửa hồ sơ ứng tuyển. |
| Người kiểm duyệt/Quản trị viên nền tảng/Người kiểm toán bảo mật | Kiểm duyệt toàn nền tảng, vận hành, phân quyền hoặc chỉ đọc dữ liệu kiểm toán theo trách nhiệm. |
| Nhà cung cấp thanh toán | VNPAY hoặc MoMo gửi phản hồi gọi lại hoặc `webhook` đã ký và nhận yêu cầu truy vấn/hoàn tiền. |
| Nhà cung cấp AI | Ollama qua bộ điều hợp nhận dữ liệu đầu vào đã lọc và trả dữ liệu đầu ra theo lược đồ; không phải tác nhân ra quyết định. |

### 4.2. Mô hình vai trò

- Danh tính nền tảng chỉ phát hành các vai trò toàn cục: `LEARNER`, `PLATFORM_ADMIN`, `FINANCE_OPERATOR`, `PLATFORM_MODERATOR`, `SECURITY_AUDITOR`. Thay đổi vai trò làm tăng `authVersion` và thu hồi các phiên làm việc liên quan.
- Study quản lý các vai trò cục bộ: `CONTENT_AUTHOR`, `CONTENT_PUBLISHER`, `ASSESSMENT_REVIEWER`, `LEARNER_SUPPORT`, `COMMUNITY_MODERATOR`, `STUDY_ADMIN`.
- Work quản lý vai trò tư cách thành viên theo không gian dữ liệu: `ENTERPRISE_OWNER`, `ENTERPRISE_ADMIN`, `RECRUITER`, `INTERVIEWER`; Trường đại học quản lý `UNIVERSITY_OWNER`, `UNIVERSITY_COORDINATOR`, `UNIVERSITY_VIEWER`.
- Vai trò chỉ là gói quyền. Dịch vụ phía máy chủ kiểm tra quyền cụ thể, tư cách thành viên không gian dữ liệu `ACTIVE`, phạm vi tài nguyên và tài khoản `ACTIVE` trên từng yêu cầu; cơ chế chặn ở giao diện không phải biện pháp bảo mật.
- Mọi người dùng đặc quyền phải hoàn tất TOTP MFA trước khi dùng quyền đặc quyền. Quyền truy cập khẩn cấp chỉ dành cho quản trị viên nền tảng được chỉ định, có lý do, thời hạn tối đa 60 phút và tạo cảnh báo kiểm toán ngay.

### 4.3. Danh mục quyền

| ID | Khóa quyền | Được cấp mặc định |
|---|---|---|
| **PERM-IAM-001** | `platform.users.read` | Quản trị viên nền tảng, Người kiểm toán bảo mật (chỉ đọc) |
| **PERM-IAM-002** | `platform.users.status.manage` | Quản trị viên nền tảng |
| **PERM-IAM-003** | `platform.roles.manage` | Quản trị viên nền tảng |
| **PERM-IAM-004** | `platform.security.audit.read` | Người kiểm toán bảo mật, Quản trị viên nền tảng |
| **PERM-STU-001** | `study.content.read_admin` | Tác giả/Nhà xuất bản nội dung, Quản trị viên Study |
| **PERM-STU-002** | `study.content.write` | Tác giả/Nhà xuất bản nội dung, Quản trị viên Study |
| **PERM-STU-003** | `study.content.publish` | Nhà xuất bản nội dung, Quản trị viên Study |
| **PERM-STU-004** | `study.content.archive` | Quản trị viên Study |
| **PERM-STU-005** | `study.content_issues.manage` | Nhà xuất bản nội dung, Quản trị viên Study |
| **PERM-STU-006** | `study.assessments.review` | Người chấm bài đánh giá, Quản trị viên Study |
| **PERM-STU-008** | `study.support.read_internal` | Nhân sự hỗ trợ người học, Quản trị viên Study |
| **PERM-STU-009** | `study.primary_path.override` | Nhân sự hỗ trợ người học được ủy quyền, Quản trị viên Study |
| **PERM-STU-010** | `study.progress.adjust` | Quản trị viên Study được ủy quyền |
| **PERM-STU-011** | `study.roles.manage` | Quản trị viên Study |
| **PERM-STU-012** | `study.community.moderate` | Người kiểm duyệt cộng đồng, Quản trị viên Study |
| **PERM-STU-013** | `study.reports.read` | Quản trị viên Study |
| **PERM-STU-014** | `study.audit.read` | Quản trị viên Study, Người kiểm toán bảo mật theo phạm vi |
| **PERM-WRK-001** | `work.enterprise.profile.manage` | Chủ sở hữu/Quản trị viên doanh nghiệp |
| **PERM-WRK-002** | `work.enterprise.verification.submit` | Chủ sở hữu/Quản trị viên doanh nghiệp |
| **PERM-WRK-003** | `work.enterprise.members.read` | Chủ sở hữu/Quản trị viên doanh nghiệp |
| **PERM-WRK-004** | `work.enterprise.members.manage` | Chủ sở hữu/Quản trị viên doanh nghiệp |
| **PERM-WRK-010** | `work.jobs.read_admin` | Chủ sở hữu/Quản trị viên doanh nghiệp, Nhà tuyển dụng |
| **PERM-WRK-011** | `work.jobs.author` | Chủ sở hữu/Quản trị viên doanh nghiệp, Nhà tuyển dụng |
| **PERM-WRK-012** | `work.jobs.submit_review` | Chủ sở hữu/Quản trị viên doanh nghiệp, Nhà tuyển dụng được ủy quyền |
| **PERM-WRK-013** | `work.jobs.publish_manage` | Chủ sở hữu/Quản trị viên doanh nghiệp; nhà xuất bản đáng tin cậy theo quyền cấp có thời hạn |
| **PERM-WRK-020** | `work.candidates.search` | Chủ sở hữu/Quản trị viên doanh nghiệp, Nhà tuyển dụng có quyền lợi sử dụng |
| **PERM-WRK-021** | `work.candidates.invite` | Chủ sở hữu/Quản trị viên doanh nghiệp, Nhà tuyển dụng có quyền lợi sử dụng |
| **PERM-WRK-030** | `work.applications.list` | Chủ sở hữu/Quản trị viên doanh nghiệp, Nhà tuyển dụng |
| **PERM-WRK-031** | `work.applications.read_unassigned` | Chủ sở hữu/Quản trị viên doanh nghiệp; Nhà tuyển dụng chỉ khi được phân công nếu không có quyền này |
| **PERM-WRK-032** | `work.applications.assign` | Chủ sở hữu/Quản trị viên doanh nghiệp, Trưởng nhóm tuyển dụng |
| **PERM-WRK-034** | `work.applications.offer_manage` | Chủ sở hữu/Quản trị viên doanh nghiệp, Nhà tuyển dụng được ủy quyền và phân công |
| **PERM-WRK-040** | `work.interviews.manage` | Chủ sở hữu/Quản trị viên doanh nghiệp, Nhà tuyển dụng được phân công |
| **PERM-WRK-050** | `work.university_partnerships.respond` | Chủ sở hữu/Quản trị viên doanh nghiệp |
| **PERM-WRK-060** | `work.promotions.manage` | Chủ sở hữu/Quản trị viên doanh nghiệp có quyền lợi sử dụng |
| **PERM-WRK-070** | `work.ai.match_explain` | Nhà tuyển dụng được phân công có quyền lợi sử dụng |
| **PERM-WRK-071** | `work.ai.shortlist_suggest` | Chủ sở hữu/Quản trị viên doanh nghiệp, Trưởng nhóm tuyển dụng có quyền lợi sử dụng |
| **PERM-UNI-001** | `university.verification.submit` | Chủ sở hữu trường đại học |
| **PERM-UNI-002** | `university.members.read` | Chủ sở hữu trường đại học |
| **PERM-UNI-003** | `university.members.manage` | Chủ sở hữu trường đại học |
| **PERM-UNI-010** | `university.affiliations.invite` | Chủ sở hữu/Điều phối viên trường đại học |
| **PERM-UNI-011** | `university.cohorts.manage` | Chủ sở hữu/Điều phối viên trường đại học |
| **PERM-UNI-020** | `university.programs.manage` | Chủ sở hữu/Điều phối viên trường đại học |
| **PERM-UNI-021** | `university.campus_jobs.distribute` | Chủ sở hữu/Điều phối viên trường đại học |
| **PERM-UNI-022** | `university.partnerships.manage` | Chủ sở hữu/Điều phối viên trường đại học |
| **PERM-UNI-023** | `university.referrals.manage` | Chủ sở hữu/Điều phối viên trường đại học |
| **PERM-UNI-030** | `university.reports.read` | Chủ sở hữu/Điều phối viên/Người xem của trường đại học |
| **PERM-UNI-031** | `university.affiliations.read_consented` | Chủ sở hữu/Điều phối viên trường đại học theo mục đích đã đồng ý |
| **PERM-PAY-001** | `billing.reconciliation.read` | Nhân sự tài chính |
| **PERM-PAY-002** | `billing.refunds.approve` | Nhân sự tài chính có phân tách người lập/người duyệt |
| **PERM-PAY-003** | `billing.reconciliation.execute` | Nhân sự tài chính được ủy quyền |
| **PERM-AIX-001** | `ai.kill_switch.manage` | Chủ sở hữu Quản trị AI/Quản trị viên nền tảng được ủy quyền |
| **PERM-AIX-002** | `ai.model_configs.manage` | Chủ sở hữu Quản trị AI |
| **PERM-AIX-003** | `ai.prompt_eval.manage` | Chủ sở hữu Quản trị AI |
| **PERM-OPS-001** | `operations.verification.review` | Người kiểm duyệt nền tảng được ủy quyền |
| **PERM-OPS-002** | `operations.job_review` | Người kiểm duyệt nền tảng |
| **PERM-OPS-003** | `operations.trusted_publisher.manage` | Quản trị viên nền tảng được ủy quyền |
| **PERM-OPS-004** | `privacy.legal_hold.manage` | Quản trị viên nền tảng được ủy quyền; Người kiểm toán bảo mật giám sát |
| **PERM-OPS-005** | `operations.break_glass.use` | Nhân sự ứng cứu sự cố được chỉ định |

Các thao tác tự phục vụ của người học/ứng viên, việc mua hàng của chính mình và trò chuyện/phỏng vấn đã được phân công được cấp qua quyền sở hữu/tư cách thành viên kết hợp với trạng thái; không tạo quyền giả ở phía máy khách. Các quyền phía trên luôn kết hợp MFA, quyền lợi sử dụng, phân công, sự đồng ý và điều kiện trên tài nguyên nếu API yêu cầu.

## 5. Năng lực và trường hợp sử dụng V1-PILOT

| Mã năng lực | Mã trường hợp sử dụng | Năng lực và kết quả |
|---|---|---|
| **CAP-IAM-001** | `UC-IAM-001` | Khách đăng ký email/mật khẩu, xác minh email và trở thành người dùng `ACTIVE`. |
| **CAP-IAM-002** | `UC-IAM-002` | Người dùng đăng nhập, thực hiện MFA khi cần, làm mới/đăng xuất và quản lý phiên làm việc an toàn. |
| **CAP-IAM-003** | `UC-IAM-003` | Quản trị viên quản lý tài khoản/vai trò toàn cục; người kiểm toán đọc dữ liệu kiểm toán bảo mật. |
| **CAP-STU-001** | `UC-STU-001` | Khách xem danh mục; người học đăng ký và học khóa độc lập đã xuất bản. |
| **CAP-STU-002** | `UC-STU-002` | Người học hoàn tất quy trình làm quen, nhận gợi ý, chọn/chuyển lộ trình chính. |
| **CAP-STU-003** | `UC-STU-003` | Người học học khối/bài học, ghi tiến độ và hoàn thành khóa học/lộ trình theo phiên bản. |
| **CAP-STU-004** | `UC-STU-004` | Người học làm bài kiểm tra/văn bản/liên kết/tệp; hệ thống quét, chấm, duyệt và cho nộp lại. |
| **CAP-STU-005** | `UC-STU-005` | Study phát hành/thu hồi minh chứng; người học chọn minh chứng để xuất khi ứng tuyển. |
| **CAP-STU-006** | `UC-STU-006` | Nhà xuất bản đáng tin cậy soạn, kiểm tra và xuất bản phiên bản nội dung bất biến. |
| **CAP-STU-007** | `UC-STU-007` | Người học dùng thông báo, cộng đồng và hỗ trợ; nhân sự vận hành xử lý đúng phạm vi. |
| **CAP-STU-008** | `UC-STU-008` | Quản trị viên Study xem báo cáo, điều chỉnh có kiểm toán và quản lý RBAC cục bộ. |
| **CAP-WRK-001** | `UC-WRK-001` | Ứng viên tạo hồ sơ nghề nghiệp, CV/hồ sơ năng lực và bản chụp ứng tuyển. |
| **CAP-WRK-002** | `UC-WRK-002` | Nhà tuyển dụng tìm ứng viên đã chủ động cho phép tìm kiếm và gửi lời mời mà không làm lộ dữ liệu riêng. |
| **CAP-WRK-003** | `UC-WRK-003` | Chủ sở hữu/quản trị viên doanh nghiệp xác minh không gian dữ liệu và quản lý tư cách thành viên an toàn. |
| **CAP-WRK-004** | `UC-WRK-004` | Doanh nghiệp soạn bản sửa đổi, duyệt, xuất bản/tạm dừng/đóng việc làm. |
| **CAP-WRK-005** | `UC-WRK-005` | Ứng viên ứng tuyển; nhà tuyển dụng vận hành hồ sơ ứng tuyển qua ATS có kiểm toán. |
| **CAP-WRK-006** | `UC-WRK-006` | Work xuất bất đồng bộ minh chứng đã chọn và hiển thị trạng thái an toàn. |
| **CAP-WRK-007** | `UC-WRK-007` | Hai bên đề xuất/xác nhận/đổi lịch và hoàn tất phỏng vấn bằng lịch nội bộ/ICS. |
| **CAP-WRK-008** | `UC-WRK-008` | Ứng viên và nhà tuyển dụng được phân công trò chuyện văn bản thời gian thực theo hồ sơ ứng tuyển. |
| **CAP-WRK-009** | `UC-WRK-009` | Ứng viên dùng TopCV, doanh nghiệp dùng TopJD; vị trí tài trợ luôn có nhãn. |
| **CAP-WRK-010** | `UC-WRK-010` | Người kiểm duyệt xử lý báo cáo/gỡ bỏ và nền tảng xem báo cáo vận hành. |
| **CAP-UNI-001** | `UC-UNI-001` | Trường đại học quản lý không gian dữ liệu, liên kết và nhóm khóa. |
| **CAP-UNI-002** | `UC-UNI-002` | Trường đại học quản lý thực tập, việc làm trong trường, hợp tác và giới thiệu. |
| **CAP-UNI-003** | `UC-UNI-003` | Trường đại học xem dữ liệu có sự đồng ý hợp lệ và báo cáo tổng hợp bảo vệ quyền riêng tư. |
| **CAP-PAY-001** | `UC-PAY-001` | Người học/doanh nghiệp tạo đơn hàng VND trả trước và chuyển sang VNPAY/MoMo. |
| **CAP-PAY-002** | `UC-PAY-002` | Webhook/IPN xác nhận thanh toán hoàn tất chính xác một lần và cấp quyền lợi sử dụng. |
| **CAP-PAY-003** | `UC-PAY-003` | Nhân sự tài chính đối soát, hoàn tiền và xử lý tranh chấp thanh toán ngược có kiểm toán. |
| **CAP-AIX-001** | `UC-AIX-001` | AI tạo bản nháp CV/JD để người dùng sửa và chủ động chấp nhận. |
| **CAP-AIX-002** | `UC-AIX-002` | AI giải thích mức độ phù hợp/đề xuất danh sách rút gọn; nhà tuyển dụng tự quyết định ATS. |
| **CAP-AIX-003** | `UC-AIX-003` | Nhân sự vận hành quản trị mô hình/lời nhắc/đánh giá và duyệt thay đổi AI. |
| **CAP-OPS-001** | `UC-OPS-001` | Người kiểm duyệt xử lý nội dung vi phạm và hành động truy cập khẩn cấp có kiểm soát. |
| **CAP-OPS-002** | `UC-OPS-002` | Người dùng xuất/xóa dữ liệu; tạm giữ pháp lý và ẩn danh hóa tuân thủ chính sách. |
| **CAP-OPS-003** | `UC-OPS-003` | Đội vận hành quan sát, khôi phục, thử lại/DLQ và xử lý sự cố. |

### 5.1. Danh mục trường hợp sử dụng chuẩn

| ID | Tên trường hợp sử dụng |
|---|---|
| **UC-IAM-001** | Đăng ký và xác minh email |
| **UC-IAM-002** | Đăng nhập, MFA và quản lý phiên làm việc |
| **UC-IAM-003** | RBAC và quản trị vòng đời tài khoản |
| **UC-STU-001** | Xem danh mục và học khóa độc lập |
| **UC-STU-002** | Làm quen, gợi ý và lộ trình chính |
| **UC-STU-003** | Học bài học và ghi nhận tiến độ |
| **UC-STU-004** | Làm, chấm và duyệt bài đánh giá |
| **UC-STU-005** | Phát hành, xuất và thu hồi minh chứng |
| **UC-STU-006** | Soạn, kiểm tra và xuất bản nội dung |
| **UC-STU-007** | Thông báo, cộng đồng và hỗ trợ |
| **UC-STU-008** | Báo cáo và vận hành Study |
| **UC-WRK-001** | Quản lý hồ sơ ứng viên, CV và hồ sơ năng lực |
| **UC-WRK-002** | Tìm kiếm ứng viên và lời mời |
| **UC-WRK-003** | Quản trị không gian dữ liệu doanh nghiệp |
| **UC-WRK-004** | Soạn, duyệt và xuất bản bản sửa đổi việc làm |
| **UC-WRK-005** | Ứng tuyển và quản lý ATS |
| **UC-WRK-006** | Chọn minh chứng Study khi ứng tuyển |
| **UC-WRK-007** | Lập và quản lý phỏng vấn |
| **UC-WRK-008** | Trò chuyện theo hồ sơ ứng tuyển |
| **UC-WRK-009** | TopCV, TopJD và vị trí tài trợ |
| **UC-WRK-010** | Kiểm duyệt và báo cáo Work |
| **UC-UNI-001** | Không gian dữ liệu trường, liên kết và nhóm khóa |
| **UC-UNI-002** | Thực tập, việc làm trong trường và giới thiệu |
| **UC-UNI-003** | Sự đồng ý và báo cáo trường |
| **UC-PAY-001** | Tạo bước thanh toán VND |
| **UC-PAY-002** | Webhook/IPN và quyền lợi sử dụng |
| **UC-PAY-003** | Hoàn tiền, tranh chấp thanh toán ngược và đối soát |
| **UC-AIX-001** | Trợ lý soạn CV/JD |
| **UC-AIX-002** | Giải thích mức độ phù hợp và đề xuất danh sách rút gọn |
| **UC-AIX-003** | Quản trị và phê duyệt của con người |
| **UC-OPS-001** | Kiểm duyệt đa miền và truy cập khẩn cấp |
| **UC-OPS-002** | Xuất, xóa/ẩn danh hóa và tạm giữ pháp lý |
| **UC-OPS-003** | Quan sát, thử lại và khôi phục |

## 6. Hành trình đầu cuối

### 6.1. Từ đăng ký đến học tập

1. Khách đăng ký bằng email/mật khẩu và chấp nhận phiên bản điều khoản hiện hành. Danh tính nền tảng tạo tài khoản chờ xác minh, thông tin xác thực Argon2id và mã email dùng một lần.
2. Liên kết còn hạn và chưa dùng chuyển tài khoản sang `ACTIVE`; người dùng đăng nhập, nhận mã truy cập có hạn 15 phút và mã làm mới xoay vòng có hạn 30 ngày.
3. Người học có thể xem/đăng ký bất kỳ khóa độc lập nào đã xuất bản ngay, không cần hoàn tất quy trình làm quen.
4. Khi muốn chọn lộ trình chính, người học hoàn tất quy trình làm quen, xem tối đa ba đề xuất có lý do và chọn một phiên bản lộ trình hiện hành.
5. Người học học theo các sự kiện nội dung; hệ thống tính bản chụp tỷ lệ hoàn thành. Sau 168 giờ kể từ lần đổi lộ trình chính gần nhất, người học có thể tự chuyển; toàn bộ tiến độ/lần làm bài cũ vẫn được giữ.

### 6.2. Từ nội dung đến minh chứng

1. Tác giả tạo bản nháp phiên bản khóa học/lộ trình, chương, bài học, khối nội dung, tài nguyên, bài đánh giá và bản ghi quyền.
2. Kiểm tra trước xuất bản xác nhận cấu trúc, quyền, nội dung đã làm sạch, tài nguyên `CLEAN`, thang điểm/bài kiểm tra hợp lệ và liên kết phiên bản đầy đủ.
3. Một nhà xuất bản khác tác giả hoặc Quản trị viên Study có `study.content.publish` sẽ xuất bản. Bản đã xuất bản không bị sửa; bản mới thay thế bản cũ nhưng lượt đăng ký cũ vẫn ghim phiên bản cũ.
4. Bài kiểm tra được chấm tự động; bài văn bản/liên kết/tệp được duyệt thủ công. Tệp chỉ được nộp sau khi quét đạt `CLEAN`; máy chủ không tải liên kết HTTPS.
5. Khi hoàn thành hợp lệ, Study phát hành minh chứng bất biến theo phiên bản và sự kiện hộp gửi; thu hồi tạo sự kiện mới, không xóa lịch sử.

### 6.3. Từ hồ sơ nghề nghiệp đến tuyển dụng

1. Ứng viên tạo hồ sơ nghề nghiệp, CV và hồ sơ năng lực; hồ sơ tìm kiếm mặc định là `PRIVATE`.
2. Khi bật chủ động cho phép tìm kiếm, chỉ các trường công khai đã chọn mới được đưa vào chỉ mục ứng viên. Tắt lựa chọn này sẽ loại hồ sơ khỏi kết quả trong tối đa 5 phút.
3. Doanh nghiệp đã xác minh tạo bản sửa đổi việc làm, gửi duyệt, xuất bản và có thể tạm dừng/đóng. Nhà tuyển dụng tìm ứng viên đã cho phép tìm kiếm và gửi lời mời; lời mời chưa tạo hồ sơ ứng tuyển hoặc cuộc trò chuyện.
4. Ứng viên mở việc làm/lời mời, chọn bản chụp CV/hồ sơ và từng minh chứng Study muốn chia sẻ, xác nhận sự đồng ý rồi gửi một hồ sơ ứng tuyển duy nhất cho việc làm đó.
5. Work ghi nhận hồ sơ ứng tuyển dù Study đang lỗi; tiến trình nền xuất minh chứng sau. Nhà tuyển dụng thấy `PENDING`, `READY`, `UNAVAILABLE`, `REVOKED` hoặc `HIDDEN`, không được coi lỗi tích hợp là dấu hiệu để loại ứng viên.
6. Nhà tuyển dụng được phân công chuyển trạng thái ATS; hai bên trò chuyện, lên lịch phỏng vấn và xử lý đề nghị. Mọi trạng thái có tác nhân, lý do khi cần và kiểm toán; hồ sơ ứng tuyển kết thúc làm cuộc trò chuyện chỉ đọc.

### 6.4. Trường đại học và tuyển dụng trong trường

1. Chủ sở hữu trường đại học xác minh không gian dữ liệu, mời điều phối viên/người xem, tạo liên kết/nhóm khóa và chương trình thực tập.
2. Ứng viên tự chấp nhận liên kết và sự đồng ý cụ thể cho chương trình; trường đại học không tự gắn sinh viên chỉ bằng email.
3. Điều phối viên phân phối việc làm vào chương trình trong trường và tạo lượt giới thiệu có trạng thái; ứng viên vẫn phải chủ động ứng tuyển và chọn minh chứng.
4. Báo cáo mặc định là tổng hợp; mọi lát cắt dưới 10 người bị ẩn. Dữ liệu cá nhân chỉ hiện theo mục đích, phạm vi và thời hạn đồng ý.

### 6.5. Mua quyền lợi và vị trí tài trợ

1. Người học hoặc doanh nghiệp chọn gói/tín dụng, hệ thống chụp bản giá bằng số nguyên VND và tạo đơn hàng có tính bất biến theo yêu cầu.
2. Người mua chọn VNPAY hoặc MoMo và được chuyển đến nhà cung cấp. URL trả về chỉ hiển thị trạng thái đang xác nhận/đã xác nhận từ máy chủ.
3. Webhook/IPN hợp lệ chuyển thanh toán sang `SETTLED` đúng một lần; cùng giao dịch tạo sổ cái/quyền lợi sử dụng và hộp gửi.
4. TopCV/TopJD tiêu quyền lợi sử dụng qua sổ cái bất biến. Kết quả tài trợ có nhãn, nằm ở vị trí riêng và không sửa điểm tự nhiên/điểm phù hợp/điểm ATS.
5. Nhân sự tài chính đối soát sai lệch, hoàn tiền về nhà cung cấp gốc hoặc xử lý tranh chấp thanh toán ngược; hệ thống điều chỉnh quyền lợi và kiểm toán theo quy tắc tại mục 11.

### 6.6. AI có con người kiểm soát

1. Người dùng chủ động yêu cầu AI, xem dữ liệu đầu vào được dùng và tiêu tín dụng nếu gói yêu cầu.
2. Tiến trình nền lọc PII/thuộc tính cấm, ghim `provider`, `modelVersion`, `promptPolicyVersion` rồi gọi bộ điều hợp Ollama bất đồng bộ.
3. Dữ liệu đầu ra theo lược đồ là bản nháp/giải thích, được đánh dấu do AI tạo. Người dùng có thể chấp nhận, sửa hoặc loại bỏ.
4. Với ghép nối/danh sách rút gọn, nhà tuyển dụng phải tự thực hiện thao tác ATS; AI không có thông tin xác thực hoặc quyền gọi chuyển trạng thái hồ sơ ứng tuyển.

## 7. Quy tắc nghiệp vụ chuẩn

### 7.1. Danh tính và phân quyền

| ID | Quy tắc |
|---|---|
| **BR-IAM-001** | V1 chỉ đăng ký bằng email/mật khẩu. Email được cắt khoảng trắng, chuẩn hóa tên miền và so khớp không phân biệt hoa thường; mỗi email chỉ thuộc một người dùng nền tảng chưa ẩn danh hóa. |
| **BR-IAM-002** | Tài khoản phải xác minh email trước khi dùng API được bảo vệ. Mật khẩu chỉ lưu bản băm Argon2id; Study và Work không được lưu mật khẩu, mã xác minh hoặc mã làm mới. |
| **BR-IAM-003** | Mã truy cập ES256 có hạn 15 phút; mã làm mới dạng opaque có hạn tối đa 30 ngày, lưu bản băm, xoay ở mỗi lần dùng và thuộc một họ phiên làm việc. |
| **BR-IAM-004** | Dùng lại mã làm mới đã tiêu thụ phải lập tức thu hồi toàn bộ họ phiên làm việc, tăng tín hiệu bảo mật và ghi kiểm toán; máy khách phải đăng nhập lại. |
| **BR-IAM-005** | TOTP MFA và mã khôi phục dùng một lần là bắt buộc với người dùng đặc quyền. Thay đổi MFA, mật khẩu, email hoặc vai trò toàn cục thu hồi các phiên làm việc không còn tin cậy. |
| **BR-IAM-006** | Trạng thái tài khoản, khóa thông tin xác thực, trạng thái làm quen, tư cách thành viên không gian dữ liệu và lượt đăng ký học là các trạng thái độc lập. Sai mật khẩu chỉ đặt `lockedUntil`; không đổi tài khoản thành trạng thái học tập. |
| **BR-IAM-007** | Tạm ngưng hoặc chuyển sang chờ xóa phải thu hồi mọi phiên làm việc và phát sự kiện có chữ ký. Study/Work phải chặn yêu cầu nếu JWT hết hạn, `authVersion` cũ hoặc bản sao chiếu cho biết tài khoản không `ACTIVE`. |
| **BR-IAM-008** | Đặt lại mật khẩu, gửi lại xác minh và đăng nhập dùng phản hồi công khai không tiết lộ email có tồn tại; giới hạn tần suất kết hợp IP, email đã chuẩn hóa và tín hiệu thiết bị. |

### 7.2. Study

| ID | Quy tắc |
|---|---|
| **BR-STU-001** | Mọi khóa học có phiên bản hiện hành đã xuất bản đều có thể đăng ký học độc lập. Người học `ACTIVE` đã xác minh email không cần làm quen hoặc chọn lộ trình chính để học độc lập. |
| **BR-STU-002** | Quy trình làm quen chỉ bắt buộc trước khi chọn lộ trình chính. Việc hoàn tất là một chiều; chỉnh sửa hồ sơ tạo lần chạy đề xuất mới nhưng không đưa trạng thái lùi lại. |
| **BR-STU-003** | Mỗi người học có tối đa một giai đoạn lộ trình chính `ACTIVE`; chọn/chuyển dùng khóa giao dịch và ràng buộc duy nhất có điều kiện. |
| **BR-STU-004** | Tự chuyển lộ trình bị khóa đúng 168 giờ theo UTC kể từ lần thay đổi lộ trình chính gần nhất. Lần chọn đầu tiên và lần chọn sau khi lộ trình đã `COMPLETED` không bị thời gian chờ. |
| **BR-STU-005** | Quản trị viên chỉ được bỏ qua thời gian chờ khi có `PERM-STU-009` (`study.primary_path.override`), nhập lý do và xác nhận tác động; lộ trình mới vẫn có `nextSwitchAllowedAt = changedAt + 168 giờ`. |
| **BR-STU-006** | Chuyển lộ trình đóng giai đoạn cũ bằng `SWITCHED_OUT`, tạo giai đoạn mới một cách nguyên tử và không xóa lượt đăng ký khóa học, tiến độ, lần làm bài, lần duyệt, hoàn thành hoặc minh chứng. |
| **BR-STU-007** | Phiên bản lộ trình/khóa học đã xuất bản là bất biến. Xuất bản phiên bản mới phải đổi phiên bản hiện hành một cách nguyên tử và đánh dấu bản cũ `SUPERSEDED`; lượt đăng ký cũ tiếp tục ghim bản cũ. |
| **BR-STU-008** | Hoàn thành chỉ được tái sử dụng khi cùng `courseVersionId`; khóa học có cùng ID ổn định nhưng khác phiên bản không được tự kế thừa hoàn thành hoặc tiến độ. |
| **BR-STU-009** | Nguồn sự thật về tiến độ là các sự kiện hoàn thành của khối nội dung, bài học và bài đánh giá. Phần trăm khóa học/lộ trình chỉ là bản chụp do máy chủ tính, có thể dựng lại và máy khách không được ghi trực tiếp. |
| **BR-STU-010** | Bài đánh giá V1 chỉ có `QUIZ`, `TEXT`, `LINK`, `FILE`. Bài kiểm tra được chấm tự động; ba loại còn lại được duyệt thủ công theo thang điểm và mỗi lần nộp lại tạo một lần làm bài mới. |
| **BR-STU-011** | Tệp bài đánh giá phải ở trạng thái `CLEAN` trước khi nộp/tải xuống/duyệt; tệp nhiễm hoặc quét thất bại không tạo lần làm bài. Đối tượng được lưu riêng tư, URL tải có hạn và chỉ được cấp sau khi ủy quyền. |
| **BR-STU-012** | Liên kết bài đánh giá chỉ chấp nhận HTTPS, tối đa 2.048 ký tự; máy chủ không tải, tạo xem trước hoặc đi theo chuyển hướng để tránh SSRF. Văn bản tối đa 20.000 ký tự. |
| **BR-STU-013** | Mỗi vị trí đặt bài đánh giá thuộc đúng một phạm vi: phiên bản lộ trình, phiên bản khóa học, chương hoặc bài học. Quan hệ không hợp lệ bị chặn ở ứng dụng và bằng ràng buộc cơ sở dữ liệu. |
| **BR-STU-014** | Nhà xuất bản đáng tin cậy không được bỏ qua kiểm tra quyền, làm sạch HTML/Markdown, quét mã độc, cấu trúc chương trình học, thang điểm hoặc kiểm toán. Tác giả không tự có quyền xuất bản. |
| **BR-STU-015** | Điều chỉnh tiến độ/lần duyệt đã ghi chỉ đi qua nghiệp vụ sửa chính theo kiểu chỉ thêm, có tác nhân/lý do; không xóa hoặc cập nhật sự kiện gốc và không có API cho người học để tính lại/đặt lại. |
| **BR-STU-016** | Hoàn thành hợp lệ phát hành minh chứng `ISSUED` gắn chủ sở hữu và phiên bản nguồn chính xác. Thu hồi chuyển sang `REVOKED`, giữ lịch sử và phát sự kiện; không tái sử dụng ID đã thu hồi. |
| **BR-STU-017** | Thông báo có khóa khử trùng lặp; liên kết cộng đồng chỉ được trả sau khi người học chấp nhận đúng phiên bản quy tắc hiện hành; cộng đồng bên ngoài không được coi là kênh lưu dữ liệu chính thức. |

### 7.3. Work và tuyển dụng

| ID | Quy tắc |
|---|---|
| **BR-WRK-001** | Hồ sơ nghề nghiệp mặc định là `PRIVATE`. Chỉ ứng viên tự bật `SEARCHABLE`; không không gian dữ liệu, nhà tuyển dụng hoặc quản trị viên thông thường nào được bật thay. |
| **BR-WRK-002** | Tìm kiếm ứng viên chỉ chứa trường công khai đã chọn, kỹ năng/kinh nghiệm tổng quát và mức độ sẵn sàng; không trả email, điện thoại, tệp CV, địa chỉ chi tiết, hồ sơ ứng tuyển, minh chứng Study hoặc thuộc tính nhạy cảm. |
| **BR-WRK-003** | Tắt cho phép tìm kiếm phải làm hồ sơ biến mất khỏi kết quả và bộ nhớ đệm trong tối đa 5 phút. Bản chụp/kiểm toán hợp pháp đã có trong hồ sơ ứng tuyển không bị xóa vì tắt tìm kiếm. |
| **BR-WRK-004** | Mọi truy vấn doanh nghiệp/trường đại học lấy không gian dữ liệu từ tư cách thành viên đang hoạt động ở máy chủ và lọc bằng khóa không gian dữ liệu; ID tài nguyên do máy khách gửi không bao giờ đủ để cấp quyền. Ràng buộc không gian dữ liệu ghép ngăn liên kết chéo không gian dữ liệu. |
| **BR-WRK-005** | Doanh nghiệp phải `VERIFIED` mới được xuất bản việc làm, tìm ứng viên, gửi lời mời hoặc mua quyền lợi cho không gian dữ liệu. Tạm ngưng chặn thay đổi mới nhưng giữ kiểm toán/lịch sử. |
| **BR-WRK-006** | Việc làm dùng thực thể ổn định và bản sửa đổi bất biến. Sửa việc làm đang xuất bản tạo bản sửa đổi nháp mới; bản đang xuất bản vẫn phục vụ đến khi bản mới được duyệt và hoán đổi một cách nguyên tử. |
| **BR-WRK-007** | Vòng đời việc làm duy nhất là `DRAFT → REVIEW_PENDING → PUBLISHED ↔ PAUSED → CLOSED\|EXPIRED\|TAKEN_DOWN`; chuyển trạng thái phải đúng quyền, phiên bản và có kiểm toán. |
| **BR-WRK-008** | Mỗi ứng viên chỉ có một hồ sơ ứng tuyển cho một việc làm. Phát lại yêu cầu bất biến trả hồ sơ cũ; gửi dữ liệu đầu vào khác sau khi đã có hồ sơ trả xung đột. |
| **BR-WRK-009** | Vòng đời hồ sơ ứng tuyển là `SUBMITTED → UNDER_REVIEW → SHORTLISTED → INTERVIEWING → OFFERED → HIRED`, với các trạng thái kết thúc `REJECTED`, `WITHDRAWN`, `OFFER_DECLINED`; mọi chuyển trạng thái ghi tác nhân, thời điểm và lý do bắt buộc khi từ chối. |
| **BR-WRK-010** | Ứng viên có thể chuyển sang `WITHDRAWN` từ `SUBMITTED`, `UNDER_REVIEW`, `SHORTLISTED` hoặc `INTERVIEWING`; ở `OFFERED`, việc từ chối của ứng viên phải là `OFFER_DECLINED`. Nhà tuyển dụng có thể chuyển sang `REJECTED` ở mọi trạng thái trước `HIRED`. Việc làm đã đóng không tự đổi hồ sơ ứng tuyển đang xử lý. |
| **BR-WRK-011** | Khi ứng tuyển, Work chụp bất biến bản sửa đổi việc làm, hồ sơ nghề nghiệp, CV và hồ sơ năng lực được chọn. Thay đổi hồ sơ/CV/việc làm sau đó không sửa bản chụp hồ sơ ứng tuyển. |
| **BR-WRK-012** | Lời mời chỉ có thời hạn; không tạo hồ sơ ứng tuyển, không cấp thông tin liên hệ và không mở trò chuyện. Ứng viên phải chủ động gửi hồ sơ ứng tuyển. |
| **BR-WRK-013** | Mỗi hồ sơ ứng tuyển có tối đa một cuộc trò chuyện 1–1. Chỉ ứng viên và nhà tuyển dụng đang hoạt động, được phân công mới tham gia; hồ sơ ứng tuyển kết thúc chuyển cuộc trò chuyện sang `READ_ONLY`. |
| **BR-WRK-014** | Lịch sử REST là nguồn sự thật của trò chuyện; WebSocket chỉ phân phối sự kiện. Máy khách kết nối lại bằng con trỏ, gửi tin nhắn có tính bất biến theo yêu cầu và thứ tự chuẩn theo số thứ tự của máy chủ. |
| **BR-WRK-015** | Phỏng vấn dùng các phiên bản lịch bất biến. Ứng viên có thể xác nhận, từ chối hoặc yêu cầu đổi lịch; yêu cầu đổi lịch không sửa khung giờ. Nhà tuyển dụng chấp nhận yêu cầu bằng cách tạo phiên bản `PROPOSED` mới; lịch nội bộ và ICS là nguồn của V1, không khẳng định đã đồng bộ với lịch ngoài. |
| **BR-WRK-016** | Nhà tuyển dụng/người phỏng vấn chỉ xem buổi phỏng vấn và phần hồ sơ được phân công. Phản hồi của người phỏng vấn không tự đổi trạng thái hồ sơ ứng tuyển và không hiển thị cho ứng viên trừ phần do nhà tuyển dụng công bố. |
| **BR-WRK-017** | Hồ sơ/việc làm tài trợ luôn có nhãn, vị trí/xếp hạng riêng và trường `organicScore` không đổi. Thanh toán không được tăng điểm phù hợp, điểm ATS hoặc quyền xem trường riêng tư. |
| **BR-WRK-018** | Kiểm duyệt gỡ bỏ giữ bản sửa đổi, hồ sơ ứng tuyển và kiểm toán; chặn khám phá/ứng tuyển mới nhưng không xóa lịch sử tuyển dụng hợp pháp. |

### 7.4. Minh chứng khi ứng tuyển và tích hợp

| ID | Quy tắc |
|---|---|
| **BR-INT-001** | Danh tính nền tảng, Study và Work dùng ba PostgreSQL vật lý riêng; không có khóa ngoại, phép nối, ghi dùng chung hoặc đọc trực tiếp cơ sở dữ liệu của nhau. |
| **BR-INT-002** | Tích hợp dùng hợp đồng có phiên bản, danh tính dịch vụ có chữ ký, hộp gửi theo giao dịch và bên nhận có tính bất biến theo ID sự kiện/yêu cầu; việc chuyển phát là ít nhất một lần. |
| **BR-INT-003** | `platformUserId` là UUID bất biến làm khóa liên hệ; không dùng email hoặc ID cục bộ của Study/Work làm khóa tích hợp. |
| **BR-INT-004** | Trình hướng dẫn ứng tuyển dùng mã truy cập đúng đối tượng Study để người học chỉ liệt kê minh chứng của chính mình; mã Work hoặc mã dịch vụ không được dùng để duyệt toàn bộ lịch sử Study. |
| **BR-INT-005** | Ứng viên chọn rõ từng minh chứng và phiên bản sự đồng ý trước khi gửi. Giao dịch hồ sơ ứng tuyển lưu ID đã chọn, sự đồng ý, yêu cầu xuất và hộp gửi; Study lỗi không hoàn tác hồ sơ ứng tuyển. |
| **BR-INT-006** | Tiến trình nền Work gửi yêu cầu xuất có chữ ký. Study kiểm tra chủ sở hữu, `ISSUED`, nguồn/phiên bản và thu hồi, rồi chỉ trả bản chụp tối thiểu; Work lưu bản chụp gắn duy nhất với `applicationId`. |
| **BR-INT-007** | Trạng thái xuất minh chứng tại Work là `PENDING`, `READY`, `UNAVAILABLE`, `REVOKED` hoặc `HIDDEN`. `UNAVAILABLE`/hết thời gian chờ không được tự từ chối, hạ điểm hoặc ẩn hồ sơ ứng tuyển. |
| **BR-INT-008** | Thu hồi sự đồng ý chuyển bản chụp sang `HIDDEN`; thu hồi ở Study chuyển sang `REVOKED`. Nội dung không còn hiển thị cho nhà tuyển dụng nhưng kiểm toán tối thiểu được giữ theo thời hạn lưu giữ. |
| **BR-INT-009** | Sự kiện trùng/lỗi thời bị bỏ qua theo phiên bản tổng thể; khoảng trống sự kiện vào luồng thử lại/bắt kịp. Sự kiện lỗi độc hại vào DLQ và không được đánh dấu thành công giả. |

### 7.5. Trường đại học

| ID | Quy tắc |
|---|---|
| **BR-UNI-001** | Trường đại học là không gian dữ liệu độc lập với doanh nghiệp; liên kết do ứng viên chấp nhận, có trạng thái/thời hạn và không được suy ra chỉ từ tên miền email. |
| **BR-UNI-002** | Tư cách thành viên nhóm khóa/chương trình không tự cấp quyền xem hồ sơ nghề nghiệp, hồ sơ ứng tuyển hoặc dữ liệu Study; mỗi mục đích cần sự đồng ý có phạm vi và thời hạn. |
| **BR-UNI-003** | Phân phối trong trường/giới thiệu không tạo hồ sơ ứng tuyển thay ứng viên và không tự chia sẻ minh chứng. Ứng viên vẫn chọn việc làm, bản chụp và sự đồng ý như khi ứng tuyển thông thường. |
| **BR-UNI-004** | Báo cáo trường đại học mặc định là tổng hợp và chỉ trả lát cắt có ít nhất 10 cá nhân; nhóm nhỏ trả trạng thái bị ẩn, không làm tròn để suy ngược. |
| **BR-UNI-005** | Khi sự đồng ý hết hạn/bị thu hồi hoặc tư cách thành viên kết thúc, dữ liệu cá nhân biến mất khỏi màn hình trường đại học; dữ liệu tổng hợp đã khử định danh hợp lệ được giữ theo thời hạn lưu giữ. |

### 7.6. Thanh toán và quyền lợi sử dụng

| ID | Quy tắc |
|---|---|
| **BR-PAY-001** | V1 chỉ hỗ trợ gói/tín dụng trả trước bằng VND qua VNPAY và MoMo cho người học hoặc doanh nghiệp; số tiền là số nguyên VND, không tự động gia hạn. |
| **BR-PAY-002** | Hệ thống không thu/lưu PAN, CVV, tài khoản ngân hàng hoặc thông tin xác thực của nhà cung cấp; không có ví nội bộ, ký quỹ trung gian, chi trả hoặc số dư rút tiền. |
| **BR-PAY-003** | Đơn hàng giữ bản chụp bất biến của gói, giá, thuế/giảm giá nếu có, loại/ID người mua và phiên bản chính sách. Thay đổi danh mục không sửa đơn hàng cũ. |
| **BR-PAY-004** | Webhook/IPN đã xác thực chữ ký và đối chiếu bên bán/đơn hàng/số tiền/đơn vị tiền tệ là nguồn xác nhận. URL trả về không được cấp quyền lợi sử dụng hoặc tự đánh dấu thanh toán thành công. |
| **BR-PAY-005** | Phản hồi gọi lại trùng/không theo thứ tự được lưu với dữ liệu đầu vào thô đã bảo vệ, xử lý bất biến theo yêu cầu và theo thứ tự ưu tiên trạng thái; lỗi đến muộn không hạ `SETTLED`. Sai lệch số tiền/đơn hàng vào duyệt, không cấp quyền lợi. |
| **BR-PAY-006** | Chỉ `SETTLED` tạo sổ cái quyền lợi/tín dụng đúng một lần trong cùng giao dịch. Quyền lợi sử dụng không được âm; mọi tiêu dùng/hoàn tiền/hết hạn đều chỉ thêm vào sổ cái. |
| **BR-PAY-007** | Đơn hàng chưa xác nhận quá thời hạn của nhà cung cấp chuyển sang `EXPIRED`. `CANCELLED` chỉ được ghi khi nhà cung cấp/chưa khởi tạo lần xác nhận chưa thu tiền; thành công đã xác minh có ưu tiên cao hơn trong cùng khóa hàng. Phản hồi gọi lại thành công hợp lệ đến muộn được xử lý qua đối soát và không cấp trùng. |
| **BR-PAY-008** | Hoàn tiền chỉ do nhân sự tài chính khởi tạo về nhà cung cấp gốc, không vượt số tiền đã hoàn tất trừ các khoản hoàn trước. Hệ thống chỉ thu hồi phần quyền lợi chưa tiêu tương ứng; yêu cầu vượt giá trị chưa tiêu cần phê duyệt ngoại lệ và ghi cờ nợ/rủi ro. |
| **BR-PAY-009** | Tranh chấp thanh toán ngược được nhà cung cấp xác nhận đóng băng quyền lợi còn lại, đặt cờ rủi ro và tạo hồ sơ việc vụ cho Tài chính. Quyền lợi đã tiêu không bị xóa lịch sử; nợ được theo dõi, không tự trừ vào đơn hàng khác. |
| **BR-PAY-010** | Đối soát chạy tự động hằng ngày và theo yêu cầu; sai lệch có mức độ, chủ sở hữu và kiểm toán. Không nhân sự vận hành nào được sửa webhook thô hoặc sổ cái đã ghi. |

### 7.7. AI và sản phẩm tài trợ

| ID | Quy tắc |
|---|---|
| **BR-AIX-001** | AI xử lý bất đồng bộ qua bộ điều hợp nhà cung cấp; nhà cung cấp mặc định của V1 là Ollama. Mỗi tác vụ ghim nhà cung cấp, phiên bản mô hình, phiên bản chính sách lời nhắc, bản băm đầu vào và phiên bản lược đồ đầu ra. |
| **BR-AIX-002** | AI chỉ tạo bản nháp CV/JD, gợi ý viết, giải thích mức độ phù hợp và đề xuất danh sách rút gọn. Dữ liệu đầu ra không tự xuất bản, gửi, ứng tuyển, thay đổi ATS, từ chối, đề nghị hoặc tuyển dụng. |
| **BR-AIX-003** | Người dùng phải nhìn thấy nhãn AI, duyệt và chủ động chấp nhận/sửa/từ chối. Bản được chấp nhận lưu nội dung do người dùng xác nhận, không giả định AI đúng. |
| **BR-AIX-004** | Ghép nối chỉ dùng kỹ năng, kinh nghiệm, học vấn công khai, tiêu chí việc làm và sở thích nghề nghiệp được phép; loại trừ giới tính, tuổi/ngày sinh, ảnh, dân tộc, tôn giáo, khuyết tật, tình trạng hôn nhân, địa chỉ chi tiết, thanh toán và trạng thái tài trợ. |
| **BR-AIX-005** | Tệp thô, thông tin liên hệ, trò chuyện riêng, phản hồi mật và lịch sử Study chưa được chọn không gửi vào AI. Minh chứng chỉ dùng trường có cấu trúc đã được đồng ý cho hồ sơ ứng tuyển tương ứng. |
| **BR-AIX-006** | Dữ liệu đầu vào được giới hạn, tách khỏi chỉ dẫn hệ thống và kiểm soát chèn lời nhắc; dữ liệu đầu ra phải qua kiểm tra lược đồ, bộ lọc an toàn và không được thực thi như lệnh/cuộc gọi công cụ. |
| **BR-AIX-007** | Lỗi/hết thời gian chờ AI không chặn tạo/sửa CV, việc làm, ứng tuyển hoặc ATS thủ công. Việc thử lại có giới hạn; người dùng không bị trừ tín dụng lần hai cho lần thử lại kỹ thuật của cùng tác vụ. |
| **BR-AIX-008** | Mô hình/lời nhắc mới phải qua đánh giá, rà soát thiên lệch/an toàn và phát hành thăm dò trước khi `ACTIVE`. Quay lại phiên bản trước không sửa dữ liệu đầu ra lịch sử; mọi ghi đè có kiểm toán. |

### 7.8. Vận hành, kiểm toán và dữ liệu

| ID | Quy tắc |
|---|---|
| **BR-OPS-001** | Kiểm toán, webhook bảo mật/thanh toán, sổ cái, lịch sử hồ sơ ứng tuyển, bản chụp minh chứng, duyệt AI và hộp gửi đều chỉ thêm; không xóa dây chuyền làm mất lịch sử. |
| **BR-OPS-002** | Kiểm toán chứa tác nhân, vai trò/không gian dữ liệu hiệu lực, hành động, tài nguyên, dữ liệu trước/sau đã che, lý do, IP/thiết bị tối thiểu, ID vết và thời điểm UTC; không chứa bí mật/mã thông báo/mật khẩu thô. |
| **BR-OPS-003** | Thông báo và tác dụng phụ ngoài giao dịch được tạo qua hộp gửi với khóa khử trùng lặp. Thử lại lũy thừa có giới hạn; hết số lần thử lại thì vào DLQ và phát cảnh báo. |
| **BR-OPS-004** | PII được mã hóa khi truyền và khi lưu; kho đối tượng riêng tư theo không gian tên chủ sở hữu. URL có chữ ký ngắn hạn không được ghi vào kiểm toán, phân tích hoặc trường tham chiếu nguồn. |
| **BR-OPS-005** | Người dùng chỉ xuất dữ liệu của chính mình ở định dạng máy đọc được; xuất dữ liệu không gian dữ liệu phải qua quyền, phạm vi và kiểm toán, không được bỏ qua sự đồng ý. |
| **BR-OPS-006** | Xóa tài khoản có thời gian ân hạn 30 ngày. Hết thời gian này: thu hồi phiên làm việc/minh chứng/sự đồng ý, xóa PII và tệp riêng tư không bị tạm giữ pháp lý, hủy liên kết và ẩn danh hóa các sự kiện cần giữ. |
| **BR-OPS-007** | Tạm giữ pháp lý chỉ do quyền được ủy quyền thực hiện, phải có căn cứ, phạm vi, ngày hết hạn/rà soát và kiểm toán; việc tạm giữ dừng xóa đúng bản ghi nhưng không khôi phục quyền hiển thị. |
| **BR-OPS-008** | Khôi phục sao lưu phải áp lại sổ cái xóa/thu hồi trước khi mở lưu lượng để dữ liệu đã xóa/thu hồi không xuất hiện trở lại. |
| **BR-OPS-009** | Mọi mốc thời gian nghiệp vụ lưu theo UTC, UUID dùng cho định danh công khai; JSON dùng camelCase, cơ sở dữ liệu dùng snake_case. |
| **BR-OPS-010** | Thay đổi quan trọng dùng tính bất biến theo yêu cầu/phiên bản lạc quan theo hợp đồng; xung đột không được âm thầm ghi đè và phải trả phiên bản hiện hành an toàn để máy khách tải lại. |

### 7.9. Chính sách nhà xuất bản đáng tin cậy

- **Study:** chỉ nhân sự nội bộ/đối tác nội dung đã được định danh, hoàn tất đào tạo xuất bản, bật MFA và có vai trò cục bộ `CONTENT_PUBLISHER` mới đủ điều kiện nhận quyền cấp. Quyền cấp nêu phạm vi lộ trình/khóa học, có hiệu lực tối đa 180 ngày và mặc định người xuất bản phải khác người sửa phiên bản gần nhất. Trong giai đoạn khởi động thử nghiệm, Quản trị viên nền tảng có thể cho phép cùng một người khi ghi `bootstrapPilot`, lý do và kiểm tra trước xuất bản độc lập; hành động được cảnh báo/kiểm toán.
- **Work:** doanh nghiệp phải `VERIFIED`; người nhận quyền cấp là thành viên `ACTIVE` có MFA. Quyền cấp chỉ được tạo khi không gian dữ liệu đã có ít nhất ba bản sửa đổi việc làm được duyệt và không có vi phạm nội dung/bảo mật đã xác nhận trong 90 ngày gần nhất; hiệu lực tối đa 180 ngày và chỉ trong đúng không gian dữ liệu/phạm vi.
- **Kiểm tra không thể bỏ qua:** quyền cấp chỉ bỏ bước chờ duyệt thủ công khi chính sách cho phép; kiểm tra quyền/tuyên bố, làm sạch, quét mã độc, cấu trúc, nội dung bị cấm, không gian dữ liệu/tài khoản/quyền lợi sử dụng và phiên bản lạc quan vẫn bắt buộc trên từng lần xuất bản.
- **Thu hồi:** tạm ngưng tài khoản/không gian dữ liệu, vi phạm nghiêm trọng, lộ khóa hoặc quyền cấp hết hạn làm mất quyền xuất bản ngay. Thu hồi không xóa bản xuất bản cũ; bản xuất bản vi phạm đi qua quy trình gỡ bỏ riêng. Chỉ `PERM-OPS-003` kèm MFA gần đây, phân tách nhiệm vụ và lý do mới được cấp/thu hồi quyền cấp.

## 8. Máy trạng thái chuẩn

### 8.1. Danh tính và Study

| Đối tượng tổng hợp | Chuyển trạng thái hợp lệ | Quy tắc bổ sung |
|---|---|---|
| Tài khoản | `PENDING_EMAIL_VERIFICATION → ACTIVE`; `ACTIVE ↔ SUSPENDED`; mọi trạng thái chưa kết thúc `→ DELETION_PENDING → ANONYMIZED` | Hủy xóa trong thời gian ân hạn sẽ trở về trạng thái trước đó; `ANONYMIZED` là trạng thái kết thúc. Khóa thông tin xác thực không phải trạng thái tài khoản. |
| Làm quen | `NOT_STARTED → IN_PROGRESS → COMPLETED` | Không chuyển lùi; đề xuất có phiên bản/lần chạy riêng. |
| Phiên bản nội dung | `DRAFT → PUBLISHED → SUPERSEDED`; `DRAFT → DISCARDED` | Bản đã xuất bản/được thay thế là bất biến. Thực thể ổn định có `ACTIVE → ARCHIVED`; lưu trữ không xóa phiên bản đang được tham chiếu. |
| Giai đoạn lộ trình chính | Không có lộ trình `→ ACTIVE`; `ACTIVE → SWITCHED_OUT\|COMPLETED\|CANCELLED_BY_ADMIN` | Chuyển lộ trình tạo `ACTIVE` mới trong cùng giao dịch; tối đa một trạng thái hoạt động. |
| Lượt đăng ký khóa học | `ENROLLED → IN_PROGRESS → COMPLETED` | Không chuyển lùi khi ôn tập; ẩn khỏi giao diện chỉ là tùy chọn. |
| Tiến độ bài học | `NOT_STARTED → IN_PROGRESS → COMPLETED` | Đơn điệu; sửa chính là sự kiện chỉ thêm. |
| Tài nguyên tệp | `CREATED → UPLOADING → UPLOADED → SCANNING → CLEAN\|INFECTED\|SCAN_FAILED`; `CLEAN → ATTACHED`; trạng thái chưa dùng `→ EXPIRED`, hợp lệ `→ DELETED` theo thời hạn lưu giữ | Chỉ `CLEAN` được đính kèm/nộp/tải xuống bởi người duyệt. Quét thất bại thử lại tối đa ba lần. |
| Lần làm bài kiểm tra | `SUBMITTED → PASSED\|FAILED` | Chấm tự động; lần làm bài được niêm phong, không sửa. |
| Lần làm bài văn bản/liên kết/tệp | `SUBMITTED → UNDER_REVIEW → PASSED\|NEEDS_REVISION\|FAILED` | `NEEDS_REVISION`/`FAILED` cho phép lần làm bài mới nếu còn hạn ngạch. |
| Minh chứng Study | `ISSUED → REVOKED` | Cả hai trạng thái đều giữ kiểm toán; phát hành lại tạo ID/phiên bản minh chứng mới. |

### 8.2. Work, trường đại học, thanh toán và AI

| Đối tượng tổng hợp | Chuyển trạng thái hợp lệ | Quy tắc bổ sung |
|---|---|---|
| Mức hiển thị ứng viên | `PRIVATE ↔ SEARCHABLE` | Tắt cho phép tìm kiếm đồng bộ chỉ mục/bộ nhớ đệm tối đa 5 phút; không ảnh hưởng bản chụp hồ sơ ứng tuyển. |
| Xác minh không gian dữ liệu | `PENDING_VERIFICATION → VERIFIED\|REJECTED`; `VERIFIED ↔ SUSPENDED` | Gửi lại sau khi bị từ chối tạo yêu cầu/phiên bản xác minh mới, không sửa quyết định cũ. |
| Việc làm | `DRAFT → REVIEW_PENDING → PUBLISHED`; `PUBLISHED ↔ PAUSED`; `PUBLISHED\|PAUSED → CLOSED\|EXPIRED\|TAKEN_DOWN` | `CLOSED`, `EXPIRED`, `TAKEN_DOWN` là trạng thái kết thúc; bản sửa đổi mới không mở lại việc làm ổn định đã kết thúc. |
| Lời mời | `SENT → VIEWED → ACCEPTED\|DECLINED\|EXPIRED`; `SENT\|VIEWED → CANCELLED` | `ACCEPTED` chỉ dẫn tới trình hướng dẫn ứng tuyển, chưa tạo hồ sơ ứng tuyển/trò chuyện. |
| Hồ sơ ứng tuyển | `SUBMITTED → UNDER_REVIEW → SHORTLISTED → INTERVIEWING → OFFERED → HIRED`; từ `SUBMITTED\|UNDER_REVIEW\|SHORTLISTED\|INTERVIEWING → REJECTED\|WITHDRAWN`; từ `OFFERED → HIRED\|REJECTED\|OFFER_DECLINED` | `HIRED`, `REJECTED`, `WITHDRAWN`, `OFFER_DECLINED` là trạng thái kết thúc qua API thông thường; không được bỏ qua bước tiến tiếp. |
| Xuất minh chứng | `PENDING → READY\|UNAVAILABLE`; `READY → REVOKED\|HIDDEN`; `UNAVAILABLE → PENDING` khi chủ động thử lại còn thời hạn đồng ý | `HIDDEN`/`REVOKED` không hiển thị nội dung; kiểm toán vẫn được giữ. |
| Phỏng vấn | `PROPOSED → CONFIRMED → COMPLETED\|NO_SHOW`; `PROPOSED\|CONFIRMED → CANCELLED` | Phản hồi `RESCHEDULE_REQUESTED` của ứng viên là sự kiện chờ xử lý, không phải trạng thái vòng đời. Khi nhà tuyển dụng chấp nhận, tạo phiên bản lịch mới ở `PROPOSED` và thay thế phiên bản cũ. |
| Cuộc trò chuyện | `ACTIVE → READ_ONLY` | Chuyển khi hồ sơ ứng tuyển kết thúc; tin nhắn cũ không sửa/xóa khỏi lịch sử ngoài quy trình kiểm duyệt/che dữ liệu có kiểm toán. |
| Liên kết trường đại học | `INVITED\|REQUESTED → ACTIVE\|DECLINED`; `ACTIVE → EXPIRED\|REVOKED` | Ứng viên phải xác nhận; hoạt động không đồng nghĩa đã đồng ý dùng dữ liệu cá nhân. |
| Điều phối đơn hàng thanh toán | `CREATED → PENDING → SETTLED\|FAILED\|EXPIRED\|CANCELLED` | `SETTLED` không bị ghi đè bởi hoàn tiền/tranh chấp thanh toán ngược; hoàn tiền, tranh chấp thanh toán ngược và điều chỉnh quyền lợi là hồ sơ việc vụ/sổ cái chỉ thêm riêng. Phản hồi gọi lại cũ không hạ trạng thái có ưu tiên cao. |
| Quyền lợi sử dụng | `ACTIVE → EXHAUSTED\|EXPIRED\|FROZEN\|REVOKED`; `FROZEN → ACTIVE\|REVOKED` | Sổ cái quyết định số dư; không tự gia hạn, không âm. |
| Tác vụ AI | `QUEUED → RUNNING → SUCCEEDED\|FAILED\|CANCELLED` | Duyệt dữ liệu đầu ra là `DRAFT → ACCEPTED\|EDITED_ACCEPT\|REJECTED\|EXPIRED`; chỉ hành động của con người mới tạo nội dung đã chấp nhận/đã sửa và không tự tạo hành động ATS. |

## 9. Kiến trúc mục tiêu và công nghệ đã khóa

### 9.1. Cấu trúc triển khai

Study2Work gồm ba dịch vụ phía máy chủ có thể triển khai độc lập và hai ứng dụng web. Mỗi dịch vụ là một khối đơn mô-đun theo ngữ cảnh giới hạn, có cơ sở dữ liệu, `migration` và chuỗi triển khai riêng. V1 không tách vi dịch vụ theo mô-đun.

| Khối | Thành phần và ngăn xếp bắt buộc |
|---|---|
| Danh tính nền tảng | FastAPI, Python, SQLAlchemy, Alembic, PostgreSQL; Argon2id; JWT ES256/JWKS; tiến trình nền email/sự kiện bảo mật. |
| Web Study | Vue 3, TypeScript, Vite, Tailwind CSS, Pinia cho trạng thái máy khách, TanStack Query cho trạng thái máy chủ, Axios và Zod tại biên API. |
| Dịch vụ phía máy chủ Study | Khối đơn mô-đun FastAPI, SQLAlchemy/Alembic, PostgreSQL, Redis, tiến trình nền ARQ, kho đối tượng riêng tư S3/MinIO, ClamAV. |
| Web Work | React, TypeScript, Vite, Tailwind CSS, Zustand cho trạng thái máy khách, TanStack Query, React Hook Form và Zod. |
| Dịch vụ phía máy chủ Work | NestJS chạy Fastify, Prisma/PostgreSQL, Redis/BullMQ, cổng WebSocket, kho đối tượng riêng tư S3/MinIO. |
| Tìm kiếm | Tìm kiếm toàn văn PostgreSQL + `pg_trgm`, chỉ mục/bản sao chiếu cụ thể hóa cục bộ; chưa dùng Elasticsearch/OpenSearch. |
| AI | Tiến trình nền Work gọi bộ điều hợp nhà cung cấp; Ollama là nhà cung cấp mặc định cho thử nghiệm. Máy chủ mô hình không được truy cập cơ sở dữ liệu trực tiếp. |
| Hệ thống ngoài | Nhà cung cấp email, VNPAY, MoMo; mọi phản hồi gọi lại đi qua API chuyên biệt, kiểm tra chữ ký và lưu kiểm toán. |
| Quan sát | Nhật ký có cấu trúc, chỉ số, vết phân tán/ID vết, bảng điều khiển và cảnh báo theo SLO; không tùy tiện ghi dữ liệu đầu vào có bí mật/PII. |

Mỗi giao diện chỉ gọi API công khai của Danh tính nền tảng/Study/Work qua HTTPS. Điểm cuối nội bộ không được công bố bằng cùng đường dẫn/điểm vào công khai. Redis, hàng đợi và không gian tên đối tượng tách theo phân hệ; không dùng một mục bộ nhớ đệm làm nguồn sự thật xuyên miền.

### 9.2. Ranh giới mô-đun

| Dịch vụ triển khai | Mô-đun nghiệp vụ |
|---|---|
| Danh tính nền tảng | Đăng ký/Xác minh, Thông tin xác thực, Phiên làm việc/MFA, RBAC toàn cục, Vòng đời tài khoản, Kiểm toán bảo mật, Hộp gửi. |
| Study | Bản sao chiếu danh tính, Hồ sơ/Làm quen, Danh mục/Xuất bản, Đăng ký/Tiến độ, Bài đánh giá/Bảo mật tệp, Minh chứng, Tương tác/Hỗ trợ, RBAC/Kiểm toán/Báo cáo Study, Tích hợp. |
| Work | Bản sao chiếu danh tính, Hồ sơ nghề nghiệp/CV/Hồ sơ năng lực, Doanh nghiệp, Trường đại học, Việc làm/Tìm nguồn, Hồ sơ ứng tuyển/ATS, Bản chụp minh chứng, Phỏng vấn/Trò chuyện, AI/Ghép nối, Thanh toán/Quyền lợi sử dụng/Khuyến mại, Tệp/Thông báo/Kiểm duyệt/Kiểm toán, Tích hợp. |

Mỗi mô-đun chỉ ghi các bảng do mình sở hữu. Tác dụng phụ sang mô-đun khác trong cùng dịch vụ triển khai đi qua dịch vụ ứng dụng/sự kiện miền sau khi xác nhận giao dịch; kho truy cập dữ liệu không được gọi chéo tùy ý hoặc cập nhật bảng của mô-đun khác.

### 9.3. Quy ước API dùng chung

- API công khai dùng `/api/v1`; dịch vụ với dịch vụ dùng `/internal/v1`; Danh tính nền tảng công bố `/.well-known/jwks.json`.
- Mỗi hệ thống có máy chủ riêng: Danh tính nền tảng, Study và Work có bên phát hành/đối tượng rõ ràng. Dịch vụ phía máy chủ kiểm tra `iss`, `aud`, `exp`, `jti`, `sid`, `sub`, `authVersion`; không tin vai trò/ID không gian dữ liệu do máy khách tự thêm.
- JSON dùng camelCase, UUID, ISO-8601 UTC. Phản hồi thống nhất gồm `success`, `businessCode`, `message`, `data`, `meta`, `traceId`.
- Phân trang theo trang dùng cho danh mục/danh sách quản trị ổn định; phân trang theo con trỏ dùng cho trò chuyện, thông báo, luồng kiểm toán/hoạt động. Sắp xếp có ID phân xử để không mất/trùng bản ghi.
- `Idempotency-Key` bắt buộc cho đăng ký, đăng ký học/chuyển lộ trình, nộp/duyệt bài đánh giá, xuất bản, ứng tuyển, thanh toán, thay đổi phỏng vấn và gửi trò chuyện. Cùng khóa với dữ liệu đầu vào khác trả xung đột.
- `If-Match`/phiên bản bắt buộc cho trình soạn thảo bản nháp, duyệt xuất bản, cập nhật ATS/phỏng vấn và tài nguyên có nguy cơ ghi đồng thời.
- Lỗi nghiệp vụ dùng mã ổn định, trạng thái HTTP đúng ngữ nghĩa và thông điệp an toàn; xác thực dữ liệu không trả vết ngăn xếp, SQL hoặc sự tồn tại của tài nguyên ngoài quyền.
- WebSocket chỉ xác thực bằng mã thông báo ngắn hạn do API Work cấp sau khi ủy quyền; kết nối lại lấy lịch sử/con trỏ qua REST.

### 9.4. Lập phiên bản và tương thích

- Thay đổi HTTP/sự kiện/lược đồ không tương thích tạo phiên bản chính mới, chạy song song trong cửa sổ chuyển đổi (`migration`) và có ngày ngừng hỗ trợ được công bố.
- Trường bổ sung là tùy chọn với bên nhận cũ. Không đổi nghĩa enum hoặc tái sử dụng mã; bên nhận phải xử lý enum chưa biết theo phương án dự phòng an toàn.
- Nội dung đã xuất bản, bản sửa đổi việc làm, bản chụp giá/gói, chính sách lời nhắc, sự đồng ý/điều khoản và định nghĩa báo cáo đều lưu phiên bản đã dùng tại thời điểm hành động.
- Chuyển đổi cơ sở dữ liệu theo mở rộng → điền bù/đọc kép nếu cần → chuyển đổi → thu gọn. Chuyển đổi phá hủy không chạy cùng lần triển khai bắt đầu dùng lược đồ mới.

## 10. Quyền sở hữu dữ liệu và tích hợp

### 10.1. Nguồn sự thật

| Dữ liệu | Chủ sở hữu duy nhất | Bên sử dụng và giới hạn |
|---|---|---|
| Email, thông tin xác thực, xác minh, phiên làm việc, MFA, tài khoản/vai trò toàn cục | Cơ sở dữ liệu Danh tính nền tảng | Study/Work nhận claim và bản sao chiếu tối thiểu; không giữ thông tin xác thực. |
| Hồ sơ người học, làm quen, phiên bản lộ trình/khóa học, đăng ký học, tiến độ, bài đánh giá, hoàn thành, minh chứng | Cơ sở dữ liệu Study | Work chỉ nhận bản chụp minh chứng được chọn; Trường đại học không đọc trực tiếp. |
| Hồ sơ nghề nghiệp, CV, hồ sơ năng lực, doanh nghiệp/trường đại học, việc làm, hồ sơ ứng tuyển, phỏng vấn, trò chuyện | Cơ sở dữ liệu Work | Study không đọc ATS; Trường đại học chỉ đọc dữ liệu Work qua chính sách/sự đồng ý trong cùng miền Work. |
| Đơn hàng/giao dịch/webhook thanh toán, quyền lợi sử dụng, khuyến mại | Cơ sở dữ liệu Work/mô-đun Thanh toán | Danh tính nền tảng không sở hữu thanh toán; nhà cung cấp chỉ thấy các trường hợp đồng cần thiết. |
| Mã kỹ năng toàn cục | Hợp đồng hệ phân loại có phiên bản | Study và Work lưu bản sao chiếu theo `skillCode`; nhãn có thể địa phương hóa. |
| Tệp nhị phân | Không gian tên riêng của phân hệ tạo tệp | Siêu dữ liệu/ACL nằm trong cùng phân hệ; xuất minh chứng không chuyển bài làm gốc. |
| Kiểm toán/thông báo/hộp gửi | Mỗi dịch vụ triển khai tự sở hữu | Không dịch vụ nào ghi trực tiếp kiểm toán/thông báo của dịch vụ khác. |

### 10.2. Hợp đồng tích hợp

- Danh tính nền tảng phát sự kiện đăng ký/xác minh/trạng thái/vai trò/xóa. Study và Work cập nhật hoặc chèn bản sao chiếu theo `platformUserId` và phiên bản tổng thể; yêu cầu đầu tiên có thể gọi đối soát nội bộ nếu bản sao chiếu chưa tồn tại.
- Study phát sự kiện minh chứng được phát hành/thu hồi và phục vụ xuất theo yêu cầu cụ thể. Work không đăng ký để xây kho minh chứng toàn cục; chỉ hồ sơ ứng tuyển có minh chứng được chọn mới tạo bản chụp.
- Sự kiện có `eventId`, `eventType`, `schemaVersion`, `occurredAt`, `aggregateId`, `aggregateVersion`, `traceId` và dữ liệu đầu vào tối thiểu; sự kiện được ký ES256/JWS bằng khóa quay vòng có `kid`.
- Yêu cầu nội bộ dùng JWT dịch vụ ES256 có `aud`, phạm vi, `jti`, TTL tối đa 5 phút; bản băm thân yêu cầu/ID yêu cầu chống phát lại. Môi trường thực tế dùng TLS và danh sách cho phép mạng; bí mật/khóa nằm trong trình quản lý bí mật, không nằm trong cơ sở dữ liệu hay kho mã.
- Bên sử dụng ghi bản ghi hộp nhận/chuyển phát trước tác dụng phụ, bỏ bản trùng, phát hiện khoảng trống và thử lại/bắt kịp bằng con trỏ. Không xác nhận tin nhắn trước khi giao dịch cục bộ được xác nhận.
- Không thực hiện giao dịch phân tán. Giao dịch hướng người dùng xác nhận dữ liệu của chủ sở hữu cộng với hộp gửi; tác dụng phụ bất đồng bộ thể hiện trạng thái rõ ràng cho giao diện.

### 10.3. Hành vi khi phụ thuộc lỗi

| Phụ thuộc lỗi | Hành vi bắt buộc |
|---|---|
| JWKS Danh tính nền tảng tạm lỗi | Dùng khóa trong bộ nhớ đệm còn hiệu lực trong thời gian quay vòng cho phép; không bỏ qua chữ ký. Khi không xác minh được thì đóng an toàn. |
| Bản sao chiếu Danh tính nền tảng chậm | API nhạy cảm đóng an toàn hoặc đối soát nội bộ; danh mục công khai vẫn hoạt động. |
| Study lỗi khi ứng tuyển | Hồ sơ ứng tuyển vẫn được tạo với minh chứng `PENDING`; tiến trình nền thử lại, rồi `UNAVAILABLE` nếu hết cửa sổ. ATS thủ công vẫn dùng được. |
| Redis/hàng đợi lỗi | Nguồn sự thật PostgreSQL vẫn xác nhận cùng hộp gửi; tiến trình nền bắt kịp sau khôi phục. Tính năng thời gian thực/bộ nhớ đệm suy giảm, không ghi mất dữ liệu. |
| Kho đối tượng/ClamAV lỗi | Tải lên/quét ở trạng thái chờ/thất bại; không được nộp hoặc tải tệp chưa sạch. Các loại bài đánh giá khác vẫn hoạt động. |
| Nhà cung cấp thanh toán hết thời gian chờ | Đơn hàng ở `PENDING`; không cấp quyền lợi sử dụng; truy vấn/đối soát xác nhận sau. Máy khách không tự thử lại tạo đơn hàng khác nếu tính bất biến theo yêu cầu còn hiệu lực. |
| AI/Ollama lỗi | Tác vụ thất bại/thử lại; CV/JD/ATS thủ công vẫn dùng được và tín dụng không bị tiêu hai lần. |
| WebSocket lỗi | Máy khách dùng lịch sử/con trỏ REST và kết nối lại; gửi tin nhắn chỉ báo thành công sau khi máy chủ xác nhận/lưu bền vững. |

## 11. Bảo mật, quyền riêng tư, lưu giữ, thanh toán và quản trị AI

### 11.1. Mức cơ sở về bảo mật

- Chính sách mật khẩu tối thiểu 12 ký tự, tối đa 128 ký tự, cho phép trình quản lý mật khẩu/cụm mật khẩu và kiểm tra danh sách mật khẩu phổ biến/bị lộ; không ép đổi định kỳ nếu không có sự cố.
- Mức cơ sở Argon2id: bộ nhớ 64 MiB, chi phí thời gian 3, song song 1; đo chuẩn lại theo hạ tầng và băm lại khi chính sách tăng. Mật khẩu/mã thông báo thô không được ghi nhật ký, lưu bộ nhớ đệm hoặc gửi sự kiện.
- Mã làm mới đặt trong cookie `Secure`, `HttpOnly`, `SameSite=Lax`, phạm vi Danh tính nền tảng; mã truy cập chỉ giữ trong bộ nhớ. Thay đổi cookie kiểm tra `Origin` đáng tin cậy và mã CSRF. CORS là danh sách cho phép, không dùng ký tự đại diện với thông tin xác thực.
- Bí mật TOTP được mã hóa bằng khóa ngoài cơ sở dữ liệu; mã khôi phục lưu bản băm. Đăng ký/thử thách MFA, giới hạn tần suất và kiểm toán độc lập, đồng thời yêu cầu xác thực gần đây cho thao tác nhạy cảm.
- Cách ly không gian dữ liệu được kiểm bằng ngữ cảnh tư cách thành viên tại lớp dịch vụ/kho truy cập dữ liệu và ràng buộc ghép. Kiểm thử IDOR xuyên không gian dữ liệu là bắt buộc cho mọi tài nguyên không gian dữ liệu.
- Dữ liệu văn bản có định dạng được làm sạch theo danh sách cho phép; CSP chặn kịch bản nội dòng; URL người dùng nhập được chuẩn hóa/thoát ký tự. Dịch vụ phía máy chủ không hiển thị HTML thô từ CV/JD/trò chuyện.
- Tải lên đi vào vùng cách ly, kiểm tra kích thước/MIME thực/tổng kiểm/đuôi tệp, quét ClamAV rồi mới chuyển vào không gian tên sạch riêng tư. Tải xuống luôn ủy quyền lại và dùng URL có chữ ký ngắn hạn.
- Giới hạn tần suất, phát hiện bất thường và kiểm toán áp dụng cho xác thực, tìm kiếm ứng viên, xuất dữ liệu, trò chuyện, thanh toán, AI và quản trị. Bí mật, khóa ký và thông tin xác thực nhà cung cấp quay vòng qua trình quản lý bí mật.
- Quét phụ thuộc/container, SAST, rà soát chuyển đổi và kiểm thử bảo mật là cổng phát hành. Lỗ hổng nghiêm trọng phải có biện pháp khắc phục hoặc chặn phát hành.

### 11.2. Quyền riêng tư và sự đồng ý

- Thu thập dữ liệu tối thiểu theo mục đích; biểu mẫu ghi rõ trường bắt buộc/tùy chọn. Phân tích không nhận CV/trò chuyện/minh chứng/thông tin liên hệ thô.
- Sự đồng ý tìm kiếm ứng viên, sự đồng ý xuất minh chứng, sự đồng ý dữ liệu trường đại học, sự đồng ý dữ liệu đầu vào AI và tùy chọn tiếp thị là các bản ghi riêng; không gộp thành một ô chọn chung.
- Sự đồng ý lưu chủ thể, bên kiểm soát/không gian dữ liệu, mục đích, phạm vi/ID tài nguyên, phiên bản chính sách, thời điểm cấp/hết hạn/thu hồi và tác nhân. Thu hồi ảnh hưởng truy cập tương lai nhưng không sửa kiểm toán hợp pháp.
- Nhà tuyển dụng chỉ thấy bản chụp của hồ sơ ứng tuyển thuộc không gian dữ liệu của mình và đúng phạm vi vai trò; tìm kiếm ứng viên không phải đường tắt để xem CV/thông tin liên hệ/minh chứng.
- Báo cáo trường đại học áp ngưỡng 10 sau mọi bộ lọc; không trả tổng phụ/tổng có thể trừ để suy ra nhóm nhỏ.
- Xuất/xóa dữ liệu quyền riêng tư chạy bất đồng bộ, có xác thực lại danh tính, thông báo hoàn tất và liên kết tải xuống có chữ ký ngắn hạn.

### 11.3. Thời hạn lưu giữ mặc định

| Loại dữ liệu | Thời hạn | Xử lý hết hạn |
|---|---|---|
| Tài liệu xác minh của doanh nghiệp/trường đại học | 180 ngày sau quyết định cuối | Xóa tệp, giữ siêu dữ liệu quyết định/kiểm toán đã che. |
| Thông báo và chi tiết chuyển phát | 180 ngày | Xóa cứng dữ liệu đầu vào; giữ đối tượng tổng hợp không PII. |
| Sự kiện phân tích học tập/hoạt động/tìm kiếm | 13 tháng | Xóa hoặc tổng hợp/ẩn danh; tiến độ/hoàn thành còn hiệu lực được giữ theo tài khoản. |
| Hồ sơ ứng tuyển, trò chuyện và bản chụp minh chứng | 12 tháng sau khi hồ sơ ứng tuyển kết thúc | Xóa/che PII và tệp nếu không bị tạm giữ pháp lý; giữ đối tượng tổng hợp/kiểm toán tối thiểu. |
| Kiểm toán bảo mật, ủy quyền, quản trị, ATS, duyệt AI của Danh tính nền tảng | Tối thiểu 24 tháng | Xóa/che theo chính sách và tạm giữ pháp lý. |
| Đơn hàng, giao dịch, webhook, sổ cái/hoàn tiền/tranh chấp thanh toán ngược | Tối thiểu 24 tháng hoặc lâu hơn theo chính sách tài chính hiện hành | Giữ bản ghi tài chính cần thiết, mã hóa/che dữ liệu đầu vào dư thừa. |
| Dữ liệu đầu vào/đầu ra AI thô kỹ thuật | 30 ngày | Xóa dữ liệu đầu vào suy luận thô; nội dung đã chấp nhận theo miền chủ sở hữu, kiểm toán/bản băm/phiên bản mô hình giữ 24 tháng. |
| Tài khoản chưa xác minh | 30 ngày từ đăng ký nếu không hoạt động | Xóa tài khoản/mã thông báo/chuyển phát theo lô có kiểm toán tổng hợp. |
| Mã dùng một lần và phiên làm việc hết hạn/thu hồi | Mã: 30 ngày; phiên: 90 ngày | Xóa cứng bản băm/chi tiết thiết bị không còn cần điều tra. |
| Tệp tải lên mồ côi | 24 giờ | Xóa đối tượng/siêu dữ liệu; vùng cách ly tệp nhiễm giữ tối đa 30 ngày để điều tra rồi xóa. |
| Hộp gửi/hộp nhận đã chuyển phát | 30 ngày; thất bại/DLQ 90 ngày | Xóa dữ liệu đầu vào sau khi bảo đảm không cần phát lại; giữ chỉ số. |
| Sao lưu | Tối đa 35 ngày | Tự hết hạn; khôi phục phải áp sổ cái xóa/thu hồi. |
| Thời gian ân hạn xóa tài khoản | 30 ngày | Sau thời gian ân hạn thực hiện `BR-OPS-006`; tạm giữ pháp lý chỉ giữ đúng phạm vi. |

Thời hạn lưu giữ tính từ thời điểm điều kiện bắt đầu, chạy bằng tiến trình có điểm kiểm soát, báo cáo số lượng và cảnh báo lỗi. Chính sách tài chính/pháp lý có thể kéo dài một bản ghi cụ thể qua tạm giữ pháp lý; không được dùng lý do đó để giữ toàn bộ dữ liệu ngoài phạm vi.

### 11.4. Quản trị thanh toán

- Bộ điều hợp VNPAY dựa trên [tài liệu thanh toán chính thức của VNPAY](https://sandbox.vnpayment.vn/apis/docs/thanh-toan-pay/pay.html); bộ điều hợp MoMo dựa trên [tài liệu thanh toán một lần chính thức của MoMo](https://developers.momo.vn/v3/docs/payment/api/credit/onetime/). Mỗi bộ điều hợp cô lập cách ký, mã kết quả, truy vấn và hoàn tiền nhưng ánh xạ về trạng thái/lỗi thanh toán chuẩn.
- Thông tin xác thực bên bán tách môi trường thử nghiệm/thực tế. Phản hồi gọi lại xác thực chữ ký trên dữ liệu đầu vào chuẩn thô trước khi phân tích nghiệp vụ; số tiền, đơn hàng, bên bán, đơn vị tiền tệ và ID giao dịch phải khớp.
- Giao dịch nhà cung cấp có ràng buộc duy nhất theo nhà cung cấp + ID giao dịch nhà cung cấp; phản hồi gọi lại thô được mã hóa, bất biến và loại bỏ bí mật. Chỉ xác nhận đúng hợp đồng sau khi đã lưu bền vững/đưa vào xử lý bền vững.
- Danh mục gói định nghĩa loại quyền lợi sử dụng, số lượng, hạn dùng và phiên bản chính sách hoàn tiền. Mua không đồng nghĩa có tiền trong ví; quyền lợi sử dụng chỉ áp dụng cho đúng sản phẩm/không gian dữ liệu đã mua.
- Vận hành tài chính áp dụng phân tách người lập/người duyệt cho hoàn tiền ngoại lệ hoặc điều chỉnh nợ; người khởi tạo không tự duyệt cùng vụ việc. Báo cáo đối soát phân biệt thiếu ở nhà cung cấp, thiếu cục bộ, sai số tiền và sai trạng thái.

### 11.5. Quản trị AI

- Danh mục chỉ cho phép mô hình/chính sách lời nhắc đã duyệt. Mẫu lời nhắc tách chỉ dẫn khỏi dữ liệu người dùng, dữ liệu đầu ra JSON theo lược đồ và lưu tổng kiểm/phiên bản để tái kiểm toán.
- Màn hình cho biết tính năng nào dùng AI, dữ liệu nào được gửi, tín dụng dự kiến và cách từ chối. Không dùng dữ liệu đầu vào/đầu ra của người dùng để huấn luyện nhà cung cấp nếu chưa có sự đồng ý riêng.
- Giải thích mức độ phù hợp phải nêu dữ kiện việc làm/hồ sơ tạo ra gợi ý, mức thiếu dữ liệu và giới hạn; không trình bày điểm như xác suất được tuyển.
- Đề xuất danh sách rút gọn là một chế độ xem phụ; danh sách nhà tuyển dụng mặc định vẫn có thể xem không qua AI. Chấp nhận đề xuất chỉ ghi hành động duyệt, nhà tuyển dụng vẫn phải chọn chuyển trạng thái ATS.
- Đánh giá trước phát hành gồm tính đúng theo lược đồ, mức độ bám nguồn, khả năng chống chèn lời nhắc, nội dung độc hại và chênh lệch kết quả giữa các nhóm kiểm thử đại diện. Bản phát hành thăm dò có công tắc ngắt và theo dõi chấp nhận/lỗi/ghi đè, không theo dõi thuộc tính nhạy cảm ở môi trường thực tế.
- Tín hiệu tài trợ/thanh toán bị loại khỏi dữ liệu đầu vào ghép nối. Nhà cung cấp AI không được gọi API Work/Study, không giữ thông tin xác thực dịch vụ và không phát sự kiện miền.

## 12. NFR, SLO và vận hành

| ID | Yêu cầu đo được |
|---|---|
| **NFR-OPS-001** | Hệ thống thử nghiệm hỗ trợ 5.000 tài khoản, 500 DAU và 50 RPS đỉnh trong 15 phút mà không vượt 80% nhóm kết nối/CPU kéo dài hoặc mất yêu cầu đã được xác nhận. |
| **NFR-OPS-002** | Mức sẵn sàng theo tháng của lõi Danh tính nền tảng, Study và Work đạt ít nhất 99,0%; phụ thuộc ngoài được đo riêng nhưng hệ thống phải thể hiện trạng thái suy giảm an toàn. |
| **NFR-OPS-003** | Độ trễ máy chủ p95: đọc đồng bộ ≤ 800 ms, thay đổi đồng bộ ≤ 1,5 giây; không tính phần việc đã công bố bất đồng bộ. Truy vấn báo cáo lớn bắt buộc bất đồng bộ/xuất dữ liệu. |
| **NFR-OPS-004** | Máy chủ trò chuyện xác nhận sau khi lưu bền vững p95 ≤ 2 giây; kết nối lại/lịch sử không mất hoặc nhân đôi tin nhắn theo khóa máy khách. |
| **NFR-OPS-005** | RPO toàn bộ PostgreSQL ≤ 15 phút; RTO cho lõi Danh tính nền tảng/Study/Work ≤ 4 giờ. Diễn tập khôi phục thực hiện ít nhất mỗi quý trong đợt thử nghiệm. |
| **NFR-OPS-006** | Bản sao chiếu hộp gửi/sự kiện p95 ≤ 60 giây khi bình thường; xuất minh chứng p95 ≤ 2 phút. Hàng tồn, tuổi lâu nhất, thử lại và DLQ có cảnh báo. |
| **NFR-OPS-007** | Việc tắt cho phép tìm kiếm ứng viên được kiểm tra đầu cuối và đáp ứng giới hạn cứng 5 phút, gồm bản sao chiếu cơ sở dữ liệu, chỉ mục, bộ nhớ đệm và phản hồi tìm kiếm đang hoạt động. |
| **NFR-OPS-008** | Quét tệp p95 ≤ 2 phút cho tệp trong giới hạn V1 khi bộ quét hoạt động bình thường; chờ/thất bại luôn đóng an toàn, có trạng thái và thử lại rõ ràng. |
| **NFR-OPS-009** | Mọi yêu cầu có ID vết; thay đổi quan trọng liên kết kiểm toán/hộp gửi/giao dịch nhà cung cấp. Nhật ký JSON có mức độ, dịch vụ, môi trường và không chứa dữ liệu đầu vào bí mật/PII. |
| **NFR-OPS-010** | Web đạt WCAG 2.2 AA cho luồng chính: bàn phím, tiêu điểm, nhãn, tương phản, thông báo lỗi và giảm chuyển động; thích ứng từ 360 px, hỗ trợ hai phiên bản chính mới nhất của Chrome, Edge, Firefox, Safari. |
| **NFR-OPS-011** | API/sự kiện/chuyển đổi cơ sở dữ liệu và tài liệu phải vượt qua bộ kiểm hợp đồng/truy vết; không phát hành khi có tham chiếu mất, phương thức+đường dẫn trùng hoặc enum/trạng thái mâu thuẫn. |
| **NFR-OPS-012** | Sao lưu được mã hóa, kiểm tra khôi phục; bí mật quay vòng; phát hiện bảo mật mức cao/nghiêm trọng, rò rỉ xuyên không gian dữ liệu hoặc lỗi toàn vẹn thanh toán là điều kiện chặn phát hành. |

### 12.1. Chỉ số và cảnh báo tối thiểu

- Danh tính nền tảng: đăng nhập thành công/thất bại/khóa, chuyển phát xác minh, dùng lại mã làm mới, lỗi MFA, phiên làm việc bị thu hồi và lỗi JWKS.
- Study: xung đột đăng ký học/chuyển lộ trình, trễ tiến độ, tuổi hàng đợi bài đánh giá, trạng thái quét tệp, lỗi xuất bản, trễ hộp gửi minh chứng.
- Work: trễ tắt cho phép tìm kiếm, xung đột chuyển trạng thái việc làm/hồ sơ ứng tuyển, tỷ lệ ứng tuyển, trạng thái xuất minh chứng, xác nhận phỏng vấn/trò chuyện và từ chối xuyên không gian dữ liệu.
- Thanh toán: phễu đơn hàng theo nhà cung cấp, lỗi chữ ký webhook, trễ hoàn tất, trùng/sai lệch, phát hành quyền lợi, hoàn tiền/tranh chấp thanh toán ngược và chênh lệch đối soát.
- AI: tuổi hàng đợi, độ trễ, lỗi lược đồ/an toàn, thử lại, người dùng chấp nhận/sửa/từ chối và trạng thái công tắc ngắt; không ghi nội dung nhạy cảm vào nhãn chỉ số.
- Cảnh báo P1: bỏ qua xác thực/chữ ký, rò rỉ xuyên không gian dữ liệu/PII, thanh toán cấp trùng/sai số tiền, mất dữ liệu đã xác nhận, nguy cơ vi phạm RPO/RTO. P2: độ trễ/mức sẵn sàng SLO, hàng tồn/DLQ, quét tệp/tắt cho phép tìm kiếm vượt ngưỡng.

## 13. Phát hành V1-PILOT

### 13.1. Thứ tự phát hành

1. **Nền tảng:** khóa OpenAPI/sự kiện/enum, dựng ba cơ sở dữ liệu, Danh tính nền tảng/JWKS, cơ chế bảo vệ không gian dữ liệu, hộp gửi/hộp nhận, kiểm toán, quan sát, sao lưu/khôi phục và cổng chất lượng CI.
2. **Lõi Study:** danh mục khóa độc lập, làm quen/lộ trình chính, lập phiên bản nội dung, tiến độ, bài đánh giá/quét tệp, phát hành minh chứng và vận hành Study.
3. **Lõi Work:** hồ sơ nghề nghiệp/CV, doanh nghiệp/việc làm, chủ động cho phép tìm kiếm/tìm kiếm ứng viên, ứng tuyển/ATS/xuất minh chứng, phỏng vấn/trò chuyện và kiểm duyệt.
4. **Trường đại học + Thanh toán:** không gian dữ liệu trường đại học/sự đồng ý/ngưỡng báo cáo, gói/đơn hàng, môi trường thử nghiệm rồi môi trường thực tế VNPAY/MoMo, quyền lợi sử dụng/khuyến mại và đối soát.
5. **AI + tài trợ:** AI chạy ngầm/đánh giá, CV/JD do con người duyệt, giải thích mức độ phù hợp/đề xuất danh sách rút gọn, vị trí tài trợ có nhãn; mở dần bằng danh sách cho phép quyền lợi sử dụng/không gian dữ liệu.

Mỗi giai đoạn chỉ mở khi hoàn tác/chuyển tiếp của `migration`, kiểm thử kiểm soát truy cập, kiểm toán, bảng điều khiển/cảnh báo, sổ tay vận hành và kiểm thử chấp nhận liên quan đều đạt. Cờ tính năng có chủ sở hữu, hạn dùng và trạng thái mặc định tắt cho thanh toán thực tế, AI và vị trí tài trợ.

### 13.2. Thử nghiệm và chuyển đổi dữ liệu cũ

- Thử nghiệm mở theo danh sách cho phép nhóm khóa/không gian dữ liệu, tăng 10% → 25% → 50% → 100% sau ít nhất một cửa sổ quan sát SLO cho mỗi mức; P1 hoặc lỗi toàn vẹn lập tức dừng tăng và tắt tính năng liên quan.
- Bản mẫu Express/EJS/MySQL của Work và lược đồ BD cũ chỉ là nguồn tham khảo dữ liệu, không phải kiến trúc mục tiêu. Không nhập mật khẩu thô/bản băm không đạt chuẩn; tài khoản phải xác minh lại email và đặt mật khẩu mới trong Danh tính nền tảng.
- Nếu có dữ liệu thật được phê duyệt, việc nhập chạy qua môi trường dàn dựng, có ánh xạ ID hệ thống cũ riêng, đối soát tổng kiểm/số lượng, chạy thử và báo cáo bản ghi lỗi. Dữ liệu không gian dữ liệu/hồ sơ ứng tuyển không đủ quyền sở hữu/sự đồng ý bị cách ly, không tự công khai.
- Nội dung cũ đã xuất bản phải được đóng thành phiên bản bất biến trước khi đăng ký học mới. Tiến độ/hoàn thành nhập chỉ được nhận khi ánh xạ chắc chắn tới phiên bản chính xác; trường hợp không xác định giữ lịch sử tham khảo nhưng không cấp hoàn thành/minh chứng.
- Thanh toán thực tế chỉ mở sau kiểm thử chữ ký phản hồi gọi lại, kiểm thử trùng/không theo thứ tự, đối soát môi trường thử nghiệm và sổ tay vận hành Tài chính. AI chỉ mở sau đánh giá/phát hành thăm dò và có công tắc ngắt đã diễn tập.

### 13.3. Hoàn tác và xử lý sự cố

- Triển khai ứng dụng tương thích ngược trước chuyển đổi; hoàn tác mã không hoàn tác dữ liệu bằng lệnh phá hủy. Sửa trạng thái dùng hành động bù trừ có kiểm toán.
- Có thể tắt riêng chỉ mục ứng viên, tiến trình nền xuất minh chứng, WebSocket, nhà cung cấp thanh toán, vị trí tài trợ hoặc AI mà việc học Study/ATS thủ công Work vẫn hoạt động.
- Khi có sự cố toàn vẹn/quyền riêng tư: cô lập tính năng, giữ minh chứng/kiểm toán, thu hồi khóa/mã thông báo nếu cần, xác định không gian dữ liệu/người dùng bị ảnh hưởng, sửa bằng phát lại/bù trừ bất biến theo yêu cầu và ghi hành động sau sự cố.

## 14. Kiểm thử chấp nhận bắt buộc

Mỗi ID kiểm thử dưới đây là một bộ kiểm thử. Bộ kiểm thử phải có dữ liệu chuẩn bị, luồng thành công, luồng thay thế/thất bại, kiểm tra bản ghi/kiểm toán/hộp gửi và khẳng định không phát sinh tác dụng phụ ngoài dự kiến. Kiểm thử hợp đồng API, ràng buộc cơ sở dữ liệu và trạng thái giao diện cùng dùng một ID kiểm thử để truy vết.

### 14.1. Danh tính và Study

| ID | Kịch bản phải đạt |
|---|---|
| **TC-IAM-001** | Đăng ký mới tạo người dùng chờ xác minh/bản băm/mã thông báo/hộp gửi đúng một lần; phát lại cùng khóa trả cùng kết quả; email trùng/phản hồi chung, mật khẩu yếu, thỏa thuận cũ, mã thông báo sai/hết hạn/đã dùng không làm lộ tài khoản hoặc tạo phiên làm việc; xác minh hợp lệ chuyển sang `ACTIVE`. |
| **TC-IAM-002** | Đăng nhập đúng/sai/bị khóa/tạm ngưng/chưa xác minh; người dùng đặc quyền bắt buộc TOTP; xoay mã làm mới thành công; hai lần làm mới đồng thời chỉ một thành công và lần dùng lại thu hồi họ phiên; đăng xuất/đăng xuất tất cả, đặt lại mật khẩu, quay vòng khóa và mã thông báo `authVersion` cũ đều bị chặn đúng. |
| **TC-IAM-003** | Quản trị viên thiếu quyền/MFA, tự tạm ngưng, gỡ quản trị viên cuối cùng hoặc `If-Match` lỗi thời bị chặn; thay đổi tạm ngưng/vai trò hợp lệ thu hồi phiên, phát sự kiện; sự kiện trùng/lỗi thời ở Study/Work không tạo bản sao chiếu sai; kiểm toán đã che và có tác nhân/lý do. |
| **TC-STU-001** | Khách thấy đúng danh mục hiện hành đã xuất bản; người học đã xác minh nhưng chưa làm quen vẫn đăng ký khóa độc lập; hai lượt đăng ký đồng thời/phát lại chỉ có một lượt đăng ký; phiên bản đã lưu trữ/chưa xuất bản bị chặn; lượt đăng ký cũ vẫn mở đúng phiên bản đã thay thế được ghim. |
| **TC-STU-002** | Làm quen lưu/hoàn tất và có phiên bản đề xuất; chọn lộ trình chính khi chưa hoàn tất bị chặn; hai lần chọn/chuyển đồng thời chỉ một `ACTIVE`; trước 168 giờ trả `nextAllowedAt`, đúng/sau mốc thành công; bỏ qua của quản trị viên cần quyền/MFA/lý do và tạo thời gian chờ mới. |
| **TC-STU-003** | Tiến độ khối/bài học đơn điệu khi yêu cầu trùng/không theo thứ tự; máy khách không ghi phần trăm; dựng lại hoàn thành/bản chụp cho cùng kết quả; chuyển lộ trình không mất sự kiện; phiên bản khóa học mới không kế thừa hoàn thành của phiên bản cũ; sửa chính giữ sự kiện gốc và có kiểm toán. |
| **TC-STU-004** | Bài kiểm tra không lộ đáp án trước khi nộp, chấm tự động đúng và lần làm bài được niêm phong; bài văn bản/liên kết/tệp vào duyệt; HTTP/không HTTPS/liên kết quá dài bị chặn và máy chủ không tải; tệp giả MIME/nhiễm/chờ/quét thất bại không được nộp/tải; hai người duyệt đồng thời chỉ một xác nhận, nộp lại tạo lần làm bài mới. |
| **TC-STU-005** | Hoàn thành phát hành minh chứng đúng chủ sở hữu/phiên bản nguồn; phát hành trùng không nhân bản; thu hồi giữ lịch sử; mã thông báo người học sai đối tượng/chủ sở hữu không đọc được; xuất chỉ mục đã chọn, sai phiên bản/bị thu hồi trả lỗi mục an toàn; dữ liệu đầu ra/sự kiện trùng không tạo bản chụp trùng. |
| **TC-STU-006** | Tác giả tạo bản nháp và trình soạn thảo lỗi thời nhận xung đột; thiếu quyền, tài nguyên chưa sạch, vị trí đặt/thang điểm lỗi, nhà xuất bản thiếu quyền/MFA hoặc kiểm tra quá hạn không được xuất bản; hai nhà xuất bản đồng thời chỉ một phiên bản thắng; hoán đổi phiên bản hiện hành nguyên tử, bộ nhớ đệm bị vô hiệu, lượt đăng ký cũ không đổi. |
| **TC-STU-007** | Bắt buộc khử trùng lặp thông báo/con trỏ đã đọc/tùy chọn; cộng đồng chưa chấp nhận/quy tắc hiện hành lỗi thời/không đủ điều kiện không nhận liên kết; báo cáo/hỗ trợ trùng, tệp bẩn và truy cập dữ liệu người khác bị chặn; nhân sự vận hành chỉ xem ghi chú nội bộ đúng quyền; ngoại tuyến/thử lại không tạo phiếu trùng. |
| **TC-STU-008** | Báo cáo tổng hợp đúng định nghĩa/độ mới; ghi đè hỗ trợ/điều chỉnh tiến độ thiếu quyền/MFA/lý do bị chặn; phân tách nhiệm vụ vai trò cục bộ và phiên bản lỗi thời được kiểm; tìm kiếm/xuất kiểm toán đúng phạm vi; tiến trình dựng lại không sửa sự kiện nguồn. |

### 14.2. Work, trường đại học, thanh toán, AI và vận hành

| ID | Kịch bản phải đạt |
|---|---|
| **TC-WRK-001** | Quyền sở hữu/xác thực/chỉnh sửa lỗi thời của hồ sơ/CV/hồ sơ năng lực và tệp riêng tư; xuất bản tạo bản sửa đổi bất biến; bản chụp ứng tuyển không đổi sau khi sửa/xóa nguồn; xuất cao cấp chỉ tiêu quyền lợi một lần và hoàn giữ chỗ khi dựng lỗi. |
| **TC-WRK-002** | Hồ sơ mặc định riêng tư; chủ động cho phép tìm kiếm cần sự đồng ý/xem trước, tìm kiếm không trả thông tin liên hệ/CV/minh chứng/trường nhạy cảm; ID công khai xuyên không gian dữ liệu không dùng được; lời mời không tạo hồ sơ ứng tuyển/trò chuyện; tắt cho phép tìm kiếm ẩn ngay tại điều kiện cơ sở dữ liệu và loại khỏi chỉ mục/bộ nhớ đệm trong ≤5 phút kể cả khi tiến trình nền thử lại. |
| **TC-WRK-003** | Tạo/xác minh doanh nghiệp, tài liệu bẩn, ID thuế trùng, chủ sở hữu tự xác minh, không gian dữ liệu chưa xác minh; mời thành viên/vai trò/chủ sở hữu cuối cùng/phiên bản lỗi thời; mọi IDOR đọc/ghi xuyên không gian dữ liệu trả không tìm thấy/từ chối và không tạo kiểm toán PII sai phạm vi. |
| **TC-WRK-004** | Xác thực bản nháp/bản sửa đổi, duyệt và xuất bản đúng quyền; quyền cấp đáng tin cậy hết hạn/bị thu hồi vẫn bị chặn và không bỏ qua chính sách; hai lượt xuất bản/tạm dừng/tiếp tục/đóng cạnh tranh chỉ một thắng; sửa bản đang xuất bản tạo bản sửa đổi mới, việc làm kết thúc không nhận ứng tuyển mới. |
| **TC-WRK-005** | Hai lượt ứng tuyển/phát lại cho cùng ứng viên/việc làm chỉ tạo một hồ sơ ứng tuyển; bản chụp đúng bản sửa đổi; chuyển ATS hợp lệ/không hợp lệ, hai nhà tuyển dụng cạnh tranh, nhà tuyển dụng không được phân công, từ chối thiếu lý do và tác nhân AI đều bị chặn; rút lui/từ chối đề nghị/tuyển dụng là trạng thái kết thúc; đóng việc làm không tự đóng hồ sơ ứng tuyển. |
| **TC-WRK-006** | Ứng tuyển với 0/nhiều minh chứng được chọn; Study sẵn sàng, hết thời gian chờ, thử lại, mục bị thu hồi/sai phiên bản; hồ sơ ứng tuyển luôn tồn tại và ATS không đổi do lỗi xuất; dữ liệu đầu ra đến sau khi thu hồi sự đồng ý vẫn bị ẩn; sự kiện thu hồi ẩn mọi bản chụp khớp, giữ kiểm toán và không tạo điểm âm. |
| **TC-WRK-007** | Phỏng vấn chỉ cho hồ sơ ứng tuyển/thành viên hợp lệ; UTC/múi giờ/kết thúc trước bắt đầu/người tham gia khác không gian dữ liệu; xác nhận/từ chối/đổi lịch tạo phiên bản, lịch lỗi thời gây xung đột; hủy/vắng mặt trước giờ bị chặn; số thứ tự ICS đúng và thông báo trùng không gửi lặp. |
| **TC-WRK-008** | Chỉ ứng viên/nhà tuyển dụng được phân công mới đăng ký nhận/gửi; một cuộc trò chuyện duy nhất; khóa tin nhắn trùng chỉ lưu bền vững một lần, số thứ tự tăng; kết nối lại từ con trỏ bù khoảng trống; WebSocket lỗi dùng REST; hồ sơ ứng tuyển kết thúc chuyển sang chỉ đọc, đánh dấu xóa trong kiểm duyệt không xóa kiểm toán. |
| **TC-WRK-009** | Mẫu/AI/khuyến mại kiểm quyền lợi và sự đồng ý của ứng viên; việc làm/hồ sơ tài trợ luôn có nhãn/vị trí riêng, điểm tự nhiên không đổi từng bit; mã thông báo lượt nhấp/lần hiển thị giả/trùng bị chặn; tắt cho phép tìm kiếm dừng khuyến mại hồ sơ; hết tín dụng/hết hạn/điều chỉnh hoàn tiền không tạo số dư âm. |
| **TC-WRK-010** | Báo cáo nội dung, duyệt/gỡ bỏ việc làm và kháng nghị đúng phạm vi/phiên bản; gỡ bỏ ẩn khám phá/ứng tuyển mới nhưng giữ hồ sơ ứng tuyển; người kiểm duyệt xuyên không gian dữ liệu chỉ qua quyền nền tảng; bộ lọc báo cáo tổng hợp/quyền riêng tư và xuất kiểm toán không lộ CV/trò chuyện/minh chứng thô. |
| **TC-UNI-001** | Trường đại học trùng/xác minh/vai trò thành viên/chủ sở hữu cuối cùng; liên kết chỉ `ACTIVE` sau khi ứng viên chấp nhận, lời mời sai người/hết hạn bị chặn; nhóm khóa chỉ nhận liên kết `ACTIVE`, cập nhật tư cách thành viên lỗi thời gây xung đột; tư cách thành viên doanh nghiệp không cấp quyền trường đại học. |
| **TC-UNI-002** | Xác thực phạm vi/ngày của chương trình/đối tác; hợp tác phải được hai bên chấp nhận; phân phối trong trường chỉ dùng việc làm đã xuất bản và không tự ứng tuyển; giới thiệu cần sự đồng ý `JOB_REFERRAL`, chỉ gửi thông báo/liên kết ứng tuyển, không mở trò chuyện/minh chứng. |
| **TC-UNI-003** | Mục đích/hết hạn/thu hồi sự đồng ý chặn ngay chế độ xem cá nhân; báo cáo theo từng bộ lọc có nhóm 9 bị ẩn, nhóm 10 được tổng hợp; tổng phụ không suy ra nhóm nhỏ; trường đại học không đọc CV/trò chuyện/minh chứng; dữ liệu tổng hợp đã ẩn danh hợp lệ còn sau khi liên kết kết thúc. |
| **TC-PAY-001** | Giá/bản chụp đơn hàng do máy chủ tính bằng số nguyên VND; quyền người mua/không gian dữ liệu, giá lỗi thời, nhà cung cấp hết thời gian chờ, thử lại và tính bất biến theo yêu cầu; URL trả về giả thành công không hoàn tất/cấp quyền; yêu cầu môi trường thử nghiệm VNPAY/MoMo ký đúng và không ghi thông tin xác thực. |
| **TC-PAY-002** | Chữ ký sai, sai lệch bên bán/đơn hàng/số tiền/đơn vị tiền tệ, phản hồi gọi lại thành công trùng/không theo thứ tự/trước phản hồi tạo; chỉ thanh toán hoàn tất đã xác minh tạo một sổ cái và một quyền lợi; lỗi đến muộn không hạ `SETTLED`; tiến trình nền/DLQ/đối soát khôi phục mà không cấp trùng. |
| **TC-PAY-003** | Hoàn tiền vượt số tiền/đã tiêu, người yêu cầu tự duyệt, duyệt lỗi thời và nhà cung cấp thất bại; hoàn tiền một phần/toàn bộ điều chỉnh phần chưa tiêu; tranh chấp thanh toán ngược đóng băng phần còn lại/vụ việc rủi ro; đối soát hằng ngày phát hiện thiếu/sai lệch ở cục bộ/nhà cung cấp; sổ cái/webhook thô không sửa được. |
| **TC-AIX-001** | AI CV/JD chỉ nhận dữ liệu đầu vào trong danh sách cho phép, chèn lời nhắc/lỗi lược đồ/dữ liệu đầu ra độc hại bị chặn; hết thời gian chờ/thử lại không trừ tín dụng lặp; dữ liệu đầu ra là bản nháp có nguồn gốc; chấp nhận/sửa/từ chối cần hành động của con người và không tự sửa CV/JD đã xuất bản. |
| **TC-AIX-002** | Ghép nối/danh sách rút gọn loại mọi trường được bảo vệ/liên hệ/thanh toán/tài trợ/minh chứng chưa đồng ý; việc làm/hồ sơ ứng tuyển khác không gian dữ liệu bị chặn; đề xuất có giải thích/độ không chắc chắn; chấp nhận đề xuất không đổi ATS; AI lỗi/bị vô hiệu vẫn dùng ATS thủ công. |
| **TC-AIX-003** | Mô hình/lời nhắc thiếu loại trừ/ngưỡng đánh giá không được `ACTIVE`; bản phát hành thăm dò và công tắc ngắt dừng tác vụ đang hàng đợi/mới, hoàn giữ chỗ; vai trò/MFA/xác thực tăng cường và cấu hình lỗi thời; hoàn tác dùng phiên bản cũ cho tác vụ mới nhưng không sửa nguồn gốc/dữ liệu đầu ra lịch sử. |
| **TC-OPS-001** | Kiểm duyệt/việc làm/xác minh/quyền cấp đáng tin cậy kiểm phân tách người lập/người duyệt, tự duyệt và phạm vi không gian dữ liệu; truy cập khẩn cấp cần phiếu/người duyệt hoặc SEV-1, hết hạn ≤60 phút; mọi truy cập/hành động được cảnh báo/kiểm toán, không biến thành vai trò vĩnh viễn. |
| **TC-OPS-002** | Xuất dữ liệu cần xác thực lại và chỉ gồm dữ liệu chủ sở hữu; yêu cầu/hủy xóa/thời gian ân hạn/tạm giữ pháp lý; sau 30 ngày PII/tệp/liên kết được xử lý đúng chủ sở hữu, minh chứng/sự đồng ý bị thu hồi; khôi phục sao lưu áp sổ cái xóa; tạm giữ pháp lý hết hạn tiếp tục xóa đúng phạm vi. |
| **TC-OPS-003** | Tải 50 RPS/500 DAU đạt độ trễ/nhóm kết nối; ngắt Redis/tiến trình nền/nhà cung cấp/AI/kết nối WebSocket và khôi phục bằng hộp gửi/thử lại/DLQ không mất dữ liệu; khôi phục sao lưu đạt RPO 15 phút/RTO 4 giờ; vết/kiểm toán liên kết; cảnh báo P1/P2 phát đúng. |

### 14.3. Điều kiện hoàn tất

- 100% `UC-*` có ít nhất một `TC-*`, API/bảng/màn hình và biểu đồ hoặc lý do không cần biểu đồ động.
- Kiểm thử đồng thời chạy với giao dịch thật; không thay bằng kho truy cập dữ liệu giả. Bộ kiểm thử bảo mật bao gồm IDOR xuyên không gian dữ liệu, leo thang đặc quyền, tài khoản tạm ngưng, phát lại mã thông báo, URL có chữ ký hết hạn, giả MIME/mã độc, XSS/SSRF và chèn lời nhắc.
- Bộ kiểm thử lỗi chủ động ngắt Danh tính nền tảng, Study, Redis, hàng đợi, kho đối tượng/bộ quét, nhà cung cấp thanh toán, Ollama và WebSocket; dữ liệu đã xác nhận phải còn khôi phục được.
- Bộ kiểm thử hiệu năng dùng dữ liệu gần quy mô thử nghiệm và báo p50/p95/p99, tỷ lệ lỗi, nhóm kết nối/khóa cơ sở dữ liệu, trễ hàng đợi; đạt toàn bộ `NFR-OPS-*`.
- Nghiệm thu chỉ đạt khi bộ kiểm Markdown/Mermaid/truy vết, kiểm thử hợp đồng, kiểm tra migration và tất cả ID kiểm thử liên quan đều đạt; mọi ngoại lệ có chủ sở hữu, hạn dùng và chấp nhận rủi ro được phê duyệt.

## 15. Ma trận truy vết tổng

Ký hiệu `A–B` là dải ID liên tục, bao gồm cả hai đầu; các ID trong dải phải tồn tại tại tài liệu sở hữu. Cột “Quy tắc/quyền/NFR” nêu quy tắc chi phối chính, không thay thế toàn bộ quy tắc dùng chung. `N/A` chỉ được dùng kèm lý do cụ thể.

| Năng lực / Trường hợp sử dụng | Quy tắc, quyền, NFR chính | Hoạt động / Trình tự | Lớp / bảng nguồn sự thật | API / sự kiện chính | Màn hình chính | Kiểm thử |
|---|---|---|---|---|---|---|
| `CAP-IAM-001` / `UC-IAM-001` | `BR-IAM-001`, `BR-IAM-002`, `BR-IAM-008`, `NFR-OPS-003` | `AC-IAM-001`, `SEQ-IAM-001` | `CLS-IAM-001`; `TBL-IAM-001–005`, `TBL-IAM-018` | `API-IAM-001–003`, `EVT-IAM-001` | `SCR-IAM-001–002` | `TC-IAM-001` |
| `CAP-IAM-002` / `UC-IAM-002` | `BR-IAM-003–007`, `NFR-OPS-002`, `NFR-OPS-012` | `AC-IAM-001`, `SEQ-IAM-001–002` | `CLS-IAM-001`; `TBL-IAM-003`, `TBL-IAM-006–010`, `TBL-IAM-017–018` | `API-IAM-004–020`, `API-IAM-024`, `EVT-IAM-002` | `SCR-IAM-003–006` | `TC-IAM-002` |
| `CAP-IAM-003` / `UC-IAM-003` | `PERM-IAM-001–004`, `BR-IAM-005–007`, `BR-OPS-001–002` | `AC-IAM-001`, `SEQ-IAM-002` | `CLS-IAM-001`; `TBL-IAM-012–018` | `API-IAM-021–023`, `EVT-IAM-002–004` | `SCR-OPS-001–002`, `SCR-OPS-024` | `TC-IAM-003` |
| `CAP-STU-001` / `UC-STU-001` | `BR-STU-001`, `BR-STU-007–009`, `NFR-OPS-003` | `AC-STU-001`, `SEQ-STU-001` | `CLS-STU-001–002`; `TBL-STU-009–016`, `TBL-STU-027` | `API-STU-001–006`, `API-STU-016–019`, `EVT-STU-001` | `SCR-STU-002–006`, `SCR-STU-014–016` | `TC-STU-001` |
| `CAP-STU-002` / `UC-STU-002` | `BR-STU-002–006`, `PERM-STU-009`, `BR-OPS-010` | `AC-STU-001`, `SEQ-STU-001` | `CLS-STU-001–002`; `TBL-STU-002`, `TBL-STU-007–010`, `TBL-STU-026` | `API-STU-007–015`, `API-STU-049` | `SCR-STU-011–013`, `SCR-OPS-015` | `TC-STU-002` |
| `CAP-STU-003` / `UC-STU-003` | `BR-STU-008–009`, `BR-STU-015`, `PERM-STU-010`, `NFR-OPS-003` | `AC-STU-002`, `SEQ-STU-002` | `CLS-STU-002`; `TBL-STU-027–032`, `TBL-STU-049` | `API-STU-018–022`, `API-STU-050`, `API-INT-009` | `SCR-STU-010`, `SCR-STU-015–016`, `SCR-STU-019`, `SCR-OPS-015` | `TC-STU-003` |
| `CAP-STU-004` / `UC-STU-004` | `BR-STU-010–013`, `BR-STU-015`, `PERM-STU-006`, `NFR-OPS-008` | `AC-STU-002`, `SEQ-STU-002–003` | `CLS-STU-002`; `TBL-STU-020–025`, `TBL-STU-033–039`, `TBL-STU-059` | `API-STU-023–033`, `API-STU-047–048` | `SCR-STU-017–018`, `SCR-OPS-012–013` | `TC-STU-004` |
| `CAP-STU-005` / `UC-STU-005` | `BR-STU-016`, `BR-INT-004–009`, `NFR-OPS-006` | `AC-INT-001`, `SEQ-INT-001` | `CLS-STU-002`, `CLS-INT-001`; `TBL-STU-031–032`, `TBL-STU-040–041`, `TBL-WRK-043–045` | `API-IAM-025`, `API-STU-061–062`, `API-INT-002–005`, `EVT-STU-002–003` | `SCR-WRK-017`, `SCR-WRK-019`, `SCR-WRK-040` | `TC-STU-005` |
| `CAP-STU-006` / `UC-STU-006` | `BR-STU-007`, `BR-STU-013–014`, `PERM-STU-001–005` | `AC-STU-003`, `SEQ-STU-004` | `CLS-STU-001`; `TBL-STU-009–025`, `TBL-STU-035–036` | `API-STU-051–059`, `API-OPS-005–006` | `SCR-OPS-003–011` | `TC-STU-006` |
| `CAP-STU-007` / `UC-STU-007` | `BR-STU-017`, `PERM-STU-008`, `PERM-STU-012`, `BR-OPS-003` | N/A — các luồng thông báo/cộng đồng/hỗ trợ độc lập, không có điều phối xuyên dịch vụ | `CLS-STU-002`; `TBL-STU-042–048` | `API-STU-034–046` | `SCR-STU-020–022`, `SCR-OPS-014` | `TC-STU-007` |
| `CAP-STU-008` / `UC-STU-008` | `BR-STU-015`, `PERM-STU-009–014`, `BR-OPS-001–003` | `AC-OPS-001`, `SEQ-OPS-001` | `CLS-STU-001–002`; `TBL-STU-003–006`, `TBL-STU-049–050`, `TBL-STU-054` | `API-STU-047–050`, `API-STU-060`, `API-OPS-007–010` | `SCR-OPS-012–016`, `SCR-OPS-021`, `SCR-OPS-024` | `TC-STU-008` |
| `CAP-WRK-001` / `UC-WRK-001` | `BR-WRK-001`, `BR-WRK-011`, `BR-OPS-004`, `NFR-OPS-003` | `AC-WRK-001`, `SEQ-WRK-003` | `CLS-WRK-001`; `TBL-WRK-004–013`, `TBL-WRK-042` | `API-WRK-005–017`, `API-AIX-001` | `SCR-WRK-011–014` | `TC-WRK-001` |
| `CAP-WRK-002` / `UC-WRK-002` | `BR-WRK-001–003`, `BR-WRK-012`, `PERM-WRK-020–021`, `NFR-OPS-007` | `AC-WRK-001`, `SEQ-WRK-001` | `CLS-WRK-001`; `TBL-WRK-005`, `TBL-WRK-037–040` | `API-WRK-007`, `API-WRK-020–021`, `API-WRK-051–053`, `API-INT-010` | `SCR-WRK-012`, `SCR-WRK-016`, `SCR-WRK-036–038` | `TC-WRK-002` |
| `CAP-WRK-003` / `UC-WRK-003` | `BR-WRK-004–005`, `PERM-WRK-001–004`, `NFR-OPS-012` | N/A — thao tác tạo/đọc/sửa/xóa (`CRUD`) không gian dữ liệu/tư cách thành viên được kiểm qua ủy quyền và ràng buộc, không có quy trình điều phối dài hạn (`saga`) ngoài duyệt xác minh | `CLS-WRK-001`; `TBL-WRK-014–018` | `API-WRK-035–041`, `API-OPS-001–002` | `SCR-WRK-030–032`, `SCR-OPS-017–018` | `TC-WRK-003` |
| `CAP-WRK-004` / `UC-WRK-004` | `BR-WRK-005–007`, `PERM-WRK-010–013`, `BR-OPS-010` | `AC-WRK-002`, `SEQ-WRK-002` | `CLS-WRK-001`; `TBL-WRK-032–036`, `TBL-WRK-074` | `API-WRK-042–050`, `API-OPS-003–006` | `SCR-WRK-033–035`, `SCR-OPS-009–011` | `TC-WRK-004` |
| `CAP-WRK-005` / `UC-WRK-005` | `BR-WRK-008–012`, `PERM-WRK-030–034`, `BR-OPS-010` | `AC-WRK-002`, `SEQ-WRK-003` | `CLS-WRK-001`; `TBL-WRK-041–048`, `TBL-WRK-072–073` | `API-WRK-022–026`, `API-WRK-054–059`, `EVT-WRK-001`, `EVT-WRK-003` | `SCR-WRK-017–019`, `SCR-WRK-039–040` | `TC-WRK-005` |
| `CAP-WRK-006` / `UC-WRK-006` | `BR-INT-004–009`, `BR-WRK-011`, `NFR-OPS-006` | `AC-INT-001`, `SEQ-INT-001` | `CLS-INT-001`; `TBL-STU-040–041`, `TBL-WRK-043–045`, `TBL-WRK-069` | `API-WRK-023`, `API-WRK-027`, `API-IAM-025`, `API-STU-061–062`, `API-INT-002–005`, `EVT-WRK-002` | `SCR-WRK-017`, `SCR-WRK-019`, `SCR-WRK-040` | `TC-WRK-006` |
| `CAP-WRK-007` / `UC-WRK-007` | `BR-WRK-015–016`, `PERM-WRK-040`, `BR-OPS-010` | `AC-WRK-003`, `SEQ-WRK-004` | `CLS-WRK-002`; `TBL-WRK-049–052`, `TBL-WRK-075` | `API-WRK-028–030`, `API-WRK-060–062` | `SCR-WRK-020`, `SCR-WRK-041` | `TC-WRK-007` |
| `CAP-WRK-008` / `UC-WRK-008` | `BR-WRK-013–014`, `BR-OPS-003`, `NFR-OPS-004` | `AC-WRK-003`, `SEQ-WRK-005` | `CLS-WRK-002`; `TBL-WRK-053–056` | `API-WRK-031–034`, `API-INT-011`, `EVT-WRK-004` | `SCR-WRK-021`, `SCR-WRK-042`, `SCR-OPS-026` | `TC-WRK-008` |
| `CAP-WRK-009` / `UC-WRK-009` | `BR-WRK-017`, `BR-PAY-006`, `BR-AIX-002–003`, `PERM-WRK-060` | `AC-WRK-001`, `AC-PAY-001`, `SEQ-WRK-001`, `SEQ-PAY-001` | `CLS-WRK-001`, `CLS-PAY-001`, `CLS-AIX-001`; `TBL-WRK-010–011`, `TBL-PAY-010–013` | `API-PAY-001–013`, `API-AIX-001–002` | `SCR-WRK-013`, `SCR-WRK-022`, `SCR-WRK-034`, `SCR-WRK-043` | `TC-WRK-009` |
| `CAP-WRK-010` / `UC-WRK-010` | `BR-WRK-018`, `PERM-OPS-001–003`, `PERM-WRK-012`, `BR-OPS-001–002` | `AC-OPS-001`, `SEQ-OPS-001` | `CLS-WRK-002`; `TBL-WRK-035–036`, `TBL-WRK-060–061` | `API-OPS-001–010`, `API-WRK-034` | `SCR-OPS-009–011`, `SCR-OPS-017–018`, `SCR-OPS-021`, `SCR-OPS-024–026` | `TC-WRK-010` |
| `CAP-UNI-001` / `UC-UNI-001` | `BR-UNI-001–002`, `PERM-UNI-001–011`, `BR-WRK-004` | `AC-UNI-001`, `SEQ-UNI-001` | `CLS-WRK-002`; `TBL-WRK-019–025`, `TBL-WRK-030` | `API-UNI-001–009` | `SCR-UNI-001–006` | `TC-UNI-001` |
| `CAP-UNI-002` / `UC-UNI-002` | `BR-UNI-002–003`, `PERM-UNI-020–023`, `PERM-WRK-050` | `AC-UNI-001`, `SEQ-UNI-001` | `CLS-WRK-002`; `TBL-WRK-026–029`, `TBL-WRK-071` | `API-UNI-010–014` | `SCR-UNI-007–010`, `SCR-WRK-043` | `TC-UNI-002` |
| `CAP-UNI-003` / `UC-UNI-003` | `BR-UNI-002`, `BR-UNI-004–005`, `PERM-UNI-030–031` | `AC-UNI-001`, `SEQ-UNI-001` | `CLS-WRK-002`; `TBL-WRK-023`, `TBL-WRK-030–031` | `API-UNI-007`, `API-UNI-015–016` | `SCR-UNI-004–005`, `SCR-UNI-011` | `TC-UNI-003` |
| `CAP-PAY-001` / `UC-PAY-001` | `BR-PAY-001–004`, `BR-PAY-007`, `NFR-OPS-003` | `AC-PAY-001`, `SEQ-PAY-001` | `CLS-PAY-001`; `TBL-PAY-001–005` | `API-PAY-001–004`, `API-PAY-016` | `SCR-WRK-022–023`, `SCR-WRK-043–044` | `TC-PAY-001` |
| `CAP-PAY-002` / `UC-PAY-002` | `BR-PAY-004–007`, `BR-OPS-003`, `NFR-OPS-006` | `AC-PAY-001`, `SEQ-PAY-001` | `CLS-PAY-001`; `TBL-PAY-003`, `TBL-PAY-005–006`, `TBL-PAY-010–011` | `API-PAY-003`, `API-PAY-005`, `API-PAY-014–015`, `EVT-PAY-001` | `SCR-WRK-022`, `SCR-WRK-043`; webhook là `SYSTEM` | `TC-PAY-002` |
| `CAP-PAY-003` / `UC-PAY-003` | `BR-PAY-008–010`, `PERM-PAY-001–003`, `BR-OPS-001–002` | `AC-PAY-001`, `SEQ-PAY-002` | `CLS-PAY-001`; `TBL-PAY-007–011` | `API-PAY-006–009`, `EVT-PAY-002` | `SCR-WRK-022`, `SCR-WRK-043`, `SCR-OPS-019–020` | `TC-PAY-003` |
| `CAP-AIX-001` / `UC-AIX-001` | `BR-AIX-001–003`, `BR-AIX-005–007`, `PERM-AIX-001` chỉ áp dụng cho công tắc ngắt | `AC-AIX-001`, `SEQ-AIX-001` | `CLS-AIX-001`; `TBL-AIX-001–006`, `TBL-WRK-010–011`, `TBL-WRK-033` | `API-AIX-001–002`, `API-AIX-005–006`, `EVT-AIX-001` | `SCR-WRK-013`, `SCR-WRK-034` | `TC-AIX-001` |
| `CAP-AIX-002` / `UC-AIX-002` | `BR-AIX-002–007`, `PERM-WRK-070–071`, `NFR-OPS-006` | `AC-AIX-001`, `SEQ-AIX-001` | `CLS-AIX-001`; `TBL-AIX-004–007`, `TBL-WRK-041–042` | `API-AIX-003–006`, `EVT-AIX-001` | `SCR-WRK-039–040` | `TC-AIX-002` |
| `CAP-AIX-003` / `UC-AIX-003` | `BR-AIX-001`, `BR-AIX-008`, `PERM-AIX-001–003`, `NFR-OPS-012` | `AC-AIX-001`, `SEQ-AIX-001` | `CLS-AIX-001`; `TBL-AIX-001–003`, `TBL-AIX-006`, `TBL-AIX-008` | `API-AIX-007–010` | `SCR-OPS-022–023` | `TC-AIX-003` |
| `CAP-OPS-001` / `UC-OPS-001` | `BR-WRK-018`, `BR-OPS-001–002`, `PERM-OPS-001–003`, `PERM-OPS-005` | `AC-OPS-001`, `SEQ-OPS-001` | `CLS-WRK-002`; `TBL-WRK-015`, `TBL-WRK-020`, `TBL-WRK-035`, `TBL-WRK-060–061` | `API-OPS-001–009` | `SCR-OPS-009–011`, `SCR-OPS-017–018`, `SCR-OPS-024–025` | `TC-OPS-001` |
| `CAP-OPS-002` / `UC-OPS-002` | `BR-OPS-005–008`, `PERM-OPS-004`, `BR-IAM-007` | `AC-OPS-001`, `SEQ-OPS-001` | `CLS-IAM-001`, `CLS-INT-001`; `TBL-IAM-001`, `TBL-IAM-017–020`, `TBL-STU-050`, `TBL-WRK-061` | `API-IAM-019–020`, `EVT-IAM-004`, `API-INT-006–007` | `SCR-IAM-006`, `SCR-OPS-024–025` | `TC-OPS-002` |
| `CAP-OPS-003` / `UC-OPS-003` | `BR-INT-009`, `BR-OPS-003`, `BR-OPS-008`, `NFR-OPS-001–012` | `AC-OPS-001`, `SEQ-OPS-001` | `CLS-INT-001`; `TBL-IAM-018–020`, `TBL-STU-052–055`, `TBL-WRK-063–064`, `TBL-WRK-070` | `API-INT-001–010`, `API-OPS-010` | `SCR-OPS-021`; tiến trình nền/cảnh báo/sổ tay vận hành là `SYSTEM` | `TC-OPS-003` |

## 16. Giả định và quyết định mặc định V1

- Đợt thử nghiệm triển khai tại Việt Nam, một vùng chính; mọi tiền tệ dùng VND và giao diện đầu tiên bằng tiếng Việt. Kiến trúc không phụ thuộc vào dữ liệu thực tế cũ.
- Người học và ứng viên là hai vai trò của cùng `platformUserId`; không tự hợp nhất tài khoản theo tên/số điện thoại/email phụ.
- Tệp bài đánh giá tối đa 25 MiB và danh sách cho phép là PDF, PNG/JPEG, TXT/MD/CSV, ZIP; CV/tệp Work áp dụng giới hạn chi tiết tại API nhưng luôn riêng tư và được quét sạch.
- Nội dung cuộc hẹn phỏng vấn có thể chứa địa chỉ hoặc liên kết do nhà tuyển dụng nhập và được làm sạch; hệ thống không tự tạo phòng họp trong V1.
- Trò chuyện V1 chỉ có tin nhắn văn bản/tin nhắn hệ thống; thao tác “xóa” của người dùng là đánh dấu xóa có lịch sử, không xóa cứng tin nhắn đã là bản ghi tuyển dụng.
- Đề xuất Study V1 dựa trên quy tắc. AI chỉ nằm trong Work/TopCV/TopJD/ghép nối và tuân thủ mục 11.5.
- PostgreSQL FTS/trigram đáp ứng tìm kiếm của đợt thử nghiệm; chỉ đề xuất cụm tìm kiếm/kho dữ liệu khi đo tải cho thấy không đạt NFR sau khi tối ưu truy vấn/chỉ mục.
- Nhà cung cấp bên ngoài không trực tiếp quyết định tài khoản/ATS/quyền lợi sử dụng. Mọi phản hồi gọi lại được ánh xạ, kiểm chứng và xác nhận giao dịch qua chủ sở hữu miền.

---

Tài liệu này hoàn tất khi cả năm tài liệu chuẩn cùng vượt qua bộ kiểm và ma trận trên không có tham chiếu bị mất. Mọi người triển khai phải giữ nguyên các quyết định đã khóa; thay đổi cần đi qua quy trình tại mục 1.2 thay vì tự chọn hành vi khác trong mã nguồn.
