---
task_id: "2026-11-23-utc-screen-ad02"
date: "2026-11-23"
primary_task_type: "test"
secondary_task_types: ["docs"]
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["Study Web AD-02 -> GET API #68 user list and POST API #105 user creation"]
status: "VERIFIED"
---

# Worklog: UTC chính thức AD-02

## READ_PLAN
| Path | Needed section/range | Task-specific reason | Status |
|---|---|---|---|
| `.agents/AGENTS.md` | Scope registry, global context, read-set rules | Load required project entry context | `READ` |
| `.agents/context-map.md` | Page graph, scope boundary, skill/workflow wiring | Load context graph before selecting deeper context | `READ` |
| `.agents/context-manifest.json` | Registered UTC skill/workflow and Study Web registry entries | Confirm canonical UTC workflow wiring and web scope boundary | `READ` |
| `.agents/project/agent-control.md` | Read-plan, target, preflight requirements | Apply task tracking rules | `READ` |
| `.agents/target.md` | Target table | Track independently verifiable operations | `READ` |
| `.agents/worklog/README.md` | Worklog creation and preflight requirements | Follow task logging convention | `READ` |
| `.agents/worklog/TEMPLATE.md` | Required worklog sections | Complete canonical evidence log | `READ` |
| `scripts/select-worklogs.mjs` | Selector invocation only | Select prior `test` worklogs for preflight | `CHECKED_BY_TOOL` |
| `.agents/worklog/2026-11-23/2026-11-23-load-study-web-utc-screen.md` | Relevant sections: expected/current behavior and discrepancy evidence | Carry forward prior Study Web screen UTC guidance | `READ` |
| `.agents/worklog/2026-11-23/utc-screen-ad01.md` | Relevant sections: expected/current behavior, source trace, discrepancy and handoff | Carry forward UTC workflow evidence; recheck AD-02 independently | `READ` |
| `.agents/worklog/2026-11-23/utc-screen-ad02.md` | Metadata, plan and active status | Confirm selector includes this active log; distinguish it from historical evidence | `READ` |
| `.agents/skills/INDEX.md` | UTC screen skill registry entry and referenced resources | Confirm the registered skill and its resource files | `READ` |
| `.agents/web-work/AGENTS.md` | Scope rules relevant to Study Web | Route exact Study Web context without loading unrelated scope | `READ` |
| `.agents/web-work/INDEX.md` | Scope page graph | Locate Study Web subcontext | `READ` |
| `.agents/web-work/study/AGENTS.md` | Study Web scope rules | Apply screen testing conventions | `READ` |
| `.agents/web-work/study/INDEX.md` | AD-02 source/DD pointers and status | Identify exact screen inputs and real dependencies | `READ` |
| `.agents/web-study/design.md` | Visual/interaction/accessibility testing guidance | Apply Study Web screen acceptance conventions | `READ` |
| `.agents/web-study/frontend-rules.md` | UI layers and testing constraints | Apply Study Web implementation/source evidence rules | `READ` |
| `.agents/skills/utc-screen-skill/SKILL.md` | Required inputs, deliverables, case coverage and validators | Follow registered UTC generation workflow | `READ` |
| `.agents/skills/utc-screen-skill/README.md` | Runtime/dependency setup for UTC scripts | Use the supported generation and validation environment | `READ` |
| `.agents/skills/utc-screen-skill/huong-dan/01_Quy_trinh_12_buoc.md` | Full required checklist | Follow the 12-step authoring and release process | `READ` |
| `.agents/skills/utc-screen-skill/huong-dan/02_Quy_tac_sinh_ca.md` | Case-writing requirements | Derive traceable, observable cases without inventing behavior | `READ` |
| `.agents/skills/utc-screen-skill/huong-dan/03_Anh_xa_Excel_JSON.md` | JSON-to-workbook field mapping | Populate the required workbook columns and status values | `READ` |
| `.agents/skills/utc-screen-skill/huong-dan/04_Mau_lenh_giao_viec_cho_AI.md` | Mandatory prompt/workflow notes | Complete the registered skill workflow | `READ` |
| `.agents/skills/utc-screen-skill/tham-chieu/Nguon_quoc_te.md` | Applicable standards reference | Avoid unsupported compliance claims | `READ` |
| `.agents/skills/utc-screen-skill/vi-du/GS-01/utc-gs01.json` | Example schema/data shape only | Reuse structure, not unapproved expectations | `READ` |
| `.agents/skills/utc-screen-skill/schema/utc-spec.schema.json` | Full schema | Produce a valid UTC specification | `READ` |
| `.agents/skills/utc-screen-skill/scripts/kiem_tra_utc.py` | CLI and validation behavior | Validate UTC requirements and case coverage | `READ` |
| `.agents/skills/utc-screen-skill/scripts/tao_utc.py` | CLI and workbook generation behavior | Confirm template mapping and supported generation path | `READ` |
| `.agents/skills/utc-screen-skill/scripts/kiem_tra_excel.py` | Workbook checker CLI and checks | Validate the generated workbook | `READ` |
| `.agents/skills/utc-screen-skill/mau/Mau_UTC_Screen.xlsx` | Template sheet inventory | Use the canonical four-sheet template | `READ` |
| `.agents/project/INDEX.md` | Ownership and boundary pointers | Load global contract context for Study Web API dependency | `READ` |
| `.agents/project/dependencies.md` | Study Web ↔ Study Server dependency | Confirm the cross-scope API boundary | `READ` |
| `.agents/project/contracts.md` | API contract ownership and status | Locate approved-vs-draft API sources for #68/#105 | `READ` |
| `.agents/server-study/AGENTS.md` | Study Server scope rules | Route API #68/#105 source evidence | `READ` |
| `.agents/server-study/INDEX.md` | Admin API module/test page pointers | Locate exact server sources and tests | `READ` |
| `.agents/server-study/modules/README.md` | Admin module routing for APIs #68/#105 | Confirm exact current server modules | `READ` |
| `.agents/server-study/tests.md` | API #68/#105 test status and runnable boundary | Distinguish existing test evidence from tests run in this task | `READ` |
| `apps/study-server/app/api/v1.py` | API #68/#105 route registration | Confirm current routes and module wiring | `READ` |
| `apps/study-server/app/modules/admin/` | Filename-only inventory for API #68/#105 packages | Locate exact server module source files | `CHECKED_BY_TOOL` |
| `apps/study-server/tests/modules/admin/` | Filename-only inventory for API #68/#105 tests | Locate exact relevant test files | `CHECKED_BY_TOOL` |
| `apps/study-server/app/modules/admin/api_68_admin_users_list/models.py` | API #68 response model | Confirm source response fields and validation types | `SKIPPED` |
| `apps/study-server/app/modules/admin/api_68_admin_users_list/validate.py` | API #68 auth and query input validation | Confirm accepted filters and page rules | `READ` |
| `apps/study-server/app/modules/admin/api_68_admin_users_list/query.py` | API #68 SQL query shape | Confirm source filtering, ordering and pagination | `READ` |
| `apps/study-server/app/modules/admin/api_68_admin_users_list/view.py` | API #68 orchestration and response | Trace auth, query, mapping and output | `READ` |
| `apps/study-server/tests/modules/admin/api_68_admin_users_list/test_admin_users_list.py` | Focused API #68 tests | Confirm executable test coverage already recorded in context | `READ` |
| `apps/study-server/app/modules/admin/api_105_admin_users_create/models.py` | API #105 request/response model | Confirm user creation input and safe response shape | `SKIPPED` |
| `apps/study-server/app/modules/admin/api_105_admin_users_create/validate.py` | API #105 auth and input validation | Confirm role, name, email and password validation source | `READ` |
| `apps/study-server/app/modules/admin/api_105_admin_users_create/query.py` | API #105 SQL operation | Confirm existing users table writes and uniqueness shape | `SKIPPED` |
| `apps/study-server/app/modules/admin/api_105_admin_users_create/view.py` | API #105 orchestration and response | Trace auth, duplicate detection, hash, transaction and output | `READ` |
| `apps/study-server/tests/modules/admin/api_105_admin_users_create/test_admin_users_create.py` | Focused API #105 tests | Confirm test coverage/status of the approved create extension | `READ` |
| `apps/study-client/docs/dd_screens/` | Filename-only inventory | Locate the canonical AD-02 DD package and referenced images | `CHECKED_BY_TOOL` |
| `apps/study-client/docs/utc_screens/` | Filename-only inventory | Avoid overwriting existing AD-02 UTC artifacts | `CHECKED_BY_TOOL` |
| `apps/study-client/src/app/features/admin/AD02/` | Filename-only inventory | Locate exact current AD-02 UI, API, model and test files | `CHECKED_BY_TOOL` |
| `apps/study-client/docs/dd_screens/AD-02-DanhSachNguoiDung/00-overview.md` | Full section | Establish DD version, approval state, scope and acceptance criteria | `READ` |
| `apps/study-client/docs/dd_screens/AD-02-DanhSachNguoiDung/01-ui-elements.md` | Full section | Trace all screen elements and markers | `READ` |
| `apps/study-client/docs/dd_screens/AD-02-DanhSachNguoiDung/02-events.md` | Full section | Derive cases for every DD event | `READ` |
| `apps/study-client/docs/dd_screens/AD-02-DanhSachNguoiDung/03-data-flow.md` | Full section | Capture screen flow, states and request ordering | `READ` |
| `apps/study-client/docs/dd_screens/AD-02-DanhSachNguoiDung/04-api-integration.md` | Full section | Capture API request/response expectations and unresolved fields | `READ` |
| `apps/study-client/docs/dd_screens/AD-02-DanhSachNguoiDung/05-business-rules.md` | Full section | Capture approved and pending business rules | `READ` |
| `apps/study-client/docs/dd_screens/AD-02-DanhSachNguoiDung/06-navigation.md` | Full section | Trace screen transitions and route decisions | `READ` |
| `apps/study-client/docs/dd_screens/AD-02-DanhSachNguoiDung/07-test-cases.md` | Full section | Reuse planning scenarios and find coverage gaps | `READ` |
| `apps/study-client/docs/dd_screens/AD-02-DanhSachNguoiDung/code.html` | Static markup only; do not execute scripts | Correlate DD labels and element hierarchy without treating prototype as runtime | `READ` |
| `apps/study-client/src/app/features/admin/` | Filename-only inventory | Locate shared route, shell and API-boundary files used by AD-02 | `CHECKED_BY_TOOL` |
| `apps/study-client/src/app/core/` | Filename-only inventory for API constants/transport files | Locate shared caller and API descriptor dependencies | `CHECKED_BY_TOOL` |
| `apps/study-client/src/app/layouts/admin/` | Filename-only inventory for Admin shell | Locate session gating and shell context | `CHECKED_BY_TOOL` |
| `apps/study-client/src/app/features/admin/admin.routes.ts` | Admin screen route registration | Confirm AD-02 route and lazy component binding | `READ` |
| `apps/study-client/src/app/core/http/admin-api.service.ts` | Authenticated HTTP wrapper | Trace shared authorization and request transport | `READ` |
| `apps/study-client/src/app/core/auth/admin-session.service.ts` | Admin session state and role gate | Confirm current session/access conditions | `SKIPPED` |
| `apps/study-client/src/app/layouts/admin/admin-layout.ts` | Admin shell session check | Trace session before screen display | `READ` |
| `apps/study-client/src/app/layouts/admin/admin-layout.html` | Admin shell template | Confirm visible gate/error status around AD-02 | `READ` |
| `apps/study-client/src/app/layouts/admin/admin-layout.css` | Admin shell styling | Only inspect if shell visual scope affects screen acceptance | `SKIPPED` |
| `apps/study-client/src/app/core/constant/api.constants.ts` | API #68/#105 descriptors | Confirm current endpoint IDs/statuses | `READ` |
| `apps/study-client/src/app/features/admin/AD02/pages/ad02-page.ts` | Screen initialization, filters, create flow and refresh handling | Recheck current AD-02 orchestration | `READ` |
| `apps/study-client/src/app/features/admin/AD02/pages/ad02-page.html` | Template controls, bindings and states | Recheck current screen structure and interactions | `READ` |
| `apps/study-client/src/app/features/admin/AD02/pages/ad02-page.css` | AD-02 component layout styles | Compare current screen structure with DD visual claims | `SKIPPED` |
| `apps/study-client/src/app/features/admin/AD02/pages/ad02-page.spec.ts` | Focused AD-02 tests | Record existing test coverage evidence; do not assume tests passed here | `READ` |
| `apps/study-client/src/app/features/admin/AD02/data-access/ad02-api.service.ts` | API #68 and #105 call construction | Trace page callers to shared transport | `READ` |
| `apps/study-client/src/app/features/admin/AD02/data-access/ad02-api-boundary.ts` | Raw response validation/status mapping | Compare current client contract with DD | `READ` |
| `apps/study-client/src/app/features/admin/AD02/models/ad02-screen.model.ts` | Filter, pagination, ID and status mapping | Recheck source behavior without converting it into expected behavior | `READ` |
| `apps/study-client/src/app/features/admin/AD02/ui/ad02-screen.ui.ts` | Screen-local interaction component | Recheck component events and local behavior | `READ` |
| `apps/study-client/src/app/features/admin/AD02/ui/ad02-create-user-dialog.ts` | Dialog state and form/event handling | Recheck user creation interaction | `READ` |
| `apps/study-client/src/app/features/admin/AD02/ui/ad02-create-user-dialog.html` | Dialog controls and status content | Recheck modal elements and bindings | `READ` |
| `apps/study-client/src/app/features/admin/AD02/ui/ad02-create-user-dialog.css` | Dialog layout | Compare DD and current UI visual scope | `SKIPPED` |
| `/home/daovh/.codex/plugins/cache/openai-primary-runtime/spreadsheets/26.1119.11507/skills/spreadsheets/SKILL.md` | Workbook authoring and verification rules | Follow current spreadsheet artifact workflow | `READ` |
| `/home/daovh/.codex/plugins/cache/openai-primary-runtime/spreadsheets/26.1119.11507/skills/spreadsheets/style_guidelines.md` | Workbook visual style guidance | Match the required workbook template | `READ` |
| `/home/daovh/.codex/plugins/cache/openai-primary-runtime/spreadsheets/26.1119.11507/skills/spreadsheets/workflows/create_workflows.md` | Local workbook creation sequence | Use the supported authoring workflow | `READ` |
| `/home/daovh/.codex/plugins/cache/openai-primary-runtime/spreadsheets/26.1119.11507/skills/spreadsheets/artifact_tool_docs/API_QUICK_START.md` | Supported import/edit/export/render methods | Author and visually inspect the workbook | `READ` |
| `/home/daovh/.cache/codex-runtimes/codex-primary-runtime/plugins/openai-primary-runtime/plugins/spreadsheets/skills/spreadsheets/container_tools/mark_artifact_operation_started.mjs` | Required pre-authoring marker invocation | Mark the single requested AD-02 workbook creation operation | `CHECKED_BY_TOOL` |

| `/home/daovh/.codex/plugins/cache/openai-primary-runtime/spreadsheets/26.1119.11507/skills/spreadsheets/SKILL.md` | Workbook authoring rules | Use the registered workbook authoring workflow | `READ` |
| `/home/daovh/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/` | Package file inventory only | Check for the required operation marker helper | `CHECKED_BY_TOOL` |
| `/home/daovh/.cache/codex-runtimes/` | Filename search only | Search the active runtime for the marker helper | `CHECKED_BY_TOOL` |
| `/home/daovh/.codex/plugins/cache/` | Filename search only | Search plugin cache for the marker helper | `CHECKED_BY_TOOL` |
| `/home/daovh/.codex/plugins/cache/openai-primary-runtime/` | Filename search only | Search current spreadsheet runtime package | `CHECKED_BY_TOOL` |
| `/home/daovh/.cache/codex-runtimes/codex-primary-runtime/` | Filename search only | Search active runtime bundle for the marker helper | `CHECKED_BY_TOOL` |
| `/home/daovh/.codex/plugins/cache/openai-primary-runtime/spreadsheets/26.1119.11507/skills/spreadsheets/container_tools/` | Filename search only | Confirm marker helper is absent from spreadsheet tools | `CHECKED_BY_TOOL` |
| `/home/daovh/.cache/codex-runtimes/codex-primary-runtime/plugins/openai-primary-runtime/` | Filename search only | Search runtime plugin package for marker helper | `CHECKED_BY_TOOL` |
| `apps/study-client/docs/utc_screens/utc-spec-AD02.json` | Generated UTC spec | Run schema/coverage validator | `CHECKED_BY_TOOL` |
| `apps/study-client/docs/utc_screens/kiem-tra-utc-AD02.json` | Final validation, blockers and release decision | Record validator outcome and release gates without replacing AD-01 report | `CHECKED_BY_TOOL` |
| `apps/study-client/docs/utc_screens/kiem-tra-excel-AD02.json` | Workbook validator result | Preserve checker output per screen | `CHECKED_BY_TOOL` |
| `apps/study-client/docs/utc_screens/UTC_AD-02_DanhSachNguoiDung.xlsx` | Four-sheet UTC workbook | Check required tabs, formulas, blank execution fields and visual layout | `CHECKED_BY_TOOL` |
| `/tmp/utc-screen-ad02/build.mjs` | Spec/workbook builder implementation | Recheck workbook generation and formatting logic | `READ` |
| `/tmp/utc-screen-ad02/cover.png` | Rendered cover | Visually review release state and summary formulas | `READ` |
| `/tmp/utc-screen-ad02/overview.png` | Rendered overview sheet | Visually review API, requirement and blocker sections | `READ` |
| `/tmp/utc-screen-ad02/screen-cases.png` | Rendered screen cases | Visually review case text, pending status and blank execution fields | `READ` |
| `/tmp/utc-screen-ad02/elements.png` | Rendered component sheet | Visually review all marker rows and supplemental dialog components | `READ` |
| `/tmp/utc-screen-ad02/element-cases.png` | Rendered component cases | Visually review case legibility and execution fields | `READ` |
| `/tmp/utc-screen-ad02/events.png` | Rendered event sheet | Visually review event catalog | `READ` |
| `/tmp/utc-screen-ad02/event-cases.png` | Rendered event cases | Visually review case legibility and execution fields | `READ` |
| `/tmp/utc-screen-ad02/template-preview/01_Bìa.png` | Template preview | Not needed after exact template workbook was imported | `SKIPPED` |
| `/tmp/utc-screen-ad02/template-preview/02_Tổng_quan.png` | Template preview | Not needed after exact template workbook was imported | `SKIPPED` |
| `/tmp/utc-screen-ad02/template-preview/03_Thành_phần.png` | Template preview | Not needed after exact template workbook was imported | `SKIPPED` |
| `/tmp/utc-screen-ad02/template-preview/04_Sự_kiện.png` | Template preview | Not needed after exact template workbook was imported | `SKIPPED` |

## LEAF_TARGET_PLAN

| Target | Single operation | Acceptance evidence |
|---|---|---|
| Xác định điều kiện phát hành UTC AD-02 | Đối chiếu DD, context và source hiện hành | DD status, blockers and source discrepancies are documented |
| Sinh UTC spec AD-02 | Tạo spec và blocker inventory | UTC validator passes with full DD traceability |
| Tạo workbook UTC AD-02 | Tạo workbook 4 sheet từ template | Workbook exists with required sheets and appropriate release status |
| Kiểm tra UTC spec AD-02 | Chạy validator trên JSON | Validator report records structure, coverage and release status |
| Kiểm tra workbook UTC AD-02 | Chạy workbook validator và xem bản render các sheet | Workbook validator passes; all sheets are readable and statuses correct |

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `test`
- selector_command: `node scripts/select-worklogs.mjs --type test --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-23/2026-11-23-load-study-web-utc-screen.md`
    - carry_forward: Keep approved DD expectations distinct from source/runtime observations; retain confirmation status for unresolved decisions; never execute static prototype HTML.
  - path: `.agents/worklog/2026-11-23/utc-screen-ad01.md`
    - carry_forward: AD-01 DD/source discrepancies demonstrate the need to recheck each screen's current source; validator and workbook checks are required for a deliverable UTC package, but AD-01 facts do not transfer to AD-02.
- shortage: `none` (7 available, 3 selected; two historical logs and current active log)

## TARGET_UPDATES

| Target | From → to | Evidence / reason |
|---|---:|---|
| Xác định điều kiện phát hành UTC AD-02 | `0% → 100%` | DD BLOCKED, 8 blocker, API #68 draft, runtime NOT VERIFIED; đã chốt deliverable là bản kế hoạch chờ xác nhận. |
| Sinh UTC spec AD-02 | `0% → 100%` | Tạo spec 18 requirement, 50 component, 14 event, 2 API; đủ 76 ca và truy vết 18/18 yêu cầu. |
| Tạo workbook UTC AD-02 | `0% → 100%` | Tạo workbook từ template canonical với đủ 4 sheet; hàng được wrap/điều chỉnh chiều cao. |
| Kiểm tra UTC spec AD-02 | `0% → 100%` | Validator không có lỗi cấu trúc; cảnh báo chặn phát hành được ghi vào báo cáo. |
| Kiểm tra workbook UTC AD-02 | `0% → 100%` | Excel validator hợp lệ, 622 công thức; xem đủ 7 bản render và kiểm tra 76 dòng case. |

## EXPECTED_BEHAVIOR

- Yêu cầu người dùng: tạo UTC bản chính thức cho AD-02 theo UTC screen skill.
- Canonical DD AD-02 hiện còn `BLOCKED — decisions remain open`; theo skill, trạng thái này chỉ cho phép phát hành kế hoạch UTC chờ xác nhận, chưa được coi là UTC chính thức để chạy/nghiệm thu.
- API #68 còn Draft — Needs Confirmation. API #105 là extension đã được người dùng duyệt, nhưng quyền user-management và tenant policy tổng thể còn mở.
- Phải tách expected behavior đã duyệt khỏi hiện trạng source; không coi screenshot/prototype là runtime.

## CURRENT_BEHAVIOR

- Source Study Web hiện đăng ký `/admin/users`, gọi GET #68 và dùng POST #105 cho dialog tạo user. Client source có loading/ready/empty/error, lọc keyword name/email, role/status exact-string, pagination, handoff bằng safe ID và reload cùng query sau tạo thành công.
- Server route hiện đăng ký GET và POST `/admin/users`; #68 implementation có local source nhưng contract DD vẫn Draft. Runtime authenticated browser, deployment, live API và DB chưa xác minh.
- Evidence test đã có trong scope context cho AD-02 client và API #105 fake-session; task này không chạy application test.
- Không có quyết định owner cho permission, tenant, enum role/status, PII/lifecycle, reset/empty-page policy, thiết kế hoặc người duyệt.

## DISCREPANCIES

- API #68 source đang dùng claim `ADMIN`, trong khi quyền user-management và tenant/scope policy chưa được owner duyệt.
- Placeholder prototype hứa tìm mã user, nhưng API #68 source chỉ tìm `full_name`/`email`; role/status enum và mapping nhãn cũng chưa được chốt.
- Screenshot/prototype có các khẳng định health, sync, audit, RBAC assurance, export/help và footer destinations không có contract/source; chúng không được đưa thành kỳ vọng runtime.
- Prototype screenshot và current Angular source khác nhau về shell, palette/typeface, component set; create-user dialog là current-source extension có API #105 riêng.
- Legacy BIGINT model và V1-PILOT UUID/schema deployment chưa được xác minh; reviewer/approver chưa xác định.

## CHANGES

- Tạo `apps/study-client/docs/utc_screens/utc-spec-AD02.json` gồm 18 requirement, 50 component, 14 event, hai API, 8 blocker và 76 test case.
- Tạo `apps/study-client/docs/utc_screens/UTC_AD-02_DanhSachNguoiDung.xlsx` từ template chuẩn, giữ trạng thái ca `Chưa chạy`, để trống kết quả/bằng chứng/người/ngày thực thi.
- Tạo `kiem-tra-utc-AD02.json` với trạng thái phát hành chờ xác nhận và `kiem-tra-excel-AD02.json` với kết quả workbook checker; không sửa/ghi đè artifact AD-01.
- `/tmp/utc-screen-ad02/build.mjs` sinh workbook từ template; đã thêm wrap và tính chiều cao hàng cho các bảng dữ liệu để nội dung nhiều dòng đọc được.
- Chỉ thay đổi tài liệu/báo cáo và tracking; không đổi source code. CONTEXT_UPDATES: none.
- Required artifact-operation marker helper không có trong các runtime/plugin paths đã tìm; đã ghi nhận là unavailable, không tự tạo helper.

## VERIFICATION

| Command / inspection | Result | Status |
|---|---|---|
| `python3 .agents/skills/utc-screen-skill/scripts/kiem_tra_utc.py --input apps/study-client/docs/utc_screens/utc-spec-AD02.json` | Cấu trúc hợp lệ; 18/18 requirement có truy vết; 76 ca; không lỗi; `du_dieu_kien_phe_duyet=false` do blocker DD | `PASS_WITH_RELEASE_BLOCKER` |
| `python3 .agents/skills/utc-screen-skill/scripts/kiem_tra_excel.py --input apps/study-client/docs/utc_screens/UTC_AD-02_DanhSachNguoiDung.xlsx` | Đủ 4 sheet; 622 công thức; không lỗi | `PASS` |
| Kiểm tra XLSX worksheet XML | 76 case có công thức kiểm tra; tất cả ở `Chưa chạy`; kết quả/bằng chứng/bug/tester/ngày còn trống; row height 127–231 pt | `PASS` |
| Xem render workbook | Đã kiểm tra 7 preview: cover, overview và các catalog/case sheets; nội dung wrap, cột thực thi rỗng, trạng thái chờ xác nhận hiển thị | `PASS` |
| Application tests / browser runtime | Không chạy theo phạm vi; test/runtime evidence có sẵn trong context không được xem là đã chạy trong task này | `NOT_RUN` |
| Required artifact-operation marker | Script không tìm thấy trong các path đã kiểm tra | `UNAVAILABLE` |

## HANDOFF

- Deliverable hiện là **BẢN KẾ HOẠCH UTC — CHỜ XÁC NHẬN**, không phải bản chính thức được duyệt để thực thi.
- Chặn phát hành: 8 blocker (`AD02-BL-001`…`AD02-BL-008`), DD BLOCKED, API #68 Draft, runtime chưa xác minh và thiếu reviewer/approver. Chi tiết quyết định cần có nằm trong `kiem-tra-utc-AD02.json`.
- Sau khi owner đóng quyết định và reviewer/approver ký duyệt, cập nhật kỳ vọng/các ca bị ảnh hưởng, xác minh môi trường kiểm thử rồi chạy lại quy trình/phê duyệt.
- Root project context không thay đổi; `validate-agent-context.mjs` không áp dụng.
