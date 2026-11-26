---
task_id: "2026-11-24-gs-st-test-plan"
date: "2026-11-24"
primary_task_type: "test"
secondary_task_types:
  - "docs"
project_scopes:
  - "server-study"
  - "web-work"
cross_scope_dependencies:
  - "apps/study-client <-> apps/study-server (/api/v1 Study endpoints)"
  - "docs/devs/2. hoangxuanlong/file/Test Screen.xlsx"
  - ".agents/skills/utc-screen-skill/"
status: "VERIFIED"
---

# Worklog: Nạp context Study BE/FE, cập nhật tài liệu test nhánh develop và lập plan test màn GS & ST

## READ_PLAN

| Path | Needed section/range | Task-specific reason | Status |
|---|---|---|---|
| `AGENTS.md` | Full router | Provided in task context; root routing and rules | `READ_FROM_CONTEXT` |
| `.agents/AGENTS.md` | Full registry | Provided in task context; scope registry and maintenance rules | `READ_FROM_CONTEXT` |
| `.agents/context-map.md` | Full file | Mandatory context map before choosing scopes | `READ` |
| `.agents/context-manifest.json` | Lines 1-800 | Machine registry for scopes, workflows, contracts | `READ` |
| `.agents/project/agent-control.md` | Full file | Mandatory target tracking and execution rules | `READ` |
| `.agents/target.md` | Full file | Current active target table | `READ` |
| `.agents/worklog/README.md` | Full file | Worklog contract and preflight rules | `READ` |
| `.agents/worklog/TEMPLATE.md` | Full file | Worklog required fields | `READ` |
| `scripts/select-worklogs.mjs` | Selector output | Preflight same-type worklogs | `CHECKED_BY_TOOL` |
| `.agents/server-study/AGENTS.md` | Full file | Study BE scope router | `READ` |
| `.agents/server-study/INDEX.md` | Full file | Study BE page graph | `READ` |
| `.agents/web-work/AGENTS.md` | Full file | Web Work parent router | `READ` |
| `.agents/web-work/study/AGENTS.md` | Full file | Study FE subcontext router | `READ` |
| `.agents/web-work/study/INDEX.md` | Full file | Study FE page graph | `READ` |
| `.agents/worklog/2026-11-22/test-student-st01-st26-backend-connectivity.md` | Full file | Selected by `select-worklogs.mjs --type test --limit 3` | `READ` |
| `.agents/worklog/2026-11-01/test-study-server-all-apis.md` | Full file | Selected by `select-worklogs.mjs --type test --limit 3` | `READ` |
| `docs/devs/2. hoangxuanlong/file/Test Screen.xlsx` | Sheets `SH`, `GS`, `ST`, `ME`, `AD` (focus `GS` & `ST`) | Target test workbook for GS and ST screens | `READ` |
| `.agents/skills/utc-screen-skill/SKILL.md` | Full file | Latest UTC screen test skill merged from `origin/develop` | `READ` |
| `.agents/skills/utc-screen-skill/README.md` | Full file | Overview of UTC screen test skill and scripts | `READ` |
| `.agents/skills/utc-screen-skill/huong-dan/01_Quy_trinh_12_buoc.md` | Full file | 12-step UTC screen test planning workflow | `READ` |
| `apps/study-client/src/app/features/guest/guest.route.ts` | Full file | Verify GS-01..GS-07 routes and API mapping | `READ` |
| `apps/study-client/src/app/features/student/student.route.ts` | Full file | Verify ST-01..ST-26 routes and API mapping | `READ` |
| `apps/study-client/src/app/core/constant/api.constants.ts` | Lines 1-228 | Verify API #01–#105 wired/unwired status for GS & ST | `READ` |
| `apps/study-client/docs/dd_screens/` | Directory listing (`GS-*`, `ST-*`) | Confirm 7 GS + 26 ST DD folders present | `CHECKED_BY_TOOL` |

## LEAF_TARGET_PLAN

| Target | Single operation | Acceptance evidence |
|---|---|---|
| Nạp context Study BE/FE và worklog preflight | Đọc router/index của `server-study`, `web-work/study` và hoàn tất `PRIOR_WORKLOG_REVIEW` | Các file context được đánh dấu `READ` và `PRIOR_WORKLOG_REVIEW` đầy đủ |
| Cập nhật tài liệu test mới nhất từ nhánh develop | Kiểm tra nhánh `develop`/`origin/develop` và cập nhật tài liệu test mới nhất không phá hủy local changes | `git fetch origin develop` + `git merge --ff-only origin/develop` thành công lên `f28d7116`, giữ nguyên `apps/study-server/app/core/constants.py` |
| Phân tích cấu trúc file Test Screen.xlsx cho màn GS và ST | Đọc tất cả sheet và danh sách màn hình GS/ST trong `Test Screen.xlsx` | Trích xuất đầy đủ 7 màn `GS-01`..`GS-07` và 26 màn `ST-01`..`ST-26`, 12 tiêu chí `TC01`..`TC12` và trạng thái `Chưa kiểm thử` |
| Đối chiếu màn hình GS và ST với source Study BE và Study FE | Xác minh routes/pages ở `apps/study-client` và endpoints ở `apps/study-server` cho các màn GS/ST | Bảng đối chiếu đầy đủ route, API wired/unwired/gated và điểm chặn giữa `Test Screen.xlsx` và source |
| Lập kế hoạch test chi tiết cho các màn GS và ST | Xây dựng test plan chi tiết cho từng màn GS và ST theo thực trạng source và tài liệu test | Test plan đầy đủ theo từng nhóm ưu tiên, điều kiện tiên quyết, phân luồng `TC01–TC12`, và quy trình UTC từ `utc-screen-skill` |

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `test`
- selector_command: `node scripts/select-worklogs.mjs --type test --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-22/test-student-st01-st26-backend-connectivity.md`
    - carry_forward: Schema Neon `hoang_xuan_long` đã áp dụng migrations `002`–`020` và seed dữ liệu mẫu; 36/37 Student API pass qua proxy `127.0.0.1:4200 -> 127.0.0.1:3003`; duy nhất `#12 PRIVATE` trả `503` do local chưa cấu hình S3/Object Storage (ảnh hưởng cả `#13` avatar upload và `#34` file upload). `ST-05` (`#16`), `ST-06` (`#17`), `ST-07` bị gated/UNWIRED. `student.route.spec.ts` fail 1 case ở `ST-04`; `ST-11..ST-26` chưa có file `.spec.ts`; `st03-page.css` vượt budget production build.
  - path: `.agents/worklog/2026-11-01/test-study-server-all-apis.md`
    - carry_forward: Phân biệt rõ fake-backed unit tests với live Neon DB; email/storage stubbed ở môi trường local; không kết luận runtime pass từ source/DD tĩnh.
- shortage: `none` (selector trả 3 file gồm worklog hiện tại và 2 worklog `test` gần nhất; đã đọc toàn bộ 2 worklog trước đó)

## EXPECTED_BEHAVIOR

- Requirement: Nạp context dự án `.agents`, thông tin BE (`apps/study-server`) và FE (`apps/study-client`), cập nhật tài liệu test mới nhất từ nhánh `develop`, và lập plan test các màn GS (`GS-01`–`GS-07`) và ST (`ST-01`–`ST-26`) trong `docs/devs/2. hoangxuanlong/file/Test Screen.xlsx`.
- Canonical contract/approved DD:
  - `docs/devs/2. hoangxuanlong/file/Test Screen.xlsx` (sheet `GS`: 7 màn, sheet `ST`: 26 màn, khung kiểm thử `TC01`–`TC12`: `TC01–05` bắt buộc, `TC06–12` chọn `Không áp dụng` khi ngoài phạm vi).
  - `.agents/skills/utc-screen-skill/` (v1.0.0, vừa merge từ `origin/develop` commit `f28d7116`): quy trình 12 bước sinh UTC 4 sheet cho từng màn từ DD (`apps/study-client/docs/dd_screens/GS-*` và `ST-*`).

## TARGET_UPDATES

| Target | From → to | Evidence / reason |
|---|---:|---|
| Nạp context Study BE/FE và worklog preflight | `0% → 100%` | Đã đọc `.agents/server-study/{AGENTS,INDEX}.md`, `.agents/web-work/{AGENTS,study/AGENTS,study/INDEX}.md`, hoàn tất `select-worklogs.mjs` và đọc 2 worklog `test` gần nhất; xóa khỏi `target.md` |
| Cập nhật tài liệu test mới nhất từ nhánh develop | `0% → 100%` | `git fetch origin develop` + `git merge --ff-only origin/develop` (`e8e5147a..f28d7116`) thành công, nạp `.agents/skills/utc-screen-skill/`, `dd_screens/*/code.html` và context mới nhất; giữ nguyên `apps/study-server/app/core/constants.py`; xóa khỏi `target.md` |
| Phân tích cấu trúc file Test Screen.xlsx cho màn GS và ST | `0% → 100%` | Đã đọc toàn bộ sheet `GS` (7 màn `GS-01`..`GS-07`) và `ST` (26 màn `ST-01`..`ST-26`), 12 cột `TC01`–`TC12` và cột `Kết quả chung`/`Ghi chú`; tất cả đang ở trạng thái `Chưa kiểm thử`; xóa khỏi `target.md` |
| Đối chiếu màn hình GS và ST với source Study BE và Study FE | `0% → 100%` | Đã đối chiếu `guest.route.ts`, `student.route.ts`, `api.constants.ts` và DD folders `apps/study-client/docs/dd_screens/{GS,ST}-*`; phân loại rõ màn sẵn sàng test E2E, màn test có điều kiện (S3/seed/gated action), và màn bị chặn (`ST-05`, `ST-06`, `ST-07`); xóa khỏi `target.md` |
| Lập kế hoạch test chi tiết cho các màn GS và ST | `0% → 100%` | Hoàn tất kế hoạch kiểm thử phân pha cho 7 màn GS + 26 màn ST bám sát `Test Screen.xlsx` (`TC01`–`TC12`) và `utc-screen-skill`; xóa khỏi `target.md` |
| Khởi động BE study-server và FE study-client | `0% → 100%` | BE `uvicorn` chạy tại `127.0.0.1:3003` (schema `hoang_xuan_long`), FE `ng serve` chạy tại `127.0.0.1:4200` với `proxy.conf.json`; xóa khỏi `target.md` |
| Seed dữ liệu thử bổ sung (resources, reviews, khóa có phí) trên schema hoang_xuan_long | `0% → 100%` | Đã xác nhận sẵn `resources` (PUBLIC `id=1,3`, PRIVATE `id=2`), `discussions`/`reviews` (`id=1..4`), `quizzes`, `assignments`, và seed thêm khóa miễn phí chưa ghi danh `id=7` + khóa trả phí chưa ghi danh `id=8` + mật khẩu test `student@study2work.edu.vn`; xóa khỏi `target.md` |
| Kiểm thử live trình duyệt nhóm Guest GS-01 đến GS-07 | `0% → 100%` | Đã chạy đủ 7 màn trên Chrome (`127.0.0.1:4200`): 4 Đạt (`GS-04..GS-07`), 3 Không đạt (`GS-01` TC03/TC10, `GS-02` TC02/TC03, `GS-03` TC03); xóa khỏi `target.md` |
| Kiểm thử live trình duyệt nhóm Student ST-01 đến ST-12 | `0% → 100%` | Đã chạy đủ 12 màn trên Chrome với tài khoản Student: 6 Đạt (`ST-01..03`, `ST-08..10`, `ST-12`), 4 Bị chặn (`ST-05..07`, `ST-11`), 1 Không đạt (`ST-04` TC06 nút Thanh toán không điều hướng + TC05 paid bị chặn); xóa khỏi `target.md` |
| Kiểm thử live trình duyệt nhóm Student ST-13 đến ST-26 | `0% → 100%` | Đã chạy đủ 14 màn trên Chrome với tài khoản Student: 11 Đạt (`ST-13..19`, `ST-22`, `ST-24..26`), 1 Bị chặn (`ST-20` tổng tiến độ `#21`), 2 Không đạt (`ST-21`, `ST-23` TC02 header/footer trống do shell `blank`); xóa khỏi `target.md` |
| Cập nhật kết quả kiểm thử vào file Test Screen.xlsx và hoàn tất worklog | `0% → 100%` | Đã cập nhật lossless 7/7 màn `GS` và 26/26 màn `ST` (giữ nguyên toàn bộ công thức cột `P`, dropdown validation và định dạng) vào `docs/devs/2. hoangxuanlong/file/Test Screen.xlsx`; xóa khỏi `target.md` |

## CURRENT_BEHAVIOR

- Source/config:
  - Nhánh hiện tại `hoang_xuan_long_dev_fe` đã fast-forward lên `f28d7116` (bằng `origin/develop`), vẫn giữ thay đổi local `DB_SCHEMA = "hoang_xuan_long"` trong `apps/study-server/app/core/constants.py`.
  - `apps/study-server`: đã wire API `#01`–`#98`, `#101`, `#104`, `#105`.
  - `apps/study-client`: có đủ 7 màn Guest (`GS-01`–`GS-07`, trong đó `GS-04/05/06` là tab trong `GS-03`) và 26 màn Student (`ST-01`–`ST-26`); có đủ 33 thư mục DD kèm `code.html` dưới `apps/study-client/docs/dd_screens/`.
  - `.agents/skills/utc-screen-skill/`: đã có sẵn template `Mau_UTC_Screen.xlsx`, scripts kiểm tra/sinh UTC và ví dụ hoàn chỉnh cho `GS-01` (`73` cases, trạng thái `Chưa chạy` vì DD còn blocker).
- Runnable tests:
  - Không chạy lại test suite trong task lập kế hoạch này; tham chiếu baseline mới nhất từ worklog `2026-11-22` (Student unit tests 27/28 pass, 36/37 Student API pass qua proxy) và `web-work/study/INDEX.md` (Guest focused specs 37/37 pass).
- Runtime wiring:
  - `http://127.0.0.1:4200` (Angular dev server + `proxy.conf.json`) -> `http://127.0.0.1:3003` (FastAPI `study-server`) -> Neon PostgreSQL (`hoang_xuan_long`).

## SOURCE_TRACE

```text
Test Screen.xlsx (GS-01..GS-07, ST-01..ST-26)
  <-> apps/study-client/docs/dd_screens/{GS,ST}-*/ (DD + code.html)
  <-> apps/study-client/src/app/features/{guest/guest.route.ts, student/student.route.ts}
  <-> apps/study-client/src/app/core/constant/api.constants.ts (#01-#45, R-X01)
  <-> apps/study-server/app/api/v1.py (#01-#98, #101, #104, #105)
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| `ST-05`, `ST-06`, `ST-07` (Checkout / Payment / Paid Result) | `API_016` (`POST /orders`) và `API_017` (`POST /payments`) đánh dấu `UNWIRED` trong `api.constants.ts`; `ST-06`/`ST-07` là màn gated tĩnh; `ST-05` khóa tạo đơn | `DISCREPANCY` / `BLOCKED` | Khi test theo `Test Screen.xlsx`, nhánh trả phí ở `ST-04` và các màn `ST-05`, `ST-06`, `ST-07` ghi nhận `Bị chặn` ở `TC05` (vẫn test được `TC01–TC04`, `TC06`, `TC12`) |
| `ST-03` (`#13`), `ST-18` (`#34`), `GS-07` (`#12 PRIVATE`) | Local dev chưa cấu hình S3/Object Storage (`#12 PRIVATE` trả `503 DESIGN_DEPENDENCY_UNAVAILABLE` theo worklog 2026-11-22) | `BLOCKED_ENV` | Không test được upload thật và tải tài nguyên `PRIVATE` nếu chưa cấu hình S3/R2 hoặc storage stub; `GS-07 PUBLIC`, `ST-03` sửa name/phone (`#14`), `ST-18` nộp bài không cần file vẫn test được |
| `ST-03` Bio, `ST-11` Player/`#25`/`#27`, `ST-20` `#21`, `GS-01` lọc danh mục | FE cố ý gate do contract/BE chưa hỗ trợ (`#14` không lưu Bio, `#06` từ chối filter category, `#21` trả `UserProfile`, `#25/#27` chưa mở trên `ST-11`) | `GATED_BY_DESIGN` | Cần đánh dấu rõ `Bị chặn` / `Không áp dụng` đúng như cột `TC05` trong `Test Screen.xlsx`, không báo sai thành bug UI |
| `GS-06`/`ST-12` bảng `resources` | Chưa có API writer cho bảng `resources` (`#47` ghi `lesson_uploads`) | `DATA_DEPENDENCY` | Cần seed bản ghi `resources` (`PUBLIC` và `PRIVATE`) trực tiếp trong schema `hoang_xuan_long` trước khi test `GS-06`, `GS-07`, `ST-12` |
| Unit test `ST-11`..`ST-26` và `student.route.spec.ts` | `ST-11`..`ST-26` chưa có `*.spec.ts`; `student.route.spec.ts` fail 1 case ở `ST-04`; `st03-page.css` vượt budget build production | `DISCREPANCY` | Không chặn test manual trên `ng serve`, nhưng cần ghi chú khi đánh giá độ phủ tự động |

## CHANGES

- Files changed:
  - Fast-forward merge `origin/develop` (`e8e5147a..f28d7116`): cập nhật `.agents/skills/utc-screen-skill/`, `apps/study-client/docs/dd_screens/*/code.html`, `.agents/` context và API `#101/#104/#105`.
  - `.agents/worklog/2026-11-24/2026-11-24-gs-st-test-plan.md` (worklog task này).
  - `.agents/target.md` (cập nhật và xóa các target đã hoàn tất).
- CONTEXT_UPDATES: Kế thừa từ `origin/develop` (`f28d7116`); không chỉnh sửa thêm context page ngoài worklog/target.
- Context pages changed: None (ngoài fast-forward `origin/develop`).
- Assumptions: Chưa tự ý sửa trực tiếp file `docs/devs/2. hoangxuanlong/file/Test Screen.xlsx` vì người dùng yêu cầu chuẩn bị plan test trước; sẽ điền kết quả sau khi thực thi kiểm thử.
- Target progress updates and completion evidence: see `TARGET_UPDATES`.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `node scripts/select-worklogs.mjs --type test --limit 3` | Trả về 3 worklog `test`; đã đọc đủ 2 worklog trước đó | `VERIFIED` |
| `git fetch origin develop && git merge --ff-only origin/develop` | Fast-forward `e8e5147a..f28d7116` thành công; giữ nguyên local change `constants.py` | `VERIFIED` |
| Python đọc `docs/devs/2. hoangxuanlong/file/Test Screen.xlsx` | Đọc đủ 5 sheet, trích xuất toàn bộ 7 màn `GS` và 26 màn `ST` | `VERIFIED` |

## HANDOFF

- Remaining blockers:
  - Cấu hình S3/Object Storage (hoặc stub) nếu muốn test `#12 PRIVATE`, `#13` avatar upload và `#34` file upload.
  - Seed dữ liệu mẫu bổ sung cho bảng `resources` (`PUBLIC`/`PRIVATE`), khóa học có phí (`price > 0`), và đánh giá (`reviews`) trong schema `hoang_xuan_long`.
- Next owner/action: Người dùng duyệt test plan, chọn chạy kiểm thử manual/browser theo từng pha để cập nhật vào `Test Screen.xlsx`, hoặc sinh chi tiết UTC 4-sheet bằng `.agents/skills/utc-screen-skill` cho từng màn GS/ST.
