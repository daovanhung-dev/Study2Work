# Thiết kế cơ sở dữ liệu Study2Work V1-PILOT

## 1. Phạm vi và quyền sở hữu

Tài liệu này là nguồn định nghĩa duy nhất cho mô hình dữ liệu logic và vật lý của V1-PILOT. Tài liệu mô tả cấu trúc cần được chuyển thành migration; không chứa DDL thực thi, seed, dữ liệu mẫu hoặc bí mật môi trường.

Hệ thống có đúng ba cụm PostgreSQL vật lý, mỗi cụm có user kết nối, backup, migration history và khóa mã hóa riêng:

| Database | Service sở hữu | Dữ liệu sở hữu | Tuyệt đối không làm |
|---|---|---|---|
| `identity_db` | Platform Identity | danh tính, credential, MFA, session, token, vai trò nền tảng, security audit | Không lưu hồ sơ học tập, CV, application hoặc payment |
| `study_db` | Study | hồ sơ học, nội dung phiên bản, enrollment/progress, assessment, evidence học tập | Không xác thực password và không truy vấn `identity_db` |
| `work_db` | Work | hồ sơ nghề nghiệp, tenant, job/ATS, interview/chat, university, AI, billing | Không xác thực password, không truy vấn Study evidence trực tiếp |

Không có foreign key hoặc join xuyên database. `identity_subject_id` trong Study/Work là UUID ngoài hệ thống được đồng bộ bằng sự kiện đã ký; `study_evidence_id` trong Work chỉ là tham chiếu yêu cầu export. Trao đổi liên dịch vụ sử dụng outbox, signed payload, idempotent consumer và bảng inbox.

## 2. Quy ước vật lý bắt buộc

### 2.1 Kiểu dữ liệu và thời gian

- ID nghiệp vụ dùng UUID v7 do ứng dụng sinh; không phụ thuộc extension database. ID từ hệ thống ngoài dùng `varchar` có giới hạn rõ.
- Thời gian dùng `timestamptz`, lưu UTC; ngày thuần túy dùng `date`; duration dùng số giây `integer`.
- Tiền dùng `bigint` theo đơn vị VND, không dùng floating point. Tỷ lệ/điểm dùng `numeric(p,s)` với check miền giá trị.
- JSON chỉ dùng `jsonb` cho snapshot/payload có schema version; trường cần lọc, join hoặc unique phải tách thành cột.
- Email canonical là chữ thường, trim Unicode; so sánh bằng khóa `email_normalized varchar(320)`, không phụ thuộc collation.
- Chuỗi trạng thái dùng PostgreSQL enum do migration quản lý. Thêm giá trị là migration forward-only; đổi tên dùng quy trình expand/contract.
- Mọi `*_at` có giá trị mặc định chỉ khi ghi trong định nghĩa. Không tự đặt default cho thời điểm nghiệp vụ.

### 2.2 Tập cột chuẩn

Các tập dưới đây là một phần đầy đủ của định nghĩa bảng. Khi bảng ghi `ENTITY`, `IMMUTABLE`, `APPEND` hoặc `TENANT_ENTITY`, toàn bộ cột tương ứng bắt buộc tồn tại ngoài các cột riêng được liệt kê.

| Tập | Toàn bộ cột | Quy tắc |
|---|---|---|
| `ENTITY` | `id uuid NOT NULL` PK; `created_at timestamptz NOT NULL DEFAULT now()`; `updated_at timestamptz NOT NULL DEFAULT now()`; `row_version bigint NOT NULL DEFAULT 1` | update phải tăng `row_version`; API `If-Match` so với giá trị này |
| `TENANT_ENTITY` | toàn bộ `ENTITY`; `tenant_id uuid NOT NULL` | có `UNIQUE(tenant_id,id)`; mọi child dùng composite FK chứa `tenant_id` |
| `IMMUTABLE` | `id uuid NOT NULL` PK; `created_at timestamptz NOT NULL DEFAULT now()` | payload đã đóng băng cấm sửa/xóa; chỉ metadata chuyển trạng thái một chiều được bảng nêu rõ mới có thể cập nhật; correction tạo record/version mới |
| `APPEND` | `id uuid NOT NULL` PK; `occurred_at timestamptz NOT NULL DEFAULT now()` | chỉ INSERT; partition theo tháng khi bảng vượt 10 triệu dòng |

`deleted_at` không được ngầm hiểu. Chỉ bảng có ghi rõ cột này mới soft-delete. Không dùng `ON DELETE CASCADE` với audit, history, payment, AI review, application snapshot, evidence snapshot, outbox/inbox hoặc dữ liệu legal hold. FK mặc định là `ON DELETE RESTRICT`; `SET NULL` chỉ khi được ghi rõ.

### 2.3 Phân loại dữ liệu

| Nhãn | Nội dung | Kiểm soát |
|---|---|---|
| `PUBLIC` | catalog, job đã publish | cache/public read được phép |
| `INTERNAL` | config, trạng thái vận hành | role theo least privilege |
| `PII` | tên, email, điện thoại, CV, chat, địa chỉ | mã hóa storage/backup, redaction log, không ghi raw vào telemetry |
| `SENSITIVE` | credential, MFA secret, token, verification document, payment signature | application-layer envelope encryption hoặc one-way hash; truy cập được audit |
| `DERIVED_SENSITIVE` | AI/match score, recruiter note, moderation | không xuất cho bên ngoài nếu không có policy/consent |

## 3. Danh mục enum canonical

Tên và giá trị dưới đây là canonical; API dùng đúng giá trị chữ hoa này.

| Context | Enum | Giá trị |
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

Không biến động từ hành động hoặc thuộc tính hiển thị thành lifecycle state; mọi trạng thái hợp lệ phải nằm trong catalog trên.

## 4. Database Platform Identity (`identity_db`)

### 4.1 Danh tính, credential và verification

#### TBL-IAM-001 — `users`

- Tập cột: `ENTITY`.
- Cột riêng: `status account_status NOT NULL DEFAULT 'PENDING_EMAIL_VERIFICATION'`; `display_name varchar(120) NULL`; `locale varchar(10) NOT NULL DEFAULT 'vi-VN'`; `timezone varchar(64) NOT NULL DEFAULT 'Asia/Ho_Chi_Minh'`; `email_verified_at timestamptz NULL`; `suspended_at timestamptz NULL`; `suspension_reason varchar(500) NULL`; `deletion_requested_at timestamptz NULL`; `anonymized_at timestamptz NULL`; `privileged_mfa_required boolean NOT NULL DEFAULT false`.
- Ràng buộc: trạng thái `SUSPENDED` yêu cầu `suspended_at` và reason; `ANONYMIZED` yêu cầu `anonymized_at`; display name sau trim dài 1–120 nếu khác null.
- Chỉ mục: `(status, created_at DESC)`; partial `(deletion_requested_at)` khi khác null.
- Dữ liệu: PII; giữ record định danh giả danh hóa vô thời hạn để bảo toàn FK/audit.

#### TBL-IAM-002 — `user_emails`

- Tập cột: `ENTITY`.
- Cột riêng: `user_id uuid NOT NULL` FK `users.id`; `email_ciphertext bytea NOT NULL`; `email_normalized varchar(320) NOT NULL`; `is_primary boolean NOT NULL DEFAULT true`; `verified_at timestamptz NULL`; `replaced_at timestamptz NULL`.
- Ràng buộc: unique toàn cục `email_normalized` khi `replaced_at IS NULL`; partial unique `(user_id)` khi `is_primary=true AND replaced_at IS NULL`; email canonical phải khớp giá trị sau decrypt tại write boundary.
- Chỉ mục: `(user_id, replaced_at)`.
- Dữ liệu: PII; khi anonymize thay ciphertext và normalized bằng alias không đảo ngược.

#### TBL-IAM-003 — `password_credentials`

- Tập cột: `ENTITY`.
- Cột riêng: `user_id uuid NOT NULL UNIQUE` FK `users.id`; `password_hash varchar(512) NOT NULL`; `algorithm varchar(32) NOT NULL DEFAULT 'ARGON2ID'`; `parameters jsonb NOT NULL`; `changed_at timestamptz NOT NULL`; `must_change boolean NOT NULL DEFAULT false`; `failed_count integer NOT NULL DEFAULT 0`; `locked_until timestamptz NULL`.
- Ràng buộc: `failed_count >= 0`; `algorithm='ARGON2ID'`; JSON chỉ chứa memory/time/parallelism/version, không chứa password.
- Chỉ mục: unique `user_id`; không index hash.
- Dữ liệu: SENSITIVE; không soft-delete, thay password ghi security audit.

#### TBL-IAM-004 — `email_verification_tokens`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `user_id uuid NOT NULL` FK `users.id`; `email_id uuid NOT NULL` FK `user_emails.id`; `purpose varchar(24) NOT NULL`; `token_hash char(64) NOT NULL UNIQUE`; `status token_status NOT NULL DEFAULT 'ACTIVE'`; `expires_at timestamptz NOT NULL`; `consumed_at timestamptz NULL`; `revoked_at timestamptz NULL`; `request_ip_hash char(64) NULL`.
- Ràng buộc: `expires_at>created_at`; consumed/revoked timestamp phải phù hợp status. Thay đổi status được thực hiện bởi security-definer procedure được cấp riêng; về logic record là append-only ngoài transition một chiều.
- Purpose chỉ `REGISTER|CHANGE_EMAIL`; change email chỉ promote `user_emails.is_primary` sau verify và revoke primary cũ trong cùng transaction.
- Chỉ mục: `(user_id,status,expires_at DESC)`.
- Dữ liệu: SENSITIVE; purge token payload sau 180 ngày, giữ audit.

#### TBL-IAM-005 — `password_reset_tokens`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `user_id uuid NOT NULL` FK `users.id`; `token_hash char(64) NOT NULL UNIQUE`; `status token_status NOT NULL DEFAULT 'ACTIVE'`; `expires_at timestamptz NOT NULL`; `consumed_at timestamptz NULL`; `revoked_at timestamptz NULL`; `session_epoch bigint NOT NULL`; `request_ip_hash char(64) NULL`.
- Ràng buộc/chỉ mục/retention: như `email_verification_tokens`; reset thành công revoke mọi refresh token có epoch cũ trong cùng transaction.

### 4.2 MFA, session và token

#### TBL-IAM-006 — `mfa_methods`

- Tập cột: `ENTITY`.
- Cột riêng: `user_id uuid NOT NULL` FK `users.id`; `type mfa_method_type NOT NULL`; `label varchar(80) NULL`; `secret_ciphertext bytea NULL`; `verified_at timestamptz NULL`; `disabled_at timestamptz NULL`.
- Ràng buộc: TOTP yêu cầu encrypted secret; recovery code chỉ là phương thức challenge dự phòng và hash thực tế nằm ở `TBL-IAM-007`, không lưu raw code tại đây; partial unique `(user_id,type)` khi chưa disabled.
- Chỉ mục: `(user_id,disabled_at)`.
- Dữ liệu: SENSITIVE; hard-delete chỉ sau account anonymization và hết legal hold.

#### TBL-IAM-007 — `mfa_recovery_codes`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `method_id uuid NOT NULL` FK `mfa_methods.id`; `code_hash char(64) NOT NULL UNIQUE`; `consumed_at timestamptz NULL`; `batch_id uuid NOT NULL`.
- Ràng buộc: chỉ code chưa consumed được dùng một lần; update duy nhất được phép là đặt `consumed_at` một chiều.
- Chỉ mục: `(method_id,consumed_at)`; SENSITIVE.

#### TBL-IAM-008 — `mfa_challenges`

- Tập cột: `ENTITY`.
- Cột riêng: `user_id uuid NOT NULL` FK `users.id`; `session_id uuid NULL`; `purpose varchar(32) NOT NULL`; `challenge_hash char(64) NOT NULL UNIQUE`; `expires_at timestamptz NOT NULL`; `attempt_count integer NOT NULL DEFAULT 0`; `max_attempts integer NOT NULL DEFAULT 5`; `verified_at timestamptz NULL`; `invalidated_at timestamptz NULL`.
- Ràng buộc: `expires_at>created_at`, `0<=attempt_count<=max_attempts`; one-way completion.
- Chỉ mục: `(user_id,purpose,expires_at DESC)`; purge sau 180 ngày.

#### TBL-IAM-009 — `auth_sessions`

- Tập cột: `ENTITY`.
- Cột riêng: `user_id uuid NOT NULL` FK `users.id`; `status session_status NOT NULL DEFAULT 'ACTIVE'`; `session_epoch bigint NOT NULL`; `device_id_hash char(64) NULL`; `device_name varchar(120) NULL`; `ip_hash char(64) NULL`; `user_agent_hash char(64) NULL`; `last_seen_at timestamptz NOT NULL`; `expires_at timestamptz NOT NULL`; `revoked_at timestamptz NULL`; `revoke_reason varchar(100) NULL`.
- Ràng buộc: `expires_at>created_at`; revoked/compromised yêu cầu `revoked_at`; không lưu raw IP/user-agent.
- Chỉ mục: `(user_id,status,last_seen_at DESC)`; `(expires_at)` partial khi ACTIVE.
- Retention: 24 tháng cho security investigation, sau đó xóa/hash sâu hơn theo legal hold.

#### TBL-IAM-010 — `refresh_tokens`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `session_id uuid NOT NULL` FK `auth_sessions.id`; `family_id uuid NOT NULL`; `parent_token_id uuid NULL` self-FK; `token_hash char(64) NOT NULL UNIQUE`; `status token_status NOT NULL DEFAULT 'ACTIVE'`; `issued_at timestamptz NOT NULL`; `expires_at timestamptz NOT NULL`; `rotated_to_id uuid NULL` self-FK; `consumed_at timestamptz NULL`; `reuse_detected_at timestamptz NULL`.
- Ràng buộc: một token chỉ có một child; unique partial `parent_token_id` khi khác null; `expires_at>issued_at`; transition một chiều bằng procedure. Phát hiện reuse khóa family và session trong transaction.
- Chỉ mục: `(family_id,status)`; `(session_id,issued_at DESC)`; `(expires_at)`.
- Dữ liệu: chỉ hash token; giữ 24 tháng sau expiry.

#### TBL-IAM-011 — `signing_keys`

- Tập cột: `ENTITY`.
- Cột riêng: `kid varchar(80) NOT NULL UNIQUE`; `algorithm varchar(16) NOT NULL DEFAULT 'ES256'`; `public_jwk jsonb NOT NULL`; `private_key_ref varchar(300) NOT NULL`; `not_before timestamptz NOT NULL`; `not_after timestamptz NOT NULL`; `activated_at timestamptz NULL`; `retired_at timestamptz NULL`.
- Ràng buộc: chỉ `ES256`; `not_after>not_before`; private material chỉ là KMS/Vault reference.
- Chỉ mục: `(activated_at,retired_at)`; public JWK INTERNAL, key reference SENSITIVE.

### 4.3 RBAC nền tảng

#### TBL-IAM-012 — `roles`

- Tập cột: `ENTITY`.
- Cột riêng: `code varchar(80) NOT NULL UNIQUE`; `name varchar(120) NOT NULL`; `description varchar(500) NOT NULL`; `is_privileged boolean NOT NULL DEFAULT false`; `is_system boolean NOT NULL DEFAULT true`; `disabled_at timestamptz NULL`.
- Ràng buộc: code chữ hoa dạng `^[A-Z][A-Z0-9_]{1,79}$`; system role không đổi code hoặc hard-delete.
- Chỉ mục: `(disabled_at,code)`.

#### TBL-IAM-013 — `permissions`

- Tập cột: `ENTITY`.
- Cột riêng: `code varchar(120) NOT NULL UNIQUE`; `service varchar(20) NOT NULL`; `description varchar(500) NOT NULL`; `risk_level smallint NOT NULL DEFAULT 1`.
- Ràng buộc: `service IN ('IDENTITY','STUDY','WORK')`; `risk_level BETWEEN 1 AND 5`.
- Chỉ mục: `(service,code)`.

#### TBL-IAM-014 — `role_permissions`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `role_id uuid NOT NULL` FK `roles.id`; `permission_id uuid NOT NULL` FK `permissions.id`; `granted_by uuid NOT NULL` FK `users.id`; `revoked_at timestamptz NULL`; `revoked_by uuid NULL` FK `users.id`.
- Ràng buộc: partial unique `(role_id,permission_id)` khi `revoked_at IS NULL`; revoked_by bắt buộc khi revoked.
- Chỉ mục: `(permission_id,revoked_at)`.

#### TBL-IAM-015 — `user_role_assignments`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `user_id uuid NOT NULL` FK `users.id`; `role_id uuid NOT NULL` FK `roles.id`; `scope_type varchar(24) NOT NULL DEFAULT 'PLATFORM'`; `scope_id uuid NULL`; `valid_from timestamptz NOT NULL DEFAULT now()`; `valid_until timestamptz NULL`; `granted_by uuid NOT NULL` FK `users.id`; `revoked_at timestamptz NULL`; `revoked_by uuid NULL` FK `users.id`; `reason varchar(500) NOT NULL`.
- Ràng buộc: `valid_until>valid_from` nếu có; scope PLATFORM yêu cầu scope_id null; partial unique `(user_id,role_id,scope_type,scope_id)` khi active; privileged assignment yêu cầu MFA ở service layer.
- Chỉ mục: `(user_id,revoked_at,valid_until)`; `(scope_type,scope_id,revoked_at)`.

### 4.4 Độ tin cậy và audit Identity

#### TBL-IAM-016 — `idempotency_keys`

- Tập cột: `ENTITY`.
- Cột riêng: `actor_id uuid NULL`; `operation varchar(120) NOT NULL`; `key_hash char(64) NOT NULL`; `request_hash char(64) NOT NULL`; `response_status integer NULL`; `response_body jsonb NULL`; `locked_until timestamptz NULL`; `completed_at timestamptz NULL`; `expires_at timestamptz NOT NULL`.
- Ràng buộc: unique `(actor_id,operation,key_hash)`; cùng key khác request hash trả conflict; response phải được redaction.
- Chỉ mục: `(expires_at)`; purge sau 24 giờ trừ register giữ 7 ngày.

#### TBL-IAM-017 — `security_audit_events`

- Tập cột: `APPEND`.
- Cột riêng: `actor_id uuid NULL`; `subject_id uuid NULL`; `action varchar(120) NOT NULL`; `outcome audit_outcome NOT NULL`; `reason_code varchar(80) NULL`; `trace_id varchar(64) NOT NULL`; `session_id uuid NULL`; `ip_hash char(64) NULL`; `user_agent_hash char(64) NULL`; `metadata jsonb NOT NULL DEFAULT '{}'`; `prev_hash char(64) NULL`; `event_hash char(64) NOT NULL UNIQUE`; `legal_hold_until timestamptz NULL`.
- Ràng buộc: event hash tính từ canonical payload và prev_hash; denied/failure yêu cầu reason code; metadata qua schema/redaction.
- Chỉ mục: `(subject_id,occurred_at DESC)`; `(actor_id,occurred_at DESC)`; `(trace_id)`; BRIN `(occurred_at)`.
- Retention: tối thiểu 24 tháng; chain hash phát hiện sửa đổi; không cascade delete.

#### TBL-IAM-018 — `outbox_events`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `aggregate_type varchar(80) NOT NULL`; `aggregate_id uuid NOT NULL`; `event_type varchar(120) NOT NULL`; `event_version integer NOT NULL`; `payload jsonb NOT NULL`; `available_at timestamptz NOT NULL DEFAULT now()`; `dedupe_key varchar(180) NOT NULL UNIQUE`; `trace_id varchar(64) NOT NULL`.
- Ràng buộc: `event_version>=1`; payload không chứa credential/token raw; toàn bộ row append-only và không chứa trạng thái delivery mutable.
- Chỉ mục: `(available_at,id)`; `(aggregate_type,aggregate_id,created_at)`.
- Retention: 24 tháng; trạng thái publish được suy ra từ attempt ở bảng kế tiếp.

#### TBL-IAM-019 — `consumer_inbox`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `consumer varchar(100) NOT NULL`; `event_id uuid NOT NULL`; `event_type varchar(120) NOT NULL`; `payload_hash char(64) NOT NULL`; `received_at timestamptz NOT NULL DEFAULT now()`; `processed_at timestamptz NULL`; `result_code varchar(80) NULL`; `trace_id varchar(64) NOT NULL`.
- Ràng buộc: unique `(consumer,event_id)`; cùng event khác payload hash là security error.
- Chỉ mục: `(consumer,processed_at,received_at)`; giữ 24 tháng.

#### TBL-IAM-020 — `outbox_delivery_attempts`

- Tập cột: `APPEND`.
- Cột riêng: `outbox_event_id uuid NOT NULL` FK `outbox_events.id`; `attempt_no integer NOT NULL`; `status outbox_status NOT NULL`; `worker_id varchar(120) NOT NULL`; `broker_message_id varchar(180) NULL`; `error_code varchar(80) NULL`; `next_retry_at timestamptz NULL`; `payload_hash char(64) NOT NULL`.
- Ràng buộc: unique `(outbox_event_id,attempt_no)`; attempt>=1; status không dùng PENDING, event chưa có attempt là pending; PUBLISHED là terminal; DEAD_LETTER chỉ sau retry policy.
- Chỉ mục: `(outbox_event_id,attempt_no DESC)`; `(status,next_retry_at,occurred_at)`; append-only 24 tháng.

## 5. Database Study (`study_db`)

### 5.1 Projection danh tính, hồ sơ và RBAC cục bộ

#### TBL-STU-001 — `identity_projections`

- Tập cột: `ENTITY`.
- Cột riêng: `identity_subject_id uuid NOT NULL UNIQUE`; `account_status account_status NOT NULL`; `email_verified boolean NOT NULL DEFAULT false`; `display_name varchar(120) NULL`; `identity_version bigint NOT NULL`; `last_event_id uuid NOT NULL UNIQUE`; `projected_at timestamptz NOT NULL`.
- Ràng buộc: `identity_version>=1`; đây không phải FK sang Identity.
- Chỉ mục: `(account_status)`; PII tối thiểu, cập nhật idempotent theo version.

#### TBL-STU-002 — `learner_profiles`

- Tập cột: `ENTITY`.
- Cột riêng: `identity_subject_id uuid NOT NULL UNIQUE`; `full_name varchar(160) NULL`; `avatar_file_id uuid NULL`; `headline varchar(200) NULL`; `bio varchar(2000) NULL`; `birth_year smallint NULL`; `city_code varchar(20) NULL`; `onboarding_completed_at timestamptz NULL`; `profile_visibility varchar(20) NOT NULL DEFAULT 'PRIVATE'`; `deleted_at timestamptz NULL`.
- Ràng buộc: birth year hợp lý từ 1900 đến năm hiện tại-13; visibility `PRIVATE|PLATFORM`; avatar FK deferred tới file table, chỉ file CLEAN.
- Chỉ mục: `(onboarding_completed_at)`; `(deleted_at)`; PII.

#### TBL-STU-003 — `service_roles`

- Tập cột: `ENTITY`.
- Cột riêng: `code varchar(80) NOT NULL UNIQUE`; `name varchar(120) NOT NULL`; `description varchar(500) NOT NULL`; `is_privileged boolean NOT NULL DEFAULT false`; `disabled_at timestamptz NULL`.
- Ràng buộc: code chữ hoa ổn định; privileged role không được cấp khi JWT thiếu MFA claim.
- Chỉ mục: `(disabled_at,code)`.

#### TBL-STU-004 — `service_permissions`

- Tập cột: `ENTITY`.
- Cột riêng: `code varchar(120) NOT NULL UNIQUE`; `description varchar(500) NOT NULL`; `risk_level smallint NOT NULL DEFAULT 1`.
- Ràng buộc: `risk_level BETWEEN 1 AND 5`.
- Chỉ mục: `(risk_level,code)`.

#### TBL-STU-005 — `service_role_permissions`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `role_id uuid NOT NULL` FK `service_roles.id`; `permission_id uuid NOT NULL` FK `service_permissions.id`; `granted_by_subject_id uuid NOT NULL`; `revoked_at timestamptz NULL`; `revoked_by_subject_id uuid NULL`.
- Ràng buộc: partial unique `(role_id,permission_id)` khi active; revoke yêu cầu actor.
- Chỉ mục: `(role_id,revoked_at)`; `(permission_id,revoked_at)`.

#### TBL-STU-006 — `service_role_assignments`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `identity_subject_id uuid NOT NULL`; `role_id uuid NOT NULL` FK `service_roles.id`; `valid_from timestamptz NOT NULL DEFAULT now()`; `valid_until timestamptz NULL`; `granted_by_subject_id uuid NOT NULL`; `reason varchar(500) NOT NULL`; `revoked_at timestamptz NULL`; `revoked_by_subject_id uuid NULL`.
- Ràng buộc: active unique `(identity_subject_id,role_id)`; thời hạn hợp lệ; privileged access được đối chiếu MFA claim từ JWT.
- Chỉ mục: `(identity_subject_id,revoked_at,valid_until)`.

### 5.2 Onboarding và gợi ý lộ trình

#### TBL-STU-007 — `onboarding_submissions`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `learner_id uuid NOT NULL` FK `learner_profiles.id`; `schema_version integer NOT NULL`; `answers jsonb NOT NULL`; `submitted_at timestamptz NOT NULL`; `supersedes_id uuid NULL` self-FK; `is_current boolean NOT NULL DEFAULT true`.
- Ràng buộc: `schema_version>=1`; partial unique `(learner_id)` khi current; JSON validate ở API bằng schema version.
- Chỉ mục: `(learner_id,submitted_at DESC)`; PII; giữ 13 tháng sau thay thế rồi aggregate/anonymize.

#### TBL-STU-008 — `path_recommendation_runs`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `learner_id uuid NOT NULL` FK `learner_profiles.id`; `onboarding_submission_id uuid NOT NULL` FK `onboarding_submissions.id`; `algorithm_version varchar(40) NOT NULL`; `input_snapshot jsonb NOT NULL`; `ranked_path_version_ids uuid[] NOT NULL`; `reason_snapshot jsonb NOT NULL`; `generated_at timestamptz NOT NULL`; `expires_at timestamptz NOT NULL`.
- Ràng buộc: arrays không rỗng, không trùng ID; expiry sau generated.
- Chỉ mục: `(learner_id,generated_at DESC)`; DERIVED_SENSITIVE; giữ 13 tháng.

### 5.3 Nội dung có phiên bản bất biến

#### TBL-STU-009 — `learning_paths`

- Tập cột: `ENTITY`.
- Cột riêng: `slug varchar(120) NOT NULL UNIQUE`; `owner_subject_id uuid NOT NULL`; `current_draft_version_id uuid NULL`; `latest_published_version_id uuid NULL`; `archived_at timestamptz NULL`.
- Ràng buộc: hai pointer nếu có phải trỏ version cùng path; published pointer chỉ trỏ PUBLISHED; slug lowercase/kebab-case.
- Chỉ mục: `(archived_at,updated_at DESC)`.

#### TBL-STU-010 — `learning_path_versions`

- Tập cột: `ENTITY`; được sửa bằng `row_version` khi DRAFT, bị khóa bất biến từ lúc submit/publish.
- Cột riêng: `path_id uuid NOT NULL` FK `learning_paths.id`; `version_no integer NOT NULL`; `status content_version_status NOT NULL DEFAULT 'DRAFT'`; `title varchar(200) NOT NULL`; `summary varchar(1000) NOT NULL`; `description_markdown text NOT NULL`; `estimated_hours integer NOT NULL`; `cover_file_id uuid NULL`; `content_hash char(64) NOT NULL`; `created_by_subject_id uuid NOT NULL`; `published_at timestamptz NULL`; `superseded_at timestamptz NULL`; `discarded_at timestamptz NULL`; `source_version_id uuid NULL` self-FK.
- Ràng buộc: unique `(path_id,version_no)`; `version_no>=1`; hours 1–10000; published yêu cầu published_at và content_hash. Sau `PUBLISHED`, trigger policy từ chối sửa mọi cột.
- Chỉ mục: `(path_id,status,version_no DESC)`; `(status,published_at DESC)`.

#### TBL-STU-011 — `courses`

- Tập cột: `ENTITY`.
- Cột riêng: `slug varchar(120) NOT NULL UNIQUE`; `owner_subject_id uuid NOT NULL`; `current_draft_version_id uuid NULL`; `latest_published_version_id uuid NULL`; `archived_at timestamptz NULL`.
- Ràng buộc: hai pointer nếu có phải trỏ version cùng course; published pointer chỉ trỏ PUBLISHED; slug lowercase/kebab-case.
- Chỉ mục: `(archived_at,updated_at DESC)`.

#### TBL-STU-012 — `course_versions`

- Tập cột: `ENTITY`; được sửa bằng `row_version` khi DRAFT, bị khóa bất biến từ lúc submit/publish.
- Cột riêng: `course_id uuid NOT NULL` FK `courses.id`; `version_no integer NOT NULL`; `status content_version_status NOT NULL DEFAULT 'DRAFT'`; `title varchar(200) NOT NULL`; `summary varchar(1000) NOT NULL`; `description_markdown text NOT NULL`; `level varchar(24) NOT NULL`; `estimated_minutes integer NOT NULL`; `thumbnail_file_id uuid NULL`; `content_hash char(64) NOT NULL`; `created_by_subject_id uuid NOT NULL`; `published_at timestamptz NULL`; `superseded_at timestamptz NULL`; `discarded_at timestamptz NULL`; `source_version_id uuid NULL` self-FK.
- Ràng buộc: unique `(course_id,version_no)`; level `BEGINNER|INTERMEDIATE|ADVANCED`; minutes 1–600000; immutable khi published.
- Chỉ mục: `(course_id,status,version_no DESC)`; GIN full-text expression trên title/summary cho catalog; `(status,published_at DESC)`.

#### TBL-STU-013 — `path_course_items`

- Tập cột: `ENTITY`; chỉ sửa khi path version cha còn DRAFT, bất biến sau submit.
- Cột riêng: `path_version_id uuid NOT NULL` FK `learning_path_versions.id`; `course_version_id uuid NOT NULL` FK `course_versions.id`; `position integer NOT NULL`; `is_required boolean NOT NULL DEFAULT true`; `unlock_rule jsonb NOT NULL DEFAULT '{}'`.
- Ràng buộc: unique `(path_version_id,position)` và `(path_version_id,course_version_id)`; `position>=1`; hai version phải PUBLISHED trước khi path publish.
- Chỉ mục: `(course_version_id,path_version_id)`.

#### TBL-STU-014 — `chapters`

- Tập cột: `ENTITY`; chỉ sửa khi course version cha còn DRAFT, bất biến sau submit.
- Cột riêng: `course_version_id uuid NOT NULL` FK `course_versions.id`; `title varchar(200) NOT NULL`; `summary varchar(1000) NULL`; `position integer NOT NULL`.
- Ràng buộc: unique `(course_version_id,position)`; `position>=1`; thừa hưởng tính immutable của course version.
- Chỉ mục: `(course_version_id,position)`.

#### TBL-STU-015 — `lessons`

- Tập cột: `ENTITY`; chỉ sửa khi course version cha còn DRAFT, bất biến sau submit.
- Cột riêng: `chapter_id uuid NOT NULL` FK `chapters.id`; `course_version_id uuid NOT NULL` FK `course_versions.id`; `title varchar(200) NOT NULL`; `summary varchar(1000) NULL`; `position integer NOT NULL`; `estimated_minutes integer NOT NULL`; `is_preview boolean NOT NULL DEFAULT false`.
- Ràng buộc: composite integrity bảo đảm chapter thuộc cùng course version; unique `(chapter_id,position)`; minutes 1–1440.
- Chỉ mục: `(course_version_id,chapter_id,position)`.

#### TBL-STU-016 — `content_blocks`

- Tập cột: `ENTITY`; chỉ sửa khi course version cha còn DRAFT, bất biến sau submit.
- Cột riêng: `lesson_id uuid NOT NULL` FK `lessons.id`; `block_type varchar(24) NOT NULL`; `position integer NOT NULL`; `content_json jsonb NOT NULL`; `plain_text text NULL`; `estimated_seconds integer NOT NULL DEFAULT 0`; `content_hash char(64) NOT NULL`.
- Ràng buộc: block type `MARKDOWN|VIDEO|IMAGE|EMBED|DOWNLOAD`; unique `(lesson_id,position)`; seconds >=0; HTML/Markdown đã sanitize; external embed theo allowlist.
- Chỉ mục: `(lesson_id,position)`; GIN full-text trên `plain_text` chỉ cho admin search.

#### TBL-STU-017 — `content_rights_attestations`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `resource_type varchar(24) NOT NULL`; `resource_version_id uuid NOT NULL`; `publisher_subject_id uuid NOT NULL`; `rights_basis varchar(40) NOT NULL`; `source_url varchar(2048) NULL`; `license_code varchar(80) NULL`; `attestation_text_hash char(64) NOT NULL`; `attested_at timestamptz NOT NULL`; `expires_at timestamptz NULL`; `revoked_at timestamptz NULL`.
- Ràng buộc: resource `PATH_VERSION|COURSE_VERSION`; rights basis trong `OWNED|LICENSED|OPEN_LICENSE|AUTHORIZED`; expiry sau attest.
- Chỉ mục: `(resource_type,resource_version_id,revoked_at)`; giữ cùng vòng đời nội dung và audit.

#### TBL-STU-018 — `content_review_decisions`

- Tập cột: `APPEND`.
- Cột riêng: `resource_type varchar(24) NOT NULL`; `resource_version_id uuid NOT NULL`; `reviewer_subject_id uuid NOT NULL`; `decision varchar(24) NOT NULL`; `reason_codes varchar(80)[] NOT NULL`; `comment varchar(2000) NULL`; `expected_row_version bigint NOT NULL`; `trace_id varchar(64) NOT NULL`.
- Ràng buộc: decision `APPROVE|REJECT|REQUEST_CHANGES`; reason required khi không approve; một review round chốt bằng optimistic lock của resource.
- Chỉ mục: `(resource_type,resource_version_id,occurred_at DESC)`; audit retention 24 tháng tối thiểu.

#### TBL-STU-019 — `trusted_publisher_grants`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `publisher_subject_id uuid NOT NULL`; `scope varchar(24) NOT NULL`; `valid_from timestamptz NOT NULL`; `valid_until timestamptz NOT NULL`; `granted_by_subject_id uuid NOT NULL`; `grant_reason varchar(1000) NOT NULL`; `eligibility_snapshot jsonb NOT NULL`; `revoked_at timestamptz NULL`; `revoked_by_subject_id uuid NULL`; `revoke_reason varchar(1000) NULL`.
- Ràng buộc: scope `STUDY_CONTENT`; valid_until>valid_from; partial unique publisher/scope khi active. Trusted publisher vẫn cần rights, sanitization, scan và audit.
- Chỉ mục: `(publisher_subject_id,scope,revoked_at,valid_until)`.

### 5.4 Assessment và rubric

#### TBL-STU-020 — `assessments`

- Tập cột: `ENTITY`; chỉ sửa khi course version cha còn DRAFT, bất biến sau submit.
- Cột riêng: `course_version_id uuid NOT NULL` FK `course_versions.id`; `type assessment_type NOT NULL`; `title varchar(200) NOT NULL`; `instructions_markdown text NOT NULL`; `max_attempts integer NULL`; `passing_score numeric(5,2) NULL`; `due_rule jsonb NULL`; `content_hash char(64) NOT NULL`.
- Ràng buộc: max attempts null hoặc 1–100; score 0–100; QUIZ yêu cầu passing score; published parent làm assessment immutable.
- Chỉ mục: `(course_version_id,type)`.

#### TBL-STU-021 — `assessment_placements`

- Tập cột: `ENTITY`; chỉ sửa khi version chứa placement còn DRAFT, bất biến sau submit.
- Cột riêng: `assessment_id uuid NOT NULL` FK `assessments.id`; `path_version_id uuid NULL` FK `learning_path_versions.id`; `course_version_id uuid NULL` FK `course_versions.id`; `chapter_id uuid NULL` FK `chapters.id`; `lesson_id uuid NULL` FK `lessons.id`; `position integer NOT NULL`; `is_required boolean NOT NULL DEFAULT true`.
- Ràng buộc: check chính xác một trong bốn scope ID khác null; unique `(assessment_id)` để một exercise có đúng một placement; position>=1; scope và assessment phải cùng cây phiên bản.
- Chỉ mục: partial theo từng scope với `(scope_id,position)`.

#### TBL-STU-022 — `quiz_questions`

- Tập cột: `ENTITY`; chỉ sửa khi course version cha còn DRAFT, bất biến sau submit.
- Cột riêng: `assessment_id uuid NOT NULL` FK `assessments.id`; `question_type varchar(24) NOT NULL`; `prompt_markdown text NOT NULL`; `explanation_markdown text NULL`; `position integer NOT NULL`; `points numeric(7,2) NOT NULL`; `shuffle_options boolean NOT NULL DEFAULT false`.
- Ràng buộc: type `SINGLE_CHOICE|MULTIPLE_CHOICE|TRUE_FALSE`; unique `(assessment_id,position)`; points>0.
- Chỉ mục: `(assessment_id,position)`.

#### TBL-STU-023 — `quiz_options`

- Tập cột: `ENTITY`; chỉ sửa khi course version cha còn DRAFT, bất biến sau submit.
- Cột riêng: `question_id uuid NOT NULL` FK `quiz_questions.id`; `label_markdown text NOT NULL`; `position integer NOT NULL`; `is_correct boolean NOT NULL`; `weight numeric(7,4) NOT NULL DEFAULT 1`.
- Ràng buộc: unique `(question_id,position)`; weight 0–1; mỗi question có ít nhất một đáp án đúng được validate khi publish.
- Chỉ mục: `(question_id,position)`; `is_correct` không trả về learner trước submit.

#### TBL-STU-024 — `rubrics`

- Tập cột: `ENTITY`; chỉ sửa khi course version cha còn DRAFT, bất biến sau submit.
- Cột riêng: `assessment_id uuid NOT NULL UNIQUE` FK `assessments.id`; `title varchar(200) NOT NULL`; `total_points numeric(7,2) NOT NULL`; `passing_points numeric(7,2) NOT NULL`; `version_no integer NOT NULL DEFAULT 1`.
- Ràng buộc: 0<passing<=total; chỉ dùng cho TEXT/LINK/FILE; rubric immutable theo assessment version.
- Chỉ mục: unique `assessment_id`.

#### TBL-STU-025 — `rubric_criteria`

- Tập cột: `ENTITY`; chỉ sửa khi course version cha còn DRAFT, bất biến sau submit.
- Cột riêng: `rubric_id uuid NOT NULL` FK `rubrics.id`; `name varchar(160) NOT NULL`; `description varchar(1000) NOT NULL`; `max_points numeric(7,2) NOT NULL`; `position integer NOT NULL`.
- Ràng buộc: unique `(rubric_id,position)`; max_points>0; tổng criteria bằng total points được kiểm tại publish.
- Chỉ mục: `(rubric_id,position)`.

### 5.5 Enrollment, fact tiến độ và completion

#### TBL-STU-026 — `primary_path_periods`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `learner_id uuid NOT NULL` FK `learner_profiles.id`; `path_version_id uuid NOT NULL` FK `learning_path_versions.id`; `status primary_path_status NOT NULL`; `started_at timestamptz NOT NULL`; `ended_at timestamptz NULL`; `end_reason varchar(80) NULL`; `supersedes_period_id uuid NULL` self-FK; `switch_request_id uuid NULL`; `selected_from_recommendation_id uuid NULL` FK `path_recommendation_runs.id`.
- Ràng buộc: exclusion/partial unique bảo đảm đúng một row `ACTIVE` mỗi learner; end timestamp required nếu không active; version phải PUBLISHED; switch tự phục vụ cách lần activation gần nhất ít nhất 168 giờ.
- Chỉ mục: `(learner_id,started_at DESC)`; `(path_version_id,status)`.

#### TBL-STU-027 — `course_enrollments`

- Tập cột: `ENTITY`.
- Cột riêng: `learner_id uuid NOT NULL` FK `learner_profiles.id`; `course_version_id uuid NOT NULL` FK `course_versions.id`; `source_type varchar(24) NOT NULL`; `source_path_period_id uuid NULL` FK `primary_path_periods.id`; `status enrollment_status NOT NULL DEFAULT 'ENROLLED'`; `enrolled_at timestamptz NOT NULL`; `first_started_at timestamptz NULL`; `completed_at timestamptz NULL`; `last_activity_at timestamptz NULL`; `hidden_from_my_courses_at timestamptz NULL`.
- Ràng buộc: unique `(learner_id,course_version_id)`; source `STANDALONE|PRIMARY_PATH|ADMIN`; path source yêu cầu period; completion timestamp theo status.
- Chỉ mục: `(learner_id,status,last_activity_at DESC)`; `(course_version_id,status)`.

#### TBL-STU-028 — `block_progress_facts`

- Tập cột: `ENTITY`.
- Cột riêng: `enrollment_id uuid NOT NULL` FK `course_enrollments.id`; `block_id uuid NOT NULL` FK `content_blocks.id`; `status progress_status NOT NULL DEFAULT 'NOT_STARTED'`; `first_started_at timestamptz NULL`; `completed_at timestamptz NULL`; `last_position_seconds integer NULL`; `last_event_id uuid NOT NULL UNIQUE`.
- Ràng buộc: unique `(enrollment_id,block_id)`; position>=0; block thuộc đúng course version của enrollment; status chỉ tiến trừ admin correction có audit.
- Chỉ mục: `(enrollment_id,status)`; `(block_id,status)`.

#### TBL-STU-029 — `lesson_progress_facts`

- Tập cột: `ENTITY`.
- Cột riêng: `enrollment_id uuid NOT NULL` FK `course_enrollments.id`; `lesson_id uuid NOT NULL` FK `lessons.id`; `status progress_status NOT NULL DEFAULT 'NOT_STARTED'`; `first_started_at timestamptz NULL`; `completed_at timestamptz NULL`; `completion_source varchar(24) NULL`.
- Ràng buộc: unique `(enrollment_id,lesson_id)`; lesson đúng course version; source `BLOCKS|ASSESSMENT|ADMIN` khi completed.
- Chỉ mục: `(enrollment_id,status)`.

#### TBL-STU-030 — `progress_snapshots`

- Tập cột: `ENTITY`.
- Cột riêng: `learner_id uuid NOT NULL` FK `learner_profiles.id`; `scope_type varchar(24) NOT NULL`; `scope_id uuid NOT NULL`; `completed_units integer NOT NULL`; `total_units integer NOT NULL`; `percent numeric(5,2) NOT NULL`; `source_high_watermark timestamptz NOT NULL`; `rebuilt_at timestamptz NOT NULL`; `calculation_version integer NOT NULL`.
- Ràng buộc: unique `(learner_id,scope_type,scope_id)`; scope `COURSE_VERSION|PATH_VERSION`; counts >=0, completed<=total, percent 0–100. Đây là cache rebuildable, không là nguồn sự thật.
- Chỉ mục: `(scope_type,scope_id,percent)`; `(learner_id,rebuilt_at DESC)`.

#### TBL-STU-031 — `course_completions`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `learner_id uuid NOT NULL` FK `learner_profiles.id`; `course_version_id uuid NOT NULL` FK `course_versions.id`; `enrollment_id uuid NOT NULL UNIQUE` FK `course_enrollments.id`; `completed_at timestamptz NOT NULL`; `rule_version integer NOT NULL`; `facts_hash char(64) NOT NULL`; `revoked_at timestamptz NULL`; `revocation_reason varchar(500) NULL`.
- Ràng buộc: unique `(learner_id,course_version_id)`; chỉ tái sử dụng completion đúng cùng `course_version_id`; revoke không xóa lịch sử.
- Chỉ mục: `(learner_id,completed_at DESC)`; `(course_version_id,completed_at)`.

#### TBL-STU-032 — `path_completions`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `learner_id uuid NOT NULL` FK `learner_profiles.id`; `path_version_id uuid NOT NULL` FK `learning_path_versions.id`; `primary_path_period_id uuid NOT NULL` FK `primary_path_periods.id`; `completed_at timestamptz NOT NULL`; `rule_version integer NOT NULL`; `course_completion_ids uuid[] NOT NULL`; `facts_hash char(64) NOT NULL`; `revoked_at timestamptz NULL`; `revocation_reason varchar(500) NULL`.
- Ràng buộc: unique `(learner_id,path_version_id,primary_path_period_id)`; array đủ course required và không trùng.
- Chỉ mục: `(learner_id,completed_at DESC)`.

### 5.6 Attempt, file scan và review

#### TBL-STU-033 — `assessment_attempts`

- Tập cột: `ENTITY`.
- Cột riêng: `learner_id uuid NOT NULL` FK `learner_profiles.id`; `enrollment_id uuid NOT NULL` FK `course_enrollments.id`; `assessment_id uuid NOT NULL` FK `assessments.id`; `attempt_no integer NOT NULL`; `status attempt_status NOT NULL DEFAULT 'SUBMITTED'`; `submitted_payload_snapshot jsonb NOT NULL`; `submitted_at timestamptz NOT NULL`; `auto_score numeric(7,2) NULL`; `final_score numeric(7,2) NULL`; `graded_at timestamptz NULL`; `grader_subject_id uuid NULL`; `content_hash char(64) NOT NULL`.
- Ràng buộc: unique `(learner_id,assessment_id,attempt_no)`; `attempt_no>=1`; submission snapshot/hash bất biến ngay khi insert; score không âm và không vượt rubric/quiz total; learner/enrollment/assessment phải cùng course version. QUIZ chuyển đồng bộ `SUBMITTED→PASSED|FAILED`; TEXT/LINK/FILE chuyển `SUBMITTED→UNDER_REVIEW→PASSED|NEEDS_REVISION|FAILED`.
- Chỉ mục: `(learner_id,assessment_id,attempt_no DESC)`; `(status,submitted_at)` cho review queue.
- Concurrency: submit khóa learner-assessment và enrollment, cấp `attempt_no`, copy rồi seal/xóa liên kết draft trong cùng transaction; idempotency ngăn hai submit. Sau insert, payload/attempt number cấm sửa; chỉ status/score projection chuyển theo auto-grade hoặc append-only review.

#### TBL-STU-034 — `assessment_answers`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `attempt_id uuid NOT NULL` FK `assessment_attempts.id`; `question_id uuid NULL` FK `quiz_questions.id`; `answer_type assessment_type NOT NULL`; `answer_text text NULL`; `answer_url varchar(2048) NULL`; `selected_option_ids uuid[] NULL`; `answer_hash char(64) NOT NULL`; `position integer NOT NULL`.
- Ràng buộc: unique `(attempt_id,position)`; payload đúng loại: QUIZ cần option IDs, TEXT cần text 1–20000, LINK cần HTTPS URL và server không fetch, FILE có file relation; dữ liệu bất biến sau submit.
- Chỉ mục: `(attempt_id,position)`; PII có thể xuất hiện trong text.

#### TBL-STU-035 — `file_objects`

- Tập cột: `ENTITY`.
- Cột riêng: `owner_subject_id uuid NOT NULL`; `purpose varchar(40) NOT NULL`; `storage_key varchar(700) NOT NULL UNIQUE`; `original_name varchar(255) NOT NULL`; `declared_mime varchar(120) NOT NULL`; `detected_mime varchar(120) NULL`; `size_bytes bigint NOT NULL`; `sha256 char(64) NOT NULL`; `scan_status file_asset_status NOT NULL DEFAULT 'CREATED'`; `uploaded_at timestamptz NULL`; `available_at timestamptz NULL`; `quarantined_at timestamptz NULL`; `expires_at timestamptz NULL`; `deleted_at timestamptz NULL`.
- Ràng buộc: size 1 byte đến hạn mức theo purpose; unique `(sha256,owner_subject_id,purpose)` chỉ khi chưa deleted; MIME detected phải thuộc allowlist purpose; chỉ CLEAN mới available/downloadable.
- Chỉ mục: `(owner_subject_id,purpose,created_at DESC)`; `(scan_status,created_at)`; `(expires_at)` partial khi khác null.
- Dữ liệu: PII; object key không chứa filename/user data; signed URL tối đa 5 phút.

#### TBL-STU-036 — `malware_scan_results`

- Tập cột: `APPEND`.
- Cột riêng: `file_id uuid NOT NULL` FK `file_objects.id`; `scanner varchar(40) NOT NULL DEFAULT 'CLAMAV'`; `engine_version varchar(80) NOT NULL`; `signature_version varchar(80) NOT NULL`; `result file_asset_status NOT NULL`; `detected_mime varchar(120) NULL`; `threat_name varchar(200) NULL`; `error_code varchar(80) NULL`; `scan_duration_ms integer NOT NULL`; `worker_id varchar(120) NOT NULL`.
- Ràng buộc: result chỉ `CLEAN|INFECTED|SCAN_FAILED`; duration>=0; threat required khi infected.
- Chỉ mục: `(file_id,occurred_at DESC)`; `(result,occurred_at)`; giữ 24 tháng.

#### TBL-STU-037 — `attempt_files`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `attempt_id uuid NOT NULL` FK `assessment_attempts.id`; `answer_id uuid NOT NULL` FK `assessment_answers.id`; `file_id uuid NOT NULL` FK `file_objects.id`; `attached_at timestamptz NOT NULL`.
- Ràng buộc: unique `(attempt_id,file_id)`; file owner là learner của attempt, purpose `ASSESSMENT`, scan CLEAN trước submit.
- Chỉ mục: `(answer_id)`; không cascade khi attempt terminal.

#### TBL-STU-038 — `assessment_reviews`

- Tập cột: `APPEND`.
- Cột riêng: `attempt_id uuid NOT NULL` FK `assessment_attempts.id`; `review_round integer NOT NULL`; `reviewer_subject_id uuid NOT NULL`; `decision review_decision NOT NULL`; `score numeric(7,2) NULL`; `feedback_markdown text NOT NULL`; `expected_attempt_version bigint NOT NULL`; `supersedes_review_id uuid NULL` self-FK; `trace_id varchar(64) NOT NULL`.
- Ràng buộc: unique `(attempt_id,review_round)`; score hợp lệ; `NEEDS_REVISION`/`FAILED` yêu cầu feedback; optimistic update trạng thái attempt chỉ cho một reviewer thắng.
- Chỉ mục: `(attempt_id,review_round DESC)`; `(reviewer_subject_id,occurred_at DESC)`; giữ 24 tháng.

#### TBL-STU-039 — `assessment_review_scores`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `review_id uuid NOT NULL` FK `assessment_reviews.id`; `criterion_id uuid NOT NULL` FK `rubric_criteria.id`; `points numeric(7,2) NOT NULL`; `comment varchar(1000) NULL`.
- Ràng buộc: unique `(review_id,criterion_id)`; points từ 0 đến criterion.max_points; tổng bằng review score.
- Chỉ mục: `(review_id)`.

### 5.7 Evidence học tập

#### TBL-STU-040 — `evidence_records`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `learner_id uuid NOT NULL` FK `learner_profiles.id`; `evidence_type varchar(32) NOT NULL`; `source_type varchar(32) NOT NULL`; `source_id uuid NOT NULL`; `source_version_id uuid NOT NULL`; `status evidence_status NOT NULL DEFAULT 'ISSUED'`; `title varchar(200) NOT NULL`; `description varchar(1000) NOT NULL`; `issued_at timestamptz NOT NULL`; `expires_at timestamptz NULL`; `revoked_at timestamptz NULL`; `revocation_reason varchar(500) NULL`; `claims_snapshot jsonb NOT NULL`; `claims_hash char(64) NOT NULL`; `issuer_key_id varchar(80) NOT NULL`; `signature varchar(512) NOT NULL`; `schema_version integer NOT NULL`.
- Ràng buộc: unique `(learner_id,source_type,source_id,source_version_id,evidence_type)`; source version bắt buộc; revoked timestamp/reason theo status; claims là tối thiểu và không chứa contact.
- Chỉ mục: `(learner_id,status,issued_at DESC)`; `(source_type,source_id)`; `(expires_at)`.
- Retention: trong Study giữ cùng completion; export ra Work luôn tạo snapshot theo application, không cấp quyền search.

#### TBL-STU-041 — `evidence_export_requests`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `request_id uuid NOT NULL UNIQUE`; `application_id uuid NOT NULL`; `learner_identity_subject_id uuid NOT NULL`; `requested_evidence_ids uuid[] NOT NULL`; `consent_id uuid NOT NULL`; `requester_service varchar(20) NOT NULL DEFAULT 'WORK'`; `request_signature_hash char(64) NOT NULL`; `requested_at timestamptz NOT NULL`; `processed_at timestamptz NULL`; `result_code varchar(80) NULL`; `response_hash char(64) NULL`; `trace_id varchar(64) NOT NULL`.
- Ràng buộc: evidence IDs không rỗng/không trùng; ownership, `ISSUED`, version, expiry/revocation được kiểm tại thời điểm xử lý; unique request đảm bảo idempotent.
- Chỉ mục: `(learner_identity_subject_id,requested_at DESC)`; `(application_id)`; giữ tối thiểu 24 tháng như consent audit.

### 5.8 Notification, community và support

#### TBL-STU-042 — `notification_preferences`

- Tập cột: `ENTITY`.
- Cột riêng: `learner_id uuid NOT NULL` FK `learner_profiles.id`; `category varchar(40) NOT NULL`; `in_app_enabled boolean NOT NULL DEFAULT true`; `email_enabled boolean NOT NULL DEFAULT true`; `quiet_hours_start time NULL`; `quiet_hours_end time NULL`; `timezone varchar(64) NOT NULL`; `consent_source varchar(40) NOT NULL`.
- Ràng buộc: unique `(learner_id,category)`; transactional/security category không được tắt bằng preference.
- Chỉ mục: `(learner_id,category)`.

#### TBL-STU-043 — `notifications`

- Tập cột: `ENTITY`.
- Cột riêng: `learner_id uuid NOT NULL` FK `learner_profiles.id`; `category varchar(40) NOT NULL`; `template_code varchar(80) NOT NULL`; `template_version integer NOT NULL`; `title varchar(200) NOT NULL`; `body varchar(4000) NOT NULL`; `action_url varchar(1000) NULL`; `dedupe_key varchar(180) NOT NULL`; `read_at timestamptz NULL`; `expires_at timestamptz NOT NULL`; `payload jsonb NOT NULL DEFAULT '{}'`.
- Ràng buộc: unique `(learner_id,dedupe_key)`; action URL chỉ internal allowlist; payload đã redaction.
- Chỉ mục: `(learner_id,read_at,created_at DESC,id DESC)` hỗ trợ cursor; `(expires_at)`.
- Retention: 180 ngày rồi purge.

#### TBL-STU-044 — `notification_deliveries`

- Tập cột: `APPEND`.
- Cột riêng: `notification_id uuid NOT NULL` FK `notifications.id`; `channel varchar(16) NOT NULL`; `status notification_status NOT NULL`; `provider_message_id varchar(160) NULL`; `attempt_no integer NOT NULL`; `error_code varchar(80) NULL`; `next_retry_at timestamptz NULL`; `dedupe_key varchar(180) NOT NULL`.
- Ràng buộc: unique `(notification_id,channel,attempt_no)` và `dedupe_key`; channel `IN_APP|EMAIL`; attempt>=1.
- Chỉ mục: `(status,next_retry_at)`; giữ 180 ngày.

#### TBL-STU-045 — `community_channels`

- Tập cột: `ENTITY`.
- Cột riêng: `scope_type varchar(24) NOT NULL`; `scope_id uuid NOT NULL`; `provider varchar(20) NOT NULL DEFAULT 'ZALO'`; `name varchar(160) NOT NULL`; `join_url_ciphertext bytea NOT NULL`; `url_fingerprint char(64) NOT NULL`; `rules_version integer NOT NULL`; `active_from timestamptz NOT NULL`; `active_until timestamptz NULL`; `disabled_at timestamptz NULL`.
- Ràng buộc: scope `PLATFORM|PATH_VERSION|COURSE_VERSION`; provider hiện chỉ ZALO; unique active `(scope_type,scope_id,provider)`; HTTPS URL.
- Chỉ mục: `(scope_type,scope_id,disabled_at)`; join URL SENSITIVE, không lộ ở public catalog.

#### TBL-STU-046 — `community_acceptances`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `learner_id uuid NOT NULL` FK `learner_profiles.id`; `channel_id uuid NOT NULL` FK `community_channels.id`; `rules_version integer NOT NULL`; `accepted_at timestamptz NOT NULL`; `ip_hash char(64) NULL`; `revoked_at timestamptz NULL`.
- Ràng buộc: active unique `(learner_id,channel_id,rules_version)`; chỉ cấp URL sau acceptance và enrollment/permission check.
- Chỉ mục: `(learner_id,accepted_at DESC)`; giữ 24 tháng.

#### TBL-STU-047 — `support_tickets`

- Tập cột: `ENTITY`.
- Cột riêng: `learner_id uuid NOT NULL` FK `learner_profiles.id`; `category varchar(40) NOT NULL`; `status varchar(24) NOT NULL DEFAULT 'OPEN'`; `subject varchar(200) NOT NULL`; `description text NOT NULL`; `priority varchar(16) NOT NULL DEFAULT 'NORMAL'`; `assigned_to_subject_id uuid NULL`; `resolved_at timestamptz NULL`; `cancelled_at timestamptz NULL`; `resolution_code varchar(80) NULL`.
- Ràng buộc: status `OPEN|IN_PROGRESS|WAITING_LEARNER|RESOLVED|CANCELLED`; priority `LOW|NORMAL|HIGH|URGENT`; terminal timestamp phù hợp.
- Chỉ mục: `(learner_id,created_at DESC)`; `(status,priority,created_at)`; PII, giữ 13 tháng sau terminal.

#### TBL-STU-048 — `support_messages`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `ticket_id uuid NOT NULL` FK `support_tickets.id`; `author_subject_id uuid NOT NULL`; `author_type varchar(16) NOT NULL`; `body text NOT NULL`; `attachment_file_ids uuid[] NOT NULL DEFAULT '{}'`; `is_internal boolean NOT NULL DEFAULT false`; `sent_at timestamptz NOT NULL`.
- Ràng buộc: author `LEARNER|STAFF`; learner không thể tạo internal; file ownership/purpose/scan được kiểm.
- Chỉ mục: `(ticket_id,sent_at,id)`; PII; giữ như ticket.

### 5.9 Vận hành Study

#### TBL-STU-049 — `admin_adjustments`

- Tập cột: `APPEND`.
- Cột riêng: `target_type varchar(32) NOT NULL`; `target_id uuid NOT NULL`; `action varchar(80) NOT NULL`; `before_snapshot jsonb NOT NULL`; `after_snapshot jsonb NOT NULL`; `reason varchar(1000) NOT NULL`; `approved_by_subject_id uuid NOT NULL`; `performed_by_subject_id uuid NOT NULL`; `trace_id varchar(64) NOT NULL`.
- Ràng buộc: maker-checker cho adjustment rủi ro cao; before/after redacted nhưng đủ khôi phục logic.
- Chỉ mục: `(target_type,target_id,occurred_at DESC)`; 24 tháng.

#### TBL-STU-050 — `audit_events`

- Tập cột: `APPEND`.
- Cột riêng: `actor_subject_id uuid NULL`; `action varchar(120) NOT NULL`; `resource_type varchar(80) NOT NULL`; `resource_id uuid NULL`; `outcome audit_outcome NOT NULL`; `business_code varchar(80) NOT NULL`; `trace_id varchar(64) NOT NULL`; `tenant_context jsonb NULL`; `changes jsonb NULL`; `metadata jsonb NOT NULL DEFAULT '{}'`; `prev_hash char(64) NULL`; `event_hash char(64) NOT NULL UNIQUE`; `legal_hold_until timestamptz NULL`.
- Ràng buộc: canonical event hash nối prev_hash theo partition; changes/metadata schema-validated và redacted; denied/failure có business code cụ thể.
- Chỉ mục: `(resource_type,resource_id,occurred_at DESC)`; `(actor_subject_id,occurred_at DESC)`; `(trace_id)`; BRIN time.
- Retention: tối thiểu 24 tháng, append-only, redaction PII theo policy.

#### TBL-STU-051 — `idempotency_keys`

- Tập cột: `ENTITY`.
- Cột riêng: `actor_subject_id uuid NULL`; `operation varchar(120) NOT NULL`; `key_hash char(64) NOT NULL`; `request_hash char(64) NOT NULL`; `response_status integer NULL`; `response_body jsonb NULL`; `locked_until timestamptz NULL`; `completed_at timestamptz NULL`; `expires_at timestamptz NOT NULL`.
- Ràng buộc: unique `(actor_subject_id,operation,key_hash)`; cùng key khác request hash trả conflict; response đã redaction.
- Chỉ mục: `(expires_at)`; giữ 24 giờ, enroll/switch/submit 7 ngày.

#### TBL-STU-052 — `outbox_events`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `aggregate_type varchar(80) NOT NULL`; `aggregate_id uuid NOT NULL`; `event_type varchar(120) NOT NULL`; `event_version integer NOT NULL`; `payload jsonb NOT NULL`; `available_at timestamptz NOT NULL DEFAULT now()`; `dedupe_key varchar(180) NOT NULL UNIQUE`; `trace_id varchar(64) NOT NULL`.
- Ràng buộc: event version>=1; payload có `schemaVersion`, `occurredAt`, `producer`, `traceId`; evidence revocation dedupe theo evidence/version; row append-only.
- Chỉ mục: `(available_at,id)`; `(aggregate_type,aggregate_id,created_at)`; giữ 24 tháng.

#### TBL-STU-053 — `consumer_inbox`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `consumer varchar(100) NOT NULL`; `event_id uuid NOT NULL`; `event_type varchar(120) NOT NULL`; `payload_hash char(64) NOT NULL`; `received_at timestamptz NOT NULL DEFAULT now()`; `processed_at timestamptz NULL`; `result_code varchar(80) NULL`; `trace_id varchar(64) NOT NULL`.
- Ràng buộc: unique `(consumer,event_id)`; cùng event khác payload hash là security error; dùng cho Identity projection và Work acknowledgement.
- Chỉ mục: `(consumer,processed_at,received_at)`; giữ 24 tháng.

#### TBL-STU-054 — `report_snapshots`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `report_code varchar(80) NOT NULL`; `period_start timestamptz NOT NULL`; `period_end timestamptz NOT NULL`; `dimension_hash char(64) NOT NULL`; `dimensions jsonb NOT NULL`; `metrics jsonb NOT NULL`; `source_high_watermark timestamptz NOT NULL`; `calculation_version integer NOT NULL`; `generated_at timestamptz NOT NULL`.
- Ràng buộc: unique `(report_code,period_start,period_end,dimension_hash,calculation_version)`; period end>start; metrics không chứa row-level PII.
- Chỉ mục: `(report_code,period_end DESC)`; giữ 13 tháng, không là warehouse.

#### TBL-STU-055 — `outbox_delivery_attempts`

- Tập cột và toàn bộ quy tắc như `TBL-IAM-020`, với `outbox_event_id` FK `TBL-STU-052`; unique event/attempt; index event/latest và status/retry; append-only 24 tháng.
- Cột riêng đầy đủ: `outbox_event_id uuid NOT NULL`; `attempt_no integer NOT NULL`; `status outbox_status NOT NULL`; `worker_id varchar(120) NOT NULL`; `broker_message_id varchar(180) NULL`; `error_code varchar(80) NULL`; `next_retry_at timestamptz NULL`; `payload_hash char(64) NOT NULL`.

#### TBL-STU-056 — `study_skills`

- Tập cột: `ENTITY`.
- Cột riêng: `code varchar(80) NOT NULL UNIQUE`; `name varchar(160) NOT NULL`; `normalized_name varchar(160) NOT NULL UNIQUE`; `category varchar(80) NULL`; `description varchar(1000) NULL`; `status varchar(16) NOT NULL DEFAULT 'ACTIVE'`; `aliases varchar(160)[] NOT NULL DEFAULT '{}'`.
- Ràng buộc: status `ACTIVE|ARCHIVED`; taxonomy Study độc lập với Work, mapping ra ngoài bằng signed code/version chứ không cross-DB FK.
- Chỉ mục: GIN trigram normalized name; GIN aliases; `(status,category)`.

#### TBL-STU-057 — `course_skill_outcomes`

- Tập cột: `ENTITY`; chỉ sửa khi course version còn DRAFT, bất biến sau submit.
- Cột riêng: `course_version_id uuid NOT NULL` FK `course_versions.id`; `skill_id uuid NOT NULL` FK `study_skills.id`; `outcome_level smallint NOT NULL`; `description varchar(1000) NOT NULL`; `position integer NOT NULL`.
- Ràng buộc: unique `(course_version_id,skill_id)` và `(course_version_id,position)`; level 1–5; archived skill không được thêm vào draft mới.
- Chỉ mục: `(skill_id,course_version_id)`; `(course_version_id,position)`.

#### TBL-STU-058 — `course_prerequisites`

- Tập cột: `ENTITY`; chỉ sửa khi course version còn DRAFT, bất biến sau submit.
- Cột riêng: `course_version_id uuid NOT NULL` FK `course_versions.id`; `required_course_version_id uuid NOT NULL` FK `course_versions.id`; `require_completion boolean NOT NULL DEFAULT true`; `position integer NOT NULL`.
- Ràng buộc: unique `(course_version_id,required_course_version_id)` và `(course_version_id,position)`; không tự tham chiếu; graph không chu trình được kiểm khi publish; prerequisite luôn pin đúng version.
- Chỉ mục: `(required_course_version_id,course_version_id)`; `(course_version_id,position)`.

#### TBL-STU-059 — `file_upload_sessions`

- Tập cột: `ENTITY`.
- Cột riêng: `file_id uuid NOT NULL UNIQUE` FK `file_objects.id`; `owner_subject_id uuid NOT NULL`; `upload_id varchar(200) NOT NULL UNIQUE`; `expected_size_bytes bigint NOT NULL`; `expected_sha256 char(64) NOT NULL`; `part_count integer NOT NULL DEFAULT 1`; `status varchar(24) NOT NULL DEFAULT 'CREATED'`; `expires_at timestamptz NOT NULL`; `completed_at timestamptz NULL`; `aborted_at timestamptz NULL`.
- Ràng buộc: size >0 theo purpose limit; parts 1–10000; status `CREATED|UPLOADING|COMPLETED|ABORTED|EXPIRED`; finalize đối chiếu size/hash rồi mới enqueue scan.
- Chỉ mục: `(owner_subject_id,status,created_at DESC)`; `(status,expires_at)`; purge session 7 ngày sau terminal.

#### TBL-STU-060 — `assessment_drafts`

- Tập cột: `ENTITY`; row chỉ mutable trước khi bị seal.
- Cột riêng: `learner_id uuid NOT NULL` FK `learner_profiles.id`; `enrollment_id uuid NOT NULL` FK `course_enrollments.id`; `assessment_id uuid NOT NULL` FK `assessments.id`; `answer_type assessment_type NOT NULL`; `payload jsonb NOT NULL`; `file_id uuid NULL` FK `file_objects.id`; `state varchar(16) NOT NULL DEFAULT 'DRAFT'`; `last_saved_at timestamptz NOT NULL`; `sealed_at timestamptz NULL`; `sealed_attempt_id uuid NULL` FK `assessment_attempts.id`; `content_hash char(64) NOT NULL`.
- Ràng buộc: unique `(learner_id,assessment_id)`; state chỉ `DRAFT|SEALED`; SEALED yêu cầu `sealed_at` và `sealed_attempt_id`, sau đó cấm sửa payload; subtype/size/HTTPS/file owner và CLEAN được validate như API. Draft không cấp `attempt_no` và không tính attempt limit.
- Chỉ mục: `(learner_id,assessment_id,state)`; `(enrollment_id,last_saved_at DESC)`.
- Concurrency/retention: `If-Match` dùng `row_version`; submit khóa draft và learner-assessment, tạo `TBL-STU-033`, rồi seal draft atomically. Draft chưa seal xóa theo yêu cầu learner hoặc sau 90 ngày không hoạt động; sealed draft giữ cùng attempt. `TBL-STU-060` là nguồn cho API draft, không dùng row attempt trạng thái DRAFT.

## 6. Database Work (`work_db`)

### 6.1 Projection danh tính và file chung

#### TBL-WRK-001 — `identity_projections`

- Tập cột: `ENTITY`.
- Cột riêng: `identity_subject_id uuid NOT NULL UNIQUE`; `account_status account_status NOT NULL`; `email_verified boolean NOT NULL DEFAULT false`; `display_name varchar(120) NULL`; `identity_version bigint NOT NULL`; `last_event_id uuid NOT NULL UNIQUE`; `projected_at timestamptz NOT NULL`.
- Ràng buộc/chỉ mục: như `TBL-STU-001`; không là cross-database FK.

#### TBL-WRK-002 — `file_objects`

- Tập cột và chính sách tương đương `TBL-STU-035`.
- Cột riêng đầy đủ: `owner_subject_id uuid NOT NULL`; `tenant_id uuid NULL`; `purpose varchar(40) NOT NULL`; `storage_key varchar(700) NOT NULL UNIQUE`; `original_name varchar(255) NOT NULL`; `declared_mime varchar(120) NOT NULL`; `detected_mime varchar(120) NULL`; `size_bytes bigint NOT NULL`; `sha256 char(64) NOT NULL`; `scan_status file_asset_status NOT NULL DEFAULT 'CREATED'`; `uploaded_at timestamptz NULL`; `available_at timestamptz NULL`; `quarantined_at timestamptz NULL`; `expires_at timestamptz NULL`; `deleted_at timestamptz NULL`.
- Ràng buộc: tenant bắt buộc với file tenant; chỉ CLEAN mới dùng; purpose `AVATAR|CV|PORTFOLIO|ENTERPRISE_LOGO|UNIVERSITY_LOGO|VERIFICATION|JOB|INVOICE`; hạn mức theo purpose. Chat V1 chỉ text/system nên không có file purpose CHAT.
- Chỉ mục: `(owner_subject_id,purpose,created_at DESC)`; `(tenant_id,purpose,created_at DESC)`; `(scan_status,created_at)`; `(expires_at)`.

#### TBL-WRK-003 — `malware_scan_results`

- Tập cột: `APPEND`.
- Cột riêng đầy đủ: `file_id uuid NOT NULL` FK `file_objects.id`; `scanner varchar(40) NOT NULL DEFAULT 'CLAMAV'`; `engine_version varchar(80) NOT NULL`; `signature_version varchar(80) NOT NULL`; `result file_asset_status NOT NULL`; `detected_mime varchar(120) NULL`; `threat_name varchar(200) NULL`; `error_code varchar(80) NULL`; `scan_duration_ms integer NOT NULL`; `worker_id varchar(120) NOT NULL`.
- Ràng buộc: result `CLEAN|INFECTED|SCAN_FAILED`; duration>=0; infected yêu cầu threat name.
- Chỉ mục: `(file_id,occurred_at DESC)`; `(result,occurred_at)`; giữ 24 tháng.

### 6.2 Candidate, CV và portfolio

#### TBL-WRK-004 — `candidate_profiles`

- Tập cột: `ENTITY`.
- Cột riêng: `identity_subject_id uuid NOT NULL UNIQUE`; `full_name varchar(160) NULL`; `headline varchar(200) NULL`; `summary text NULL`; `phone_ciphertext bytea NULL`; `phone_last4 char(4) NULL`; `city_code varchar(20) NULL`; `country_code char(2) NOT NULL DEFAULT 'VN'`; `avatar_file_id uuid NULL` FK `file_objects.id`; `visibility candidate_visibility NOT NULL DEFAULT 'PRIVATE'`; `search_opted_in_at timestamptz NULL`; `search_opted_out_at timestamptz NULL`; `available_from date NULL`; `deleted_at timestamptz NULL`.
- Ràng buộc: SEARCHABLE yêu cầu opted-in; opt-out timestamp khi PRIVATE sau opt-in; avatar CLEAN; phone E.164 trước encrypt.
- Chỉ mục: `(visibility,updated_at DESC)`; `(city_code,visibility)`; `(deleted_at)`; PII.

#### TBL-WRK-005 — `candidate_search_preferences`

- Tập cột: `ENTITY`.
- Cột riêng: `candidate_id uuid NOT NULL UNIQUE` FK `candidate_profiles.id`; `desired_titles varchar(120)[] NOT NULL DEFAULT '{}'`; `desired_locations varchar(20)[] NOT NULL DEFAULT '{}'`; `work_modes varchar(16)[] NOT NULL DEFAULT '{}'`; `employment_types varchar(24)[] NOT NULL DEFAULT '{}'`; `salary_min_vnd bigint NULL`; `salary_visibility boolean NOT NULL DEFAULT false`; `notice_days integer NULL`; `excluded_enterprise_ids uuid[] NOT NULL DEFAULT '{}'`.
- Ràng buộc: salary>=0, notice 0–365; arrays capped 20/20/5/10/200.
- Chỉ mục: GIN arrays cho search; dữ liệu chỉ vào search index khi profile SEARCHABLE.

#### TBL-WRK-006 — `skills`

- Tập cột: `ENTITY`.
- Cột riêng: `slug varchar(120) NOT NULL UNIQUE`; `name varchar(160) NOT NULL`; `normalized_name varchar(160) NOT NULL UNIQUE`; `category varchar(80) NULL`; `status varchar(16) NOT NULL DEFAULT 'ACTIVE'`; `aliases varchar(160)[] NOT NULL DEFAULT '{}'`.
- Ràng buộc: status `ACTIVE|ARCHIVED`; slug lowercase/kebab-case; aliases canonical không trùng normalized name khác.
- Chỉ mục: GIN trigram `normalized_name`; GIN aliases; PUBLIC taxonomy.

#### TBL-WRK-007 — `candidate_skills`

- Tập cột: `ENTITY`.
- Cột riêng: `candidate_id uuid NOT NULL` FK `candidate_profiles.id`; `skill_id uuid NOT NULL` FK `skills.id`; `proficiency smallint NULL`; `years_experience numeric(4,1) NULL`; `last_used_year smallint NULL`; `source varchar(24) NOT NULL`; `is_visible boolean NOT NULL DEFAULT true`.
- Ràng buộc: unique `(candidate_id,skill_id)`; proficiency 1–5; years 0–80; source `SELF|CV_PARSED|ADMIN`, parsed suggestion cần candidate confirmation trước searchable.
- Chỉ mục: `(skill_id,candidate_id)` partial visible; `(candidate_id,updated_at DESC)`.

#### TBL-WRK-008 — `candidate_experiences`

- Tập cột: `ENTITY`.
- Cột riêng: `candidate_id uuid NOT NULL` FK `candidate_profiles.id`; `company_name varchar(200) NOT NULL`; `title varchar(160) NOT NULL`; `start_date date NOT NULL`; `end_date date NULL`; `is_current boolean NOT NULL DEFAULT false`; `description text NULL`; `position integer NOT NULL`; `visibility varchar(16) NOT NULL DEFAULT 'PRIVATE'`.
- Ràng buộc: end>=start; current yêu cầu end null; unique `(candidate_id,position)`; visibility `PRIVATE|SEARCH`.
- Chỉ mục: `(candidate_id,position)`; PII.

#### TBL-WRK-009 — `candidate_educations`

- Tập cột: `ENTITY`.
- Cột riêng: `candidate_id uuid NOT NULL` FK `candidate_profiles.id`; `institution_name varchar(240) NOT NULL`; `degree varchar(160) NULL`; `field_of_study varchar(160) NULL`; `start_date date NULL`; `end_date date NULL`; `description varchar(2000) NULL`; `position integer NOT NULL`; `visibility varchar(16) NOT NULL DEFAULT 'PRIVATE'`.
- Ràng buộc: end>=start nếu đủ; unique `(candidate_id,position)`; visibility `PRIVATE|SEARCH`.
- Chỉ mục: `(candidate_id,position)`; PII.

#### TBL-WRK-010 — `cvs`

- Tập cột: `ENTITY`.
- Cột riêng: `candidate_id uuid NOT NULL` FK `candidate_profiles.id`; `title varchar(160) NOT NULL`; `is_default boolean NOT NULL DEFAULT false`; `current_draft_version_id uuid NULL`; `latest_published_version_id uuid NULL`; `archived_at timestamptz NULL`.
- Ràng buộc: partial unique `(candidate_id)` khi default và active; max 20 active CV/candidate enforced transactionally.
- Chỉ mục: `(candidate_id,archived_at,updated_at DESC)`.

#### TBL-WRK-011 — `cv_versions`

- Tập cột: `ENTITY`; chỉ sửa bằng `row_version` khi DRAFT, bất biến sau publish.
- Cột riêng: `cv_id uuid NOT NULL` FK `cvs.id`; `version_no integer NOT NULL`; `status cv_revision_status NOT NULL DEFAULT 'DRAFT'`; `template_code varchar(80) NOT NULL`; `template_version integer NOT NULL`; `content_json jsonb NOT NULL`; `rendered_file_id uuid NULL` FK `file_objects.id`; `source_file_id uuid NULL` FK `file_objects.id`; `content_hash char(64) NOT NULL`; `created_by_subject_id uuid NOT NULL`; `published_at timestamptz NULL`; `superseded_at timestamptz NULL`; `discarded_at timestamptz NULL`; `source_version_id uuid NULL` self-FK.
- Ràng buộc: unique `(cv_id,version_no)`; schema-validated content; published immutable và yêu cầu CLEAN rendered file; template entitlement kiểm khi publish/export.
- Chỉ mục: `(cv_id,status,version_no DESC)`; PII, giữ 12 tháng sau archive hoặc theo application snapshot.

#### TBL-WRK-012 — `portfolio_items`

- Tập cột: `ENTITY`.
- Cột riêng: `candidate_id uuid NOT NULL` FK `candidate_profiles.id`; `title varchar(200) NOT NULL`; `description text NULL`; `url varchar(2048) NULL`; `file_id uuid NULL` FK `file_objects.id`; `position integer NOT NULL`; `visibility varchar(16) NOT NULL DEFAULT 'PRIVATE'`; `published_at timestamptz NULL`; `archived_at timestamptz NULL`.
- Ràng buộc: chính xác ít nhất URL HTTPS hoặc CLEAN file; unique `(candidate_id,position)`; visibility `PRIVATE|SEARCH|APPLICATION_ONLY`.
- Chỉ mục: `(candidate_id,archived_at,position)`.

#### TBL-WRK-013 — `saved_jobs`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `candidate_id uuid NOT NULL` FK `candidate_profiles.id`; `job_id uuid NOT NULL`; `saved_at timestamptz NOT NULL`; `removed_at timestamptz NULL`.
- Ràng buộc: active unique `(candidate_id,job_id)`; remove là transition một chiều.
- Chỉ mục: `(candidate_id,removed_at,saved_at DESC)`.

### 6.3 Tenant Enterprise, membership và verification

#### TBL-WRK-014 — `enterprise_tenants`

- Tập cột: `ENTITY`.
- Cột riêng: `legal_name varchar(240) NOT NULL`; `display_name varchar(200) NOT NULL`; `tax_code varchar(32) NOT NULL`; `tax_code_country char(2) NOT NULL DEFAULT 'VN'`; `slug varchar(120) NOT NULL UNIQUE`; `status tenant_status NOT NULL DEFAULT 'PENDING_VERIFICATION'`; `website_url varchar(2048) NULL`; `description text NULL`; `logo_file_id uuid NULL` FK `file_objects.id`; `verified_at timestamptz NULL`; `suspended_at timestamptz NULL`; `closed_at timestamptz NULL`.
- Ràng buộc: unique `(tax_code_country,tax_code)`; ACTIVE yêu cầu verified_at; website HTTPS; logo CLEAN.
- Chỉ mục: `(status,created_at DESC)`; GIN trigram display name; PII/INTERNAL theo trường.

#### TBL-WRK-015 — `enterprise_verification_cases`

- Tập cột: `TENANT_ENTITY` với `tenant_id` FK `enterprise_tenants.id`.
- Cột riêng: `case_no integer NOT NULL`; `status varchar(24) NOT NULL DEFAULT 'SUBMITTED'`; `submitted_by_subject_id uuid NOT NULL`; `document_file_ids uuid[] NOT NULL`; `submitted_snapshot jsonb NOT NULL`; `reviewer_subject_id uuid NULL`; `reviewed_at timestamptz NULL`; `decision_reason_codes varchar(80)[] NOT NULL DEFAULT '{}'`; `comment varchar(2000) NULL`; `expires_at timestamptz NULL`.
- Ràng buộc: unique `(tenant_id,case_no)`; status `SUBMITTED|IN_REVIEW|APPROVED|REJECTED|EXPIRED`; documents không rỗng và đều CLEAN/VERIFICATION; reviewer required khi terminal.
- Chỉ mục: `(status,created_at)`; `(tenant_id,case_no DESC)`.
- Retention: verification documents xóa 180 ngày sau decision/expiry nếu không legal hold; giữ metadata/audit 24 tháng.

#### TBL-WRK-016 — `enterprise_memberships`

- Tập cột: `TENANT_ENTITY` với `tenant_id` FK `enterprise_tenants.id`.
- Cột riêng: `identity_subject_id uuid NOT NULL`; `role_code varchar(40) NOT NULL`; `status membership_status NOT NULL`; `joined_at timestamptz NULL`; `suspended_at timestamptz NULL`; `left_at timestamptz NULL`; `invited_by_subject_id uuid NULL`; `valid_until timestamptz NULL`.
- Ràng buộc: unique `(tenant_id,identity_subject_id)`; role `OWNER|ADMIN|RECRUITER|HIRING_MANAGER|BILLING|VIEWER`; active yêu cầu joined; ít nhất một active OWNER bằng deferred business constraint.
- Chỉ mục: `(identity_subject_id,status)`; `(tenant_id,status,role_code)`.

#### TBL-WRK-017 — `enterprise_invites`

- Tập cột: `TENANT_ENTITY` với `tenant_id` FK `enterprise_tenants.id`.
- Cột riêng: `email_normalized varchar(320) NOT NULL`; `email_ciphertext bytea NOT NULL`; `role_code varchar(40) NOT NULL`; `token_hash char(64) NOT NULL UNIQUE`; `invited_by_subject_id uuid NOT NULL`; `expires_at timestamptz NOT NULL`; `accepted_at timestamptz NULL`; `revoked_at timestamptz NULL`.
- Ràng buộc: partial unique `(tenant_id,email_normalized)` khi chưa accepted/revoked; expiry>created; không log raw email/token.
- Chỉ mục: `(tenant_id,expires_at)`; purge ciphertext/token sau 180 ngày.

#### TBL-WRK-018 — `trusted_publisher_grants`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `tenant_id uuid NOT NULL` FK `enterprise_tenants.id`; `scope varchar(24) NOT NULL DEFAULT 'JOB'`; `valid_from timestamptz NOT NULL`; `valid_until timestamptz NOT NULL`; `granted_by_subject_id uuid NOT NULL`; `grant_reason varchar(1000) NOT NULL`; `eligibility_snapshot jsonb NOT NULL`; `revoked_at timestamptz NULL`; `revoked_by_subject_id uuid NULL`; `revoke_reason varchar(1000) NULL`.
- Ràng buộc: active unique `(tenant_id,scope)`; thời hạn hợp lệ; eligibility snapshot ghi số publication approved và clean-day; bootstrap pilot phải có lý do admin.
- Chỉ mục: `(tenant_id,scope,revoked_at,valid_until)`; không bỏ qua automated validation/audit.

### 6.4 University tenant và consent

#### TBL-WRK-019 — `university_tenants`

- Tập cột: `ENTITY`.
- Cột riêng: `legal_name varchar(240) NOT NULL`; `display_name varchar(200) NOT NULL`; `institution_code varchar(80) NOT NULL UNIQUE`; `slug varchar(120) NOT NULL UNIQUE`; `status tenant_status NOT NULL DEFAULT 'PENDING_VERIFICATION'`; `website_url varchar(2048) NULL`; `logo_file_id uuid NULL` FK `file_objects.id`; `verified_at timestamptz NULL`; `suspended_at timestamptz NULL`; `closed_at timestamptz NULL`.
- Ràng buộc: ACTIVE cần verified; HTTPS; logo CLEAN.
- Chỉ mục: `(status,created_at DESC)`; GIN trigram display name.

#### TBL-WRK-020 — `university_verification_cases`

- Tập cột: `TENANT_ENTITY` với `tenant_id` FK `university_tenants.id`.
- Cột riêng: toàn bộ cột riêng của `TBL-WRK-015` gồm `case_no`, `status`, submitter, document IDs, snapshot, reviewer/decision/time/expiry; thêm `accreditation_code varchar(120) NULL`.
- Ràng buộc: unique `(tenant_id,case_no)`; cùng state machine verification; document phải CLEAN và đúng tenant.
- Chỉ mục: `(status,created_at)`; `(tenant_id,case_no DESC)`; retention tài liệu 180 ngày.

#### TBL-WRK-021 — `university_memberships`

- Tập cột: `TENANT_ENTITY` với `tenant_id` FK `university_tenants.id`.
- Cột riêng: `identity_subject_id uuid NOT NULL`; `role_code varchar(40) NOT NULL`; `status membership_status NOT NULL`; `joined_at timestamptz NULL`; `suspended_at timestamptz NULL`; `left_at timestamptz NULL`; `invited_by_subject_id uuid NULL`; `valid_until timestamptz NULL`.
- Ràng buộc: unique `(tenant_id,identity_subject_id)`; role `OWNER|ADMIN|COORDINATOR|ANALYST|VIEWER`; active cần joined; ít nhất một active OWNER.
- Chỉ mục: `(identity_subject_id,status)`; `(tenant_id,status,role_code)`.

#### TBL-WRK-022 — `university_invites`

- Tập cột: `TENANT_ENTITY` với `tenant_id` FK `university_tenants.id`.
- Cột riêng: `email_normalized varchar(320) NOT NULL`; `email_ciphertext bytea NOT NULL`; `role_code varchar(40) NOT NULL`; `token_hash char(64) NOT NULL UNIQUE`; `invited_by_subject_id uuid NOT NULL`; `expires_at timestamptz NOT NULL`; `accepted_at timestamptz NULL`; `revoked_at timestamptz NULL`.
- Ràng buộc: role theo University; active unique tenant/email; expiry>created; accepted/revoked một chiều.
- Chỉ mục: `(tenant_id,expires_at)`; purge ciphertext/token sau 180 ngày.

#### TBL-WRK-023 — `student_affiliations`

- Tập cột: `TENANT_ENTITY` với `tenant_id` FK `university_tenants.id`.
- Cột riêng: `candidate_id uuid NOT NULL` FK `candidate_profiles.id`; `student_code_ciphertext bytea NULL`; `student_code_fingerprint char(64) NULL`; `affiliation_status varchar(24) NOT NULL DEFAULT 'PENDING'`; `starts_on date NULL`; `ends_on date NULL`; `verified_by_subject_id uuid NULL`; `verified_at timestamptz NULL`; `revoked_at timestamptz NULL`.
- Ràng buộc: active unique `(tenant_id,candidate_id)`; fingerprint unique trong tenant khi có; status `PENDING|VERIFIED|REJECTED|ENDED|REVOKED`; date range hợp lệ.
- Chỉ mục: `(tenant_id,affiliation_status)`; `(candidate_id,affiliation_status)`; PII.

#### TBL-WRK-024 — `cohorts`

- Tập cột: `TENANT_ENTITY` với `tenant_id` FK `university_tenants.id`.
- Cột riêng: `code varchar(80) NOT NULL`; `name varchar(200) NOT NULL`; `academic_year varchar(20) NOT NULL`; `starts_on date NULL`; `ends_on date NULL`; `archived_at timestamptz NULL`.
- Ràng buộc: unique `(tenant_id,code)`; date range hợp lệ.
- Chỉ mục: `(tenant_id,academic_year,archived_at)`.

#### TBL-WRK-025 — `cohort_memberships`

- Tập cột: `TENANT_ENTITY` với `tenant_id` FK `university_tenants.id`.
- Cột riêng: `cohort_id uuid NOT NULL`; `affiliation_id uuid NOT NULL`; `joined_at timestamptz NOT NULL`; `left_at timestamptz NULL`.
- Ràng buộc: composite FK `(tenant_id,cohort_id)` -> cohorts và `(tenant_id,affiliation_id)` -> affiliations; active unique `(tenant_id,cohort_id,affiliation_id)`; left>=joined.
- Chỉ mục: `(tenant_id,cohort_id,left_at)`; `(tenant_id,affiliation_id)`.

#### TBL-WRK-026 — `internship_programs`

- Tập cột: `TENANT_ENTITY` với `tenant_id` FK `university_tenants.id`.
- Cột riêng: `code varchar(80) NOT NULL`; `name varchar(200) NOT NULL`; `description text NOT NULL`; `starts_on date NOT NULL`; `ends_on date NOT NULL`; `status varchar(24) NOT NULL DEFAULT 'DRAFT'`; `eligibility_rule jsonb NOT NULL`; `created_by_subject_id uuid NOT NULL`; `published_at timestamptz NULL`; `closed_at timestamptz NULL`.
- Ràng buộc: unique `(tenant_id,code)`; end>=start; status `DRAFT|PUBLISHED|CLOSED|CANCELLED`; schema-validated eligibility.
- Chỉ mục: `(tenant_id,status,starts_on)`.

#### TBL-WRK-027 — `campus_job_distributions`

- Tập cột: `TENANT_ENTITY` với `tenant_id` FK `university_tenants.id`.
- Cột riêng: `job_id uuid NOT NULL`; `program_id uuid NULL`; `cohort_id uuid NULL`; `distributed_by_subject_id uuid NOT NULL`; `distributed_at timestamptz NOT NULL`; `expires_at timestamptz NULL`; `message varchar(1000) NULL`; `withdrawn_at timestamptz NULL`.
- Ràng buộc: composite FKs tenant tới program/cohort; ít nhất một target; unique active `(tenant_id,job_id,program_id,cohort_id)`.
- Chỉ mục: `(tenant_id,distributed_at DESC)`; `(job_id,withdrawn_at)`.

#### TBL-WRK-028 — `partnerships`

- Tập cột: `TENANT_ENTITY` với `tenant_id` FK `university_tenants.id`.
- Cột riêng: `enterprise_tenant_id uuid NOT NULL` FK `enterprise_tenants.id`; `status varchar(24) NOT NULL DEFAULT 'PROPOSED'`; `scope jsonb NOT NULL`; `starts_on date NULL`; `ends_on date NULL`; `proposed_by_subject_id uuid NOT NULL`; `accepted_by_subject_id uuid NULL`; `accepted_at timestamptz NULL`; `ended_at timestamptz NULL`.
- Ràng buộc: unique active `(tenant_id,enterprise_tenant_id)`; status `PROPOSED|ACTIVE|DECLINED|ENDED`; date range hợp lệ.
- Chỉ mục: `(tenant_id,status)`; `(enterprise_tenant_id,status)`.

#### TBL-WRK-029 — `candidate_referrals`

- Tập cột: `TENANT_ENTITY` với `tenant_id` FK `university_tenants.id`.
- Cột riêng: `candidate_id uuid NOT NULL` FK `candidate_profiles.id`; `job_id uuid NOT NULL`; `affiliation_id uuid NOT NULL`; `referred_by_subject_id uuid NOT NULL`; `consent_grant_id uuid NOT NULL`; `status varchar(24) NOT NULL DEFAULT 'SENT'`; `message varchar(1000) NULL`; `sent_at timestamptz NOT NULL`; `responded_at timestamptz NULL`.
- Ràng buộc: composite affiliation FK; unique `(tenant_id,candidate_id,job_id)`; status `SENT|VIEWED|ACCEPTED|DECLINED|EXPIRED`; consent phải active và đúng scope.
- Chỉ mục: `(tenant_id,status,sent_at DESC)`; `(candidate_id,sent_at DESC)`.

#### TBL-WRK-030 — `data_consent_grants`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `candidate_id uuid NOT NULL` FK `candidate_profiles.id`; `grantee_type varchar(24) NOT NULL`; `grantee_tenant_id uuid NOT NULL`; `scope varchar(40)[] NOT NULL`; `purpose varchar(500) NOT NULL`; `valid_from timestamptz NOT NULL`; `valid_until timestamptz NOT NULL`; `policy_version integer NOT NULL`; `granted_at timestamptz NOT NULL`; `withdrawn_at timestamptz NULL`; `withdrawal_reason varchar(500) NULL`.
- Ràng buộc: grantee `UNIVERSITY|ENTERPRISE`; scope allowlist và không rỗng; valid_until>valid_from; withdrawal một chiều. Không FK đa hình; service kiểm đúng tenant table.
- Chỉ mục: `(candidate_id,grantee_type,grantee_tenant_id,withdrawn_at,valid_until)`; giữ 24 tháng.

#### TBL-WRK-031 — `university_report_runs`

- Tập cột: `TENANT_ENTITY` với `tenant_id` FK `university_tenants.id`.
- Cột riêng: `report_code varchar(80) NOT NULL`; `filters jsonb NOT NULL`; `period_start date NOT NULL`; `period_end date NOT NULL`; `status varchar(20) NOT NULL DEFAULT 'QUEUED'`; `requested_by_subject_id uuid NOT NULL`; `result_metrics jsonb NULL`; `group_size_min integer NOT NULL DEFAULT 10`; `source_high_watermark timestamptz NULL`; `completed_at timestamptz NULL`; `expires_at timestamptz NOT NULL`.
- Ràng buộc: group_size_min>=10; status `QUEUED|RUNNING|READY|FAILED|EXPIRED`; result tuyệt đối không chứa nhóm <10 hoặc row-level PII.
- Chỉ mục: `(tenant_id,status,created_at DESC)`; retention 13 tháng.

### 6.5 Job bất biến, moderation và sourcing

#### TBL-WRK-032 — `jobs`

- Tập cột: `TENANT_ENTITY` với `tenant_id` FK `enterprise_tenants.id`.
- Cột riêng: `slug varchar(160) NOT NULL`; `status job_status NOT NULL DEFAULT 'DRAFT'`; `current_draft_revision_id uuid NULL`; `published_revision_id uuid NULL`; `created_by_subject_id uuid NOT NULL`; `published_at timestamptz NULL`; `paused_at timestamptz NULL`; `closed_at timestamptz NULL`; `expires_at timestamptz NULL`; `taken_down_at timestamptz NULL`; `terminal_reason_code varchar(80) NULL`.
- Ràng buộc: unique `(tenant_id,slug)`; lifecycle transition canonical; timestamps phù hợp; terminal không trở lại published.
- Chỉ mục: `(tenant_id,status,updated_at DESC)`; `(status,published_at DESC)`; `(expires_at)` partial published/paused.

#### TBL-WRK-033 — `job_revisions`

- Tập cột: `ENTITY`; chỉ sửa bằng `row_version` khi DRAFT, bất biến từ lúc submit/publish.
- Cột riêng: `tenant_id uuid NOT NULL`; `job_id uuid NOT NULL`; `revision_no integer NOT NULL`; `status job_revision_status NOT NULL DEFAULT 'DRAFT'`; `title varchar(200) NOT NULL`; `description_markdown text NOT NULL`; `requirements_markdown text NOT NULL`; `benefits_markdown text NULL`; `employment_type varchar(24) NOT NULL`; `work_mode varchar(16) NOT NULL`; `location_codes varchar(20)[] NOT NULL`; `salary_min_vnd bigint NULL`; `salary_max_vnd bigint NULL`; `salary_visible boolean NOT NULL DEFAULT false`; `headcount integer NOT NULL DEFAULT 1`; `application_deadline timestamptz NULL`; `content_hash char(64) NOT NULL`; `created_by_subject_id uuid NOT NULL`; `submitted_at timestamptz NULL`; `approved_at timestamptz NULL`; `published_at timestamptz NULL`; `superseded_at timestamptz NULL`; `discarded_at timestamptz NULL`; `source_revision_id uuid NULL` self-FK.
- Ràng buộc: composite FK `(tenant_id,job_id)` -> jobs; unique `(job_id,revision_no)`; salary min/max hợp lệ; headcount 1–10000; HTML sanitize; published revision immutable.
- Chỉ mục: `(tenant_id,job_id,revision_no DESC)`; GIN full-text title/description/requirements; GIN locations; `(status,submitted_at)`.

#### TBL-WRK-034 — `job_skill_requirements`

- Tập cột: `ENTITY`; chỉ sửa khi job revision cha còn DRAFT, bất biến sau submit.
- Cột riêng: `tenant_id uuid NOT NULL`; `job_revision_id uuid NOT NULL` FK `job_revisions.id`; `skill_id uuid NOT NULL` FK `skills.id`; `required_level smallint NULL`; `min_years numeric(4,1) NULL`; `is_required boolean NOT NULL DEFAULT false`; `weight numeric(5,2) NOT NULL DEFAULT 1`.
- Ràng buộc: unique `(job_revision_id,skill_id)`; level 1–5; years 0–80; weight 0–100; tenant khớp revision.
- Chỉ mục: `(skill_id,job_revision_id)`; `(tenant_id,job_revision_id)`.

#### TBL-WRK-035 — `job_review_decisions`

- Tập cột: `APPEND`.
- Cột riêng: `tenant_id uuid NOT NULL`; `job_id uuid NOT NULL`; `job_revision_id uuid NOT NULL`; `reviewer_subject_id uuid NOT NULL`; `decision varchar(24) NOT NULL`; `reason_codes varchar(80)[] NOT NULL`; `comment varchar(2000) NULL`; `expected_job_version bigint NOT NULL`; `trace_id varchar(64) NOT NULL`.
- Ràng buộc: tenant/job/revision nhất quán; decision `APPROVE|REJECT|REQUEST_CHANGES|TAKE_DOWN`; reason khi không approve; two-reviewer race giải bằng optimistic lock.
- Chỉ mục: `(job_revision_id,occurred_at DESC)`; `(reviewer_subject_id,occurred_at DESC)`; 24 tháng.

#### TBL-WRK-036 — `job_status_history`

- Tập cột: `APPEND`.
- Cột riêng: `tenant_id uuid NOT NULL`; `job_id uuid NOT NULL`; `from_status job_status NULL`; `to_status job_status NOT NULL`; `actor_subject_id uuid NULL`; `reason_code varchar(80) NOT NULL`; `job_revision_id uuid NULL`; `trace_id varchar(64) NOT NULL`.
- Ràng buộc: transition thuộc state machine; tenant/job consistency.
- Chỉ mục: `(job_id,occurred_at,id)`; `(tenant_id,to_status,occurred_at DESC)`; 24 tháng.

#### TBL-WRK-037 — `candidate_search_documents`

- Tập cột: `ENTITY`.
- Cột riêng: `candidate_id uuid NOT NULL UNIQUE` FK `candidate_profiles.id`; `visibility candidate_visibility NOT NULL`; `search_vector tsvector NULL`; `skill_ids uuid[] NOT NULL DEFAULT '{}'`; `location_codes varchar(20)[] NOT NULL DEFAULT '{}'`; `experience_months integer NULL`; `headline_redacted varchar(200) NULL`; `source_version bigint NOT NULL`; `indexed_at timestamptz NULL`; `remove_by timestamptz NULL`; `removed_at timestamptz NULL`.
- Ràng buộc: không chứa contact, CV, Study evidence, exact school dates hoặc sensitive demographics; PRIVATE yêu cầu vector null sau removal; opt-out đặt `remove_by<=now()+5 minutes`.
- Chỉ mục: GIN search_vector; GIN skill/location arrays; `(visibility,indexed_at)`; `(remove_by)` partial chưa removed. Đây là projection rebuildable.

#### TBL-WRK-038 — `candidate_invitations`

- Tập cột: `TENANT_ENTITY` với `tenant_id` FK `enterprise_tenants.id`.
- Cột riêng: `job_id uuid NOT NULL`; `candidate_id uuid NOT NULL` FK `candidate_profiles.id`; `invited_by_subject_id uuid NOT NULL`; `message varchar(1000) NULL`; `status varchar(24) NOT NULL DEFAULT 'SENT'`; `sent_at timestamptz NOT NULL`; `viewed_at timestamptz NULL`; `responded_at timestamptz NULL`; `expires_at timestamptz NOT NULL`.
- Ràng buộc: unique `(tenant_id,job_id,candidate_id)`; status `SENT|VIEWED|ACCEPTED|DECLINED|EXPIRED`; invitation không tạo application/conversation.
- Chỉ mục: `(candidate_id,status,sent_at DESC)`; `(tenant_id,job_id,status)`.

#### TBL-WRK-039 — `talent_lists`

- Tập cột: `TENANT_ENTITY` với `tenant_id` FK `enterprise_tenants.id`.
- Cột riêng: `name varchar(160) NOT NULL`; `description varchar(1000) NULL`; `created_by_subject_id uuid NOT NULL`; `archived_at timestamptz NULL`.
- Ràng buộc: unique active `(tenant_id,name)`.
- Chỉ mục: `(tenant_id,archived_at,updated_at DESC)`.

#### TBL-WRK-040 — `talent_list_items`

- Tập cột: `TENANT_ENTITY` với `tenant_id` FK `enterprise_tenants.id`.
- Cột riêng: `list_id uuid NOT NULL`; `candidate_id uuid NOT NULL` FK `candidate_profiles.id`; `added_by_subject_id uuid NOT NULL`; `source varchar(24) NOT NULL`; `removed_at timestamptz NULL`.
- Ràng buộc: composite FK `(tenant_id,list_id)` -> talent list; active unique `(tenant_id,list_id,candidate_id)`; chỉ thêm candidate đang searchable hoặc đã có application trong tenant.
- Chỉ mục: `(tenant_id,list_id,removed_at,created_at DESC)`; opt-out làm ẩn search-derived item trong 5 phút.

### 6.6 Application, snapshot và ATS

#### TBL-WRK-041 — `applications`

- Tập cột: `TENANT_ENTITY` với `tenant_id` FK `enterprise_tenants.id`.
- Cột riêng: `candidate_id uuid NOT NULL` FK `candidate_profiles.id`; `job_id uuid NOT NULL`; `job_revision_id uuid NOT NULL`; `status application_status NOT NULL DEFAULT 'SUBMITTED'`; `submitted_at timestamptz NOT NULL`; `source varchar(24) NOT NULL`; `current_assignee_subject_id uuid NULL`; `last_status_at timestamptz NOT NULL`; `withdrawn_at timestamptz NULL`; `terminal_at timestamptz NULL`; `consent_policy_version integer NOT NULL`; `row_security_key uuid NOT NULL`.
- Ràng buộc: unique `(candidate_id,job_id)`; tenant/job/revision consistency; revision phải là published snapshot lúc apply; state transition canonical; terminal timestamps đúng.
- Chỉ mục: `(candidate_id,submitted_at DESC)`; `(tenant_id,job_id,status,submitted_at DESC)`; `(tenant_id,current_assignee_subject_id,status)`.
- Concurrency: transaction apply dùng unique constraint làm arbiter; không check-then-insert ngoài transaction.

#### TBL-WRK-042 — `application_snapshots`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `tenant_id uuid NOT NULL`; `application_id uuid NOT NULL UNIQUE`; `candidate_profile_snapshot jsonb NOT NULL`; `cv_version_id uuid NOT NULL`; `cv_snapshot jsonb NOT NULL`; `portfolio_snapshot jsonb NOT NULL DEFAULT '[]'`; `cover_letter_snapshot text NULL`; `screening_answers_snapshot jsonb NOT NULL DEFAULT '[]'`; `job_revision_id uuid NOT NULL`; `job_snapshot jsonb NOT NULL`; `schema_version integer NOT NULL`; `snapshot_hash char(64) NOT NULL`; `captured_at timestamptz NOT NULL`.
- Ràng buộc: tenant/application consistency; snapshots schema-validated, immutable, chỉ dữ liệu candidate đã xác nhận; CV/job/evidence không đọc live khi đánh giá application.
- Chỉ mục: `(tenant_id,application_id)`; retention 12 tháng sau terminal, legal hold có thể kéo dài.

#### TBL-WRK-043 — `application_evidence_selections`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `tenant_id uuid NOT NULL`; `application_id uuid NOT NULL`; `study_evidence_id uuid NOT NULL`; `selected_by_subject_id uuid NOT NULL`; `consent_id uuid NOT NULL`; `consent_policy_version integer NOT NULL`; `selected_at timestamptz NOT NULL`.
- Ràng buộc: unique `(application_id,study_evidence_id)`; candidate phải là chủ application; selected IDs do learner chọn rõ; Work không có evidence global.
- Chỉ mục: `(application_id,selected_at)`; giữ audit 24 tháng, nội dung snapshot theo retention application.

#### TBL-WRK-044 — `evidence_export_requests`

- Tập cột: `ENTITY`.
- Cột riêng: `tenant_id uuid NOT NULL`; `application_id uuid NOT NULL`; `request_id uuid NOT NULL UNIQUE`; `selected_evidence_ids uuid[] NOT NULL`; `consent_id uuid NOT NULL`; `status evidence_export_status NOT NULL DEFAULT 'PENDING'`; `attempt_count integer NOT NULL DEFAULT 0`; `next_retry_at timestamptz NULL`; `last_error_code varchar(80) NULL`; `sent_at timestamptz NULL`; `completed_at timestamptz NULL`; `request_payload_hash char(64) NOT NULL`.
- Ràng buộc: unique `(application_id,request_id)`; IDs không rỗng/trùng; attempt>=0; application transaction tạo selection, request và outbox cùng lúc; Study outage không rollback application.
- Chỉ mục: `(status,next_retry_at,id)` cho worker; `(application_id,created_at DESC)`.

#### TBL-WRK-045 — `application_evidence_snapshots`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `tenant_id uuid NOT NULL`; `application_id uuid NOT NULL`; `study_evidence_id uuid NOT NULL`; `request_id uuid NOT NULL`; `result_status evidence_export_status NOT NULL`; `evidence_type varchar(32) NULL`; `title varchar(200) NULL`; `description varchar(1000) NULL`; `issuer varchar(160) NULL`; `issued_at timestamptz NULL`; `source_version_id uuid NULL`; `claims_snapshot jsonb NULL`; `claims_hash char(64) NULL`; `signature_verification jsonb NULL`; `received_at timestamptz NULL`; `unavailable_reason_code varchar(80) NULL`.
- Ràng buộc: unique `(application_id,study_evidence_id)`; result chỉ `READY|UNAVAILABLE`; READY yêu cầu minimal snapshot/hash/verification; UNAVAILABLE không chứa giả định tiêu cực. Snapshot tuyệt đối không update khi consent/revocation đổi.
- Chỉ mục: `(application_id,result_status)`; `(study_evidence_id,result_status)`; retention 12 tháng post-terminal, audit metadata 24 tháng.

#### TBL-WRK-046 — `application_status_history`

- Tập cột: `APPEND`.
- Cột riêng: `tenant_id uuid NOT NULL`; `application_id uuid NOT NULL`; `from_status application_status NULL`; `to_status application_status NOT NULL`; `actor_subject_id uuid NOT NULL`; `reason_code varchar(80) NOT NULL`; `comment varchar(1000) NULL`; `expected_application_version bigint NOT NULL`; `source varchar(24) NOT NULL`; `trace_id varchar(64) NOT NULL`.
- Ràng buộc: transition canonical; application/tenant consistent; AI không được là actor/source đổi status.
- Chỉ mục: `(application_id,occurred_at,id)`; `(tenant_id,to_status,occurred_at DESC)`; append-only.

#### TBL-WRK-047 — `application_assignments`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `tenant_id uuid NOT NULL`; `application_id uuid NOT NULL`; `assignee_subject_id uuid NOT NULL`; `assigned_by_subject_id uuid NOT NULL`; `assigned_at timestamptz NOT NULL`; `unassigned_at timestamptz NULL`; `unassigned_by_subject_id uuid NULL`; `reason varchar(500) NULL`.
- Ràng buộc: active unique `(application_id,assignee_subject_id)`; assignee là active recruiter/hiring manager trong cùng tenant; unassign actor/time đồng tồn tại.
- Chỉ mục: `(tenant_id,assignee_subject_id,unassigned_at,assigned_at DESC)`.

#### TBL-WRK-048 — `application_notes`

- Tập cột: `TENANT_ENTITY` với `tenant_id` FK `enterprise_tenants.id`.
- Cột riêng: `application_id uuid NOT NULL`; `author_subject_id uuid NOT NULL`; `body text NOT NULL`; `visibility varchar(24) NOT NULL DEFAULT 'RECRUITING_TEAM'`; `edited_at timestamptz NULL`; `deleted_at timestamptz NULL`; `content_hash char(64) NOT NULL`.
- Ràng buộc: visibility `PRIVATE_AUTHOR|RECRUITING_TEAM`; author active membership; edit/delete giữ audit before/after; cấm thuộc tính bảo vệ/nhạy cảm theo policy.
- Chỉ mục: `(tenant_id,application_id,created_at DESC)`; DERIVED_SENSITIVE; 12 tháng post-terminal hoặc legal hold.

### 6.7 Interview và lịch nội bộ

#### TBL-WRK-049 — `interviews`

- Tập cột: `TENANT_ENTITY` với `tenant_id` FK `enterprise_tenants.id`.
- Cột riêng: `application_id uuid NOT NULL`; `status interview_status NOT NULL DEFAULT 'PROPOSED'`; `current_schedule_version integer NOT NULL DEFAULT 1`; `title varchar(200) NOT NULL`; `interview_type varchar(24) NOT NULL`; `location_text varchar(500) NULL`; `meeting_url varchar(2048) NULL`; `timezone varchar(64) NOT NULL`; `created_by_subject_id uuid NOT NULL`; `cancelled_at timestamptz NULL`; `completed_at timestamptz NULL`; `no_show_party varchar(16) NULL`.
- Ràng buộc: application/tenant consistent; type `PHONE|VIDEO|ONSITE`; meeting URL HTTPS chỉ cho VIDEO; status timestamps tương ứng; không tích hợp Google/Microsoft OAuth trong V1.
- Chỉ mục: `(tenant_id,application_id,created_at DESC)`; `(tenant_id,status,updated_at)`.

#### TBL-WRK-050 — `interview_schedule_versions`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `tenant_id uuid NOT NULL`; `interview_id uuid NOT NULL`; `version_no integer NOT NULL`; `starts_at timestamptz NOT NULL`; `ends_at timestamptz NOT NULL`; `timezone varchar(64) NOT NULL`; `proposed_by_subject_id uuid NOT NULL`; `change_reason varchar(1000) NULL`; `supersedes_version_id uuid NULL` self-FK; `created_ics_sequence integer NOT NULL`; `content_hash char(64) NOT NULL`.
- Ràng buộc: unique `(interview_id,version_no)`; end>start; tenant consistent; reschedule tạo version mới, không sửa phiên bản cũ.
- Chỉ mục: `(interview_id,version_no DESC)`; `(tenant_id,starts_at,ends_at)`.

#### TBL-WRK-051 — `interview_participants`

- Tập cột: `TENANT_ENTITY` với `tenant_id` FK `enterprise_tenants.id`.
- Cột riêng: `interview_id uuid NOT NULL`; `identity_subject_id uuid NOT NULL`; `participant_role varchar(24) NOT NULL`; `response varchar(24) NOT NULL DEFAULT 'PENDING'`; `responded_at timestamptz NULL`; `last_notified_schedule_version integer NOT NULL DEFAULT 0`.
- Ràng buộc: unique `(interview_id,identity_subject_id)`; role `CANDIDATE|INTERVIEWER|ORGANIZER`; response `PENDING|ACCEPTED|DECLINED|TENTATIVE`; candidate phải là application owner, staff là active membership.
- Chỉ mục: `(identity_subject_id,response,updated_at DESC)`; `(tenant_id,interview_id)`.

#### TBL-WRK-052 — `interview_status_history`

- Tập cột: `APPEND`.
- Cột riêng: `tenant_id uuid NOT NULL`; `interview_id uuid NOT NULL`; `from_status interview_status NULL`; `to_status interview_status NOT NULL`; `schedule_version integer NOT NULL`; `actor_subject_id uuid NOT NULL`; `reason_code varchar(80) NOT NULL`; `trace_id varchar(64) NOT NULL`.
- Ràng buộc: transition canonical và tenant consistent; complete/no-show/cancel là terminal.
- Chỉ mục: `(interview_id,occurred_at,id)`; 24 tháng.

### 6.8 Chat application-scoped

#### TBL-WRK-053 — `conversations`

- Tập cột: `TENANT_ENTITY` với `tenant_id` FK `enterprise_tenants.id`.
- Cột riêng: `application_id uuid NOT NULL UNIQUE`; `status conversation_status NOT NULL DEFAULT 'ACTIVE'`; `candidate_subject_id uuid NOT NULL`; `recruiter_subject_id uuid NOT NULL`; `opened_at timestamptz NOT NULL`; `read_only_at timestamptz NULL`; `last_message_at timestamptz NULL`; `last_message_id uuid NULL`.
- Ràng buộc: đúng một conversation mỗi application; chỉ tạo sau application; recruiter phải được assign và active tenant member; terminal application chuyển READ_ONLY transactionally/eventually idempotent.
- Chỉ mục: `(candidate_subject_id,last_message_at DESC)`; `(tenant_id,recruiter_subject_id,last_message_at DESC)`; `(application_id)`.

#### TBL-WRK-054 — `messages`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `tenant_id uuid NOT NULL`; `conversation_id uuid NOT NULL`; `sender_subject_id uuid NULL`; `client_message_id uuid NOT NULL`; `message_type varchar(16) NOT NULL DEFAULT 'TEXT'`; `body text NOT NULL`; `sent_at timestamptz NOT NULL`; `server_sequence bigint NOT NULL`; `deleted_for_all_at timestamptz NULL`; `moderation_status varchar(24) NOT NULL DEFAULT 'CLEAR'`; `content_hash char(64) NOT NULL`.
- Ràng buộc: unique `(conversation_id,client_message_id)` và `(conversation_id,server_sequence)`; type chỉ `TEXT|SYSTEM`; text 1–5000 ký tự sau trim và không chứa HTML thực thi; TEXT yêu cầu sender là participant, SYSTEM yêu cầu sender null và chỉ worker có quyền insert; conversation ACTIVE; delete text chỉ trong 15 phút và vẫn lưu audit/hash/sequence. V1 không có attachment chat.
- Chỉ mục: `(conversation_id,server_sequence DESC)` cho cursor REST; `(sender_subject_id,sent_at DESC)`; 12 tháng post-terminal.

#### TBL-WRK-055 — `conversation_read_cursors`

- Tập cột: `ENTITY`.
- Cột riêng: `tenant_id uuid NOT NULL`; `conversation_id uuid NOT NULL`; `identity_subject_id uuid NOT NULL`; `last_read_sequence bigint NOT NULL DEFAULT 0`; `last_read_at timestamptz NULL`.
- Ràng buộc: unique `(conversation_id,identity_subject_id)`; cursor chỉ tăng; subject là participant.
- Chỉ mục: `(identity_subject_id,updated_at DESC)`.

#### TBL-WRK-056 — `websocket_connection_leases`

- Tập cột: `ENTITY`.
- Cột riêng: `identity_subject_id uuid NOT NULL`; `connection_id uuid NOT NULL UNIQUE`; `node_id varchar(120) NOT NULL`; `connected_at timestamptz NOT NULL`; `last_heartbeat_at timestamptz NOT NULL`; `expires_at timestamptz NOT NULL`; `revoked_at timestamptz NULL`.
- Ràng buộc: expiry>heartbeat; lease ephemeral, PostgreSQL là fallback registry còn Redis là runtime fanout.
- Chỉ mục: `(identity_subject_id,expires_at)`; `(expires_at)`; purge trong 24 giờ.

### 6.9 AI và matching có người duyệt

#### TBL-AIX-001 — `ai_model_versions`

- Tập cột: `ENTITY`.
- Cột riêng: `provider varchar(40) NOT NULL`; `model_key varchar(160) NOT NULL`; `version varchar(120) NOT NULL`; `capability varchar(40) NOT NULL`; `endpoint_config_ref varchar(300) NOT NULL`; `data_residency varchar(80) NOT NULL`; `enabled boolean NOT NULL DEFAULT false`; `activated_at timestamptz NULL`; `retired_at timestamptz NULL`; `risk_class varchar(24) NOT NULL`.
- Ràng buộc: unique `(provider,model_key,version,capability)`; default pilot provider `OLLAMA`; config chỉ là secret-manager reference.
- Chỉ mục: `(capability,enabled,activated_at DESC)`; INTERNAL.

#### TBL-AIX-002 — `ai_prompt_versions`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `prompt_code varchar(80) NOT NULL`; `version_no integer NOT NULL`; `capability varchar(40) NOT NULL`; `system_prompt text NOT NULL`; `input_schema jsonb NOT NULL`; `output_schema jsonb NOT NULL`; `excluded_fields varchar(120)[] NOT NULL`; `injection_policy_version integer NOT NULL`; `created_by_subject_id uuid NOT NULL`; `approved_by_subject_id uuid NOT NULL`; `activated_at timestamptz NULL`; `retired_at timestamptz NULL`; `content_hash char(64) NOT NULL`.
- Ràng buộc: unique `(prompt_code,version_no)`; maker-checker; excluded fields tối thiểu chứa protected/sensitive attributes theo capability.
- Chỉ mục: `(prompt_code,activated_at DESC)`; không sửa prompt đã dùng.

#### TBL-AIX-003 — `ai_policy_versions`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `policy_code varchar(80) NOT NULL`; `version_no integer NOT NULL`; `capability varchar(40) NOT NULL`; `rules jsonb NOT NULL`; `allowed_input_fields varchar(120)[] NOT NULL`; `forbidden_actions varchar(120)[] NOT NULL`; `approved_by_subject_id uuid NOT NULL`; `activated_at timestamptz NOT NULL`; `retired_at timestamptz NULL`; `content_hash char(64) NOT NULL`.
- Ràng buộc: unique `(policy_code,version_no)`; forbidden actions luôn gồm ATS status mutation, reject và hire tự động.
- Chỉ mục: `(capability,activated_at DESC)`.

#### TBL-AIX-004 — `ai_jobs`

- Tập cột: `ENTITY`.
- Cột riêng: `tenant_id uuid NULL`; `actor_subject_id uuid NOT NULL`; `capability varchar(40) NOT NULL`; `resource_type varchar(40) NOT NULL`; `resource_id uuid NOT NULL`; `model_version_id uuid NOT NULL` FK `ai_model_versions.id`; `prompt_version_id uuid NOT NULL` FK `ai_prompt_versions.id`; `policy_version_id uuid NOT NULL` FK `ai_policy_versions.id`; `status ai_job_status NOT NULL DEFAULT 'QUEUED'`; `input_snapshot_redacted jsonb NOT NULL`; `input_hash char(64) NOT NULL`; `queued_at timestamptz NOT NULL`; `started_at timestamptz NULL`; `completed_at timestamptz NULL`; `attempt_count integer NOT NULL DEFAULT 0`; `last_error_code varchar(80) NULL`; `kill_switch_snapshot boolean NOT NULL`; `trace_id varchar(64) NOT NULL`.
- Ràng buộc: capability `CV_DRAFT|JD_DRAFT|MATCH_EXPLANATION|SHORTLIST_SUGGESTION`; attempt>=0; input schema/policy validate; job async; source text được bọc untrusted delimiter chống prompt injection.
- Chỉ mục: `(status,created_at,id)` worker; `(actor_subject_id,created_at DESC)`; `(tenant_id,resource_type,resource_id,created_at DESC)`.
- Retention: input/output 12 tháng hoặc ngắn hơn theo consent; audit metadata 24 tháng.

#### TBL-AIX-005 — `ai_outputs`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `ai_job_id uuid NOT NULL UNIQUE` FK `ai_jobs.id`; `output_json jsonb NOT NULL`; `output_text text NULL`; `output_hash char(64) NOT NULL`; `safety_flags varchar(80)[] NOT NULL DEFAULT '{}'`; `provider_request_id varchar(160) NULL`; `latency_ms integer NOT NULL`; `token_usage jsonb NULL`; `generated_at timestamptz NOT NULL`.
- Ràng buộc: output schema validate; latency>=0; không chứa excluded fields; provider request ID không chứa secret.
- Chỉ mục: `(generated_at)`; DERIVED_SENSITIVE.

#### TBL-AIX-006 — `ai_human_reviews`

- Tập cột: `APPEND`.
- Cột riêng: `ai_job_id uuid NOT NULL` FK `ai_jobs.id`; `output_id uuid NOT NULL` FK `ai_outputs.id`; `reviewer_subject_id uuid NOT NULL`; `decision ai_review_decision NOT NULL`; `edited_output_snapshot jsonb NULL`; `reason_codes varchar(80)[] NOT NULL DEFAULT '{}'`; `comment varchar(2000) NULL`; `applied_to_resource_at timestamptz NULL`; `trace_id varchar(64) NOT NULL`.
- Ràng buộc: `EDITED_ACCEPT` cần snapshot; `REJECTED` cần reason; apply chỉ sau explicit human action; trạng thái review output được suy ra từ review cuối (`DRAFT` nếu chưa review, `EXPIRED` nếu quá hạn) và không trộn với `ai_job_status`; một output có thể review lại nhưng chỉ một accepted/applied final bằng transaction.
- Chỉ mục: `(ai_job_id,occurred_at DESC)`; `(reviewer_subject_id,occurred_at DESC)`; append-only 24 tháng.

#### TBL-AIX-007 — `match_score_snapshots`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `tenant_id uuid NOT NULL`; `job_revision_id uuid NOT NULL`; `candidate_id uuid NOT NULL` FK `candidate_profiles.id`; `application_id uuid NULL`; `algorithm_version varchar(80) NOT NULL`; `feature_policy_version integer NOT NULL`; `allowed_feature_snapshot jsonb NOT NULL`; `score numeric(5,2) NOT NULL`; `explanation jsonb NOT NULL`; `ai_job_id uuid NULL` FK `ai_jobs.id`; `calculated_at timestamptz NOT NULL`; `expires_at timestamptz NOT NULL`.
- Ràng buộc: score 0–100; feature snapshot không chứa protected attributes, Study evidence, sponsored status hoặc contact; score chỉ gợi ý, không đổi ATS.
- Chỉ mục: `(tenant_id,job_revision_id,score DESC)`; `(application_id,calculated_at DESC)`; DERIVED_SENSITIVE.

#### TBL-AIX-008 — `ai_kill_switches`

- Tập cột: `ENTITY`.
- Cột riêng: `capability varchar(40) NOT NULL UNIQUE`; `disabled boolean NOT NULL DEFAULT false`; `reason varchar(1000) NULL`; `changed_by_subject_id uuid NOT NULL`; `changed_at timestamptz NOT NULL`; `expires_at timestamptz NULL`.
- Ràng buộc: disabled cần reason; mọi thay đổi audit; worker kiểm trước và sau provider call.
- Chỉ mục: `(disabled,capability)`.

### 6.10 Billing, payment, entitlement và promotion

#### TBL-PAY-001 — `products`

- Tập cột: `ENTITY`.
- Cột riêng: `code varchar(80) NOT NULL UNIQUE`; `buyer_type varchar(20) NOT NULL`; `name varchar(200) NOT NULL`; `description varchar(2000) NOT NULL`; `product_type varchar(32) NOT NULL`; `entitlement_code varchar(80) NOT NULL`; `credit_amount bigint NULL`; `validity_days integer NOT NULL`; `active_from timestamptz NOT NULL`; `active_until timestamptz NULL`.
- Ràng buộc: buyer `CANDIDATE|ENTERPRISE`; type `PACKAGE|CREDIT_PACK|PREMIUM_TEMPLATE|SPONSORED_PLACEMENT`; credit>=0; validity 1–3650; no auto-renew.
- Chỉ mục: `(buyer_type,active_from,active_until)`; PUBLIC catalog phần được publish.

#### TBL-PAY-002 — `product_prices`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `product_id uuid NOT NULL` FK `products.id`; `version_no integer NOT NULL`; `currency char(3) NOT NULL DEFAULT 'VND'`; `amount_vnd bigint NOT NULL`; `tax_rate numeric(5,2) NOT NULL DEFAULT 0`; `valid_from timestamptz NOT NULL`; `valid_until timestamptz NULL`; `created_by_subject_id uuid NOT NULL`.
- Ràng buộc: unique `(product_id,version_no)`; amount>0; currency VND; tax 0–100; non-overlap effective periods.
- Chỉ mục: `(product_id,valid_from DESC)`.

#### TBL-PAY-003 — `orders`

- Tập cột: `ENTITY`.
- Cột riêng: `order_no varchar(40) NOT NULL UNIQUE`; `buyer_subject_id uuid NOT NULL`; `buyer_type varchar(20) NOT NULL`; `tenant_id uuid NULL`; `status order_status NOT NULL DEFAULT 'CREATED'`; `currency char(3) NOT NULL DEFAULT 'VND'`; `subtotal_vnd bigint NOT NULL`; `tax_vnd bigint NOT NULL`; `total_vnd bigint NOT NULL`; `pricing_snapshot jsonb NOT NULL`; `created_at_client timestamptz NULL`; `expires_at timestamptz NOT NULL`; `settled_at timestamptz NULL`; `failed_at timestamptz NULL`; `cancelled_at timestamptz NULL`; `idempotency_key_hash char(64) NOT NULL`.
- Ràng buộc: unique `(buyer_subject_id,idempotency_key_hash)`; amounts>=0, total=subtotal+tax; enterprise buyer yêu cầu tenant; không auto-renew/wallet/escrow/payout.
- Chỉ mục: `(buyer_subject_id,created_at DESC)`; `(tenant_id,status,created_at DESC)`; `(status,expires_at)`.

#### TBL-PAY-004 — `order_items`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `order_id uuid NOT NULL` FK `orders.id`; `product_id uuid NOT NULL` FK `products.id`; `price_version_id uuid NOT NULL` FK `product_prices.id`; `quantity integer NOT NULL`; `unit_amount_vnd bigint NOT NULL`; `tax_vnd bigint NOT NULL`; `line_total_vnd bigint NOT NULL`; `product_snapshot jsonb NOT NULL`.
- Ràng buộc: unique `(order_id,product_id,price_version_id)`; quantity 1–10000; line math chính xác; price/product snapshot bất biến.
- Chỉ mục: `(order_id)`.

#### TBL-PAY-005 — `payment_attempts`

- Tập cột: `ENTITY`.
- Cột riêng: `order_id uuid NOT NULL` FK `orders.id`; `attempt_no integer NOT NULL`; `provider payment_provider NOT NULL`; `status payment_status NOT NULL DEFAULT 'CREATED'`; `amount_vnd bigint NOT NULL`; `provider_order_id varchar(160) NOT NULL`; `provider_transaction_id varchar(160) NULL`; `request_payload_hash char(64) NOT NULL`; `response_code varchar(80) NULL`; `checkout_url_ciphertext bytea NULL`; `return_seen_at timestamptz NULL`; `settled_at timestamptz NULL`; `failed_at timestamptz NULL`; `expires_at timestamptz NOT NULL`; `last_provider_occurred_at timestamptz NULL`.
- Ràng buộc: unique `(order_id,attempt_no)`; unique `(provider,provider_order_id)`; partial unique `(provider,provider_transaction_id)` khi có; amount bằng order total; return URL không settle payment.
- Chỉ mục: `(order_id,attempt_no DESC)`; `(provider,status,updated_at)`; `(status,expires_at)`.

#### TBL-PAY-006 — `payment_webhook_events`

- Tập cột: `APPEND`.
- Cột riêng: `provider payment_provider NOT NULL`; `provider_event_id varchar(200) NOT NULL`; `provider_order_id varchar(160) NOT NULL`; `provider_transaction_id varchar(160) NULL`; `provider_occurred_at timestamptz NULL`; `received_at timestamptz NOT NULL`; `signature_valid boolean NOT NULL`; `source_ip_hash char(64) NULL`; `headers_redacted jsonb NOT NULL`; `payload_ciphertext bytea NOT NULL`; `payload_hash char(64) NOT NULL`; `processing_status varchar(24) NOT NULL DEFAULT 'RECEIVED'`; `processed_at timestamptz NULL`; `result_code varchar(80) NULL`; `trace_id varchar(64) NOT NULL`.
- Ràng buộc: unique `(provider,provider_event_id)`; fallback dedupe unique `(provider,payload_hash)`; invalid signature chỉ audit, không mutate; out-of-order so với `last_provider_occurred_at` và state precedence.
- Chỉ mục: `(processing_status,received_at,id)`; `(provider,provider_order_id,received_at DESC)`; append-only 24 tháng hoặc lâu hơn theo finance policy.

#### TBL-PAY-007 — `payment_reconciliations`

- Tập cột: `APPEND`.
- Cột riêng: `provider payment_provider NOT NULL`; `payment_attempt_id uuid NULL` FK `payment_attempts.id`; `reconciliation_date date NOT NULL`; `provider_status varchar(80) NOT NULL`; `local_status payment_status NULL`; `amount_vnd bigint NOT NULL`; `matched boolean NOT NULL`; `discrepancy_code varchar(80) NULL`; `provider_payload_hash char(64) NOT NULL`; `resolved_at timestamptz NULL`; `resolved_by_subject_id uuid NULL`; `resolution_note varchar(1000) NULL`.
- Ràng buộc: amount>=0; unmatched yêu cầu discrepancy; resolution actor/note đồng tồn tại.
- Chỉ mục: `(provider,reconciliation_date,matched)`; `(payment_attempt_id,occurred_at DESC)`; 24 tháng+.

#### TBL-PAY-008 — `refunds`

- Tập cột: `ENTITY`.
- Cột riêng: `order_id uuid NOT NULL` FK `orders.id`; `payment_attempt_id uuid NOT NULL` FK `payment_attempts.id`; `refund_no varchar(60) NOT NULL UNIQUE`; `amount_vnd bigint NOT NULL`; `reason_code varchar(80) NOT NULL`; `reason_text varchar(1000) NULL`; `status varchar(24) NOT NULL DEFAULT 'REQUESTED'`; `requested_by_subject_id uuid NOT NULL`; `approved_by_subject_id uuid NULL`; `provider_refund_id varchar(160) NULL`; `requested_at timestamptz NOT NULL`; `processed_at timestamptz NULL`; `failed_at timestamptz NULL`.
- Ràng buộc: amount>0 và tổng settled refund <= payment; status `REQUESTED|APPROVED|PROCESSING|SETTLED|FAILED|REJECTED`; maker-checker; unique provider refund khi có.
- Chỉ mục: `(order_id,created_at DESC)`; `(status,created_at)`; 24 tháng+.

#### TBL-PAY-009 — `chargebacks`

- Tập cột: `APPEND`.
- Cột riêng: `payment_attempt_id uuid NOT NULL` FK `payment_attempts.id`; `provider_case_id varchar(160) NOT NULL`; `amount_vnd bigint NOT NULL`; `reason_code varchar(80) NOT NULL`; `status varchar(24) NOT NULL`; `opened_at timestamptz NOT NULL`; `resolved_at timestamptz NULL`; `resolution varchar(80) NULL`; `provider_payload_hash char(64) NOT NULL`.
- Ràng buộc: unique `(payment_attempt_id,provider_case_id)`; amount>0; status `OPEN|WON|LOST|CLOSED`; chargeback tạo reversal/entitlement revoke idempotent.
- Chỉ mục: `(status,opened_at)`; 24 tháng+.

#### TBL-PAY-010 — `entitlements`

- Tập cột: `ENTITY`.
- Cột riêng: `owner_subject_id uuid NOT NULL`; `owner_type varchar(20) NOT NULL`; `tenant_id uuid NULL`; `order_item_id uuid NOT NULL` FK `order_items.id`; `code varchar(80) NOT NULL`; `status entitlement_status NOT NULL DEFAULT 'ACTIVE'`; `quantity_total bigint NOT NULL`; `quantity_consumed bigint NOT NULL DEFAULT 0`; `valid_from timestamptz NOT NULL`; `valid_until timestamptz NULL`; `activated_at timestamptz NOT NULL`; `frozen_at timestamptz NULL`; `revoked_at timestamptz NULL`; `revoke_reason varchar(500) NULL`.
- Ràng buộc: unique `(order_item_id,code)`; 0<=consumed<=total; row chỉ được tạo trong settlement transaction đã xác thực, không tồn tại entitlement PENDING; `ACTIVE→EXHAUSTED|EXPIRED|FROZEN|REVOKED`, `FROZEN→ACTIVE|REVOKED`; enterprise owner yêu cầu tenant; validity hợp lệ.
- Chỉ mục: `(owner_subject_id,code,status,valid_until)`; `(tenant_id,code,status,valid_until)`.

#### TBL-PAY-011 — `credit_ledger_entries`

- Tập cột: `APPEND`.
- Cột riêng: `entitlement_id uuid NOT NULL` FK `entitlements.id`; `owner_subject_id uuid NOT NULL`; `tenant_id uuid NULL`; `entry_type ledger_entry_type NOT NULL`; `quantity_delta bigint NOT NULL`; `balance_after bigint NOT NULL`; `reference_type varchar(40) NOT NULL`; `reference_id uuid NOT NULL`; `idempotency_key varchar(180) NOT NULL`; `actor_subject_id uuid NULL`; `reason varchar(500) NULL`.
- Ràng buộc: unique `(entitlement_id,idempotency_key)`; delta khác 0; balance>=0; entry sign phù hợp type; balance được serialize bằng row lock entitlement.
- Chỉ mục: `(entitlement_id,occurred_at,id)`; `(tenant_id,occurred_at DESC)`; append-only 24 tháng+.

#### TBL-PAY-012 — `promotion_campaigns`

- Tập cột: `ENTITY`.
- Cột riêng: `code varchar(80) NOT NULL UNIQUE`; `name varchar(200) NOT NULL`; `promotion_type varchar(32) NOT NULL`; `sponsor_subject_id uuid NOT NULL`; `sponsor_tenant_id uuid NULL`; `status promotion_status NOT NULL DEFAULT 'SCHEDULED'`; `starts_at timestamptz NOT NULL`; `ends_at timestamptz NOT NULL`; `budget_vnd bigint NULL`; `label_text varchar(120) NOT NULL DEFAULT 'Được tài trợ'`; `targeting_rules jsonb NOT NULL`; `created_by_subject_id uuid NOT NULL`; `approved_by_subject_id uuid NOT NULL`.
- Ràng buộc: type `SPONSORED_PROFILE|SPONSORED_JOB`; end>start; budget>=0; label không rỗng; maker-checker; promotion không tác động organic/match/ATS.
- Chỉ mục: `(status,starts_at,ends_at)`; `(sponsor_tenant_id,status)`.

#### TBL-PAY-013 — `sponsored_placements`

- Tập cột: `ENTITY`.
- Cột riêng: `campaign_id uuid NOT NULL` FK `promotion_campaigns.id`; `resource_type varchar(24) NOT NULL`; `resource_id uuid NOT NULL`; `entitlement_id uuid NOT NULL` FK `entitlements.id`; `starts_at timestamptz NOT NULL`; `ends_at timestamptz NOT NULL`; `status promotion_status NOT NULL`; `label_text varchar(120) NOT NULL`; `targeting_snapshot jsonb NOT NULL`; `impression_count bigint NOT NULL DEFAULT 0`; `click_count bigint NOT NULL DEFAULT 0`.
- Ràng buộc: resource `CANDIDATE_PROFILE|JOB`; time within campaign; label required; searchable candidate opt-in/job published; sponsored rank stored riêng và không ghi vào match score.
- Chỉ mục: `(resource_type,status,starts_at,ends_at)`; `(campaign_id,status)`.

#### TBL-PAY-014 — `invoices`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `order_id uuid NOT NULL UNIQUE` FK `orders.id`; `invoice_no varchar(60) NOT NULL UNIQUE`; `buyer_snapshot jsonb NOT NULL`; `tax_snapshot jsonb NOT NULL`; `amount_vnd bigint NOT NULL`; `issued_at timestamptz NOT NULL`; `file_id uuid NOT NULL` FK `file_objects.id`; `content_hash char(64) NOT NULL`; `voided_at timestamptz NULL`; `void_reason varchar(500) NULL`; `replacement_invoice_id uuid NULL` self-FK.
- Ràng buộc: file CLEAN, amount bằng số tiền SETTLED; correction tạo replacement, không sửa invoice.
- Chỉ mục: `(issued_at DESC)`; finance retention theo luật, tối thiểu 24 tháng.

### 6.11 Notification, moderation và vận hành Work

#### TBL-WRK-057 — `notification_preferences`

- Tập cột: `ENTITY`.
- Cột riêng: `identity_subject_id uuid NOT NULL`; `category varchar(40) NOT NULL`; `in_app_enabled boolean NOT NULL DEFAULT true`; `email_enabled boolean NOT NULL DEFAULT true`; `quiet_hours_start time NULL`; `quiet_hours_end time NULL`; `timezone varchar(64) NOT NULL`; `consent_source varchar(40) NOT NULL`.
- Ràng buộc: unique `(identity_subject_id,category)`; transactional/security category không được tắt.
- Chỉ mục: `(identity_subject_id,category)`.

#### TBL-WRK-058 — `notifications`

- Tập cột: `ENTITY`.
- Cột riêng: `identity_subject_id uuid NOT NULL`; `tenant_id uuid NULL`; `category varchar(40) NOT NULL`; `template_code varchar(80) NOT NULL`; `template_version integer NOT NULL`; `title varchar(200) NOT NULL`; `body varchar(4000) NOT NULL`; `action_url varchar(1000) NULL`; `dedupe_key varchar(180) NOT NULL`; `read_at timestamptz NULL`; `expires_at timestamptz NOT NULL`; `payload jsonb NOT NULL DEFAULT '{}'`.
- Ràng buộc: unique `(identity_subject_id,dedupe_key)`; URL allowlist; payload redacted.
- Chỉ mục: `(identity_subject_id,read_at,created_at DESC,id DESC)` cursor; `(expires_at)`; retention 180 ngày.

#### TBL-WRK-059 — `notification_deliveries`

- Tập cột: `APPEND`.
- Cột riêng: `notification_id uuid NOT NULL` FK `notifications.id`; `channel varchar(16) NOT NULL`; `status notification_status NOT NULL`; `provider_message_id varchar(160) NULL`; `attempt_no integer NOT NULL`; `error_code varchar(80) NULL`; `next_retry_at timestamptz NULL`; `dedupe_key varchar(180) NOT NULL`.
- Ràng buộc: unique notification/channel/attempt và dedupe key; channel `IN_APP|EMAIL`; attempt>=1.
- Chỉ mục: `(status,next_retry_at)`; retention 180 ngày.

#### TBL-WRK-060 — `moderation_reports`

- Tập cột: `ENTITY`.
- Cột riêng: `reporter_subject_id uuid NOT NULL`; `tenant_id uuid NULL`; `resource_type varchar(40) NOT NULL`; `resource_id uuid NOT NULL`; `reason_code varchar(80) NOT NULL`; `description varchar(2000) NULL`; `evidence_file_ids uuid[] NOT NULL DEFAULT '{}'`; `status varchar(24) NOT NULL DEFAULT 'OPEN'`; `assigned_to_subject_id uuid NULL`; `decision varchar(80) NULL`; `resolved_at timestamptz NULL`.
- Ràng buộc: status `OPEN|IN_REVIEW|RESOLVED|DISMISSED`; terminal needs decision; files CLEAN.
- Chỉ mục: `(status,created_at)`; `(resource_type,resource_id,created_at DESC)`; 24 tháng.

#### TBL-WRK-061 — `audit_events`

- Tập cột: `APPEND`.
- Cột riêng: `actor_subject_id uuid NULL`; `action varchar(120) NOT NULL`; `resource_type varchar(80) NOT NULL`; `resource_id uuid NULL`; `outcome audit_outcome NOT NULL`; `business_code varchar(80) NOT NULL`; `trace_id varchar(64) NOT NULL`; `tenant_context jsonb NULL`; `changes jsonb NULL`; `metadata jsonb NOT NULL DEFAULT '{}'`; `prev_hash char(64) NULL`; `event_hash char(64) NOT NULL UNIQUE`; `legal_hold_until timestamptz NULL`.
- Ràng buộc: tenant context có tenant type/ID/membership; canonical chain hash; changes/metadata redacted; append-only.
- Chỉ mục: resource/time, actor/time, tenant/time, trace, BRIN occurred time; retention 24 tháng+.

#### TBL-WRK-062 — `idempotency_keys`

- Tập cột: `ENTITY`.
- Cột riêng: `actor_subject_id uuid NULL`; `operation varchar(120) NOT NULL`; `key_hash char(64) NOT NULL`; `request_hash char(64) NOT NULL`; `response_status integer NULL`; `response_body jsonb NULL`; `locked_until timestamptz NULL`; `completed_at timestamptz NULL`; `expires_at timestamptz NOT NULL`.
- Ràng buộc: unique actor/operation/key; same key khác request hash conflict; response redacted.
- Chỉ mục: `(expires_at)`; apply/payment/interview/chat giữ 7 ngày, mutation khác 24 giờ.

#### TBL-WRK-063 — `outbox_events`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `aggregate_type varchar(80) NOT NULL`; `aggregate_id uuid NOT NULL`; `event_type varchar(120) NOT NULL`; `event_version integer NOT NULL`; `payload jsonb NOT NULL`; `available_at timestamptz NOT NULL DEFAULT now()`; `dedupe_key varchar(180) NOT NULL UNIQUE`; `trace_id varchar(64) NOT NULL`.
- Ràng buộc: version>=1; event có schema/version/trace; payment settled và application created ghi cùng aggregate transaction; append-only.
- Chỉ mục: `(available_at,id)`; `(aggregate_type,aggregate_id,created_at)`; 24 tháng.

#### TBL-WRK-064 — `consumer_inbox`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `consumer varchar(100) NOT NULL`; `event_id uuid NOT NULL`; `event_type varchar(120) NOT NULL`; `payload_hash char(64) NOT NULL`; `received_at timestamptz NOT NULL DEFAULT now()`; `processed_at timestamptz NULL`; `result_code varchar(80) NULL`; `trace_id varchar(64) NOT NULL`.
- Ràng buộc: unique `(consumer,event_id)`; same event khác hash là security error; consumers gồm Identity, Study evidence và internal workers.
- Chỉ mục: `(consumer,processed_at,received_at)`; 24 tháng.

#### TBL-WRK-065 — `admin_adjustments`

- Tập cột: `APPEND`.
- Cột riêng: `tenant_id uuid NULL`; `target_type varchar(32) NOT NULL`; `target_id uuid NOT NULL`; `action varchar(80) NOT NULL`; `before_snapshot jsonb NOT NULL`; `after_snapshot jsonb NOT NULL`; `reason varchar(1000) NOT NULL`; `approved_by_subject_id uuid NOT NULL`; `performed_by_subject_id uuid NOT NULL`; `trace_id varchar(64) NOT NULL`.
- Ràng buộc: payment/credit adjustment bắt buộc maker-checker, hai actor khác nhau và reference ticket trong reason; snapshots redacted.
- Chỉ mục: `(target_type,target_id,occurred_at DESC)`; `(tenant_id,occurred_at DESC)`; append-only 24 tháng+.

#### TBL-WRK-066 — `tenant_roles`

- Tập cột: `ENTITY`.
- Cột riêng: `tenant_type varchar(20) NOT NULL`; `code varchar(40) NOT NULL`; `name varchar(120) NOT NULL`; `description varchar(500) NOT NULL`; `is_system boolean NOT NULL DEFAULT true`; `is_privileged boolean NOT NULL DEFAULT false`; `disabled_at timestamptz NULL`.
- Ràng buộc: unique `(tenant_type,code)`; tenant type `ENTERPRISE|UNIVERSITY`; code phải khớp role catalog của membership tương ứng.
- Chỉ mục: `(tenant_type,disabled_at,code)`.

#### TBL-WRK-067 — `tenant_permissions`

- Tập cột: `ENTITY`.
- Cột riêng: `code varchar(120) NOT NULL UNIQUE`; `tenant_type varchar(20) NOT NULL`; `description varchar(500) NOT NULL`; `risk_level smallint NOT NULL DEFAULT 1`; `disabled_at timestamptz NULL`.
- Ràng buộc: tenant type `ENTERPRISE|UNIVERSITY|BOTH`; risk 1–5.
- Chỉ mục: `(tenant_type,disabled_at,code)`.

#### TBL-WRK-068 — `tenant_role_permissions`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `role_id uuid NOT NULL` FK `tenant_roles.id`; `permission_id uuid NOT NULL` FK `tenant_permissions.id`; `granted_by_subject_id uuid NOT NULL`; `valid_from timestamptz NOT NULL DEFAULT now()`; `valid_until timestamptz NULL`; `revoked_at timestamptz NULL`; `revoked_by_subject_id uuid NULL`; `reason varchar(500) NOT NULL`.
- Ràng buộc: partial unique `(role_id,permission_id)` khi active; role/permission tenant type tương thích; validity hợp lệ; revoke yêu cầu actor.
- Chỉ mục: `(role_id,revoked_at,valid_until)`; `(permission_id,revoked_at)`.

#### TBL-WRK-069 — `application_evidence_state_events`

- Tập cột: `APPEND`.
- Cột riêng: `tenant_id uuid NOT NULL`; `application_id uuid NOT NULL`; `study_evidence_id uuid NOT NULL`; `from_status evidence_export_status NULL`; `to_status evidence_export_status NOT NULL`; `source varchar(32) NOT NULL`; `actor_subject_id uuid NULL`; `source_event_id uuid NULL`; `reason_code varchar(80) NOT NULL`; `trace_id varchar(64) NOT NULL`.
- Ràng buộc: unique `(source,source_event_id)` khi source event có; transition `PENDING→READY|UNAVAILABLE`, `READY→HIDDEN|REVOKED`, `UNAVAILABLE→READY|HIDDEN`, `HIDDEN→REVOKED`; withdrawal/revocation không sửa snapshot.
- Chỉ mục: `(application_id,study_evidence_id,occurred_at DESC,id DESC)` để lấy state hiệu lực; `(study_evidence_id,occurred_at DESC)` cho revocation; append-only 24 tháng.

#### TBL-WRK-070 — `outbox_delivery_attempts`

- Tập cột và toàn bộ quy tắc như `TBL-IAM-020`, với `outbox_event_id` FK `TBL-WRK-063`; unique event/attempt; index event/latest và status/retry; append-only 24 tháng.
- Cột riêng đầy đủ: `outbox_event_id uuid NOT NULL`; `attempt_no integer NOT NULL`; `status outbox_status NOT NULL`; `worker_id varchar(120) NOT NULL`; `broker_message_id varchar(180) NULL`; `error_code varchar(80) NULL`; `next_retry_at timestamptz NULL`; `payload_hash char(64) NOT NULL`.

#### TBL-WRK-071 — `internship_program_participants`

- Tập cột: `TENANT_ENTITY` với `tenant_id` FK `university_tenants.id`.
- Cột riêng: `program_id uuid NOT NULL`; `affiliation_id uuid NOT NULL`; `status varchar(24) NOT NULL DEFAULT 'ENROLLED'`; `enrolled_at timestamptz NOT NULL`; `completed_at timestamptz NULL`; `withdrawn_at timestamptz NULL`; `outcome_code varchar(80) NULL`.
- Ràng buộc: composite FKs `(tenant_id,program_id)` và `(tenant_id,affiliation_id)`; unique `(tenant_id,program_id,affiliation_id)`; status `ENROLLED|COMPLETED|WITHDRAWN|REMOVED`; terminal timestamp tương ứng.
- Chỉ mục: `(tenant_id,program_id,status)`; `(tenant_id,affiliation_id,created_at DESC)`; báo cáo cá nhân vẫn cần consent active.

#### TBL-WRK-072 — `application_offer_versions`

- Tập cột: `IMMUTABLE`.
- Cột riêng: `tenant_id uuid NOT NULL`; `application_id uuid NOT NULL`; `version_no integer NOT NULL`; `title varchar(200) NOT NULL`; `terms_snapshot jsonb NOT NULL`; `salary_vnd bigint NULL`; `starts_on date NULL`; `expires_at timestamptz NOT NULL`; `created_by_subject_id uuid NOT NULL`; `approved_by_subject_id uuid NOT NULL`; `issued_at timestamptz NOT NULL`; `supersedes_version_id uuid NULL` self-FK; `content_hash char(64) NOT NULL`.
- Ràng buộc: unique `(application_id,version_no)`; salary>=0; expiry>issued; maker-checker; application/tenant consistent và đang ở nhánh cho phép offer; correction tạo version mới.
- Chỉ mục: `(application_id,version_no DESC)`; PII/financial terms, retention như application.

#### TBL-WRK-073 — `application_offer_state_events`

- Tập cột: `APPEND`.
- Cột riêng: `tenant_id uuid NOT NULL`; `application_id uuid NOT NULL`; `offer_version_id uuid NOT NULL` FK `application_offer_versions.id`; `from_status varchar(24) NULL`; `to_status varchar(24) NOT NULL`; `actor_subject_id uuid NOT NULL`; `reason_code varchar(80) NOT NULL`; `trace_id varchar(64) NOT NULL`.
- Ràng buộc: status `ISSUED|VIEWED|ACCEPTED|DECLINED|EXPIRED|WITHDRAWN`; transition hợp lệ; ACCEPTED/DECLINED đồng bộ application status trong cùng transaction; offer history không sửa/xóa.
- Chỉ mục: `(application_id,occurred_at,id)`; `(offer_version_id,occurred_at DESC)`; 24 tháng.

#### TBL-WRK-074 — `job_screening_questions`

- Tập cột: `ENTITY`; chỉ sửa khi job revision còn DRAFT, bất biến sau submit.
- Cột riêng: `tenant_id uuid NOT NULL`; `job_revision_id uuid NOT NULL` FK `job_revisions.id`; `question_type varchar(24) NOT NULL`; `prompt varchar(1000) NOT NULL`; `is_required boolean NOT NULL DEFAULT false`; `options jsonb NULL`; `validation_rule jsonb NULL`; `position integer NOT NULL`.
- Ràng buộc: unique `(job_revision_id,position)`; type `TEXT|SINGLE_CHOICE|MULTIPLE_CHOICE|YES_NO|NUMBER`; options bắt buộc đúng loại; cấm hỏi protected attributes; tenant khớp revision.
- Chỉ mục: `(tenant_id,job_revision_id,position)`.

#### TBL-WRK-075 — `interview_feedback`

- Tập cột: `APPEND`.
- Cột riêng: `tenant_id uuid NOT NULL`; `interview_id uuid NOT NULL`; `reviewer_subject_id uuid NOT NULL`; `recommendation varchar(24) NOT NULL`; `score numeric(5,2) NULL`; `rubric_snapshot jsonb NOT NULL`; `comment text NULL`; `submitted_at timestamptz NOT NULL`; `trace_id varchar(64) NOT NULL`.
- Ràng buộc: unique `(interview_id,reviewer_subject_id)`; recommendation `STRONG_NO|NO|NEUTRAL|YES|STRONG_YES`; score 0–100; reviewer là participant/active tenant member; protected-attribute policy áp dụng.
- Chỉ mục: `(tenant_id,interview_id,submitted_at)`; DERIVED_SENSITIVE, retention như application.

#### TBL-WRK-076 — `file_upload_sessions`

- Tập cột: `ENTITY`.
- Cột riêng: `file_id uuid NOT NULL UNIQUE` FK `file_objects.id`; `owner_subject_id uuid NOT NULL`; `tenant_id uuid NULL`; `upload_id varchar(200) NOT NULL UNIQUE`; `expected_size_bytes bigint NOT NULL`; `expected_sha256 char(64) NOT NULL`; `part_count integer NOT NULL DEFAULT 1`; `status varchar(24) NOT NULL DEFAULT 'CREATED'`; `expires_at timestamptz NOT NULL`; `completed_at timestamptz NULL`; `aborted_at timestamptz NULL`.
- Ràng buộc: size >0 theo purpose limit; parts 1–10000; status `CREATED|UPLOADING|COMPLETED|ABORTED|EXPIRED`; finalize kiểm size/hash rồi enqueue ClamAV.
- Chỉ mục: `(owner_subject_id,status,created_at DESC)`; `(tenant_id,status,created_at DESC)`; `(status,expires_at)`; purge 7 ngày sau terminal.

## 7. Toàn vẹn tenant, quyền và Row-Level Security

1. API không nhận `tenant_id` làm nguồn quyền. Service lấy `identity_subject_id` từ JWT, resolve active membership, rồi gắn tenant context server-side.
2. Tất cả bảng `TENANT_ENTITY` có `UNIQUE(tenant_id,id)`. Child tenant lưu lại `tenant_id` và dùng composite FK `(tenant_id,parent_id)`; do đó không thể gắn application/note/interview/chat vào tenant khác.
3. PostgreSQL RLS bật defense-in-depth cho bảng tenant. Transaction đặt `SET LOCAL app.subject_id` và `app.tenant_id` từ context đã xác minh; worker dùng service role tách biệt và vẫn truyền tenant.
4. Candidate-own data dùng predicate `candidate.identity_subject_id = app.subject_id`. Recruiter candidate search chỉ đọc projection searchable; application access cần assignment hoặc tenant permission.
5. Admin break-glass dùng role tạm thời, MFA, reason/ticket, expiry tối đa 60 phút và ghi security audit trước + sau truy cập.
6. Background job mang `tenant_id`, `actor_subject_id`, `trace_id`, policy version; worker từ chối payload thiếu context.

## 8. Ma trận query – index bắt buộc

| Query/capability | Bảng và predicate chính | Index được dùng | Giới hạn/khóa |
|---|---|---|---|
| Login | email normalized active | `user_emails(email_normalized)` unique | rate limit theo email/IP hash; không lộ account existence |
| Refresh token | token hash; session/family active | token unique; `(family_id,status)` | khóa token + session; reuse revoke cả family |
| Catalog Study | published + text/order | course version FTS; `(status,published_at)` | page pagination; catalog cache |
| Primary path | learner + ACTIVE | partial unique active path | `FOR UPDATE` learner advisory key khi switch |
| Enroll course | learner/version | unique enrollment | `INSERT ... ON CONFLICT` idempotent |
| Study home | learner active enrollments/progress | enrollment learner/status; snapshot unique | snapshot stale được rebuild từ facts |
| Review assessment | review pending ordered | `(status,submitted_at)` | reviewer claim dùng `SKIP LOCKED`; decision optimistic lock |
| Notification inbox | subject/read/time/id | composite cursor indexes | cursor `(created_at,id)`, page size <=100 |
| Candidate search | visibility + FTS/skill/location | GIN search vector/arrays | chỉ redacted projection; opt-out SLA 5 phút |
| Public job search | PUBLISHED + FTS/location | revision FTS/GIN; job status/time | sponsored query riêng rồi label/merge |
| ATS board | tenant/job/status/time | application tenant/job/status | max 100/page; tenant derived server-side |
| Duplicate apply | candidate/job | unique `(candidate_id,job_id)` | single transaction + idempotency key |
| Interview calendar | tenant/time range/status | schedule tenant/start/end | range max 90 ngày |
| Chat history | conversation + sequence | message `(conversation_id,server_sequence)` | cursor; REST source of truth |
| Payment webhook | provider event/order | webhook unique; payment provider order | lock payment/order; transition precedence |
| Credit spend | entitlement active/balance | entitlement owner/code/status | lock entitlement; append ledger atomically |
| Audit stream | tenant/resource/time | composite + BRIN time | cursor, privileged permission |
| University report | tenant/report/status | report run tenant/status/time | aggregate group >=10; no row-level result |

Mỗi migration thêm query mới phải kèm `EXPLAIN (ANALYZE, BUFFERS)` trên dataset pilot giả lập. Không tạo index chỉ để “dự phòng”; index không được dùng qua hai kỳ release phải được đánh giá loại bỏ bằng migration riêng.

## 9. Transaction, locking và xử lý cạnh tranh

| Tình huống | Transaction boundary và khóa | Kết quả bắt buộc |
|---|---|---|
| Refresh đồng thời/reuse | khóa refresh token, session và các token family theo thứ tự ID | một rotation thành công; lần dùng lại đánh dấu COMPROMISED, revoke family/session và phát audit/outbox |
| Hai primary path switch | advisory lock theo learner + `FOR UPDATE` active period | đúng một ACTIVE; đóng/pause period cũ và tạo period mới/outbox trong cùng commit |
| Enrollment trùng | unique learner/courseVersion + idempotency record | cùng request trả cùng response, không nhân đôi progress |
| Hai attempt submit | lock attempt/enrollment, compare `row_version`, freeze answer/file snapshot | chỉ một submit; request trùng trả replay, payload khác trả conflict |
| Hai reviewer | optimistic compare attempt/job/application version | một decision áp dụng; người còn lại nhận 409 và tải dữ liệu mới |
| Publish content/job | lock aggregate pointer; validate revision hash/rights/scan; update pointer + history + outbox | revision published bất biến; stale `If-Match` không publish |
| Apply đồng thời | insert application unique, snapshot, evidence selections/request, conversation eligibility và outbox trong một transaction | đúng một application; Study outage chỉ để evidence PENDING |
| Terminal application | lock application và conversation | status history + conversation READ_ONLY cùng commit hoặc consumer idempotent bảo đảm hội tụ |
| Webhook trùng/out-of-order | insert webhook dedupe trước, lock payment/order, so state precedence/provider time | không double-settle; return URL không tạo entitlement |
| Entitlement/credit spend | lock entitlement, kiểm active/expiry/balance, append ledger rồi tăng consumed | balance không âm; retry cùng idempotency không spend lần hai |

Thứ tự khóa chuẩn: aggregate root trước, child theo UUID tăng dần, sau cùng outbox. Transaction không gọi network. External call luôn sau commit qua worker/outbox; kết quả ghi bằng transaction idempotent mới.

## 10. Versioning, append-only, outbox và cache

- Path/course/job/CV revision: bản `DRAFT` có thể sửa bằng optimistic concurrency ở aggregate/editor storage; khi submit hệ thống đóng băng thành immutable revision. Nếu cần chỉnh, clone sang version mới. Enrollment/application luôn trỏ phiên bản cụ thể.
- Snapshot application, evidence, payment webhook, status history, review decision, AI output/review, audit, ledger, inbox/outbox là append-only. “Xóa” chỉ ẩn nội dung theo policy và giữ tombstone/hash/audit.
- Mọi mutation phát event lưu aggregate và outbox cùng transaction. Publisher chọn event chưa có attempt `PUBLISHED`, giữ advisory lock theo event, ghi delivery attempt append-only; retry backoff có jitter và attempt cuối `DEAD_LETTER`. Replay giữ cùng `event_id`/`dedupe_key`.
- Consumer ghi inbox trước/đồng transaction với projection. Duplicate cùng hash trả success; duplicate khác hash dừng và báo security incident.
- Redis chỉ cache/session rate limit/queue/fanout. Không là nguồn thật. Cache key mang service, resource ID, version và tenant; mutation invalidate theo outbox. Redis outage degrade về DB/rate limit fail-closed cho auth-sensitive operation.
- Progress percent, candidate search document và report snapshot là projection có high-watermark/calculation version, rebuild được từ fact/history.

## 11. Retention, xóa tài khoản, anonymization và legal hold

| Nhóm | Retention mặc định | Hành động hết hạn |
|---|---|---|
| Notification + delivery | 180 ngày | purge body/payload và record nếu không audit hold |
| Learning activity/support | 13 tháng sau activity/terminal | aggregate metric rồi xóa PII; completion/evidence còn hiệu lực được giữ |
| Application/chat/evidence snapshot/note | 12 tháng sau application terminal | xóa nội dung PII/object; giữ tombstone/hash và audit theo legal hold |
| Audit/security/payment/webhook/ledger/review | tối thiểu 24 tháng hoặc lâu hơn theo finance/legal policy | partition archive mã hóa; chỉ purge theo approved schedule |
| Verification document | 180 ngày sau decision/expiry | xóa object và encryption key; giữ metadata decision/hash |
| Idempotency | 24 giờ; critical mutation 7 ngày | purge response/payload, giữ business aggregate |
| Backup | tối đa 35 ngày | lifecycle delete; restore test định kỳ |
| Deletion request | grace 30 ngày | cho phép cancel trong grace; sau đó orchestration anonymize từng service |

Quy trình deletion:

1. Identity đặt `DELETION_PENDING`, revoke session/token, phát event có deadline; không xóa ngay.
2. Study/Work đánh dấu subject pending, khóa mutation không thiết yếu và thu hồi search/consent tức thì.
3. Sau 30 ngày, mỗi service thay PII bằng alias ngẫu nhiên, xóa/mã hóa hủy khóa file, giữ financial/security/audit tối thiểu. Identity phát `ANONYMIZED` khi nhận acknowledgement.
4. Application/payment có legal hold chỉ pseudonymize trường không cần pháp lý; record hold ghi `legal_hold_until`, reason và approver trong audit, không âm thầm bỏ qua purge.
5. Backup không sửa trực tiếp; dữ liệu đã xóa có thể tồn tại tối đa 35 ngày nhưng restore runbook phải chạy deletion replay trước khi mở traffic.

Candidate opt-out không chờ deletion: transaction đặt PRIVATE và outbox; worker xóa search projection trong tối đa 5 phút, sponsored profile dừng đồng thời. Consent withdrawal ẩn university/evidence ngay; revocation tạo state event `REVOKED`, không sửa evidence snapshot và vẫn giữ audit.

## 12. Mã hóa, secret và dữ liệu nhạy cảm

- TLS mọi kết nối; PostgreSQL volume/backup và object storage mã hóa. Cột ciphertext dùng envelope encryption với KMS/Vault key version trong metadata mã hóa, không lưu key trong DB.
- Password chỉ Argon2id hash; refresh/verification/reset/invite/recovery code chỉ lưu hash. JWT private key chỉ lưu reference; public JWK được publish.
- Không lưu card, tài khoản ví, CVV, payment credential, provider secret hoặc raw webhook signing key. Webhook raw payload mã hóa để đối soát; log chỉ có hash/ID đã redaction.
- Signed URL có audience, subject/resource, expiry <=5 phút, one-purpose; API kiểm ownership/tenant trước khi ký. File MIME kiểm magic bytes, malware scan, quarantine; filename luôn escape khi download.
- AI input là snapshot allowlist; loại email/phone/name khi capability không cần, protected attributes, Study evidence và sponsored status khỏi matching. Nội dung CV/JD được coi là untrusted prompt data.

## 13. Migration, backup và khôi phục

### 13.1 Migration policy

- Mỗi service sở hữu migration sequence riêng: Identity/Study dùng Alembic, Work dùng Prisma migration có SQL review. CI chạy từ database trống và từ bản production gần nhất.
- Dùng expand/contract: thêm nullable/default-safe cột → deploy dual read/write/backfill theo batch → kiểm mismatch zero → chuyển read → thêm NOT NULL/constraint → bỏ cột cũ ở release sau.
- Không rename/drop/đổi enum phá vỡ trong cùng release. Index lớn dùng `CREATE INDEX CONCURRENTLY`; constraint lớn thêm `NOT VALID`, backfill rồi `VALIDATE`.
- Backfill có checkpoint, rate limit, tenant scope, idempotency và audit; không giữ lock transaction dài. Migration tuyệt đối không gọi service ngoài hoặc seed dữ liệu production.
- Schema version event/API tương thích tối thiểu một phiên bản trước. Consumer lạ field phải bỏ qua; thiếu required version phải vào DLQ, không đoán.
- Mọi migration có owner, rollback/roll-forward plan, ước lượng lock/disk, query plan và kiểm retention/RLS/composite FK.

### 13.2 Backup/DR

- PostgreSQL PITR bằng WAL, backup full hằng ngày; retention tối đa 35 ngày; object storage versioning/lifecycle cùng policy. Backup từng DB độc lập nhưng recovery manifest ghi high-watermark event để replay projection.
- RPO 15 phút, RTO 4 giờ. Restore drill tối thiểu mỗi quý, kiểm checksum, migration version, inbox/outbox replay, signed-key/JWKS continuity và deletion replay.
- Không lấy transaction distributed xuyên ba DB. Sau restore, dùng outbox/inbox/reconciliation để hội tụ; payment reconciliation và evidence export được chạy trước khi mở mutation liên quan.

## 14. Checklist nghiệm thu mô hình dữ liệu

- Ba DB không có cross-database FK/query; mọi external ID và event đều có version/dedupe/trace.
- Đúng một primary path ACTIVE; một enrollment/learner/course version; một application/candidate/job; một conversation/application.
- Published revision và mọi snapshot/history/audit/payment/AI review/outbox là immutable hoặc append-only theo định nghĩa.
- Mọi tenant child có tenant context + composite FK; test cross-tenant IDOR thất bại kể cả khi đoán đúng UUID.
- File chưa CLEAN không được attach/publish/download; MIME spoof/malware bị quarantine.
- Candidate PRIVATE không nằm trong search/sponsored trong tối đa 5 phút; search không chứa contact/CV/Study evidence.
- Payment chỉ SETTLED bởi webhook/IPN hoặc reconciliation đã xác minh; callback trùng/out-of-order không tạo entitlement/credit hai lần.
- AI không ghi ATS state; score không dùng protected/evidence/sponsored fields; mọi output áp dụng có human review.
- Retention, account deletion, consent withdrawal, legal hold và backup deletion replay có test tự động/restore drill.
- Query-index matrix có test plan trên dữ liệu pilot 5.000 account, 500 DAU, 50 RPS và không vượt SLO đã khóa.
