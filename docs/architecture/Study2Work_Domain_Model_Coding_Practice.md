# Study2Work Domain Model

**Dự án:** Study2Work  
**Định hướng:** EdTech + HRTech  
**Mục tiêu sản phẩm:** `Learn -> Practice -> Evaluate -> Build Portfolio -> Connect Employer`

Tài liệu này mô tả domain model theo hướng **code-first**, đủ rõ để:
- thiết kế database,
- viết API spec,
- sinh class/entity,
- phân module theo clean architecture,
- hỗ trợ team dev làm thực chiến.

---

## 1. Mục tiêu domain

Study2Work không phải chỉ là LMS, cũng không phải chỉ là platform tuyển dụng. Domain của hệ thống cần phản ánh đúng 3 trục giá trị:

1. **Đào tạo thực chiến**
   - có lộ trình học rõ ràng,
   - có bài tập, quiz, assignment,
   - có project nhóm,
   - có mentor review.

2. **Đánh giá năng lực**
   - không chỉ chấm điểm,
   - mà ghi nhận tiến bộ, skill matrix, rubric, feedback,
   - kết quả đánh giá phải dùng được cho tuyển dụng.

3. **Kết nối việc làm**
   - portfolio, CV, profile năng lực,
   - job post, matching, shortlist, interview, offer.

---

## 2. Phạm vi domain

### 2.1 Core domain
Đây là phần tạo ra giá trị khác biệt lớn nhất.

- **Practice & Assessment**
- **Career & Employer**

### 2.2 Supporting domain
- **Learning Journey**
- **Project & Teamwork**
- **AI Assistant**
- **Community & Engagement**

### 2.3 Generic domain
- **Identity & Access**
- **Profile**
- **Notification**
- **File Storage**
- **Admin & Platform**

---

## 3. Bounded contexts

| Bounded Context | Trách nhiệm chính | Aggregate root đề xuất |
|---|---|---|
| Identity & Access | đăng ký, đăng nhập, token, role, permission | `User`, `Session`, `Role` |
| Profile | thông tin cá nhân, hồ sơ học viên/mentor/doanh nghiệp | `Profile`, `StudentProfile`, `MentorProfile`, `EmployerProfile` |
| Learning Journey | lộ trình học, lesson, module, live session, bookmark | `LearningPath`, `Module`, `Lesson`, `LiveSession` |
| Practice & Assessment | quiz, assignment, submission, review, skill matrix | `Assignment`, `Quiz`, `Submission`, `SkillAssessment` |
| Project & Teamwork | project nhóm, task board, sprint, code review | `Project`, `Team`, `Task`, `Sprint` |
| Career & Employer | portfolio, CV, job, application, interview | `Portfolio`, `CV`, `JobPost`, `Application` |
| AI Assistant | AI roadmap, CV review, interview coach | `AIRequest`, `AIInsight`, `ReviewReport` |
| Admin & Platform | system settings, audit log, moderation, analytics | `SystemSetting`, `AuditLog`, `AnalyticsSnapshot` |

---

## 4. Domain principles

### 4.1 Nguyên tắc thiết kế
- **User là gốc danh tính**, không ôm toàn bộ nghiệp vụ.
- **Mỗi bounded context sở hữu dữ liệu của riêng nó**.
- **Dữ liệu tính toán** như score, match score, skill level nên là derived data.
- **Artifact quan trọng** như submission, review, portfolio snapshot cần versioning.
- **AI không được là nguồn dữ liệu chuẩn**, AI chỉ tạo gợi ý hoặc bản nháp.

### 4.2 Nguyên tắc triển khai
- Aggregate nhỏ, rõ ràng, dễ transaction.
- Tránh service god-object.
- Tránh join xuyên context trong code nghiệp vụ.
- Mọi dữ liệu nhạy cảm phải đi qua permission check.
- Tách command model và read model nếu cần.

---

## 5. Domain model theo từng context

## 5.1 Identity & Access

### Aggregate root
- `User`
- `Role`
- `Session`

### Entity / Value Object
- `Credential`
- `RefreshToken`
- `VerificationToken`
- `OAuthIdentity`
- `Permission`
- `UserRole`
- `PasswordResetToken`
- `EmailAddress`
- `PhoneNumber`

### Trách nhiệm
- đăng ký tài khoản,
- xác thực email/phone,
- đăng nhập,
- refresh token,
- phân quyền,
- khóa/mở tài khoản.

### Invariants
- email và phone phải unique,
- refresh token có thể revoke,
- user trạng thái phải hợp lệ: `PENDING`, `ACTIVE`, `SUSPENDED`, `DELETED`,
- password hash không bao giờ lưu plaintext.

---

## 5.2 Profile

### Aggregate root
- `Profile`

### Entity
- `StudentProfile`
- `MentorProfile`
- `EmployerProfile`
- `Education`
- `Experience`
- `SocialLink`
- `Skill`
- `UserSkill`

### Value Object
- `FullName`
- `DisplayName`
- `Location`
- `CareerGoal`
- `SkillLevel`

### Trách nhiệm
- lưu hồ sơ cá nhân,
- mô tả vai trò người dùng,
- chuẩn hóa thông tin public/private,
- lưu kỹ năng và định hướng nghề nghiệp.

### Invariants
- một user có thể có nhiều loại profile logic nhưng chỉ một identity chính,
- thông tin public phải tách khỏi internal profile,
- skill level phải theo enum hoặc normalized scale.

---

## 5.3 Learning Journey

### Aggregate root
- `LearningPath`
- `Module`
- `Lesson`
- `LiveSession`

### Entity
- `PathStage`
- `LessonContent`
- `LessonComment`
- `Bookmark`
- `LearningProgress`

### Value Object
- `PathProgress`
- `LessonOrder`
- `Visibility`
- `ContentType`

### Trách nhiệm
- quản lý lộ trình học,
- sắp xếp lesson theo thứ tự,
- quản lý video, tài liệu, bài học live,
- theo dõi tiến độ học,
- lưu bookmark và comment.

### Invariants
- lesson phải thuộc đúng module,
- progress phải phản ánh hành vi thật của user,
- content publish/draft phải rõ ràng,
- bookmark không được trùng cùng một user + lesson.

---

## 5.4 Practice & Assessment

### Aggregate root
- `Assignment`
- `Quiz`
- `Submission`
- `SkillAssessment`

### Entity
- `Question`
- `Choice`
- `SubmissionAnswer`
- `Rubric`
- `RubricCriterion`
- `Review`
- `Feedback`
- `SkillMatrix`
- `SkillLevel`
- `AssessmentHistory`

### Value Object
- `Score`
- `RubricScore`
- `AssessmentStatus`
- `SubmissionStatus`

### Trách nhiệm
- tạo quiz/assignment,
- nhận bài nộp,
- chấm tự động / chấm tay,
- review theo rubric,
- cập nhật skill matrix,
- lưu lịch sử năng lực.

### Invariants
- submission sau khi nộp phải bất biến hoặc versioned,
- rubric phải versioned để không phá dữ liệu cũ,
- skill level chỉ thay đổi khi có nguồn hợp lệ,
- điểm số không nên chỉnh trực tiếp nếu có event gốc.

### Đây là lõi thực chiến
Phần này nên được ưu tiên cao nhất vì nó biến hệ thống thành nền tảng “học để làm được việc”, không chỉ học lý thuyết.

---

## 5.5 Project & Teamwork

### Aggregate root
- `Project`
- `Team`
- `Sprint`
- `Task`

### Entity
- `TeamMember`
- `TaskComment`
- `TaskAttachment`
- `GitRepositoryLink`
- `PullRequestReview`
- `ProjectMilestone`
- `WorkLog`

### Value Object
- `TaskStatus`
- `Priority`
- `TeamRole`
- `SprintStatus`

### Trách nhiệm
- quản lý project thực tế,
- chia team,
- phân vai dev/tester/leader/reviewer,
- theo dõi task board,
- gắn repo Git,
- lưu review code.

### Invariants
- task phải có owner hoặc assignee rõ,
- team member có role cụ thể,
- trạng thái task phải đi theo workflow đã định,
- sprint chỉ nhận task thuộc đúng project.

---

## 5.6 Career & Employer

### Aggregate root
- `Portfolio`
- `CV`
- `JobPost`
- `Application`
- `Interview`

### Entity
- `PortfolioItem`
- `CVSection`
- `JobRequirement`
- `JobSkillRequirement`
- `Shortlist`
- `InterviewSchedule`
- `InterviewFeedback`
- `Offer`
- `CandidateSnapshot`
- `MatchScore`

### Value Object
- `ApplicationStatus`
- `JobType`
- `EmploymentType`
- `InterviewMode`
- `MatchLevel`

### Trách nhiệm
- xây portfolio và CV,
- đăng job/thực tập/fresher,
- matching ứng viên,
- shortlist,
- phỏng vấn,
- lưu kết quả tuyển dụng.

### Invariants
- application status phải theo state machine,
- employer chỉ xem được profile đã publish và đã được phép,
- match score là dữ liệu suy luận, không phải truth source,
- mỗi portfolio item nên gắn evidence thực tế như project/submission/review.

---

## 5.7 AI Assistant

### Aggregate root
- `AIRequest`
- `AIConversation`
- `ReviewReport`

### Entity
- `AIInsight`
- `RoadmapSuggestion`
- `CVReviewItem`
- `InterviewPracticeSession`
- `CodeExplanationRequest`

### Trách nhiệm
- gợi ý roadmap,
- review CV,
- hỗ trợ giải thích code,
- luyện phỏng vấn,
- tạo insight học tập.

### Invariants
- AI output chỉ là recommendation,
- luôn lưu input snapshot nếu cần audit,
- không để AI overwrite dữ liệu gốc,
- phải có cơ chế rate limit và logging.

---

## 5.8 Admin & Platform

### Aggregate root
- `SystemSetting`
- `AuditLog`
- `AnalyticsSnapshot`

### Entity
- `FeatureFlag`
- `ModerationCase`
- `NotificationTemplate`
- `ContentReport`

### Trách nhiệm
- quản trị hệ thống,
- cấu hình platform,
- theo dõi audit,
- kiểm soát nội dung,
- xem analytics.

### Invariants
- mọi hành động quản trị phải có audit log,
- settings nên dùng key/value typed,
- feature flag phải có môi trường áp dụng.

---

## 6. Domain events

Các event nên dùng để tách context và hỗ trợ event-driven flow:

- `UserRegistered`
- `EmailVerified`
- `LearningPathAssigned`
- `LessonCompleted`
- `AssignmentSubmitted`
- `SubmissionReviewed`
- `SkillLevelUpdated`
- `TeamCreated`
- `TaskAssigned`
- `ProjectReviewed`
- `PortfolioPublished`
- `JobApplied`
- `CandidateShortlisted`
- `InterviewScheduled`
- `AIReviewCompleted`
- `SystemSettingChanged`

### Quy tắc đặt tên
- dùng dạng quá khứ,
- chỉ mô tả việc đã xảy ra,
- không mô tả hành động của service.

---

## 7. Command / Query hướng thiết kế

### Command
- `RegisterUser`
- `LoginUser`
- `AssignLearningPath`
- `SubmitAssignment`
- `ReviewSubmission`
- `CreateProject`
- `JoinTeam`
- `PublishPortfolio`
- `ApplyJob`
- `ScheduleInterview`

### Query
- `GetStudentDashboard`
- `GetLearningProgress`
- `GetSkillMatrix`
- `GetPortfolioView`
- `SearchCandidates`
- `GetEmployerDashboard`

### Gợi ý
- Command thay đổi state.
- Query chỉ đọc dữ liệu.
- Nếu hệ thống lớn hơn, tách read model riêng cho dashboard, search, analytics.

---

## 8. Data ownership and consistency

### Quy tắc sở hữu dữ liệu
- `User` sở hữu identity.
- `Profile` sở hữu thông tin hiển thị.
- `Learning` sở hữu content và progress.
- `Practice` sở hữu submission và assessment.
- `Project` sở hữu team/task/review.
- `Career` sở hữu portfolio/job/application.
- `Admin` sở hữu setting/audit.

### Quy tắc consistency
- Trong một aggregate: **strong consistency**.
- Giữa các aggregate: **eventual consistency** là hợp lý hơn.
- Tránh transaction kéo dài qua nhiều context.
- Các chỉ số như progress, score, match score nên cập nhật qua event handler.

---

## 9. Đề xuất package structure

```text
study2work/
├── apps/
│   ├── web-public/
│   ├── web-student/
│   ├── web-mentor/
│   ├── web-employer/
│   ├── web-admin/
│   └── mobile-app/
├── services/
│   ├── auth-service/
│   ├── learning-service/
│   ├── practice-service/
│   ├── project-service/
│   ├── career-service/
│   ├── ai-service/
│   └── admin-service/
├── shared/
│   ├── domain/
│   ├── application/
│   ├── infrastructure/
│   └── contracts/
└── docs/
    ├── domain/
    ├── api/
    ├── erd/
    └── sequence/
```

### Nếu đi theo modular monolith
Mỗi module vẫn nên có:
- `domain`
- `application`
- `infrastructure`
- `presentation`

---

## 10. Mapping domain sang code

### Domain layer
- entity
- aggregate
- value object
- domain event
- domain service
- repository interface

### Application layer
- use case
- command handler
- query handler
- DTO
- mapper
- transaction orchestration

### Infrastructure layer
- repository implementation
- ORM model
- cache
- message broker
- email service
- object storage

### Presentation layer
- controller
- route
- validation
- response mapper
- auth guard

---

## 11. Validation rules cần chuẩn hóa

### Identity
- email format
- password policy
- OTP expiration
- refresh token rotation

### Learning
- lesson/module must exist
- content publish state
- progress ownership

### Practice
- submission deadline
- plagiarism / duplicate checks
- rubric validation
- score range validation

### Career
- job post status
- profile visibility
- application status transitions
- interview scheduling conflict

### Admin
- permission check
- audit required
- setting key whitelist

---

## 12. State machine gợi ý

### Application
`DRAFT -> APPLIED -> SHORTLISTED -> INTERVIEWING -> OFFERED -> HIRED`
or
`DRAFT -> APPLIED -> REJECTED`

### Submission
`DRAFT -> SUBMITTED -> IN_REVIEW -> GRADED -> ARCHIVED`

### Project task
`TODO -> IN_PROGRESS -> IN_REVIEW -> DONE`
or
`TODO -> BLOCKED -> IN_PROGRESS -> DONE`

### Lesson progress
`LOCKED -> AVAILABLE -> STARTED -> COMPLETED`

---

## 13. Read models nên có

- Student dashboard
- Mentor dashboard
- Employer dashboard
- Admin analytics
- Learning progress view
- Skill matrix view
- Search candidate view
- Portfolio public view

Read model nên tối ưu cho:
- filter,
- search,
- sort,
- pagination,
- dashboard KPI.

---

## 14. Business rules quan trọng nhất

1. **Học viên phải được đánh giá qua quá trình**, không chỉ qua bài test cuối.
2. **Skill matrix phải tích lũy từ nhiều nguồn**: bài tập, project, mentor review, lịch sử task.
3. **Portfolio phải có evidence thật**.
4. **Employer chỉ được tìm trên dữ liệu publish và hợp lệ**.
5. **AI là trợ lý**, không thay thế quyết định nghiệp vụ.
6. **Audit log bắt buộc cho hành động quản trị và tuyển dụng quan trọng**.
7. **Versioning bắt buộc** cho submission, rubric, portfolio snapshot và CV snapshot.

---

## 15. MVP domain scope khuyến nghị

Nếu làm thật và muốn ra sản phẩm nhanh, nên ưu tiên:

### Phase 1
- Identity & Access
- Profile
- Learning Journey cơ bản
- Practice & Assessment cơ bản
- Mentor review
- Student dashboard

### Phase 2
- Project & Teamwork
- Skill matrix
- Portfolio builder
- CV builder

### Phase 3
- Career & Employer
- Matching
- Interview workflow
- Employer dashboard

### Phase 4
- AI Assistant
- Analytics nâng cao
- Community features
- Automation / recommendations

---

## 16. Domain glossary

- **Student**: người học chính.
- **Mentor**: người review, hướng dẫn, đánh giá.
- **Employer**: doanh nghiệp tuyển dụng.
- **Learning Path**: lộ trình học.
- **Assignment**: bài tập có nộp.
- **Submission**: kết quả nộp bài.
- **Rubric**: tiêu chí chấm.
- **Skill Matrix**: ma trận năng lực.
- **Portfolio**: hồ sơ dự án/kết quả thực chiến.
- **Application**: hồ sơ ứng tuyển.
- **Match Score**: điểm phù hợp giữa ứng viên và job.

---

## 17. Kết luận

Domain của Study2Work nên được thiết kế xoay quanh **năng lực thực chiến**, không chỉ xoay quanh nội dung học. Trọng tâm của hệ thống là:
- học có lộ trình,
- làm có đánh giá,
- đánh giá có chuẩn,
- chuẩn đó phục vụ tuyển dụng.

Nếu triển khai đúng cấu trúc trên, hệ thống sẽ đủ nền tảng để phát triển thành:
- IT Academy,
- Talent Network,
- Hiring Platform,
- Skill Assessment System,
- AI-supported learning platform.

