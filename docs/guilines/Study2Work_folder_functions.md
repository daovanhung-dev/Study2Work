# Mô tả chức năng toàn bộ folder dự án Study2Work

Tài liệu này mô tả chức năng của các folder đã được tạo theo kiến trúc monorepo của dự án **Study2Work**.

---

## 1) Root của dự án

### `Study2Work/`
Thư mục gốc của toàn bộ hệ thống. Chứa các ứng dụng frontend, backend, package dùng chung, hạ tầng triển khai, tài liệu, dữ liệu lưu trữ, script, test và các file cấu hình cấp cao.

### Các file gốc ở root
- `.env.example`: mẫu biến môi trường cho toàn dự án.
- `.gitignore`: danh sách file/thư mục không đưa lên Git.
- `.editorconfig`: chuẩn định dạng code cơ bản.
- `README.md`: giới thiệu dự án và cách chạy.
- `LICENSE`: giấy phép sử dụng.
- `CHANGELOG.md`: lịch sử thay đổi theo phiên bản.
- `CONTRIBUTING.md`: hướng dẫn đóng góp.
- `docker-compose.yml`: cấu hình chạy nhiều service bằng Docker Compose.
- `prettier.config.js`: cấu hình format code.
- `eslint.config.js`: cấu hình kiểm tra code.

---

## 2) `apps/` — Nhóm ứng dụng frontend và mobile

### `apps/`
Chứa toàn bộ các ứng dụng đầu cuối của hệ thống. Mỗi app phục vụ một nhóm người dùng hoặc mục đích riêng.

---

### `apps/web-public/`
Ứng dụng public dùng cho người dùng chưa đăng nhập hoặc khách truy cập.

#### `src/`
Chứa mã nguồn chính của website public.
- `app/`: khởi tạo ứng dụng, cấu hình router, providers, layout gốc.
- `components/`: các component dùng lại nhiều nơi.
- `layouts/`: bố cục trang như header, footer, sidebar, default layout.
- `pages/`: các trang chính của website.
- `sections/`: các khối nội dung lớn trên landing page.
- `services/`: lớp gọi API và xử lý dữ liệu từ backend.
- `stores/`: quản lý state toàn cục.
- `utils/`: các hàm tiện ích.
- `assets/`: hình ảnh, icon, font, file tĩnh.

#### `public/`
Chứa tài nguyên tĩnh được phục vụ trực tiếp từ trình duyệt.

#### `tests/`
Chứa test cho website public.

---

### `apps/web-student/`
Ứng dụng dành cho học viên.

#### `src/`
- `app/`: bootstrap ứng dụng và cấu hình toàn cục.
- `components/`: component dùng chung cho học viên.
- `modules/`: chia theo nghiệp vụ của học viên.
  - `dashboard/`: trang tổng quan tiến độ học tập.
  - `learning/`: học bài, học lộ trình, xem nội dung.
  - `practice/`: làm bài luyện tập, quiz, bài tập.
  - `assessment/`: kiểm tra, đánh giá năng lực.
  - `projects/`: quản lý dự án học tập và bài nộp.
  - `portfolio/`: hồ sơ năng lực và sản phẩm cá nhân.
  - `cv-builder/`: tạo và chỉnh sửa CV.
  - `interview/`: luyện phỏng vấn, câu hỏi, phản hồi.
  - `community/`: tham gia cộng đồng học tập.
- `routes/`: khai báo đường dẫn và phân quyền route.
- `services/`: gọi API và xử lý dữ liệu.
- `stores/`: state của ứng dụng.
- `composables/`: logic tái sử dụng theo kiểu hook/composable.
- `utils/`: tiện ích dùng chung.
- `assets/`: tài nguyên tĩnh.

#### `tests/`
Chứa kiểm thử cho web học viên.

---

### `apps/web-mentor/`
Ứng dụng dành cho mentor/giảng viên.

#### `src/`
- `app/`: khởi tạo app và config chung.
- `modules/`: chức năng theo nghiệp vụ mentor.
  - `dashboard/`: tổng quan lớp, học viên, công việc.
  - `class-management/`: quản lý lớp và nhóm học.
  - `assignments/`: giao và quản lý bài tập.
  - `code-review/`: review code, nhận xét, góp ý.
  - `assessments/`: tạo, chấm, quản lý đánh giá.
  - `mentoring-sessions/`: quản lý buổi mentoring.
  - `workshops/`: tổ chức và quản lý workshop.
- `components/`: component dùng chung.
- `services/`: lớp gọi API.
- `stores/`: state của mentor.
- `assets/`: tài nguyên tĩnh.

#### `tests/`
Kiểm thử các luồng nghiệp vụ mentor.

---

### `apps/web-employer/`
Ứng dụng dành cho doanh nghiệp.

#### `src/`
- `app/`: khởi tạo app.
- `modules/`: chia theo chức năng tuyển dụng.
  - `company-profile/`: hồ sơ doanh nghiệp.
  - `job-posts/`: đăng và quản lý tin tuyển dụng.
  - `candidate-search/`: tìm kiếm ứng viên.
  - `candidate-profile/`: xem hồ sơ ứng viên.
  - `shortlist/`: danh sách ứng viên quan tâm.
  - `hiring-workflow/`: quy trình tuyển dụng.
- `components/`: component tái sử dụng.
- `services/`: API và xử lý dữ liệu.
- `stores/`: state toàn cục.
- `assets/`: tài nguyên tĩnh.

#### `tests/`
Kiểm thử các tính năng dành cho doanh nghiệp.

---

### `apps/web-admin/`
Ứng dụng dành cho quản trị hệ thống.

#### `src/`
- `app/`: khởi tạo ứng dụng admin.
- `modules/`: các nghiệp vụ quản trị.
  - `dashboard/`: dashboard quản trị.
  - `user-management/`: quản lý người dùng.
  - `role-permission/`: phân quyền, vai trò.
  - `content-management/`: quản lý nội dung hệ thống.
  - `mentor-management/`: quản lý mentor.
  - `employer-management/`: quản lý doanh nghiệp.
  - `assessment-management/`: quản lý đánh giá.
  - `report-analytics/`: báo cáo, phân tích dữ liệu.
  - `system-settings/`: cài đặt hệ thống.
- `components/`: component dùng chung.
- `services/`: giao tiếp với backend.
- `stores/`: state cho admin.
- `assets/`: tài nguyên tĩnh.

#### `tests/`
Kiểm thử chức năng quản trị.

---

### `apps/mobile-app/`
Ứng dụng Flutter cho mobile.

#### `lib/`
- `app/`: khởi tạo app, router, dependency injection, bootstrap.
- `core/`: phần lõi dùng chung.
  - `config/`: cấu hình môi trường, API, app settings.
  - `constants/`: hằng số.
  - `theme/`: màu sắc, typography, theme system.
  - `routes/`: khai báo route.
  - `utils/`: tiện ích lõi.
- `features/`: chia theo từng nghiệp vụ.
  - `auth/`: đăng nhập, đăng ký, xác thực.
  - `dashboard/`: màn hình tổng quan.
  - `learning/`: học tập.
  - `practice/`: luyện tập.
  - `assessment/`: đánh giá.
  - `portfolio/`: hồ sơ năng lực.
  - `community/`: cộng đồng.
  - `profile/`: hồ sơ cá nhân.
- `shared/`: widget, helper, model dùng chung.
- `main.dart`: điểm khởi chạy ứng dụng.

#### `test/`
Kiểm thử cho ứng dụng Flutter.

---

## 3) `backend/` — Ứng dụng backend

### `backend/`
Chứa toàn bộ logic server, API, nghiệp vụ, tích hợp và tầng dữ liệu.

### `backend/src/`
- `main.ts`: điểm khởi chạy backend.
- `app.module.ts`: module gốc của ứng dụng.
- `config/`: cấu hình môi trường, database, auth, logger.
- `common/`: các thành phần dùng chung cho toàn backend.
  - `constants/`: hằng số dùng chung.
  - `decorators/`: decorator tùy biến.
  - `dto/`: DTO dùng chung.
  - `enums/`: enum hệ thống.
  - `exceptions/`: custom exception.
  - `filters/`: exception filters.
  - `guards/`: auth guard, role guard.
  - `interceptors/`: intercept request/response.
  - `interfaces/`: interface và contract.
  - `pipes/`: validation và transform pipe.
  - `utils/`: hàm tiện ích dùng chung.
- `database/`: tầng dữ liệu và truy cập DB.
  - `migrations/`: migration schema.
  - `seeds/`: dữ liệu mẫu ban đầu.
  - `entities/`: entity mô tả bảng dữ liệu.
  - `repositories/`: lớp truy cập dữ liệu.
- `modules/`: các module nghiệp vụ chính.
  - `auth/`: xác thực và phân quyền.
  - `users/`: quản lý người dùng.
  - `learning/`: nghiệp vụ học tập.
  - `practice/`: bài tập, luyện tập.
  - `assessment/`: kiểm tra, đánh giá.
  - `projects/`: dự án, bài nộp, collaboration.
  - `portfolio/`: portfolio và hồ sơ năng lực.
  - `career/`: CV, matching, hướng nghiệp.
  - `employer/`: nghiệp vụ doanh nghiệp và tuyển dụng.
  - `community/`: cộng đồng, thảo luận.
  - `notifications/`: thông báo đa kênh.
  - `ai/`: tích hợp AI, prompt, adapter.
  - `admin/`: nghiệp vụ quản trị.
  - `analytics/`: thống kê, báo cáo, phân tích.
- `events/`: xử lý sự kiện nội bộ hoặc event-driven.
- `jobs/`: background job, schedule job, queue job.
- `integrations/`: tích hợp dịch vụ bên ngoài.
- `bootstrap/`: các bước khởi tạo hệ thống, load config, seed, init module.

### `backend/test/`
Kiểm thử backend.

### `backend/src/modules/*/`
Mỗi module nghiệp vụ nên tách theo chuẩn nội bộ:
- `controllers/`: nhận request, trả response.
- `services/`: xử lý nghiệp vụ.
- `dtos/`: dữ liệu vào/ra.
- `strategies/`: chiến lược xác thực hoặc xử lý riêng.
- `guards/`: bảo vệ quyền truy cập.
- `interfaces/`: contract kiểu dữ liệu.
- `constants/`: hằng số của module.
- `entities/`: entity riêng của module.
- `repositories/`: truy cập dữ liệu.
- `validators/`: kiểm tra dữ liệu đặc thù.
- `*.module.ts`: khai báo module NestJS.
- `README.md`: ghi chú riêng cho module.

---

## 4) Mô tả các module backend chi tiết

### `backend/src/modules/auth/`
Quản lý đăng ký, đăng nhập, refresh token, quên mật khẩu, reset mật khẩu, phân quyền truy cập.

### `backend/src/modules/users/`
Quản lý hồ sơ người dùng, trạng thái tài khoản, thông tin cá nhân, role liên quan.

### `backend/src/modules/learning/`
Quản lý lộ trình học, bài học, tiến độ, nội dung học, chương, module học tập.

### `backend/src/modules/practice/`
Quản lý bài luyện tập, quiz, bài tập thực hành, chấm điểm và kết quả luyện tập.

### `backend/src/modules/assessment/`
Quản lý kiểm tra năng lực, rubric, đề đánh giá, bài nộp và kết quả chấm.

### `backend/src/modules/projects/`
Quản lý dự án nhóm/cá nhân, thành viên dự án, submission, review code.

### `backend/src/modules/portfolio/`
Quản lý portfolio cá nhân, template, generator, xuất hồ sơ năng lực.

### `backend/src/modules/career/`
Hỗ trợ CV, matching nghề nghiệp, phỏng vấn, định hướng lộ trình việc làm.

### `backend/src/modules/employer/`
Quản lý đăng tuyển, tìm ứng viên, shortlist, quy trình tuyển dụng của doanh nghiệp.

### `backend/src/modules/community/`
Quản lý bài đăng, bình luận, thảo luận, tương tác cộng đồng.

### `backend/src/modules/notifications/`
Gửi thông báo qua email, in-app, push notification và quản lý template nội dung.

### `backend/src/modules/ai/`
Tích hợp AI cho gợi ý học tập, đánh giá, hỗ trợ nội dung và các provider bên ngoài.

### `backend/src/modules/admin/`
Các nghiệp vụ quản trị hệ thống, duyệt nội dung, giám sát và cấu hình.

### `backend/src/modules/analytics/`
Thu thập và phân tích dữ liệu hệ thống, báo cáo hoạt động, dashboard số liệu.

---

## 5) `packages/` — Thư viện dùng chung

### `packages/`
Chứa các package dùng lại giữa nhiều app.

- `shared-types/`: kiểu dữ liệu dùng chung.
- `shared-ui/`: component UI dùng chung.
- `shared-utils/`: hàm tiện ích dùng chung.
- `eslint-config/`: cấu hình ESLint dùng chung.
- `tsconfig/`: cấu hình TypeScript dùng chung.
- `design-system/`: hệ thống design tokens, theme, component guideline.

---

## 6) `infrastructure/` — Hạ tầng triển khai

### `infrastructure/`
Chứa cấu hình hạ tầng cho build, deploy, giám sát và chạy production.

- `docker/`: Dockerfile cho từng thành phần.
  - `backend.Dockerfile`: build backend container.
  - `web.Dockerfile`: build web container.
  - `mobile.Dockerfile`: cấu hình build hỗ trợ mobile nếu cần.
- `nginx/`: cấu hình reverse proxy, static hosting.
- `terraform/`: hạ tầng dưới dạng code.
- `kubernetes/`: manifest deploy trên K8s.
- `ci-cd/`: pipeline CI/CD.
  - `build.yml`: build pipeline.
  - `test.yml`: test pipeline.
  - `deploy.yml`: deploy pipeline.
- `monitoring/`: giám sát hệ thống.
  - `prometheus/`: thu thập metrics.
  - `grafana/`: dashboard trực quan.
  - `alerting/`: cảnh báo sự cố.

---

## 7) `docs/` — Tài liệu dự án

### `docs/`
Chứa toàn bộ tài liệu kỹ thuật và tài liệu sản phẩm.

- `architecture/`: mô tả kiến trúc tổng thể.
  - `system-overview.md`: tổng quan hệ thống.
  - `module-map.md`: bản đồ module.
  - `deployment.md`: mô tả triển khai.
  - `scalability.md`: khả năng mở rộng.
- `database/`: tài liệu dữ liệu.
  - `erd.md`: ERD.
  - `data-dictionary.md`: từ điển dữ liệu.
  - `naming-conventions.md`: quy tắc đặt tên dữ liệu.
- `api/`: tài liệu API theo từng domain.
  - `auth-dd.md`
  - `learning-dd.md`
  - `assessment-dd.md`
  - `portfolio-dd.md`
  - `employer-dd.md`
- `diagrams/`: lưu các loại biểu đồ.
  - `use-case/`
  - `activity/`
  - `sequence/`
  - `class/`
- `product/`: tài liệu sản phẩm.
  - `scope.md`: phạm vi sản phẩm.
  - `roadmap.md`: lộ trình phát triển.
  - `release-plan.md`: kế hoạch phát hành.
- `specs/`: đặc tả yêu cầu.
  - `requirements.md`: yêu cầu hệ thống.
  - `acceptance-criteria.md`: tiêu chí nghiệm thu.

---

## 8) `storage/` — Dữ liệu upload và file phát sinh

### `storage/`
Lưu file do người dùng tải lên, file xuất ra và file tạm.

- `uploads/`: toàn bộ file upload.
  - `avatars/`: ảnh đại diện.
  - `portfolios/`: file portfolio.
  - `resumes/`: CV, resume.
  - `project-files/`: file dự án.
  - `certificates/`: chứng chỉ.
- `exports/`: file xuất ra từ hệ thống.
- `imports/`: file nhập vào hệ thống.
- `temp/`: file tạm thời, xóa định kỳ.

---

## 9) `scripts/` — Script vận hành

### `scripts/`
Chứa script hỗ trợ vận hành, seed dữ liệu, backup/restore và dọn dẹp.

- `seed-admin.sh`: tạo tài khoản admin ban đầu.
- `seed-demo-data.sh`: nạp dữ liệu demo.
- `backup-db.sh`: sao lưu database.
- `restore-db.sh`: phục hồi database.
- `cleanup-temp.sh`: dọn file tạm.

---

## 10) `tests/` — Kiểm thử cấp dự án

### `tests/`
Chứa hệ thống test độc lập với từng app hoặc module.

- `unit/`: test đơn vị.
- `integration/`: test tích hợp.
- `e2e/`: test end-to-end.
- `fixtures/`: dữ liệu mẫu cho test.
- `mocks/`: đối tượng giả lập.
- `performance/`: test hiệu năng.

---

## 11) `deployment/` — Tài nguyên triển khai

### `deployment/`
Chứa các file triển khai thực tế cho môi trường dev, staging, production nếu cần thêm ngoài `infrastructure/`.

---

## 12) `.github/` — Tự động hóa GitHub

### `.github/`
Chứa workflow, issue template, pull request template, automation của GitHub.

---

## 13) Mô tả ngắn theo hướng sử dụng thực tế

- `apps/`: lớp giao diện và trải nghiệm người dùng.
- `backend/`: toàn bộ xử lý nghiệp vụ và API.
- `packages/`: phần dùng chung để giảm trùng lặp.
- `infrastructure/`: dựng môi trường và triển khai.
- `docs/`: mô tả và chuẩn hóa hệ thống.
- `storage/`: nơi lưu file.
- `scripts/`: tự động hóa công việc vận hành.
- `tests/`: hệ thống kiểm thử.
- `deployment/`: tài nguyên triển khai bổ sung.
- `.github/`: pipeline và tự động hóa repo.

---

## 14) Kết luận

Cấu trúc này được thiết kế để:
- dễ tách module,
- dễ mở rộng từ MVP sang hệ sinh thái lớn,
- dễ phân quyền team,
- dễ bảo trì và tái sử dụng code,
- phù hợp cho mô hình monorepo dài hạn.

