# Study2Work Business Code & Debug Standard

Nguồn gốc: `Study2Work_BusinessCode_Debug.xlsx`.

Mục tiêu của bản MD này là giữ đủ dữ liệu, đồng thời sắp xếp lại để dễ đọc, dễ tra cứu và dễ dùng cho AI coding / dev coding.

## README

| Row | Col A | Col B |
|---|---|---|
| 1 | Study2Work - Business Code & Debug Standard |  |
| 2 | Generated At | 2026-06-03 10:36:48 |
| 4 | Mục tiêu |  |
| 5 | Chuẩn hóa business code, error code, trace log và debug flow cho hệ thống Study2Work (EdTech + HRTech). |  |
| 7 | Nguồn tham chiếu |  |
| 8 | Đề án hệ thống đào tạo & kết nối nhân sự IT thực chiến. |  |


## Business_Modules

| BusinessCode | Module | SubModule | Description | DebugPurpose | Priority | Owner |
|---|---|---|---|---|---|---|
| AUTH | Authentication | Login | Đăng nhập hệ thống | Debug login/auth flow | Critical | Backend |
| AUTH | Authentication | Register | Đăng ký tài khoản | Debug register flow | Critical | Backend |
| AUTH | Authentication | JWT | Token/JWT xử lý | Debug token issue | Critical | Backend |
| USER | User Management | Profile | Quản lý hồ sơ người dùng | Debug profile API | High | Backend |
| LEARN | Learning | Roadmap | Lộ trình học | Debug roadmap data | High | Backend |
| LEARN | Learning | Quiz | Quiz và bài tập | Debug submit answer | High | Backend |
| LEARN | Learning | Assignment | Assignment workflow | Debug assignment flow | High | Backend |
| PROJECT | Project | TeamProject | Project nhóm | Debug project collaboration | High | Backend |
| MENTOR | Mentor | Review | Mentor review | Debug mentor review | Medium | Backend |
| EMPLOYER | Employer | Recruitment | Tuyển dụng | Debug employer matching | High | Backend |
| PORTFOLIO | Portfolio | CVBuilder | CV Builder | Debug portfolio generation | Medium | Frontend |
| AI | AI Services | AITutor | AI tutor và review | Debug AI service | High | AI Team |
| NOTI | Notification | Email | Email notification | Debug mail queue | Medium | Backend |
| SYSTEM | System | Logging | System logging | Centralized debug tracking | Critical | DevOps |


## API_Business_Codes

| BusinessCode | APIName | HTTPMethod | Endpoint | Purpose | ExpectedLogKey | TraceExample |
|---|---|---|---|---|---|---|
| AUTH-LOGIN-001 | User Login | POST | /api/v1/auth/login | Xử lý đăng nhập | traceId,userId,status | AUTH-LOGIN-FAIL |
| AUTH-REGISTER-001 | User Register | POST | /api/v1/auth/register | Đăng ký tài khoản | traceId,email,status | REGISTER-DUPLICATE |
| USER-PROFILE-001 | Get Profile | GET | /api/v1/users/profile | Lấy profile user | traceId,userId | PROFILE-NOT-FOUND |
| LEARN-QUIZ-001 | Submit Quiz | POST | /api/v1/quiz/submit | Submit bài quiz | traceId,quizId,score | QUIZ-SUBMIT-ERROR |
| PROJECT-TEAM-001 | Create Team Project | POST | /api/v1/projects/team | Tạo project nhóm | traceId,projectId | PROJECT-CREATE-ERROR |
| EMPLOYER-MATCH-001 | Matching Candidate | GET | /api/v1/employer/match | Matching ứng viên | traceId,companyId | MATCHING-TIMEOUT |


## Error_Codes

| ErrorCode | Layer | Description | PossibleCause | RecommendedAction | Severity |
|---|---|---|---|---|---|
| E401 | AUTH | Unauthorized | JWT invalid/expired | Refresh token & re-login | Critical |
| E403 | AUTH | Forbidden | Permission denied | Check RBAC | High |
| E404 | API | Resource not found | Wrong ID/data missing | Check database | Medium |
| E409 | DATABASE | Duplicate data | Unique constraint | Validate input | Medium |
| E422 | VALIDATION | Validation failed | Payload invalid | Check request schema | Medium |
| E500 | SYSTEM | Internal server error | Unhandled exception | Check stacktrace | Critical |
| E502 | GATEWAY | Bad gateway | Service unavailable | Check microservice | High |
| E504 | TIMEOUT | Request timeout | Long processing | Optimize query/cache | High |


## Debug_Flow

| FlowCode | BusinessFlow | StepOrder | StepName | ExpectedBehavior | LogCheckpoint |
|---|---|---|---|---|---|
| FLOW-AUTH | User Login | 1 | Input Credentials | Validate payload | REQ_RECEIVED |
| FLOW-AUTH | User Login | 2 | Check User | Verify user exists | USER_FOUND |
| FLOW-AUTH | User Login | 3 | Verify Password | Compare hash | PASSWORD_OK |
| FLOW-AUTH | User Login | 4 | Generate JWT | Create token | JWT_CREATED |
| FLOW-AUTH | User Login | 5 | Return Response | HTTP 200 | LOGIN_SUCCESS |
| FLOW-QUIZ | Submit Quiz | 1 | Validate Quiz | Quiz exists | QUIZ_VALID |
| FLOW-QUIZ | Submit Quiz | 2 | Save Answer | Persist answers | ANSWER_SAVED |
| FLOW-QUIZ | Submit Quiz | 3 | Calculate Score | Generate score | SCORE_CALCULATED |


## Log_Convention

| LogLevel | Convention | Example | Usage |
|---|---|---|---|
| INFO | [MODULE]-[ACTION]-SUCCESS | AUTH-LOGIN-SUCCESS | Business success flow |
| WARN | [MODULE]-[ACTION]-WARNING | QUIZ-SUBMIT-WARNING | Non-blocking issue |
| ERROR | [MODULE]-[ACTION]-ERROR | PAYMENT-CREATE-ERROR | Critical business error |
| DEBUG | [MODULE]-[DETAIL]-TRACE | JWT-DECODE-TRACE | Internal debug trace |


## Trace_Standard

| Field | Type | Description | Mandatory |
|---|---|---|---|
| traceId | UUID | Unique request identifier | YES |
| userId | String | User identifier | YES |
| sessionId | String | Session identifier | Optional |
| moduleCode | String | Business module code | YES |
| apiCode | String | API business code | YES |
| timestamp | Datetime | Event timestamp | YES |
| deviceInfo | String | Client device/browser | Optional |
| ipAddress | String | Client IP | Optional |
