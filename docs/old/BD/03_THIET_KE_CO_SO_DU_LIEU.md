# Thiết kế cơ sở dữ liệu Study2Work V1-PILOT

## 1. Phạm vi và quyền sở hữu

Tài liệu này là nguồn định nghĩa duy nhất cho mô hình dữ liệu lô-gic và vật lý của V1-PILOT. Tài liệu mô tả cấu trúc cần được chuyển thành bản chuyển đổi lược đồ; không chứa DDL thực thi, dữ liệu khởi tạo, dữ liệu mẫu hoặc bí mật môi trường.

Hệ thống có đúng ba cụm PostgreSQL vật lý; mỗi cụm có người dùng kết nối, bản sao lưu, lịch sử chuyển đổi lược đồ và khóa mã hóa riêng:

| Cơ sở dữ liệu | Dịch vụ sở hữu | Dữ liệu sở hữu | Tuyệt đối không làm |
|---|---|---|---|
| `identity_db` | Dịch vụ Định danh nền tảng | danh tính, thông tin xác thực, MFA, phiên đăng nhập, mã thông báo, vai trò nền tảng, nhật ký kiểm toán bảo mật | Không lưu hồ sơ học tập, CV, đơn ứng tuyển hoặc thanh toán |
| `study_db` | Dịch vụ Học tập | hồ sơ học, nội dung có phiên bản, ghi danh/tiến độ, bài đánh giá, minh chứng học tập | Không xác thực mật khẩu và không truy vấn `identity_db` |
| `work_db` | Dịch vụ Việc làm | hồ sơ nghề nghiệp, tổ chức, việc làm/ATS, phỏng vấn/trò chuyện, trường đại học, AI, thanh toán | Không xác thực mật khẩu, không truy vấn trực tiếp minh chứng của Dịch vụ Học tập |

Không có khóa ngoại hoặc phép nối xuyên cơ sở dữ liệu. `identity_subject_id` trong Dịch vụ Học tập/Việc làm là UUID ngoài hệ thống được đồng bộ bằng sự kiện đã ký; `study_evidence_id` trong Dịch vụ Việc làm chỉ là tham chiếu yêu cầu xuất dữ liệu. Trao đổi liên dịch vụ sử dụng hộp thư đi, tải tin có chữ ký, bộ nhận xử lý lặp an toàn và bảng hộp thư đến.

## 2. Quy ước vật lý bắt buộc

### 2.1 Kiểu dữ liệu và thời gian

- ID nghiệp vụ dùng UUID v7 do ứng dụng sinh; không phụ thuộc phần mở rộng của cơ sở dữ liệu. ID từ hệ thống ngoài dùng `varchar` có giới hạn rõ.
- Thời gian dùng `timestamptz`, lưu UTC; ngày thuần túy dùng `date`; thời lượng dùng số giây `integer`.
- Tiền dùng `bigint` theo đơn vị VND, không dùng số dấu chấm động. Tỷ lệ/điểm dùng `numeric(p,s)` với ràng buộc kiểm tra miền giá trị.
- JSON chỉ dùng `jsonb` cho ảnh chụp dữ liệu/tải tin có phiên bản lược đồ; trường cần lọc, nối hoặc bảo đảm duy nhất phải tách thành cột.
- Thư điện tử được chuẩn hóa thành chữ thường và loại bỏ khoảng trắng Unicode; so sánh bằng khóa `email_normalized varchar(320)`, không phụ thuộc quy tắc đối chiếu.
- Chuỗi trạng thái dùng kiểu liệt kê PostgreSQL do bản chuyển đổi lược đồ quản lý. Việc thêm giá trị chỉ tiến về phía trước; đổi tên dùng quy trình mở rộng/thu hẹp.
- Mọi `*_at` có giá trị mặc định chỉ khi ghi trong định nghĩa. Không tự đặt giá trị mặc định cho thời điểm nghiệp vụ.

### 2.2 Tập cột chuẩn

Các tập dưới đây là một phần đầy đủ của định nghĩa bảng. Khi bảng ghi `ENTITY`, `IMMUTABLE`, `APPEND` hoặc `TENANT_ENTITY`, toàn bộ cột tương ứng bắt buộc tồn tại ngoài các cột riêng được liệt kê.

| Tập | Toàn bộ cột | Quy tắc |
|---|---|---|
| `ENTITY` | `id uuid NOT NULL` PK; `created_at timestamptz NOT NULL DEFAULT now()`; `updated_at timestamptz NOT NULL DEFAULT now()`; `row_version bigint NOT NULL DEFAULT 1` | khi cập nhật phải tăng `row_version`; API `If-Match` so với giá trị này |
| `TENANT_ENTITY` | toàn bộ `ENTITY`; `tenant_id uuid NOT NULL` | có `UNIQUE(tenant_id,id)`; mọi bảng con dùng khóa ngoại ghép chứa `tenant_id` |
| `IMMUTABLE` | `id uuid NOT NULL` PK; `created_at timestamptz NOT NULL DEFAULT now()` | tải tin đã đóng băng cấm sửa/xóa; chỉ siêu dữ liệu có chuyển trạng thái một chiều được bảng nêu rõ mới có thể cập nhật; sửa sai tạo bản ghi/phiên bản mới |
| `APPEND` | `id uuid NOT NULL` PK; `occurred_at timestamptz NOT NULL DEFAULT now()` | chỉ được thêm mới; phân vùng theo tháng khi bảng vượt 10 triệu dòng |

`deleted_at` không được ngầm hiểu. Chỉ bảng có ghi rõ cột này mới xóa mềm. Không dùng `ON DELETE CASCADE` với nhật ký kiểm toán, lịch sử, thanh toán, duyệt AI, ảnh chụp đơn ứng tuyển, ảnh chụp minh chứng, hộp thư đi/đến hoặc dữ liệu đang tạm giữ pháp lý. Khóa ngoại mặc định là `ON DELETE RESTRICT`; `SET NULL` chỉ khi được ghi rõ.

### 2.3 Phân loại dữ liệu

| Nhãn | Nội dung | Kiểm soát |
|---|---|---|
| `PUBLIC` | danh mục, việc làm đã xuất bản | được phép lưu đệm/đọc công khai |
| `INTERNAL` | cấu hình, trạng thái vận hành | vai trò theo nguyên tắc đặc quyền tối thiểu |
| `PII` | tên, thư điện tử, điện thoại, CV, trò chuyện, địa chỉ | mã hóa vùng lưu trữ/bản sao lưu, che dữ liệu trong nhật ký, không ghi dữ liệu gốc vào đo từ xa |
| `SENSITIVE` | thông tin xác thực, bí mật MFA, mã thông báo, tài liệu xác minh, chữ ký thanh toán | mã hóa phong bì ở tầng ứng dụng hoặc hàm băm một chiều; mọi truy cập đều được kiểm toán |
| `DERIVED_SENSITIVE` | AI/điểm phù hợp, ghi chú nhà tuyển dụng, kiểm duyệt | không xuất ra ngoài nếu không có chính sách/sự đồng ý |

## 3. Danh mục kiểu liệt kê chuẩn

Tên và giá trị dưới đây là chuẩn; API dùng đúng các giá trị chữ hoa này.

| Ngữ cảnh | Kiểu liệt kê | Giá trị |
|---|---|---|
| IAM | `account_status` | `PENDING_EMAIL_VERIFICATION`, `ACTIVE`, `SUSPENDED`, `DELETION_PENDING`, `ANONYMIZED` |
| IAM | `mfa_method_type` | `TOTP`, `RECOVERY_CODE` |
| IAM | `token_status` | `ACTIVE`, `CONSUMED`, `REVOKED`, `EXPIRED` |
| IAM | `session_status` | `ACTIVE`, `REVOKED`, `COMPROMISED`, `EXPIRED` |
| IAM | `audit_outcome` | `SUCCESS`, `DENIED`, `FAILURE` |
| STU | `content_version_status` | `DRAFT`, `PUBLISHED`, `SUPERSEDED`, `DISCARDED` |
| STU | `primary_path_status` | `ACTIVE`, `SWITCHED_OUT`, `COMPLETED`, `CANCELLED_BY_ADMIN` |
| STU | `enrollment_status` | `ENROLLED`, `IN_PROGRESS`, `COMPLETED` |
| STU | `progress_status` | `NOT_STARTED`, `IN_PROGRESS`, `COMPLETED` |
| STU | `assessment_type` | `QUIZ`, `TEXT`, `LINK`, `FILE` |
| STU | `attempt_status` | `SUBMITTED`, `UNDER_REVIEW`, `PASSED`, `NEEDS_REVISION`, `FAILED` |
| STU | `review_decision` | `PASSED`, `NEEDS_REVISION`, `FAILED` |
| STU/WRK | `file_asset_status` | `CREATED`, `UPLOADING`, `UPLOADED`, `SCANNING`, `CLEAN`, `INFECTED`, `SCAN_FAILED`, `ATTACHED`, `EXPIRED`, `DELETED` |
| STU | `evidence_status` | `ISSUED`, `REVOKED` |
| STU/WRK | `notification_status` | `QUEUED`, `SENT`, `DELIVERED`, `FAILED`, `SUPPRESSED` |
| WRK | `candidate_visibility` | `PRIVATE`, `SEARCHABLE` |
| WRK | `tenant_status` | `PENDING_VERIFICATION`, `VERIFIED`, `SUSPENDED`, `REJECTED`, `CLOSED` |
| WRK | `membership_status` | `INVITED`, `ACTIVE`, `SUSPENDED`, `LEFT`, `REVOKED` |
| WRK | `cv_revision_status` | `DRAFT`, `PUBLISHED`, `SUPERSEDED`, `DISCARDED` |
| WRK | `job_revision_status` | `DRAFT`, `REVIEW_PENDING`, `APPROVED`, `PUBLISHED`, `SUPERSEDED`, `REJECTED`, `DISCARDED` |
| WRK | `job_status` | `DRAFT`, `REVIEW_PENDING`, `PUBLISHED`, `PAUSED`, `CLOSED`, `EXPIRED`, `TAKEN_DOWN` |
| WRK | `application_status` | `SUBMITTED`, `UNDER_REVIEW`, `SHORTLISTED`, `INTERVIEWING`, `OFFERED`, `HIRED`, `REJECTED`, `WITHDRAWN`, `OFFER_DECLINED` |
| WRK | `interview_status` | `PROPOSED`, `CONFIRMED`, `CANCELLED`, `NO_SHOW`, `COMPLETED` |
| WRK | `conversation_status` | `ACTIVE`, `READ_ONLY` |
| WRK | `evidence_export_status` | `PENDING`, `READY`, `UNAVAILABLE`, `HIDDEN`, `REVOKED` |
| WRK | `ai_job_status` | `QUEUED`, `RUNNING`, `SUCCEEDED`, `FAILED`, `CANCELLED` |
| WRK | `ai_review_decision` | `ACCEPTED`, `EDITED_ACCEPT`, `REJECTED` |
| WRK | `ai_output_review_status` | `DRAFT`, `ACCEPTED`, `EDITED_ACCEPT`, `REJECTED`, `EXPIRED` |
| PAY | `order_status` | `CREATED`, `PENDING`, `SETTLED`, `FAILED`, `EXPIRED`, `CANCELLED` |
| PAY | `payment_status` | `CREATED`, `PENDING`, `SETTLED`, `FAILED`, `EXPIRED`, `CANCELLED` |
| PAY | `payment_provider` | `VNPAY`, `MOMO` |
| PAY | `entitlement_status` | `ACTIVE`, `EXHAUSTED`, `EXPIRED`, `FROZEN`, `REVOKED` |
| PAY | `ledger_entry_type` | `GRANT`, `SPEND`, `REFUND`, `EXPIRE`, `REVERSAL`, `ADJUSTMENT` |
| PAY | `promotion_status` | `SCHEDULED`, `ACTIVE`, `PAUSED`, `ENDED`, `CANCELLED` |
| UNI | `consent_status` | `ACTIVE`, `WITHDRAWN`, `EXPIRED` |
| OPS | `outbox_status` | `PENDING`, `PUBLISHED`, `FAILED`, `DEAD_LETTER` |

Không biến hành động hoặc thuộc tính hiển thị thành trạng thái vòng đời; mọi trạng thái hợp lệ phải nằm trong danh mục trên.

## 4. Cơ sở dữ liệu Định danh nền tảng (`identity_db`)

### 4.1 Danh tính, thông tin xác thực và xác minh

#### TBL-IAM-001 — `users`

- Tập cột: `ENTITY`.
- Cột riêng: `status account_status NOT NULL DEFAULT 'PENDING_EMAIL_VERIFICATION'`; `display_name varchar(120) NULL`; `locale varchar(10) NOT NULL DEFAULT 'vi-VN'`; `timezone varchar(64) NOT NULL DEFAULT 'Asia/Ho_Chi_Minh'`; `email_verified_at timestamptz NULL`; `suspended_at timestamptz NULL`; `suspension_reason varchar(500) NULL`; `deletion_requested_at timestamptz NULL`; `anonymized_at timestamptz NULL`; `privileged_mfa_required boolean NOT NULL DEFAULT false`.
- Ràng buộc: trạng thái `SUSPENDED` yêu cầu `suspended_at` và lý do; `ANONYMIZED` yêu cầu `anonymized_at`; tên hiển thị sau khi cắt khoảng trắng dài 1–120 nếu có giá trị.
- Chỉ mục: `(status, created_at DESC)`; chỉ mục một phần trên `(deletion_requested_at)` khi có giá trị.
- Dữ liệu: PII; giữ bản ghi định danh đã giả danh hóa vô thời hạn để bảo toàn khóa ngoại/kiểm toán.

#### TBL-IAM-002 — `user_emails`

- Tập cột: `ENTITY`.
- Cột riêng: `user_id uuid NOT NULL` FK `users.id`; `email_ciphertext bytea NOT NULL`; `email_normalized varchar(320) NOT NULL`; `is_primary boolean NOT NULL DEFAULT true`; `verified_at timestamptz NULL`; `replaced_at timestamptz NULL`.
- Ràng buộc: duy nhất toàn cục `email_normalized` khi `replaced_at IS NULL`; duy nhất một phần trên `(user_id)` khi `is_primary=true AND replaced_at IS NULL`; thư điện tử chuẩn phải khớp giá trị sau giải mã tại ranh giới ghi dữ liệu.
- Chỉ mục: `(user_id, replaced_at)`.
- Dữ liệu: PII; khi ẩn danh hóa, thay dữ liệu mã hóa và dữ liệu chuẩn hóa bằng bí danh không thể đảo ngược.

#### TBL-IAM-003 — `password_credentials`

- Tập cột: `ENTITY`.
- Cột riêng: `user_id uuid NOT NULL UNIQUE` FK `users.id`; `password_hash varchar(512) NOT NULL`; `algorithm varchar(32) NOT NULL DEFAULT 'ARGON2ID'`; `parameters jsonb NOT NULL`; `changed_at timestamptz NOT NULL`; `must_change boolean NOT NULL DEFAULT false`; `failed_count integer NOT NULL DEFAULT 0`; `locked_until timestamptz NULL`.
- Ràng buộc: `failed_count >= 0`; `algorithm='ARGON2ID'`; JSON chỉ chứa bộ nhớ/thời gian/song song/phiên bản, không chứa mật khẩu.
- Chỉ mục: duy nhất `user_id`; không lập chỉ mục hàm băm.
- Dữ liệu: SENSITIVE; không xóa mềm, việc đổi mật khẩu ghi vào nhật ký kiểm toán bảo mật.

#### TBL-IAM-004 — `email_verification_tokens`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `user_id uuid NOT NULL` FK `users.id`; `email_id uuid NOT NULL` FK `user_emails.id`; `purpose varchar(24) NOT NULL`; `token_hash char(64) NOT NULL UNIQUE`; `status token_status NOT NULL DEFAULT 'ACTIVE'`; `expires_at timestamptz NOT NULL`; `consumed_at timestamptz NULL`; `revoked_at timestamptz NULL`; `request_ip_hash char(64) NULL`.
- Ràng buộc: `expires_at>created_at`; dấu thời gian `consumed`/`revoked` phải phù hợp `status`. Việc đổi trạng thái do thủ tục có quyền bảo mật riêng thực hiện; về mặt quy tắc, bản ghi chỉ được thêm mới ngoài chuyển trạng thái một chiều.
- `purpose` chỉ nhận `REGISTER|CHANGE_EMAIL`; đổi thư điện tử chỉ nâng `user_emails.is_primary` sau khi xác minh và thu hồi địa chỉ thư điện tử chính cũ trong cùng giao dịch.
- Chỉ mục: `(user_id,status,expires_at DESC)`.
- Dữ liệu: SENSITIVE; dọn tải tin của mã thông báo sau 180 ngày, vẫn giữ kiểm toán.

#### TBL-IAM-005 — `password_reset_tokens`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `user_id uuid NOT NULL` FK `users.id`; `token_hash char(64) NOT NULL UNIQUE`; `status token_status NOT NULL DEFAULT 'ACTIVE'`; `expires_at timestamptz NOT NULL`; `consumed_at timestamptz NULL`; `revoked_at timestamptz NULL`; `session_epoch bigint NOT NULL`; `request_ip_hash char(64) NULL`.
- Ràng buộc/chỉ mục/thời hạn lưu giữ: như `email_verification_tokens`; đặt lại thành công sẽ thu hồi mọi mã làm mới có thế hệ phiên cũ trong cùng giao dịch.

### 4.2 MFA, phiên đăng nhập và mã thông báo

#### TBL-IAM-006 — `mfa_methods`

- Tập cột: `ENTITY`.
- Cột riêng: `user_id uuid NOT NULL` FK `users.id`; `type mfa_method_type NOT NULL`; `label varchar(80) NULL`; `secret_ciphertext bytea NULL`; `verified_at timestamptz NULL`; `disabled_at timestamptz NULL`.
- Ràng buộc: TOTP yêu cầu bí mật được mã hóa; mã khôi phục chỉ là phương thức thử thách dự phòng và hàm băm thực tế nằm ở `TBL-IAM-007`, không lưu mã gốc tại đây; duy nhất một phần trên `(user_id,type)` khi chưa bị vô hiệu hóa.
- Chỉ mục: `(user_id,disabled_at)`.
- Dữ liệu: SENSITIVE; chỉ xóa cứng sau khi tài khoản được ẩn danh hóa và hết thời gian tạm giữ pháp lý.

#### TBL-IAM-007 — `mfa_recovery_codes`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `method_id uuid NOT NULL` FK `mfa_methods.id`; `code_hash char(64) NOT NULL UNIQUE`; `consumed_at timestamptz NULL`; `batch_id uuid NOT NULL`.
- Ràng buộc: chỉ mã chưa dùng mới được dùng một lần; cập nhật duy nhất được phép là đặt `consumed_at` theo một chiều.
- Chỉ mục: `(method_id,consumed_at)`; SENSITIVE.

#### TBL-IAM-008 — `mfa_challenges`

- Tập cột: `ENTITY`.
- Cột riêng: `user_id uuid NOT NULL` FK `users.id`; `session_id uuid NULL`; `purpose varchar(32) NOT NULL`; `challenge_hash char(64) NOT NULL UNIQUE`; `expires_at timestamptz NOT NULL`; `attempt_count integer NOT NULL DEFAULT 0`; `max_attempts integer NOT NULL DEFAULT 5`; `verified_at timestamptz NULL`; `invalidated_at timestamptz NULL`.
- Ràng buộc: `expires_at>created_at`, `0<=attempt_count<=max_attempts`; hoàn tất theo một chiều.
- Chỉ mục: `(user_id,purpose,expires_at DESC)`; dọn sau 180 ngày.

#### TBL-IAM-009 — `auth_sessions`

- Tập cột: `ENTITY`.
- Cột riêng: `user_id uuid NOT NULL` FK `users.id`; `status session_status NOT NULL DEFAULT 'ACTIVE'`; `session_epoch bigint NOT NULL`; `device_id_hash char(64) NULL`; `device_name varchar(120) NULL`; `ip_hash char(64) NULL`; `user_agent_hash char(64) NULL`; `last_seen_at timestamptz NOT NULL`; `expires_at timestamptz NOT NULL`; `revoked_at timestamptz NULL`; `revoke_reason varchar(100) NULL`.
- Ràng buộc: `expires_at>created_at`; trạng thái thu hồi/xâm phạm yêu cầu `revoked_at`; không lưu IP/tác nhân người dùng gốc.
- Chỉ mục: `(user_id,status,last_seen_at DESC)`; chỉ mục một phần trên `(expires_at)` khi `ACTIVE`.
- Thời hạn lưu giữ: 24 tháng cho điều tra bảo mật, sau đó xóa/băm sâu hơn theo quy định tạm giữ pháp lý.

#### TBL-IAM-010 — `refresh_tokens`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `session_id uuid NOT NULL` FK `auth_sessions.id`; `family_id uuid NOT NULL`; `parent_token_id uuid NULL` self-FK; `token_hash char(64) NOT NULL UNIQUE`; `status token_status NOT NULL DEFAULT 'ACTIVE'`; `issued_at timestamptz NOT NULL`; `expires_at timestamptz NOT NULL`; `rotated_to_id uuid NULL` self-FK; `consumed_at timestamptz NULL`; `reuse_detected_at timestamptz NULL`.
- Ràng buộc: một mã thông báo chỉ có một bản con; duy nhất một phần trên `parent_token_id` khi có giá trị; `expires_at>issued_at`; chuyển trạng thái một chiều bằng thủ tục. Khi phát hiện dùng lại, khóa cả họ mã thông báo và phiên trong cùng giao dịch.
- Chỉ mục: `(family_id,status)`; `(session_id,issued_at DESC)`; `(expires_at)`.
- Dữ liệu: chỉ lưu hàm băm mã thông báo; giữ 24 tháng sau khi hết hạn.

#### TBL-IAM-011 — `signing_keys`

- Tập cột: `ENTITY`.
- Cột riêng: `kid varchar(80) NOT NULL UNIQUE`; `algorithm varchar(16) NOT NULL DEFAULT 'ES256'`; `public_jwk jsonb NOT NULL`; `private_key_ref varchar(300) NOT NULL`; `not_before timestamptz NOT NULL`; `not_after timestamptz NOT NULL`; `activated_at timestamptz NULL`; `retired_at timestamptz NULL`.
- Ràng buộc: chỉ `ES256`; `not_after>not_before`; vật liệu khóa riêng chỉ là tham chiếu KMS/Vault.
- Chỉ mục: `(activated_at,retired_at)`; JWK công khai là INTERNAL, tham chiếu khóa là SENSITIVE.

### 4.3 Kiểm soát truy cập theo vai trò của nền tảng

#### TBL-IAM-012 — `roles`

- Tập cột: `ENTITY`.
- Cột riêng: `code varchar(80) NOT NULL UNIQUE`; `name varchar(120) NOT NULL`; `description varchar(500) NOT NULL`; `is_privileged boolean NOT NULL DEFAULT false`; `is_system boolean NOT NULL DEFAULT true`; `disabled_at timestamptz NULL`.
- Ràng buộc: mã chữ hoa dạng `^[A-Z][A-Z0-9_]{1,79}$`; vai trò hệ thống không đổi mã hoặc xóa cứng.
- Chỉ mục: `(disabled_at,code)`.

#### TBL-IAM-013 — `permissions`

- Tập cột: `ENTITY`.
- Cột riêng: `code varchar(120) NOT NULL UNIQUE`; `service varchar(20) NOT NULL`; `description varchar(500) NOT NULL`; `risk_level smallint NOT NULL DEFAULT 1`.
- Ràng buộc: `service IN ('IDENTITY','STUDY','WORK')`; `risk_level BETWEEN 1 AND 5`.
- Chỉ mục: `(service,code)`.

#### TBL-IAM-014 — `role_permissions`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `role_id uuid NOT NULL` FK `roles.id`; `permission_id uuid NOT NULL` FK `permissions.id`; `granted_by uuid NOT NULL` FK `users.id`; `revoked_at timestamptz NULL`; `revoked_by uuid NULL` FK `users.id`.
- Ràng buộc: duy nhất một phần trên `(role_id,permission_id)` khi `revoked_at IS NULL`; `revoked_by` là bắt buộc khi đã thu hồi.
- Chỉ mục: `(permission_id,revoked_at)`.

#### TBL-IAM-015 — `user_role_assignments`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `user_id uuid NOT NULL` FK `users.id`; `role_id uuid NOT NULL` FK `roles.id`; `scope_type varchar(24) NOT NULL DEFAULT 'PLATFORM'`; `scope_id uuid NULL`; `valid_from timestamptz NOT NULL DEFAULT now()`; `valid_until timestamptz NULL`; `granted_by uuid NOT NULL` FK `users.id`; `revoked_at timestamptz NULL`; `revoked_by uuid NULL` FK `users.id`; `reason varchar(500) NOT NULL`.
- Ràng buộc: `valid_until>valid_from` nếu có; phạm vi `PLATFORM` yêu cầu `scope_id` không có giá trị; duy nhất một phần trên `(user_id,role_id,scope_type,scope_id)` khi còn hiệu lực; việc gán vai trò đặc quyền yêu cầu MFA ở tầng dịch vụ.
- Chỉ mục: `(user_id,revoked_at,valid_until)`; `(scope_type,scope_id,revoked_at)`.

### 4.4 Độ tin cậy và kiểm toán Định danh

#### TBL-IAM-016 — `idempotency_keys`

- Tập cột: `ENTITY`.
- Cột riêng: `actor_id uuid NULL`; `operation varchar(120) NOT NULL`; `key_hash char(64) NOT NULL`; `request_hash char(64) NOT NULL`; `response_status integer NULL`; `response_body jsonb NULL`; `locked_until timestamptz NULL`; `completed_at timestamptz NULL`; `expires_at timestamptz NOT NULL`.
- Ràng buộc: duy nhất `(actor_id,operation,key_hash)`; cùng khóa nhưng khác hàm băm yêu cầu trả xung đột; phản hồi phải được che dữ liệu.
- Chỉ mục: `(expires_at)`; dọn sau 24 giờ, riêng đăng ký giữ 7 ngày.

#### TBL-IAM-017 — `security_audit_events`

- Tập cột: `APPEND`.
- Cột riêng: `actor_id uuid NULL`; `subject_id uuid NULL`; `action varchar(120) NOT NULL`; `outcome audit_outcome NOT NULL`; `reason_code varchar(80) NULL`; `trace_id varchar(64) NOT NULL`; `session_id uuid NULL`; `ip_hash char(64) NULL`; `user_agent_hash char(64) NULL`; `metadata jsonb NOT NULL DEFAULT '{}'`; `prev_hash char(64) NULL`; `event_hash char(64) NOT NULL UNIQUE`; `legal_hold_until timestamptz NULL`.
- Ràng buộc: hàm băm sự kiện tính từ tải tin chuẩn và `prev_hash`; từ chối/thất bại yêu cầu mã lý do; siêu dữ liệu qua lược đồ/che dữ liệu.
- Chỉ mục: `(subject_id,occurred_at DESC)`; `(actor_id,occurred_at DESC)`; `(trace_id)`; BRIN `(occurred_at)`.
- Thời hạn lưu giữ: tối thiểu 24 tháng; chuỗi hàm băm phát hiện sửa đổi; không xóa dây chuyền.

#### TBL-IAM-018 — `outbox_events`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `aggregate_type varchar(80) NOT NULL`; `aggregate_id uuid NOT NULL`; `event_type varchar(120) NOT NULL`; `event_version integer NOT NULL`; `payload jsonb NOT NULL`; `available_at timestamptz NOT NULL DEFAULT now()`; `dedupe_key varchar(180) NOT NULL UNIQUE`; `trace_id varchar(64) NOT NULL`.
- Ràng buộc: `event_version>=1`; tải tin không chứa thông tin xác thực/mã thông báo gốc; toàn bộ hàng chỉ được thêm mới và không chứa trạng thái giao nhận có thể sửa.
- Chỉ mục: `(available_at,id)`; `(aggregate_type,aggregate_id,created_at)`.
- Thời hạn lưu giữ: 24 tháng; trạng thái xuất bản được suy ra từ lần thử ở bảng kế tiếp.

#### TBL-IAM-019 — `consumer_inbox`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `consumer varchar(100) NOT NULL`; `event_id uuid NOT NULL`; `event_type varchar(120) NOT NULL`; `payload_hash char(64) NOT NULL`; `received_at timestamptz NOT NULL DEFAULT now()`; `processed_at timestamptz NULL`; `result_code varchar(80) NULL`; `trace_id varchar(64) NOT NULL`.
- Ràng buộc: duy nhất `(consumer,event_id)`; cùng sự kiện nhưng khác hàm băm tải tin là lỗi bảo mật.
- Chỉ mục: `(consumer,processed_at,received_at)`; giữ 24 tháng.

#### TBL-IAM-020 — `outbox_delivery_attempts`

- Tập cột: `APPEND`.
- Cột riêng: `outbox_event_id uuid NOT NULL` FK `outbox_events.id`; `attempt_no integer NOT NULL`; `status outbox_status NOT NULL`; `worker_id varchar(120) NOT NULL`; `broker_message_id varchar(180) NULL`; `error_code varchar(80) NULL`; `next_retry_at timestamptz NULL`; `payload_hash char(64) NOT NULL`.
- Ràng buộc: duy nhất `(outbox_event_id,attempt_no)`; `attempt>=1`; `status` không dùng `PENDING`, sự kiện chưa có lần thử là đang chờ; `PUBLISHED` là trạng thái kết thúc; `DEAD_LETTER` chỉ xuất hiện sau chính sách thử lại.
- Chỉ mục: `(outbox_event_id,attempt_no DESC)`; `(status,next_retry_at,occurred_at)`; chỉ được thêm mới trong 24 tháng.

## 5. Cơ sở dữ liệu Học tập (`study_db`)

### 5.1 Bản chiếu danh tính, hồ sơ và kiểm soát truy cập cục bộ theo vai trò

#### TBL-STU-001 — `identity_projections`

- Tập cột: `ENTITY`.
- Cột riêng: `identity_subject_id uuid NOT NULL UNIQUE`; `account_status account_status NOT NULL`; `email_verified boolean NOT NULL DEFAULT false`; `display_name varchar(120) NULL`; `identity_version bigint NOT NULL`; `last_event_id uuid NOT NULL UNIQUE`; `projected_at timestamptz NOT NULL`.
- Ràng buộc: `identity_version>=1`; đây không phải khóa ngoại sang Dịch vụ Định danh.
- Chỉ mục: `(account_status)`; PII tối thiểu, cập nhật lặp an toàn theo phiên bản.

#### TBL-STU-002 — `learner_profiles`

- Tập cột: `ENTITY`.
- Cột riêng: `identity_subject_id uuid NOT NULL UNIQUE`; `full_name varchar(160) NULL`; `avatar_file_id uuid NULL`; `headline varchar(200) NULL`; `bio varchar(2000) NULL`; `birth_year smallint NULL`; `city_code varchar(20) NULL`; `onboarding_completed_at timestamptz NULL`; `profile_visibility varchar(20) NOT NULL DEFAULT 'PRIVATE'`; `deleted_at timestamptz NULL`.
- Ràng buộc: năm sinh hợp lý từ 1900 đến năm hiện tại trừ 13; `visibility` là `PRIVATE|PLATFORM`; khóa ngoại ảnh đại diện được kiểm tra trì hoãn tới bảng tệp, chỉ nhận tệp `CLEAN`.
- Chỉ mục: `(onboarding_completed_at)`; `(deleted_at)`; PII.

#### TBL-STU-003 — `service_roles`

- Tập cột: `ENTITY`.
- Cột riêng: `code varchar(80) NOT NULL UNIQUE`; `name varchar(120) NOT NULL`; `description varchar(500) NOT NULL`; `is_privileged boolean NOT NULL DEFAULT false`; `disabled_at timestamptz NULL`.
- Ràng buộc: mã chữ hoa ổn định; không cấp vai trò đặc quyền khi JWT thiếu trường xác nhận MFA.
- Chỉ mục: `(disabled_at,code)`.

#### TBL-STU-004 — `service_permissions`

- Tập cột: `ENTITY`.
- Cột riêng: `code varchar(120) NOT NULL UNIQUE`; `description varchar(500) NOT NULL`; `risk_level smallint NOT NULL DEFAULT 1`.
- Ràng buộc: `risk_level BETWEEN 1 AND 5`.
- Chỉ mục: `(risk_level,code)`.

#### TBL-STU-005 — `service_role_permissions`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `role_id uuid NOT NULL` FK `service_roles.id`; `permission_id uuid NOT NULL` FK `service_permissions.id`; `granted_by_subject_id uuid NOT NULL`; `revoked_at timestamptz NULL`; `revoked_by_subject_id uuid NULL`.
- Ràng buộc: duy nhất một phần trên `(role_id,permission_id)` khi còn hiệu lực; thu hồi yêu cầu chủ thể thực hiện.
- Chỉ mục: `(role_id,revoked_at)`; `(permission_id,revoked_at)`.

#### TBL-STU-006 — `service_role_assignments`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `identity_subject_id uuid NOT NULL`; `role_id uuid NOT NULL` FK `service_roles.id`; `valid_from timestamptz NOT NULL DEFAULT now()`; `valid_until timestamptz NULL`; `granted_by_subject_id uuid NOT NULL`; `reason varchar(500) NOT NULL`; `revoked_at timestamptz NULL`; `revoked_by_subject_id uuid NULL`.
- Ràng buộc: duy nhất khi còn hiệu lực trên `(identity_subject_id,role_id)`; thời hạn hợp lệ; quyền truy cập đặc quyền được đối chiếu trường xác nhận MFA từ JWT.
- Chỉ mục: `(identity_subject_id,revoked_at,valid_until)`.

### 5.2 Thiết lập ban đầu và gợi ý lộ trình

#### TBL-STU-007 — `onboarding_submissions`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `learner_id uuid NOT NULL` FK `learner_profiles.id`; `schema_version integer NOT NULL`; `answers jsonb NOT NULL`; `submitted_at timestamptz NOT NULL`; `supersedes_id uuid NULL` self-FK; `is_current boolean NOT NULL DEFAULT true`.
- Ràng buộc: `schema_version>=1`; duy nhất một phần trên `(learner_id)` khi là bản hiện hành; JSON được kiểm tra tại API theo phiên bản lược đồ.
- Chỉ mục: `(learner_id,submitted_at DESC)`; PII; giữ 13 tháng sau khi thay thế rồi tổng hợp/ẩn danh hóa.

#### TBL-STU-008 — `path_recommendation_runs`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `learner_id uuid NOT NULL` FK `learner_profiles.id`; `onboarding_submission_id uuid NOT NULL` FK `onboarding_submissions.id`; `algorithm_version varchar(40) NOT NULL`; `input_snapshot jsonb NOT NULL`; `ranked_path_version_ids uuid[] NOT NULL`; `reason_snapshot jsonb NOT NULL`; `generated_at timestamptz NOT NULL`; `expires_at timestamptz NOT NULL`.
- Ràng buộc: mảng không rỗng, không trùng ID; hết hạn sau khi sinh.
- Chỉ mục: `(learner_id,generated_at DESC)`; DERIVED_SENSITIVE; giữ 13 tháng.

### 5.3 Nội dung có phiên bản bất biến

#### TBL-STU-009 — `learning_paths`

- Tập cột: `ENTITY`.
- Cột riêng: `slug varchar(120) NOT NULL UNIQUE`; `owner_subject_id uuid NOT NULL`; `current_draft_version_id uuid NULL`; `latest_published_version_id uuid NULL`; `archived_at timestamptz NULL`.
- Ràng buộc: hai con trỏ nếu có phải trỏ đến phiên bản cùng lộ trình; con trỏ đã xuất bản chỉ trỏ `PUBLISHED`; giá trị `slug` dùng chữ thường và dấu gạch nối.
- Chỉ mục: `(archived_at,updated_at DESC)`.

#### TBL-STU-010 — `learning_path_versions`

- Tập cột: `ENTITY`; được sửa bằng `row_version` khi `DRAFT`, bị khóa bất biến từ lúc gửi duyệt/xuất bản.
- Cột riêng: `path_id uuid NOT NULL` FK `learning_paths.id`; `version_no integer NOT NULL`; `status content_version_status NOT NULL DEFAULT 'DRAFT'`; `title varchar(200) NOT NULL`; `summary varchar(1000) NOT NULL`; `description_markdown text NOT NULL`; `estimated_hours integer NOT NULL`; `cover_file_id uuid NULL`; `content_hash char(64) NOT NULL`; `created_by_subject_id uuid NOT NULL`; `published_at timestamptz NULL`; `superseded_at timestamptz NULL`; `discarded_at timestamptz NULL`; `source_version_id uuid NULL` self-FK.
- Ràng buộc: duy nhất `(path_id,version_no)`; `version_no>=1`; thời lượng 1–10000 giờ; bản đã xuất bản yêu cầu `published_at` và `content_hash`. Sau `PUBLISHED`, cơ chế kích hoạt của cơ sở dữ liệu từ chối sửa mọi cột.
- Chỉ mục: `(path_id,status,version_no DESC)`; `(status,published_at DESC)`.

#### TBL-STU-011 — `courses`

- Tập cột: `ENTITY`.
- Cột riêng: `slug varchar(120) NOT NULL UNIQUE`; `owner_subject_id uuid NOT NULL`; `current_draft_version_id uuid NULL`; `latest_published_version_id uuid NULL`; `archived_at timestamptz NULL`.
- Ràng buộc: hai con trỏ nếu có phải trỏ đến phiên bản cùng khóa học; con trỏ đã xuất bản chỉ trỏ `PUBLISHED`; giá trị `slug` dùng chữ thường và dấu gạch nối.
- Chỉ mục: `(archived_at,updated_at DESC)`.

#### TBL-STU-012 — `course_versions`

- Tập cột: `ENTITY`; được sửa bằng `row_version` khi `DRAFT`, bị khóa bất biến từ lúc gửi duyệt/xuất bản.
- Cột riêng: `course_id uuid NOT NULL` FK `courses.id`; `version_no integer NOT NULL`; `status content_version_status NOT NULL DEFAULT 'DRAFT'`; `title varchar(200) NOT NULL`; `summary varchar(1000) NOT NULL`; `description_markdown text NOT NULL`; `level varchar(24) NOT NULL`; `estimated_minutes integer NOT NULL`; `thumbnail_file_id uuid NULL`; `content_hash char(64) NOT NULL`; `created_by_subject_id uuid NOT NULL`; `published_at timestamptz NULL`; `superseded_at timestamptz NULL`; `discarded_at timestamptz NULL`; `source_version_id uuid NULL` self-FK.
- Ràng buộc: duy nhất `(course_id,version_no)`; `level` là `BEGINNER|INTERMEDIATE|ADVANCED`; thời lượng 1–600000 phút; bất biến khi đã xuất bản.
- Chỉ mục: `(course_id,status,version_no DESC)`; biểu thức tìm kiếm toàn văn GIN trên tiêu đề/tóm tắt cho danh mục; `(status,published_at DESC)`.

#### TBL-STU-013 — `path_course_items`

- Tập cột: `ENTITY`; chỉ sửa khi phiên bản lộ trình cha còn `DRAFT`, bất biến sau khi gửi duyệt.
- Cột riêng: `path_version_id uuid NOT NULL` FK `learning_path_versions.id`; `course_version_id uuid NOT NULL` FK `course_versions.id`; `position integer NOT NULL`; `is_required boolean NOT NULL DEFAULT true`; `unlock_rule jsonb NOT NULL DEFAULT '{}'`.
- Ràng buộc: duy nhất `(path_version_id,position)` và `(path_version_id,course_version_id)`; `position>=1`; hai phiên bản phải `PUBLISHED` trước khi xuất bản lộ trình.
- Chỉ mục: `(course_version_id,path_version_id)`.

#### TBL-STU-014 — `chapters`

- Tập cột: `ENTITY`; chỉ sửa khi phiên bản khóa học cha còn `DRAFT`, bất biến sau khi gửi duyệt.
- Cột riêng: `course_version_id uuid NOT NULL` FK `course_versions.id`; `title varchar(200) NOT NULL`; `summary varchar(1000) NULL`; `position integer NOT NULL`.
- Ràng buộc: duy nhất `(course_version_id,position)`; `position>=1`; thừa hưởng tính bất biến của phiên bản khóa học.
- Chỉ mục: `(course_version_id,position)`.

#### TBL-STU-015 — `lessons`

- Tập cột: `ENTITY`; chỉ sửa khi phiên bản khóa học cha còn `DRAFT`, bất biến sau khi gửi duyệt.
- Cột riêng: `chapter_id uuid NOT NULL` FK `chapters.id`; `course_version_id uuid NOT NULL` FK `course_versions.id`; `title varchar(200) NOT NULL`; `summary varchar(1000) NULL`; `position integer NOT NULL`; `estimated_minutes integer NOT NULL`; `is_preview boolean NOT NULL DEFAULT false`.
- Ràng buộc: tính toàn vẹn ghép bảo đảm chương thuộc cùng phiên bản khóa học; duy nhất `(chapter_id,position)`; thời lượng 1–1440 phút.
- Chỉ mục: `(course_version_id,chapter_id,position)`.

#### TBL-STU-016 — `content_blocks`

- Tập cột: `ENTITY`; chỉ sửa khi phiên bản khóa học cha còn `DRAFT`, bất biến sau khi gửi duyệt.
- Cột riêng: `lesson_id uuid NOT NULL` FK `lessons.id`; `block_type varchar(24) NOT NULL`; `position integer NOT NULL`; `content_json jsonb NOT NULL`; `plain_text text NULL`; `estimated_seconds integer NOT NULL DEFAULT 0`; `content_hash char(64) NOT NULL`.
- Ràng buộc: `block_type` là `MARKDOWN|VIDEO|IMAGE|EMBED|DOWNLOAD`; duy nhất `(lesson_id,position)`; số giây >=0; HTML/Markdown đã được làm sạch; nội dung nhúng ngoài theo danh sách cho phép.
- Chỉ mục: `(lesson_id,position)`; tìm kiếm toàn văn GIN trên `plain_text` chỉ dành cho tìm kiếm quản trị.

#### TBL-STU-017 — `content_rights_attestations`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `resource_type varchar(24) NOT NULL`; `resource_version_id uuid NOT NULL`; `publisher_subject_id uuid NOT NULL`; `rights_basis varchar(40) NOT NULL`; `source_url varchar(2048) NULL`; `license_code varchar(80) NULL`; `attestation_text_hash char(64) NOT NULL`; `attested_at timestamptz NOT NULL`; `expires_at timestamptz NULL`; `revoked_at timestamptz NULL`.
- Ràng buộc: `resource_type` là `PATH_VERSION|COURSE_VERSION`; căn cứ quyền thuộc `OWNED|LICENSED|OPEN_LICENSE|AUTHORIZED`; hết hạn sau khi xác nhận.
- Chỉ mục: `(resource_type,resource_version_id,revoked_at)`; giữ theo vòng đời nội dung và kiểm toán.

#### TBL-STU-018 — `content_review_decisions`

- Tập cột: `APPEND`.
- Cột riêng: `resource_type varchar(24) NOT NULL`; `resource_version_id uuid NOT NULL`; `reviewer_subject_id uuid NOT NULL`; `decision varchar(24) NOT NULL`; `reason_codes varchar(80)[] NOT NULL`; `comment varchar(2000) NULL`; `expected_row_version bigint NOT NULL`; `trace_id varchar(64) NOT NULL`.
- Ràng buộc: `decision` là `APPROVE|REJECT|REQUEST_CHANGES`; lý do bắt buộc khi không phê duyệt; một vòng duyệt được chốt bằng khóa lạc quan của tài nguyên.
- Chỉ mục: `(resource_type,resource_version_id,occurred_at DESC)`; thời hạn lưu giữ kiểm toán tối thiểu 24 tháng.

#### TBL-STU-019 — `trusted_publisher_grants`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `publisher_subject_id uuid NOT NULL`; `scope varchar(24) NOT NULL`; `valid_from timestamptz NOT NULL`; `valid_until timestamptz NOT NULL`; `granted_by_subject_id uuid NOT NULL`; `grant_reason varchar(1000) NOT NULL`; `eligibility_snapshot jsonb NOT NULL`; `revoked_at timestamptz NULL`; `revoked_by_subject_id uuid NULL`; `revoke_reason varchar(1000) NULL`.
- Ràng buộc: `scope` là `STUDY_CONTENT`; `valid_until>valid_from`; duy nhất một phần theo người xuất bản/phạm vi khi còn hiệu lực. Người xuất bản đáng tin cậy vẫn phải đáp ứng quyền nội dung, làm sạch, quét và kiểm toán.
- Chỉ mục: `(publisher_subject_id,scope,revoked_at,valid_until)`.

### 5.4 Bài đánh giá và thang chấm điểm

#### TBL-STU-020 — `assessments`

- Tập cột: `ENTITY`; chỉ sửa khi phiên bản khóa học cha còn `DRAFT`, bất biến sau khi gửi duyệt.
- Cột riêng: `course_version_id uuid NOT NULL` FK `course_versions.id`; `type assessment_type NOT NULL`; `title varchar(200) NOT NULL`; `instructions_markdown text NOT NULL`; `max_attempts integer NULL`; `passing_score numeric(5,2) NULL`; `due_rule jsonb NULL`; `content_hash char(64) NOT NULL`.
- Ràng buộc: số lượt làm tối đa không có giá trị hoặc nằm trong khoảng 1–100; điểm 0–100; `QUIZ` yêu cầu điểm đạt; bản cha đã xuất bản làm bài đánh giá bất biến.
- Chỉ mục: `(course_version_id,type)`.

#### TBL-STU-021 — `assessment_placements`

- Tập cột: `ENTITY`; chỉ sửa khi phiên bản chứa vị trí đặt còn `DRAFT`, bất biến sau khi gửi duyệt.
- Cột riêng: `assessment_id uuid NOT NULL` FK `assessments.id`; `path_version_id uuid NULL` FK `learning_path_versions.id`; `course_version_id uuid NULL` FK `course_versions.id`; `chapter_id uuid NULL` FK `chapters.id`; `lesson_id uuid NULL` FK `lessons.id`; `position integer NOT NULL`; `is_required boolean NOT NULL DEFAULT true`.
- Ràng buộc: kiểm tra chính xác một trong bốn ID phạm vi có giá trị; duy nhất `(assessment_id)` để một bài tập có đúng một vị trí đặt; `position>=1`; phạm vi và bài đánh giá phải cùng cây phiên bản.
- Chỉ mục: chỉ mục một phần theo từng phạm vi với `(scope_id,position)`.

#### TBL-STU-022 — `quiz_questions`

- Tập cột: `ENTITY`; chỉ sửa khi phiên bản khóa học cha còn `DRAFT`, bất biến sau khi gửi duyệt.
- Cột riêng: `assessment_id uuid NOT NULL` FK `assessments.id`; `question_type varchar(24) NOT NULL`; `prompt_markdown text NOT NULL`; `explanation_markdown text NULL`; `position integer NOT NULL`; `points numeric(7,2) NOT NULL`; `shuffle_options boolean NOT NULL DEFAULT false`.
- Ràng buộc: `question_type` là `SINGLE_CHOICE|MULTIPLE_CHOICE|TRUE_FALSE`; duy nhất `(assessment_id,position)`; điểm >0.
- Chỉ mục: `(assessment_id,position)`.

#### TBL-STU-023 — `quiz_options`

- Tập cột: `ENTITY`; chỉ sửa khi phiên bản khóa học cha còn `DRAFT`, bất biến sau khi gửi duyệt.
- Cột riêng: `question_id uuid NOT NULL` FK `quiz_questions.id`; `label_markdown text NOT NULL`; `position integer NOT NULL`; `is_correct boolean NOT NULL`; `weight numeric(7,4) NOT NULL DEFAULT 1`.
- Ràng buộc: duy nhất `(question_id,position)`; trọng số 0–1; mỗi câu hỏi phải có ít nhất một đáp án đúng, được kiểm tra khi xuất bản.
- Chỉ mục: `(question_id,position)`; `is_correct` không trả về người học trước khi gửi bài.

#### TBL-STU-024 — `rubrics`

- Tập cột: `ENTITY`; chỉ sửa khi phiên bản khóa học cha còn `DRAFT`, bất biến sau khi gửi duyệt.
- Cột riêng: `assessment_id uuid NOT NULL UNIQUE` FK `assessments.id`; `title varchar(200) NOT NULL`; `total_points numeric(7,2) NOT NULL`; `passing_points numeric(7,2) NOT NULL`; `version_no integer NOT NULL DEFAULT 1`.
- Ràng buộc: `0<passing<=total`; chỉ dùng cho `TEXT|LINK|FILE`; thang chấm điểm bất biến theo phiên bản bài đánh giá.
- Chỉ mục: duy nhất `assessment_id`.

#### TBL-STU-025 — `rubric_criteria`

- Tập cột: `ENTITY`; chỉ sửa khi phiên bản khóa học cha còn `DRAFT`, bất biến sau khi gửi duyệt.
- Cột riêng: `rubric_id uuid NOT NULL` FK `rubrics.id`; `name varchar(160) NOT NULL`; `description varchar(1000) NOT NULL`; `max_points numeric(7,2) NOT NULL`; `position integer NOT NULL`.
- Ràng buộc: duy nhất `(rubric_id,position)`; `max_points>0`; tổng tiêu chí bằng tổng điểm được kiểm khi xuất bản.
- Chỉ mục: `(rubric_id,position)`.

### 5.5 Ghi danh, dữ kiện tiến độ và hoàn thành

#### TBL-STU-026 — `primary_path_periods`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `learner_id uuid NOT NULL` FK `learner_profiles.id`; `path_version_id uuid NOT NULL` FK `learning_path_versions.id`; `status primary_path_status NOT NULL`; `started_at timestamptz NOT NULL`; `ended_at timestamptz NULL`; `end_reason varchar(80) NULL`; `supersedes_period_id uuid NULL` self-FK; `switch_request_id uuid NULL`; `selected_from_recommendation_id uuid NULL` FK `path_recommendation_runs.id`.
- Ràng buộc: ràng buộc loại trừ/duy nhất một phần bảo đảm đúng một hàng `ACTIVE` cho mỗi người học; dấu thời gian kết thúc bắt buộc nếu không còn hiệu lực; phiên bản phải `PUBLISHED`; người học tự đổi lộ trình cách lần kích hoạt gần nhất ít nhất 168 giờ.
- Chỉ mục: `(learner_id,started_at DESC)`; `(path_version_id,status)`.

#### TBL-STU-027 — `course_enrollments`

- Tập cột: `ENTITY`.
- Cột riêng: `learner_id uuid NOT NULL` FK `learner_profiles.id`; `course_version_id uuid NOT NULL` FK `course_versions.id`; `source_type varchar(24) NOT NULL`; `source_path_period_id uuid NULL` FK `primary_path_periods.id`; `status enrollment_status NOT NULL DEFAULT 'ENROLLED'`; `enrolled_at timestamptz NOT NULL`; `first_started_at timestamptz NULL`; `completed_at timestamptz NULL`; `last_activity_at timestamptz NULL`; `hidden_from_my_courses_at timestamptz NULL`.
- Ràng buộc: duy nhất `(learner_id,course_version_id)`; `source_type` là `STANDALONE|PRIMARY_PATH|ADMIN`; nguồn từ lộ trình yêu cầu một kỳ lộ trình; dấu thời gian hoàn thành theo `status`.
- Chỉ mục: `(learner_id,status,last_activity_at DESC)`; `(course_version_id,status)`.

#### TBL-STU-028 — `block_progress_facts`

- Tập cột: `ENTITY`.
- Cột riêng: `enrollment_id uuid NOT NULL` FK `course_enrollments.id`; `block_id uuid NOT NULL` FK `content_blocks.id`; `status progress_status NOT NULL DEFAULT 'NOT_STARTED'`; `first_started_at timestamptz NULL`; `completed_at timestamptz NULL`; `last_position_seconds integer NULL`; `last_event_id uuid NOT NULL UNIQUE`.
- Ràng buộc: duy nhất `(enrollment_id,block_id)`; vị trí >=0; khối nội dung thuộc đúng phiên bản khóa học của lần ghi danh; trạng thái chỉ tiến tới trừ khi quản trị viên hiệu chỉnh có kiểm toán.
- Chỉ mục: `(enrollment_id,status)`; `(block_id,status)`.

#### TBL-STU-029 — `lesson_progress_facts`

- Tập cột: `ENTITY`.
- Cột riêng: `enrollment_id uuid NOT NULL` FK `course_enrollments.id`; `lesson_id uuid NOT NULL` FK `lessons.id`; `status progress_status NOT NULL DEFAULT 'NOT_STARTED'`; `first_started_at timestamptz NULL`; `completed_at timestamptz NULL`; `completion_source varchar(24) NULL`.
- Ràng buộc: duy nhất `(enrollment_id,lesson_id)`; bài học thuộc đúng phiên bản khóa học; `completion_source` là `BLOCKS|ASSESSMENT|ADMIN` khi đã hoàn thành.
- Chỉ mục: `(enrollment_id,status)`.

#### TBL-STU-030 — `progress_snapshots`

- Tập cột: `ENTITY`.
- Cột riêng: `learner_id uuid NOT NULL` FK `learner_profiles.id`; `scope_type varchar(24) NOT NULL`; `scope_id uuid NOT NULL`; `completed_units integer NOT NULL`; `total_units integer NOT NULL`; `percent numeric(5,2) NOT NULL`; `source_high_watermark timestamptz NOT NULL`; `rebuilt_at timestamptz NOT NULL`; `calculation_version integer NOT NULL`.
- Ràng buộc: duy nhất `(learner_id,scope_type,scope_id)`; `scope_type` là `COURSE_VERSION|PATH_VERSION`; các số đếm >=0, đã hoàn thành <= tổng số, phần trăm 0–100. Đây là bộ nhớ đệm có thể dựng lại, không phải nguồn dữ liệu gốc.
- Chỉ mục: `(scope_type,scope_id,percent)`; `(learner_id,rebuilt_at DESC)`.

#### TBL-STU-031 — `course_completions`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `learner_id uuid NOT NULL` FK `learner_profiles.id`; `course_version_id uuid NOT NULL` FK `course_versions.id`; `enrollment_id uuid NOT NULL UNIQUE` FK `course_enrollments.id`; `completed_at timestamptz NOT NULL`; `rule_version integer NOT NULL`; `facts_hash char(64) NOT NULL`; `revoked_at timestamptz NULL`; `revocation_reason varchar(500) NULL`.
- Ràng buộc: duy nhất `(learner_id,course_version_id)`; chỉ tái sử dụng kết quả hoàn thành đúng cùng `course_version_id`; thu hồi không xóa lịch sử.
- Chỉ mục: `(learner_id,completed_at DESC)`; `(course_version_id,completed_at)`.

#### TBL-STU-032 — `path_completions`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `learner_id uuid NOT NULL` FK `learner_profiles.id`; `path_version_id uuid NOT NULL` FK `learning_path_versions.id`; `primary_path_period_id uuid NOT NULL` FK `primary_path_periods.id`; `completed_at timestamptz NOT NULL`; `rule_version integer NOT NULL`; `course_completion_ids uuid[] NOT NULL`; `facts_hash char(64) NOT NULL`; `revoked_at timestamptz NULL`; `revocation_reason varchar(500) NULL`.
- Ràng buộc: duy nhất `(learner_id,path_version_id,primary_path_period_id)`; mảng phải đủ các khóa học bắt buộc và không trùng.
- Chỉ mục: `(learner_id,completed_at DESC)`.

### 5.6 Lượt làm bài, quét tệp và chấm duyệt

#### TBL-STU-033 — `assessment_attempts`

- Tập cột: `ENTITY`.
- Cột riêng: `learner_id uuid NOT NULL` FK `learner_profiles.id`; `enrollment_id uuid NOT NULL` FK `course_enrollments.id`; `assessment_id uuid NOT NULL` FK `assessments.id`; `attempt_no integer NOT NULL`; `status attempt_status NOT NULL DEFAULT 'SUBMITTED'`; `submitted_payload_snapshot jsonb NOT NULL`; `submitted_at timestamptz NOT NULL`; `auto_score numeric(7,2) NULL`; `final_score numeric(7,2) NULL`; `graded_at timestamptz NULL`; `grader_subject_id uuid NULL`; `content_hash char(64) NOT NULL`.
- Ràng buộc: duy nhất `(learner_id,assessment_id,attempt_no)`; `attempt_no>=1`; ảnh chụp dữ liệu/hàm băm bài nộp bất biến ngay khi chèn; điểm không âm và không vượt tổng thang chấm/bài trắc nghiệm; người học/lần ghi danh/bài đánh giá phải cùng phiên bản khóa học. `QUIZ` chuyển đồng bộ `SUBMITTED→PASSED|FAILED`; `TEXT|LINK|FILE` chuyển `SUBMITTED→UNDER_REVIEW→PASSED|NEEDS_REVISION|FAILED`.
- Chỉ mục: `(learner_id,assessment_id,attempt_no DESC)`; `(status,submitted_at)` cho hàng đợi chấm duyệt.
- Xử lý đồng thời: việc nộp bài khóa cặp người học–bài đánh giá và lần ghi danh, cấp `attempt_no`, sao chép rồi niêm phong/xóa liên kết bản nháp trong cùng giao dịch; cơ chế khóa lặp ngăn hai lần nộp. Sau khi chèn, tải tin/số lần làm không được sửa; chỉ bản chiếu trạng thái/điểm chuyển theo chấm tự động hoặc duyệt chỉ-bổ-sung.

#### TBL-STU-034 — `assessment_answers`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `attempt_id uuid NOT NULL` FK `assessment_attempts.id`; `question_id uuid NULL` FK `quiz_questions.id`; `answer_type assessment_type NOT NULL`; `answer_text text NULL`; `answer_url varchar(2048) NULL`; `selected_option_ids uuid[] NULL`; `answer_hash char(64) NOT NULL`; `position integer NOT NULL`.
- Ràng buộc: duy nhất `(attempt_id,position)`; tải tin đúng loại: `QUIZ` cần ID lựa chọn, `TEXT` cần văn bản 1–20000 ký tự, `LINK` cần URL HTTPS và máy chủ không tự tải, `FILE` có liên kết tệp; dữ liệu bất biến sau khi nộp.
- Chỉ mục: `(attempt_id,position)`; PII có thể xuất hiện trong văn bản.

#### TBL-STU-035 — `file_objects`

- Tập cột: `ENTITY`.
- Cột riêng: `owner_subject_id uuid NOT NULL`; `purpose varchar(40) NOT NULL`; `storage_key varchar(700) NOT NULL UNIQUE`; `original_name varchar(255) NOT NULL`; `declared_mime varchar(120) NOT NULL`; `detected_mime varchar(120) NULL`; `size_bytes bigint NOT NULL`; `sha256 char(64) NOT NULL`; `scan_status file_asset_status NOT NULL DEFAULT 'CREATED'`; `uploaded_at timestamptz NULL`; `available_at timestamptz NULL`; `quarantined_at timestamptz NULL`; `expires_at timestamptz NULL`; `deleted_at timestamptz NULL`.
- Ràng buộc: kích thước từ 1 byte đến hạn mức theo `purpose`; duy nhất `(sha256,owner_subject_id,purpose)` khi chưa bị xóa; MIME phát hiện phải thuộc danh sách cho phép của mục đích; chỉ `CLEAN` mới sẵn sàng để tải.
- Chỉ mục: `(owner_subject_id,purpose,created_at DESC)`; `(scan_status,created_at)`; chỉ mục một phần trên `(expires_at)` khi có giá trị.
- Dữ liệu: PII; khóa đối tượng không chứa tên tệp/dữ liệu người dùng; URL có chữ ký tối đa 5 phút.

#### TBL-STU-036 — `malware_scan_results`

- Tập cột: `APPEND`.
- Cột riêng: `file_id uuid NOT NULL` FK `file_objects.id`; `scanner varchar(40) NOT NULL DEFAULT 'CLAMAV'`; `engine_version varchar(80) NOT NULL`; `signature_version varchar(80) NOT NULL`; `result file_asset_status NOT NULL`; `detected_mime varchar(120) NULL`; `threat_name varchar(200) NULL`; `error_code varchar(80) NULL`; `scan_duration_ms integer NOT NULL`; `worker_id varchar(120) NOT NULL`.
- Ràng buộc: `result` chỉ nhận `CLEAN|INFECTED|SCAN_FAILED`; thời lượng >=0; tên mối đe dọa bắt buộc khi đã nhiễm.
- Chỉ mục: `(file_id,occurred_at DESC)`; `(result,occurred_at)`; giữ 24 tháng.

#### TBL-STU-037 — `attempt_files`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `attempt_id uuid NOT NULL` FK `assessment_attempts.id`; `answer_id uuid NOT NULL` FK `assessment_answers.id`; `file_id uuid NOT NULL` FK `file_objects.id`; `attached_at timestamptz NOT NULL`.
- Ràng buộc: duy nhất `(attempt_id,file_id)`; chủ tệp là người học của lượt làm, `purpose` là `ASSESSMENT`, tệp đã quét `CLEAN` trước khi nộp.
- Chỉ mục: `(answer_id)`; không xóa dây chuyền khi lượt làm ở trạng thái kết thúc.

#### TBL-STU-038 — `assessment_reviews`

- Tập cột: `APPEND`.
- Cột riêng: `attempt_id uuid NOT NULL` FK `assessment_attempts.id`; `review_round integer NOT NULL`; `reviewer_subject_id uuid NOT NULL`; `decision review_decision NOT NULL`; `score numeric(7,2) NULL`; `feedback_markdown text NOT NULL`; `expected_attempt_version bigint NOT NULL`; `supersedes_review_id uuid NULL` self-FK; `trace_id varchar(64) NOT NULL`.
- Ràng buộc: duy nhất `(attempt_id,review_round)`; điểm hợp lệ; `NEEDS_REVISION`/`FAILED` yêu cầu phản hồi; cập nhật lạc quan trạng thái lượt làm chỉ cho phép một người chấm thắng.
- Chỉ mục: `(attempt_id,review_round DESC)`; `(reviewer_subject_id,occurred_at DESC)`; giữ 24 tháng.

#### TBL-STU-039 — `assessment_review_scores`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `review_id uuid NOT NULL` FK `assessment_reviews.id`; `criterion_id uuid NOT NULL` FK `rubric_criteria.id`; `points numeric(7,2) NOT NULL`; `comment varchar(1000) NULL`.
- Ràng buộc: duy nhất `(review_id,criterion_id)`; điểm từ 0 đến `criterion.max_points`; tổng bằng điểm chấm duyệt.
- Chỉ mục: `(review_id)`.

### 5.7 Minh chứng học tập

#### TBL-STU-040 — `evidence_records`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `learner_id uuid NOT NULL` FK `learner_profiles.id`; `evidence_type varchar(32) NOT NULL`; `source_type varchar(32) NOT NULL`; `source_id uuid NOT NULL`; `source_version_id uuid NOT NULL`; `status evidence_status NOT NULL DEFAULT 'ISSUED'`; `title varchar(200) NOT NULL`; `description varchar(1000) NOT NULL`; `issued_at timestamptz NOT NULL`; `expires_at timestamptz NULL`; `revoked_at timestamptz NULL`; `revocation_reason varchar(500) NULL`; `claims_snapshot jsonb NOT NULL`; `claims_hash char(64) NOT NULL`; `issuer_key_id varchar(80) NOT NULL`; `signature varchar(512) NOT NULL`; `schema_version integer NOT NULL`.
- Ràng buộc: duy nhất `(learner_id,source_type,source_id,source_version_id,evidence_type)`; phiên bản nguồn bắt buộc; dấu thời gian/lý do thu hồi theo `status`; dữ liệu xác nhận là tối thiểu và không chứa thông tin liên hệ.
- Chỉ mục: `(learner_id,status,issued_at DESC)`; `(source_type,source_id)`; `(expires_at)`.
- Thời hạn lưu giữ: Dịch vụ Học tập giữ cùng kết quả hoàn thành; xuất sang Dịch vụ Việc làm luôn tạo ảnh chụp theo đơn ứng tuyển, không cấp quyền tìm kiếm.

#### TBL-STU-041 — `evidence_export_requests`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `request_id uuid NOT NULL UNIQUE`; `application_id uuid NOT NULL`; `learner_identity_subject_id uuid NOT NULL`; `requested_evidence_ids uuid[] NOT NULL`; `consent_id uuid NOT NULL`; `requester_service varchar(20) NOT NULL DEFAULT 'WORK'`; `request_signature_hash char(64) NOT NULL`; `requested_at timestamptz NOT NULL`; `processed_at timestamptz NULL`; `result_code varchar(80) NULL`; `response_hash char(64) NULL`; `trace_id varchar(64) NOT NULL`.
- Ràng buộc: ID minh chứng không rỗng/không trùng; quyền sở hữu, `ISSUED`, phiên bản, hết hạn/thu hồi được kiểm tại thời điểm xử lý; yêu cầu duy nhất bảo đảm xử lý lặp an toàn.
- Chỉ mục: `(learner_identity_subject_id,requested_at DESC)`; `(application_id)`; giữ tối thiểu 24 tháng như kiểm toán sự đồng ý.

### 5.8 Thông báo, cộng đồng và hỗ trợ

#### TBL-STU-042 — `notification_preferences`

- Tập cột: `ENTITY`.
- Cột riêng: `learner_id uuid NOT NULL` FK `learner_profiles.id`; `category varchar(40) NOT NULL`; `in_app_enabled boolean NOT NULL DEFAULT true`; `email_enabled boolean NOT NULL DEFAULT true`; `quiet_hours_start time NULL`; `quiet_hours_end time NULL`; `timezone varchar(64) NOT NULL`; `consent_source varchar(40) NOT NULL`.
- Ràng buộc: duy nhất `(learner_id,category)`; danh mục giao dịch/bảo mật không được tắt bằng tùy chọn.
- Chỉ mục: `(learner_id,category)`.

#### TBL-STU-043 — `notifications`

- Tập cột: `ENTITY`.
- Cột riêng: `learner_id uuid NOT NULL` FK `learner_profiles.id`; `category varchar(40) NOT NULL`; `template_code varchar(80) NOT NULL`; `template_version integer NOT NULL`; `title varchar(200) NOT NULL`; `body varchar(4000) NOT NULL`; `action_url varchar(1000) NULL`; `dedupe_key varchar(180) NOT NULL`; `read_at timestamptz NULL`; `expires_at timestamptz NOT NULL`; `payload jsonb NOT NULL DEFAULT '{}'`.
- Ràng buộc: duy nhất `(learner_id,dedupe_key)`; URL hành động chỉ thuộc danh sách nội bộ được phép; tải tin đã được che dữ liệu.
- Chỉ mục: `(learner_id,read_at,created_at DESC,id DESC)` hỗ trợ con trỏ; `(expires_at)`.
- Thời hạn lưu giữ: 180 ngày rồi dọn.

#### TBL-STU-044 — `notification_deliveries`

- Tập cột: `APPEND`.
- Cột riêng: `notification_id uuid NOT NULL` FK `notifications.id`; `channel varchar(16) NOT NULL`; `status notification_status NOT NULL`; `provider_message_id varchar(160) NULL`; `attempt_no integer NOT NULL`; `error_code varchar(80) NULL`; `next_retry_at timestamptz NULL`; `dedupe_key varchar(180) NOT NULL`.
- Ràng buộc: duy nhất `(notification_id,channel,attempt_no)` và `dedupe_key`; `channel` là `IN_APP|EMAIL`; `attempt>=1`.
- Chỉ mục: `(status,next_retry_at)`; giữ 180 ngày.

#### TBL-STU-045 — `community_channels`

- Tập cột: `ENTITY`.
- Cột riêng: `scope_type varchar(24) NOT NULL`; `scope_id uuid NOT NULL`; `provider varchar(20) NOT NULL DEFAULT 'ZALO'`; `name varchar(160) NOT NULL`; `join_url_ciphertext bytea NOT NULL`; `url_fingerprint char(64) NOT NULL`; `rules_version integer NOT NULL`; `active_from timestamptz NOT NULL`; `active_until timestamptz NULL`; `disabled_at timestamptz NULL`.
- Ràng buộc: `scope_type` là `PLATFORM|PATH_VERSION|COURSE_VERSION`; nhà cung cấp hiện chỉ là ZALO; duy nhất khi còn hiệu lực trên `(scope_type,scope_id,provider)`; URL HTTPS.
- Chỉ mục: `(scope_type,scope_id,disabled_at)`; URL tham gia là SENSITIVE, không lộ trong danh mục công khai.

#### TBL-STU-046 — `community_acceptances`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `learner_id uuid NOT NULL` FK `learner_profiles.id`; `channel_id uuid NOT NULL` FK `community_channels.id`; `rules_version integer NOT NULL`; `accepted_at timestamptz NOT NULL`; `ip_hash char(64) NULL`; `revoked_at timestamptz NULL`.
- Ràng buộc: duy nhất khi còn hiệu lực trên `(learner_id,channel_id,rules_version)`; chỉ cấp URL sau khi chấp nhận và kiểm tra ghi danh/quyền.
- Chỉ mục: `(learner_id,accepted_at DESC)`; giữ 24 tháng.

#### TBL-STU-047 — `support_tickets`

- Tập cột: `ENTITY`.
- Cột riêng: `learner_id uuid NOT NULL` FK `learner_profiles.id`; `category varchar(40) NOT NULL`; `status varchar(24) NOT NULL DEFAULT 'OPEN'`; `subject varchar(200) NOT NULL`; `description text NOT NULL`; `priority varchar(16) NOT NULL DEFAULT 'NORMAL'`; `assigned_to_subject_id uuid NULL`; `resolved_at timestamptz NULL`; `cancelled_at timestamptz NULL`; `resolution_code varchar(80) NULL`.
- Ràng buộc: `status` là `OPEN|IN_PROGRESS|WAITING_LEARNER|RESOLVED|CANCELLED`; `priority` là `LOW|NORMAL|HIGH|URGENT`; dấu thời gian kết thúc phải phù hợp.
- Chỉ mục: `(learner_id,created_at DESC)`; `(status,priority,created_at)`; PII, giữ 13 tháng sau trạng thái kết thúc.

#### TBL-STU-048 — `support_messages`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `ticket_id uuid NOT NULL` FK `support_tickets.id`; `author_subject_id uuid NOT NULL`; `author_type varchar(16) NOT NULL`; `body text NOT NULL`; `attachment_file_ids uuid[] NOT NULL DEFAULT '{}'`; `is_internal boolean NOT NULL DEFAULT false`; `sent_at timestamptz NOT NULL`.
- Ràng buộc: `author_type` là `LEARNER|STAFF`; người học không thể tạo nội bộ; quyền sở hữu/mục đích/trạng thái quét của tệp được kiểm.
- Chỉ mục: `(ticket_id,sent_at,id)`; PII; thời hạn lưu giữ giống yêu cầu hỗ trợ.

### 5.9 Vận hành Dịch vụ Học tập

#### TBL-STU-049 — `admin_adjustments`

- Tập cột: `APPEND`.
- Cột riêng: `target_type varchar(32) NOT NULL`; `target_id uuid NOT NULL`; `action varchar(80) NOT NULL`; `before_snapshot jsonb NOT NULL`; `after_snapshot jsonb NOT NULL`; `reason varchar(1000) NOT NULL`; `approved_by_subject_id uuid NOT NULL`; `performed_by_subject_id uuid NOT NULL`; `trace_id varchar(64) NOT NULL`.
- Ràng buộc: áp dụng nguyên tắc người tạo–người kiểm tra cho hiệu chỉnh rủi ro cao; dữ liệu trước/sau được che nhưng đủ để khôi phục quy tắc.
- Chỉ mục: `(target_type,target_id,occurred_at DESC)`; 24 tháng.

#### TBL-STU-050 — `audit_events`

- Tập cột: `APPEND`.
- Cột riêng: `actor_subject_id uuid NULL`; `action varchar(120) NOT NULL`; `resource_type varchar(80) NOT NULL`; `resource_id uuid NULL`; `outcome audit_outcome NOT NULL`; `business_code varchar(80) NOT NULL`; `trace_id varchar(64) NOT NULL`; `tenant_context jsonb NULL`; `changes jsonb NULL`; `metadata jsonb NOT NULL DEFAULT '{}'`; `prev_hash char(64) NULL`; `event_hash char(64) NOT NULL UNIQUE`; `legal_hold_until timestamptz NULL`.
- Ràng buộc: hàm băm sự kiện chuẩn nối `prev_hash` theo phân vùng; thay đổi/siêu dữ liệu được kiểm theo lược đồ và che dữ liệu; từ chối/thất bại có mã nghiệp vụ cụ thể.
- Chỉ mục: `(resource_type,resource_id,occurred_at DESC)`; `(actor_subject_id,occurred_at DESC)`; `(trace_id)`; BRIN theo thời gian.
- Thời hạn lưu giữ: tối thiểu 24 tháng, chỉ bổ sung, che PII theo chính sách.

#### TBL-STU-051 — `idempotency_keys`

- Tập cột: `ENTITY`.
- Cột riêng: `actor_subject_id uuid NULL`; `operation varchar(120) NOT NULL`; `key_hash char(64) NOT NULL`; `request_hash char(64) NOT NULL`; `response_status integer NULL`; `response_body jsonb NULL`; `locked_until timestamptz NULL`; `completed_at timestamptz NULL`; `expires_at timestamptz NOT NULL`.
- Ràng buộc: duy nhất `(actor_subject_id,operation,key_hash)`; cùng khóa nhưng khác hàm băm yêu cầu trả xung đột; phản hồi đã được che dữ liệu.
- Chỉ mục: `(expires_at)`; giữ 24 giờ, riêng ghi danh/đổi lộ trình/nộp bài giữ 7 ngày.

#### TBL-STU-052 — `outbox_events`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `aggregate_type varchar(80) NOT NULL`; `aggregate_id uuid NOT NULL`; `event_type varchar(120) NOT NULL`; `event_version integer NOT NULL`; `payload jsonb NOT NULL`; `available_at timestamptz NOT NULL DEFAULT now()`; `dedupe_key varchar(180) NOT NULL UNIQUE`; `trace_id varchar(64) NOT NULL`.
- Ràng buộc: phiên bản sự kiện >=1; tải tin có `schemaVersion`, `occurredAt`, `producer`, `traceId`; thu hồi minh chứng khử trùng lặp theo minh chứng/phiên bản; hàng chỉ được thêm mới.
- Chỉ mục: `(available_at,id)`; `(aggregate_type,aggregate_id,created_at)`; giữ 24 tháng.

#### TBL-STU-053 — `consumer_inbox`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `consumer varchar(100) NOT NULL`; `event_id uuid NOT NULL`; `event_type varchar(120) NOT NULL`; `payload_hash char(64) NOT NULL`; `received_at timestamptz NOT NULL DEFAULT now()`; `processed_at timestamptz NULL`; `result_code varchar(80) NULL`; `trace_id varchar(64) NOT NULL`.
- Ràng buộc: duy nhất `(consumer,event_id)`; cùng sự kiện nhưng khác hàm băm tải tin là lỗi bảo mật; dùng cho bản chiếu Dịch vụ Định danh và xác nhận của Dịch vụ Việc làm.
- Chỉ mục: `(consumer,processed_at,received_at)`; giữ 24 tháng.

#### TBL-STU-054 — `report_snapshots`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `report_code varchar(80) NOT NULL`; `period_start timestamptz NOT NULL`; `period_end timestamptz NOT NULL`; `dimension_hash char(64) NOT NULL`; `dimensions jsonb NOT NULL`; `metrics jsonb NOT NULL`; `source_high_watermark timestamptz NOT NULL`; `calculation_version integer NOT NULL`; `generated_at timestamptz NOT NULL`.
- Ràng buộc: duy nhất `(report_code,period_start,period_end,dimension_hash,calculation_version)`; cuối kỳ phải sau đầu kỳ; số liệu không chứa PII ở cấp từng dòng.
- Chỉ mục: `(report_code,period_end DESC)`; giữ 13 tháng, không phải kho dữ liệu.

#### TBL-STU-055 — `outbox_delivery_attempts`

- Tập cột và toàn bộ quy tắc như `TBL-IAM-020`, với `outbox_event_id` là khóa ngoại tới `TBL-STU-052`; sự kiện/lần thử là duy nhất; chỉ mục theo sự kiện/mới nhất và trạng thái/thử lại; chỉ bổ sung trong 24 tháng.
- Cột riêng đầy đủ: `outbox_event_id uuid NOT NULL`; `attempt_no integer NOT NULL`; `status outbox_status NOT NULL`; `worker_id varchar(120) NOT NULL`; `broker_message_id varchar(180) NULL`; `error_code varchar(80) NULL`; `next_retry_at timestamptz NULL`; `payload_hash char(64) NOT NULL`.

#### TBL-STU-056 — `study_skills`

- Tập cột: `ENTITY`.
- Cột riêng: `code varchar(80) NOT NULL UNIQUE`; `name varchar(160) NOT NULL`; `normalized_name varchar(160) NOT NULL UNIQUE`; `category varchar(80) NULL`; `description varchar(1000) NULL`; `status varchar(16) NOT NULL DEFAULT 'ACTIVE'`; `aliases varchar(160)[] NOT NULL DEFAULT '{}'`.
- Ràng buộc: `status` là `ACTIVE|ARCHIVED`; phân loại kỹ năng của Dịch vụ Học tập độc lập với Dịch vụ Việc làm, ánh xạ ra ngoài bằng mã/phiên bản đã ký chứ không dùng khóa ngoại xuyên cơ sở dữ liệu.
- Chỉ mục: GIN ba ký tự trên tên chuẩn hóa; GIN trên bí danh; `(status,category)`.

#### TBL-STU-057 — `course_skill_outcomes`

- Tập cột: `ENTITY`; chỉ sửa khi phiên bản khóa học còn `DRAFT`, bất biến sau khi gửi duyệt.
- Cột riêng: `course_version_id uuid NOT NULL` FK `course_versions.id`; `skill_id uuid NOT NULL` FK `study_skills.id`; `outcome_level smallint NOT NULL`; `description varchar(1000) NOT NULL`; `position integer NOT NULL`.
- Ràng buộc: duy nhất `(course_version_id,skill_id)` và `(course_version_id,position)`; cấp độ 1–5; kỹ năng đã lưu trữ không được thêm vào bản nháp mới.
- Chỉ mục: `(skill_id,course_version_id)`; `(course_version_id,position)`.

#### TBL-STU-058 — `course_prerequisites`

- Tập cột: `ENTITY`; chỉ sửa khi phiên bản khóa học còn `DRAFT`, bất biến sau khi gửi duyệt.
- Cột riêng: `course_version_id uuid NOT NULL` FK `course_versions.id`; `required_course_version_id uuid NOT NULL` FK `course_versions.id`; `require_completion boolean NOT NULL DEFAULT true`; `position integer NOT NULL`.
- Ràng buộc: duy nhất `(course_version_id,required_course_version_id)` và `(course_version_id,position)`; không tự tham chiếu; đồ thị không chu trình được kiểm khi xuất bản; điều kiện tiên quyết luôn ghim đúng phiên bản.
- Chỉ mục: `(required_course_version_id,course_version_id)`; `(course_version_id,position)`.

#### TBL-STU-059 — `file_upload_sessions`

- Tập cột: `ENTITY`.
- Cột riêng: `file_id uuid NOT NULL UNIQUE` FK `file_objects.id`; `owner_subject_id uuid NOT NULL`; `upload_id varchar(200) NOT NULL UNIQUE`; `expected_size_bytes bigint NOT NULL`; `expected_sha256 char(64) NOT NULL`; `part_count integer NOT NULL DEFAULT 1`; `status varchar(24) NOT NULL DEFAULT 'CREATED'`; `expires_at timestamptz NOT NULL`; `completed_at timestamptz NULL`; `aborted_at timestamptz NULL`.
- Ràng buộc: kích thước >0 theo hạn mức `purpose`; số phần 1–10000; `status` là `CREATED|UPLOADING|COMPLETED|ABORTED|EXPIRED`; khi hoàn tất, đối chiếu kích thước/hàm băm rồi mới xếp quét tệp vào hàng đợi.
- Chỉ mục: `(owner_subject_id,status,created_at DESC)`; `(status,expires_at)`; dọn phiên tải lên 7 ngày sau trạng thái kết thúc.

#### TBL-STU-060 — `assessment_drafts`

- Tập cột: `ENTITY`; hàng chỉ có thể sửa trước khi được niêm phong.
- Cột riêng: `learner_id uuid NOT NULL` FK `learner_profiles.id`; `enrollment_id uuid NOT NULL` FK `course_enrollments.id`; `assessment_id uuid NOT NULL` FK `assessments.id`; `answer_type assessment_type NOT NULL`; `payload jsonb NOT NULL`; `file_id uuid NULL` FK `file_objects.id`; `state varchar(16) NOT NULL DEFAULT 'DRAFT'`; `last_saved_at timestamptz NOT NULL`; `sealed_at timestamptz NULL`; `sealed_attempt_id uuid NULL` FK `assessment_attempts.id`; `content_hash char(64) NOT NULL`.
- Ràng buộc: duy nhất `(learner_id,assessment_id)`; `state` chỉ là `DRAFT|SEALED`; `SEALED` yêu cầu `sealed_at` và `sealed_attempt_id`, sau đó cấm sửa tải tin; loại phụ/kích thước/HTTPS/chủ tệp và `CLEAN` được kiểm như API. Bản nháp không cấp `attempt_no` và không tính vào hạn mức lượt làm.
- Chỉ mục: `(learner_id,assessment_id,state)`; `(enrollment_id,last_saved_at DESC)`.
- Xử lý đồng thời/thời hạn lưu giữ: `If-Match` dùng `row_version`; việc nộp bài khóa bản nháp và cặp người học–bài đánh giá, tạo `TBL-STU-033`, rồi niêm phong bản nháp theo cách nguyên tử. Bản nháp chưa niêm phong bị xóa theo yêu cầu người học hoặc sau 90 ngày không hoạt động; bản nháp đã niêm phong giữ cùng lượt làm. `TBL-STU-060` là nguồn cho API bản nháp, không dùng hàng lượt làm ở trạng thái `DRAFT`.

## 6. Cơ sở dữ liệu Việc làm (`work_db`)

### 6.1 Bản chiếu danh tính và tệp dùng chung

#### TBL-WRK-001 — `identity_projections`

- Tập cột: `ENTITY`.
- Cột riêng: `identity_subject_id uuid NOT NULL UNIQUE`; `account_status account_status NOT NULL`; `email_verified boolean NOT NULL DEFAULT false`; `display_name varchar(120) NULL`; `identity_version bigint NOT NULL`; `last_event_id uuid NOT NULL UNIQUE`; `projected_at timestamptz NOT NULL`.
- Ràng buộc/chỉ mục: như `TBL-STU-001`; không phải khóa ngoại xuyên cơ sở dữ liệu.

#### TBL-WRK-002 — `file_objects`

- Tập cột và chính sách tương đương `TBL-STU-035`.
- Cột riêng đầy đủ: `owner_subject_id uuid NOT NULL`; `tenant_id uuid NULL`; `purpose varchar(40) NOT NULL`; `storage_key varchar(700) NOT NULL UNIQUE`; `original_name varchar(255) NOT NULL`; `declared_mime varchar(120) NOT NULL`; `detected_mime varchar(120) NULL`; `size_bytes bigint NOT NULL`; `sha256 char(64) NOT NULL`; `scan_status file_asset_status NOT NULL DEFAULT 'CREATED'`; `uploaded_at timestamptz NULL`; `available_at timestamptz NULL`; `quarantined_at timestamptz NULL`; `expires_at timestamptz NULL`; `deleted_at timestamptz NULL`.
- Ràng buộc: `tenant_id` bắt buộc với tệp của tổ chức; chỉ tệp `CLEAN` mới được dùng; `purpose` là `AVATAR|CV|PORTFOLIO|ENTERPRISE_LOGO|UNIVERSITY_LOGO|VERIFICATION|JOB|INVOICE`; hạn mức theo `purpose`. Trò chuyện V1 chỉ có nội dung `TEXT|SYSTEM`, nên không có tệp với `purpose` `CHAT`.
- Chỉ mục: `(owner_subject_id,purpose,created_at DESC)`; `(tenant_id,purpose,created_at DESC)`; `(scan_status,created_at)`; `(expires_at)`.

#### TBL-WRK-003 — `malware_scan_results`

- Tập cột: `APPEND`.
- Cột riêng đầy đủ: `file_id uuid NOT NULL` FK `file_objects.id`; `scanner varchar(40) NOT NULL DEFAULT 'CLAMAV'`; `engine_version varchar(80) NOT NULL`; `signature_version varchar(80) NOT NULL`; `result file_asset_status NOT NULL`; `detected_mime varchar(120) NULL`; `threat_name varchar(200) NULL`; `error_code varchar(80) NULL`; `scan_duration_ms integer NOT NULL`; `worker_id varchar(120) NOT NULL`.
- Ràng buộc: `result` là `CLEAN|INFECTED|SCAN_FAILED`; thời lượng >=0; trạng thái `INFECTED` yêu cầu tên mối đe dọa.
- Chỉ mục: `(file_id,occurred_at DESC)`; `(result,occurred_at)`; giữ 24 tháng.

### 6.2 Ứng viên, CV và hồ sơ năng lực

#### TBL-WRK-004 — `candidate_profiles`

- Tập cột: `ENTITY`.
- Cột riêng: `identity_subject_id uuid NOT NULL UNIQUE`; `full_name varchar(160) NULL`; `headline varchar(200) NULL`; `summary text NULL`; `phone_ciphertext bytea NULL`; `phone_last4 char(4) NULL`; `city_code varchar(20) NULL`; `country_code char(2) NOT NULL DEFAULT 'VN'`; `avatar_file_id uuid NULL` FK `file_objects.id`; `visibility candidate_visibility NOT NULL DEFAULT 'PRIVATE'`; `search_opted_in_at timestamptz NULL`; `search_opted_out_at timestamptz NULL`; `available_from date NULL`; `deleted_at timestamptz NULL`.
- Ràng buộc: `SEARCHABLE` yêu cầu đã chủ động cho phép tìm kiếm; khi chuyển sang `PRIVATE` sau khi đã cho phép, phải có dấu thời gian rút quyền; ảnh đại diện phải `CLEAN`; số điện thoại tuân thủ E.164 trước khi mã hóa.
- Chỉ mục: `(visibility,updated_at DESC)`; `(city_code,visibility)`; `(deleted_at)`; PII.

#### TBL-WRK-005 — `candidate_search_preferences`

- Tập cột: `ENTITY`.
- Cột riêng: `candidate_id uuid NOT NULL UNIQUE` FK `candidate_profiles.id`; `desired_titles varchar(120)[] NOT NULL DEFAULT '{}'`; `desired_locations varchar(20)[] NOT NULL DEFAULT '{}'`; `work_modes varchar(16)[] NOT NULL DEFAULT '{}'`; `employment_types varchar(24)[] NOT NULL DEFAULT '{}'`; `salary_min_vnd bigint NULL`; `salary_visibility boolean NOT NULL DEFAULT false`; `notice_days integer NULL`; `excluded_enterprise_ids uuid[] NOT NULL DEFAULT '{}'`.
- Ràng buộc: lương >=0, số ngày báo trước 0–365; các mảng bị giới hạn lần lượt 20/20/5/10/200 phần tử.
- Chỉ mục: GIN trên các mảng phục vụ tìm kiếm; dữ liệu chỉ vào chỉ mục tìm kiếm khi hồ sơ ở trạng thái `SEARCHABLE`.

#### TBL-WRK-006 — `skills`

- Tập cột: `ENTITY`.
- Cột riêng: `slug varchar(120) NOT NULL UNIQUE`; `name varchar(160) NOT NULL`; `normalized_name varchar(160) NOT NULL UNIQUE`; `category varchar(80) NULL`; `status varchar(16) NOT NULL DEFAULT 'ACTIVE'`; `aliases varchar(160)[] NOT NULL DEFAULT '{}'`.
- Ràng buộc: `status` là `ACTIVE|ARCHIVED`; giá trị `slug` dùng chữ thường và dấu gạch nối; các bí danh chuẩn hóa không trùng với `normalized_name` khác.
- Chỉ mục: GIN ba ký tự trên `normalized_name`; GIN trên các bí danh; danh mục là `PUBLIC`.

#### TBL-WRK-007 — `candidate_skills`

- Tập cột: `ENTITY`.
- Cột riêng: `candidate_id uuid NOT NULL` FK `candidate_profiles.id`; `skill_id uuid NOT NULL` FK `skills.id`; `proficiency smallint NULL`; `years_experience numeric(4,1) NULL`; `last_used_year smallint NULL`; `source varchar(24) NOT NULL`; `is_visible boolean NOT NULL DEFAULT true`.
- Ràng buộc: duy nhất `(candidate_id,skill_id)`; mức thành thạo 1–5; số năm 0–80; `source` là `SELF|CV_PARSED|ADMIN`, gợi ý đã phân tích cần ứng viên xác nhận trước khi đưa vào khả năng tìm kiếm.
- Chỉ mục: `(skill_id,candidate_id)` một phần theo `is_visible`; `(candidate_id,updated_at DESC)`.

#### TBL-WRK-008 — `candidate_experiences`

- Tập cột: `ENTITY`.
- Cột riêng: `candidate_id uuid NOT NULL` FK `candidate_profiles.id`; `company_name varchar(200) NOT NULL`; `title varchar(160) NOT NULL`; `start_date date NOT NULL`; `end_date date NULL`; `is_current boolean NOT NULL DEFAULT false`; `description text NULL`; `position integer NOT NULL`; `visibility varchar(16) NOT NULL DEFAULT 'PRIVATE'`.
- Ràng buộc: ngày kết thúc không trước ngày bắt đầu; `is_current` yêu cầu ngày kết thúc không có giá trị; duy nhất `(candidate_id,position)`; `visibility` là `PRIVATE|SEARCH`.
- Chỉ mục: `(candidate_id,position)`; PII.

#### TBL-WRK-009 — `candidate_educations`

- Tập cột: `ENTITY`.
- Cột riêng: `candidate_id uuid NOT NULL` FK `candidate_profiles.id`; `institution_name varchar(240) NOT NULL`; `degree varchar(160) NULL`; `field_of_study varchar(160) NULL`; `start_date date NULL`; `end_date date NULL`; `description varchar(2000) NULL`; `position integer NOT NULL`; `visibility varchar(16) NOT NULL DEFAULT 'PRIVATE'`.
- Ràng buộc: nếu có đủ hai ngày thì ngày kết thúc không trước ngày bắt đầu; duy nhất `(candidate_id,position)`; `visibility` là `PRIVATE|SEARCH`.
- Chỉ mục: `(candidate_id,position)`; PII.

#### TBL-WRK-010 — `cvs`

- Tập cột: `ENTITY`.
- Cột riêng: `candidate_id uuid NOT NULL` FK `candidate_profiles.id`; `title varchar(160) NOT NULL`; `is_default boolean NOT NULL DEFAULT false`; `current_draft_version_id uuid NULL`; `latest_published_version_id uuid NULL`; `archived_at timestamptz NULL`.
- Ràng buộc: duy nhất một phần trên `(candidate_id)` khi là mặc định và còn hiệu lực; tối đa 20 CV còn hiệu lực mỗi ứng viên, được bảo đảm trong giao dịch.
- Chỉ mục: `(candidate_id,archived_at,updated_at DESC)`.

#### TBL-WRK-011 — `cv_versions`

- Tập cột: `ENTITY`; chỉ sửa bằng `row_version` khi `DRAFT`, bất biến sau khi xuất bản.
- Cột riêng: `cv_id uuid NOT NULL` FK `cvs.id`; `version_no integer NOT NULL`; `status cv_revision_status NOT NULL DEFAULT 'DRAFT'`; `template_code varchar(80) NOT NULL`; `template_version integer NOT NULL`; `content_json jsonb NOT NULL`; `rendered_file_id uuid NULL` FK `file_objects.id`; `source_file_id uuid NULL` FK `file_objects.id`; `content_hash char(64) NOT NULL`; `created_by_subject_id uuid NOT NULL`; `published_at timestamptz NULL`; `superseded_at timestamptz NULL`; `discarded_at timestamptz NULL`; `source_version_id uuid NULL` self-FK.
- Ràng buộc: duy nhất `(cv_id,version_no)`; nội dung được kiểm theo lược đồ; bản `PUBLISHED` là bất biến và yêu cầu tệp kết xuất `CLEAN`; quyền dùng mẫu được kiểm khi xuất bản/xuất dữ liệu.
- Chỉ mục: `(cv_id,status,version_no DESC)`; PII, giữ 12 tháng sau lưu trữ hoặc theo ảnh chụp đơn ứng tuyển.

#### TBL-WRK-012 — `portfolio_items`

- Tập cột: `ENTITY`.
- Cột riêng: `candidate_id uuid NOT NULL` FK `candidate_profiles.id`; `title varchar(200) NOT NULL`; `description text NULL`; `url varchar(2048) NULL`; `file_id uuid NULL` FK `file_objects.id`; `position integer NOT NULL`; `visibility varchar(16) NOT NULL DEFAULT 'PRIVATE'`; `published_at timestamptz NULL`; `archived_at timestamptz NULL`.
- Ràng buộc: phải có chính xác một URL HTTPS hoặc tệp `CLEAN`; duy nhất `(candidate_id,position)`; `visibility` là `PRIVATE|SEARCH|APPLICATION_ONLY`.
- Chỉ mục: `(candidate_id,archived_at,position)`.

#### TBL-WRK-013 — `saved_jobs`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `candidate_id uuid NOT NULL` FK `candidate_profiles.id`; `job_id uuid NOT NULL`; `saved_at timestamptz NOT NULL`; `removed_at timestamptz NULL`.
- Ràng buộc: duy nhất một phần trên `(candidate_id,job_id)` khi còn hiệu lực; thao tác bỏ lưu là chuyển trạng thái một chiều.
- Chỉ mục: `(candidate_id,removed_at,saved_at DESC)`.

### 6.3 Tổ chức doanh nghiệp, tư cách thành viên và xác minh

#### TBL-WRK-014 — `enterprise_tenants`

- Tập cột: `ENTITY`.
- Cột riêng: `legal_name varchar(240) NOT NULL`; `display_name varchar(200) NOT NULL`; `tax_code varchar(32) NOT NULL`; `tax_code_country char(2) NOT NULL DEFAULT 'VN'`; `slug varchar(120) NOT NULL UNIQUE`; `status tenant_status NOT NULL DEFAULT 'PENDING_VERIFICATION'`; `website_url varchar(2048) NULL`; `description text NULL`; `logo_file_id uuid NULL` FK `file_objects.id`; `verified_at timestamptz NULL`; `suspended_at timestamptz NULL`; `closed_at timestamptz NULL`.
- Ràng buộc: duy nhất `(tax_code_country,tax_code)`; `VERIFIED` yêu cầu `verified_at`; trang web dùng HTTPS; biểu trưng phải `CLEAN`.
- Chỉ mục: `(status,created_at DESC)`; GIN ba ký tự trên tên hiển thị; phân loại `PII`/`INTERNAL` theo từng trường.

#### TBL-WRK-015 — `enterprise_verification_cases`

- Tập cột: `TENANT_ENTITY` với `tenant_id` FK `enterprise_tenants.id`.
- Cột riêng: `case_no integer NOT NULL`; `status varchar(24) NOT NULL DEFAULT 'SUBMITTED'`; `submitted_by_subject_id uuid NOT NULL`; `document_file_ids uuid[] NOT NULL`; `submitted_snapshot jsonb NOT NULL`; `reviewer_subject_id uuid NULL`; `reviewed_at timestamptz NULL`; `decision_reason_codes varchar(80)[] NOT NULL DEFAULT '{}'`; `comment varchar(2000) NULL`; `expires_at timestamptz NULL`.
- Ràng buộc: duy nhất `(tenant_id,case_no)`; `status` là `SUBMITTED|IN_REVIEW|APPROVED|REJECTED|EXPIRED`; tài liệu không rỗng và đều `CLEAN` với mục đích `VERIFICATION`; người duyệt bắt buộc khi ở trạng thái kết thúc.
- Chỉ mục: `(status,created_at)`; `(tenant_id,case_no DESC)`.
- Thời hạn lưu giữ: tài liệu xác minh được xóa sau 180 ngày kể từ quyết định/hết hạn nếu không bị tạm giữ pháp lý; giữ siêu dữ liệu/kiểm toán 24 tháng.

#### TBL-WRK-016 — `enterprise_memberships`

- Tập cột: `TENANT_ENTITY` với `tenant_id` FK `enterprise_tenants.id`.
- Cột riêng: `identity_subject_id uuid NOT NULL`; `role_code varchar(40) NOT NULL`; `status membership_status NOT NULL`; `joined_at timestamptz NULL`; `suspended_at timestamptz NULL`; `left_at timestamptz NULL`; `invited_by_subject_id uuid NULL`; `valid_until timestamptz NULL`.
- Ràng buộc: duy nhất `(tenant_id,identity_subject_id)`; `role_code` là `OWNER|ADMIN|RECRUITER|HIRING_MANAGER|BILLING|VIEWER`; trạng thái hiệu lực yêu cầu đã tham gia; luôn có ít nhất một `OWNER` còn hiệu lực nhờ ràng buộc nghiệp vụ kiểm tra trì hoãn.
- Chỉ mục: `(identity_subject_id,status)`; `(tenant_id,status,role_code)`.

#### TBL-WRK-017 — `enterprise_invites`

- Tập cột: `TENANT_ENTITY` với `tenant_id` FK `enterprise_tenants.id`.
- Cột riêng: `email_normalized varchar(320) NOT NULL`; `email_ciphertext bytea NOT NULL`; `role_code varchar(40) NOT NULL`; `token_hash char(64) NOT NULL UNIQUE`; `invited_by_subject_id uuid NOT NULL`; `expires_at timestamptz NOT NULL`; `accepted_at timestamptz NULL`; `revoked_at timestamptz NULL`.
- Ràng buộc: duy nhất một phần trên `(tenant_id,email_normalized)` khi chưa được chấp nhận/thu hồi; hết hạn phải sau khi tạo; không ghi nhật ký thư điện tử/mã thông báo gốc.
- Chỉ mục: `(tenant_id,expires_at)`; dọn dữ liệu mã hóa/mã thông báo sau 180 ngày.

#### TBL-WRK-018 — `trusted_publisher_grants`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `tenant_id uuid NOT NULL` FK `enterprise_tenants.id`; `scope varchar(24) NOT NULL DEFAULT 'JOB'`; `valid_from timestamptz NOT NULL`; `valid_until timestamptz NOT NULL`; `granted_by_subject_id uuid NOT NULL`; `grant_reason varchar(1000) NOT NULL`; `eligibility_snapshot jsonb NOT NULL`; `revoked_at timestamptz NULL`; `revoked_by_subject_id uuid NULL`; `revoke_reason varchar(1000) NULL`.
- Ràng buộc: duy nhất một phần trên `(tenant_id,scope)` khi còn hiệu lực; thời hạn hợp lệ; ảnh chụp điều kiện ghi số lần xuất bản được phê duyệt và ngày tệp sạch; việc khởi tạo thí điểm phải có lý do quản trị.
- Chỉ mục: `(tenant_id,scope,revoked_at,valid_until)`; không bỏ qua việc kiểm tra tự động/kiểm toán.

### 6.4 Tổ chức trường đại học và sự đồng ý

#### TBL-WRK-019 — `university_tenants`

- Tập cột: `ENTITY`.
- Cột riêng: `legal_name varchar(240) NOT NULL`; `display_name varchar(200) NOT NULL`; `institution_code varchar(80) NOT NULL UNIQUE`; `slug varchar(120) NOT NULL UNIQUE`; `status tenant_status NOT NULL DEFAULT 'PENDING_VERIFICATION'`; `website_url varchar(2048) NULL`; `logo_file_id uuid NULL` FK `file_objects.id`; `verified_at timestamptz NULL`; `suspended_at timestamptz NULL`; `closed_at timestamptz NULL`.
- Ràng buộc: `VERIFIED` yêu cầu `verified_at`; URL dùng HTTPS; biểu trưng phải `CLEAN`.
- Chỉ mục: `(status,created_at DESC)`; GIN ba ký tự trên tên hiển thị.

#### TBL-WRK-020 — `university_verification_cases`

- Tập cột: `TENANT_ENTITY` với `tenant_id` FK `university_tenants.id`.
- Cột riêng: toàn bộ cột riêng của `TBL-WRK-015` gồm `case_no`, `status`, chủ thể gửi, ID tài liệu, ảnh chụp dữ liệu, người duyệt/quyết định/thời điểm/hết hạn; thêm `accreditation_code varchar(120) NULL`.
- Ràng buộc: duy nhất `(tenant_id,case_no)`; dùng cùng máy trạng thái xác minh; tài liệu phải `CLEAN` và thuộc đúng tổ chức.
- Chỉ mục: `(status,created_at)`; `(tenant_id,case_no DESC)`; thời hạn lưu giữ tài liệu là 180 ngày.

#### TBL-WRK-021 — `university_memberships`

- Tập cột: `TENANT_ENTITY` với `tenant_id` FK `university_tenants.id`.
- Cột riêng: `identity_subject_id uuid NOT NULL`; `role_code varchar(40) NOT NULL`; `status membership_status NOT NULL`; `joined_at timestamptz NULL`; `suspended_at timestamptz NULL`; `left_at timestamptz NULL`; `invited_by_subject_id uuid NULL`; `valid_until timestamptz NULL`.
- Ràng buộc: duy nhất `(tenant_id,identity_subject_id)`; `role_code` là `OWNER|ADMIN|COORDINATOR|ANALYST|VIEWER`; trạng thái hiệu lực yêu cầu đã tham gia; luôn có ít nhất một `OWNER` còn hiệu lực.
- Chỉ mục: `(identity_subject_id,status)`; `(tenant_id,status,role_code)`.

#### TBL-WRK-022 — `university_invites`

- Tập cột: `TENANT_ENTITY` với `tenant_id` FK `university_tenants.id`.
- Cột riêng: `email_normalized varchar(320) NOT NULL`; `email_ciphertext bytea NOT NULL`; `role_code varchar(40) NOT NULL`; `token_hash char(64) NOT NULL UNIQUE`; `invited_by_subject_id uuid NOT NULL`; `expires_at timestamptz NOT NULL`; `accepted_at timestamptz NULL`; `revoked_at timestamptz NULL`.
- Ràng buộc: vai trò theo Trường đại học; duy nhất một phần theo tổ chức/thư điện tử khi còn hiệu lực; hết hạn sau khi tạo; chấp nhận/thu hồi theo một chiều.
- Chỉ mục: `(tenant_id,expires_at)`; dọn dữ liệu mã hóa/mã thông báo sau 180 ngày.

#### TBL-WRK-023 — `student_affiliations`

- Tập cột: `TENANT_ENTITY` với `tenant_id` FK `university_tenants.id`.
- Cột riêng: `candidate_id uuid NOT NULL` FK `candidate_profiles.id`; `student_code_ciphertext bytea NULL`; `student_code_fingerprint char(64) NULL`; `affiliation_status varchar(24) NOT NULL DEFAULT 'PENDING'`; `starts_on date NULL`; `ends_on date NULL`; `verified_by_subject_id uuid NULL`; `verified_at timestamptz NULL`; `revoked_at timestamptz NULL`.
- Ràng buộc: duy nhất một phần trên `(tenant_id,candidate_id)` khi còn hiệu lực; dấu vân tay là duy nhất trong tổ chức khi có; `affiliation_status` là `PENDING|VERIFIED|REJECTED|ENDED|REVOKED`; khoảng ngày hợp lệ.
- Chỉ mục: `(tenant_id,affiliation_status)`; `(candidate_id,affiliation_status)`; PII.

#### TBL-WRK-024 — `cohorts`

- Tập cột: `TENANT_ENTITY` với `tenant_id` FK `university_tenants.id`.
- Cột riêng: `code varchar(80) NOT NULL`; `name varchar(200) NOT NULL`; `academic_year varchar(20) NOT NULL`; `starts_on date NULL`; `ends_on date NULL`; `archived_at timestamptz NULL`.
- Ràng buộc: duy nhất `(tenant_id,code)`; khoảng ngày hợp lệ.
- Chỉ mục: `(tenant_id,academic_year,archived_at)`.

#### TBL-WRK-025 — `cohort_memberships`

- Tập cột: `TENANT_ENTITY` với `tenant_id` FK `university_tenants.id`.
- Cột riêng: `cohort_id uuid NOT NULL`; `affiliation_id uuid NOT NULL`; `joined_at timestamptz NOT NULL`; `left_at timestamptz NULL`.
- Ràng buộc: khóa ngoại ghép `(tenant_id,cohort_id)` tới `cohorts` và `(tenant_id,affiliation_id)` tới `student_affiliations`; duy nhất một phần trên `(tenant_id,cohort_id,affiliation_id)` khi còn hiệu lực; ngày rời không trước ngày tham gia.
- Chỉ mục: `(tenant_id,cohort_id,left_at)`; `(tenant_id,affiliation_id)`.

#### TBL-WRK-026 — `internship_programs`

- Tập cột: `TENANT_ENTITY` với `tenant_id` FK `university_tenants.id`.
- Cột riêng: `code varchar(80) NOT NULL`; `name varchar(200) NOT NULL`; `description text NOT NULL`; `starts_on date NOT NULL`; `ends_on date NOT NULL`; `status varchar(24) NOT NULL DEFAULT 'DRAFT'`; `eligibility_rule jsonb NOT NULL`; `created_by_subject_id uuid NOT NULL`; `published_at timestamptz NULL`; `closed_at timestamptz NULL`.
- Ràng buộc: duy nhất `(tenant_id,code)`; ngày kết thúc không trước ngày bắt đầu; `status` là `DRAFT|PUBLISHED|CLOSED|CANCELLED`; điều kiện tham gia được kiểm theo lược đồ.
- Chỉ mục: `(tenant_id,status,starts_on)`.

#### TBL-WRK-027 — `campus_job_distributions`

- Tập cột: `TENANT_ENTITY` với `tenant_id` FK `university_tenants.id`.
- Cột riêng: `job_id uuid NOT NULL`; `program_id uuid NULL`; `cohort_id uuid NULL`; `distributed_by_subject_id uuid NOT NULL`; `distributed_at timestamptz NOT NULL`; `expires_at timestamptz NULL`; `message varchar(1000) NULL`; `withdrawn_at timestamptz NULL`.
- Ràng buộc: khóa ngoại ghép theo tổ chức tới chương trình/nhóm; có ít nhất một đối tượng nhận; duy nhất một phần trên `(tenant_id,job_id,program_id,cohort_id)` khi còn hiệu lực.
- Chỉ mục: `(tenant_id,distributed_at DESC)`; `(job_id,withdrawn_at)`.

#### TBL-WRK-028 — `partnerships`

- Tập cột: `TENANT_ENTITY` với `tenant_id` FK `university_tenants.id`.
- Cột riêng: `enterprise_tenant_id uuid NOT NULL` FK `enterprise_tenants.id`; `status varchar(24) NOT NULL DEFAULT 'PROPOSED'`; `scope jsonb NOT NULL`; `starts_on date NULL`; `ends_on date NULL`; `proposed_by_subject_id uuid NOT NULL`; `accepted_by_subject_id uuid NULL`; `accepted_at timestamptz NULL`; `ended_at timestamptz NULL`.
- Ràng buộc: duy nhất một phần trên `(tenant_id,enterprise_tenant_id)` khi còn hiệu lực; `status` là `PROPOSED|ACTIVE|DECLINED|ENDED`; khoảng ngày hợp lệ.
- Chỉ mục: `(tenant_id,status)`; `(enterprise_tenant_id,status)`.

#### TBL-WRK-029 — `candidate_referrals`

- Tập cột: `TENANT_ENTITY` với `tenant_id` FK `university_tenants.id`.
- Cột riêng: `candidate_id uuid NOT NULL` FK `candidate_profiles.id`; `job_id uuid NOT NULL`; `affiliation_id uuid NOT NULL`; `referred_by_subject_id uuid NOT NULL`; `consent_grant_id uuid NOT NULL`; `status varchar(24) NOT NULL DEFAULT 'SENT'`; `message varchar(1000) NULL`; `sent_at timestamptz NOT NULL`; `responded_at timestamptz NULL`.
- Ràng buộc: khóa ngoại ghép đến tư cách sinh viên; duy nhất `(tenant_id,candidate_id,job_id)`; `status` là `SENT|VIEWED|ACCEPTED|DECLINED|EXPIRED`; sự đồng ý phải còn hiệu lực và đúng phạm vi.
- Chỉ mục: `(tenant_id,status,sent_at DESC)`; `(candidate_id,sent_at DESC)`.

#### TBL-WRK-030 — `data_consent_grants`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `candidate_id uuid NOT NULL` FK `candidate_profiles.id`; `grantee_type varchar(24) NOT NULL`; `grantee_tenant_id uuid NOT NULL`; `scope varchar(40)[] NOT NULL`; `purpose varchar(500) NOT NULL`; `valid_from timestamptz NOT NULL`; `valid_until timestamptz NOT NULL`; `policy_version integer NOT NULL`; `granted_at timestamptz NOT NULL`; `withdrawn_at timestamptz NULL`; `withdrawal_reason varchar(500) NULL`.
- Ràng buộc: bên nhận là `UNIVERSITY|ENTERPRISE`; `scope` thuộc danh sách cho phép và không rỗng; `valid_until>valid_from`; rút sự đồng ý theo một chiều. Không dùng khóa ngoại đa hình; dịch vụ kiểm đúng bảng tổ chức.
- Chỉ mục: `(candidate_id,grantee_type,grantee_tenant_id,withdrawn_at,valid_until)`; giữ 24 tháng.

#### TBL-WRK-031 — `university_report_runs`

- Tập cột: `TENANT_ENTITY` với `tenant_id` FK `university_tenants.id`.
- Cột riêng: `report_code varchar(80) NOT NULL`; `filters jsonb NOT NULL`; `period_start date NOT NULL`; `period_end date NOT NULL`; `status varchar(20) NOT NULL DEFAULT 'QUEUED'`; `requested_by_subject_id uuid NOT NULL`; `result_metrics jsonb NULL`; `group_size_min integer NOT NULL DEFAULT 10`; `source_high_watermark timestamptz NULL`; `completed_at timestamptz NULL`; `expires_at timestamptz NOT NULL`.
- Ràng buộc: `group_size_min>=10`; `status` là `QUEUED|RUNNING|READY|FAILED|EXPIRED`; kết quả tuyệt đối không chứa nhóm dưới 10 người hoặc PII ở cấp từng dòng.
- Chỉ mục: `(tenant_id,status,created_at DESC)`; thời hạn lưu giữ 13 tháng.

### 6.5 Việc làm bất biến, kiểm duyệt và tìm nguồn ứng viên

#### TBL-WRK-032 — `jobs`

- Tập cột: `TENANT_ENTITY` với `tenant_id` FK `enterprise_tenants.id`.
- Cột riêng: `slug varchar(160) NOT NULL`; `status job_status NOT NULL DEFAULT 'DRAFT'`; `current_draft_revision_id uuid NULL`; `published_revision_id uuid NULL`; `created_by_subject_id uuid NOT NULL`; `published_at timestamptz NULL`; `paused_at timestamptz NULL`; `closed_at timestamptz NULL`; `expires_at timestamptz NULL`; `taken_down_at timestamptz NULL`; `terminal_reason_code varchar(80) NULL`.
- Ràng buộc: duy nhất `(tenant_id,slug)`; chuyển trạng thái theo vòng đời chuẩn; các dấu thời gian phải phù hợp; trạng thái kết thúc không quay lại `PUBLISHED`.
- Chỉ mục: `(tenant_id,status,updated_at DESC)`; `(status,published_at DESC)`; chỉ mục một phần trên `(expires_at)` cho các trạng thái `PUBLISHED|PAUSED`.

#### TBL-WRK-033 — `job_revisions`

- Tập cột: `ENTITY`; chỉ sửa bằng `row_version` khi `DRAFT`, bất biến từ lúc gửi duyệt/xuất bản.
- Cột riêng: `tenant_id uuid NOT NULL`; `job_id uuid NOT NULL`; `revision_no integer NOT NULL`; `status job_revision_status NOT NULL DEFAULT 'DRAFT'`; `title varchar(200) NOT NULL`; `description_markdown text NOT NULL`; `requirements_markdown text NOT NULL`; `benefits_markdown text NULL`; `employment_type varchar(24) NOT NULL`; `work_mode varchar(16) NOT NULL`; `location_codes varchar(20)[] NOT NULL`; `salary_min_vnd bigint NULL`; `salary_max_vnd bigint NULL`; `salary_visible boolean NOT NULL DEFAULT false`; `headcount integer NOT NULL DEFAULT 1`; `application_deadline timestamptz NULL`; `content_hash char(64) NOT NULL`; `created_by_subject_id uuid NOT NULL`; `submitted_at timestamptz NULL`; `approved_at timestamptz NULL`; `published_at timestamptz NULL`; `superseded_at timestamptz NULL`; `discarded_at timestamptz NULL`; `source_revision_id uuid NULL` self-FK.
- Ràng buộc: khóa ngoại ghép `(tenant_id,job_id)` tới `jobs`; duy nhất `(job_id,revision_no)`; lương tối thiểu/tối đa hợp lệ; số lượng cần tuyển 1–10000; HTML được làm sạch; bản `PUBLISHED` là bất biến.
- Chỉ mục: `(tenant_id,job_id,revision_no DESC)`; GIN tìm kiếm toàn văn trên tiêu đề/mô tả/yêu cầu; GIN trên địa điểm; `(status,submitted_at)`.

#### TBL-WRK-034 — `job_skill_requirements`

- Tập cột: `ENTITY`; chỉ sửa khi bản sửa việc làm cha còn `DRAFT`, bất biến sau khi gửi duyệt.
- Cột riêng: `tenant_id uuid NOT NULL`; `job_revision_id uuid NOT NULL` FK `job_revisions.id`; `skill_id uuid NOT NULL` FK `skills.id`; `required_level smallint NULL`; `min_years numeric(4,1) NULL`; `is_required boolean NOT NULL DEFAULT false`; `weight numeric(5,2) NOT NULL DEFAULT 1`.
- Ràng buộc: duy nhất `(job_revision_id,skill_id)`; cấp độ 1–5; số năm 0–80; trọng số 0–100; tổ chức khớp bản sửa.
- Chỉ mục: `(skill_id,job_revision_id)`; `(tenant_id,job_revision_id)`.

#### TBL-WRK-035 — `job_review_decisions`

- Tập cột: `APPEND`.
- Cột riêng: `tenant_id uuid NOT NULL`; `job_id uuid NOT NULL`; `job_revision_id uuid NOT NULL`; `reviewer_subject_id uuid NOT NULL`; `decision varchar(24) NOT NULL`; `reason_codes varchar(80)[] NOT NULL`; `comment varchar(2000) NULL`; `expected_job_version bigint NOT NULL`; `trace_id varchar(64) NOT NULL`.
- Ràng buộc: tổ chức/việc làm/bản sửa nhất quán; `decision` là `APPROVE|REJECT|REQUEST_CHANGES|TAKE_DOWN`; yêu cầu lý do khi không phê duyệt; xung đột giữa hai người duyệt được giải bằng khóa lạc quan.
- Chỉ mục: `(job_revision_id,occurred_at DESC)`; `(reviewer_subject_id,occurred_at DESC)`; 24 tháng.

#### TBL-WRK-036 — `job_status_history`

- Tập cột: `APPEND`.
- Cột riêng: `tenant_id uuid NOT NULL`; `job_id uuid NOT NULL`; `from_status job_status NULL`; `to_status job_status NOT NULL`; `actor_subject_id uuid NULL`; `reason_code varchar(80) NOT NULL`; `job_revision_id uuid NULL`; `trace_id varchar(64) NOT NULL`.
- Ràng buộc: chuyển trạng thái thuộc máy trạng thái đã định nghĩa; tổ chức/việc làm nhất quán.
- Chỉ mục: `(job_id,occurred_at,id)`; `(tenant_id,to_status,occurred_at DESC)`; 24 tháng.

#### TBL-WRK-037 — `candidate_search_documents`

- Tập cột: `ENTITY`.
- Cột riêng: `candidate_id uuid NOT NULL UNIQUE` FK `candidate_profiles.id`; `visibility candidate_visibility NOT NULL`; `search_vector tsvector NULL`; `skill_ids uuid[] NOT NULL DEFAULT '{}'`; `location_codes varchar(20)[] NOT NULL DEFAULT '{}'`; `experience_months integer NULL`; `headline_redacted varchar(200) NULL`; `source_version bigint NOT NULL`; `indexed_at timestamptz NULL`; `remove_by timestamptz NULL`; `removed_at timestamptz NULL`.
- Ràng buộc: không chứa thông tin liên hệ, CV, minh chứng Học tập, ngày học chính xác hoặc nhân khẩu học nhạy cảm; `PRIVATE` yêu cầu vectơ không có giá trị sau khi gỡ; rút quyền tìm kiếm đặt `remove_by<=now()+5 minutes`.
- Chỉ mục: GIN trên `search_vector`; GIN trên các mảng kỹ năng/địa điểm; `(visibility,indexed_at)`; chỉ mục một phần trên `(remove_by)` cho dữ liệu chưa gỡ. Đây là bản chiếu có thể dựng lại.

#### TBL-WRK-038 — `candidate_invitations`

- Tập cột: `TENANT_ENTITY` với `tenant_id` FK `enterprise_tenants.id`.
- Cột riêng: `job_id uuid NOT NULL`; `candidate_id uuid NOT NULL` FK `candidate_profiles.id`; `invited_by_subject_id uuid NOT NULL`; `message varchar(1000) NULL`; `status varchar(24) NOT NULL DEFAULT 'SENT'`; `sent_at timestamptz NOT NULL`; `viewed_at timestamptz NULL`; `responded_at timestamptz NULL`; `expires_at timestamptz NOT NULL`.
- Ràng buộc: duy nhất `(tenant_id,job_id,candidate_id)`; `status` là `SENT|VIEWED|ACCEPTED|DECLINED|EXPIRED`; thư mời không tạo đơn ứng tuyển/cuộc trò chuyện.
- Chỉ mục: `(candidate_id,status,sent_at DESC)`; `(tenant_id,job_id,status)`.

#### TBL-WRK-039 — `talent_lists`

- Tập cột: `TENANT_ENTITY` với `tenant_id` FK `enterprise_tenants.id`.
- Cột riêng: `name varchar(160) NOT NULL`; `description varchar(1000) NULL`; `created_by_subject_id uuid NOT NULL`; `archived_at timestamptz NULL`.
- Ràng buộc: duy nhất một phần trên `(tenant_id,name)` khi còn hiệu lực.
- Chỉ mục: `(tenant_id,archived_at,updated_at DESC)`.

#### TBL-WRK-040 — `talent_list_items`

- Tập cột: `TENANT_ENTITY` với `tenant_id` FK `enterprise_tenants.id`.
- Cột riêng: `list_id uuid NOT NULL`; `candidate_id uuid NOT NULL` FK `candidate_profiles.id`; `added_by_subject_id uuid NOT NULL`; `source varchar(24) NOT NULL`; `removed_at timestamptz NULL`.
- Ràng buộc: khóa ngoại ghép `(tenant_id,list_id)` tới `talent_lists`; duy nhất một phần trên `(tenant_id,list_id,candidate_id)` khi còn hiệu lực; chỉ thêm ứng viên đang `SEARCHABLE` hoặc đã có đơn ứng tuyển trong tổ chức.
- Chỉ mục: `(tenant_id,list_id,removed_at,created_at DESC)`; rút quyền tìm kiếm làm ẩn mục có nguồn từ tìm kiếm trong 5 phút.

### 6.6 Đơn ứng tuyển, ảnh chụp dữ liệu và ATS

#### TBL-WRK-041 — `applications`

- Tập cột: `TENANT_ENTITY` với `tenant_id` FK `enterprise_tenants.id`.
- Cột riêng: `candidate_id uuid NOT NULL` FK `candidate_profiles.id`; `job_id uuid NOT NULL`; `job_revision_id uuid NOT NULL`; `status application_status NOT NULL DEFAULT 'SUBMITTED'`; `submitted_at timestamptz NOT NULL`; `source varchar(24) NOT NULL`; `current_assignee_subject_id uuid NULL`; `last_status_at timestamptz NOT NULL`; `withdrawn_at timestamptz NULL`; `terminal_at timestamptz NULL`; `consent_policy_version integer NOT NULL`; `row_security_key uuid NOT NULL`.
- Ràng buộc: duy nhất `(candidate_id,job_id)`; tổ chức/việc làm/bản sửa nhất quán; bản sửa phải là ảnh chụp `PUBLISHED` lúc nộp đơn; chuyển trạng thái theo vòng đời chuẩn; dấu thời gian kết thúc đúng.
- Chỉ mục: `(candidate_id,submitted_at DESC)`; `(tenant_id,job_id,status,submitted_at DESC)`; `(tenant_id,current_assignee_subject_id,status)`.
- Xử lý đồng thời: giao dịch nộp đơn dùng ràng buộc duy nhất làm cơ chế phân xử; không kiểm tra rồi chèn ở ngoài giao dịch.

#### TBL-WRK-042 — `application_snapshots`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `tenant_id uuid NOT NULL`; `application_id uuid NOT NULL UNIQUE`; `candidate_profile_snapshot jsonb NOT NULL`; `cv_version_id uuid NOT NULL`; `cv_snapshot jsonb NOT NULL`; `portfolio_snapshot jsonb NOT NULL DEFAULT '[]'`; `cover_letter_snapshot text NULL`; `screening_answers_snapshot jsonb NOT NULL DEFAULT '[]'`; `job_revision_id uuid NOT NULL`; `job_snapshot jsonb NOT NULL`; `schema_version integer NOT NULL`; `snapshot_hash char(64) NOT NULL`; `captured_at timestamptz NOT NULL`.
- Ràng buộc: tổ chức/đơn ứng tuyển nhất quán; các ảnh chụp dữ liệu được kiểm theo lược đồ, bất biến và chỉ chứa dữ liệu ứng viên đã xác nhận; CV/việc làm/minh chứng không được đọc trực tiếp khi đánh giá đơn ứng tuyển.
- Chỉ mục: `(tenant_id,application_id)`; lưu 12 tháng sau trạng thái kết thúc, có thể kéo dài khi tạm giữ pháp lý.

#### TBL-WRK-043 — `application_evidence_selections`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `tenant_id uuid NOT NULL`; `application_id uuid NOT NULL`; `study_evidence_id uuid NOT NULL`; `selected_by_subject_id uuid NOT NULL`; `consent_id uuid NOT NULL`; `consent_policy_version integer NOT NULL`; `selected_at timestamptz NOT NULL`.
- Ràng buộc: duy nhất `(application_id,study_evidence_id)`; ứng viên phải là chủ đơn ứng tuyển; các ID được chọn do người học xác nhận rõ; Dịch vụ Việc làm không có kho minh chứng dùng chung toàn cục.
- Chỉ mục: `(application_id,selected_at)`; giữ kiểm toán 24 tháng, nội dung ảnh chụp theo thời hạn lưu giữ của đơn ứng tuyển.

#### TBL-WRK-044 — `evidence_export_requests`

- Tập cột: `ENTITY`.
- Cột riêng: `tenant_id uuid NOT NULL`; `application_id uuid NOT NULL`; `request_id uuid NOT NULL UNIQUE`; `selected_evidence_ids uuid[] NOT NULL`; `consent_id uuid NOT NULL`; `status evidence_export_status NOT NULL DEFAULT 'PENDING'`; `attempt_count integer NOT NULL DEFAULT 0`; `next_retry_at timestamptz NULL`; `last_error_code varchar(80) NULL`; `sent_at timestamptz NULL`; `completed_at timestamptz NULL`; `request_payload_hash char(64) NOT NULL`.
- Ràng buộc: duy nhất `(application_id,request_id)`; các ID không rỗng/trùng; `attempt_count>=0`; giao dịch đơn ứng tuyển tạo lựa chọn, yêu cầu và hộp thư đi cùng lúc; Dịch vụ Học tập ngừng hoạt động không làm hoàn tác đơn ứng tuyển.
- Chỉ mục: `(status,next_retry_at,id)` cho tiến trình nền; `(application_id,created_at DESC)`.

#### TBL-WRK-045 — `application_evidence_snapshots`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `tenant_id uuid NOT NULL`; `application_id uuid NOT NULL`; `study_evidence_id uuid NOT NULL`; `request_id uuid NOT NULL`; `result_status evidence_export_status NOT NULL`; `evidence_type varchar(32) NULL`; `title varchar(200) NULL`; `description varchar(1000) NULL`; `issuer varchar(160) NULL`; `issued_at timestamptz NULL`; `source_version_id uuid NULL`; `claims_snapshot jsonb NULL`; `claims_hash char(64) NULL`; `signature_verification jsonb NULL`; `received_at timestamptz NULL`; `unavailable_reason_code varchar(80) NULL`.
- Ràng buộc: duy nhất `(application_id,study_evidence_id)`; `result_status` chỉ là `READY|UNAVAILABLE`; `READY` yêu cầu ảnh chụp tối thiểu/hàm băm/xác minh; `UNAVAILABLE` không chứa giả định tiêu cực. Ảnh chụp dữ liệu tuyệt đối không được cập nhật khi sự đồng ý/thu hồi thay đổi.
- Chỉ mục: `(application_id,result_status)`; `(study_evidence_id,result_status)`; lưu 12 tháng sau trạng thái kết thúc, giữ siêu dữ liệu kiểm toán 24 tháng.

#### TBL-WRK-046 — `application_status_history`

- Tập cột: `APPEND`.
- Cột riêng: `tenant_id uuid NOT NULL`; `application_id uuid NOT NULL`; `from_status application_status NULL`; `to_status application_status NOT NULL`; `actor_subject_id uuid NOT NULL`; `reason_code varchar(80) NOT NULL`; `comment varchar(1000) NULL`; `expected_application_version bigint NOT NULL`; `source varchar(24) NOT NULL`; `trace_id varchar(64) NOT NULL`.
- Ràng buộc: chuyển trạng thái theo chuẩn; đơn ứng tuyển/tổ chức nhất quán; AI không được là chủ thể/nguồn đổi trạng thái.
- Chỉ mục: `(application_id,occurred_at,id)`; `(tenant_id,to_status,occurred_at DESC)`; chỉ bổ sung.

#### TBL-WRK-047 — `application_assignments`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `tenant_id uuid NOT NULL`; `application_id uuid NOT NULL`; `assignee_subject_id uuid NOT NULL`; `assigned_by_subject_id uuid NOT NULL`; `assigned_at timestamptz NOT NULL`; `unassigned_at timestamptz NULL`; `unassigned_by_subject_id uuid NULL`; `reason varchar(500) NULL`.
- Ràng buộc: duy nhất một phần trên `(application_id,assignee_subject_id)` khi còn hiệu lực; người được phân công là `RECRUITER|HIRING_MANAGER` còn hiệu lực trong cùng tổ chức; chủ thể/thời điểm bỏ phân công phải cùng tồn tại.
- Chỉ mục: `(tenant_id,assignee_subject_id,unassigned_at,assigned_at DESC)`.

#### TBL-WRK-048 — `application_notes`

- Tập cột: `TENANT_ENTITY` với `tenant_id` FK `enterprise_tenants.id`.
- Cột riêng: `application_id uuid NOT NULL`; `author_subject_id uuid NOT NULL`; `body text NOT NULL`; `visibility varchar(24) NOT NULL DEFAULT 'RECRUITING_TEAM'`; `edited_at timestamptz NULL`; `deleted_at timestamptz NULL`; `content_hash char(64) NOT NULL`.
- Ràng buộc: `visibility` là `PRIVATE_AUTHOR|RECRUITING_TEAM`; người viết có tư cách thành viên còn hiệu lực; sửa/xóa giữ kiểm toán trước/sau; cấm thuộc tính được bảo vệ/nhạy cảm theo chính sách.
- Chỉ mục: `(tenant_id,application_id,created_at DESC)`; `DERIVED_SENSITIVE`; 12 tháng sau trạng thái kết thúc hoặc theo tạm giữ pháp lý.

### 6.7 Phỏng vấn và lịch nội bộ

#### TBL-WRK-049 — `interviews`

- Tập cột: `TENANT_ENTITY` với `tenant_id` FK `enterprise_tenants.id`.
- Cột riêng: `application_id uuid NOT NULL`; `status interview_status NOT NULL DEFAULT 'PROPOSED'`; `current_schedule_version integer NOT NULL DEFAULT 1`; `title varchar(200) NOT NULL`; `interview_type varchar(24) NOT NULL`; `location_text varchar(500) NULL`; `meeting_url varchar(2048) NULL`; `timezone varchar(64) NOT NULL`; `created_by_subject_id uuid NOT NULL`; `cancelled_at timestamptz NULL`; `completed_at timestamptz NULL`; `no_show_party varchar(16) NULL`.
- Ràng buộc: đơn ứng tuyển/tổ chức nhất quán; `interview_type` là `PHONE|VIDEO|ONSITE`; URL cuộc họp HTTPS chỉ dành cho `VIDEO`; dấu thời gian phù hợp `status`; V1 không tích hợp OAuth của Google/Microsoft.
- Chỉ mục: `(tenant_id,application_id,created_at DESC)`; `(tenant_id,status,updated_at)`.

#### TBL-WRK-050 — `interview_schedule_versions`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `tenant_id uuid NOT NULL`; `interview_id uuid NOT NULL`; `version_no integer NOT NULL`; `starts_at timestamptz NOT NULL`; `ends_at timestamptz NOT NULL`; `timezone varchar(64) NOT NULL`; `proposed_by_subject_id uuid NOT NULL`; `change_reason varchar(1000) NULL`; `supersedes_version_id uuid NULL` self-FK; `created_ics_sequence integer NOT NULL`; `content_hash char(64) NOT NULL`.
- Ràng buộc: duy nhất `(interview_id,version_no)`; kết thúc sau bắt đầu; tổ chức nhất quán; đổi lịch tạo phiên bản mới, không sửa phiên bản cũ. Chỉ nhân sự tổ chức có quyền điều phối mới tạo phiên bản lịch; ứng viên chỉ phản hồi hoặc yêu cầu đổi lịch ở tầng API.
- Chỉ mục: `(interview_id,version_no DESC)`; `(tenant_id,starts_at,ends_at)`.

#### TBL-WRK-051 — `interview_participants`

- Tập cột: `TENANT_ENTITY` với `tenant_id` FK `enterprise_tenants.id`.
- Cột riêng: `interview_id uuid NOT NULL`; `identity_subject_id uuid NOT NULL`; `participant_role varchar(24) NOT NULL`; `response varchar(24) NOT NULL DEFAULT 'PENDING'`; `responded_at timestamptz NULL`; `last_notified_schedule_version integer NOT NULL DEFAULT 0`.
- Ràng buộc: duy nhất `(interview_id,identity_subject_id)`; `participant_role` là `CANDIDATE|INTERVIEWER|ORGANIZER`; `response` là `PENDING|ACCEPTED|DECLINED|TENTATIVE`; ứng viên phải là chủ đơn ứng tuyển, nhân sự phải có tư cách thành viên còn hiệu lực.
- Chỉ mục: `(identity_subject_id,response,updated_at DESC)`; `(tenant_id,interview_id)`.

#### TBL-WRK-052 — `interview_status_history`

- Tập cột: `APPEND`.
- Cột riêng: `tenant_id uuid NOT NULL`; `interview_id uuid NOT NULL`; `from_status interview_status NULL`; `to_status interview_status NOT NULL`; `schedule_version integer NOT NULL`; `actor_subject_id uuid NOT NULL`; `reason_code varchar(80) NOT NULL`; `trace_id varchar(64) NOT NULL`.
- Ràng buộc: chuyển trạng thái theo chuẩn và tổ chức nhất quán; hoàn tất/vắng mặt/hủy là trạng thái kết thúc.
- Chỉ mục: `(interview_id,occurred_at,id)`; 24 tháng.

### 6.8 Trò chuyện theo phạm vi đơn ứng tuyển

#### TBL-WRK-053 — `conversations`

- Tập cột: `TENANT_ENTITY` với `tenant_id` FK `enterprise_tenants.id`.
- Cột riêng: `application_id uuid NOT NULL UNIQUE`; `status conversation_status NOT NULL DEFAULT 'ACTIVE'`; `candidate_subject_id uuid NOT NULL`; `recruiter_subject_id uuid NOT NULL`; `opened_at timestamptz NOT NULL`; `read_only_at timestamptz NULL`; `last_message_at timestamptz NULL`; `last_message_id uuid NULL`.
- Ràng buộc: đúng một cuộc trò chuyện mỗi đơn ứng tuyển; chỉ tạo sau khi có đơn; nhà tuyển dụng phải được phân công và có tư cách thành viên còn hiệu lực; đơn ứng tuyển kết thúc chuyển cuộc trò chuyện sang `READ_ONLY` theo giao dịch hoặc cuối cùng hội tụ theo cơ chế lặp an toàn.
- Chỉ mục: `(candidate_subject_id,last_message_at DESC)`; `(tenant_id,recruiter_subject_id,last_message_at DESC)`; `(application_id)`.

#### TBL-WRK-054 — `messages`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `tenant_id uuid NOT NULL`; `conversation_id uuid NOT NULL`; `sender_subject_id uuid NULL`; `client_message_id uuid NOT NULL`; `message_type varchar(16) NOT NULL DEFAULT 'TEXT'`; `body text NOT NULL`; `sent_at timestamptz NOT NULL`; `server_sequence bigint NOT NULL`; `deleted_for_all_at timestamptz NULL`; `moderation_status varchar(24) NOT NULL DEFAULT 'CLEAR'`; `content_hash char(64) NOT NULL`.
- Ràng buộc: duy nhất `(conversation_id,client_message_id)` và `(conversation_id,server_sequence)`; `message_type` chỉ là `TEXT|SYSTEM`; văn bản dài 1–5000 ký tự sau khi loại bỏ khoảng trắng và không chứa HTML thực thi; `TEXT` yêu cầu người gửi là người tham gia, `SYSTEM` yêu cầu người gửi để trống và chỉ tiến trình nền có quyền chèn; cuộc trò chuyện ở trạng thái `ACTIVE`; chỉ được xóa nội dung trong 15 phút và vẫn lưu kiểm toán/hàm băm/số thứ tự. V1 không có tệp đính kèm trong trò chuyện.
- Chỉ mục: `(conversation_id,server_sequence DESC)` cho con trỏ REST; `(sender_subject_id,sent_at DESC)`; 12 tháng sau trạng thái kết thúc.

#### TBL-WRK-055 — `conversation_read_cursors`

- Tập cột: `ENTITY`.
- Cột riêng: `tenant_id uuid NOT NULL`; `conversation_id uuid NOT NULL`; `identity_subject_id uuid NOT NULL`; `last_read_sequence bigint NOT NULL DEFAULT 0`; `last_read_at timestamptz NULL`.
- Ràng buộc: duy nhất `(conversation_id,identity_subject_id)`; con trỏ chỉ tăng; chủ thể là người tham gia.
- Chỉ mục: `(identity_subject_id,updated_at DESC)`.

#### TBL-WRK-056 — `websocket_connection_leases`

- Tập cột: `ENTITY`.
- Cột riêng: `identity_subject_id uuid NOT NULL`; `connection_id uuid NOT NULL UNIQUE`; `node_id varchar(120) NOT NULL`; `connected_at timestamptz NOT NULL`; `last_heartbeat_at timestamptz NOT NULL`; `expires_at timestamptz NOT NULL`; `revoked_at timestamptz NULL`.
- Ràng buộc: hết hạn sau nhịp tim; quyền thuê là dữ liệu tạm thời, PostgreSQL là sổ đăng ký dự phòng còn Redis dùng để phân phối thời gian thực.
- Chỉ mục: `(identity_subject_id,expires_at)`; `(expires_at)`; dọn trong 24 giờ.

### 6.9 AI và đối sánh có người duyệt

#### TBL-AIX-001 — `ai_model_versions`

- Tập cột: `ENTITY`.
- Cột riêng: `provider varchar(40) NOT NULL`; `model_key varchar(160) NOT NULL`; `version varchar(120) NOT NULL`; `capability varchar(40) NOT NULL`; `endpoint_config_ref varchar(300) NOT NULL`; `data_residency varchar(80) NOT NULL`; `enabled boolean NOT NULL DEFAULT false`; `activated_at timestamptz NULL`; `retired_at timestamptz NULL`; `risk_class varchar(24) NOT NULL`.
- Ràng buộc: duy nhất `(provider,model_key,version,capability)`; nhà cung cấp mặc định của đợt thí điểm là `OLLAMA`; cấu hình chỉ là tham chiếu đến trình quản lý bí mật.
- Chỉ mục: `(capability,enabled,activated_at DESC)`; INTERNAL.

#### TBL-AIX-002 — `ai_prompt_versions`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `prompt_code varchar(80) NOT NULL`; `version_no integer NOT NULL`; `capability varchar(40) NOT NULL`; `system_prompt text NOT NULL`; `input_schema jsonb NOT NULL`; `output_schema jsonb NOT NULL`; `excluded_fields varchar(120)[] NOT NULL`; `injection_policy_version integer NOT NULL`; `created_by_subject_id uuid NOT NULL`; `approved_by_subject_id uuid NOT NULL`; `activated_at timestamptz NULL`; `retired_at timestamptz NULL`; `content_hash char(64) NOT NULL`.
- Ràng buộc: duy nhất `(prompt_code,version_no)`; áp dụng nguyên tắc người tạo–người kiểm tra; danh sách trường loại trừ tối thiểu chứa thuộc tính được bảo vệ/nhạy cảm theo năng lực.
- Chỉ mục: `(prompt_code,activated_at DESC)`; không sửa lời nhắc đã dùng.

#### TBL-AIX-003 — `ai_policy_versions`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `policy_code varchar(80) NOT NULL`; `version_no integer NOT NULL`; `capability varchar(40) NOT NULL`; `rules jsonb NOT NULL`; `allowed_input_fields varchar(120)[] NOT NULL`; `forbidden_actions varchar(120)[] NOT NULL`; `approved_by_subject_id uuid NOT NULL`; `activated_at timestamptz NOT NULL`; `retired_at timestamptz NULL`; `content_hash char(64) NOT NULL`.
- Ràng buộc: duy nhất `(policy_code,version_no)`; các hành động cấm luôn gồm thay đổi trạng thái ATS, tự động từ chối và tự động tuyển dụng.
- Chỉ mục: `(capability,activated_at DESC)`.

#### TBL-AIX-004 — `ai_jobs`

- Tập cột: `ENTITY`.
- Cột riêng: `tenant_id uuid NULL`; `actor_subject_id uuid NOT NULL`; `capability varchar(40) NOT NULL`; `resource_type varchar(40) NOT NULL`; `resource_id uuid NOT NULL`; `model_version_id uuid NOT NULL` FK `ai_model_versions.id`; `prompt_version_id uuid NOT NULL` FK `ai_prompt_versions.id`; `policy_version_id uuid NOT NULL` FK `ai_policy_versions.id`; `status ai_job_status NOT NULL DEFAULT 'QUEUED'`; `input_snapshot_redacted jsonb NOT NULL`; `input_hash char(64) NOT NULL`; `queued_at timestamptz NOT NULL`; `started_at timestamptz NULL`; `completed_at timestamptz NULL`; `attempt_count integer NOT NULL DEFAULT 0`; `last_error_code varchar(80) NULL`; `kill_switch_snapshot boolean NOT NULL`; `trace_id varchar(64) NOT NULL`.
- Ràng buộc: `capability` là `CV_DRAFT|JD_DRAFT|MATCH_EXPLANATION|SHORTLIST_SUGGESTION`; `attempt_count>=0`; đầu vào được kiểm theo lược đồ/chính sách; tác vụ chạy bất đồng bộ; văn bản nguồn được bọc bằng dấu phân cách không tin cậy để chống chèn chỉ dẫn.
- Chỉ mục: `(status,created_at,id)` cho tiến trình nền; `(actor_subject_id,created_at DESC)`; `(tenant_id,resource_type,resource_id,created_at DESC)`.
- Thời hạn lưu giữ: đầu vào/đầu ra 12 tháng hoặc ngắn hơn theo sự đồng ý; siêu dữ liệu kiểm toán 24 tháng.

#### TBL-AIX-005 — `ai_outputs`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `ai_job_id uuid NOT NULL UNIQUE` FK `ai_jobs.id`; `output_json jsonb NOT NULL`; `output_text text NULL`; `output_hash char(64) NOT NULL`; `safety_flags varchar(80)[] NOT NULL DEFAULT '{}'`; `provider_request_id varchar(160) NULL`; `latency_ms integer NOT NULL`; `token_usage jsonb NULL`; `generated_at timestamptz NOT NULL`.
- Ràng buộc: đầu ra được kiểm theo lược đồ; độ trễ >=0; không chứa trường bị loại trừ; ID yêu cầu của nhà cung cấp không chứa bí mật.
- Chỉ mục: `(generated_at)`; DERIVED_SENSITIVE.

#### TBL-AIX-006 — `ai_human_reviews`

- Tập cột: `APPEND`.
- Cột riêng: `ai_job_id uuid NOT NULL` FK `ai_jobs.id`; `output_id uuid NOT NULL` FK `ai_outputs.id`; `reviewer_subject_id uuid NOT NULL`; `decision ai_review_decision NOT NULL`; `edited_output_snapshot jsonb NULL`; `reason_codes varchar(80)[] NOT NULL DEFAULT '{}'`; `comment varchar(2000) NULL`; `applied_to_resource_at timestamptz NULL`; `trace_id varchar(64) NOT NULL`.
- Ràng buộc: `EDITED_ACCEPT` cần ảnh chụp dữ liệu; `REJECTED` cần lý do; chỉ áp dụng sau hành động rõ ràng của con người; trạng thái duyệt đầu ra được suy ra từ lần duyệt cuối (`DRAFT` nếu chưa duyệt, `EXPIRED` nếu quá hạn) và không trộn với `ai_job_status`; một đầu ra có thể được duyệt lại nhưng chỉ có một kết quả cuối được chấp nhận/áp dụng trong giao dịch.
- Chỉ mục: `(ai_job_id,occurred_at DESC)`; `(reviewer_subject_id,occurred_at DESC)`; chỉ bổ sung trong 24 tháng.

#### TBL-AIX-007 — `match_score_snapshots`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `tenant_id uuid NOT NULL`; `job_revision_id uuid NOT NULL`; `candidate_id uuid NOT NULL` FK `candidate_profiles.id`; `application_id uuid NULL`; `algorithm_version varchar(80) NOT NULL`; `feature_policy_version integer NOT NULL`; `allowed_feature_snapshot jsonb NOT NULL`; `score numeric(5,2) NOT NULL`; `explanation jsonb NOT NULL`; `ai_job_id uuid NULL` FK `ai_jobs.id`; `calculated_at timestamptz NOT NULL`; `expires_at timestamptz NOT NULL`.
- Ràng buộc: điểm 0–100; ảnh chụp đặc trưng không chứa thuộc tính được bảo vệ, minh chứng Học tập, trạng thái tài trợ hoặc thông tin liên hệ; điểm chỉ để gợi ý, không thay đổi ATS.
- Chỉ mục: `(tenant_id,job_revision_id,score DESC)`; `(application_id,calculated_at DESC)`; DERIVED_SENSITIVE.

#### TBL-AIX-008 — `ai_kill_switches`

- Tập cột: `ENTITY`.
- Cột riêng: `capability varchar(40) NOT NULL UNIQUE`; `disabled boolean NOT NULL DEFAULT false`; `reason varchar(1000) NULL`; `changed_by_subject_id uuid NOT NULL`; `changed_at timestamptz NOT NULL`; `expires_at timestamptz NULL`.
- Ràng buộc: `disabled` cần lý do; mọi thay đổi được kiểm toán; tiến trình nền kiểm tra trước và sau khi gọi nhà cung cấp.
- Chỉ mục: `(disabled,capability)`.

### 6.10 Lập hóa đơn, thanh toán, quyền sử dụng và quảng bá

#### TBL-PAY-001 — `products`

- Tập cột: `ENTITY`.
- Cột riêng: `code varchar(80) NOT NULL UNIQUE`; `buyer_type varchar(20) NOT NULL`; `name varchar(200) NOT NULL`; `description varchar(2000) NOT NULL`; `product_type varchar(32) NOT NULL`; `entitlement_code varchar(80) NOT NULL`; `credit_amount bigint NULL`; `validity_days integer NOT NULL`; `active_from timestamptz NOT NULL`; `active_until timestamptz NULL`.
- Ràng buộc: bên mua là `CANDIDATE|ENTERPRISE`; loại là `PACKAGE|CREDIT_PACK|PREMIUM_TEMPLATE|SPONSORED_PLACEMENT`; số tín dụng >=0; thời hạn 1–3650 ngày; không tự gia hạn.
- Chỉ mục: `(buyer_type,active_from,active_until)`; phần danh mục đã xuất bản là `PUBLIC`.

#### TBL-PAY-002 — `product_prices`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `product_id uuid NOT NULL` FK `products.id`; `version_no integer NOT NULL`; `currency char(3) NOT NULL DEFAULT 'VND'`; `amount_vnd bigint NOT NULL`; `tax_rate numeric(5,2) NOT NULL DEFAULT 0`; `valid_from timestamptz NOT NULL`; `valid_until timestamptz NULL`; `created_by_subject_id uuid NOT NULL`.
- Ràng buộc: duy nhất `(product_id,version_no)`; số tiền >0; tiền tệ là VND; thuế 0–100; các khoảng hiệu lực không chồng lấn.
- Chỉ mục: `(product_id,valid_from DESC)`.

#### TBL-PAY-003 — `orders`

- Tập cột: `ENTITY`.
- Cột riêng: `order_no varchar(40) NOT NULL UNIQUE`; `buyer_subject_id uuid NOT NULL`; `buyer_type varchar(20) NOT NULL`; `tenant_id uuid NULL`; `status order_status NOT NULL DEFAULT 'CREATED'`; `currency char(3) NOT NULL DEFAULT 'VND'`; `subtotal_vnd bigint NOT NULL`; `tax_vnd bigint NOT NULL`; `total_vnd bigint NOT NULL`; `pricing_snapshot jsonb NOT NULL`; `created_at_client timestamptz NULL`; `expires_at timestamptz NOT NULL`; `settled_at timestamptz NULL`; `failed_at timestamptz NULL`; `cancelled_at timestamptz NULL`; `idempotency_key_hash char(64) NOT NULL`.
- Ràng buộc: duy nhất `(buyer_subject_id,idempotency_key_hash)`; các số tiền >=0, tổng tiền = tạm tính + thuế; bên mua doanh nghiệp yêu cầu tổ chức; không tự gia hạn/ví/ký quỹ/chi trả.
- Chỉ mục: `(buyer_subject_id,created_at DESC)`; `(tenant_id,status,created_at DESC)`; `(status,expires_at)`.

#### TBL-PAY-004 — `order_items`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `order_id uuid NOT NULL` FK `orders.id`; `product_id uuid NOT NULL` FK `products.id`; `price_version_id uuid NOT NULL` FK `product_prices.id`; `quantity integer NOT NULL`; `unit_amount_vnd bigint NOT NULL`; `tax_vnd bigint NOT NULL`; `line_total_vnd bigint NOT NULL`; `product_snapshot jsonb NOT NULL`.
- Ràng buộc: duy nhất `(order_id,product_id,price_version_id)`; số lượng 1–10000; phép tính từng dòng chính xác; ảnh chụp giá/sản phẩm là bất biến.
- Chỉ mục: `(order_id)`.

#### TBL-PAY-005 — `payment_attempts`

- Tập cột: `ENTITY`.
- Cột riêng: `order_id uuid NOT NULL` FK `orders.id`; `attempt_no integer NOT NULL`; `provider payment_provider NOT NULL`; `status payment_status NOT NULL DEFAULT 'CREATED'`; `amount_vnd bigint NOT NULL`; `provider_order_id varchar(160) NOT NULL`; `provider_transaction_id varchar(160) NULL`; `request_payload_hash char(64) NOT NULL`; `response_code varchar(80) NULL`; `checkout_url_ciphertext bytea NULL`; `return_seen_at timestamptz NULL`; `settled_at timestamptz NULL`; `failed_at timestamptz NULL`; `expires_at timestamptz NOT NULL`; `last_provider_occurred_at timestamptz NULL`.
- Ràng buộc: duy nhất `(order_id,attempt_no)`; duy nhất `(provider,provider_order_id)`; duy nhất một phần trên `(provider,provider_transaction_id)` khi có; số tiền bằng tổng đơn hàng; URL trả về không xác lập thanh toán.
- Chỉ mục: `(order_id,attempt_no DESC)`; `(provider,status,updated_at)`; `(status,expires_at)`.

#### TBL-PAY-006 — `payment_webhook_events`

- Tập cột: `APPEND`.
- Cột riêng: `provider payment_provider NOT NULL`; `provider_event_id varchar(200) NOT NULL`; `provider_order_id varchar(160) NOT NULL`; `provider_transaction_id varchar(160) NULL`; `provider_occurred_at timestamptz NULL`; `received_at timestamptz NOT NULL`; `signature_valid boolean NOT NULL`; `source_ip_hash char(64) NULL`; `headers_redacted jsonb NOT NULL`; `payload_ciphertext bytea NOT NULL`; `payload_hash char(64) NOT NULL`; `processing_status varchar(24) NOT NULL DEFAULT 'RECEIVED'`; `processed_at timestamptz NULL`; `result_code varchar(80) NULL`; `trace_id varchar(64) NOT NULL`.
- Ràng buộc: duy nhất `(provider,provider_event_id)`; cơ chế khử trùng lặp dự phòng là duy nhất `(provider,payload_hash)`; chữ ký không hợp lệ chỉ được kiểm toán, không làm thay đổi dữ liệu; xử lý sự kiện đến không theo thứ tự dựa trên `last_provider_occurred_at` và thứ tự ưu tiên trạng thái.
- Chỉ mục: `(processing_status,received_at,id)`; `(provider,provider_order_id,received_at DESC)`; chỉ bổ sung trong 24 tháng hoặc lâu hơn theo chính sách tài chính.

#### TBL-PAY-007 — `payment_reconciliations`

- Tập cột: `APPEND`.
- Cột riêng: `provider payment_provider NOT NULL`; `payment_attempt_id uuid NULL` FK `payment_attempts.id`; `reconciliation_date date NOT NULL`; `provider_status varchar(80) NOT NULL`; `local_status payment_status NULL`; `amount_vnd bigint NOT NULL`; `matched boolean NOT NULL`; `discrepancy_code varchar(80) NULL`; `provider_payload_hash char(64) NOT NULL`; `resolved_at timestamptz NULL`; `resolved_by_subject_id uuid NULL`; `resolution_note varchar(1000) NULL`.
- Ràng buộc: số tiền >=0; không khớp yêu cầu mã chênh lệch; chủ thể/ghi chú giải quyết phải cùng tồn tại.
- Chỉ mục: `(provider,reconciliation_date,matched)`; `(payment_attempt_id,occurred_at DESC)`; 24 tháng+.

#### TBL-PAY-008 — `refunds`

- Tập cột: `ENTITY`.
- Cột riêng: `order_id uuid NOT NULL` FK `orders.id`; `payment_attempt_id uuid NOT NULL` FK `payment_attempts.id`; `refund_no varchar(60) NOT NULL UNIQUE`; `amount_vnd bigint NOT NULL`; `reason_code varchar(80) NOT NULL`; `reason_text varchar(1000) NULL`; `status varchar(24) NOT NULL DEFAULT 'REQUESTED'`; `requested_by_subject_id uuid NOT NULL`; `approved_by_subject_id uuid NULL`; `provider_refund_id varchar(160) NULL`; `requested_at timestamptz NOT NULL`; `processed_at timestamptz NULL`; `failed_at timestamptz NULL`.
- Ràng buộc: số tiền >0 và tổng hoàn tiền đã xác lập không vượt khoản thanh toán; `status` là `REQUESTED|APPROVED|PROCESSING|SETTLED|FAILED|REJECTED`; áp dụng nguyên tắc người tạo–người kiểm tra; mã hoàn tiền của nhà cung cấp là duy nhất khi có.
- Chỉ mục: `(order_id,created_at DESC)`; `(status,created_at)`; 24 tháng+.

#### TBL-PAY-009 — `chargebacks`

- Tập cột: `APPEND`.
- Cột riêng: `payment_attempt_id uuid NOT NULL` FK `payment_attempts.id`; `provider_case_id varchar(160) NOT NULL`; `amount_vnd bigint NOT NULL`; `reason_code varchar(80) NOT NULL`; `status varchar(24) NOT NULL`; `opened_at timestamptz NOT NULL`; `resolved_at timestamptz NULL`; `resolution varchar(80) NULL`; `provider_payload_hash char(64) NOT NULL`.
- Ràng buộc: duy nhất `(payment_attempt_id,provider_case_id)`; số tiền >0; `status` là `OPEN|WON|LOST|CLOSED`; tra soát tạo bút toán đảo/quyền sử dụng bị thu hồi theo cơ chế lặp an toàn.
- Chỉ mục: `(status,opened_at)`; 24 tháng+.

#### TBL-PAY-010 — `entitlements`

- Tập cột: `ENTITY`.
- Cột riêng: `owner_subject_id uuid NOT NULL`; `owner_type varchar(20) NOT NULL`; `tenant_id uuid NULL`; `order_item_id uuid NOT NULL` FK `order_items.id`; `code varchar(80) NOT NULL`; `status entitlement_status NOT NULL DEFAULT 'ACTIVE'`; `quantity_total bigint NOT NULL`; `quantity_consumed bigint NOT NULL DEFAULT 0`; `valid_from timestamptz NOT NULL`; `valid_until timestamptz NULL`; `activated_at timestamptz NOT NULL`; `frozen_at timestamptz NULL`; `revoked_at timestamptz NULL`; `revoke_reason varchar(500) NULL`.
- Ràng buộc: duy nhất `(order_item_id,code)`; `0<=quantity_consumed<=quantity_total`; hàng chỉ được tạo trong giao dịch xác lập thanh toán đã được xác thực, không tồn tại quyền sử dụng `PENDING`; `ACTIVE→EXHAUSTED|EXPIRED|FROZEN|REVOKED`, `FROZEN→ACTIVE|REVOKED`; chủ sở hữu doanh nghiệp yêu cầu tổ chức; thời hạn hiệu lực hợp lệ.
- Chỉ mục: `(owner_subject_id,code,status,valid_until)`; `(tenant_id,code,status,valid_until)`.

#### TBL-PAY-011 — `credit_ledger_entries`

- Tập cột: `APPEND`.
- Cột riêng: `entitlement_id uuid NOT NULL` FK `entitlements.id`; `owner_subject_id uuid NOT NULL`; `tenant_id uuid NULL`; `entry_type ledger_entry_type NOT NULL`; `quantity_delta bigint NOT NULL`; `balance_after bigint NOT NULL`; `reference_type varchar(40) NOT NULL`; `reference_id uuid NOT NULL`; `idempotency_key varchar(180) NOT NULL`; `actor_subject_id uuid NULL`; `reason varchar(500) NULL`.
- Ràng buộc: duy nhất `(entitlement_id,idempotency_key)`; thay đổi số lượng khác 0; số dư >=0; dấu của bút toán phù hợp loại; số dư được tuần tự hóa bằng khóa hàng quyền sử dụng.
- Chỉ mục: `(entitlement_id,occurred_at,id)`; `(tenant_id,occurred_at DESC)`; chỉ bổ sung tối thiểu 24 tháng.

#### TBL-PAY-012 — `promotion_campaigns`

- Tập cột: `ENTITY`.
- Cột riêng: `code varchar(80) NOT NULL UNIQUE`; `name varchar(200) NOT NULL`; `promotion_type varchar(32) NOT NULL`; `sponsor_subject_id uuid NOT NULL`; `sponsor_tenant_id uuid NULL`; `status promotion_status NOT NULL DEFAULT 'SCHEDULED'`; `starts_at timestamptz NOT NULL`; `ends_at timestamptz NOT NULL`; `budget_vnd bigint NULL`; `label_text varchar(120) NOT NULL DEFAULT 'Được tài trợ'`; `targeting_rules jsonb NOT NULL`; `created_by_subject_id uuid NOT NULL`; `approved_by_subject_id uuid NOT NULL`.
- Ràng buộc: loại là `SPONSORED_PROFILE|SPONSORED_JOB`; kết thúc sau bắt đầu; ngân sách >=0; nhãn không rỗng; áp dụng nguyên tắc người tạo–người kiểm tra; chiến dịch không tác động kết quả tự nhiên/đối sánh/ATS.
- Chỉ mục: `(status,starts_at,ends_at)`; `(sponsor_tenant_id,status)`.

#### TBL-PAY-013 — `sponsored_placements`

- Tập cột: `ENTITY`.
- Cột riêng: `campaign_id uuid NOT NULL` FK `promotion_campaigns.id`; `resource_type varchar(24) NOT NULL`; `resource_id uuid NOT NULL`; `entitlement_id uuid NOT NULL` FK `entitlements.id`; `starts_at timestamptz NOT NULL`; `ends_at timestamptz NOT NULL`; `status promotion_status NOT NULL`; `label_text varchar(120) NOT NULL`; `targeting_snapshot jsonb NOT NULL`; `impression_count bigint NOT NULL DEFAULT 0`; `click_count bigint NOT NULL DEFAULT 0`.
- Ràng buộc: tài nguyên là `CANDIDATE_PROFILE|JOB`; thời gian nằm trong chiến dịch; nhãn bắt buộc; ứng viên có thể tìm kiếm phải chủ động cho phép, việc làm phải `PUBLISHED`; thứ hạng tài trợ được lưu riêng và không ghi vào điểm đối sánh.
- Chỉ mục: `(resource_type,status,starts_at,ends_at)`; `(campaign_id,status)`.

#### TBL-PAY-014 — `invoices`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `order_id uuid NOT NULL UNIQUE` FK `orders.id`; `invoice_no varchar(60) NOT NULL UNIQUE`; `buyer_snapshot jsonb NOT NULL`; `tax_snapshot jsonb NOT NULL`; `amount_vnd bigint NOT NULL`; `issued_at timestamptz NOT NULL`; `file_id uuid NOT NULL` FK `file_objects.id`; `content_hash char(64) NOT NULL`; `voided_at timestamptz NULL`; `void_reason varchar(500) NULL`; `replacement_invoice_id uuid NULL` self-FK.
- Ràng buộc: tệp phải `CLEAN`, số tiền bằng số tiền `SETTLED`; sửa sai tạo hóa đơn thay thế, không sửa hóa đơn cũ.
- Chỉ mục: `(issued_at DESC)`; thời hạn lưu giữ tài chính theo luật, tối thiểu 24 tháng.

### 6.11 Thông báo, kiểm duyệt và vận hành Dịch vụ Việc làm

#### TBL-WRK-057 — `notification_preferences`

- Tập cột: `ENTITY`.
- Cột riêng: `identity_subject_id uuid NOT NULL`; `category varchar(40) NOT NULL`; `in_app_enabled boolean NOT NULL DEFAULT true`; `email_enabled boolean NOT NULL DEFAULT true`; `quiet_hours_start time NULL`; `quiet_hours_end time NULL`; `timezone varchar(64) NOT NULL`; `consent_source varchar(40) NOT NULL`.
- Ràng buộc: duy nhất `(identity_subject_id,category)`; danh mục giao dịch/bảo mật không được tắt.
- Chỉ mục: `(identity_subject_id,category)`.

#### TBL-WRK-058 — `notifications`

- Tập cột: `ENTITY`.
- Cột riêng: `identity_subject_id uuid NOT NULL`; `tenant_id uuid NULL`; `category varchar(40) NOT NULL`; `template_code varchar(80) NOT NULL`; `template_version integer NOT NULL`; `title varchar(200) NOT NULL`; `body varchar(4000) NOT NULL`; `action_url varchar(1000) NULL`; `dedupe_key varchar(180) NOT NULL`; `read_at timestamptz NULL`; `expires_at timestamptz NOT NULL`; `payload jsonb NOT NULL DEFAULT '{}'`.
- Ràng buộc: duy nhất `(identity_subject_id,dedupe_key)`; URL thuộc danh sách cho phép; tải tin đã được che dữ liệu.
- Chỉ mục: `(identity_subject_id,read_at,created_at DESC,id DESC)` cho con trỏ; `(expires_at)`; thời hạn lưu giữ 180 ngày.

#### TBL-WRK-059 — `notification_deliveries`

- Tập cột: `APPEND`.
- Cột riêng: `notification_id uuid NOT NULL` FK `notifications.id`; `channel varchar(16) NOT NULL`; `status notification_status NOT NULL`; `provider_message_id varchar(160) NULL`; `attempt_no integer NOT NULL`; `error_code varchar(80) NULL`; `next_retry_at timestamptz NULL`; `dedupe_key varchar(180) NOT NULL`.
- Ràng buộc: duy nhất theo thông báo/kênh/lần thử và theo khóa khử trùng lặp; `channel` là `IN_APP|EMAIL`; `attempt_no>=1`.
- Chỉ mục: `(status,next_retry_at)`; thời hạn lưu giữ 180 ngày.

#### TBL-WRK-060 — `moderation_reports`

- Tập cột: `ENTITY`.
- Cột riêng: `reporter_subject_id uuid NOT NULL`; `tenant_id uuid NULL`; `resource_type varchar(40) NOT NULL`; `resource_id uuid NOT NULL`; `reason_code varchar(80) NOT NULL`; `description varchar(2000) NULL`; `evidence_file_ids uuid[] NOT NULL DEFAULT '{}'`; `status varchar(24) NOT NULL DEFAULT 'OPEN'`; `assigned_to_subject_id uuid NULL`; `decision varchar(80) NULL`; `resolved_at timestamptz NULL`.
- Ràng buộc: `status` là `OPEN|IN_REVIEW|RESOLVED|DISMISSED`; trạng thái kết thúc cần quyết định; các tệp phải `CLEAN`.
- Chỉ mục: `(status,created_at)`; `(resource_type,resource_id,created_at DESC)`; 24 tháng.

#### TBL-WRK-061 — `audit_events`

- Tập cột: `APPEND`.
- Cột riêng: `actor_subject_id uuid NULL`; `action varchar(120) NOT NULL`; `resource_type varchar(80) NOT NULL`; `resource_id uuid NULL`; `outcome audit_outcome NOT NULL`; `business_code varchar(80) NOT NULL`; `trace_id varchar(64) NOT NULL`; `tenant_context jsonb NULL`; `changes jsonb NULL`; `metadata jsonb NOT NULL DEFAULT '{}'`; `prev_hash char(64) NULL`; `event_hash char(64) NOT NULL UNIQUE`; `legal_hold_until timestamptz NULL`.
- Ràng buộc: ngữ cảnh tổ chức có loại/ID/tư cách thành viên; chuỗi hàm băm chuẩn; thay đổi/siêu dữ liệu đã được che; chỉ bổ sung.
- Chỉ mục: tài nguyên/thời gian, chủ thể/thời gian, tổ chức/thời gian, dấu vết, BRIN theo thời điểm xảy ra; lưu tối thiểu 24 tháng.

#### TBL-WRK-062 — `idempotency_keys`

- Tập cột: `ENTITY`.
- Cột riêng: `actor_subject_id uuid NULL`; `operation varchar(120) NOT NULL`; `key_hash char(64) NOT NULL`; `request_hash char(64) NOT NULL`; `response_status integer NULL`; `response_body jsonb NULL`; `locked_until timestamptz NULL`; `completed_at timestamptz NULL`; `expires_at timestamptz NOT NULL`.
- Ràng buộc: duy nhất theo chủ thể/thao tác/khóa; cùng khóa nhưng khác hàm băm yêu cầu trả xung đột; phản hồi được che dữ liệu.
- Chỉ mục: `(expires_at)`; nộp đơn/thanh toán/phỏng vấn/trò chuyện giữ 7 ngày, thay đổi khác giữ 24 giờ.

#### TBL-WRK-063 — `outbox_events`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `aggregate_type varchar(80) NOT NULL`; `aggregate_id uuid NOT NULL`; `event_type varchar(120) NOT NULL`; `event_version integer NOT NULL`; `payload jsonb NOT NULL`; `available_at timestamptz NOT NULL DEFAULT now()`; `dedupe_key varchar(180) NOT NULL UNIQUE`; `trace_id varchar(64) NOT NULL`.
- Ràng buộc: `event_version>=1`; sự kiện có lược đồ/phiên bản/dấu vết; thanh toán `SETTLED` và đơn ứng tuyển tạo mới ghi trong cùng giao dịch tổng hợp; chỉ bổ sung.
- Chỉ mục: `(available_at,id)`; `(aggregate_type,aggregate_id,created_at)`; 24 tháng.

#### TBL-WRK-064 — `consumer_inbox`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `consumer varchar(100) NOT NULL`; `event_id uuid NOT NULL`; `event_type varchar(120) NOT NULL`; `payload_hash char(64) NOT NULL`; `received_at timestamptz NOT NULL DEFAULT now()`; `processed_at timestamptz NULL`; `result_code varchar(80) NULL`; `trace_id varchar(64) NOT NULL`.
- Ràng buộc: duy nhất `(consumer,event_id)`; cùng sự kiện nhưng khác hàm băm là lỗi bảo mật; bộ nhận gồm Dịch vụ Định danh, minh chứng Dịch vụ Học tập và các tiến trình nội bộ.
- Chỉ mục: `(consumer,processed_at,received_at)`; 24 tháng.

#### TBL-WRK-065 — `admin_adjustments`

- Tập cột: `APPEND`.
- Cột riêng: `tenant_id uuid NULL`; `target_type varchar(32) NOT NULL`; `target_id uuid NOT NULL`; `action varchar(80) NOT NULL`; `before_snapshot jsonb NOT NULL`; `after_snapshot jsonb NOT NULL`; `reason varchar(1000) NOT NULL`; `approved_by_subject_id uuid NOT NULL`; `performed_by_subject_id uuid NOT NULL`; `trace_id varchar(64) NOT NULL`.
- Ràng buộc: hiệu chỉnh thanh toán/tín dụng bắt buộc theo nguyên tắc người tạo–người kiểm tra, hai chủ thể khác nhau và có mã phiếu tham chiếu trong lý do; ảnh chụp dữ liệu đã được che.
- Chỉ mục: `(target_type,target_id,occurred_at DESC)`; `(tenant_id,occurred_at DESC)`; chỉ bổ sung tối thiểu 24 tháng.

#### TBL-WRK-066 — `tenant_roles`

- Tập cột: `ENTITY`.
- Cột riêng: `tenant_type varchar(20) NOT NULL`; `code varchar(40) NOT NULL`; `name varchar(120) NOT NULL`; `description varchar(500) NOT NULL`; `is_system boolean NOT NULL DEFAULT true`; `is_privileged boolean NOT NULL DEFAULT false`; `disabled_at timestamptz NULL`.
- Ràng buộc: duy nhất `(tenant_type,code)`; loại tổ chức là `ENTERPRISE|UNIVERSITY`; mã phải khớp danh mục vai trò của tư cách thành viên tương ứng.
- Chỉ mục: `(tenant_type,disabled_at,code)`.

#### TBL-WRK-067 — `tenant_permissions`

- Tập cột: `ENTITY`.
- Cột riêng: `code varchar(120) NOT NULL UNIQUE`; `tenant_type varchar(20) NOT NULL`; `description varchar(500) NOT NULL`; `risk_level smallint NOT NULL DEFAULT 1`; `disabled_at timestamptz NULL`.
- Ràng buộc: loại tổ chức là `ENTERPRISE|UNIVERSITY|BOTH`; mức rủi ro 1–5.
- Chỉ mục: `(tenant_type,disabled_at,code)`.

#### TBL-WRK-068 — `tenant_role_permissions`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `role_id uuid NOT NULL` FK `tenant_roles.id`; `permission_id uuid NOT NULL` FK `tenant_permissions.id`; `granted_by_subject_id uuid NOT NULL`; `valid_from timestamptz NOT NULL DEFAULT now()`; `valid_until timestamptz NULL`; `revoked_at timestamptz NULL`; `revoked_by_subject_id uuid NULL`; `reason varchar(500) NOT NULL`.
- Ràng buộc: duy nhất một phần trên `(role_id,permission_id)` khi còn hiệu lực; loại tổ chức của vai trò/quyền tương thích; thời hạn hiệu lực hợp lệ; thu hồi yêu cầu chủ thể thực hiện.
- Chỉ mục: `(role_id,revoked_at,valid_until)`; `(permission_id,revoked_at)`.

#### TBL-WRK-069 — `application_evidence_state_events`

- Tập cột: `APPEND`.
- Cột riêng: `tenant_id uuid NOT NULL`; `application_id uuid NOT NULL`; `study_evidence_id uuid NOT NULL`; `from_status evidence_export_status NULL`; `to_status evidence_export_status NOT NULL`; `source varchar(32) NOT NULL`; `actor_subject_id uuid NULL`; `source_event_id uuid NULL`; `reason_code varchar(80) NOT NULL`; `trace_id varchar(64) NOT NULL`.
- Ràng buộc: duy nhất `(source,source_event_id)` khi có sự kiện nguồn; chuyển trạng thái `PENDING→READY|UNAVAILABLE`, `READY→REVOKED` hoặc `HIDDEN` khi rút đồng ý, `UNAVAILABLE→PENDING` hoặc `HIDDEN` khi rút đồng ý, `HIDDEN→REVOKED`; `HIDDEN` chỉ dùng khi rút đồng ý. Việc rút đồng ý/thu hồi không sửa ảnh chụp dữ liệu.
- Chỉ mục: `(application_id,study_evidence_id,occurred_at DESC,id DESC)` để lấy trạng thái hiệu lực; `(study_evidence_id,occurred_at DESC)` cho thu hồi; chỉ bổ sung trong 24 tháng.

#### TBL-WRK-070 — `outbox_delivery_attempts`

- Tập cột và toàn bộ quy tắc như `TBL-IAM-020`, với `outbox_event_id` là khóa ngoại tới `TBL-WRK-063`; duy nhất theo sự kiện/lần thử; chỉ mục theo sự kiện/mới nhất và trạng thái/thử lại; chỉ bổ sung trong 24 tháng.
- Cột riêng đầy đủ: `outbox_event_id uuid NOT NULL`; `attempt_no integer NOT NULL`; `status outbox_status NOT NULL`; `worker_id varchar(120) NOT NULL`; `broker_message_id varchar(180) NULL`; `error_code varchar(80) NULL`; `next_retry_at timestamptz NULL`; `payload_hash char(64) NOT NULL`.

#### TBL-WRK-071 — `internship_program_participants`

- Tập cột: `TENANT_ENTITY` với `tenant_id` FK `university_tenants.id`.
- Cột riêng: `program_id uuid NOT NULL`; `affiliation_id uuid NOT NULL`; `status varchar(24) NOT NULL DEFAULT 'ENROLLED'`; `enrolled_at timestamptz NOT NULL`; `completed_at timestamptz NULL`; `withdrawn_at timestamptz NULL`; `outcome_code varchar(80) NULL`.
- Ràng buộc: khóa ngoại ghép `(tenant_id,program_id)` và `(tenant_id,affiliation_id)`; duy nhất `(tenant_id,program_id,affiliation_id)`; `status` là `ENROLLED|COMPLETED|WITHDRAWN|REMOVED`; dấu thời gian kết thúc tương ứng.
- Chỉ mục: `(tenant_id,program_id,status)`; `(tenant_id,affiliation_id,created_at DESC)`; báo cáo cá nhân vẫn cần sự đồng ý còn hiệu lực.

#### TBL-WRK-072 — `application_offer_versions`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `tenant_id uuid NOT NULL`; `application_id uuid NOT NULL`; `version_no integer NOT NULL`; `title varchar(200) NOT NULL`; `terms_snapshot jsonb NOT NULL`; `salary_vnd bigint NULL`; `starts_on date NULL`; `expires_at timestamptz NOT NULL`; `created_by_subject_id uuid NOT NULL`; `approved_by_subject_id uuid NOT NULL`; `issued_at timestamptz NOT NULL`; `supersedes_version_id uuid NULL` self-FK; `content_hash char(64) NOT NULL`.
- Ràng buộc: duy nhất `(application_id,version_no)`; lương >=0; hết hạn sau khi phát hành; áp dụng nguyên tắc người tạo–người kiểm tra; đơn ứng tuyển/tổ chức nhất quán và đang ở nhánh cho phép đề nghị; sửa sai tạo phiên bản mới.
- Chỉ mục: `(application_id,version_no DESC)`; PII/điều khoản tài chính, thời hạn lưu giữ như đơn ứng tuyển.

#### TBL-WRK-073 — `application_offer_state_events`

- Tập cột: `APPEND`.
- Cột riêng: `tenant_id uuid NOT NULL`; `application_id uuid NOT NULL`; `offer_version_id uuid NOT NULL` FK `application_offer_versions.id`; `from_status varchar(24) NULL`; `to_status varchar(24) NOT NULL`; `actor_subject_id uuid NOT NULL`; `reason_code varchar(80) NOT NULL`; `trace_id varchar(64) NOT NULL`.
- Ràng buộc: `status` là `ISSUED|VIEWED|ACCEPTED|DECLINED|EXPIRED|WITHDRAWN`; chuyển trạng thái hợp lệ; `ACCEPTED|DECLINED` đồng bộ trạng thái đơn ứng tuyển trong cùng giao dịch; lịch sử đề nghị không sửa/xóa.
- Chỉ mục: `(application_id,occurred_at,id)`; `(offer_version_id,occurred_at DESC)`; 24 tháng.

#### TBL-WRK-074 — `job_screening_questions`

- Tập cột: `ENTITY`; chỉ sửa khi bản sửa việc làm còn `DRAFT`, bất biến sau khi gửi duyệt.
- Cột riêng: `tenant_id uuid NOT NULL`; `job_revision_id uuid NOT NULL` FK `job_revisions.id`; `question_type varchar(24) NOT NULL`; `prompt varchar(1000) NOT NULL`; `is_required boolean NOT NULL DEFAULT false`; `options jsonb NULL`; `validation_rule jsonb NULL`; `position integer NOT NULL`.
- Ràng buộc: duy nhất `(job_revision_id,position)`; `question_type` là `TEXT|SINGLE_CHOICE|MULTIPLE_CHOICE|YES_NO|NUMBER`; các lựa chọn bắt buộc đúng loại; cấm hỏi thuộc tính được bảo vệ; tổ chức khớp bản sửa.
- Chỉ mục: `(tenant_id,job_revision_id,position)`.

#### TBL-WRK-075 — `interview_feedback`

- Tập cột: `APPEND`.
- Cột riêng: `tenant_id uuid NOT NULL`; `interview_id uuid NOT NULL`; `reviewer_subject_id uuid NOT NULL`; `recommendation varchar(24) NOT NULL`; `score numeric(5,2) NULL`; `rubric_snapshot jsonb NOT NULL`; `comment text NULL`; `submitted_at timestamptz NOT NULL`; `trace_id varchar(64) NOT NULL`.
- Ràng buộc: duy nhất `(interview_id,reviewer_subject_id)`; `recommendation` là `STRONG_NO|NO|NEUTRAL|YES|STRONG_YES`; điểm 0–100; người duyệt là người tham gia/thành viên tổ chức còn hiệu lực; áp dụng chính sách thuộc tính được bảo vệ.
- Chỉ mục: `(tenant_id,interview_id,submitted_at)`; `DERIVED_SENSITIVE`, thời hạn lưu giữ như đơn ứng tuyển.

#### TBL-WRK-076 — `file_upload_sessions`

- Tập cột: `ENTITY`.
- Cột riêng: `file_id uuid NOT NULL UNIQUE` FK `file_objects.id`; `owner_subject_id uuid NOT NULL`; `tenant_id uuid NULL`; `upload_id varchar(200) NOT NULL UNIQUE`; `expected_size_bytes bigint NOT NULL`; `expected_sha256 char(64) NOT NULL`; `part_count integer NOT NULL DEFAULT 1`; `status varchar(24) NOT NULL DEFAULT 'CREATED'`; `expires_at timestamptz NOT NULL`; `completed_at timestamptz NULL`; `aborted_at timestamptz NULL`.
- Ràng buộc: kích thước >0 theo hạn mức `purpose`; số phần 1–10000; `status` là `CREATED|UPLOADING|COMPLETED|ABORTED|EXPIRED`; khi hoàn tất, kiểm kích thước/hàm băm rồi đưa ClamAV vào hàng đợi.
- Chỉ mục: `(owner_subject_id,status,created_at DESC)`; `(tenant_id,status,created_at DESC)`; `(status,expires_at)`; dọn sau 7 ngày kể từ trạng thái kết thúc.

## 7. Toàn vẹn tổ chức, quyền và bảo mật cấp hàng

1. API không nhận `tenant_id` làm nguồn quyền. Dịch vụ lấy `identity_subject_id` từ JWT, xác định tư cách thành viên còn hiệu lực, rồi gắn ngữ cảnh tổ chức ở phía máy chủ.
2. Tất cả bảng `TENANT_ENTITY` có `UNIQUE(tenant_id,id)`. Bảng con của tổ chức lưu lại `tenant_id` và dùng khóa ngoại ghép `(tenant_id,parent_id)`; do đó không thể gắn đơn ứng tuyển/ghi chú/phỏng vấn/trò chuyện vào tổ chức khác.
3. PostgreSQL RLS bổ sung phòng vệ nhiều lớp cho bảng tổ chức. Giao dịch đặt `SET LOCAL app.subject_id` và `app.tenant_id` từ ngữ cảnh đã xác minh; tiến trình nền dùng vai trò dịch vụ tách biệt và vẫn truyền tổ chức.
4. Dữ liệu thuộc ứng viên dùng điều kiện `candidate.identity_subject_id = app.subject_id`. Tìm kiếm ứng viên của nhà tuyển dụng chỉ đọc bản chiếu có thể tìm kiếm; truy cập đơn ứng tuyển cần được phân công hoặc có quyền của tổ chức.
5. Truy cập khẩn cấp của quản trị viên dùng vai trò tạm thời, MFA, lý do/mã phiếu, thời hạn tối đa 60 phút và ghi kiểm toán bảo mật trước/sau truy cập.
6. Tác vụ nền mang `tenant_id`, `actor_subject_id`, `trace_id`, phiên bản chính sách; tiến trình nền từ chối tải tin thiếu ngữ cảnh.

## 8. Ma trận truy vấn – chỉ mục bắt buộc

| Truy vấn/năng lực | Bảng và điều kiện chính | Chỉ mục được dùng | Giới hạn/khóa |
|---|---|---|---|
| Đăng nhập | thư điện tử chuẩn hóa còn hiệu lực | `user_emails(email_normalized)` duy nhất | giới hạn tần suất theo hàm băm thư điện tử/IP; không lộ sự tồn tại của tài khoản |
| Làm mới mã thông báo | hàm băm mã thông báo; phiên/họ mã còn hiệu lực | mã thông báo duy nhất; `(family_id,status)` | khóa mã thông báo + phiên; phát hiện dùng lại sẽ thu hồi cả họ |
| Danh mục Học tập | đã xuất bản + văn bản/thứ tự | FTS của phiên bản khóa học; `(status,published_at)` | phân trang; lưu đệm danh mục |
| Lộ trình chính | người học + `ACTIVE` | duy nhất một phần cho lộ trình còn hiệu lực | khóa tư vấn của người học cùng `FOR UPDATE` khi chuyển đổi |
| Ghi danh khóa học | người học/phiên bản | ghi danh duy nhất | `INSERT ... ON CONFLICT` xử lý lặp an toàn |
| Trang chủ Học tập | ghi danh/tiến độ còn hiệu lực của người học | ghi danh theo người học/trạng thái; ảnh chụp duy nhất | ảnh chụp cũ được dựng lại từ dữ kiện gốc |
| Duyệt bài đánh giá | cần duyệt theo thứ tự | `(status,submitted_at)` | người duyệt nhận việc với `SKIP LOCKED`; quyết định dùng khóa lạc quan |
| Hộp thư thông báo | chủ thể/đã đọc/thời gian/ID | chỉ mục con trỏ ghép | con trỏ `(created_at,id)`, tối đa 100 mục/trang |
| Tìm kiếm ứng viên | khả năng hiển thị + FTS/kỹ năng/địa điểm | GIN trên vectơ tìm kiếm/mảng | chỉ dùng bản chiếu đã che dữ liệu; thời hạn gỡ quyền tìm kiếm 5 phút |
| Tìm kiếm việc làm công khai | `PUBLISHED` + FTS/địa điểm | FTS/GIN của bản sửa; trạng thái/thời gian việc làm | truy vấn tài trợ riêng, rồi gắn nhãn/hợp nhất |
| Bảng ATS | tổ chức/việc làm/trạng thái/thời gian | đơn ứng tuyển theo tổ chức/việc làm/trạng thái | tối đa 100 mục/trang; tổ chức được suy ra ở phía máy chủ |
| Nộp đơn trùng | ứng viên/việc làm | duy nhất `(candidate_id,job_id)` | một giao dịch cùng khóa lặp an toàn |
| Lịch phỏng vấn | tổ chức/khoảng thời gian/trạng thái | lịch theo tổ chức/bắt đầu/kết thúc | khoảng thời gian tối đa 90 ngày |
| Lịch sử trò chuyện | cuộc trò chuyện + số thứ tự | tin nhắn `(conversation_id,server_sequence)` | con trỏ; REST là nguồn dữ liệu chuẩn |
| Phản hồi gọi lại thanh toán | sự kiện/đơn hàng của nhà cung cấp | phản hồi gọi lại duy nhất; đơn hàng nhà cung cấp | khóa khoản thanh toán/đơn hàng; ưu tiên chuyển trạng thái |
| Chi tiêu tín dụng | quyền sử dụng còn hiệu lực/số dư | quyền sử dụng theo chủ sở hữu/mã/trạng thái | khóa quyền sử dụng; ghi sổ nguyên tử |
| Luồng kiểm toán | tổ chức/tài nguyên/thời gian | chỉ mục ghép + BRIN theo thời gian | con trỏ, yêu cầu quyền đặc quyền |
| Báo cáo trường đại học | tổ chức/báo cáo/trạng thái | lượt tạo báo cáo theo tổ chức/trạng thái/thời gian | nhóm tổng hợp >=10; không có kết quả theo từng dòng |

Mỗi bản chuyển đổi lược đồ thêm truy vấn mới phải kèm `EXPLAIN (ANALYZE, BUFFERS)` trên tập dữ liệu thí điểm giả lập. Không tạo chỉ mục chỉ để “dự phòng”; chỉ mục không được dùng qua hai kỳ phát hành phải được đánh giá loại bỏ bằng bản chuyển đổi riêng.

## 9. Giao dịch, khóa và xử lý cạnh tranh

| Tình huống | Ranh giới giao dịch và khóa | Kết quả bắt buộc |
|---|---|---|
| Làm mới/dùng lại đồng thời | khóa mã thông báo làm mới, phiên và họ mã thông báo theo thứ tự ID | đúng một lần xoay vòng thành công; lần dùng lại đánh dấu `COMPROMISED`, thu hồi họ mã/phiên và phát kiểm toán/hộp thư đi |
| Hai lần đổi lộ trình chính | khóa tư vấn theo người học + `FOR UPDATE` kỳ còn hiệu lực | đúng một `ACTIVE`; đóng/tạm dừng kỳ cũ và tạo kỳ mới/hộp thư đi trong cùng lần cam kết |
| Ghi danh trùng | bản ghi duy nhất theo người học/phiên bản khóa học + khóa lặp an toàn | cùng yêu cầu trả cùng phản hồi, không nhân đôi tiến độ |
| Hai lần nộp bài | khóa lượt làm/ghi danh, so sánh `row_version`, đóng băng ảnh chụp đáp án/tệp | chỉ một lần nộp; yêu cầu trùng trả lại kết quả trước, tải tin khác trả xung đột |
| Hai người duyệt | so sánh lạc quan phiên bản lượt làm/việc làm/đơn ứng tuyển | một quyết định được áp dụng; người còn lại nhận 409 và tải dữ liệu mới |
| Xuất bản nội dung/việc làm | khóa con trỏ tổng hợp; kiểm hàm băm/quyền/quét của bản sửa; cập nhật con trỏ + lịch sử + hộp thư đi | bản sửa `PUBLISHED` là bất biến; `If-Match` cũ không được xuất bản |
| Nộp đơn đồng thời | chèn đơn ứng tuyển duy nhất, ảnh chụp dữ liệu, lựa chọn/yêu cầu minh chứng, điều kiện tạo trò chuyện và hộp thư đi trong một giao dịch | đúng một đơn ứng tuyển; Dịch vụ Học tập ngừng hoạt động chỉ khiến minh chứng ở `PENDING` |
| Đơn ứng tuyển kết thúc | khóa đơn ứng tuyển và cuộc trò chuyện | lịch sử trạng thái + cuộc trò chuyện `READ_ONLY` cùng lần cam kết hoặc bộ nhận lặp an toàn bảo đảm hội tụ |
| Phản hồi gọi lại trùng/không theo thứ tự | chèn khóa khử trùng lặp phản hồi gọi lại trước, khóa khoản thanh toán/đơn hàng, so thứ tự ưu tiên trạng thái/thời gian nhà cung cấp | không xác lập thanh toán hai lần; URL trả về không tạo quyền sử dụng |
| Chi tiêu quyền sử dụng/tín dụng | khóa quyền sử dụng, kiểm trạng thái hiệu lực/hết hạn/số dư, ghi sổ rồi tăng số đã dùng | số dư không âm; thử lại cùng khóa lặp an toàn không chi tiêu lần hai |

Thứ tự khóa chuẩn: gốc tổng hợp trước, bản ghi con theo UUID tăng dần, sau cùng là hộp thư đi. Giao dịch không gọi mạng. Lời gọi bên ngoài luôn diễn ra sau khi cam kết qua tiến trình nền/hộp thư đi; kết quả được ghi bằng giao dịch lặp an toàn mới.

## 10. Quản lý phiên bản, chỉ bổ sung, hộp thư đi và bộ nhớ đệm

- Bản sửa lộ trình/khóa học/việc làm/CV: bản `DRAFT` có thể sửa bằng xử lý đồng thời lạc quan ở lưu trữ tổng hợp/trình soạn thảo; khi gửi duyệt, hệ thống đóng băng thành bản sửa bất biến. Nếu cần chỉnh, sao chép sang phiên bản mới. Lần ghi danh/đơn ứng tuyển luôn trỏ tới phiên bản cụ thể.
- Ảnh chụp đơn ứng tuyển, minh chứng, phản hồi gọi lại thanh toán, lịch sử trạng thái, quyết định duyệt, đầu ra/duyệt AI, kiểm toán, sổ cái, hộp thư đến/đi chỉ được bổ sung. “Xóa” chỉ ẩn nội dung theo chính sách và giữ bản đánh dấu đã xóa/hàm băm/kiểm toán.
- Mọi thay đổi phát sự kiện, lưu tổng hợp và hộp thư đi trong cùng giao dịch. Bộ phát chọn sự kiện chưa có lần thử `PUBLISHED`, giữ khóa tư vấn theo sự kiện, ghi lần thử giao nhận chỉ-bổ-sung; việc thử lại có thời gian chờ tăng dần kèm ngẫu nhiên và lần thử cuối là `DEAD_LETTER`. Phát lại giữ nguyên `event_id`/`dedupe_key`.
- Bộ nhận ghi hộp thư đến trước hoặc cùng giao dịch với bản chiếu. Bản trùng có cùng hàm băm trả thành công; khác hàm băm thì dừng và báo sự cố bảo mật.
- Redis chỉ dùng cho lưu đệm/giới hạn tần suất phiên/hàng đợi/phân phối. Không phải nguồn dữ liệu chuẩn. Khóa lưu đệm mang dịch vụ, ID tài nguyên, phiên bản và tổ chức; thay đổi làm mất hiệu lực theo hộp thư đi. Redis ngừng hoạt động sẽ giảm cấp về cơ sở dữ liệu/giới hạn tần suất và từ chối kín các thao tác nhạy cảm về xác thực.
- Phần trăm tiến độ, tài liệu tìm kiếm ứng viên và ảnh chụp báo cáo là bản chiếu có mốc dữ liệu cao nhất/phiên bản tính toán, có thể dựng lại từ dữ kiện/lịch sử.

## 11. Lưu giữ, xóa tài khoản, ẩn danh hóa và tạm giữ pháp lý

| Nhóm | Thời hạn lưu giữ mặc định | Hành động khi hết hạn |
|---|---|---|
| Thông báo + giao nhận | 180 ngày | dọn nội dung/tải tin và bản ghi nếu không có tạm giữ kiểm toán |
| Hoạt động học tập/hỗ trợ | 13 tháng sau hoạt động/trạng thái kết thúc | tổng hợp số liệu rồi xóa PII; kết quả hoàn thành/minh chứng còn hiệu lực được giữ |
| Đơn ứng tuyển/trò chuyện/ảnh chụp minh chứng/ghi chú | 12 tháng sau khi đơn ứng tuyển kết thúc | xóa nội dung PII/đối tượng; giữ bản đánh dấu đã xóa/hàm băm và kiểm toán theo tạm giữ pháp lý |
| Kiểm toán/bảo mật/thanh toán/phản hồi gọi lại/sổ cái/duyệt | tối thiểu 24 tháng hoặc lâu hơn theo chính sách tài chính/pháp lý | phân vùng lưu trữ mã hóa; chỉ dọn theo lịch đã phê duyệt |
| Tài liệu xác minh | 180 ngày sau quyết định/hết hạn | xóa đối tượng và khóa mã hóa; giữ siêu dữ liệu quyết định/hàm băm |
| Khóa lặp an toàn | 24 giờ; thay đổi quan trọng 7 ngày | dọn phản hồi/tải tin, giữ tổng hợp nghiệp vụ |
| Bản sao lưu | tối đa 35 ngày | xóa theo vòng đời; kiểm thử khôi phục định kỳ |
| Yêu cầu xóa | thời gian ân hạn 30 ngày | cho phép hủy trong thời gian ân hạn; sau đó điều phối ẩn danh hóa từng dịch vụ |

Quy trình xóa tài khoản:

1. Dịch vụ Định danh đặt `DELETION_PENDING`, thu hồi phiên/mã thông báo, phát sự kiện có hạn chót; không xóa ngay.
2. Dịch vụ Học tập/Việc làm đánh dấu chủ thể đang chờ xóa, khóa các thay đổi không thiết yếu và thu hồi khả năng tìm kiếm/sự đồng ý ngay lập tức.
3. Sau 30 ngày, mỗi dịch vụ thay PII bằng bí danh ngẫu nhiên, xóa hoặc hủy khóa mã hóa tệp, giữ dữ liệu tài chính/bảo mật/kiểm toán tối thiểu. Dịch vụ Định danh phát `ANONYMIZED` khi nhận xác nhận hoàn tất.
4. Đơn ứng tuyển/thanh toán có tạm giữ pháp lý chỉ giả danh hóa trường không cần cho mục đích pháp lý; bản ghi tạm giữ ghi `legal_hold_until`, lý do và người phê duyệt trong kiểm toán, không âm thầm bỏ qua việc dọn dữ liệu.
5. Bản sao lưu không bị sửa trực tiếp; dữ liệu đã xóa có thể còn tối đa 35 ngày nhưng hướng dẫn khôi phục phải chạy phát lại quy trình xóa trước khi mở lưu lượng.

Ứng viên rút quyền tìm kiếm không chờ xóa tài khoản: giao dịch đặt `PRIVATE` và ghi hộp thư đi; tiến trình nền xóa bản chiếu tìm kiếm trong tối đa 5 phút, đồng thời dừng hồ sơ tài trợ. Rút sự đồng ý ẩn dữ liệu trường đại học/minh chứng ngay; thu hồi tạo sự kiện trạng thái `REVOKED`, không sửa ảnh chụp minh chứng và vẫn giữ kiểm toán.

## 12. Mã hóa, bí mật và dữ liệu nhạy cảm

- TLS cho mọi kết nối; vùng lưu trữ/bản sao lưu PostgreSQL và kho đối tượng được mã hóa. Cột dữ liệu mã hóa dùng mã hóa phong bì với phiên bản khóa KMS/Vault trong siêu dữ liệu mã hóa, không lưu khóa trong cơ sở dữ liệu.
- Mật khẩu chỉ lưu hàm băm Argon2id; mã làm mới/xác minh/đặt lại/mời/khôi phục chỉ lưu hàm băm. Khóa riêng JWT chỉ lưu tham chiếu; JWK công khai được xuất bản.
- Không lưu số thẻ, tài khoản ví, CVV, thông tin xác thực thanh toán, bí mật nhà cung cấp hoặc khóa ký phản hồi gọi lại gốc. Tải tin phản hồi gọi lại gốc được mã hóa để đối soát; nhật ký chỉ có hàm băm/ID đã được che dữ liệu.
- URL có chữ ký có đối tượng nhận, chủ thể/tài nguyên, thời hạn <=5 phút và chỉ một mục đích; API kiểm quyền sở hữu/tổ chức trước khi ký. Tệp MIME được kiểm tra chữ ký định dạng, quét mã độc và cách ly; tên tệp luôn được thoát ký tự khi tải xuống.
- Đầu vào AI theo danh sách trường cho phép; loại thư điện tử/điện thoại/tên khi năng lực không cần, thuộc tính được bảo vệ, minh chứng Học tập và trạng thái tài trợ khỏi đối sánh. Nội dung CV/JD được coi là dữ liệu chỉ dẫn không tin cậy.

## 13. Chuyển đổi lược đồ, sao lưu và khôi phục

### 13.1 Chính sách chuyển đổi lược đồ

- Mỗi dịch vụ sở hữu chuỗi chuyển đổi lược đồ riêng: Dịch vụ Định danh/Học tập dùng Alembic, Dịch vụ Việc làm dùng chuyển đổi Prisma có rà soát SQL. CI chạy từ cơ sở dữ liệu trống và từ bản phát hành gần nhất.
- Dùng quy trình mở rộng/thu hẹp: thêm cột cho phép không có giá trị/an toàn với giá trị mặc định → triển khai đọc/ghi kép và bù dữ liệu theo lô → kiểm chênh lệch bằng không → chuyển luồng đọc → thêm `NOT NULL`/ràng buộc → bỏ cột cũ ở đợt phát hành sau.
- Không đổi tên/xóa/đổi kiểu liệt kê gây phá vỡ trong cùng đợt phát hành. Chỉ mục lớn dùng `CREATE INDEX CONCURRENTLY`; ràng buộc lớn thêm `NOT VALID`, bù dữ liệu rồi `VALIDATE`.
- Bù dữ liệu có điểm kiểm, giới hạn tần suất, phạm vi tổ chức, xử lý lặp an toàn và kiểm toán; không giữ khóa giao dịch lâu. Bản chuyển đổi tuyệt đối không gọi dịch vụ ngoài hoặc khởi tạo dữ liệu phát hành.
- Phiên bản lược đồ của sự kiện/API tương thích tối thiểu một phiên bản trước. Bộ nhận gặp trường lạ phải bỏ qua; thiếu phiên bản bắt buộc phải vào DLQ, không suy đoán.
- Mọi bản chuyển đổi có người sở hữu, kế hoạch quay lui/tiến tiếp, ước lượng khóa/dung lượng đĩa, kế hoạch truy vấn và kiểm tra thời hạn lưu giữ/RLS/khóa ngoại ghép.

### 13.2 Sao lưu/khôi phục thảm họa

- PostgreSQL dùng PITR bằng WAL, sao lưu đầy đủ hằng ngày; lưu tối đa 35 ngày; quản lý phiên bản/vòng đời kho đối tượng theo cùng chính sách. Mỗi cơ sở dữ liệu được sao lưu độc lập nhưng bản kê khôi phục ghi mốc sự kiện cao nhất để phát lại bản chiếu.
- RPO 15 phút, RTO 4 giờ. Diễn tập khôi phục tối thiểu mỗi quý, kiểm tổng kiểm, phiên bản chuyển đổi lược đồ, phát lại hộp thư đến/đi, tính liên tục khóa ký/JWKS và phát lại quy trình xóa.
- Không dùng giao dịch phân tán xuyên ba cơ sở dữ liệu. Sau khi khôi phục, dùng hộp thư đi/đến/đối soát để hội tụ; đối soát thanh toán và xuất minh chứng được chạy trước khi mở các thay đổi liên quan.

## 14. Danh sách kiểm tra nghiệm thu mô hình dữ liệu

- Ba cơ sở dữ liệu không có khóa ngoại/truy vấn xuyên cơ sở dữ liệu; mọi ID ngoài hệ thống và sự kiện đều có phiên bản/khử trùng lặp/dấu vết.
- Đúng một lộ trình chính `ACTIVE`; một lần ghi danh trên mỗi người học/phiên bản khóa học; một đơn ứng tuyển trên mỗi ứng viên/việc làm; một cuộc trò chuyện trên mỗi đơn ứng tuyển.
- Bản sửa `PUBLISHED` và mọi ảnh chụp dữ liệu/lịch sử/kiểm toán/thanh toán/duyệt AI/hộp thư đi là bất biến hoặc chỉ bổ sung theo định nghĩa.
- Mọi bảng con của tổ chức có ngữ cảnh tổ chức + khóa ngoại ghép; kiểm thử IDOR xuyên tổ chức thất bại kể cả khi đoán đúng UUID.
- Tệp chưa `CLEAN` không được đính kèm/xuất bản/tải xuống; giả mạo MIME/mã độc bị cách ly.
- Ứng viên `PRIVATE` không nằm trong tìm kiếm/tài trợ trong tối đa 5 phút; tìm kiếm không chứa thông tin liên hệ/CV/minh chứng Học tập.
- Thanh toán chỉ `SETTLED` bởi phản hồi gọi lại/IPN hoặc đối soát đã xác minh; phản hồi gọi lại trùng/không theo thứ tự không tạo quyền sử dụng/tín dụng hai lần.
- AI không ghi trạng thái ATS; điểm không dùng trường được bảo vệ/minh chứng/tài trợ; mọi đầu ra được áp dụng đều có người duyệt.
- Thời hạn lưu giữ, xóa tài khoản, rút sự đồng ý, tạm giữ pháp lý và phát lại xóa từ bản sao lưu có kiểm thử tự động/diễn tập khôi phục.
- Ma trận truy vấn–chỉ mục có kế hoạch kiểm thử trên dữ liệu thí điểm 5.000 tài khoản, 500 DAU, 50 RPS và không vượt SLO đã chốt.
