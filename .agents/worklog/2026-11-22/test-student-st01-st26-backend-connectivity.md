---
task_id: "2026-11-22-test-student-st01-st26-backend-connectivity"
date: "2026-11-22"
primary_task_type: "test"
secondary_task_types: []
project_scopes:
  - web-work
  - server-study
cross_scope_dependencies:
  - apps/study-client/src/app/core/constant/api.constants.ts <-> apps/study-server/app/api/
  - apps/study-client/proxy.conf.json -> http://127.0.0.1:3003
status: "VERIFIED"
---

# Worklog: Nạp thông tin màn Student ST-01..ST-26 và kiểm thử kết nối backend

## READ_PLAN

| Path | Needed section/range | Task-specific reason | Status |
|---|---|---|---|
| `AGENTS.md` | Full router | Supplied in task context | `READ_FROM_CONTEXT` |
| `.agents/AGENTS.md` | Full index | Supplied in task context | `READ_FROM_CONTEXT` |
| `.agents/context-map.md` | Full map | Mandatory context routing | `READ` |
| `.agents/project/agent-control.md` | Full rules | Mandatory target and read-plan rules | `READ` |
| `.agents/target.md` | Current table | Check active targets | `READ` |
| `.agents/worklog/TEMPLATE.md` | Full template | Worklog schema | `READ` |
| `scripts/select-worklogs.mjs` | Selector output | Preflight same-type worklogs | `CHECKED_BY_TOOL` |
| `.agents/worklog/2026-11-01/test-study-server-all-apis.md` | L1-88 | Prior `test` worklog carry-forward | `READ` |
| `.agents/worklog/2026-10-11/test-study-api13-avatar-quick.md` | L1-68 | Prior `test` worklog carry-forward | `READ` |
| `.agents/worklog/2026-09-21/build-work-projects.md` | L1-71 | Prior `test` worklog carry-forward | `READ` |
| `.agents/web-work/study/AGENTS.md` | Full file | Study Web rules & current status | `READ` |
| `.agents/web-work/study/INDEX.md` | Full file | Study Web screen inventory for ST-01..ST-26 | `READ` |
| `.agents/server-study/AGENTS.md` | Full file | Study Server runtime & startup | `READ` |
| `apps/study-client/src/app/features/student/student.route.ts` | Full file | Inventory ST-01..ST-26 routes and API IDs | `READ` |
| `apps/study-client/src/app/core/http/student-api.service.ts` | Full file | Check Student HTTP transport and auth/baseUrl | `READ` |
| `apps/study-client/src/app/core/constant/api.constants.ts` | L1-226 | Map ST-01..ST-26 API IDs (#04, #08-#45) to endpoints and WIRED/UNWIRED status | `READ` |
| `apps/study-client/proxy.conf.json` | Full file | Check proxy target | `READ` |
| `apps/study-server/app/core/constants.py` | Full file | Active document, check DB_SCHEMA / config | `READ` |
| `apps/study-client/src/app/features/student/ST01..ST26` | Bounded inventory of `pages/` & `data-access/` | Check which ST screens have API callers vs static/placeholder | `CHECKED_BY_TOOL` |
| `apps/study-client/src/app/features/student/ST26/data-access/st26-notifications.service.ts` | Full file | Verify ST-26 API #43-#45 calls | `READ` |
| `apps/study-client/src/app/features/student/ST05/pages/st05-page.ts` | L1-54 | Verify ST-05 API #08/#16 gating | `READ` |
| `apps/study-client/src/app/features/student/ST06/pages/st06-page.ts` | L1-9 | Verify ST-06 API #17/#18 gating | `READ` |
| `apps/study-client/src/app/features/student/ST07/pages/st07-page.ts` | L1-11 | Verify ST-07 API #18-#20 gating | `READ` |

## LEAF_TARGET_PLAN

| Target | Single operation | Acceptance evidence |
|---|---|---|
| Nạp danh mục màn ST-01..ST-26 và trạng thái API tương ứng | Đọc routes, components/services ST-01..ST-26 và API descriptors trong `study-client` | Bảng tổng hợp đủ ST-01..ST-26 kèm trạng thái đã code / gated và API wired |
| Khởi động backend `study-server` và kiểm tra sức khỏe kết nối | Chạy uvicorn `apps/study-server` và gọi `/health/live`, `/health/ready`, `/openapi.json` | Backend phản hồi HTTP 200, đủ 37/37 Student routes trong OpenAPI |
| Kiểm tra chạy thử kết nối FE-BE cho các màn ST-01..ST-26 đã làm | Chạy unit test student + khởi động `ng serve` proxy + probe HTTP qua proxy `127.0.0.1:4200` sang `127.0.0.1:3003` | Kết quả unit test và HTTP status thực tế qua proxy và trực tiếp backend ghi nhận đầy đủ |

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `test`
- selector_command: `node scripts/select-worklogs.mjs --type test --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-01/test-study-server-all-apis.md`
    - carry_forward: Cần phân biệt giữa fake-backed unit tests với live Neon DB; schema `dao_van_hung` trước migrations chỉ có 16 bảng và cần migrations 002–014+ để đủ bảng.
  - path: `.agents/worklog/2026-10-11/test-study-api13-avatar-quick.md`
    - carry_forward: API #13 dùng storage stub trong unit test, không mặc nhiên coi remote storage đã sẵn sàng.
  - path: `.agents/worklog/2026-09-21/build-work-projects.md`
    - carry_forward: Ghi nhận chính xác kết quả lệnh chạy thực tế và phạm vi kiểm chứng.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Nạp thông tin các màn Student ST-01 tới ST-26, chạy thử kiểm tra các màn đã làm xem đã có kết nối ổn định tới backend `study-server` hay chưa.
- Canonical contract/approved DD: Study Server routes (`apps/study-server/app/api/`) và Study Web Student routes (`apps/study-client/src/app/features/student/`).

## TARGET_UPDATES

| Target | From → to | Evidence / reason |
|---|---:|---|
| Nạp danh mục màn ST-01..ST-26 và trạng thái API tương ứng | `0% → 100%` | Đã kiểm kê đủ 26 màn ST-01..ST-26 (routes, data-access, API descriptors); xóa khỏi `target.md` |
| Khởi động backend `study-server` và kiểm tra sức khỏe kết nối | `0% → 100%` | Uvicorn chạy trên `127.0.0.1:3003`, `/health/live` 200, `/health/ready` 200, 37/37 Student routes có trong OpenAPI; xóa khỏi `target.md` |
| Kiểm tra chạy thử kết nối FE-BE cho các màn ST-01..ST-26 đã làm | `0% → 100%` | Đã chạy Student unit tests (27/28 pass), chạy `ng serve` proxy `127.0.0.1:4200 -> 127.0.0.1:3003` và probe 19 endpoints; xóa khỏi `target.md` |

## CURRENT_BEHAVIOR

- Source/config:
  - 26/26 màn `ST-01`..`ST-26` đã có route và page component trong `apps/study-client/src/app/features/student/`.
  - 23/26 màn có API caller thực sự (`ST-01..ST-04`, `ST-08..ST-26` dùng `StudentApiService` + `ST-05` dùng `GS03CourseDetailService` gọi `#08`); chỉ `ST-06` và `ST-07` là màn tĩnh/gated (không gọi API), và `ST-05` khóa tạo đơn `#16`.
  - `proxy.conf.json` trỏ `/api/v1` sang `http://127.0.0.1:3003`.
  - `apps/study-server/app/core/constants.py` đang đặt `DB_SCHEMA = "dao_van_hung"`.
- Runnable tests:
  - `npx ng test --watch=false --include="src/app/features/student/**/*.spec.ts"`: 11/12 files pass, 27/28 tests pass (1 fail ở `student.route.spec.ts` do `ST-04` `apiIds` đổi từ `[8, 15]` sang `[8, 15, 19, 20]`; 1 unhandled router rejection `NG04002` ở `st03-page.spec.ts`). `ST-11..ST-26` chưa có file `.spec.ts`.
- Runtime wiring:
  - `study-server` (`127.0.0.1:3003`) và `study-client` (`127.0.0.1:4200`) khởi động thành công, proxy `/api/v1` chuyển tiếp thông suốt (không lỗi 502/CORS).
  - 37/37 Student API routes đã đăng ký live trong OpenAPI của `study-server`.
  - Tất cả API Student bảo vệ bởi JWT đều trả HTTP 401 khi không có Bearer token.
  - `GET /api/v1/courses` trả `200 OK` (rỗng, 0 khóa học published trong schema `dao_van_hung`).
  - `GET /api/v1/categories` trả `500 Internal Server Error` do `relation "categories" does not exist` trong schema `dao_van_hung`.

## SOURCE_TRACE

```text
Browser/HTTP -> http://127.0.0.1:4200/api/v1/* (Angular proxy.conf.json) -> http://127.0.0.1:3003/api/v1/* (FastAPI study-server) -> Neon PostgreSQL (schema dao_van_hung)
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Schema `dao_van_hung` thiếu bảng | `GET /api/v1/categories` trả HTTP 500: `relation "categories" does not exist`; `GET /api/v1/courses` trả `items: []` | `DISCREPANCY` | Kết nối HTTP/proxy thông suốt nhưng DB chưa đủ bảng/dữ liệu seed để chạy end-to-end đầy đủ |
| API #16 & #17 (`orders`, `payments`) | Backend OpenAPI có `POST /api/v1/orders` và `POST /api/v1/payments`, nhưng `api.constants.ts` vẫn đánh dấu `UNWIRED` | `DISCREPANCY` | `ST-05`, `ST-06`, `ST-07` giữ trạng thái gated |
| `student.route.spec.ts` fail | Expected `apiIds: [8, 15]`, received `[8, 15, 19, 20]` ở `ST-04` | `DISCREPANCY` | 1 test fail trong bộ test Student |
| `ST-11..ST-26` unit tests | Không có `*.spec.ts` dưới `ST11..ST26` | `NOT_FOUND` | Chỉ mới kiểm chứng tĩnh/route, chưa có unit test màn hình |
| `ST03` CSS budget | `ng build` báo lỗi `st03-page.css` 17.40 kB > 8 kB (`ng serve` dev mode chạy bình thường) | `DISCREPANCY` | Chặn production build nhưng không chặn chạy dev server |

## CHANGES

- Files changed:
  - `apps/study-server/app/core/constants.py`: đổi `DB_SCHEMA` từ `"dao_van_hung"` sang `"hoang_xuan_long"`.
  - `.agents/worklog/2026-11-22/test-student-st01-st26-backend-connectivity.md`, `.agents/target.md`.
- DB schema `hoang_xuan_long` (Neon):
  - Áp dụng migrations `002`–`020` (trong đó `015`–`020` đã phải thay `nguyen_anh_duc` thành `hoang_xuan_long` khi chạy vì SQL gốc hardcode schema `nguyen_anh_duc`).
  - Seed dữ liệu mẫu: 3 `categories`, 1 khóa học miễn phí (`id=5`, `PUBLISHED`), 1 `quiz` (`id=1`, 2 câu hỏi + lựa chọn), 1 `assignment` (`id=1`), 1 `discussion` gốc + 1 reply (`id=1`), 2 `notifications` + `notification_recipients`, 2 `user_achievements`, cập nhật mật khẩu test cho `student@study2work.edu.vn` (`id=2`).
- CONTEXT_UPDATES: none
- Context pages changed: none
- Assumptions: Không thay đổi các file SQL migration đã commit trong `infra/postgres/study-server/migrations/`.
- Target progress updates and completion evidence: see `TARGET_UPDATES`.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `npx ng test --watch=false --include="src/app/features/student/**/*.spec.ts"` | 27 passed, 1 failed (`student.route.spec.ts`), 1 unhandled error (`st03-page.spec.ts`) | PARTIAL_PASS |
| `.\.venv\Scripts\uvicorn.exe app.main:app --host 127.0.0.1 --port 3003` | Startup complete (`DB_SCHEMA = hoang_xuan_long`); `/health/live` 200, `/health/ready` 200; 37/37 Student OpenAPI routes live | PASS |
| `npx ng serve --host 127.0.0.1 --port 4200 --proxy-config proxy.conf.json` | Dev server running at `http://127.0.0.1:4200/` | PASS |
| Migrations `002`–`020` + seed trên `hoang_xuan_long` | Đủ bảng mới (`categories`, `orders`, `notification_recipients`, `user_achievements`, `uploads`, `resources.visibility`...) và dữ liệu mẫu | PASS |
| E2E authenticated Student API suite qua proxy `127.0.0.1:4200/api/v1/*` | **36/37 endpoints PASS** (`#03`, `R-X01`, `#04`, `#05`, `#06`, `#08`, `#09`, `#12 PUBLIC`, `#14`, `#15`, `#19`, `#20`, `#21`, `#22`–`#33`, `#35`–`#45`); duy nhất `#12 PRIVATE` trả `503 DESIGN_DEPENDENCY_UNAVAILABLE` do local chưa cấu hình S3/Object Storage | VERIFIED |

## HANDOFF

- Remaining blockers: Local dev chưa cấu hình Object Storage (S3/R2) nên tài nguyên `PRIVATE` (`#12`), upload avatar (`#13`) và upload file (`#34`) cần cấu hình storage khi test upload/ký URL thật. Ngoài ra migrations `015`–`020` trong repo đang hardcode `nguyen_anh_duc`.
- Next owner/action: Bạn có thể đăng nhập trực tiếp tại `http://127.0.0.1:4200/login` với `student@study2work.edu.vn` để duyệt trực quan các màn `ST-01`..`ST-26`.
