# Plan 04 — Onboarding

## 1. Mục tiêu

Hoàn thành **7 file Detail Design API** theo `Detail_Design_API_Template_Optimized.xlsx` cho phạm vi API từ STT **21–27**.

- API trực tiếp từ tài liệu/sequence: **4**.
- API suy dẫn từ BD: **3**.
- Module: 03. Onboarding (7).
- Lý do quy mô batch: 7 API bao phủ một stateful workflow hoàn chỉnh từ cấu hình, draft, gợi ý đến xác nhận.

> API có `Basis = SUY DẪN` chỉ được chốt ở trạng thái **Draft — Needs Confirmation** cho đến khi endpoint, contract và business rule được xác nhận. Không biến suy luận thành dữ kiện.

## 2. Điều kiện tiên quyết

- Plan 02.
- Catalog learning paths.
- Onboarding state machine.
- Áp dụng canonical response envelope từ `Study2Work_System_Architecture.md`: `success`, `businessCode`, `message`, `data`, `meta`, `traceId`; lỗi dùng `errors[]` và không trả stack trace.
- Khóa quy ước JSON/query naming (`camelCase` hay `snake_case`) trước khi chốt bản Final; catalog hiện còn các tên như `page_size` trong khi kiến trúc tích hợp minh họa `pageSize`.
- Mỗi API là một workbook riêng; không gộp nhiều API vào một workbook.

## 3. Nguồn bắt buộc phải đọc khi thực hiện plan

- `BD/0. Study2Work_Study_Business_Description.md`
- `BD/base/0. Study2Work_System_Architecture.md`
- `BD/base/1. Study2Work_Study_Architecture.md`
- `BD/diagram/UC/01. Study2Work_Study_Diagram_UC_Tong_Quan.md`
- `BD/diagram/CLASS/01. Study2Work_Study_Diagram_CLASS_Mo_Hinh_Nghiep_Vu.md`
- `BD/diagram/CLASS/study2work_study_full_schema_seed.sql`
- `Detail_Design_API_Template_Optimized.xlsx`
- `Study2Work_API_Catalog_from_BD(1).csv`
- `BD/03. Study2Work_Study_BasicDesign_Onboarding.md`
- `BD/diagram/SEQUENCE/04. Study2Work_Study_SEQ_Onboarding_Goi_Y_Lo_Trinh.md`
- `BD/diagram/AC/04. Study2Work_Study_AC_Onboarding.md`
- `BD/04. Study2Work_Study_BasicDesign_Lo_Trinh_Hoc.md`

## 4. Danh sách API phải hoàn thành

### API 021 — `GET /api/v1/onboarding/config`

- **DD filename:** `API_021_GET_onboarding_config.xlsx`
- **Module:** 03. Onboarding
- **Authentication/Authorization:** Verified Learner
- **Basis:** SUY DẪN
- **Source:** BD-03
- **Purpose:** Lấy cấu hình bước onboarding, mục tiêu, công nghệ và lựa chọn nền tảng.
- **Input baseline:** Query: version?
- **Output baseline:** data: version, steps[], programming_levels[], technologies[], experience_types[], support_needs[], goals[], time_slot_options[]
- **Business rules:** ONB-06

### API 022 — `GET /api/v1/onboarding/current`

- **DD filename:** `API_022_GET_onboarding_current.xlsx`
- **Module:** 03. Onboarding
- **Authentication/Authorization:** Verified Learner
- **Basis:** TRỰC TIẾP
- **Source:** SEQ-04
- **Purpose:** Lấy trạng thái onboarding, bản nháp và bước cần tiếp tục.
- **Input baseline:** Không có
- **Output baseline:** data: status, current_step, completed_steps[], draft_answers, selected_path_id?, last_saved_at
- **Business rules:** ONB-05

### API 023 — `PATCH /api/v1/onboarding/draft`

- **DD filename:** `API_023_PATCH_onboarding_draft.xlsx`
- **Module:** 03. Onboarding
- **Authentication/Authorization:** Verified Learner
- **Basis:** TRỰC TIẾP
- **Source:** SEQ-04
- **Purpose:** Lưu hợp lệ dữ liệu từng bước và cho phép tiếp tục sau khi thoát.
- **Input baseline:** Body: step_code, answers (basic_info/background/goals/study_time), current_step
- **Output baseline:** data: saved=true, current_step, completed_steps[], draft_answers, validation, onboarding_status=ONBOARDING_IN_PROGRESS
- **Business rules:** ONB-05

### API 024 — `GET /api/v1/onboarding/recommended-paths`

- **DD filename:** `API_024_GET_onboarding_recommended_paths.xlsx`
- **Module:** 03. Onboarding
- **Authentication/Authorization:** Verified Learner
- **Basis:** TRỰC TIẾP
- **Source:** SEQ-04
- **Purpose:** Sinh danh sách lộ trình gợi ý từ hồ sơ onboarding.
- **Input baseline:** Query: limit?; sử dụng bản nháp onboarding đã lưu
- **Output baseline:** data[]: path_id, name, match_reason[], target_users[], prerequisites[], duration, outcomes[], difficulty, score_or_rank
- **Business rules:** ONB-04

### API 025 — `PUT /api/v1/onboarding/selected-path`

- **DD filename:** `API_025_PUT_onboarding_selected_path.xlsx`
- **Module:** 03. Onboarding
- **Authentication/Authorization:** Verified Learner
- **Basis:** SUY DẪN
- **Source:** BD-03
- **Purpose:** Chọn duy nhất một lộ trình để xác nhận; chưa kích hoạt.
- **Input baseline:** Body: path_id
- **Output baseline:** data: selected_path, selected_at, still_published, activation_not_started=true
- **Business rules:** ONB-03, ONB-04

### API 026 — `GET /api/v1/onboarding/review`

- **DD filename:** `API_026_GET_onboarding_review.xlsx`
- **Module:** 03. Onboarding
- **Authentication/Authorization:** Verified Learner
- **Basis:** SUY DẪN
- **Source:** BD-03
- **Purpose:** Lấy toàn bộ thông tin xác nhận trước khi hoàn tất onboarding.
- **Input baseline:** Không có
- **Output baseline:** data: basic_info, background, goals, study_time, selected_path, one_active_path_rule, exception_policy, missing_fields[]
- **Business rules:** ONB-01

### API 027 — `POST /api/v1/onboarding/confirm`

- **DD filename:** `API_027_POST_onboarding_confirm.xlsx`
- **Module:** 03. Onboarding
- **Authentication/Authorization:** Verified Learner
- **Basis:** TRỰC TIẾP
- **Source:** SEQ-04
- **Purpose:** Xác nhận dữ liệu và chuyển tài khoản sang READY_TO_LEARN.
- **Input baseline:** Body: selected_path_id, confirmed=true, accepted_learning_rules=true
- **Output baseline:** data: completed=true, confirmed_at, account_status=READY_TO_LEARN, selected_path, next_route
- **Business rules:** ONB-01, ONB-02, ONB-08

## 5. Trọng tâm thiết kế của batch

- Draft phải idempotent, cho phép tiếp tục đúng bước và không làm mất dữ liệu hợp lệ.
- Recommendation phải nêu rõ input, ranking/selection rule và fallback khi không có kết quả.
- Chỉ một selected path; selected chưa đồng nghĩa activated.
- Confirm phải kiểm tra lại toàn bộ dữ liệu và chuyển trạng thái READY_TO_LEARN trong transaction.

## 6. Quy trình thực hiện cho từng API

1. **Reconcile nguồn:** đối chiếu catalog với BD, AC, Sequence, Class Diagram, schema SQL và kiến trúc. Ghi rõ dữ kiện, suy luận, giả định và xung đột.
2. **Tạo workbook:** sao chép template; đặt filename theo danh sách; không thay đổi cấu trúc sheet nếu chưa có lý do.
3. **Overview + History:** điền định danh, module, endpoint, method, auth, owner, source, transaction, affected tables, assumptions và version `0.1.0 Draft`.
4. **Request:** mô tả Path/Query/Header/Body theo JSON Path; type, format, required, nullable, default, validation và ví dụ.
5. **Response:** dùng canonical envelope; mọi field phải có source và mapping; list API phải có `meta.pagination`; HTTP 204 không có body.
6. **Data Mapping:** viết theo đúng execution order; tại mỗi query nêu bảng, mục đích, params, SQL/pseudocode, xử lý kết quả; nêu transaction, locking, idempotency, side effects và rollback.
7. **Error:** liệt kê toàn bộ validation/auth/permission/not-found/conflict/business/system/dependency errors; mỗi lỗi trỏ về Data Mapping Ref.; business code không trùng nghĩa.
8. **DB sheets:** chỉ duplicate `DB_TABLE_TEMPLATE` cho bảng có INSERT/UPDATE/DELETE/UPSERT hoặc thay đổi schema/constraint/index. SELECT thuần chỉ mô tả trong Data Mapping.
9. **Review chéo:** Request → variable → query/table → response; Data Mapping → Error; mutation → audit/notification/outbox; xóa toàn bộ placeholder không áp dụng.
10. **Chốt trạng thái:** chỉ đổi sang `Ready for Review` khi toàn bộ checklist đạt; API suy dẫn vẫn giữ cờ xác nhận.

## 7. Deliverables

- **7 workbook `.xlsx`**, đúng tên trong mục 4.
- `PLAN_RESULT.md` của batch: trạng thái từng API, nguồn đã dùng, assumption, conflict, reviewer note và lỗi còn mở.
- `BUSINESS_CODE_DELTA.md` nếu phát sinh business code mới hoặc xung đột ý nghĩa.
- `OPEN_QUESTIONS.md` chỉ chứa câu hỏi có ảnh hưởng contract/nghiệp vụ/bảo mật/dữ liệu; không đưa câu hỏi có thể tự giải quyết từ nguồn.

## 8. Definition of Done

- [ ] Đủ 7/7 API, không thiếu STT và không trùng endpoint.
- [ ] Overview khớp method, endpoint, auth, module và source.
- [ ] Mọi request field được sử dụng hoặc ghi rõ không sử dụng.
- [ ] Mọi response field có source/mapping và null/empty rule.
- [ ] Flow Data Mapping đúng execution order và đủ query params/result handling.
- [ ] Transaction, locking, idempotency, concurrency và rollback được mô tả khi áp dụng.
- [ ] Mọi lỗi trong flow xuất hiện trong sheet Error và có Data Mapping Ref.
- [ ] DB table sheets chỉ có cho bảng bị thay đổi.
- [ ] Không còn placeholder `<...>` chưa được giải thích.
- [ ] API suy dẫn được gắn cờ và không tự chuyển thành Final.
