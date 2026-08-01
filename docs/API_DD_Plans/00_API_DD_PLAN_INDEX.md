# Master Plan — Tạo Detail Design cho 157 API Study2Work Study

## 1. Kết luận phạm vi

- Baseline catalog: **157 API**.
- Chia thành **20 plan**, mỗi plan **4–11 API**, nhóm theo aggregate/lifecycle/security boundary thay vì chia máy móc theo số lượng.
- Tổng basis: **32 API trực tiếp**, **125 API suy dẫn**.
- Mỗi API tạo **01 workbook `.xlsx`** từ `Detail_Design_API_Template_Optimized.xlsx`.
- Thứ tự plan là thứ tự khuyến nghị để giảm dependency và rework.

## 2. Foundation Gate trước khi tạo DD Final

1. Dùng response envelope chuẩn kiến trúc tích hợp: `success`, `businessCode`, `message`, `data`, `meta`, `traceId`; lỗi có `errors[]`.
2. Khóa JSON/query naming convention và pagination convention.
3. Khóa role/permission vocabulary và authorization scope.
4. Khóa business code registry dùng chung.
5. Quyết định hai endpoint SEQ-08 có nằm trong public catalog hay là internal use case.
6. API suy dẫn chỉ được tạo ở trạng thái Draft/Needs Confirmation.

## 3. Danh sách plan

| Plan | Phạm vi STT | API | Trực tiếp | Suy dẫn | File |
|---:|---:|---:|---:|---:|---|
| 01 | 1–6 | 6 | 3 | 3 | [PLAN_01_Public_Catalog.md](./PLAN_01_Public_Catalog.md) |
| 02 | 7–15 | 9 | 3 | 6 | [PLAN_02_Authentication_Core.md](./PLAN_02_Authentication_Core.md) |
| 03 | 16–20 | 5 | 0 | 5 | [PLAN_03_Profile_Contact_Navigation.md](./PLAN_03_Profile_Contact_Navigation.md) |
| 04 | 21–27 | 7 | 4 | 3 | [PLAN_04_Onboarding.md](./PLAN_04_Onboarding.md) |
| 05 | 28–38 | 11 | 2 | 9 | [PLAN_05_Learning_Paths_and_Support_Requests.md](./PLAN_05_Learning_Paths_and_Support_Requests.md) |
| 06 | 39–47 | 9 | 1 | 8 | [PLAN_06_Courses_Chapters_Lessons_Resources.md](./PLAN_06_Courses_Chapters_Lessons_Resources.md) |
| 07 | 48–56 | 9 | 2 | 7 | [PLAN_07_Learner_Exercises_Submissions.md](./PLAN_07_Learner_Exercises_Submissions.md) |
| 08 | 57–60 | 4 | 1 | 3 | [PLAN_08_Admin_Exercise_Review.md](./PLAN_08_Admin_Exercise_Review.md) |
| 09 | 61–69 | 9 | 1 | 8 | [PLAN_09_Progress_Completion.md](./PLAN_09_Progress_Completion.md) |
| 10 | 70–74 | 5 | 3 | 2 | [PLAN_10_Learner_Community.md](./PLAN_10_Learner_Community.md) |
| 11 | 75–82 | 8 | 1 | 7 | [PLAN_11_Admin_Community.md](./PLAN_11_Admin_Community.md) |
| 12 | 83–93 | 11 | 4 | 7 | [PLAN_12_Notifications.md](./PLAN_12_Notifications.md) |
| 13 | 94–100 | 7 | 0 | 7 | [PLAN_13_Admin_Learning_Paths.md](./PLAN_13_Admin_Learning_Paths.md) |
| 14 | 101–108 | 8 | 0 | 8 | [PLAN_14_Admin_Courses.md](./PLAN_14_Admin_Courses.md) |
| 15 | 109–117 | 9 | 0 | 9 | [PLAN_15_Admin_Chapters_Lessons.md](./PLAN_15_Admin_Chapters_Lessons.md) |
| 16 | 118–127 | 10 | 2 | 8 | [PLAN_16_Admin_Resources_Exercises_Publishing.md](./PLAN_16_Admin_Resources_Exercises_Publishing.md) |
| 17 | 128–133 | 6 | 2 | 4 | [PLAN_17_Admin_Learner_Lookup_Support.md](./PLAN_17_Admin_Learner_Lookup_Support.md) |
| 18 | 134–141 | 8 | 0 | 8 | [PLAN_18_Admin_Learner_Exceptional_Actions.md](./PLAN_18_Admin_Learner_Exceptional_Actions.md) |
| 19 | 142–149 | 8 | 2 | 6 | [PLAN_19_Operational_Reports.md](./PLAN_19_Operational_Reports.md) |
| 20 | 150–157 | 8 | 1 | 7 | [PLAN_20_RBAC_Audit.md](./PLAN_20_RBAC_Audit.md) |
| **Tổng** | **1–157** | **157** | **32** | **125** | |

## 4. Thứ tự triển khai khuyến nghị

1. Plan 01–04: public catalog, auth, profile, onboarding.
2. Plan 05–09: learning path, content, exercise, progress.
3. Plan 10–12: community và notification.
4. Plan 13–16: admin content lifecycle và publishing.
5. Plan 17–18: learner support và exceptional operations.
6. Plan 19–20: reporting, RBAC và audit.

## 5. Quy ước output

- Root đề xuất: `docs/DD/API/`.
- Mỗi plan có thư mục riêng: `docs/DD/API/PLAN_XX/`.
- Workbook: `API_<STT>_<METHOD>_<endpoint-slug>.xlsx`.
- Kết quả batch: `PLAN_RESULT.md`, `BUSINESS_CODE_DELTA.md`, `OPEN_QUESTIONS.md`.

## 6. Quality Gate toàn dự án

- [ ] Không thiếu/không trùng API.
- [ ] Endpoint, method, auth, request và response có nguồn truy vết.
- [ ] Mọi query có table, params, SQL/pseudocode và result handling.
- [ ] Mutation có transaction boundary, locking/concurrency, rollback và audit.
- [ ] Mọi error có HTTP status, business code, safe message và Data Mapping Ref.
- [ ] DB sheets chỉ tạo cho bảng bị thay đổi.
- [ ] Không còn placeholder hoặc assumption không gắn nhãn.
- [ ] API suy dẫn không được đánh dấu Final khi chưa xác nhận.

## 7. Tài liệu đi kèm

- [Báo cáo đọc nguồn và kiểm kê](./00_SOURCE_READ_REPORT.md)