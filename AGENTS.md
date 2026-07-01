# Study2Work - AI Agent Guide

Study2Work trong repo này đang được chuẩn hóa cho phạm vi Study: học, thực hành, đánh giá, mentor, teamwork, AI học tập và quản trị nền tảng. `docs/BD/Study2Work_Study_BD_Codex_Ready.md` là nguồn nghiệp vụ chính cho Study; không mở rộng sang recruitment/employer/job/CV nếu chưa có BD/DD được phê duyệt riêng.

## Source Of Truth

1. Ưu tiên: BD đã phê duyệt -> DD đã phê duyệt -> ADR/decision đã chốt -> code hiện tại là bằng chứng triển khai, không tự động là nghiệp vụ đúng.
2. Khi tài liệu mâu thuẫn, ghi `CONFLICT` hoặc `OPEN_QUESTION`; không tự quyết business rule.
3. Không coding theo DD `DRAFT` hoặc `IN_REVIEW` nếu chưa có phê duyệt rõ ràng, trừ khi user yêu cầu prototype.

## Stack Và Trạng Thái Repo

- Repo hiện là skeleton monorepo: `apps/`, `backend/`, `packages/`, `docs/`, `tests/`, `deployment/`, `infrastructure/`.
- Repo có cấu trúc backend TypeScript/NestJS-like trống (`backend/src/modules/*`, `nest-cli.json`, `package.json` rỗng).
- BD Study canonical chọn Python 3.12+ + FastAPI + Pydantic v2, SQLAlchemy 2.0 + Alembic, PostgreSQL, Redis.
- `CONFLICT`: skeleton repo cũ có Career/Employer/Recruitment folders; BD Study yêu cầu không build employer, job, application, matching, shortlist, offer, CV builder, AI CV review, AI interview assistant.
- `OPEN_QUESTION`: chưa có ADR-001 trong repo để chốt FastAPI/Python ngoài BD.

## Commands

| Task | Command | Notes |
|---|---|---|
| Discover files | `rg --files` | Dùng trước khi mở file lớn. |
| Search docs/code | `rg "<keyword>" <path>` | Tìm theo module, feature, business code. |
| Build/test/lint/format | `OPEN_QUESTION` | Manifests/scripts hiện rỗng; không bịa command. |
| AGENTS line count | `(Get-Content AGENTS.md).Count` | Phải dưới 200 dòng. |

## Code Rules

- Chỉ sửa code sau khi xác định module, feature/function, actor, BD/DD nguồn, checklist, skill liên quan, file ảnh hưởng và test dự kiến.
- Không sửa ngoài phạm vi task nếu không có lý do kỹ thuật rõ ràng.
- Protected API phải kiểm tra auth, RBAC, ownership/scope, validation, state transition và trả response envelope chuẩn có `businessCode`, `timestamp`, `traceId`.
- Business logic không nằm trong route/controller; domain/application giữ invariant và state transition.
- Không log hoặc đưa vào docs secret, token, password, API key, OAuth secret, hidden tests hoặc dữ liệu nhạy cảm.
- Auto grading và AI/LLM phải async; không chạy untrusted code trong main API process.

## Documentation Rules

- Đọc context theo progressive disclosure; không đọc toàn bộ repo hoặc toàn bộ `docs/` mù quáng.
- Mỗi thay đổi phải truy được về BD/DD/checklist/worklog/issue.
- Trạng thái biến động nằm ở checklist/worklog, không nhồi vào `AGENTS.md`.
- Nếu thiết kế thay đổi, cập nhật DD changelog hoặc ghi `OPEN_QUESTION`.
- Không tạo checklist trùng module; cập nhật checklist hiện có.

## Docs Map

| File | When to read |
|---|---|
| `docs/agent/WORKFLOW.md` | Luồng bắt đầu phiên, trước/sau coding, worklog, skill, retrospective. |
| `docs/agent/CONTEXT_INDEX.md` | Chọn module, BD/DD, checklist, skill, worklog cần đọc. |
| `docs/agent/STATUS_MODEL.md` | Chuẩn trạng thái DD/coding/bug/test. |
| `docs/worklog/INDEX.md` | Chọn tối đa 10 worklog gần nhất và tối đa 5 worklog liên quan để đọc sâu. |
| `docs/checklists/<MODULE_CODE>.md` | Trạng thái module, bug/open question, evidence và next work. |
| `docs/BD/Study2Work_Study_BD_Codex_Ready.md` | Nguồn nghiệp vụ Study bắt buộc trước DD/coding/test. |
| `docs/DD/DD_Module_Creation_Guide_EN.md` | Khi tạo hoặc kiểm tra DD module. |
| `docs/DD/DD_Module_Template/` | Cấu trúc chuẩn DD module. |
| `docs/architecture/Study2Work_Domain_Model_Coding_Practice.md` | Domain model, aggregates, events, ownership. |
| `docs/architecture/Study2Work_BusinessCode_Debug.md` | BusinessCode, error/log/trace conventions. |
| `docs/diagrams/` | Use case/activity/ERD/sequence khi cần trace flow. |

## Required Workflow

- Trước phân tích/coding: đọc `AGENTS.md`, `docs/agent/CONTEXT_INDEX.md`, `docs/worklog/INDEX.md`; xác định module/feature/task type; đọc checklist và BD/DD/skill liên quan.
- Trước coding: lập plan ngắn theo dependency, liệt kê file dự kiến sửa và test cần chạy.
- Sau coding: chạy test/lint/build phù hợp, ghi evidence, tạo worklog mới, cập nhật `docs/worklog/INDEX.md`, checklist module và DD changelog nếu thiết kế đổi.
- Chi tiết bắt buộc: `docs/agent/WORKFLOW.md`.
