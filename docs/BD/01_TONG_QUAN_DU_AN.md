# Study2Work — Tổng quan dự án và thiết kế đích V1-PILOT

| Thuộc tính | Giá trị |
|---|---|
| Trạng thái | Canonical — được phê duyệt cho V1-PILOT |
| Phạm vi | Platform Identity, Study, Work và các tích hợp dùng chung |
| Đối tượng đọc | Product, BA, UX/UI, kiến trúc sư, lập trình viên, QA, DevOps, vận hành và bảo mật |
| Múi giờ nghiệp vụ | `Asia/Ho_Chi_Minh`; mọi thời điểm lưu trữ và trao đổi qua API là UTC |
| Ngôn ngữ dữ liệu | Giao diện tiếng Việt; mã, enum và hợp đồng kỹ thuật dùng tiếng Anh |
| Cỡ pilot | 5.000 tài khoản, 500 DAU, đỉnh 50 RPS |

## 1. Quản trị bộ tài liệu

### 1.1. Vai trò của tài liệu

Tài liệu này là nguồn chuẩn cho **ý định sản phẩm và mọi quyết định xuyên hệ thống**. Bốn tài liệu còn lại cụ thể hóa nhưng không được thay đổi các quyết định tại đây:

| Tài liệu | Nội dung sở hữu |
|---|---|
| `01_TONG_QUAN_DU_AN.md` | Phạm vi, năng lực, use case, quyền, quy tắc nghiệp vụ, kiến trúc, NFR và test chấp nhận |
| `02_BIEU_DO_HE_THONG.md` | Định nghĩa `AC`, `CLS`, `SEQ` và biểu đồ use case dùng các `UC` tại đây |
| `03_THIET_KE_CO_SO_DU_LIEU.md` | Định nghĩa enum và `TBL`, ràng buộc, chỉ mục, transaction, retention vật lý |
| `04_DAC_TA_API.md` | Định nghĩa `API`, `EVT`, `ERR`, hợp đồng HTTP/WebSocket/webhook và logic truy vấn |
| `05_DAC_TA_MAN_HINH.md` | Định nghĩa `SCR`, route, trường hiển thị, trạng thái và luồng tương tác |

Thứ tự ưu tiên khi có sai khác là: quyết định nghiệp vụ tại tài liệu này → hợp đồng API/event → mô hình dữ liệu → biểu đồ → mô tả màn hình. OpenAPI, migration và event schema là hợp đồng thực thi dẫn xuất; pull request làm thay đổi hành vi phải cập nhật tài liệu sở hữu và các hợp đồng liên quan trong cùng thay đổi.

### 1.2. Quy ước định danh và thay đổi

- ID có dạng `TYPE-CTX-NNN`; `CTX` thuộc `IAM`, `STU`, `WRK`, `PAY`, `UNI`, `AIX`, `INT`, `OPS`.
- Tài liệu này sở hữu `CAP`, `UC`, `BR`, `PERM`, `NFR`, `TC`. ID đã phát hành không được tái sử dụng cho nghĩa khác; mục bị loại phải được đánh dấu ngừng dùng trong lịch sử thay đổi.
- Mọi thay đổi trạng thái, quyền truy cập, dữ liệu cá nhân, thanh toán hoặc quyết định AI cần ít nhất một business rule, một test chấp nhận và một dòng truy vết.
- Nội dung đã khóa cho V1-PILOT chỉ được thay đổi qua ADR hoặc quyết định sản phẩm có người chịu trách nhiệm, tác động tương thích và kế hoạch chuyển đổi rõ ràng.
- Không lấy prototype Work cũ, tài liệu BD cũ hoặc mã nguồn đang chạy làm căn cứ để ghi đè đặc tả đích này.

### 1.3. Trách nhiệm phê duyệt

| Nhóm thay đổi | Người chịu trách nhiệm cuối | Bên bắt buộc rà soát |
|---|---|---|
| Phạm vi, journey, business rule | Product Owner | BA, Tech Lead, QA |
| Identity, quyền, tenant, privacy | Security/Platform Owner | Product, Tech Lead, DPO/người phụ trách dữ liệu |
| Study và Work domain | Domain Owner tương ứng | Product, Data, QA |
| Thanh toán, hoàn tiền | Finance Owner | Product, Security, Work Owner |
| AI và matching | AI Governance Owner | Product, Security, Recruitment Domain Owner |
| NFR, vận hành, khôi phục | Platform/Operations Owner | Các Domain Owner, Security |

## 2. Tầm nhìn, mục tiêu và phạm vi

### 2.1. Tầm nhìn

Study2Work là hệ sinh thái EdTech + HRTech giúp người học xây năng lực có cấu trúc trong Study, chủ động dùng minh chứng đã chọn để ứng tuyển trong Work, và giúp doanh nghiệp/trường đại học vận hành tuyển dụng thực tập minh bạch. Hệ thống ưu tiên consent, khả năng kiểm toán và quyết định có con người chịu trách nhiệm.

### 2.2. Mục tiêu V1-PILOT

1. Cung cấp một danh tính email/password an toàn cho toàn nền tảng, không sao chép credential vào Study hoặc Work.
2. Cho phép học độc lập mọi khóa đã xuất bản; onboarding chỉ phục vụ lựa chọn lộ trình chính.
3. Bảo toàn lịch sử học và phiên bản nội dung, phát hành minh chứng có thể thu hồi.
4. Cung cấp hồ sơ nghề nghiệp, CV, job, ứng tuyển, ATS, phỏng vấn và chat 1–1 theo hồ sơ ứng tuyển.
5. Cho phép doanh nghiệp tìm ứng viên chỉ khi ứng viên chủ động bật tìm kiếm, không lộ thông tin liên hệ, CV hoặc evidence trong kết quả tìm kiếm.
6. Hỗ trợ tenant doanh nghiệp và trường đại học với phân quyền, consent và cách ly dữ liệu.
7. Bán gói/credit trả trước bằng VND qua VNPAY và MoMo; kích hoạt quyền lợi chính xác một lần theo xác nhận từ provider.
8. Dùng AI để soạn thảo và giải thích/đề xuất, không tự ra quyết định tuyển dụng hoặc thay đổi trạng thái ATS.

### 2.3. Trong phạm vi

- Web responsive cho khách, người học/ứng viên, doanh nghiệp, trường đại học và đội vận hành.
- Identity: đăng ký email/password, xác minh email, đăng nhập, reset password, session, rotating refresh token, TOTP MFA, quản trị trạng thái và vai trò nền tảng.
- Study: catalog, onboarding, đề xuất lộ trình, lộ trình chính, khóa học độc lập, nội dung phiên bản, tiến độ, assessment, file scan, evidence, thông báo, cộng đồng, hỗ trợ và quản trị nội dung.
- Work: hồ sơ nghề nghiệp, CV/portfolio, candidate search, tenant doanh nghiệp, job revision, ATS, evidence khi apply, interview, chat, notification và moderation.
- University: affiliation, cohort, chương trình thực tập, phân phối campus job, partnership/referral và báo cáo aggregate.
- TopCV/TopJD: template cao cấp, AI writing, sponsored profile/job có nhãn và quyền lợi trả trước.
- Thanh toán: VNPAY, MoMo, đối soát, hoàn tiền, chargeback và entitlement.
- AI bất đồng bộ qua provider adapter, mặc định Ollama cho pilot.
- Audit, privacy request, retention, quan sát vận hành, backup và disaster recovery.

### 2.4. Ngoài phạm vi

- Đăng nhập social, số điện thoại/OTP, SSO doanh nghiệp và định danh điện tử.
- Ứng dụng mobile native, thanh toán trong ứng dụng và thông báo push native.
- Marketplace giảng viên, live class, proctoring, coding sandbox và chấm source code tự động.
- Group chat, gọi thoại/video, gửi file trong chat; V1 chỉ có text và system message 1–1 theo application.
- Đồng bộ Google/Microsoft Calendar hoặc nền tảng họp; V1 dùng lịch nội bộ và file/link ICS.
- Auto-renew subscription, lưu thẻ, ví nội bộ, escrow, payout, payroll hoặc marketplace commission.
- AI tự động apply, tự động đổi ATS, xếp hạng bằng thuộc tính nhạy cảm, tự reject/hire hoặc thay con người phê duyệt.
- Search cluster, data warehouse, microservice theo từng module và database query chéo.
- Theo dõi cá nhân bởi trường đại học khi chưa có consent còn hiệu lực; nhóm báo cáo dưới 10 người.

## 3. Thuật ngữ chuẩn

| Thuật ngữ | Định nghĩa canonical |
|---|---|
| Platform Identity | Deployable dùng chung sở hữu user, credential, verification, session, token, global role và security audit. |
| Platform user | Danh tính toàn cục có `platformUserId` UUID bất biến. |
| Projection | Bản sao tối thiểu, cuối cùng nhất quán của identity hoặc taxonomy trong database domain; không phải credential. |
| Learner | Platform user sử dụng Study. |
| Candidate | Platform user sở hữu hồ sơ nghề nghiệp trong Work; cùng người có thể đồng thời là Learner. |
| Tenant | Biên dữ liệu doanh nghiệp hoặc trường đại học; mọi truy vấn tenant phải lấy tenant từ membership đã xác thực phía server. |
| Membership | Quan hệ user–tenant có role, trạng thái và thời hạn; không phải global role. |
| Primary path | Một lộ trình chính đang `ACTIVE`; không hạn chế học các khóa standalone. |
| Stable entity | Danh tính bền vững của path/course/job; nội dung xuất bản nằm trong revision/version bất biến. |
| Evidence | Minh chứng Study đã phát hành cho một kết quả học tập, có version, owner và trạng thái thu hồi. |
| Evidence snapshot | Bản chụp tối thiểu Work lưu theo application sau khi ứng viên chọn evidence và đồng ý xuất. |
| Consent | Bản ghi chủ thể, mục đích, phạm vi, phiên bản điều khoản, thời điểm cấp/hết hạn/thu hồi. |
| ATS | Luồng xử lý application của doanh nghiệp; mọi thay đổi trạng thái có actor và audit. |
| Candidate search opt-in | Sự đồng ý riêng để hồ sơ được lập chỉ mục/tìm thấy; mặc định tắt. |
| Organic score | Điểm phù hợp không chịu ảnh hưởng bởi thanh toán hay sponsored placement. |
| Sponsored placement | Vị trí quảng bá trả phí, luôn có nhãn và xếp riêng khỏi organic score. |
| Entitlement | Quyền sử dụng/credit phát sinh từ order đã `SETTLED`; có số dư, hạn dùng và ledger. |
| Idempotency | Cùng principal, operation và `Idempotency-Key` cho cùng payload trả lại cùng kết quả, không tạo side effect lần hai. |
| Outbox | Event được ghi cùng transaction với thay đổi domain rồi worker phát đi ít nhất một lần. |
| Terminal state | Trạng thái không thể chuyển tiếp qua API nghiệp vụ thông thường. |
| Privileged user | Mọi internal operator hoặc thành viên tenant có quyền xem dữ liệu người khác, xuất bản, tuyển dụng, tài chính, phân quyền hay audit. |
| PII | Dữ liệu có thể nhận diện cá nhân như email, tên, liên hệ, CV, địa chỉ, file và lịch sử ứng tuyển. |

## 4. Actor, tenant, vai trò và quyền

### 4.1. Actor

| Actor | Phạm vi hành động |
|---|---|
| Guest | Xem landing/catalog/job công khai; đăng ký, xác minh và đăng nhập. |
| Learner/Candidate | Quản lý dữ liệu của chính mình, học, ứng tuyển, consent, thanh toán và privacy request. |
| Content Author / Publisher | Soạn nội dung / kiểm tra và xuất bản phiên bản Study. |
| Assessment Reviewer | Chấm text/link/file theo rubric; không sửa bài đã submit. |
| Learner Support / Community Moderator | Xử lý hỗ trợ hoặc moderation trong đúng phạm vi được giao. |
| Enterprise Owner / Admin | Quản lý tenant, membership, billing, job và chính sách tuyển dụng. |
| Recruiter / Interviewer | Recruiter vận hành sourcing/ATS; Interviewer chỉ xem hồ sơ/phỏng vấn được phân công và feedback được phép. |
| University Owner / Coordinator / Viewer | Quản lý tenant, affiliation/cohort/program/referral hoặc chỉ xem báo cáo aggregate theo role. |
| Finance Operator | Đối soát, xử lý hoàn tiền/chargeback; không được tự cấp role hoặc sửa application. |
| Platform Moderator / Admin / Security Auditor | Moderation toàn nền tảng, vận hành, phân quyền hoặc chỉ đọc audit theo trách nhiệm. |
| Payment Provider | VNPAY hoặc MoMo gửi callback/webhook đã ký và nhận yêu cầu query/refund. |
| AI Provider | Ollama qua adapter nhận input đã lọc và trả output có schema; không là actor quyết định. |

### 4.2. Mô hình role

- Platform Identity chỉ phát global role thô: `LEARNER`, `PLATFORM_ADMIN`, `FINANCE_OPERATOR`, `PLATFORM_MODERATOR`, `SECURITY_AUDITOR`. Role thay đổi làm tăng `authVersion` và thu hồi session liên quan.
- Study giữ local role: `CONTENT_AUTHOR`, `CONTENT_PUBLISHER`, `ASSESSMENT_REVIEWER`, `LEARNER_SUPPORT`, `COMMUNITY_MODERATOR`, `STUDY_ADMIN`.
- Work giữ membership role theo tenant: `ENTERPRISE_OWNER`, `ENTERPRISE_ADMIN`, `RECRUITER`, `INTERVIEWER`; University giữ `UNIVERSITY_OWNER`, `UNIVERSITY_COORDINATOR`, `UNIVERSITY_VIEWER`.
- Role chỉ là gói quyền. Backend kiểm permission cụ thể, tenant membership `ACTIVE`, resource scope và account `ACTIVE` trên từng request; frontend guard không phải biện pháp bảo mật.
- Mọi privileged user phải hoàn tất TOTP MFA trước khi dùng quyền đặc quyền. Break-glass chỉ dành cho Platform Admin được chỉ định, có lý do, thời hạn tối đa 60 phút và audit cảnh báo ngay.

### 4.3. Catalog permission

| ID | Permission key | Được cấp mặc định |
|---|---|---|
| **PERM-IAM-001** | `platform.users.read` | Platform Admin, Security Auditor (chỉ đọc) |
| **PERM-IAM-002** | `platform.users.status.manage` | Platform Admin |
| **PERM-IAM-003** | `platform.roles.manage` | Platform Admin |
| **PERM-IAM-004** | `platform.security.audit.read` | Security Auditor, Platform Admin |
| **PERM-STU-001** | `study.content.read_admin` | Content Author/Publisher, Study Admin |
| **PERM-STU-002** | `study.content.write` | Content Author/Publisher, Study Admin |
| **PERM-STU-003** | `study.content.publish` | Content Publisher, Study Admin |
| **PERM-STU-004** | `study.content.archive` | Study Admin |
| **PERM-STU-005** | `study.content_issues.manage` | Content Publisher, Study Admin |
| **PERM-STU-006** | `study.assessments.review` | Assessment Reviewer, Study Admin |
| **PERM-STU-008** | `study.support.read_internal` | Learner Support, Study Admin |
| **PERM-STU-009** | `study.primary_path.override` | Learner Support được ủy quyền, Study Admin |
| **PERM-STU-010** | `study.progress.adjust` | Study Admin được ủy quyền |
| **PERM-STU-011** | `study.roles.manage` | Study Admin |
| **PERM-STU-012** | `study.community.moderate` | Community Moderator, Study Admin |
| **PERM-STU-013** | `study.reports.read` | Study Admin |
| **PERM-STU-014** | `study.audit.read` | Study Admin, Security Auditor theo scope |
| **PERM-WRK-001** | `work.enterprise.profile.manage` | Enterprise Owner/Admin |
| **PERM-WRK-002** | `work.enterprise.verification.submit` | Enterprise Owner/Admin |
| **PERM-WRK-003** | `work.enterprise.members.read` | Enterprise Owner/Admin |
| **PERM-WRK-004** | `work.enterprise.members.manage` | Enterprise Owner/Admin |
| **PERM-WRK-010** | `work.jobs.read_admin` | Enterprise Owner/Admin, Recruiter |
| **PERM-WRK-011** | `work.jobs.author` | Enterprise Owner/Admin, Recruiter |
| **PERM-WRK-012** | `work.jobs.submit_review` | Enterprise Owner/Admin, Recruiter được ủy quyền |
| **PERM-WRK-013** | `work.jobs.publish_manage` | Enterprise Owner/Admin; trusted publisher theo grant có hạn |
| **PERM-WRK-020** | `work.candidates.search` | Enterprise Owner/Admin, Recruiter có entitlement |
| **PERM-WRK-021** | `work.candidates.invite` | Enterprise Owner/Admin, Recruiter có entitlement |
| **PERM-WRK-030** | `work.applications.list` | Enterprise Owner/Admin, Recruiter |
| **PERM-WRK-031** | `work.applications.read_unassigned` | Enterprise Owner/Admin; Recruiter chỉ khi được phân công nếu không có quyền này |
| **PERM-WRK-032** | `work.applications.assign` | Enterprise Owner/Admin, lead recruiter |
| **PERM-WRK-034** | `work.applications.offer_manage` | Enterprise Owner/Admin, Recruiter được ủy quyền và phân công |
| **PERM-WRK-040** | `work.interviews.manage` | Enterprise Owner/Admin, Recruiter được phân công |
| **PERM-WRK-050** | `work.university_partnerships.respond` | Enterprise Owner/Admin |
| **PERM-WRK-060** | `work.promotions.manage` | Enterprise Owner/Admin có entitlement |
| **PERM-WRK-070** | `work.ai.match_explain` | Recruiter được phân công có entitlement |
| **PERM-WRK-071** | `work.ai.shortlist_suggest` | Enterprise Owner/Admin, lead recruiter có entitlement |
| **PERM-UNI-001** | `university.verification.submit` | University Owner |
| **PERM-UNI-002** | `university.members.read` | University Owner |
| **PERM-UNI-003** | `university.members.manage` | University Owner |
| **PERM-UNI-010** | `university.affiliations.invite` | University Owner/Coordinator |
| **PERM-UNI-011** | `university.cohorts.manage` | University Owner/Coordinator |
| **PERM-UNI-020** | `university.programs.manage` | University Owner/Coordinator |
| **PERM-UNI-021** | `university.campus_jobs.distribute` | University Owner/Coordinator |
| **PERM-UNI-022** | `university.partnerships.manage` | University Owner/Coordinator |
| **PERM-UNI-023** | `university.referrals.manage` | University Owner/Coordinator |
| **PERM-UNI-030** | `university.reports.read` | University Owner/Coordinator/Viewer |
| **PERM-UNI-031** | `university.affiliations.read_consented` | University Owner/Coordinator theo purpose consent |
| **PERM-PAY-001** | `billing.reconciliation.read` | Finance Operator |
| **PERM-PAY-002** | `billing.refunds.approve` | Finance Operator có maker/checker separation |
| **PERM-PAY-003** | `billing.reconciliation.execute` | Finance Operator được ủy quyền |
| **PERM-AIX-001** | `ai.kill_switch.manage` | AI Governance Owner/Platform Admin được ủy quyền |
| **PERM-AIX-002** | `ai.model_configs.manage` | AI Governance Owner |
| **PERM-AIX-003** | `ai.prompt_eval.manage` | AI Governance Owner |
| **PERM-OPS-001** | `operations.verification.review` | Platform Moderator được ủy quyền |
| **PERM-OPS-002** | `operations.job_review` | Platform Moderator |
| **PERM-OPS-003** | `operations.trusted_publisher.manage` | Platform Admin được ủy quyền |
| **PERM-OPS-004** | `privacy.legal_hold.manage` | Platform Admin được ủy quyền; Security Auditor giám sát |
| **PERM-OPS-005** | `operations.break_glass.use` | Incident responder được chỉ định |

Self-service của Learner/Candidate, mua hàng của chính mình và chat/interview được phân công được cấp qua ownership/membership + trạng thái, không tạo permission giả trên client. Permission phía trên luôn kết hợp MFA, entitlement, assignment, consent và resource predicate nếu endpoint yêu cầu.

## 5. Năng lực và use case V1-PILOT

| Capability ID | Use case ID | Năng lực và kết quả |
|---|---|---|
| **CAP-IAM-001** | `UC-IAM-001` | Guest đăng ký email/password, xác minh email và trở thành user `ACTIVE`. |
| **CAP-IAM-002** | `UC-IAM-002` | User đăng nhập, MFA khi cần, refresh/logout và quản lý session an toàn. |
| **CAP-IAM-003** | `UC-IAM-003` | Admin quản lý account/global role; auditor đọc security audit. |
| **CAP-STU-001** | `UC-STU-001` | Khách xem catalog; learner enroll và học khóa standalone đã xuất bản. |
| **CAP-STU-002** | `UC-STU-002` | Learner onboarding, nhận gợi ý, chọn/chuyển primary path. |
| **CAP-STU-003** | `UC-STU-003` | Learner học block/lesson, ghi progress và hoàn thành course/path theo version. |
| **CAP-STU-004** | `UC-STU-004` | Learner làm quiz/text/link/file; hệ thống scan/chấm/review/resubmit. |
| **CAP-STU-005** | `UC-STU-005` | Study phát hành/thu hồi evidence; learner chọn evidence để xuất khi apply. |
| **CAP-STU-006** | `UC-STU-006` | Trusted publisher soạn, kiểm tra và xuất bản version nội dung bất biến. |
| **CAP-STU-007** | `UC-STU-007` | Learner dùng notification, community và support; operator xử lý đúng scope. |
| **CAP-STU-008** | `UC-STU-008` | Study Admin xem báo cáo, điều chỉnh có audit và quản lý local RBAC. |
| **CAP-WRK-001** | `UC-WRK-001` | Candidate tạo career profile, CV/portfolio và snapshot ứng tuyển. |
| **CAP-WRK-002** | `UC-WRK-002` | Recruiter tìm candidate opt-in và gửi invitation không làm lộ dữ liệu riêng. |
| **CAP-WRK-003** | `UC-WRK-003` | Enterprise Owner/Admin xác minh tenant và quản lý membership an toàn. |
| **CAP-WRK-004** | `UC-WRK-004` | Enterprise soạn revision, duyệt, publish/pause/close job. |
| **CAP-WRK-005** | `UC-WRK-005` | Candidate apply; recruiter vận hành application qua ATS có audit. |
| **CAP-WRK-006** | `UC-WRK-006` | Work xuất evidence đã chọn bất đồng bộ và hiển thị trạng thái an toàn. |
| **CAP-WRK-007** | `UC-WRK-007` | Hai bên đề xuất/xác nhận/đổi lịch và hoàn tất interview bằng lịch nội bộ/ICS. |
| **CAP-WRK-008** | `UC-WRK-008` | Candidate và recruiter được phân công chat text realtime theo application. |
| **CAP-WRK-009** | `UC-WRK-009` | Candidate dùng TopCV, enterprise dùng TopJD; sponsored placement luôn có nhãn. |
| **CAP-WRK-010** | `UC-WRK-010` | Moderator xử lý report/takedown và platform xem báo cáo vận hành. |
| **CAP-UNI-001** | `UC-UNI-001` | University quản lý tenant, affiliation và cohort. |
| **CAP-UNI-002** | `UC-UNI-002` | University quản lý internship, campus job, partnership và referral. |
| **CAP-UNI-003** | `UC-UNI-003` | University xem dữ liệu consent hợp lệ và báo cáo aggregate bảo vệ riêng tư. |
| **CAP-PAY-001** | `UC-PAY-001` | Student/Enterprise tạo order VND trả trước và chuyển sang VNPAY/MoMo. |
| **CAP-PAY-002** | `UC-PAY-002` | Webhook/IPN xác nhận settlement chính xác một lần và cấp entitlement. |
| **CAP-PAY-003** | `UC-PAY-003` | Finance đối soát, hoàn tiền và xử lý chargeback có audit. |
| **CAP-AIX-001** | `UC-AIX-001` | AI tạo draft CV/JD để người dùng sửa và chủ động chấp nhận. |
| **CAP-AIX-002** | `UC-AIX-002` | AI giải thích match/đề xuất shortlist; recruiter tự quyết định ATS. |
| **CAP-AIX-003** | `UC-AIX-003` | Operator quản trị model/prompt/evaluation và duyệt thay đổi AI. |
| **CAP-OPS-001** | `UC-OPS-001` | Moderator xử lý nội dung vi phạm và hành động break-glass có kiểm soát. |
| **CAP-OPS-002** | `UC-OPS-002` | User export/xóa dữ liệu; legal hold và anonymization tuân thủ policy. |
| **CAP-OPS-003** | `UC-OPS-003` | Operations quan sát, khôi phục, retry/DLQ và xử lý sự cố. |

### 5.1. Danh mục use case canonical

| ID | Tên use case |
|---|---|
| **UC-IAM-001** | Đăng ký và xác minh email |
| **UC-IAM-002** | Đăng nhập, MFA và quản lý session |
| **UC-IAM-003** | RBAC và quản trị vòng đời account |
| **UC-STU-001** | Xem catalog và học course standalone |
| **UC-STU-002** | Onboarding, gợi ý và primary path |
| **UC-STU-003** | Học lesson và ghi nhận progress |
| **UC-STU-004** | Làm, chấm và review assessment |
| **UC-STU-005** | Phát hành, xuất và thu hồi evidence |
| **UC-STU-006** | Soạn, kiểm tra và publish nội dung |
| **UC-STU-007** | Notification, community và support |
| **UC-STU-008** | Báo cáo và vận hành Study |
| **UC-WRK-001** | Quản lý candidate profile, CV và portfolio |
| **UC-WRK-002** | Candidate search và invitation |
| **UC-WRK-003** | Quản trị enterprise tenant |
| **UC-WRK-004** | Soạn, duyệt và publish job revision |
| **UC-WRK-005** | Apply và quản lý ATS |
| **UC-WRK-006** | Chọn Study evidence khi apply |
| **UC-WRK-007** | Lập và quản lý interview |
| **UC-WRK-008** | Chat theo application |
| **UC-WRK-009** | TopCV, TopJD và sponsored placement |
| **UC-WRK-010** | Moderation và báo cáo Work |
| **UC-UNI-001** | Tenant trường, affiliation và cohort |
| **UC-UNI-002** | Internship, campus job và referral |
| **UC-UNI-003** | Consent và báo cáo trường |
| **UC-PAY-001** | Tạo checkout VND |
| **UC-PAY-002** | Webhook/IPN và entitlement |
| **UC-PAY-003** | Refund, chargeback và reconciliation |
| **UC-AIX-001** | Trợ lý soạn CV/JD |
| **UC-AIX-002** | Match explanation và shortlist suggestion |
| **UC-AIX-003** | Governance và human approval |
| **UC-OPS-001** | Moderation đa miền và break-glass |
| **UC-OPS-002** | Export, xóa/anonymize và legal hold |
| **UC-OPS-003** | Quan sát, retry và khôi phục |

## 6. Journey đầu cuối

### 6.1. Từ đăng ký đến học tập

1. Guest đăng ký bằng email/password và chấp nhận phiên bản điều khoản hiện hành. Identity tạo account chờ xác minh, credential Argon2id và email token một lần.
2. Link còn hạn và chưa dùng chuyển account sang `ACTIVE`; user đăng nhập, nhận access token 15 phút và refresh token xoay vòng 30 ngày.
3. Learner có thể xem/enroll bất kỳ course standalone đã xuất bản ngay, không cần onboarding.
4. Khi muốn chọn primary path, learner hoàn tất onboarding, xem tối đa ba đề xuất có lý do và chọn một path version hiện hành.
5. Learner học theo content facts; hệ thống tính snapshot phần trăm. Sau 168 giờ kể từ lần đổi primary path gần nhất, learner có thể tự chuyển và toàn bộ progress/attempt cũ được giữ.

### 6.2. Từ nội dung đến evidence

1. Author tạo draft course/path version, chapter, lesson, block, resource, assessment và rights record.
2. Pre-publish check xác nhận cấu trúc, rights, nội dung sanitize, asset `CLEAN`, rubric/quiz hợp lệ và liên kết version đầy đủ.
3. Publisher khác quyền author hoặc Study Admin có `study.content.publish` xuất bản. Bản published không sửa; bản mới supersede bản cũ nhưng enrollment cũ vẫn pin version cũ.
4. Quiz được auto-grade; text/link/file vào manual review. File chỉ nộp sau scan `CLEAN`, link HTTPS không được backend fetch.
5. Khi completion hợp lệ, Study phát hành evidence bất biến theo version và outbox event; revoke tạo sự kiện mới, không xóa lịch sử.

### 6.3. Từ hồ sơ nghề nghiệp đến tuyển dụng

1. Candidate tạo career profile, CV và portfolio; hồ sơ tìm kiếm mặc định `PRIVATE`.
2. Khi bật opt-in, chỉ trường public đã chọn được đưa vào candidate index. Tắt opt-in loại khỏi kết quả trong tối đa 5 phút.
3. Enterprise đã xác minh tạo job revision, gửi duyệt, publish và có thể pause/close. Recruiter tìm candidate opt-in và gửi invitation; invitation chưa tạo application hoặc chat.
4. Candidate mở job/invitation, chọn CV/profile snapshot và từng Study evidence muốn chia sẻ, xác nhận consent rồi submit một application duy nhất cho job.
5. Work commit application dù Study đang lỗi; worker xuất evidence sau. Recruiter thấy `PENDING`, `READY`, `UNAVAILABLE`, `REVOKED` hoặc `HIDDEN`, không được dùng lỗi tích hợp làm tín hiệu loại.
6. Recruiter được phân công chuyển ATS; hai bên chat, lên lịch interview và xử lý offer. Mọi trạng thái có actor, reason khi cần và audit; application terminal làm chat chỉ đọc.

### 6.4. University và campus recruitment

1. University Owner xác minh tenant, mời coordinator/viewer, tạo affiliation/cohort và chương trình thực tập.
2. Candidate tự chấp nhận affiliation và consent cụ thể cho chương trình; University không tự gắn sinh viên bằng email.
3. Coordinator phân phối job vào campus program và tạo referral có trạng thái; candidate vẫn phải chủ động apply và chọn evidence.
4. Báo cáo mặc định aggregate; mọi lát cắt dưới 10 người bị ẩn. Dữ liệu cá nhân chỉ hiện trong mục đích, phạm vi và thời hạn consent.

### 6.5. Mua quyền lợi và sponsored placement

1. Student hoặc Enterprise chọn package/credit, hệ thống chụp snapshot giá bằng số nguyên VND và tạo order idempotent.
2. Người mua chọn VNPAY hoặc MoMo và được chuyển đến provider. Return URL chỉ hiển thị trạng thái đang xác nhận/đã xác nhận từ server.
3. Webhook/IPN hợp lệ chuyển payment sang `SETTLED` đúng một lần; cùng transaction tạo ledger/entitlement và outbox.
4. TopCV/TopJD tiêu entitlement qua ledger bất biến. Sponsored result có nhãn, nằm ở slot riêng và không sửa organic/match/ATS score.
5. Finance đối soát sai lệch, refund về provider gốc hoặc xử lý chargeback; hệ thống điều chỉnh quyền lợi và audit theo quy tắc tại mục 11.

### 6.6. AI có con người kiểm soát

1. User chủ động yêu cầu AI, xem dữ liệu đầu vào được dùng và tiêu credit nếu gói yêu cầu.
2. Worker lọc PII/thuộc tính cấm, ghim `provider`, `modelVersion`, `promptPolicyVersion` rồi gọi Ollama adapter bất đồng bộ.
3. Output có schema là draft/explanation, được đánh dấu do AI tạo. User có thể chấp nhận, sửa hoặc loại bỏ.
4. Với matching/shortlist, recruiter phải tự thực hiện thao tác ATS; AI không có credential/quyền gọi transition application.

## 7. Quy tắc nghiệp vụ canonical

### 7.1. Identity và phân quyền

| ID | Quy tắc |
|---|---|
| **BR-IAM-001** | V1 chỉ đăng ký bằng email/password. Email được trim, normalize domain và so khớp không phân biệt hoa thường; mỗi email chỉ thuộc một platform user chưa anonymize. |
| **BR-IAM-002** | Account phải xác minh email trước khi dùng API được bảo vệ. Password chỉ lưu Argon2id hash; Study và Work không được lưu password, verification token hoặc refresh token. |
| **BR-IAM-003** | Access token ES256 có hạn 15 phút; refresh token dạng opaque có hạn tối đa 30 ngày, lưu hash, xoay ở mỗi lần dùng và thuộc một session family. |
| **BR-IAM-004** | Dùng lại refresh token đã tiêu thụ lập tức thu hồi toàn session family, tăng security signal và ghi audit; client phải đăng nhập lại. |
| **BR-IAM-005** | TOTP MFA và recovery code dùng một lần là bắt buộc cho privileged user. Thay đổi MFA, password, email hoặc global role thu hồi session không còn tin cậy. |
| **BR-IAM-006** | Account status, credential lock, onboarding status, tenant membership và learning enrollment là các trạng thái độc lập. Sai password chỉ đặt `lockedUntil`; không đổi account thành trạng thái học tập. |
| **BR-IAM-007** | Suspend hoặc chuyển sang deletion pending thu hồi mọi session và phát signed event. Study/Work phải chặn request nếu JWT hết hạn, `authVersion` cũ hoặc projection cho biết account không `ACTIVE`. |
| **BR-IAM-008** | Reset password, resend verification và login dùng phản hồi công khai không tiết lộ email có tồn tại; rate limit kết hợp IP, normalized email và device signal. |

### 7.2. Study

| ID | Quy tắc |
|---|---|
| **BR-STU-001** | Mọi course có current published version đều independently enrollable. Learner `ACTIVE` và đã xác minh email không cần onboarding hoặc primary path để học standalone. |
| **BR-STU-002** | Onboarding chỉ bắt buộc trước khi chọn primary path. Hoàn tất onboarding là đơn điệu; chỉnh profile tạo recommendation run mới nhưng không đưa trạng thái lùi. |
| **BR-STU-003** | Mỗi learner có tối đa một primary path period `ACTIVE`; selection/switch dùng transaction lock và partial unique constraint. |
| **BR-STU-004** | Self-switch bị khóa đúng 168 giờ tính theo UTC kể từ lần primary path thay đổi gần nhất. Initial selection và chọn sau khi path đã `COMPLETED` không bị cooldown. |
| **BR-STU-005** | Admin chỉ bypass cooldown khi có `PERM-STU-009` (`study.primary_path.override`), nhập reason và xác nhận tác động; path mới vẫn có `nextSwitchAllowedAt = changedAt + 168 giờ`. |
| **BR-STU-006** | Switch đóng period cũ bằng `SWITCHED_OUT`, tạo period mới atomically và không xóa course enrollment, progress, attempt, review, completion hay evidence. |
| **BR-STU-007** | Published path/course version là bất biến. Publish version mới atomically đổi current version và đánh dấu bản cũ `SUPERSEDED`; enrollment cũ tiếp tục pin bản cũ. |
| **BR-STU-008** | Completion chỉ tái sử dụng khi đúng cùng `courseVersionId`; course có stable ID giống nhau nhưng version khác không được tự kế thừa completion hoặc progress. |
| **BR-STU-009** | Nguồn sự thật tiến độ là completion fact của content block, lesson và assessment. Course/path percent chỉ là snapshot server tính, có thể rebuild và client không được ghi trực tiếp. |
| **BR-STU-010** | Assessment V1 chỉ có `QUIZ`, `TEXT`, `LINK`, `FILE`. Quiz auto-grade; ba loại còn lại manual review theo rubric và mỗi lần resubmit tạo attempt mới. |
| **BR-STU-011** | File assessment phải ở trạng thái `CLEAN` trước khi submit/download/review; infected hoặc scan failed không tạo attempt. Object lưu private, URL tải có hạn và được cấp sau authorization. |
| **BR-STU-012** | Link assessment chỉ chấp nhận HTTPS tối đa 2.048 ký tự; backend không fetch, resolve preview hoặc follow redirect để tránh SSRF. Text tối đa 20.000 ký tự. |
| **BR-STU-013** | Mỗi assessment placement thuộc đúng một scope: path version, course version, chapter hoặc lesson. Quan hệ không hợp lệ bị chặn ở application và database constraint. |
| **BR-STU-014** | Trusted publisher không được bỏ qua rights check, HTML/Markdown sanitization, malware scan, cấu trúc curriculum, rubric hoặc audit. Author không tự có quyền publish. |
| **BR-STU-015** | Điều chỉnh progress/review đã ghi chỉ qua nghiệp vụ correction append-only có actor/reason; không xóa hoặc update fact gốc và không có learner API để recalculate/reset. |
| **BR-STU-016** | Completion hợp lệ phát hành evidence `ISSUED` gắn owner và exact source version. Revoke chuyển `REVOKED`, giữ lịch sử và phát event; không tái sử dụng ID đã thu hồi. |
| **BR-STU-017** | Notification có dedupe key; community link chỉ trả sau khi learner chấp nhận đúng rules version hiện hành; external community không được coi là kênh lưu dữ liệu chính thức. |

### 7.3. Work và tuyển dụng

| ID | Quy tắc |
|---|---|
| **BR-WRK-001** | Career profile mặc định `PRIVATE`. Chỉ candidate tự bật `SEARCHABLE`; không tenant, recruiter hoặc admin thông thường nào được bật thay. |
| **BR-WRK-002** | Candidate search chỉ chứa field public đã chọn, skill/kinh nghiệm tổng quát và availability; không trả email, phone, CV file, địa chỉ chi tiết, application, Study evidence hoặc thuộc tính nhạy cảm. |
| **BR-WRK-003** | Opt-out phải làm hồ sơ biến mất khỏi kết quả và cache trong tối đa 5 phút. Snapshot/audit hợp pháp đã có trong application không bị xóa bởi opt-out tìm kiếm. |
| **BR-WRK-004** | Mọi enterprise/university query lấy tenant từ active membership phía server và lọc bằng tenant key; resource ID do client gửi không bao giờ đủ để cấp quyền. Composite tenant constraint ngăn liên kết chéo tenant. |
| **BR-WRK-005** | Enterprise phải `VERIFIED` mới publish job, search candidate, gửi invitation hoặc mua quyền lợi tenant. Suspension chặn mutation mới nhưng giữ audit/history. |
| **BR-WRK-006** | Job dùng stable entity và immutable revision. Sửa job đang published tạo draft revision mới; bản đang published vẫn phục vụ cho đến khi bản mới được duyệt và swap atomically. |
| **BR-WRK-007** | Job lifecycle duy nhất là `DRAFT → REVIEW_PENDING → PUBLISHED ↔ PAUSED → CLOSED|EXPIRED|TAKEN_DOWN`; transition phải đúng quyền, version và audit. |
| **BR-WRK-008** | Mỗi candidate chỉ có một application cho một job. Idempotent replay trả application cũ; submit khác payload sau khi đã có application trả conflict. |
| **BR-WRK-009** | Application lifecycle là `SUBMITTED → UNDER_REVIEW → SHORTLISTED → INTERVIEWING → OFFERED → HIRED`, với terminal `REJECTED`, `WITHDRAWN`, `OFFER_DECLINED`; mọi transition ghi actor, thời điểm và reason bắt buộc khi reject. |
| **BR-WRK-010** | Candidate có thể chuyển `WITHDRAWN` từ `SUBMITTED`, `UNDER_REVIEW`, `SHORTLISTED` hoặc `INTERVIEWING`; ở `OFFERED`, từ chối của candidate phải là `OFFER_DECLINED`. Recruiter có thể `REJECTED` ở mọi trạng thái trước `HIRED`. Job đóng không tự đổi application đang xử lý. |
| **BR-WRK-011** | Khi apply, Work chụp bất biến job revision, career profile, CV và portfolio được chọn. Thay đổi hồ sơ/CV/job sau đó không sửa application snapshot. |
| **BR-WRK-012** | Invitation chỉ là lời mời có hạn; không tạo application, không cấp contact và không mở chat. Candidate phải chủ động submit application. |
| **BR-WRK-013** | Mỗi application có tối đa một conversation 1–1. Chỉ candidate và recruiter active được phân công tham gia; application terminal chuyển conversation sang `READ_ONLY`. |
| **BR-WRK-014** | REST history là nguồn sự thật của chat; WebSocket chỉ phân phối event. Client reconnect bằng cursor, message send idempotent và thứ tự chuẩn theo server sequence. |
| **BR-WRK-015** | Interview dùng immutable schedule versions. Candidate có thể confirm, decline hoặc yêu cầu đổi lịch; yêu cầu đổi lịch không sửa slot. Recruiter chấp nhận yêu cầu bằng cách tạo version `PROPOSED` mới; lịch nội bộ và ICS là nguồn V1, không khẳng định đã đồng bộ lịch ngoài. |
| **BR-WRK-016** | Recruiter/interviewer chỉ xem interview và phần hồ sơ được phân công. Feedback interviewer không tự đổi application status và không hiển thị cho candidate trừ phần được recruiter công bố. |
| **BR-WRK-017** | Sponsored profile/job luôn có nhãn, slot/rank riêng và trường `organicScore` không đổi. Payment không được tăng match score, ATS score hoặc quyền xem field riêng tư. |
| **BR-WRK-018** | Moderation takedown giữ revision, application và audit; chặn discovery/apply mới nhưng không xóa lịch sử tuyển dụng hợp pháp. |

### 7.4. Evidence khi ứng tuyển và tích hợp

| ID | Quy tắc |
|---|---|
| **BR-INT-001** | Identity, Study và Work dùng ba PostgreSQL vật lý riêng; không cross-database FK, join, shared write hoặc đọc trực tiếp database của nhau. |
| **BR-INT-002** | Tích hợp dùng contract versioned, signed service identity, transactional outbox và consumer idempotent theo event/request ID; delivery là at-least-once. |
| **BR-INT-003** | `platformUserId` UUID bất biến là khóa liên hệ; không dùng email hoặc local Study/Work ID làm integration key. |
| **BR-INT-004** | Apply wizard dùng access token đúng audience Study để learner chỉ liệt kê evidence của chính mình; token Work hoặc service token không được dùng để browse toàn bộ Study history. |
| **BR-INT-005** | Candidate chọn rõ từng evidence và consent version trước submit. Application transaction lưu selected ID, consent, export request và outbox; Study outage không rollback application. |
| **BR-INT-006** | Worker Work gửi signed export request. Study kiểm owner, `ISSUED`, source/version và revocation rồi chỉ trả snapshot tối thiểu; Work lưu snapshot gắn duy nhất với `applicationId`. |
| **BR-INT-007** | Evidence export state tại Work là `PENDING`, `READY`, `UNAVAILABLE`, `REVOKED` hoặc `HIDDEN`. `UNAVAILABLE`/timeout không được tự reject, hạ score hoặc ẩn application. |
| **BR-INT-008** | Consent withdrawal chuyển snapshot sang `HIDDEN`; Study revocation chuyển `REVOKED`. Nội dung không còn hiển thị cho recruiter nhưng audit tối thiểu được giữ theo retention. |
| **BR-INT-009** | Event duplicate/stale bị bỏ qua theo aggregate version; event gap vào retry/catch-up. Poison event vào DLQ và không được đánh dấu thành công giả. |

### 7.5. University

| ID | Quy tắc |
|---|---|
| **BR-UNI-001** | University là tenant độc lập với enterprise; affiliation do candidate chấp nhận, có trạng thái/thời hạn và không được suy ra chỉ từ email domain. |
| **BR-UNI-002** | Cohort/program membership không tự cấp quyền xem hồ sơ nghề nghiệp, application hoặc Study data; mỗi mục đích cần consent có scope và expiry. |
| **BR-UNI-003** | Campus distribution/referral không tạo application thay candidate và không chia sẻ evidence tự động. Candidate vẫn chọn job, snapshot và consent như apply thông thường. |
| **BR-UNI-004** | Báo cáo University mặc định aggregate và chỉ trả lát cắt có ít nhất 10 cá nhân; nhóm nhỏ trả trạng thái suppressed, không làm tròn để suy ngược. |
| **BR-UNI-005** | Khi consent hết hạn/thu hồi hoặc membership kết thúc, dữ liệu cá nhân biến mất khỏi màn University; aggregate đã khử định danh hợp lệ được giữ theo retention. |

### 7.6. Thanh toán và entitlement

| ID | Quy tắc |
|---|---|
| **BR-PAY-001** | V1 chỉ hỗ trợ gói/credit trả trước bằng VND qua VNPAY và MoMo cho Student hoặc Enterprise; số tiền là integer VND, không auto-renew. |
| **BR-PAY-002** | Hệ thống không thu/lưu PAN, CVV, tài khoản ngân hàng hoặc credential provider; không có ví nội bộ, escrow, payout hay số dư rút tiền. |
| **BR-PAY-003** | Order giữ immutable snapshot package, giá, thuế/giảm giá nếu có, buyer type/ID và policy version. Đổi catalog không sửa order cũ. |
| **BR-PAY-004** | Webhook/IPN đã xác thực chữ ký và đối chiếu merchant/order/amount/currency là nguồn xác nhận. Return URL không được cấp entitlement hoặc tự đánh dấu thanh toán thành công. |
| **BR-PAY-005** | Callback duplicate/out-of-order được lưu raw payload đã bảo vệ, xử lý idempotent và theo state precedence; late failure không hạ `SETTLED`. Amount/order mismatch vào review, không cấp quyền lợi. |
| **BR-PAY-006** | Chỉ `SETTLED` tạo entitlement/credit ledger đúng một lần trong cùng transaction. Entitlement không được âm; mọi consume/refund/expire là ledger append-only. |
| **BR-PAY-007** | Order chưa xác nhận quá thời hạn provider chuyển `EXPIRED`. `CANCELLED` chỉ được commit khi provider/chưa khởi tạo attempt xác nhận chưa thu tiền; verified success thắng trong cùng row lock. Callback success hợp lệ đến muộn được reconciliation xử lý và không cấp trùng. |
| **BR-PAY-008** | Refund chỉ do Finance Operator khởi tạo về provider gốc, không vượt settled amount trừ các refund trước. Hệ thống chỉ revoke phần entitlement chưa tiêu tương ứng; yêu cầu vượt giá trị chưa tiêu cần phê duyệt ngoại lệ và ghi debt/risk flag. |
| **BR-PAY-009** | Provider-confirmed chargeback đóng băng entitlement còn lại, đặt risk flag và tạo case Finance. Quyền lợi đã tiêu không bị xóa lịch sử; debt được theo dõi, không tự trừ order khác. |
| **BR-PAY-010** | Reconciliation chạy tự động hằng ngày và on-demand; sai lệch có severity, owner và audit. Không operator nào được sửa raw webhook hoặc ledger đã ghi. |

### 7.7. AI và sponsored product

| ID | Quy tắc |
|---|---|
| **BR-AIX-001** | AI chạy bất đồng bộ qua provider adapter; provider mặc định V1 là Ollama. Mỗi task pin provider, model version, prompt policy version, input hash và output schema version. |
| **BR-AIX-002** | AI chỉ tạo CV/JD draft, writing suggestion, match explanation và shortlist suggestion. Output không tự publish, gửi, apply, thay đổi ATS, reject, offer hoặc hire. |
| **BR-AIX-003** | Người dùng phải nhìn thấy nhãn AI, review và chủ động accept/edit/reject. Bản accept lưu nội dung người dùng xác nhận, không giả định AI đúng. |
| **BR-AIX-004** | Matching chỉ dùng skill, kinh nghiệm, học vấn công khai, tiêu chí job và preference nghề nghiệp được phép; loại gender, tuổi/ngày sinh, ảnh, dân tộc, tôn giáo, khuyết tật, tình trạng hôn nhân, địa chỉ chi tiết, payment và sponsored status. |
| **BR-AIX-005** | Raw file, contact, chat riêng, feedback mật và Study history chưa được chọn không gửi vào AI. Evidence chỉ dùng field cấu trúc đã consent cho application tương ứng. |
| **BR-AIX-006** | Input được giới hạn, phân tách khỏi system instruction và kiểm prompt injection; output phải qua schema validation, safety filter và không được thực thi như lệnh/tool call. |
| **BR-AIX-007** | Lỗi/timeout AI không chặn tạo/sửa CV, job, apply hoặc ATS thủ công. Retry có giới hạn; người dùng không bị trừ credit lần hai cho retry kỹ thuật cùng task. |
| **BR-AIX-008** | Model/prompt mới phải qua evaluation, bias/safety review và canary trước khi active. Rollback về version trước không sửa output lịch sử; mọi override có audit. |

### 7.8. Vận hành, audit và dữ liệu

| ID | Quy tắc |
|---|---|
| **BR-OPS-001** | Audit/security/payment webhook/ledger/application history/evidence snapshot/AI review/outbox là append-only; không cascade delete làm mất lịch sử. |
| **BR-OPS-002** | Audit chứa actor, effective role/tenant, action, resource, before/after đã redact, reason, IP/device tối thiểu, trace ID và thời điểm UTC; không chứa secret/token/raw password. |
| **BR-OPS-003** | Notification và side effect ngoài transaction được tạo qua outbox với dedupe key. Retry exponential có giới hạn; hết retry vào DLQ và cảnh báo. |
| **BR-OPS-004** | PII mã hóa khi truyền và khi lưu; object storage private theo namespace owner. Signed URL ngắn hạn, không được ghi vào audit/analytics/referrer. |
| **BR-OPS-005** | User export chỉ gồm dữ liệu của chính mình ở định dạng máy đọc được; tenant export phải qua permission, phạm vi và audit, không bypass consent. |
| **BR-OPS-006** | Account deletion có grace 30 ngày. Hết grace: revoke session/evidence/consent, xóa PII và private file không bị legal hold, hủy mapping và anonymize fact cần giữ. |
| **BR-OPS-007** | Legal hold chỉ do quyền được ủy quyền, có căn cứ, scope, expiry/review date và audit; hold tạm dừng xóa đúng record nhưng không khôi phục quyền hiển thị. |
| **BR-OPS-008** | Restore backup phải áp lại deletion/revocation ledger trước khi mở traffic để dữ liệu đã xóa/thu hồi không sống lại. |
| **BR-OPS-009** | Tất cả business timestamp lưu UTC, UUID cho identifier công khai; JSON camelCase, database snake_case. |
| **BR-OPS-010** | Mutation quan trọng dùng idempotency/optimistic version theo hợp đồng; conflict không silently overwrite và trả current version an toàn để client tải lại. |

### 7.9. Chính sách trusted publisher

- **Study:** chỉ nhân sự nội bộ/đối tác nội dung đã được định danh, hoàn tất đào tạo publishing, bật MFA và có local role `CONTENT_PUBLISHER` mới đủ điều kiện nhận grant. Grant nêu scope path/course, có hiệu lực tối đa 180 ngày và mặc định người publish phải khác người sửa version gần nhất. Trong bootstrap pilot, Platform Admin có thể cho phép cùng người khi ghi `bootstrapPilot`, lý do và pre-publish check độc lập; hành động được cảnh báo/audit.
- **Work:** enterprise phải `VERIFIED`; grantee là membership active có MFA. Grant chỉ được cấp khi tenant đã có ít nhất ba job revision được duyệt và không có vi phạm content/security đã xác nhận trong 90 ngày gần nhất; hiệu lực tối đa 180 ngày và chỉ trong đúng tenant/scope.
- **Kiểm tra không thể bỏ qua:** grant chỉ bỏ bước chờ manual review khi policy cho phép; rights/declaration, sanitization, malware scan, cấu trúc, prohibited-content check, tenant/account/entitlement và optimistic version vẫn bắt buộc trên từng lần publish.
- **Thu hồi:** suspend account/tenant, vi phạm nghiêm trọng, key compromise hoặc grant hết hạn làm mất quyền publish ngay. Thu hồi không xóa publication cũ; publication vi phạm đi qua takedown riêng. Chỉ `PERM-OPS-003` với recent MFA, separation-of-duties và reason mới được cấp/thu hồi grant.

## 8. State machine chuẩn

### 8.1. Identity và Study

| Aggregate | Chuyển trạng thái hợp lệ | Quy tắc bổ sung |
|---|---|---|
| Account | `PENDING_EMAIL_VERIFICATION → ACTIVE`; `ACTIVE ↔ SUSPENDED`; mọi trạng thái chưa terminal `→ DELETION_PENDING → ANONYMIZED` | Hủy deletion trong grace trở về trạng thái trước đó; `ANONYMIZED` terminal. Credential lock không phải account state. |
| Onboarding | `NOT_STARTED → IN_PROGRESS → COMPLETED` | Không chuyển lùi; recommendation có version/run riêng. |
| Content version | `DRAFT → PUBLISHED → SUPERSEDED`; `DRAFT → DISCARDED` | Published/superseded immutable. Stable entity có `ACTIVE → ARCHIVED`; archive không xóa version đang được tham chiếu. |
| Primary path period | Không có path `→ ACTIVE`; `ACTIVE → SWITCHED_OUT|COMPLETED|CANCELLED_BY_ADMIN` | Switch tạo `ACTIVE` mới trong cùng transaction; tối đa một active. |
| Course enrollment | `ENROLLED → IN_PROGRESS → COMPLETED` | Không chuyển lùi khi ôn tập; ẩn khỏi UI chỉ là preference. |
| Lesson progress | `NOT_STARTED → IN_PROGRESS → COMPLETED` | Monotonic; correction là event append-only. |
| File asset | `CREATED → UPLOADING → UPLOADED → SCANNING → CLEAN|INFECTED|SCAN_FAILED`; `CLEAN → ATTACHED`; trạng thái chưa dùng `→ EXPIRED`, hợp lệ `→ DELETED` theo retention | Chỉ `CLEAN` được attach/submit/download bởi reviewer. Scan failed retry tối đa ba lần. |
| Quiz attempt | `SUBMITTED → PASSED|FAILED` | Auto-grade; attempt sealed, không sửa. |
| Text/Link/File attempt | `SUBMITTED → UNDER_REVIEW → PASSED|NEEDS_REVISION|FAILED` | `NEEDS_REVISION`/`FAILED` cho phép attempt mới nếu còn quota. |
| Study evidence | `ISSUED → REVOKED` | Cả hai trạng thái giữ audit; issue lại tạo evidence ID/version mới. |

### 8.2. Work, University, payment và AI

| Aggregate | Chuyển trạng thái hợp lệ | Quy tắc bổ sung |
|---|---|---|
| Candidate visibility | `PRIVATE ↔ SEARCHABLE` | Opt-out đồng bộ index/cache tối đa 5 phút; không ảnh hưởng application snapshot. |
| Tenant verification | `PENDING_VERIFICATION → VERIFIED|REJECTED`; `VERIFIED ↔ SUSPENDED` | Submit lại sau reject tạo verification request/version mới, không sửa quyết định cũ. |
| Job | `DRAFT → REVIEW_PENDING → PUBLISHED`; `PUBLISHED ↔ PAUSED`; `PUBLISHED|PAUSED → CLOSED|EXPIRED|TAKEN_DOWN` | `CLOSED`, `EXPIRED`, `TAKEN_DOWN` terminal; revision mới không mở lại stable job terminal. |
| Invitation | `SENT → VIEWED → ACCEPTED|DECLINED|EXPIRED`; `SENT|VIEWED → CANCELLED` | `ACCEPTED` chỉ dẫn tới apply wizard, chưa tạo application/chat. |
| Application | `SUBMITTED → UNDER_REVIEW → SHORTLISTED → INTERVIEWING → OFFERED → HIRED`; từ `SUBMITTED|UNDER_REVIEW|SHORTLISTED|INTERVIEWING → REJECTED|WITHDRAWN`; từ `OFFERED → HIRED|REJECTED|OFFER_DECLINED` | `HIRED`, `REJECTED`, `WITHDRAWN`, `OFFER_DECLINED` terminal qua API thông thường; không nhảy cóc bước forward. |
| Evidence export | `PENDING → READY|UNAVAILABLE`; `READY → REVOKED|HIDDEN`; `UNAVAILABLE → PENDING` khi retry chủ động còn hạn consent | Hidden/revoked không hiển thị nội dung; audit còn giữ. |
| Interview | `PROPOSED → CONFIRMED → COMPLETED|NO_SHOW`; `PROPOSED|CONFIRMED → CANCELLED` | Candidate response `RESCHEDULE_REQUESTED` là event chờ xử lý, không là lifecycle state. Khi recruiter chấp nhận, tạo schedule version mới ở `PROPOSED` và supersede version cũ. |
| Conversation | `ACTIVE → READ_ONLY` | Chuyển khi application terminal; message cũ không sửa/xóa khỏi history ngoài quy trình moderation/redaction có audit. |
| University affiliation | `INVITED|REQUESTED → ACTIVE|DECLINED`; `ACTIVE → EXPIRED|REVOKED` | Candidate phải xác nhận; active không đồng nghĩa consent dữ liệu cá nhân. |
| Payment order orchestration | `CREATED → PENDING → SETTLED|FAILED|EXPIRED|CANCELLED` | `SETTLED` không bị rewrite bởi refund/chargeback; refund, chargeback và entitlement adjustment là case/ledger append-only riêng. Callback cũ không hạ state có precedence cao. |
| Entitlement | `ACTIVE → EXHAUSTED|EXPIRED|FROZEN|REVOKED`; `FROZEN → ACTIVE|REVOKED` | Ledger quyết định số dư; không auto-renew, không âm. |
| AI task | `QUEUED → RUNNING → SUCCEEDED|FAILED|CANCELLED` | Output review `DRAFT → ACCEPTED|EDITED_ACCEPT|REJECTED|EXPIRED`; chỉ human action tạo accepted/edited content và không tự tạo ATS action. |

## 9. Kiến trúc đích và công nghệ đã khóa

### 9.1. Topology triển khai

Study2Work gồm ba deployable backend độc lập và hai web application. Mỗi backend là modular monolith theo bounded context, có database/migration/pipeline riêng. Không tách microservice theo module trong V1.

| Khối | Thành phần và stack bắt buộc |
|---|---|
| Platform Identity | FastAPI, Python, SQLAlchemy, Alembic, PostgreSQL; Argon2id; JWT ES256/JWKS; worker email/security event. |
| Study Web | Vue 3, TypeScript, Vite, Tailwind CSS, Pinia cho client state, TanStack Query cho server state, Axios và Zod tại biên API. |
| Study Backend | FastAPI modular monolith, SQLAlchemy/Alembic, PostgreSQL, Redis, ARQ worker, S3/MinIO private object storage, ClamAV. |
| Work Web | React, TypeScript, Vite, Tailwind CSS, Zustand cho client state, TanStack Query, React Hook Form và Zod. |
| Work Backend | NestJS chạy Fastify, Prisma/PostgreSQL, Redis/BullMQ, WebSocket gateway, S3/MinIO private object storage. |
| Search | PostgreSQL full-text search + `pg_trgm`, index/materialized projection cục bộ; chưa dùng Elasticsearch/OpenSearch. |
| AI | Work worker gọi provider adapter; Ollama là provider mặc định pilot. Model server không được truy cập database trực tiếp. |
| Ngoại vi | Email provider, VNPAY, MoMo; mọi callback qua endpoint chuyên biệt, kiểm signature và lưu audit. |
| Quan sát | Structured log, metrics, distributed trace/trace ID, dashboard và alert theo SLO; không log secret/PII payload tùy tiện. |

Mỗi frontend chỉ gọi public API của Identity/Study/Work qua HTTPS. Internal endpoint không được expose bằng cùng route/public ingress. Redis, queue và object namespace tách theo subsystem; không dùng một cache entry làm nguồn sự thật xuyên domain.

### 9.2. Ranh giới module

| Deployable | Module nghiệp vụ |
|---|---|
| Identity | Registration/Verification, Credential, Session/MFA, Global RBAC, Account Lifecycle, Security Audit, Outbox. |
| Study | Identity Projection, Profile/Onboarding, Catalog/Publishing, Enrollment/Progress, Assessment/File Security, Evidence, Engagement/Support, Study RBAC/Audit/Reporting, Integration. |
| Work | Identity Projection, Career Profile/CV/Portfolio, Enterprise, University, Job/Sourcing, Application/ATS, Evidence Snapshot, Interview/Chat, AI/Matching, Billing/Entitlement/Promotion, File/Notification/Moderation/Audit, Integration. |

Module chỉ ghi bảng do mình sở hữu. Side effect sang module khác trong cùng deployable đi qua application service/domain event sau commit; repository không được gọi chéo tùy ý hoặc cập nhật bảng của module khác.

### 9.3. Quy ước API dùng chung

- Public API dùng `/api/v1`; service-to-service dùng `/internal/v1`; Identity công bố `/.well-known/jwks.json`.
- Host riêng: Identity, Study và Work có issuer/audience rõ ràng. Backend kiểm `iss`, `aud`, `exp`, `jti`, `sid`, `sub`, `authVersion`; không tin role/tenant ID do client tự thêm.
- JSON camelCase, UUID, ISO-8601 UTC. Response duy nhất gồm `success`, `businessCode`, `message`, `data`, `meta`, `traceId`.
- Page pagination dùng cho catalog/admin list ổn định; cursor pagination dùng cho chat, notification, audit/activity stream. Sort có tie-breaker ID để không mất/trùng bản ghi.
- `Idempotency-Key` bắt buộc cho register, enroll/switch, assessment submit/review, publish, apply, payment, interview mutation và chat send. Cùng key khác payload trả conflict.
- `If-Match`/version bắt buộc cho draft editor, publish review, ATS/interview update và các resource có nguy cơ ghi đồng thời.
- Business error dùng mã ổn định, HTTP status đúng ngữ nghĩa và message an toàn; validation không trả stack trace, SQL hoặc existence của resource ngoài quyền.
- WebSocket chỉ xác thực bằng token ngắn hạn do Work API cấp sau authorization; reconnect lấy history/cursor qua REST.

### 9.4. Versioning và compatibility

- Breaking HTTP/event/schema change tạo major version mới, chạy song song trong cửa sổ migration và có ngày ngừng hỗ trợ được công bố.
- Additive field là optional cho consumer cũ. Không đổi nghĩa enum hoặc tái sử dụng code; consumer phải xử lý enum chưa biết theo fallback an toàn.
- Published content, job revision, price/package snapshot, prompt policy, consent/terms và report definition đều lưu version được dùng tại thời điểm hành động.
- Migration database theo expand → backfill/dual-read nếu cần → switch → contract. Migration destructive không chạy cùng lần deploy bắt đầu dùng schema mới.

## 10. Ownership dữ liệu và tích hợp

### 10.1. Nguồn sự thật

| Dữ liệu | Owner duy nhất | Consumer và giới hạn |
|---|---|---|
| Email, credential, verification, session, MFA, global account/role | Identity DB | Study/Work nhận claim và projection tối thiểu; không giữ credential. |
| Learner profile, onboarding, path/course version, enrollment, progress, assessment, completion, evidence | Study DB | Work chỉ nhận evidence snapshot được chọn; University không đọc trực tiếp. |
| Career profile, CV, portfolio, enterprise/university, job, application, interview, chat | Work DB | Study không đọc ATS; University chỉ đọc Work data qua policy/consent trong cùng Work domain. |
| Payment order/transaction/webhook, entitlement, promotion | Work DB/Billing module | Identity không sở hữu billing; provider chỉ thấy field contract cần thiết. |
| Global skill code | Versioned taxonomy contract | Study và Work lưu projection theo `skillCode`; label có thể địa phương hóa. |
| File nhị phân | Namespace riêng của subsystem tạo file | Metadata/ACL nằm cùng subsystem; evidence export không chuyển bài làm gốc. |
| Audit/notification/outbox | Mỗi deployable tự sở hữu | Không service nào ghi trực tiếp audit/notification của service khác. |

### 10.2. Contract tích hợp

- Identity phát event đăng ký/xác minh/status/role/deletion. Study và Work upsert projection theo `platformUserId` và aggregate version; request đầu tiên có thể gọi reconcile nội bộ nếu projection chưa tồn tại.
- Study phát evidence issued/revoked và phục vụ export theo request cụ thể. Work không subscribe để xây kho evidence toàn cục; chỉ application có selected evidence mới tạo snapshot.
- Sự kiện có `eventId`, `eventType`, `schemaVersion`, `occurredAt`, `aggregateId`, `aggregateVersion`, `traceId` và payload tối thiểu; event được ký ES256/JWS bằng key quay vòng có `kid`.
- Internal request dùng service JWT ES256 có `aud`, scope, `jti`, TTL tối đa 5 phút; body hash/request ID chống replay. Production dùng TLS và network allowlist; secret/key nằm trong secret manager, không nằm trong database hay repository.
- Consumer ghi inbox/delivery record trước side effect, bỏ duplicate, phát hiện gap và retry/catch-up bằng cursor. Không xác nhận message trước khi local transaction commit.
- Không thực hiện distributed transaction. User-facing transaction commit dữ liệu owner + outbox; side effect eventual thể hiện trạng thái rõ ràng cho UI.

### 10.3. Hành vi khi dependency lỗi

| Dependency lỗi | Hành vi bắt buộc |
|---|---|
| Identity JWKS tạm lỗi | Dùng key cache còn hiệu lực trong thời gian quay vòng cho phép; không bỏ qua signature. Khi không xác minh được thì fail closed. |
| Identity projection chậm | Endpoint nhạy cảm fail closed hoặc reconcile nội bộ; catalog công khai vẫn hoạt động. |
| Study lỗi lúc apply | Application vẫn được tạo với evidence `PENDING`; worker retry, rồi `UNAVAILABLE` nếu hết cửa sổ. ATS thủ công vẫn dùng được. |
| Redis/queue lỗi | Nguồn sự thật PostgreSQL vẫn commit cùng outbox; worker bắt kịp sau phục hồi. Tính năng realtime/cache degrade, không ghi mất dữ liệu. |
| Object storage/ClamAV lỗi | Upload/scan ở pending/failed; không submit hoặc tải file chưa sạch. Các loại assessment khác vẫn hoạt động. |
| Payment provider timeout | Order ở `PENDING`; không cấp entitlement; query/reconciliation xác nhận sau. Client không tự retry tạo order khác nếu idempotency còn hiệu lực. |
| AI/Ollama lỗi | Task failed/retry; CV/JD/ATS thủ công vẫn dùng được và credit không bị tiêu hai lần. |
| WebSocket lỗi | Client dùng REST history/cursor và reconnect; gửi message chỉ báo thành công sau server acknowledgement/persist. |

## 11. Bảo mật, privacy, retention, payment và AI governance

### 11.1. Baseline bảo mật

- Password policy tối thiểu 12 ký tự, tối đa 128 ký tự, cho phép password manager/passphrase và kiểm danh sách password phổ biến/bị lộ; không ép đổi định kỳ nếu không có sự cố.
- Argon2id baseline: memory 64 MiB, time cost 3, parallelism 1; benchmark lại theo hạ tầng và rehash khi policy tăng. Raw password/token không log, cache hoặc gửi event.
- Refresh token đặt trong cookie `Secure`, `HttpOnly`, `SameSite=Lax`, scope Identity; access token chỉ giữ trong memory. Cookie mutation kiểm trusted `Origin` và CSRF token. CORS là allowlist, không wildcard với credential.
- TOTP secret mã hóa bằng key ngoài database; recovery code lưu hash. MFA enrollment/challenge/rate limit/audit độc lập và yêu cầu recent authentication cho thao tác nhạy cảm.
- Tenant isolation được kiểm bằng membership context ở service/repository và composite constraint. Test IDOR xuyên tenant bắt buộc cho mọi resource tenant.
- Dữ liệu rich text sanitize theo allowlist; CSP chặn inline script; URL do người dùng nhập được normalize/escape. Backend không render HTML thô từ CV/JD/chat.
- Upload đi vào quarantine, kiểm size/MIME thực/checksum/extension, scan ClamAV rồi mới chuyển private clean namespace. Download luôn authorize lại và dùng signed URL ngắn hạn.
- Rate limit, anomaly detection và audit áp dụng cho auth, candidate search, export, chat, payment, AI và admin. Secret, signing key và provider credential quay vòng qua secret manager.
- Dependency/container scan, SAST, migration review và security test là release gate. Lỗ hổng nghiêm trọng có biện pháp khắc phục hoặc chặn phát hành.

### 11.2. Privacy và consent

- Thu thập tối thiểu theo mục đích; form ghi rõ field bắt buộc/tùy chọn. Analytics không nhận raw CV/chat/evidence/contact.
- Candidate search consent, evidence export consent, University data consent, AI input consent và marketing preference là các bản ghi riêng; không gộp thành một checkbox chung.
- Consent lưu subject, controller/tenant, purpose, scope/resource IDs, policy version, granted/expired/revoked time và actor. Thu hồi ảnh hưởng truy cập tương lai nhưng không sửa audit hợp pháp.
- Recruiter chỉ thấy snapshot của application tenant mình và scope role; candidate search không phải đường tắt để xem CV/contact/evidence.
- University report áp threshold 10 sau mọi filter; không trả subtotal/total có thể trừ để suy ra nhóm nhỏ.
- Privacy export/delete chạy bất đồng bộ, có identity re-authentication, thông báo hoàn tất và signed download link ngắn hạn.

### 11.3. Retention mặc định

| Loại dữ liệu | Thời hạn | Xử lý hết hạn |
|---|---|---|
| Verification document của enterprise/university | 180 ngày sau quyết định cuối | Xóa file, giữ decision metadata/audit đã redact. |
| Notification và delivery detail | 180 ngày | Hard-delete payload; giữ aggregate không PII. |
| Learning/activity/search analytics event | 13 tháng | Xóa hoặc aggregate/ẩn danh; progress/completion còn hiệu lực được giữ theo account. |
| Application, chat và evidence snapshot | 12 tháng sau application terminal | Xóa/redact PII và file nếu không có legal hold; giữ aggregate/audit tối thiểu. |
| Identity security, authorization, admin, ATS, AI review audit | Tối thiểu 24 tháng | Xóa/redact theo policy và legal hold. |
| Payment order, transaction, webhook, ledger/refund/chargeback | Tối thiểu 24 tháng hoặc lâu hơn theo policy tài chính hiện hành | Giữ record tài chính cần thiết, mã hóa/redact payload dư thừa. |
| AI raw input/output kỹ thuật | 30 ngày | Xóa raw inference payload; accepted content theo owner domain, audit/hash/model version giữ 24 tháng. |
| Unverified account | 30 ngày từ đăng ký nếu không hoạt động | Xóa account/token/delivery theo batch có audit aggregate. |
| Expired/revoked one-time token và session | Token: 30 ngày; session: 90 ngày | Hard-delete hash/device detail không còn cần điều tra. |
| Orphan upload | 24 giờ | Xóa object/metadata; infected quarantine giữ tối đa 30 ngày để điều tra rồi xóa. |
| Delivered outbox/inbox | 30 ngày; failed/DLQ 90 ngày | Xóa payload sau khi bảo đảm không cần replay; giữ metric. |
| Backup | Tối đa 35 ngày | Tự hết hạn; restore phải áp deletion/revocation ledger. |
| Account deletion grace | 30 ngày | Sau grace thực hiện `BR-OPS-006`; legal hold chỉ giữ đúng scope. |

Retention tính từ thời điểm điều kiện bắt đầu, chạy bằng job có checkpoint, report số lượng và cảnh báo lỗi. Policy tài chính/pháp lý có thể kéo dài record cụ thể qua legal hold; không được dùng lý do đó để giữ toàn bộ dữ liệu ngoài scope.

### 11.4. Payment governance

- Adapter VNPAY dựa trên [tài liệu thanh toán chính thức của VNPAY](https://sandbox.vnpayment.vn/apis/docs/thanh-toan-pay/pay.html); adapter MoMo dựa trên [tài liệu One Time Payment chính thức của MoMo](https://developers.momo.vn/v3/docs/payment/api/credit/onetime/). Mỗi adapter cô lập cách ký, mã kết quả, query và refund nhưng ánh xạ về state/payment error canonical.
- Merchant credential tách sandbox/production. Callback xác thực signature trên raw canonical payload trước parse business; amount, order, merchant, currency và transaction ID phải khớp.
- Provider transaction có unique constraint theo provider + provider transaction ID; raw callback mã hóa, immutable và loại secret. Acknowledge đúng contract chỉ sau khi đã persist/đưa vào xử lý bền vững.
- Package catalog định nghĩa entitlement type, quantity, expiry và refund policy version. Mua không đồng nghĩa có tiền trong ví; entitlement chỉ dùng đúng sản phẩm/tenant đã mua.
- Finance operation áp dụng maker/checker cho refund ngoại lệ hoặc điều chỉnh debt; người khởi tạo không tự duyệt cùng case. Reconciliation report phân biệt provider missing, local missing, amount mismatch và state mismatch.

### 11.5. AI governance

- Registry chỉ cho phép model/prompt policy đã duyệt. Prompt template tách instruction khỏi dữ liệu người dùng, output JSON theo schema và lưu checksum/version để tái kiểm toán.
- Màn hình cho biết tính năng nào dùng AI, dữ liệu nào được gửi, credit dự kiến và cách từ chối. Không dùng input/output user cho huấn luyện provider nếu chưa có consent riêng.
- Match explanation phải nêu dữ kiện job/profile tạo ra gợi ý, mức thiếu dữ liệu và giới hạn; không trình bày score như xác suất được tuyển.
- Shortlist suggestion là một view phụ; danh sách recruiter mặc định vẫn có thể xem không qua AI. Accept suggestion chỉ ghi review action, recruiter còn phải chọn transition ATS.
- Đánh giá trước phát hành gồm correctness theo schema, groundedness, prompt-injection resistance, toxic content và chênh lệch kết quả giữa nhóm kiểm thử đại diện. Canary có kill switch và theo dõi acceptance/error/override, không theo dõi thuộc tính nhạy cảm production.
- Sponsored/payment signal bị loại khỏi input matching. AI Provider không được gọi API Work/Study, không giữ service credential và không phát event domain.

## 12. NFR, SLO và vận hành

| ID | Yêu cầu đo được |
|---|---|
| **NFR-OPS-001** | Hệ thống pilot hỗ trợ 5.000 account, 500 DAU và 50 RPS đỉnh trong 15 phút mà không vượt 80% connection pool/CPU kéo dài hoặc mất request đã acknowledge. |
| **NFR-OPS-002** | Availability theo tháng của Identity, Study core và Work core đạt ít nhất 99,0%; dependency ngoài được đo riêng nhưng hệ thống phải thể hiện degraded state an toàn. |
| **NFR-OPS-003** | p95 server latency: read đồng bộ ≤ 800 ms, mutation đồng bộ ≤ 1,5 giây; không tính phần việc đã công bố async. Query report lớn bắt buộc async/export. |
| **NFR-OPS-004** | Chat server acknowledgement sau khi persist p95 ≤ 2 giây; reconnect/history không mất hoặc nhân đôi message theo client key. |
| **NFR-OPS-005** | RPO toàn bộ PostgreSQL ≤ 15 phút; RTO cho Identity/Study/Work core ≤ 4 giờ. Restore drill thực hiện ít nhất mỗi quý trong pilot. |
| **NFR-OPS-006** | Outbox/event projection p95 ≤ 60 giây khi bình thường; evidence export p95 ≤ 2 phút. Backlog, oldest age, retry và DLQ có alert. |
| **NFR-OPS-007** | Candidate opt-out được kiểm end-to-end và đáp ứng hard limit 5 phút gồm DB projection, index, cache và active search response. |
| **NFR-OPS-008** | File scan p95 ≤ 2 phút cho file trong giới hạn V1 khi scanner khỏe; pending/failed luôn fail closed, có trạng thái và retry rõ ràng. |
| **NFR-OPS-009** | Mọi request có trace ID; mutation quan trọng liên kết audit/outbox/provider transaction. Log JSON có severity, service, environment và không chứa secret/PII payload. |
| **NFR-OPS-010** | Web đạt WCAG 2.2 AA cho luồng chính: keyboard, focus, label, contrast, error announcement và reduced motion; responsive từ 360 px, hỗ trợ hai phiên bản major mới nhất của Chrome, Edge, Firefox, Safari. |
| **NFR-OPS-011** | API/event/database migration và tài liệu phải pass contract/trace validator; không phát hành khi có reference mất, duplicate method+path hoặc enum/state mâu thuẫn. |
| **NFR-OPS-012** | Backup mã hóa, kiểm restore; secret quay vòng; high/critical security finding, cross-tenant leak hoặc payment integrity failure là release blocker. |

### 12.1. Chỉ số và cảnh báo tối thiểu

- Identity: login success/failure/lock, verification delivery, refresh reuse, MFA failure, revoked session và JWKS error.
- Study: enrollment/switch conflict, progress lag, assessment queue age, file scan state, publish failure, evidence outbox lag.
- Work: search opt-out lag, job/app transition conflict, apply rate, evidence export state, interview/chat acknowledgement và cross-tenant denial.
- Billing: order funnel theo provider, webhook signature failure, settlement lag, duplicate/mismatch, entitlement issue, refund/chargeback và reconciliation difference.
- AI: queue age, latency, schema/safety failure, retry, user accept/edit/reject và kill-switch state; không log nội dung nhạy cảm vào metric label.
- Alert P1: auth/signature bypass, cross-tenant/PII leak, payment cấp trùng/sai amount, mất dữ liệu đã acknowledge, RPO/RTO nguy cơ vi phạm. P2: SLO latency/availability, backlog/DLQ, scan/search opt-out vượt ngưỡng.

## 13. Rollout V1-PILOT

### 13.1. Thứ tự phát hành

1. **Foundation:** khóa OpenAPI/event/enum, dựng ba database, Identity/JWKS, tenant guard, outbox/inbox, audit, observability, backup/restore và CI quality gate.
2. **Study core:** catalog standalone, onboarding/primary path, content versioning, progress, assessment/file scan, evidence issuance và Study operations.
3. **Work core:** career profile/CV, enterprise/job, candidate opt-in/search, apply/ATS/evidence export, interview/chat và moderation.
4. **University + Billing:** tenant university/consent/report threshold, package/order, sandbox rồi production VNPAY/MoMo, entitlement/promotion và reconciliation.
5. **AI + sponsored:** AI shadow/evaluation, human-reviewed CV/JD, match explanation/shortlist suggestion, sponsored slot có nhãn; mở dần bằng entitlement/tenant allowlist.

Mỗi giai đoạn chỉ mở khi migration rollback/forward, access-control test, audit, dashboard/alert, runbook và acceptance tests liên quan đều pass. Feature flag có owner, expiry và trạng thái mặc định off cho payment production, AI và sponsored placement.

### 13.2. Pilot và migration dữ liệu cũ

- Pilot mở theo cohort/tenant allowlist, tăng 10% → 25% → 50% → 100% sau ít nhất một cửa sổ quan sát SLO cho mỗi mức; P1 hoặc integrity error lập tức dừng tăng và tắt feature liên quan.
- Prototype Express/EJS/MySQL của Work và schema BD cũ chỉ là nguồn tham khảo dữ liệu, không là kiến trúc đích. Không nhập plaintext password/hash không đạt chuẩn; account được xác minh lại email và đặt password mới trong Identity.
- Import, nếu có dữ liệu thật được phê duyệt, chạy qua staging, mapping ID hệ thống cũ riêng, checksum/count reconciliation, dry-run và báo cáo bản ghi lỗi. Dữ liệu tenant/application không đủ ownership/consent bị cách ly, không tự công khai.
- Published content cũ phải được đóng thành version bất biến trước khi enroll mới. Progress/import completion chỉ nhận khi ánh xạ chắc chắn tới exact version; trường hợp không xác định giữ lịch sử tham khảo nhưng không cấp completion/evidence.
- Payment production chỉ mở sau callback signature test, duplicate/out-of-order test, sandbox reconciliation và Finance runbook. AI chỉ mở sau evaluation/canary và có kill switch đã diễn tập.

### 13.3. Rollback và xử lý sự cố

- Deploy application backward-compatible trước migration; rollback code không rollback dữ liệu bằng lệnh destructive. State correction dùng audited compensating action.
- Có thể tắt riêng candidate index, evidence export worker, WebSocket, provider payment, sponsored slot hoặc AI mà Study learning/Work ATS thủ công vẫn hoạt động.
- Khi integrity/privacy incident: cô lập feature, giữ evidence/audit, thu hồi key/token nếu cần, xác định tenant/user bị ảnh hưởng, sửa bằng replay/compensation idempotent và ghi post-incident action.

## 14. Test chấp nhận bắt buộc

Mỗi test ID dưới đây là một test suite. Suite phải có dữ liệu chuẩn bị, happy path, alternate/failure path, kiểm tra record/audit/outbox và assertion không phát sinh side effect ngoài dự kiến. Test API contract, database constraint và UI state cùng dùng một test ID để truy vết.

### 14.1. Identity và Study

| ID | Kịch bản phải pass |
|---|---|
| **TC-IAM-001** | Register mới tạo pending user/hash/token/outbox một lần; replay cùng key trả cùng kết quả; email trùng/generic response, password yếu, agreement cũ, token sai/hết hạn/đã dùng không lộ account hoặc tạo session; verify hợp lệ chuyển `ACTIVE`. |
| **TC-IAM-002** | Login đúng/sai/locked/suspended/unverified; privileged user bắt buộc TOTP; refresh xoay thành công; hai refresh đồng thời chỉ một thành công và lần reuse thu hồi family; logout/logout-all, reset password, key rollover và token `authVersion` cũ đều bị chặn đúng. |
| **TC-IAM-003** | Admin thiếu permission/MFA, tự suspend, gỡ last admin hoặc stale `If-Match` bị chặn; suspend/role change hợp lệ thu hồi session, phát event; duplicate/stale event ở Study/Work không tạo projection sai; audit đã redact và có actor/reason. |
| **TC-STU-001** | Guest thấy đúng current published catalog; learner đã verify nhưng chưa onboarding vẫn enroll standalone; hai enroll đồng thời/replay chỉ có một enrollment; archived/unpublished version bị chặn; enrollment cũ vẫn mở đúng superseded pinned version. |
| **TC-STU-002** | Onboarding lưu/complete và recommendation version; chọn primary path khi chưa complete bị chặn; hai selection/switch đồng thời chỉ một `ACTIVE`; trước 168 giờ trả `nextAllowedAt`, đúng/sau mốc thành công; admin bypass cần quyền/MFA/reason và tạo cooldown mới. |
| **TC-STU-003** | Progress block/lesson monotonic khi request duplicate/out-of-order; client không ghi percent; completion/snapshot rebuild cho cùng kết quả; switch path không mất facts; course version mới không kế thừa completion version cũ; correction giữ fact gốc và có audit. |
| **TC-STU-004** | Quiz không lộ answer trước submit, auto-grade đúng và attempt sealed; text/link/file vào review; HTTP/non-HTTPS/link quá dài bị chặn và backend không fetch; file MIME spoof/infected/pending/scan-failed không submit/download; hai reviewer đồng thời chỉ một commit, resubmit tạo attempt mới. |
| **TC-STU-005** | Completion phát evidence đúng owner/source version; duplicate issue không nhân bản; revoke giữ history; learner token sai audience/owner không đọc được; export selected-only, version mismatch/revoked trả item lỗi an toàn; duplicate result/event không tạo snapshot trùng. |
| **TC-STU-006** | Author tạo draft và stale editor nhận conflict; thiếu rights, asset chưa clean, placement/rubric lỗi, publisher thiếu quyền/MFA hoặc check quá hạn không publish; hai publisher đồng thời chỉ một version thắng; swap current atomically, cache invalidated, enrollment cũ không đổi. |
| **TC-STU-007** | Notification dedupe/read cursor/preferences bắt buộc; community chưa accept/current rule stale/không eligible không nhận link; report/support duplicate, file bẩn và access người khác bị chặn; operator chỉ xem internal note đúng quyền; offline/retry không tạo ticket trùng. |
| **TC-STU-008** | Report aggregate đúng definition/freshness; support override/progress adjustment thiếu quyền/MFA/reason bị chặn; local role separation-of-duties và stale version được kiểm; audit search/export đúng scope; rebuild job không sửa source facts. |

### 14.2. Work, University, payment, AI và vận hành

| ID | Kịch bản phải pass |
|---|---|
| **TC-WRK-001** | Profile/CV/portfolio ownership, validation, stale edit và private file; publish tạo immutable revision; apply snapshot không đổi sau khi sửa/xóa nguồn; premium export chỉ tiêu entitlement một lần và hoàn reservation khi render lỗi. |
| **TC-WRK-002** | Profile mặc định private; opt-in cần consent/preview, search không trả contact/CV/evidence/sensitive field; cross-tenant public ID không dùng được; invitation không tạo application/chat; opt-out ẩn tức thì ở DB predicate và loại index/cache trong ≤5 phút kể cả worker retry. |
| **TC-WRK-003** | Tạo/xác minh enterprise, document bẩn, duplicate tax ID, owner tự verify, tenant chưa verified; member invite/role/last owner/stale version; toàn bộ IDOR đọc/ghi xuyên tenant trả not-found/denied và không tạo audit PII sai scope. |
| **TC-WRK-004** | Draft/revision validation, review và publish đúng quyền; trusted grant hết hạn/revoked vẫn bị chặn và không bypass policy; hai publish/pause/resume/close cạnh tranh chỉ một thắng; sửa published tạo revision mới, job terminal không nhận apply mới. |
| **TC-WRK-005** | Hai apply/replay cho cùng candidate/job chỉ một application; snapshot đúng revision; ATS transition hợp lệ/không hợp lệ, hai recruiter cạnh tranh, unassigned recruiter, reject thiếu reason và AI actor đều bị chặn; withdraw/offer decline/hire terminal; đóng job không tự đóng application. |
| **TC-WRK-006** | Apply với 0/nhiều evidence selected; Study sẵn sàng, timeout, retry, item revoked/version mismatch; application luôn tồn tại và ATS không đổi bởi export lỗi; result đến sau consent withdrawal vẫn hidden; revoke event ẩn mọi snapshot khớp, giữ audit và không tạo negative score. |
| **TC-WRK-007** | Interview chỉ cho application/member hợp lệ; UTC/timezone/end-before-start/participant khác tenant; confirm/decline/reschedule tạo version, stale schedule conflict; cancel/no-show trước giờ bị chặn; ICS sequence đúng và duplicate notification không gửi lặp. |
| **TC-WRK-008** | Chỉ candidate/recruiter assigned subscribe/send; conversation duy nhất; message key duplicate chỉ persist một lần, sequence tăng; reconnect từ cursor bù gap; WebSocket lỗi dùng REST; application terminal chuyển read-only, moderation tombstone không xóa audit. |
| **TC-WRK-009** | Template/AI/promotion kiểm entitlement và candidate consent; sponsored job/profile luôn có nhãn/slot riêng, organic score bit-for-bit không đổi; click/impression token giả/duplicate bị chặn; opt-out dừng profile promotion; hết credit/expiry/refund điều chỉnh không tạo số dư âm. |
| **TC-WRK-010** | Report nội dung, job review/takedown và kháng nghị đúng scope/version; takedown ẩn discovery/apply mới nhưng giữ application; moderator xuyên tenant chỉ qua platform permission; report aggregate/privacy filter và audit export không lộ raw CV/chat/evidence. |
| **TC-UNI-001** | University duplicate/verify/member role/last owner; affiliation chỉ active sau candidate accept, invitation sai người/hết hạn bị chặn; cohort chỉ nhận active affiliation, stale membership update conflict; enterprise membership không cấp quyền university. |
| **TC-UNI-002** | Program/partner scope/date validation; partnership phải hai bên chấp nhận; campus distribution chỉ job published và không auto-apply; referral cần consent `JOB_REFERRAL`, chỉ gửi thông báo/apply link, không mở chat/evidence. |
| **TC-UNI-003** | Consent purpose/expiry/revocation chặn individual view ngay; report từng filter có nhóm 9 bị suppress, nhóm 10 được aggregate; subtotal không suy ra nhóm nhỏ; University không đọc CV/chat/evidence; aggregate anonymized hợp lệ còn sau affiliation kết thúc. |
| **TC-PAY-001** | Giá/order snapshot do server tính bằng integer VND; buyer/tenant permission, stale price, provider timeout, retry và idempotency; return URL giả success không settle/cấp quyền; VNPAY/MoMo sandbox request ký đúng và không log credential. |
| **TC-PAY-002** | Signature sai, merchant/order/amount/currency mismatch, callback success duplicate/out-of-order/trước create response; chỉ verified settlement tạo một ledger và một entitlement; late failure không hạ settled; worker/DLQ/reconciliation phục hồi mà không cấp trùng. |
| **TC-PAY-003** | Refund vượt amount/đã tiêu, requester tự approve, stale review và provider fail; partial/full refund điều chỉnh phần chưa tiêu; chargeback freeze còn lại/risk case; daily reconciliation phát hiện local/provider missing/mismatch; ledger/raw webhook không sửa được. |
| **TC-AIX-001** | AI CV/JD chỉ nhận allowlisted input, prompt injection/schema/toxic output bị chặn; timeout/retry không trừ credit lặp; result là draft có provenance; accept/edit/reject cần human action và không tự sửa published CV/JD. |
| **TC-AIX-002** | Match/shortlist loại mọi protected/contact/payment/sponsored/evidence không consent field; job/application khác tenant bị chặn; suggestion có explanation/uncertainty; accept suggestion không đổi ATS; lỗi/disabled AI vẫn dùng ATS thủ công. |
| **TC-AIX-003** | Model/prompt thiếu exclusion/evaluation threshold không active; canary và kill switch dừng queued/new task, hoàn reservation; role/MFA/step-up và stale config; rollback dùng version cũ cho task mới nhưng không sửa provenance/output lịch sử. |
| **TC-OPS-001** | Moderation/job/verification/trusted grant kiểm maker-checker, self-review và tenant scope; break-glass cần ticket/approver hoặc SEV-1, hết hạn ≤60 phút; mọi access/action được alert/audit, không biến thành role vĩnh viễn. |
| **TC-OPS-002** | Export cần re-auth và chỉ dữ liệu owner; deletion request/cancel/grace/legal hold; sau 30 ngày PII/file/mapping bị xử lý đúng owner, evidence/consent revoked; restore backup áp deletion ledger; legal hold hết hạn tiếp tục deletion đúng scope. |
| **TC-OPS-003** | Load 50 RPS/500 DAU đạt latency/pool; kill Redis/worker/provider/AI/socket và phục hồi bằng outbox/retry/DLQ không mất dữ liệu; backup restore đạt RPO 15 phút/RTO 4 giờ; trace/audit liên kết; alert P1/P2 phát đúng. |

### 14.3. Điều kiện hoàn tất

- 100% `UC-*` có ít nhất một `TC-*`, API/table/screen và diagram hoặc lý do không cần diagram động.
- Test concurrency chạy với transaction thật; không thay bằng mock repository. Security suite bao gồm cross-tenant IDOR, privilege escalation, suspended account, token replay, signed URL hết hạn, malware/MIME spoof, XSS/SSRF và prompt injection.
- Failure suite chủ động ngắt Identity, Study, Redis, queue, object storage/scanner, payment provider, Ollama và WebSocket; dữ liệu đã acknowledge phải còn khôi phục được.
- Performance suite dùng dữ liệu gần cỡ pilot và báo p50/p95/p99, error rate, DB pool/lock, queue lag; pass theo toàn bộ `NFR-OPS-*`.
- Nghiệm thu chỉ đạt khi trace/Markdown/Mermaid validator, contract test, migration check và tất cả test ID liên quan đều pass; mọi ngoại lệ có owner, expiry và risk acceptance được phê duyệt.

## 15. Ma trận truy vết tổng

Ký hiệu `A–B` là dải ID liên tục, bao gồm cả hai đầu; các ID trong dải phải tồn tại tại tài liệu sở hữu. Cột “Quy tắc/quyền/NFR” nêu rule chi phối chính, không thay thế toàn bộ rule dùng chung. `N/A` chỉ được dùng kèm lý do cụ thể.

| Capability / Use case | Quy tắc, quyền, NFR chính | Activity / Sequence | Class / bảng nguồn sự thật | API / event chính | Màn hình chính | Test |
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
| `CAP-STU-007` / `UC-STU-007` | `BR-STU-017`, `PERM-STU-008`, `PERM-STU-012`, `BR-OPS-003` | N/A — các luồng notification/community/support độc lập, không có orchestration xuyên service | `CLS-STU-002`; `TBL-STU-042–048` | `API-STU-034–046` | `SCR-STU-020–022`, `SCR-OPS-014` | `TC-STU-007` |
| `CAP-STU-008` / `UC-STU-008` | `BR-STU-015`, `PERM-STU-009–014`, `BR-OPS-001–003` | `AC-OPS-001`, `SEQ-OPS-001` | `CLS-STU-001–002`; `TBL-STU-003–006`, `TBL-STU-049–050`, `TBL-STU-054` | `API-STU-047–050`, `API-STU-060`, `API-OPS-007–010` | `SCR-OPS-012–016`, `SCR-OPS-021`, `SCR-OPS-024` | `TC-STU-008` |
| `CAP-WRK-001` / `UC-WRK-001` | `BR-WRK-001`, `BR-WRK-011`, `BR-OPS-004`, `NFR-OPS-003` | `AC-WRK-001`, `SEQ-WRK-003` | `CLS-WRK-001`; `TBL-WRK-004–013`, `TBL-WRK-042` | `API-WRK-005–017`, `API-AIX-001` | `SCR-WRK-011–014` | `TC-WRK-001` |
| `CAP-WRK-002` / `UC-WRK-002` | `BR-WRK-001–003`, `BR-WRK-012`, `PERM-WRK-020–021`, `NFR-OPS-007` | `AC-WRK-001`, `SEQ-WRK-001` | `CLS-WRK-001`; `TBL-WRK-005`, `TBL-WRK-037–040` | `API-WRK-007`, `API-WRK-020–021`, `API-WRK-051–053`, `API-INT-010` | `SCR-WRK-012`, `SCR-WRK-016`, `SCR-WRK-036–038` | `TC-WRK-002` |
| `CAP-WRK-003` / `UC-WRK-003` | `BR-WRK-004–005`, `PERM-WRK-001–004`, `NFR-OPS-012` | N/A — CRUD tenant/membership được kiểm qua authorization và constraint, không có saga ngoài verification review | `CLS-WRK-001`; `TBL-WRK-014–018` | `API-WRK-035–041`, `API-OPS-001–002` | `SCR-WRK-030–032`, `SCR-OPS-017–018` | `TC-WRK-003` |
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
| `CAP-AIX-001` / `UC-AIX-001` | `BR-AIX-001–003`, `BR-AIX-005–007`, `PERM-AIX-001` chỉ áp dụng kill switch | `AC-AIX-001`, `SEQ-AIX-001` | `CLS-AIX-001`; `TBL-AIX-001–006`, `TBL-WRK-010–011`, `TBL-WRK-033` | `API-AIX-001–002`, `API-AIX-005–006`, `EVT-AIX-001` | `SCR-WRK-013`, `SCR-WRK-034` | `TC-AIX-001` |
| `CAP-AIX-002` / `UC-AIX-002` | `BR-AIX-002–007`, `PERM-WRK-070–071`, `NFR-OPS-006` | `AC-AIX-001`, `SEQ-AIX-001` | `CLS-AIX-001`; `TBL-AIX-004–007`, `TBL-WRK-041–042` | `API-AIX-003–006`, `EVT-AIX-001` | `SCR-WRK-039–040` | `TC-AIX-002` |
| `CAP-AIX-003` / `UC-AIX-003` | `BR-AIX-001`, `BR-AIX-008`, `PERM-AIX-001–003`, `NFR-OPS-012` | `AC-AIX-001`, `SEQ-AIX-001` | `CLS-AIX-001`; `TBL-AIX-001–003`, `TBL-AIX-006`, `TBL-AIX-008` | `API-AIX-007–010` | `SCR-OPS-022–023` | `TC-AIX-003` |
| `CAP-OPS-001` / `UC-OPS-001` | `BR-WRK-018`, `BR-OPS-001–002`, `PERM-OPS-001–003`, `PERM-OPS-005` | `AC-OPS-001`, `SEQ-OPS-001` | `CLS-WRK-002`; `TBL-WRK-015`, `TBL-WRK-020`, `TBL-WRK-035`, `TBL-WRK-060–061` | `API-OPS-001–009` | `SCR-OPS-009–011`, `SCR-OPS-017–018`, `SCR-OPS-024–025` | `TC-OPS-001` |
| `CAP-OPS-002` / `UC-OPS-002` | `BR-OPS-005–008`, `PERM-OPS-004`, `BR-IAM-007` | `AC-OPS-001`, `SEQ-OPS-001` | `CLS-IAM-001`, `CLS-INT-001`; `TBL-IAM-001`, `TBL-IAM-017–020`, `TBL-STU-050`, `TBL-WRK-061` | `API-IAM-019–020`, `EVT-IAM-004`, `API-INT-006–007` | `SCR-IAM-006`, `SCR-OPS-024–025` | `TC-OPS-002` |
| `CAP-OPS-003` / `UC-OPS-003` | `BR-INT-009`, `BR-OPS-003`, `BR-OPS-008`, `NFR-OPS-001–012` | `AC-OPS-001`, `SEQ-OPS-001` | `CLS-INT-001`; `TBL-IAM-018–020`, `TBL-STU-052–055`, `TBL-WRK-063–064`, `TBL-WRK-070` | `API-INT-001–010`, `API-OPS-010` | `SCR-OPS-021`; worker/alert/runbook là `SYSTEM` | `TC-OPS-003` |

## 16. Giả định và quyết định mặc định V1

- Pilot là triển khai tại Việt Nam, một region chính; mọi tiền tệ VND và giao diện đầu tiên tiếng Việt. Kiến trúc không phụ thuộc vào việc có production data cũ.
- Student và Candidate là hai persona của cùng `platformUserId`; không merge account tự động theo tên/phone/email phụ.
- Assessment file tối đa 25 MiB và allowlist PDF, PNG/JPEG, TXT/MD/CSV, ZIP; Work CV/file áp giới hạn chi tiết tại API nhưng luôn private + scan sạch.
- Interview meeting text có thể chứa địa chỉ hoặc link do recruiter nhập và được sanitize; hệ thống không tự tạo phòng họp V1.
- Chat V1 chỉ text/system message; thao tác “xóa” của user là tombstone có history, không hard-delete message đã là record tuyển dụng.
- Recommendation Study V1 là rule-based. AI chỉ nằm trong Work/TopCV/TopJD/matching và tuân thủ mục 11.5.
- PostgreSQL FTS/trigram đáp ứng search pilot; chỉ đề xuất search cluster/warehouse khi đo tải cho thấy không đạt NFR sau tối ưu query/index.
- External provider không quyết định account/ATS/entitlement trực tiếp. Mọi callback được ánh xạ, kiểm chứng và commit qua domain owner.

---

Tài liệu này hoàn tất khi năm tài liệu canonical cùng pass validator và ma trận trên không có reference mất. Mọi implementer phải giữ nguyên các quyết định đã khóa; thay đổi cần đi qua quy trình tại mục 1.2 thay vì tự chọn hành vi khác trong code.
