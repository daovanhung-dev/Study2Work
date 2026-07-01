# Kiến trúc tree hoàn chỉnh dự án Study2Work

> Mục tiêu: tổ chức toàn bộ hệ thống theo hướng **monorepo**, dễ mở rộng từ MVP sang Assessment và Career & Employer.

## 1) Cấu trúc tổng thể

```text
Study2Work/
├── apps/
│   ├── web-public/
│   ├── web-student/
│   ├── web-mentor/
│   ├── web-employer/
│   ├── web-admin/
│   └── mobile-app/
├── backend/
├── packages/
├── infrastructure/
├── docs/
├── tests/
├── scripts/
├── storage/
├── deployment/
├── .github/
├── .env.example
├── .gitignore
├── README.md
└── docker-compose.yml
```

---

## 2) Frontend applications

### 2.1 `apps/web-public/`
Dành cho landing page, giới thiệu sản phẩm, blog, SEO, workshop, nội dung cộng đồng.

```text
apps/web-public/
├── src/
│   ├── app/
│   ├── components/
│   ├── layouts/
│   ├── pages/
│   ├── sections/
│   ├── services/
│   ├── stores/
│   ├── utils/
│   └── assets/
├── public/
├── tests/
├── package.json
└── README.md
```

### 2.2 `apps/web-student/`
Dành cho học viên: học tập, làm bài, project, portfolio, CV, phỏng vấn.

```text
apps/web-student/
├── src/
│   ├── app/
│   ├── components/
│   ├── modules/
│   │   ├── dashboard/
│   │   ├── learning/
│   │   ├── practice/
│   │   ├── assessment/
│   │   ├── projects/
│   │   ├── portfolio/
│   │   ├── cv-builder/
│   │   ├── interview/
│   │   └── community/
│   ├── routes/
│   ├── services/
│   ├── stores/
│   ├── composables/
│   ├── utils/
│   └── assets/
├── tests/
├── package.json
└── README.md
```

### 2.3 `apps/web-mentor/`
Dành cho mentor: quản lý nhóm, chấm bài, review code, rubric, workshop.

```text
apps/web-mentor/
├── src/
│   ├── app/
│   ├── modules/
│   │   ├── dashboard/
│   │   ├── class-management/
│   │   ├── assignments/
│   │   ├── code-review/
│   │   ├── assessments/
│   │   ├── mentoring-sessions/
│   │   └── workshops/
│   ├── components/
│   ├── services/
│   ├── stores/
│   └── assets/
├── tests/
├── package.json
└── README.md
```

### 2.4 `apps/web-employer/`
Dành cho doanh nghiệp: đăng tuyển, xem talent pool, shortlist, liên hệ.

```text
apps/web-employer/
├── src/
│   ├── app/
│   ├── modules/
│   │   ├── company-profile/
│   │   ├── job-posts/
│   │   ├── candidate-search/
│   │   ├── candidate-profile/
│   │   ├── shortlist/
│   │   └── hiring-workflow/
│   ├── components/
│   ├── services/
│   ├── stores/
│   └── assets/
├── tests/
├── package.json
└── README.md
```

### 2.5 `apps/web-admin/`
Dành cho quản trị hệ thống.

```text
apps/web-admin/
├── src/
│   ├── app/
│   ├── modules/
│   │   ├── dashboard/
│   │   ├── user-management/
│   │   ├── role-permission/
│   │   ├── content-management/
│   │   ├── mentor-management/
│   │   ├── employer-management/
│   │   ├── assessment-management/
│   │   ├── report-analytics/
│   │   └── system-settings/
│   ├── components/
│   ├── services/
│   ├── stores/
│   └── assets/
├── tests/
├── package.json
└── README.md
```

### 2.6 `apps/mobile-app/`
Dành cho Flutter mobile app.

```text
apps/mobile-app/
├── lib/
│   ├── app/
│   ├── core/
│   │   ├── config/
│   │   ├── constants/
│   │   ├── theme/
│   │   ├── routes/
│   │   └── utils/
│   ├── features/
│   │   ├── auth/
│   │   ├── dashboard/
│   │   ├── learning/
│   │   ├── practice/
│   │   ├── assessment/
│   │   ├── portfolio/
│   │   ├── community/
│   │   └── profile/
│   ├── shared/
│   └── main.dart
├── test/
├── pubspec.yaml
└── README.md
```

---

## 3) Backend application

### 3.1 `backend/`
Backend nên chia theo **module nghiệp vụ**, không chia theo kỹ thuật rời rạc.

```text
backend/
├── src/
│   ├── main.ts
│   ├── app.module.ts
│   ├── config/
│   ├── common/
│   │   ├── constants/
│   │   ├── decorators/
│   │   ├── dto/
│   │   ├── enums/
│   │   ├── exceptions/
│   │   ├── filters/
│   │   ├── guards/
│   │   ├── interceptors/
│   │   ├── interfaces/
│   │   ├── pipes/
│   │   └── utils/
│   ├── database/
│   │   ├── migrations/
│   │   ├── seeds/
│   │   ├── entities/
│   │   └── repositories/
│   ├── modules/
│   │   ├── auth/
│   │   ├── users/
│   │   ├── learning/
│   │   ├── practice/
│   │   ├── assessment/
│   │   ├── projects/
│   │   ├── portfolio/
│   │   ├── career/
│   │   ├── employer/
│   │   ├── community/
│   │   ├── notifications/
│   │   ├── ai/
│   │   ├── admin/
│   │   └── analytics/
│   ├── events/
│   ├── jobs/
│   ├── integrations/
│   └── bootstrap/
├── test/
├── package.json
├── tsconfig.json
├── nest-cli.json
└── README.md
```

### 3.2 Cấu trúc chuẩn cho từng module backend

Ví dụ với một module:

```text
backend/src/modules/auth/
├── controllers/
│   └── auth.controller.ts
├── services/
│   └── auth.service.ts
├── dtos/
│   ├── login.dto.ts
│   ├── register.dto.ts
│   ├── refresh-token.dto.ts
│   └── reset-password.dto.ts
├── strategies/
│   ├── jwt.strategy.ts
│   └── local.strategy.ts
├── guards/
│   ├── jwt-auth.guard.ts
│   └── roles.guard.ts
├── interfaces/
├── constants/
├── entities/
│   └── session.entity.ts
├── repositories/
├── validators/
├── auth.module.ts
└── README.md
```

Áp dụng tương tự cho:

- `users/`
- `learning/`
- `practice/`
- `assessment/`
- `projects/`
- `portfolio/`
- `career/`
- `employer/`
- `community/`
- `notifications/`
- `ai/`
- `admin/`
- `analytics/`

---

## 4) Gợi ý tree chi tiết theo nghiệp vụ

### 4.1 Learning
```text
backend/src/modules/learning/
├── controllers/
├── services/
├── dtos/
├── entities/
├── repositories/
├── learning.module.ts
└── README.md
```

### 4.2 Practice
```text
backend/src/modules/practice/
├── controllers/
├── services/
├── dtos/
├── entities/
├── repositories/
├── practice.module.ts
└── README.md
```

### 4.3 Assessment
```text
backend/src/modules/assessment/
├── controllers/
├── services/
├── dtos/
├── entities/
├── rubric/
├── repositories/
├── assessment.module.ts
└── README.md
```

### 4.4 Projects
```text
backend/src/modules/projects/
├── controllers/
├── services/
├── dtos/
├── entities/
├── repositories/
├── project-members/
├── code-reviews/
├── submissions/
├── projects.module.ts
└── README.md
```

### 4.5 Portfolio
```text
backend/src/modules/portfolio/
├── controllers/
├── services/
├── dtos/
├── entities/
├── templates/
├── generators/
├── repositories/
├── portfolio.module.ts
└── README.md
```

### 4.6 Career
```text
backend/src/modules/career/
├── controllers/
├── services/
├── dtos/
├── entities/
├── resume/
├── interview/
├── matching/
├── repositories/
├── career.module.ts
└── README.md
```

### 4.7 Employer
```text
backend/src/modules/employer/
├── controllers/
├── services/
├── dtos/
├── entities/
├── job-posts/
├── shortlist/
├── candidate-search/
├── repositories/
├── employer.module.ts
└── README.md
```

### 4.8 AI
```text
backend/src/modules/ai/
├── controllers/
├── services/
├── dtos/
├── prompts/
├── providers/
├── adapters/
├── repositories/
├── ai.module.ts
└── README.md
```

### 4.9 Notifications
```text
backend/src/modules/notifications/
├── controllers/
├── services/
├── dtos/
├── channels/
│   ├── email/
│   ├── in-app/
│   └── push/
├── templates/
├── repositories/
├── notifications.module.ts
└── README.md
```

---

## 5) Packages dùng chung

```text
packages/
├── shared-types/
├── shared-ui/
├── shared-utils/
├── eslint-config/
├── tsconfig/
└── design-system/
```

---

## 6) Infrastructure

```text
infrastructure/
├── docker/
│   ├── backend.Dockerfile
│   ├── web.Dockerfile
│   └── mobile.Dockerfile
├── nginx/
├── terraform/
├── kubernetes/
├── ci-cd/
│   ├── build.yml
│   ├── test.yml
│   └── deploy.yml
└── monitoring/
    ├── prometheus/
    ├── grafana/
    └── alerting/
```

---

## 7) Tài liệu dự án

```text
docs/
├── architecture/
│   ├── system-overview.md
│   ├── module-map.md
│   ├── deployment.md
│   └── scalability.md
├── database/
│   ├── erd.md
│   ├── data-dictionary.md
│   └── naming-conventions.md
├── api/
│   ├── auth-dd.md
│   ├── learning-dd.md
│   ├── assessment-dd.md
│   ├── portfolio-dd.md
│   └── employer-dd.md
├── diagrams/
│   ├── use-case/
│   ├── activity/
│   ├── sequence/
│   └── class/
├── product/
│   ├── scope.md
│   ├── roadmap.md
│   └── release-plan.md
└── specs/
    ├── requirements.md
    └── acceptance-criteria.md
```

---

## 8) Database / storage / seed

```text
storage/
├── uploads/
│   ├── avatars/
│   ├── portfolios/
│   ├── resumes/
│   ├── project-files/
│   └── certificates/
├── exports/
├── imports/
└── temp/
```

```text
scripts/
├── seed-admin.sh
├── seed-demo-data.sh
├── backup-db.sh
├── restore-db.sh
└── cleanup-temp.sh
```

---

## 9) Test structure

```text
tests/
├── unit/
├── integration/
├── e2e/
├── fixtures/
├── mocks/
└── performance/
```

---

## 10) Các file gốc nên có ở root

```text
README.md
LICENSE
CHANGELOG.md
CONTRIBUTING.md
docker-compose.yml
.env.example
.gitignore
.editorconfig
prettier.config.js
eslint.config.js
```

---

## 11) Gợi ý cách phát triển thực tế

### Phase 1 - MVP
- Auth
- Learning path
- Video / bài tập / quiz
- Dashboard học viên
- Mentor cơ bản
- Cộng đồng học tập

### Phase 2 - Practice & Assessment
- Assignment nâng cao
- Team project
- Review code
- Skill matrix
- Mentor workflow

### Phase 3 - Career & Employer
- Portfolio builder
- CV builder
- Hồ sơ năng lực
- Dashboard doanh nghiệp
- Matching ứng viên
- Tuyển thực tập / fresher

---

## 12) Gợi ý đặt chuẩn tên thư mục

- Folder: `kebab-case`
- File service/controller/module: `*.service.ts`, `*.controller.ts`, `*.module.ts`
- DTO: `*.dto.ts`
- Entity: `*.entity.ts`
- Guard: `*.guard.ts`
- Interceptor: `*.interceptor.ts`
- Pipe: `*.pipe.ts`

---

## 13) Kết luận

Tree này phù hợp để bạn dùng làm **khung source code thật**, vừa đủ chặt để quản lý, vừa đủ rộng để mở rộng từ MVP sang hệ sinh thái EdTech + HRTech. Nó bám sát các nhóm chức năng cốt lõi của hệ thống: học tập, thực hành, đánh giá năng lực, portfolio, kết nối doanh nghiệp và AI hỗ trợ.

