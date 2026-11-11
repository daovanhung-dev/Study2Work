---
task_id: "2026-11-10-study-web-api-service"
date: "2026-11-10"
primary_task_type: "coding"
secondary_task_types: ["docs"]
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["Study API `/api/v1` prefix and shared JSON response envelope"]
status: "PARTIAL"
---

# Worklog: Study Web API service dùng chung

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `node scripts/select-worklogs.mjs --type coding --limit 3`
- selector_result: `READY`; 93 worklog cùng loại; chọn và đọc đủ 3.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-09/init-study-angular.md`
    - carry_forward: Study Web là Angular 22 scaffold; giữ API nghiệp vụ và auth unwired; không tạo test target nếu task không yêu cầu.
  - path: `.agents/worklog/2026-10-26/implement-api74-admin-course-detail.md`
    - carry_forward: Recheck source hiện tại; phân biệt contract trực tiếp với fallback; DDL/fake tests không xác minh live schema.
  - path: `.agents/worklog/2026-10-26/implement-api75-admin-course-update.md`
    - carry_forward: Giữ query/client boundary theo scope; không tự thêm policy/API contract; validator nền có lỗi DB Admin ngoài scope.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Tạo HTTP service generic cho Study Web dùng Angular `HttpClient`/RxJS, hỗ trợ GET/POST/PUT/PATCH/DELETE, query/body/headers caller truyền, trả nguyên `ApiEnvelope<T>` và giữ lỗi `HttpErrorResponse`; dùng `/api/v1` cùng Angular dev proxy tới Study API tại `127.0.0.1:3003`. Không thêm feature, endpoint wrapper, token store hoặc automated tests.
- Canonical contract/approved DD: User-approved plan trong hội thoại; Study API `success_response()` envelope và `APIRouter(prefix="/api/v1")` trong source hiện tại.

## CURRENT_BEHAVIOR

- Source/config: `apps/study-client` có Angular 22 standalone scaffold; `app.config.ts` chỉ đăng ký browser error listener và router; chưa có HTTP provider/service/proxy. `apps/study-server/app/core/responses.py` trả `success`, `businessCode`, `message`, `data`, `meta`, `traceId`; API router prefix là `/api/v1`. Angular CLI builder hỗ trợ `serve.proxyConfig`.
- Runnable tests: Angular workspace không có test target; theo yêu cầu không thêm/chạy tests. Build được yêu cầu chạy sau sửa.
- Runtime wiring: Chưa có Study Web endpoint call, auth/token store hoặc deployment base URL được xác nhận. Local API CORS defaults không gồm Study Web origin; dùng same-origin dev proxy.

## SOURCE_TRACE

```text
Study Web caller -> StudyApiService -> Angular HttpClient -> `/api/v1` dev proxy -> Study API router -> JSON envelope; HTTP failures propagate as HttpErrorResponse
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Study API OpenAPI | `contracts/openapi/study/README.md` chỉ là placeholder; source xác nhận shared envelope và `/api/v1` prefix. | `SOURCE_BACKED_TRANSPORT_ONLY` | Không khai báo DTO/endpoint nghiệp vụ; response generic theo envelope hiện có. |
| Local CORS | Study Web chạy tại 4200; CORS example/default không bao gồm origin này; dev-server có proxyConfig. | `LOCAL_PROXY_REQUIRED` | Proxy same-origin tránh thay đổi CORS/server scope. |
| Production routing | Chưa có production API URL/deployment config được xác nhận. | `NOT_FOUND / OUT_OF_SCOPE` | Không hard-code production host; production phải route same-origin `/api/v1`. |

## CHANGES

- Files changed: `apps/study-client/src/app/app.config.ts`, `apps/study-client/src/app/core/http/api-envelope.ts`, `apps/study-client/src/app/core/http/study-api.service.ts`, `apps/study-client/src/app/core/.gitkeep` (removed), `apps/study-client/proxy.conf.json`, `apps/study-client/angular.json`, Study Web architecture/context pages, project architecture/dependencies pages, context map/manifest, and this worklog.
- CONTEXT_UPDATES: Đăng ký shared HTTP transport, local proxy, current generic envelope type và required source paths; giữ business feature API/auth ở trạng thái unwired.
- Context pages changed: `.agents/web-work/AGENTS.md`, `.agents/web-work/study/AGENTS.md`, `.agents/web-work/study/INDEX.md`, `.agents/context-map.md`, `.agents/project/architecture.md`, `.agents/project/dependencies.md`, `apps/study-client/gui/architech.md`, `.agents/context-manifest.json`.
- Assumptions: `request<T>` nhận path suffix dưới `/api/v1`; `HttpParams` dùng cho query; caller cung cấp `HttpHeaders`; service không tự parse/mapping endpoint-specific `data`.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| Worklog preflight | `READY`; 3 exact-type `coding` worklogs đã đọc; không thiếu. | VERIFIED |
| `git status --short` trước edit | Chỉ có untracked `.agents/worklog/2026-11-10/` từ task nạp context trước đó; không có source changes cần ghi đè. | VERIFIED |
| Source/config inspection | Angular CLI `serve.proxyConfig` supported; Study API source uses `/api/v1` and the six-field success envelope; Study Web has no existing HTTP service or feature call. | VERIFIED_STATIC |
| `npm run build` | Angular production build succeeds; initial bundle 210.46 kB raw (57.47 kB estimated transfer). | VERIFIED_BUILD |
| Angular dev server + root request | `npm start -- --host 127.0.0.1 --port 4200` starts with proxy config; `GET /` returns HTTP 200. | VERIFIED_LOCAL_SMOKE |
| Proxied API request | `GET /api/v1/categories` returns HTTP 502 and Vite logs `ECONNREFUSED 127.0.0.1:3003`; direct `GET http://127.0.0.1:3003/health/live` also cannot connect. Study API was not running, so response/error-envelope behavior could not be confirmed end-to-end. | BLOCKED_BACKEND_UNAVAILABLE |
| JSON config parse | `angular.json`, `proxy.conf.json`, and `.agents/context-manifest.json` parse successfully. | VERIFIED_STATIC |
| `git diff --check` | No whitespace errors in tracked diff. | VERIFIED |
| `node scripts/validate-agent-context.mjs` | Exit 1, `AGENT_CONTEXT_INVALID`, 83 baseline findings: missing DB Admin context/source/links, 33 orphan `create_dd_screen` resources, and stale source snapshots across server-study, server-work, web-work, Study Web, Work Web, mobile-work, and DB Admin. No new Study Web registry/link finding; Study Web remains snapshot-stale. | BASELINE_INVALID |
| Automated tests | Not added or run as specified in the plan; Study Web has no test target. | NOT_RUN_BY_SCOPE |

## HANDOFF

- Remaining blockers: Study API is unavailable locally for an end-to-end response check; production routing is unspecified; repository context validator remains invalid from unrelated baseline findings and stale snapshots.
- Next owner/action: Complete service/proxy/context update, run build and context validator, then record baseline findings.
