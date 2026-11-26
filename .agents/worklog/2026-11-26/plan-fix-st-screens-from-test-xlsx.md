---
task_id: "2026-11-26-plan-fix-st-screens-from-test-xlsx"
date: "2026-11-26"
primary_task_type: "fix"
secondary_task_types:
  - docs
project_scopes:
  - web-work
  - server-study
cross_scope_dependencies:
  - apps/study-client/src/app/features/student/ <-> apps/study-server/app/api/ <-> infra/postgres/study-server/
status: "VERIFIED"
---

# Worklog: Phân tích lỗi ST từ Test Screen.xlsx, đối chiếu DD & ảnh, lên phương án fix và note DB

## READ_PLAN

| Path | Needed section/range | Task-specific reason | Status |
|---|---|---|---|
| `AGENTS.md` | Full router | Supplied in task context | `READ_FROM_CONTEXT` |
| `.agents/AGENTS.md` | Full index | Supplied in task context | `READ_FROM_CONTEXT` |
| `scripts/select-worklogs.mjs` | Selector output | Preflight `fix` worklogs | `CHECKED_BY_TOOL` |
| `.agents/worklog/2026-11-22/enable-admin-course-creation.md` | L1-80 | Prior `fix` worklog | `READ` |
| `.agents/worklog/2026-11-22/fix-admin-user-create.md` | L1-80 | Prior `fix` worklog | `READ` |
| `.agents/worklog/2026-11-22/fix-study-admin-courses-runtime-check.md` | L1-80 | Prior `fix` worklog | `READ` |
| `docs/devs/2. hoangxuanlong/file/Test Screen.xlsx` | ST sheet (R1-R28) | Danh sách lỗi thực tế của 26 màn ST | `CHECKED_BY_TOOL` |
| `apps/study-client/docs/dd_screens/screen-index.md` | Full file | Đường dẫn tới các package DD ST-01..ST-26 | `READ` |
| `apps/study-client/docs/dd_screens/ST-{01,04,05,06,07,08,11,20,21,23}*/images/screen-clean.png` | Visual assets | Đối chiếu giao diện yêu cầu của các màn có lỗi | `READ` |
| `apps/study-client/src/app/layouts/student/student-layout.{html,ts}` | Full files | Trace lỗi icon `♧` và `shell: 'blank'` | `READ` |
| `apps/study-client/src/app/shared/ui/student-public-frame.{html,ts}` | Full files | Trace lỗi header vẫn hiện Đăng nhập/Đăng ký | `READ` |
| `apps/study-client/src/app/features/student/ST01/pages/st01-page.html` | L1-90 | Trace ST-01 header và widget tiến độ | `READ` |
| `apps/study-client/src/app/features/student/ST04/pages/st04-page.{html,ts,css}` | Full files | Trace lỗi điều hướng ST-04 -> ST-05 | `READ` |
| `apps/study-client/src/app/features/student/ST05/pages/st05-page.html` | Full file | Trace ST-05 checkout gate và nút quay lại | `READ` |
| `apps/study-client/src/app/features/student/ST08/pages/st08-page.ts` | Full file | Trace thiếu filter COMPLETED và nhãn trạng thái | `READ` |
| `apps/study-client/src/app/features/student/ST11/pages/st11-page.{html,ts}` | Full files | Trace khóa player/#25/#27 trên FE | `READ` |
| `apps/study-client/src/app/features/student/ST20/pages/st20-page.ts` | Full file | Trace ST-20 khóa #21 | `READ` |
| `apps/study-server/app/modules/student/api_{14,16,17,20,21}*` | view/validate/models | Xác minh nguyên nhân gốc BE và yêu cầu DB | `READ` |

## LEAF_TARGET_PLAN

| Target | Single operation | Acceptance evidence |
|---|---|---|
| Đọc toàn bộ lỗi trong `Test Screen.xlsx` và tổng hợp các màn ST bị lỗi | Trích xuất toàn bộ sheet ST từ `Test Screen.xlsx` | Tổng hợp đủ 3 màn Không đạt, 5 màn Bị chặn và các ghi chú nhỏ |
| Đối chiếu DD và ảnh mô tả màn ST tương ứng trong `apps/study-client/docs/dd_screens` | Xem 10 ảnh `screen-clean.png` và đối chiếu `screen-index.md` | Xác nhận yêu cầu giao diện header/footer/icon/flow |
| Trace source FE/BE và schema DB cho từng lỗi để xác định nguyên nhân gốc | Đọc FE components/layouts, BE views/models và kiểm tra cột thực tế trên schema `hoang_xuan_long` | Mỗi lỗi đều có file/dòng bằng chứng cụ thể |
| Lập phương án fix chi tiết và tạo note các thay đổi DB cần thiết | Tạo artifact `plan-fix-st-screens.md` và file `DB_Changes_Note_ST_Screens.md` | Hoàn thành 2 tài liệu sẵn sàng review & triển khai |

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `fix`
- selector_command: `node scripts/select-worklogs.mjs --type fix --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-22/enable-admin-course-creation.md`
    - carry_forward: Luôn bám source-verified evidence trước khi mở khóa action, không tự bịa field ngoài contract.
  - path: `.agents/worklog/2026-11-22/fix-admin-user-create.md`
    - carry_forward: Tách rõ thay đổi FE, BE và DB schema; giữ nguyên các thay đổi không liên quan.
  - path: `.agents/worklog/2026-11-22/fix-study-admin-courses-runtime-check.md`
    - carry_forward: Đối chiếu trực tiếp source hiện hành và runtime thực tế, phân biệt lỗi thật với gate theo thiết kế.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Xem lại DD và ảnh màn ST trong `apps/study-client/docs/dd_screens`, dựa trên các lỗi trong `Test Screen.xlsx` để lập phương án fix chi tiết và tạo note các thay đổi cột/bảng DB cần thiết.

## TARGET_UPDATES

| Target | From → to | Evidence / reason |
|---|---:|---|
| Đọc toàn bộ lỗi trong `Test Screen.xlsx` và tổng hợp các màn ST bị lỗi | `0% → 100%` | Đọc đủ R1–R28 sheet ST |
| Đối chiếu DD và ảnh mô tả màn ST tương ứng trong `apps/study-client/docs/dd_screens` | `0% → 100%` | Đã kiểm tra ảnh `screen-clean.png` và `screen-index.md` |
| Trace source FE/BE và schema DB cho từng lỗi để xác định nguyên nhân gốc | `0% → 100%` | Đã trace đủ FE, BE (`api_14/16/17/20/21`) và 7 bảng DB live |
| Lập phương án fix chi tiết và tạo note các thay đổi DB cần thiết | `0% → 100%` | Đã tạo `plan-fix-st-screens.md` và `DB_Changes_Note_ST_Screens.md` |

## CURRENT_BEHAVIOR

- Source/config: Đã xác định đầy đủ nguyên nhân gốc cho 3 màn Không đạt (`ST-04`, `ST-21`, `ST-23`), 5 màn Bị chặn (`ST-05`, `ST-06`, `ST-07`, `ST-11`, `ST-20`), và các lỗi UI/hồ sơ (`ST-01`, `ST-03`, `ST-08`, `StudentLayout`).
- Runnable tests: Chưa sửa code nên chưa chạy lại test.
- Runtime wiring: Đã đối chiếu trực tiếp cấu trúc cột thực tế trên schema `hoang_xuan_long`.

## SOURCE_TRACE

```text
Test Screen.xlsx (ST sheet) -> DD screens & images -> StudentLayout / StudentPublicFrame / ST01..ST26 -> api_14/16/17/20/21 -> Neon schema hoang_xuan_long
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| `ST-21`, `ST-23` shell | `student.route.ts` dùng `shell: 'blank'` | `DISCREPANCY` | Header/footer render trống (`TC02 Không đạt`) |
| `StudentLayout` notification icon | `student-layout.html#L98` dùng `♧` | `DISCREPANCY` | Sai icon trên mọi màn portal (`ST-11`, `ST-13`...) |
| `StudentPublicFrame` header | Hardcode `Đăng nhập`/`Đăng ký` | `DISCREPANCY` | Hiện nút login dù đã đăng nhập Student (`ST-01`) |
| `ST-08` filter & label | Chỉ có `'all' \| 'active'`, không map `COMPLETED` | `DISCREPANCY` | Khóa hoàn thành hiển thị `"Trạng thái đang được xác nhận"` |
| `ST-11` player/#25/#27 | Backend `#24/#25/#27` trả 200 OK nhưng FE khóa placeholder | `DISCREPANCY` | `ST-11` bị chặn ở `TC05` |
| API `#21` (`ST-20`, `ST-01`) | `api_21_users_me_progress/view.py` trả `UserProfile` thay vì tổng hợp tiến độ | `DISCREPANCY` | `ST-20` & widget tiến độ `ST-01` bị chặn |
| `users.bio` (`ST-03`) | Cột `bio` không tồn tại trong bảng `users` | `NOT_FOUND` | Trường `Bio` bị khóa |
| `payments` / `orders` (`ST-05..07`) | `payments` thiếu `order_id`, `operation_id`, `checkout_url`; API `#17` trả `503`; FE `API_016` là `UNWIRED` | `DISCREPANCY` | Luồng mua khóa trả phí bị chặn |

## CHANGES

- Files changed (FE):
  - `apps/study-client/src/app/features/student/student.route.ts`: đổi `shell: 'blank'` → `'portal'` cho `ST-21` và `ST-23`.
  - `apps/study-client/src/app/layouts/student/student-layout.html`: thay ký tự `♧` bằng SVG icon chuông Thông báo.
  - `apps/study-client/src/app/shared/ui/student-public-frame.{ts,html,css}`: inject `StudentSessionService`, ẩn `Đăng nhập / Đăng ký` và hiển thị Thông báo + tên/avatar Học viên + `Đăng xuất` khi đã đăng nhập.
  - `apps/study-client/src/app/features/student/ST04/pages/st04-page.{ts,html}` & `ST05/pages/st05-page.{ts,html}`: đồng bộ header đã đăng nhập, gắn handler `goToCheckout` rõ ràng cho `ST-04` → `ST-05`, sửa nút quay lại trên `ST-05` trỏ về `/student/enroll/:courseId`.
  - `apps/study-client/src/app/features/student/ST08/data-access/st08-courses.service.ts` & `ST08/pages/st08-page.{ts,html}`: thêm bộ lọc `COMPLETED` ("Đã hoàn thành"), map nhãn `"Đã hoàn thành"` / `"Đã hủy"` và liên kết sang `/student/progress/:courseId`.
  - `apps/study-client/src/app/features/student/ST11/data-access/st11-lesson.service.ts` & `ST11/pages/st11-page.{ts,html,css}`: mở khóa `<video controls>`, nối API `#25` ("Đánh dấu hoàn thành") và API `#27` ("Bài tiếp theo").
  - `apps/study-client/src/app/features/student/shared/models/student-api.models.ts`, `ST20/data-access/st20-progress.service.ts`, `ST20/pages/st20-page.{ts,html}`, `ST01/data-access/st01-overview.service.ts`, `ST01/pages/st01-page.{ts,html,spec.ts}`: nối API `#21` tiến độ tổng hợp thật lên `ST-20` và `ST-01`.
  - `apps/study-client/src/app/features/student/student.route.spec.ts`, `ST03/pages/st03-page.spec.ts`, `student-fixes.spec.ts` (mới): sửa 2 lỗi test cũ và thêm 7 regression tests.
- Files changed (BE):
  - `apps/study-server/app/modules/student/api_21_users_me_progress/{models.py,query.py,view.py}`: sửa API `#21` tổng hợp tiến độ thật từ `enrollments` + `lessons` + `lesson_progress` (không thay đổi DB).
  - `apps/study-server/tests/modules/student/api_21_users_me_progress/test_users_me_progress.py`: cập nhật 5 unit tests theo contract tiến độ tổng hợp mới.
- Files changed (Docs / Test Report):
  - `docs/devs/2. hoangxuanlong/file/DB_Changes_Note_ST_Screens.md`
  - `docs/devs/2. hoangxuanlong/file/Test Screen.xlsx` (cập nhật 19 ô trên sheet `ST`)
- CONTEXT_UPDATES: none
- Context pages changed: none
- Assumptions: Chưa thực hiện bất kỳ thay đổi bảng/cột DB nào (`ST-03 bio`, `ST-05/06/07` thanh toán giữ nguyên theo yêu cầu).
- Target progress updates and completion evidence: see `TARGET_UPDATES`.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `npx ng test --watch=false --include="src/app/features/student/**/*.spec.ts"` | **13/13 files passed, 35/35 tests passed**, 0 errors | PASS |
| `.\.venv\Scripts\pytest.exe tests/modules/student/api_21_users_me_progress -q` | **5/5 passed** | PASS |
| Live E2E via Angular proxy `127.0.0.1:4200/api/v1/*` → `127.0.0.1:3003` (`hoang_xuan_long`) | **8/8 endpoints PASS** (`#21` trả 40% / 2/5 bài / 4 khóa, `#20 COMPLETED`, `#20 ACTIVE`, `#24`, `#25`, `#27`, `#37`, `#39`) | PASS |
| Cập nhật `Test Screen.xlsx` (sheet `ST`) | Cập nhật 19/19 ô cho `ST-01`, `ST-04`, `ST-08`, `ST-11`, `ST-13`, `ST-20`, `ST-21`, `ST-23` | PASS |

## HANDOFF

- Remaining blockers: Các màn phụ thuộc thay đổi DB (`ST-05`, `ST-06`, `ST-07` thanh toán và `ST-03` trường `bio`) giữ trạng thái `Bị chặn` theo đúng `DB_Changes_Note_ST_Screens.md`. Trình duyệt Chrome trên máy chưa bật remote debugging nên không chụp/click trực tiếp qua DevTools MCP, nhưng đã xác minh qua Angular Vitest + live HTTP proxy và cả 2 server (`127.0.0.1:4200` và `127.0.0.1:3003`) vẫn đang chạy sẵn để bạn kiểm tra trực tiếp.
- Next owner/action: Kiểm tra trực quan trên trình duyệt tại `http://127.0.0.1:4200` và chốt phương án cho các mục liên quan DB khi sẵn sàng.
