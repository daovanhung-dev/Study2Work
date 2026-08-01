# Plan 10 — Learner Community

## 1. Mục tiêu

Hoàn thành **5 file Detail Design API** theo `Detail_Design_API_Template_Optimized.xlsx` cho phạm vi API từ STT **70–74**.

- API trực tiếp từ tài liệu/sequence: **3**.
- API suy dẫn từ BD: **2**.
- Module: 08. Cộng đồng Zalo (5).
- Lý do quy mô batch: 5 API learner tập trung eligibility, mở link Zalo và báo cáo vi phạm.

> API có `Basis = SUY DẪN` chỉ được chốt ở trạng thái **Draft — Needs Confirmation** cho đến khi endpoint, contract và business rule được xác nhận. Không biến suy luận thành dữ kiện.

## 2. Điều kiện tiên quyết

- Learning path/course access.
- Community group status.
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
- `BD/08. Study2Work_Study_BasicDesign_Cong_Dong_Zalo.md`
- `BD/diagram/SEQUENCE/09. Study2Work_Study_SEQ_Cong_Dong_Zalo.md`
- `BD/diagram/AC/09. Study2Work_Study_AC_Cong_Dong_Zalo.md`

## 4. Danh sách API phải hoàn thành

### API 070 — `GET /api/v1/community-groups`

- **DD filename:** `API_070_GET_community_groups.xlsx`
- **Module:** 08. Cộng đồng Zalo
- **Authentication/Authorization:** Learner/Optional Public
- **Basis:** TRỰC TIẾP
- **Source:** SEQ-09
- **Purpose:** Lấy các nhóm cộng đồng phù hợp theo quyền, lộ trình, khóa học hoặc chủ đề.
- **Input baseline:** Query: path_id?, course_id?, topic?, scope?, status?
- **Output baseline:** data[]: id, name, description, scope, moderator_summary, status, can_view_link, rules_ack_required
- **Business rules:** COM-06

### API 071 — `GET /api/v1/community-groups/{group_id}`

- **DD filename:** `API_071_GET_community_groups_by_group_id.xlsx`
- **Module:** 08. Cộng đồng Zalo
- **Authentication/Authorization:** Learner/Optional Public
- **Basis:** SUY DẪN
- **Source:** BD-08
- **Purpose:** Xem thông tin nhóm và quy tắc; link chỉ trả khi đủ quyền.
- **Input baseline:** Path: group_id
- **Output baseline:** data: group fields, rules[], status, access_state, join_link? hoặc link_hidden_reason
- **Business rules:** COM-06

### API 072 — `POST /api/v1/community-groups/{group_id}/open-link`

- **DD filename:** `API_072_POST_community_groups_by_group_id_open_link.xlsx`
- **Module:** 08. Cộng đồng Zalo
- **Authentication/Authorization:** Learner
- **Basis:** TRỰC TIẾP
- **Source:** SEQ-09
- **Purpose:** Xác nhận đã đọc quy tắc, ghi nhận sự kiện mở link và trả liên kết Zalo.
- **Input baseline:** Path: group_id; Body: accepted_rules=true, rules_version
- **Output baseline:** data: join_url, opened_at, event_id, disclaimer='opened_not_joined'
- **Business rules:** COM-04, COM-05

### API 073 — `POST /api/v1/community-groups/{group_id}/reports`

- **DD filename:** `API_073_POST_community_groups_by_group_id_reports.xlsx`
- **Module:** 08. Cộng đồng Zalo
- **Authentication/Authorization:** Learner
- **Basis:** TRỰC TIẾP
- **Source:** SEQ-09
- **Purpose:** Báo link hỏng, spam/lừa đảo, sai nội dung, moderator hoặc quy tắc.
- **Input baseline:** Path: group_id; Body: issue_type, description, evidence_url?
- **Output baseline:** data: report_id, status=OPEN, submitted_at
- **Business rules:** COM-07

### API 074 — `GET /api/v1/me/community-reports`

- **DD filename:** `API_074_GET_me_community_reports.xlsx`
- **Module:** 08. Cộng đồng Zalo
- **Authentication/Authorization:** Learner
- **Basis:** SUY DẪN
- **Source:** BD-08
- **Purpose:** Theo dõi báo cáo cộng đồng đã gửi.
- **Input baseline:** Query: status?, page, page_size
- **Output baseline:** data[]: report_id, group_summary, issue_type, status, response?, created_at, resolved_at?; meta
- **Business rules:** Module 4.5

## 5. Trọng tâm thiết kế của batch

- Không trả link khi learner chưa đủ điều kiện hoặc group không hoạt động.
- Open-link phải xác nhận rule acceptance và ghi event/audit.
- Link cần mask/secure handling; tránh cache sai phạm vi.
- Report phải chống spam, có category, evidence và trạng thái theo dõi.

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

- **5 workbook `.xlsx`**, đúng tên trong mục 4.
- `PLAN_RESULT.md` của batch: trạng thái từng API, nguồn đã dùng, assumption, conflict, reviewer note và lỗi còn mở.
- `BUSINESS_CODE_DELTA.md` nếu phát sinh business code mới hoặc xung đột ý nghĩa.
- `OPEN_QUESTIONS.md` chỉ chứa câu hỏi có ảnh hưởng contract/nghiệp vụ/bảo mật/dữ liệu; không đưa câu hỏi có thể tự giải quyết từ nguồn.

## 8. Definition of Done

- [ ] Đủ 5/5 API, không thiếu STT và không trùng endpoint.
- [ ] Overview khớp method, endpoint, auth, module và source.
- [ ] Mọi request field được sử dụng hoặc ghi rõ không sử dụng.
- [ ] Mọi response field có source/mapping và null/empty rule.
- [ ] Flow Data Mapping đúng execution order và đủ query params/result handling.
- [ ] Transaction, locking, idempotency, concurrency và rollback được mô tả khi áp dụng.
- [ ] Mọi lỗi trong flow xuất hiện trong sheet Error và có Data Mapping Ref.
- [ ] DB table sheets chỉ có cho bảng bị thay đổi.
- [ ] Không còn placeholder `<...>` chưa được giải thích.
- [ ] API suy dẫn được gắn cờ và không tự chuyển thành Final.
