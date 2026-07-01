# Study2Work (S2W) – UI Screen List Checklist

Tài liệu này liệt kê toàn bộ màn hình/view cần có cho hệ thống Study2Work, để bạn có thể làm dần theo area, module, mức ưu tiên và giai đoạn triển khai.

## Cách dùng
- `P0`: bắt buộc làm trước.
- `P1`: nên làm trong MVP hoặc ngay sau MVP.
- `P2`: giai đoạn mở rộng.
- `Status`: Not started / In progress / Done / Blocked.

## Tổng quan
- Tổng số màn hình/view: 210
- Khu vực chính: Public, Auth, System, Student, Mentor, Enterprise, Admin, Shared

## Danh sách màn hình

### Public (25)

#### Homepage

| ID | Screen / View | View Type | Purpose | User Role | Priority | Phase | Depends On | Related Screens | Notes |
|---|---|---|---|---|---|---|---|---|---|
| UI-001 | Home | Page | Product promise, journey, trust signals, key CTAs | Guest | P0 | MVP |  | About, Features, Courses, Paths, Jobs, Login | Main entry page |
| UI-002 | About | Page | Product story, mission, problem-solution fit | Guest | P2 | MVP |  | Home, Features, Roadmap |  |
| UI-003 | Features | Page | Core platform capabilities and role-based value | Guest | P1 | MVP |  | Home, Roadmap, Pricing |  |
| UI-004 | Roadmap | Page | Learning journey overview: Learn → Practice → Evaluate → Portfolio → Employer | Guest | P1 | MVP |  | Home, Learning Paths |  |


#### Learning

| ID | Screen / View | View Type | Purpose | User Role | Priority | Phase | Depends On | Related Screens | Notes |
|---|---|---|---|---|---|---|---|---|---|
| UI-005 | Courses Catalog | Page | Browse courses by path, skill, difficulty, duration | Guest | P1 | MVP |  | Course Detail, Learning Paths |  |
| UI-006 | Course Detail | Page | Course overview, modules, lessons, instructor, CTA | Guest | P1 | MVP |  | Courses Catalog, Login, Register |  |
| UI-007 | Learning Paths Catalog | Page | Browse structured learning paths by goal and level | Guest | P1 | MVP |  | Path Detail, Roadmap |  |
| UI-008 | Learning Path Detail | Page | Stages, prerequisites, outcomes, progress preview, enroll CTA | Guest | P1 | MVP |  | Learning Paths Catalog, Course Detail |  |


#### Mentor

| ID | Screen / View | View Type | Purpose | User Role | Priority | Phase | Depends On | Related Screens | Notes |
|---|---|---|---|---|---|---|---|---|---|
| UI-009 | Mentors List | Page | Browse mentors by specialization, rating, availability | Guest | P1 | MVP |  | Mentor Profile, Contact |  |
| UI-010 | Mentor Profile | Page | Mentor bio, expertise, reviews, session options | Guest | P1 | MVP |  | Mentors List, Login |  |


#### Portfolio

| ID | Screen / View | View Type | Purpose | User Role | Priority | Phase | Depends On | Related Screens | Notes |
|---|---|---|---|---|---|---|---|---|---|
| UI-011 | Projects Showcase | Page | Featured project showcase and real outcomes | Guest | P1 | MVP |  | Project Detail, Success Stories |  |
| UI-012 | Project Detail | Page | Project scope, stack, team roles, evidence, results | Guest | P1 | MVP |  | Projects Showcase, Learning Paths |  |


#### Career

| ID | Screen / View | View Type | Purpose | User Role | Priority | Phase | Depends On | Related Screens | Notes |
|---|---|---|---|---|---|---|---|---|---|
| UI-013 | Jobs Board | Page | Internship/fresher/remote jobs with search and filters | Guest | P0 | MVP |  | Job Detail, Login, Register |  |
| UI-014 | Job Detail | Page | Company summary, requirements, perks, process, apply CTA | Guest | P0 | MVP |  | Jobs Board, Apply Job, Login |  |


#### Proof

| ID | Screen / View | View Type | Purpose | User Role | Priority | Phase | Depends On | Related Screens | Notes |
|---|---|---|---|---|---|---|---|---|---|
| UI-015 | Success Stories | Page | Learner outcomes, testimonials, hiring outcomes | Guest | P2 | MVP |  | Story Detail, Home |  |
| UI-016 | Story Detail | Page | Detailed success story with timeline and evidence | Guest | P2 | Phase 2 |  | Success Stories |  |


#### Pricing

| ID | Screen / View | View Type | Purpose | User Role | Priority | Phase | Depends On | Related Screens | Notes |
|---|---|---|---|---|---|---|---|---|---|
| UI-017 | Pricing | Page | B2C, B2B, SaaS subscription tiers and comparison | Guest | P1 | MVP |  | Features, Contact |  |


#### Community

| ID | Screen / View | View Type | Purpose | User Role | Priority | Phase | Depends On | Related Screens | Notes |
|---|---|---|---|---|---|---|---|---|---|
| UI-018 | Community Feed | Page | Announcements, discussions, challenges, events | Guest | P2 | Phase 2 |  | Post Detail, Group Detail |  |


#### Blog

| ID | Screen / View | View Type | Purpose | User Role | Priority | Phase | Depends On | Related Screens | Notes |
|---|---|---|---|---|---|---|---|---|---|
| UI-019 | Blog Index | Page | Articles, guides, workshops, announcements | Guest | P2 | Phase 2 |  | Blog Post Detail |  |
| UI-020 | Blog Post Detail | Page | Single post reading view with author and related content | Guest | P2 | Phase 2 |  | Blog Index |  |


#### Support

| ID | Screen / View | View Type | Purpose | User Role | Priority | Phase | Depends On | Related Screens | Notes |
|---|---|---|---|---|---|---|---|---|---|
| UI-021 | FAQ | Page | Frequently asked questions and quick answers | Guest | P2 | MVP |  | Contact, Help Center |  |
| UI-022 | Contact | Page | Contact form, support channels, office info | Guest | P2 | MVP |  | FAQ, Careers |  |
| UI-023 | Careers | Page | Hiring page for Study2Work internal recruitment | Guest | P2 | Phase 2 |  | Contact |  |


#### Legal

| ID | Screen / View | View Type | Purpose | User Role | Priority | Phase | Depends On | Related Screens | Notes |
|---|---|---|---|---|---|---|---|---|---|
| UI-024 | Terms | Page | Terms of service and platform rules | Guest | P2 | MVP |  | Privacy |  |
| UI-025 | Privacy | Page | Privacy policy and data handling | Guest | P2 | MVP |  | Terms |  |


### Auth (5)

#### Authentication

| ID | Screen / View | View Type | Purpose | User Role | Priority | Phase | Depends On | Related Screens | Notes |
|---|---|---|---|---|---|---|---|---|---|
| UI-026 | Login | Page | Sign in with email/password and social login | Guest | P0 | MVP |  | Register, Forgot Password, Verify Email |  |
| UI-027 | Register | Page | Create student/mentor/enterprise account | Guest | P0 | MVP |  | Login, Verify Email |  |
| UI-028 | Forgot Password | Page | Request password reset link or code | Guest | P0 | MVP |  | Reset Password, Login |  |
| UI-029 | Reset Password | Page | Set a new password securely | Guest | P0 | MVP |  | Forgot Password, Login |  |
| UI-030 | Verify Email | Page | Confirm account email before access | Guest | P0 | MVP |  | Register, Login |  |


### System (3)

#### Error

| ID | Screen / View | View Type | Purpose | User Role | Priority | Phase | Depends On | Related Screens | Notes |
|---|---|---|---|---|---|---|---|---|---|
| UI-031 | 404 Not Found | Page | Missing route or deleted resource | Guest | P1 | MVP |  | Home, Login |  |
| UI-032 | 500 Server Error | Page | Unexpected server-side failure | Guest | P1 | MVP |  | Home, Support |  |
| UI-033 | Maintenance | Page | Planned downtime and service notice | Guest | P2 | Phase 2 |  | Home, Support |  |


### Student (86)

#### Dashboard

| ID | Screen / View | View Type | Purpose | User Role | Priority | Phase | Depends On | Related Screens | Notes |
|---|---|---|---|---|---|---|---|---|---|
| UI-034 | Student Dashboard | Page | Overview of progress, tasks, feedback, recommendations | Student | P0 | MVP |  | Notifications, Profile, Learning Progress |  |


#### Onboarding

| ID | Screen / View | View Type | Purpose | User Role | Priority | Phase | Depends On | Related Screens | Notes |
|---|---|---|---|---|---|---|---|---|---|
| UI-035 | Welcome | Page | First-time welcome and setup entry | Student | P0 | MVP |  | Career Goal, Skill Assessment |  |
| UI-036 | Career Goal | Page | Choose target role and learning objective | Student | P0 | MVP |  | Skill Assessment, Path Recommendation |  |
| UI-037 | Skill Assessment | Page | Initial skill diagnostic questionnaire | Student | P0 | MVP |  | Career Goal, Path Recommendation |  |
| UI-038 | Path Recommendation | Page | Suggested learning path and reasoning | Student | P0 | MVP |  | Roadmap Setup, Dashboard |  |
| UI-039 | Roadmap Setup | Page | Configure milestones, reminders, and goals | Student | P1 | MVP |  | Path Recommendation |  |
| UI-040 | Completion | Page | Success summary and start learning CTA | Student | P1 | MVP |  | Student Dashboard |  |


#### Profile

| ID | Screen / View | View Type | Purpose | User Role | Priority | Phase | Depends On | Related Screens | Notes |
|---|---|---|---|---|---|---|---|---|---|
| UI-041 | Profile Overview | Page | Personal info, skills, experience, links | Student | P0 | MVP |  | Profile Edit, CV Builder |  |
| UI-042 | Profile Edit | Page | Edit personal data, avatar, bio, links, visibility | Student | P0 | MVP |  | Profile Overview, Settings |  |


#### Learning

| ID | Screen / View | View Type | Purpose | User Role | Priority | Phase | Depends On | Related Screens | Notes |
|---|---|---|---|---|---|---|---|---|---|
| UI-043 | Learning Catalog | Page | All enrolled and suggested learning content | Student | P0 | MVP |  | Course Detail, Lesson Detail |  |
| UI-044 | Course Detail (Student) | Page | Student-specific course progress and continue CTA | Student | P0 | MVP |  | Learning Catalog, Lesson Detail |  |
| UI-045 | Lesson Detail | Page | Lesson content, outline, progress, notes, attachments | Student | P0 | MVP |  | Video Lesson, Reading Lesson, Quiz |  |
| UI-046 | Video Lesson | Page | Video player, transcript, bookmarks, discussion | Student | P0 | MVP |  | Lesson Detail |  |
| UI-047 | Reading Lesson | Page | Long-form content reading view with notes and bookmarks | Student | P1 | MVP |  | Lesson Detail |  |
| UI-048 | Live Session Detail | Page | Live class schedule, join link, materials, attendance | Student | P1 | Phase 2 |  | Lesson Detail, Attendance Tracking |  |
| UI-049 | Quiz | Page | Question flow, timer, answer state, submit controls | Student | P0 | MVP |  | Submission Result, Review Result |  |
| UI-050 | Assignment Detail | Page | Brief, rubric, deadline, attachments, submission instructions | Student | P0 | MVP |  | Submission Form, Review Result |  |
| UI-056 | Learning Progress | Page | Progress by course, path, lesson, and milestones | Student | P1 | MVP |  | Student Dashboard |  |


#### Practice

| ID | Screen / View | View Type | Purpose | User Role | Priority | Phase | Depends On | Related Screens | Notes |
|---|---|---|---|---|---|---|---|---|---|
| UI-051 | Lab Screen | Page | Hands-on exercise with starter files and output preview | Student | P1 | MVP |  | Practice Coding, Submission Form |  |
| UI-052 | Practice Coding | Page | Code editor, test cases, run/submit actions, console output | Student | P0 | MVP |  | Lab Screen, Submission Result |  |
| UI-053 | Submission Form | Page | Upload code/files or submit answer with confirmation | Student | P0 | MVP |  | Submission Result |  |
| UI-054 | Submission Result | Page | Score, failed tests, feedback summary, retry CTA | Student | P0 | MVP |  | Review Result, Assignment Detail |  |
| UI-055 | Review Result | Page | Mentor feedback, rubric, comments, improvements | Student | P0 | MVP |  | Submission Result |  |


#### Projects

| ID | Screen / View | View Type | Purpose | User Role | Priority | Phase | Depends On | Related Screens | Notes |
|---|---|---|---|---|---|---|---|---|---|
| UI-057 | Project Dashboard | Page | Active project, milestones, tasks, activity, files | Student | P0 | Phase 2 |  | Sprint Board, Kanban Board |  |
| UI-058 | Project List | Page | All projects with status, role, progress, and deadline | Student | P1 | Phase 2 |  | Project Detail |  |
| UI-059 | Project Detail | Page | Project overview, team, roles, files, timeline, reviews | Student | P0 | Phase 2 |  | Task Detail, Team Members |  |
| UI-060 | Sprint Board | Page | Sprint planning and sprint status tracking | Student | P1 | Phase 2 |  | Kanban Board, Backlog |  |
| UI-061 | Kanban Board | Page | Task drag-and-drop style columns | Student | P0 | Phase 2 |  | Task Detail, Issue Detail |  |
| UI-062 | Backlog | Page | Unplanned tasks and upcoming work items | Student | P1 | Phase 2 |  | Kanban Board |  |
| UI-063 | Task Detail | Page | Task description, assignee, checklist, comments, history | Student | P0 | Phase 2 |  | Issue Detail, Code Review |  |
| UI-064 | Issue Detail | Page | Bug/issue summary, reproduction steps, resolution thread | Student | P1 | Phase 2 |  | Task Detail |  |
| UI-065 | Pull Request Review | Page | Diff, review comments, approvals, status history | Student | P1 | Phase 2 |  | Code Review |  |
| UI-066 | Code Review | Page | Inline code feedback and review workflow | Student | P0 | Phase 2 |  | Pull Request Review |  |
| UI-067 | Team Members | Page | Team list, roles, contact, activity, availability | Student | P1 | Phase 2 |  | Project Detail |  |
| UI-068 | Meeting Notes | Page | Agenda, decisions, action items, attachments | Student | P2 | Phase 2 |  | Project Detail |  |
| UI-069 | Project Files | Page | Shared documents, source files, artifacts | Student | P1 | Phase 2 |  | Project Detail |  |
| UI-070 | Project Timeline | Page | Milestones, deadlines, progress over time | Student | P1 | Phase 2 |  | Project Detail |  |
| UI-071 | Project Analytics | Page | Task velocity, bottlenecks, completion rate | Student | P2 | Phase 2 |  | Project Dashboard |  |


#### Portfolio

| ID | Screen / View | View Type | Purpose | User Role | Priority | Phase | Depends On | Related Screens | Notes |
|---|---|---|---|---|---|---|---|---|---|
| UI-072 | Portfolio Builder | Page | Build public portfolio from projects, skills, and evidence | Student | P0 | MVP |  | Portfolio Preview, Public Portfolio Page |  |
| UI-073 | Portfolio Templates | Page | Choose layout/template for portfolio presentation | Student | P1 | MVP |  | Portfolio Builder |  |
| UI-074 | Portfolio Section Editor | Page | Edit sections: intro, projects, skills, achievements | Student | P0 | MVP |  | Portfolio Builder |  |
| UI-075 | Portfolio Preview | Page | Preview before publish | Student | P0 | MVP |  | Portfolio Builder, Public Portfolio Page |  |
| UI-076 | Public Portfolio Page | Page | Public-facing portfolio view with share link | Student | P0 | MVP |  | Portfolio Preview |  |
| UI-077 | Portfolio Version History | Page | Snapshot history and restore action | Student | P1 | Phase 2 |  | Portfolio Builder |  |


#### CV

| ID | Screen / View | View Type | Purpose | User Role | Priority | Phase | Depends On | Related Screens | Notes |
|---|---|---|---|---|---|---|---|---|---|
| UI-078 | CV Builder | Page | Structured CV creation and editing | Student | P0 | MVP |  | CV Templates, CV Preview, Export PDF |  |
| UI-079 | CV Templates | Page | Template selection for CV styles | Student | P1 | MVP |  | CV Builder |  |
| UI-080 | CV Section Editor | Page | Edit summary, education, experience, skills, projects | Student | P0 | MVP |  | CV Builder |  |
| UI-081 | CV Preview | Page | Printable CV preview panel | Student | P0 | MVP |  | Export PDF |  |
| UI-082 | CV Export PDF | Page | Export/download CV as PDF | Student | P0 | MVP |  | CV Preview |  |
| UI-083 | CV Version History | Page | CV snapshots and restore workflow | Student | P1 | Phase 2 |  | CV Builder |  |


#### Skills

| ID | Screen / View | View Type | Purpose | User Role | Priority | Phase | Depends On | Related Screens | Notes |
|---|---|---|---|---|---|---|---|---|---|
| UI-084 | Skill Dashboard | Page | Summary of skill levels, evidence, and gaps | Student | P0 | MVP |  | Skill Growth, Skill Radar |  |
| UI-085 | Skill Growth | Page | Skill progression over time | Student | P1 | MVP |  | Skill Dashboard |  |
| UI-086 | Skill Radar | Page | Radar chart view for skill profile | Student | P1 | MVP |  | Skill Dashboard |  |
| UI-087 | Skill Assessment Result | Page | Assessment outcome and recommendations | Student | P0 | MVP |  | Mentor Evaluation |  |
| UI-088 | Mentor Evaluation | Page | Mentor scoring and qualitative feedback | Student | P0 | MVP |  | Skill Assessment Result |  |
| UI-089 | Competency Map | Page | Map of required competencies for target role | Student | P1 | MVP |  | Skill Plan |  |
| UI-090 | Skill Plan | Page | Action plan for filling skill gaps | Student | P1 | MVP |  | Competency Map |  |


#### Interview

| ID | Screen / View | View Type | Purpose | User Role | Priority | Phase | Depends On | Related Screens | Notes |
|---|---|---|---|---|---|---|---|---|---|
| UI-091 | Mock Interview | Page | Practice interview session and prompts | Student | P1 | Phase 2 |  | AI Interview, Interview Report |  |
| UI-092 | AI Interview | Page | AI-driven interview simulation | Student | P1 | Phase 2 |  | Mock Interview |  |
| UI-093 | Interview Preparation | Page | Preparation checklist and practice resources | Student | P2 | Phase 2 |  | Mock Interview |  |
| UI-094 | Interview Report | Page | Results, strengths, gaps, and next steps | Student | P1 | Phase 2 |  | AI Interview |  |
| UI-095 | Interview History | Page | Past interview sessions and reports | Student | P2 | Phase 2 |  | Interview Report |  |


#### Career

| ID | Screen / View | View Type | Purpose | User Role | Priority | Phase | Depends On | Related Screens | Notes |
|---|---|---|---|---|---|---|---|---|---|
| UI-096 | Internship Board | Page | Internship opportunities with filters | Student | P0 | MVP |  | Job Detail, Apply Job |  |
| UI-097 | Fresher Jobs Board | Page | Entry-level jobs with filters and sorting | Student | P0 | MVP |  | Job Detail, Apply Job |  |
| UI-098 | Remote Jobs Board | Page | Remote/online job opportunities | Student | P1 | MVP |  | Job Detail |  |
| UI-099 | Job Detail (Student) | Page | Job overview and apply path for student users | Student | P0 | MVP |  | Apply Job, Saved Jobs |  |
| UI-100 | Apply Job | Page | Application form, CV selection, portfolio selection, confirmation | Student | P0 | MVP |  | Application Tracking |  |
| UI-101 | Application Tracking | Page | Application status timeline and stage updates | Student | P0 | MVP |  | Apply Job, Application History |  |
| UI-102 | Saved Jobs | Page | Saved/favorited jobs list | Student | P1 | MVP |  | Jobs Board |  |
| UI-103 | Recommended Jobs | Page | AI or rule-based job recommendations | Student | P1 | MVP |  | Jobs Board |  |
| UI-104 | Application History | Page | Past applications and outcomes | Student | P1 | MVP |  | Application Tracking |  |


#### Community

| ID | Screen / View | View Type | Purpose | User Role | Priority | Phase | Depends On | Related Screens | Notes |
|---|---|---|---|---|---|---|---|---|---|
| UI-105 | Community Feed | Page | Posts, announcements, Q&A, activities | Student | P2 | Phase 2 |  | Post Detail, Groups |  |
| UI-106 | Group Detail | Page | Group overview, members, posts, join actions | Student | P2 | Phase 2 |  | Community Feed |  |
| UI-107 | Discussion Detail | Page | Threaded discussion and replies | Student | P2 | Phase 2 |  | Community Feed |  |
| UI-108 | Event Detail | Page | Workshop/event detail and registration | Student | P2 | Phase 2 |  | Community Feed |  |
| UI-109 | Challenge Detail | Page | Coding/challenge detail with ranking | Student | P2 | Phase 2 |  | Leaderboard |  |
| UI-110 | Leaderboard | Page | Rankings by points, challenge, or progress | Student | P2 | Phase 2 |  | Challenge Detail |  |
| UI-111 | Post Detail | Page | Single post view with comments and reactions | Student | P2 | Phase 2 |  | Comment Thread |  |
| UI-112 | Comment Thread | Page | Nested comments and replies | Student | P2 | Phase 2 |  | Post Detail |  |


#### AI

| ID | Screen / View | View Type | Purpose | User Role | Priority | Phase | Depends On | Related Screens | Notes |
|---|---|---|---|---|---|---|---|---|---|
| UI-113 | AI Tutor | Page | Learning assistant, explanations, and hints | Student | P1 | Phase 2 |  | AI Chat Panel |  |
| UI-114 | AI Code Review | Page | AI-based code analysis and suggestions | Student | P1 | Phase 2 |  | Practice Coding, Code Review |  |
| UI-115 | AI Career Advisor | Page | Career guidance and roadmap advice | Student | P1 | Phase 2 |  | Recommended Jobs, Skill Plan |  |
| UI-116 | AI CV Review | Page | CV feedback and improvement suggestions | Student | P1 | Phase 2 |  | CV Builder |  |
| UI-117 | AI Portfolio Review | Page | Portfolio assessment and content recommendations | Student | P1 | Phase 2 |  | Portfolio Builder |  |
| UI-118 | AI Chat Panel | Page | Persistent assistant side panel or full-screen chat | Student | P1 | Phase 2 |  | AI Conversation History |  |
| UI-119 | AI Conversation History | Page | List of previous AI chats and requests | Student | P2 | Phase 2 |  | AI Chat Panel |  |


### Mentor (18)

#### Dashboard

| ID | Screen / View | View Type | Purpose | User Role | Priority | Phase | Depends On | Related Screens | Notes |
|---|---|---|---|---|---|---|---|---|---|
| UI-120 | Mentor Dashboard | Page | Review queue, student progress, sessions, workload | Mentor | P0 | MVP |  | Student Monitoring, Feedback Center |  |


#### Students

| ID | Screen / View | View Type | Purpose | User Role | Priority | Phase | Depends On | Related Screens | Notes |
|---|---|---|---|---|---|---|---|---|---|
| UI-121 | Student Monitoring | Page | Class/cohort progress and risk list | Mentor | P0 | MVP |  | Student Detail, Cohort Management |  |
| UI-122 | Student Detail | Page | Student profile, progress, submissions, feedback history | Mentor | P0 | MVP |  | Assignment Review, Skill Evaluation |  |


#### Classes

| ID | Screen / View | View Type | Purpose | User Role | Priority | Phase | Depends On | Related Screens | Notes |
|---|---|---|---|---|---|---|---|---|---|
| UI-123 | Class Management | Page | Class list, schedules, content, attendance | Mentor | P1 | Phase 2 |  | Cohort Management |  |
| UI-124 | Cohort Management | Page | Cohort setup, members, milestones, status | Mentor | P1 | Phase 2 |  | Class Management |  |


#### Review

| ID | Screen / View | View Type | Purpose | User Role | Priority | Phase | Depends On | Related Screens | Notes |
|---|---|---|---|---|---|---|---|---|---|
| UI-125 | Assignment Review | Page | Submission preview, rubric scoring, comments, approve/reject | Mentor | P0 | MVP |  | Review Result, Feedback Center |  |
| UI-126 | Code Review | Page | Diff view, inline comments, test feedback, approval | Mentor | P0 | MVP |  | Pull Request Review |  |
| UI-127 | Project Review | Page | Project evidence, milestones, team collaboration review | Mentor | P1 | Phase 2 |  | Project Detail |  |


#### Skills

| ID | Screen / View | View Type | Purpose | User Role | Priority | Phase | Depends On | Related Screens | Notes |
|---|---|---|---|---|---|---|---|---|---|
| UI-128 | Skill Evaluation | Page | Radar, criteria breakdown, evidence, recommendations | Mentor | P0 | MVP |  | Competency Map |  |


#### Assessment

| ID | Screen / View | View Type | Purpose | User Role | Priority | Phase | Depends On | Related Screens | Notes |
|---|---|---|---|---|---|---|---|---|---|
| UI-129 | Rubric Management | Page | Create and version scoring rubrics | Mentor | P1 | Phase 2 |  | Assignment Review |  |


#### Programs

| ID | Screen / View | View Type | Purpose | User Role | Priority | Phase | Depends On | Related Screens | Notes |
|---|---|---|---|---|---|---|---|---|---|
| UI-130 | Workshop Management | Page | Workshops, sessions, attendees, materials | Mentor | P1 | Phase 2 |  | Mentoring Sessions |  |
| UI-131 | Mentoring Sessions | Page | Session list, detail, notes, outcomes | Mentor | P1 | Phase 2 |  | Schedule Calendar |  |
| UI-132 | Schedule Calendar | Page | Mentor calendar and session bookings | Mentor | P1 | Phase 2 |  | Mentoring Sessions |  |
| UI-133 | Attendance Tracking | Page | Attendance, lateness, absence tracking | Mentor | P2 | Phase 2 |  | Class Management |  |


#### Feedback

| ID | Screen / View | View Type | Purpose | User Role | Priority | Phase | Depends On | Related Screens | Notes |
|---|---|---|---|---|---|---|---|---|---|
| UI-134 | Feedback Center | Page | Draft, published, pending feedback items | Mentor | P0 | MVP |  | Assignment Review, Student Detail |  |


#### Profile

| ID | Screen / View | View Type | Purpose | User Role | Priority | Phase | Depends On | Related Screens | Notes |
|---|---|---|---|---|---|---|---|---|---|
| UI-135 | Mentor Earnings | Page | Earnings summary if applicable | Mentor | P2 | Phase 2 |  | Mentor Analytics |  |
| UI-136 | Mentor Profile | Page | Public/private mentor profile management | Mentor | P1 | MVP |  | Public Mentor Profile |  |


#### Analytics

| ID | Screen / View | View Type | Purpose | User Role | Priority | Phase | Depends On | Related Screens | Notes |
|---|---|---|---|---|---|---|---|---|---|
| UI-137 | Mentor Analytics | Page | Review volume, turnaround, learner impact | Mentor | P2 | Phase 2 |  | Mentor Dashboard |  |


### Enterprise (18)

#### Dashboard

| ID | Screen / View | View Type | Purpose | User Role | Priority | Phase | Depends On | Related Screens | Notes |
|---|---|---|---|---|---|---|---|---|---|
| UI-138 | Company Dashboard | Page | Hiring summary, jobs, pipeline, metrics | Enterprise | P0 | MVP |  | Job Management, Candidate Search |  |


#### Company

| ID | Screen / View | View Type | Purpose | User Role | Priority | Phase | Depends On | Related Screens | Notes |
|---|---|---|---|---|---|---|---|---|---|
| UI-139 | Company Profile | Page | Brand, size, industry, benefits, verification | Enterprise | P0 | MVP |  | Employer Branding |  |


#### Jobs

| ID | Screen / View | View Type | Purpose | User Role | Priority | Phase | Depends On | Related Screens | Notes |
|---|---|---|---|---|---|---|---|---|---|
| UI-140 | Job Posting | Page | Create structured job form | Enterprise | P0 | MVP |  | Job Management, Apply Job |  |
| UI-141 | Job Posting Edit | Page | Edit and republish job details | Enterprise | P0 | MVP |  | Job Posting |  |
| UI-142 | Job Management | Page | Jobs list, status, edit, pause, close actions | Enterprise | P0 | MVP |  | Job Posting, Job Detail |  |
| UI-143 | Job Management Detail | Page | Single job analytics and applicants | Enterprise | P1 | MVP |  | Application Pipeline |  |


#### Talent

| ID | Screen / View | View Type | Purpose | User Role | Priority | Phase | Depends On | Related Screens | Notes |
|---|---|---|---|---|---|---|---|---|---|
| UI-144 | Candidate Search | Page | Search/filter candidates by skill, level, project, score | Enterprise | P0 | MVP |  | Talent Pool, Candidate Detail |  |
| UI-145 | Talent Pool | Page | Saved and shortlisted candidate cards | Enterprise | P0 | MVP |  | Candidate Search |  |
| UI-146 | Candidate Detail | Page | Profile, CV, portfolio, skills, evidence, timeline | Enterprise | P0 | MVP |  | Portfolio Viewer, Skill Matrix Viewer |  |
| UI-147 | Portfolio Viewer | Page | Public portfolio review layout | Enterprise | P0 | MVP |  | Candidate Detail |  |
| UI-148 | Skill Matrix Viewer | Page | Skill comparison against role requirements | Enterprise | P0 | MVP |  | Candidate Detail |  |


#### Hiring

| ID | Screen / View | View Type | Purpose | User Role | Priority | Phase | Depends On | Related Screens | Notes |
|---|---|---|---|---|---|---|---|---|---|
| UI-149 | Application Pipeline | Page | Kanban/status pipeline from applied to hired | Enterprise | P0 | MVP |  | Interview Scheduling |  |
| UI-150 | Interview Scheduling | Page | Calendar, stage, slots, meeting links, notes | Enterprise | P1 | MVP |  | Application Pipeline |  |
| UI-151 | Hiring Analytics | Page | Funnel, conversion, source quality, time-to-hire | Enterprise | P1 | Phase 2 |  | Recruitment Reports |  |
| UI-152 | Recruitment Reports | Page | Exportable hiring reports and insights | Enterprise | P2 | Phase 2 |  | Hiring Analytics |  |


#### Brand

| ID | Screen / View | View Type | Purpose | User Role | Priority | Phase | Depends On | Related Screens | Notes |
|---|---|---|---|---|---|---|---|---|---|
| UI-153 | Employer Branding | Page | Company story, culture, benefits, showcase | Enterprise | P2 | Phase 2 |  | Company Profile |  |


#### Billing

| ID | Screen / View | View Type | Purpose | User Role | Priority | Phase | Depends On | Related Screens | Notes |
|---|---|---|---|---|---|---|---|---|---|
| UI-154 | Subscription Management | Page | Plan selection, seats, limits, renewal | Enterprise | P1 | MVP |  | Billing |  |
| UI-155 | Billing | Page | Invoices, payment methods, usage, history | Enterprise | P1 | MVP |  | Subscription Management |  |


### Admin (24)

#### Dashboard

| ID | Screen / View | View Type | Purpose | User Role | Priority | Phase | Depends On | Related Screens | Notes |
|---|---|---|---|---|---|---|---|---|---|
| UI-156 | Admin Dashboard | Page | Platform KPIs, usage, moderation, health, revenue | Admin | P0 | MVP |  | User Management, Platform Health Monitoring |  |


#### Users

| ID | Screen / View | View Type | Purpose | User Role | Priority | Phase | Depends On | Related Screens | Notes |
|---|---|---|---|---|---|---|---|---|---|
| UI-157 | User Management | Page | Search, filter, suspend, role assignment | Admin | P0 | MVP |  | User Detail, Role Management |  |
| UI-158 | User Detail | Page | Single user summary, roles, activity, flags | Admin | P0 | MVP |  | User Management |  |


#### Access

| ID | Screen / View | View Type | Purpose | User Role | Priority | Phase | Depends On | Related Screens | Notes |
|---|---|---|---|---|---|---|---|---|---|
| UI-159 | Role Management | Page | Role definitions and role assignment matrix | Admin | P0 | MVP |  | Permission Management |  |
| UI-160 | Permission Management | Page | Permission matrix and toggles | Admin | P0 | MVP |  | Role Management |  |


#### Learning

| ID | Screen / View | View Type | Purpose | User Role | Priority | Phase | Depends On | Related Screens | Notes |
|---|---|---|---|---|---|---|---|---|---|
| UI-161 | Course Management | Page | Course list, publish, ordering, preview | Admin | P1 | MVP |  | Lesson Management |  |
| UI-162 | Lesson Management | Page | Lesson tree, content edit, publish states | Admin | P1 | MVP |  | Course Management |  |
| UI-163 | Quiz Management | Page | Quiz builder, question bank, versioning | Admin | P1 | MVP |  | Assignment Management |  |
| UI-164 | Assignment Management | Page | Assignment definitions, rubrics, status | Admin | P1 | MVP |  | Quiz Management |  |


#### Projects

| ID | Screen / View | View Type | Purpose | User Role | Priority | Phase | Depends On | Related Screens | Notes |
|---|---|---|---|---|---|---|---|---|---|
| UI-165 | Project Management | Page | Project registry, team oversight, flags | Admin | P2 | Phase 2 |  | User Management |  |


#### Skills

| ID | Screen / View | View Type | Purpose | User Role | Priority | Phase | Depends On | Related Screens | Notes |
|---|---|---|---|---|---|---|---|---|---|
| UI-166 | Skill Framework | Page | Skill taxonomy, levels, mappings, role requirements | Admin | P1 | MVP |  | Roadmap Management |  |
| UI-167 | Roadmap Management | Page | Learning stages, milestones, prerequisites | Admin | P1 | MVP |  | Skill Framework |  |


#### People

| ID | Screen / View | View Type | Purpose | User Role | Priority | Phase | Depends On | Related Screens | Notes |
|---|---|---|---|---|---|---|---|---|---|
| UI-168 | Mentor Management | Page | Mentor approval, workload, specialization, status | Admin | P1 | MVP |  | Mentor Profile |  |
| UI-169 | Enterprise Management | Page | Company verification, activity, quality review | Admin | P1 | MVP |  | Company Profile |  |


#### Jobs

| ID | Screen / View | View Type | Purpose | User Role | Priority | Phase | Depends On | Related Screens | Notes |
|---|---|---|---|---|---|---|---|---|---|
| UI-170 | Job Management | Page | Platform-wide job moderation and control | Admin | P1 | MVP |  | Job Posting |  |


#### Moderation

| ID | Screen / View | View Type | Purpose | User Role | Priority | Phase | Depends On | Related Screens | Notes |
|---|---|---|---|---|---|---|---|---|---|
| UI-171 | Community Moderation | Page | Reported posts, comments, actions, logs | Admin | P2 | Phase 2 |  | Content Moderation |  |
| UI-172 | Content Moderation | Page | Learning content and public content review | Admin | P2 | Phase 2 |  | Community Moderation |  |


#### AI

| ID | Screen / View | View Type | Purpose | User Role | Priority | Phase | Depends On | Related Screens | Notes |
|---|---|---|---|---|---|---|---|---|---|
| UI-173 | AI Configuration | Page | Prompts, feature flags, safety, policies | Admin | P1 | Phase 2 |  | AI Tutor, AI Chat Panel |  |


#### Notifications

| ID | Screen / View | View Type | Purpose | User Role | Priority | Phase | Depends On | Related Screens | Notes |
|---|---|---|---|---|---|---|---|---|---|
| UI-174 | Notification Center | Page | Templates, channels, delivery history | Admin | P1 | MVP |  | Reminder Center |  |


#### Audit

| ID | Screen / View | View Type | Purpose | User Role | Priority | Phase | Depends On | Related Screens | Notes |
|---|---|---|---|---|---|---|---|---|---|
| UI-175 | Audit Logs | Page | Immutable action trail and filters | Admin | P0 | MVP |  | User Management |  |


#### System

| ID | Screen / View | View Type | Purpose | User Role | Priority | Phase | Depends On | Related Screens | Notes |
|---|---|---|---|---|---|---|---|---|---|
| UI-176 | System Settings | Page | Key/value platform configuration | Admin | P1 | MVP |  | AI Configuration |  |
| UI-179 | Platform Health Monitoring | Page | Uptime, queues, errors, performance | Admin | P1 | MVP |  | Audit Logs |  |


#### Analytics

| ID | Screen / View | View Type | Purpose | User Role | Priority | Phase | Depends On | Related Screens | Notes |
|---|---|---|---|---|---|---|---|---|---|
| UI-177 | Revenue Analytics | Page | Income, plan usage, billing metrics | Admin | P2 | Phase 2 |  | Business Analytics |  |
| UI-178 | Business Analytics | Page | Growth, retention, funnel, cohorts | Admin | P2 | Phase 2 |  | Revenue Analytics |  |


### Shared (31)

#### Notifications

| ID | Screen / View | View Type | Purpose | User Role | Priority | Phase | Depends On | Related Screens | Notes |
|---|---|---|---|---|---|---|---|---|---|
| UI-180 | Notification Center | Page | Unified in-app notification list and filters | All Authenticated | P0 | MVP |  | Notification Detail, Reminder Center |  |
| UI-181 | Notification Detail | Page | Single notification with related action | All Authenticated | P1 | MVP |  | Notification Center |  |
| UI-182 | Reminder Center | Page | Scheduled reminders and due items | All Authenticated | P1 | MVP |  | Notification Center |  |
| UI-183 | In-App Notification Drawer | Drawer | Quick notification glance from topbar | All Authenticated | P1 | MVP |  | Notification Center |  |
| UI-184 | Email Notification Preview | Page | Email content preview and test send | Admin | P2 | Phase 2 |  | Notification Center |  |
| UI-185 | Push Notification Preview | Page | Push content preview | Admin | P2 | Phase 2 |  | Notification Center |  |


#### Settings

| ID | Screen / View | View Type | Purpose | User Role | Priority | Phase | Depends On | Related Screens | Notes |
|---|---|---|---|---|---|---|---|---|---|
| UI-186 | Profile Settings | Page | Basic profile and public info settings | All Authenticated | P0 | MVP |  | Account Settings, Profile Edit |  |
| UI-187 | Account Settings | Page | Email, password, login methods, account controls | All Authenticated | P0 | MVP |  | Security Settings |  |
| UI-188 | Security Settings | Page | Password, sessions, devices, login history | All Authenticated | P0 | MVP |  | 2FA Settings |  |
| UI-189 | 2FA Settings | Page | Two-factor authentication setup | All Authenticated | P1 | MVP |  | Security Settings |  |
| UI-190 | Privacy Settings | Page | Visibility, public data, discoverability | All Authenticated | P1 | MVP |  | Profile Settings |  |
| UI-191 | Language Settings | Page | Language and localization preferences | All Authenticated | P2 | MVP |  | Theme Settings |  |
| UI-192 | Theme Settings | Page | Light/dark mode and appearance controls | All Authenticated | P2 | MVP |  | Language Settings |  |
| UI-193 | Notification Preferences | Page | Channel and event-based notification toggles | All Authenticated | P0 | MVP |  | Notification Center |  |
| UI-194 | Connected Accounts | Page | Google/GitHub and external account connections | All Authenticated | P2 | Phase 2 |  | Security Settings |  |
| UI-195 | Billing Settings | Page | Billing settings and payment methods for paid plans | Enterprise | P1 | MVP |  | Subscription Settings |  |
| UI-196 | Subscription Settings | Page | Subscription plan, renewal, usage, limits | Enterprise | P1 | MVP |  | Billing Settings |  |
| UI-197 | Delete Account Confirmation | Modal | Account deletion warning and confirmation | All Authenticated | P0 | MVP |  | Account Settings |  |


#### Support

| ID | Screen / View | View Type | Purpose | User Role | Priority | Phase | Depends On | Related Screens | Notes |
|---|---|---|---|---|---|---|---|---|---|
| UI-198 | Help Center | Page | Self-service help and guidance | All Authenticated | P2 | Phase 2 |  | Support Contact |  |
| UI-199 | Support Contact | Page | Support form, channels, escalation | All Authenticated | P2 | Phase 2 |  | Help Center |  |


#### Modals

| ID | Screen / View | View Type | Purpose | User Role | Priority | Phase | Depends On | Related Screens | Notes |
|---|---|---|---|---|---|---|---|---|---|
| UI-200 | Publish Confirmation | Modal | Confirm publishing content, courses, jobs, or portfolio | All Authenticated | P1 | MVP |  | Course Management, Job Posting, Portfolio Builder |  |
| UI-201 | Delete Confirmation | Modal | Confirm destructive actions | All Authenticated | P0 | MVP |  | Delete Account Confirmation |  |
| UI-202 | Submit Confirmation | Modal | Confirm quiz, assignment, or code submission | Student | P0 | MVP |  | Quiz, Submission Form |  |
| UI-203 | Apply Job Confirmation | Modal | Final apply step before sending application | Student | P0 | MVP |  | Apply Job |  |
| UI-204 | Withdraw Application Confirmation | Modal | Confirm withdrawal from a job application | Student | P1 | MVP |  | Application Tracking |  |
| UI-205 | Shortlist Candidate | Modal | Confirm adding candidate to shortlist | Enterprise | P1 | MVP |  | Candidate Detail, Talent Pool |  |
| UI-206 | Schedule Interview | Modal | Create interview schedule and slot | Enterprise | P1 | MVP |  | Interview Scheduling |  |
| UI-207 | Review Submit | Modal | Submit mentor review or rubric result | Mentor | P0 | MVP |  | Assignment Review, Code Review |  |
| UI-208 | Report Content | Modal | Report community or content issues | All Authenticated | P2 | Phase 2 |  | Community Moderation |  |
| UI-209 | AI Settings | Modal | Adjust AI prompt / safety / context options | Admin | P2 | Phase 2 |  | AI Configuration |  |
| UI-210 | Logout Confirmation | Modal | Confirm sign-out action | All Authenticated | P1 | MVP |  | Account Settings |  |

## Gợi ý thứ tự triển khai
1. Public + Auth + System pages.
2. Student core: dashboard, onboarding, learning, practice, portfolio, CV, career.
3. Mentor core: dashboard, student monitoring, assignment review, code review, feedback.
4. Enterprise core: company dashboard, jobs, candidate search, pipeline, billing.
5. Admin core: user/role/permission, content, moderation, analytics, system settings.
6. Shared components: notifications, settings, modals, drawers, empty/loading/error states.

## Ghi chú
Tài liệu này bám theo cấu trúc monorepo và domain của Study2Work, ưu tiên luồng Learn → Practice → Evaluate → Build Portfolio → Connect Employer → Hire.