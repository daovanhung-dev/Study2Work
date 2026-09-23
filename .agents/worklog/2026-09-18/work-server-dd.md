---
task_id: "2026-09-18-work-server-dd"
date: "2026-09-18"
primary_task_type: "docs"
secondary_task_types: ["test"]
project_scopes: ["server-work"]
cross_scope_dependencies: ["contracts/openapi/work/legacy-web.openapi.json", "apps/work-client/web/src/shared/api/work.ts"]
status: "VERIFIED"
---

# Worklog: Source-backed DD cho toàn bộ Work Server API

## EXPECTED_BEHAVIOR

- Requirement: Tạo DD Markdown cho đúng 18 operation đang được đăng ký trong `apps/work-server/src/routes/api_routes.ts`, lưu tại `apps/work-server/docs/dd`, giữ nguyên cấu trúc/thứ tự của `createDD-markdown` template.
- Canonical contract/approved DD: dùng `operationId` từ `contracts/openapi/work/legacy-web.openapi.json`; loại endpoint chỉ có trong target `openapi.json`, service legacy và module chưa được router wire.

## CURRENT_BEHAVIOR

- Source/config: Route, handler, service, middleware JWT, Multer, response helper, Prisma schema/migration và Work Web client đã được đối chiếu cho từng operation.
- Runnable tests: Không có server integration test suite được check-in cho Work Server; đã chạy static DD validator, contract validator và context validator.
- Runtime wiring: 18 route hiện tại được wire; các service chat/messenger/notification/top và auth legacy không được đưa vào inventory runtime.

## SOURCE_TRACE

```text
api_routes.ts -> handler -> middleware/service -> Prisma query/mutation -> reply/jsonSafe -> DD request/response/error/data mapping
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Login alias | `loginStudent/loginBusiness` dùng `matkhau ?? password`; client và legacy contract dùng `password` | VERIFIED / DOCUMENTED | DD ghi nhận cả hai key và giữ source behavior hiện tại |
| Request validation | Một số constraint trong legacy OpenAPI không được source enforce trực tiếp | VERIFIED / DOCUMENTED | DD đánh dấu source-vs-contract drift, không tự thêm validation |
| Sensitive response fields | Một số full Prisma result có thể chứa `matkhau` | VERIFIED / DOCUMENTED | DD ghi nhận security exposure; không sửa runtime trong task docs |
| Transaction boundary | Mutation hiện không mở explicit Prisma transaction | VERIFIED / DOCUMENTED | DD ghi `N/A` theo source, không suy diễn atomicity |
| Target-only API | `contracts/openapi/work/openapi.json` có endpoint chưa được `api_routes.ts` wire | VERIFIED / EXCLUDED | Không tạo DD runtime cho endpoint chưa có source wiring |

## CHANGES

- Files changed: `apps/work-server/docs/dd/` gồm 18 API folders, 4 reports và `work-server-dd.zip`; worklog này.
- CONTEXT_UPDATES: Không thay đổi runtime source, route, schema hoặc contract.
- Context pages changed: Không thay đổi `.agents/` context pages; `context-manifest.json` đã được validator kiểm tra.
- Assumptions: Mọi API còn discrepancy giữ status `Draft — Needs Confirmation`; không ghi credential, JWT secret hay token thật.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `python3 scripts/generate_work_server_dd.py --replace` | Generated 18 API DD folders | VERIFIED |
| Static DD validator | `DD_STATIC_VALIDATION_OK folders=18 markdown=148` | VERIFIED |
| `deno run --allow-read --allow-env --allow-run scripts/validate-contracts.mjs` | `Contract validation passed.` | VERIFIED |
| `deno run --allow-read --allow-env --allow-run scripts/validate-agent-context.mjs` | `AGENT_CONTEXT_OK (.agents/context-manifest.json)` | VERIFIED |
| Work Server runtime integration test suite | No checked-in server test runner found | NOT_FOUND |

## HANDOFF

- Remaining blockers: Reviewer/approver confirmation và các câu hỏi contract/security trong `apps/work-server/docs/dd/OPEN_QUESTIONS.md`.
- Next owner/action: Review source discrepancies, đặc biệt `matkhau` exposure và chuẩn hóa password field; sau đó có thể chuyển DD từ Draft sang approved version.
