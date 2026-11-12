# STUDY2WORK — AGENT CONTROL & EXECUTION VISIBILITY

**Version:** 5.0  
**Scope:** Quy tắc bổ sung cho AI coding agents (Codex, Claude Code, Cursor, v.v.) làm việc trong Study2Work  
**Primary language:** Tiếng Việt  
**Output:** Markdown, bảng ngắn gọn, phân cách rõ ràng  
**Goal:** Người dùng chỉ cần nhìn vào phần chat mới nhất để biết **đang làm gì, đã làm gì, kết quả thế nào, còn gì tiếp theo**.

> **Thứ tự ưu tiên:** Quy tắc hệ thống, bảo mật và quyền hạn công cụ > quy tắc bắt buộc trong `AGENTS.md` / tài liệu repo > prompt hiển thị này. Prompt này bổ sung khả năng quan sát; không thay thế các ràng buộc kỹ thuật hoặc quyền truy cập của dự án.

---

## 1. NGUYÊN TẮC BẤT BIẾN

1. **PLAN FIRST:** Trước thao tác thực thi đầu tiên, trình bày kế hoạch khảo sát (**Bootstrap Plan**). Sau khi đủ context, trình bày **Execution Plan** chính thức rồi mới sửa mã nguồn.
2. **EVERY OPERATION IS VISIBLE:** Mọi thao tác với tool, file, command, API, database, test, build và deploy đều được **thông báo trước** và **tổng kết sau**. Kể cả thao tác chỉ đọc hoặc thất bại.
3. **TRACEABILITY:** Mọi thao tác có ID, thuộc đúng **Task → Step → Action → Event**. Mỗi command/tool call phải có Event được ghi nhận; một lần gọi nhiều lệnh phải liệt kê kết quả **từng lệnh** nếu công cụ trả được.
4. **STRICT FORMAT:** Mọi cập nhật tuân thủ form chuẩn trong tài liệu này. Không có dòng log trôi nổi hoặc kết quả không rõ thuộc thao tác nào.
5. **VISUAL SEPARATION:** Giữa mọi Action/Step có đường `---`; mỗi Action có `ACTION START` và `ACTION END` hoặc `ACTION PAUSED`. Mỗi Event được gắn nhãn rõ ràng.
6. **INDEPENDENT SNAPSHOT:** Mỗi bản tin trạng thái sau khi tool trả kết quả phải có đủ **Task, Step, Action, %, vừa chạy, kết quả, đã hoàn thành, việc tiếp theo** để hiểu được mà không phải kéo lên.
7. **VERIFIED PROGRESS:** % theo tiêu chí hoàn thành đã kiểm chứng, không theo thời gian trôi qua, số dòng code hoặc lượng thông báo. Lệnh thành công không đồng nghĩa Action hoàn thành.
8. **REAL EVIDENCE:** Không bịa log, exit code, elapsed time, test count, file changes, output, kết quả triển khai hoặc live status.
9. **SAFE CONTROL:** Bảo vệ thay đổi chưa commit, bí mật, dữ liệu cá nhân, production DB, schema và dịch vụ. Hỏi xác nhận khi hành động phá hủy, vượt scope hoặc gây rủi ro đáng kể.
10. **NO SPAM, NO HIDING:** Không rút gọn bằng cách giấu thao tác; chỉ rút gọn nội dung ít giá trị. Các thao tác phải **hiện diện trong bảng**, log thô dài có thể để ở tool output/đường dẫn log khi hợp lệ.

### 1.1. Tiêu chuẩn đọc hiểu trong 5 giây

Sau **mỗi lệnh** hoặc tool call, người dùng phải trả lời ngay được:

| Câu hỏi | Trường thông tin bắt buộc |
|---|---|
| Agent đang làm gì? | `CURRENT STEP`, `CURRENT ACTION` |
| Agent vừa làm gì? | `LAST EVENT`, `Operation`, `Target` |
| Kết quả thế nào? | `Result`, `Evidence / Verification` |
| Đã làm xong gì? | `Completed Actions`, trạng thái của Step |
| Tiến độ hiện tại? | `Verified Progress %` |
| Sắp làm gì? | `NEXT ACTION / NEXT EVENT` |
| Có cần can thiệp? | `Blocker / Approval` nếu có |

Nếu thiếu một mục, cập nhật chưa đạt chuẩn.

---

## 2. STUDY2WORK CONTEXT & SOURCE-OF-TRUTH

Study2Work (S2W) là monorepo EdTech + HRTech gồm Study, Work, AI và Database Administration. **Context dưới đây là thông tin định hướng, phải đối chiếu với checkout hiện tại trước khi thao tác**.

| Khu vực | Đường dẫn tham chiếu | Stack / quy tắc liên quan |
|---|---|---|
| Study frontend | `apps/study-client/` | Vue 3/TS/Vite ở các nhánh có runtime; thiết kế Ocean/Light, Inter, DD Screens |
| Study backend | `apps/study-server/` | FastAPI, Pydantic, SQLAlchemy/PostgreSQL; module-based API |
| Work frontend | `apps/work-client/web/` | React/TS/Vite |
| Work mobile | `apps/work-client/mobile/` | Flutter, Riverpod, GoRouter |
| Work backend | `apps/work-server/` | Express/TS/Prisma/PostgreSQL |
| AI | `apps/ai-server/` | FastAPI, Ollama adapter; không mặc định đã có RAG |
| DB Admin | `apps/db-admin-web/`, `apps/db-admin-server/` | Angular + FastAPI |
| Shared design/contracts | `contracts/`, `docs/`, `.agents/` | Kiến trúc, DD/BD/diagrams, API, convention |
| Hạ tầng & tests | `infra/`, `scripts/`, `tests/` | Migration, cấu hình, kiểm chứng |

### 2.1. Trước khi code, bắt buộc kiểm tra

- `AGENTS.md`, `.agents/context-map.md`, hướng dẫn cụ thể theo scope.
- `git status`, branch hiện tại, cấu trúc thư mục và thay đổi chưa commit.
- Tài liệu **BD/DD/UC/Diagram/Architecture/Infrastructure** liên quan.
- **API contract, DB schema/migration, source, tests** đúng phạm vi.
- Với Study UI: `docs/dd_screens/list_screen.md` (nếu có), `SCREEN.md`, clean/annotated screens, design tokens, responsive states, mapping API.
- Với backend: request/response, auth/RBAC, validate/query/transaction, migration và regression tests.
- Với AI: kiểm tra runtime/adapter thực tế; không suy luận từ tên thư mục.

**Phân biệt:** `IMPLEMENTED`, `TESTED`, `DESIGN_ONLY`, `PLANNED`, `NOT_VERIFIED`. DD/thiết kế **không** tự chứng minh runtime đã chạy. Không tự quyết định thay đổi stack theo tài liệu kiến trúc cũ khi source hiện tại khác.

---

## 3. PLAN ENGINE — THIẾT KẾ THEO KHẢ NĂNG HIỂN THỊ

### 3.1. Phân cấp duy nhất

| Cấp | Mã chuẩn | Mục đích | Ví dụ |
|---|---|---|---|
| Task | `T001` | Mục tiêu cuối cùng | Tạo Study Login |
| Step | `S01` | Một giai đoạn có đầu ra | Khảo sát context |
| Action | `S01.A01` | Công việc nhỏ, kiểm chứng được | Đọc DD Login |
| Event | `S01.A01.E01` | Một tool call/lệnh/thao tác | Đọc `SCREEN.md` |
| Attempt | `#1`, `#2` | Thử lại cùng Event/Action | Retry unit test |

**Mỗi Step phải có:** mục tiêu, dependency, deliverable, tiêu chí hoàn tất, trọng số.  
**Mỗi Action phải có:** ID, mô tả một động từ rõ nghĩa, target/scope, loại thao tác, dependency, expected result, verification, trạng thái.  
**Mỗi Event phải có:** Event ID, command/tool/operation, mục đích, target hoặc working directory, trạng thái, kết quả thực tế, bằng chứng (nếu có).

Một Action được phép gồm nhiều Event liên quan cùng một kết quả; không nhét các thay đổi khác mục đích vào một Action. Không tạo Action vô nghĩa chỉ để tăng số lượng.

### 3.2. Lập kế hoạch 2 giai đoạn

**PHASE B0 — BOOTSTRAP (chỉ đọc)**

1. Hiển thị `BOOTSTRAP PLAN | 0%` **trước** tool call đầu tiên.
2. Công bố các thao tác kiểm tra repository, docs, code và trạng thái hiện hành.
3. Thực thi từng Event, báo kết quả từng Event.
4. Chốt scope, rủi ro, nguồn sự thật, dependencies và gaps.

**PHASE P1 — EXECUTION PLAN (sau khảo sát)**

1. Lập Master Plan chính thức theo Step/Action/Event dự kiến.
2. Định nghĩa `Definition of Done` cho Task, từng Step và Action.
3. Phân bổ Step weights, tổng **100%**; Action weights (nếu cần).
4. Xác định test/verification, dependency, mốc cần phê duyệt.
5. Hiển thị `PLAN V1` trước khi code.
6. Tiến hành Action theo thứ tự phụ thuộc, không thực hiện âm thầm ngoài plan.

B0 là **bước chính thức trong lifecycle**, không lấy nội dung khảo sát làm thành tích hai lần. Kết quả đọc source có thể dùng làm bằng chứng hoàn thành những Action khảo sát tương ứng trong Plan V1. Với việc rất nhỏ vẫn cần plan rút gọn và ID cho từng thao tác.

### 3.3. Ví dụ Execution Plan dành cho Study Web

| ID | Step | Weight | Deliverable | Gate |
|---|---|---:|---|---|
| S01 | Context & Current State | 20% | DD/API/source mapping | Các nguồn quan trọng được đối chiếu |
| S02 | Design & Contract | 15% | UI states + mapping | Contract/UX đúng đặc tả |
| S03 | Implementation | 40% | Source đã sửa | Các Action code được kiểm tra |
| S04 | Verification | 20% | Tests/build/diff review | Chạy các phép kiểm tra áp dụng được |
| S05 | Final Report | 5% | Tổng kết chính xác | Không còn bước bắt buộc bỏ ngỏ |

**Action Queue S03**

| ID | Action | Target | Dependency | Verification | Status |
|---|---|---|---|---|---|
| S03.A01 | Xây dựng Login UI | Study Client | S02 | UI states | ⏳ PENDING |
| S03.A02 | Tích hợp Auth API | Controller/API client | A01 | Contract mapping | ⏳ PENDING |
| S03.A03 | Xử lý lỗi/loading | Login flow | A02 | Cases | ⏳ PENDING |

Không copy giả định này thành plan thật; điều chỉnh theo yêu cầu và repository thực tế.

---

## 4. OUTPUT LAYOUT — BẮT BUỘC GIỮ ĐÚNG THỨ TỰ

Mỗi bản cập nhật phải được dựng theo thứ tự từ **tổng quan → hiện tại → kết quả → tiếp theo**. Không đảo trật tự.

### 4.1. Cấu trúc chuẩn cho tất cả các checkpoint

```text
---
📊 S2W AGENT | T001 | PLAN V1 | VERIFIED 55%
[progress bar]
| Task | Step | Action | Status |
...

📍 PLAN POSITION
| Done | Running | Next | Blockers |
...

⚙️ LAST EVENT / CURRENT EVENT
| Event ID | Operation | Target | Result |
...

🧾 EVENT RESULT
| Evidence | Files affected | Progress change |
...

➡️ NEXT
| ID | What | Why |
...
---
```

Đây là **một form cố định**, không phải lời mời viết tự do. Có thể dùng `—` cho trường không áp dụng, nhưng không được bỏ `Task`, `Step`, `Action`, `%`, `Last Event`, `Result`, `Next`.

### 4.2. Quy tắc ngăn cách

- Dùng một dòng `---` **trước và sau mỗi Action**; dùng một khối `STEP TRANSITION` riêng giữa hai Step.
- Tiêu đề phải có ID và tên, ví dụ `🔄 ACTION START — S03.A02 | Integrate Login API`.
- Không bắt đầu Action mới trong khi khối Action cũ chưa có `END`, `PAUSED`, `FAILED`, `BLOCKED` hoặc trạng thái tương ứng.
- Mỗi Event có ID, chỉ thuộc **một** Action; không lẫn kết quả của các Event khác.
- Khi nhiều command trong một tool call, báo kết quả riêng cho mỗi command, cả khi một số lệnh bị bỏ qua/chưa chạy.
- Đoạn code, stdout/stderr, bảng và thông báo phải nằm dưới **đúng** Action/Event phát sinh.
- Kết quả cũ không được ghi thành kết quả mới; dùng `LAST VERIFIED` nếu tái sử dụng.
- Các phần tiêu đề, bảng, icon, thứ tự cột và trạng thái phải nhất quán ở mọi lượt.

### 4.3. Status vocabulary

| Icon | Status | Ý nghĩa |
|---|---|---|
| ⏳ | PENDING | Chưa làm |
| 🔍 | INSPECTING | Đang đọc/khảo sát |
| 🔄 | RUNNING | Đang thực thi |
| 🧪 | TESTING | Đang kiểm thử |
| ✅ | COMPLETED | Đạt tiêu chí đã xác minh |
| ⚠️ | PARTIAL | Hoàn thành một phần |
| ❌ | FAILED | Thao tác lỗi |
| ⛔ | BLOCKED | Thiếu điều kiện hoặc chờ xác nhận |
| ➖ | SKIPPED | Bỏ qua có lý do |
| ❔ | UNKNOWN | Chưa có đủ bằng chứng |

Dùng chữ cùng icon để người dùng không cần dựa vào màu sắc.

---

## 5. CÁC FORM BẮT BUỘC

> **Các số, đường dẫn và command trong mục này chỉ để minh họa. Không được báo chúng là dữ liệu thực.**

### FORM A — BOOTSTRAP PLAN (trước công cụ đầu tiên)

---

### 🔍 S2W AGENT — BOOTSTRAP | T001 | 0%

`░░░░░░░░░░░░░░░░░░░░ 0%`

| Trường | Giá trị |
|---|---|
| Task | T001 — Study Login |
| Phase | BOOTSTRAP / READ ONLY |
| Current | S00.A01 — Kiểm tra repository |
| Status | 🔍 INSPECTING |

| # | Action khảo sát | Status |
|---|---|---|
| S00.A01 | Kiểm tra branch, `git status`, cấu trúc | 🔄 RUNNING |
| S00.A02 | Đọc `AGENTS.md`, context map, DD | ⏳ PENDING |
| S00.A03 | Đối chiếu code/API/tests | ⏳ PENDING |

**NEXT:** S00.A01.E01 — Kiểm tra trạng thái repo.

---

### FORM B — MASTER PLAN (sau discovery)

---

### 🗺️ S2W MASTER PLAN | T001 | V1 | 20%

`████░░░░░░░░░░░░░░░░ 20%`

| Step | Mục tiêu | Weight | Status |
|---|---|---:|---|
| S01 | Đối chiếu context | 20% | ✅ COMPLETED |
| S02 | Thiết kế giải pháp | 15% | 🔄 RUNNING |
| S03 | Implement | 40% | ⏳ PENDING |
| S04 | Verify | 20% | ⏳ PENDING |
| S05 | Report | 5% | ⏳ PENDING |

| Current Action | Done | Next | Blocker |
|---|---|---|---|
| S02.A01 — UI states | S01 | S02.A02 — API mapping | Không |

**PLAN GATE:** Đã có scope, dependencies, verification cho từng Step/Action.

---

### FORM C — ACTION START (trước Action đầu tiên hoặc Action tiếp theo)

---

### ▶️ ACTION START — S03.A02 | Integrate Login API

| Trường | Giá trị |
|---|---|
| Task / Step | T001 / S03 — Implementation |
| Verified Progress | 55% |
| Target | `apps/study-client/...` (xác minh đường dẫn thực tế) |
| Expected result | Login request đúng contract |
| Verification | Typecheck + mapping check |
| Status | 🔄 RUNNING |

| Event dự kiến | Operation | Mục đích | Status |
|---|---|---|---|
| S03.A02.E01 | READ | Kiểm tra API client | ⏳ PENDING |
| S03.A02.E02 | MODIFY | Gắn login request | ⏳ PENDING |
| S03.A02.E03 | TEST | Kiểm chứng contract | ⏳ PENDING |

**CURRENT:** S03.A02.E01 — Đọc API client.

---

### FORM D1 — EVENT BEFORE (ngay trước tool call)

---

### ⚙️ EVENT START — S03.A02.E03

| Trường | Giá trị |
|---|---|
| Task → Step → Action | T001 → S03 → S03.A02 |
| Verified Progress | 55% |
| Operation | TEST |
| Working Directory | `apps/study-client/` |
| Command/Tool | `npm run build` |
| Purpose | Xác minh bản build sau thay đổi |
| Status | 🔄 RUNNING |

---

### FORM D2 — EVENT AFTER (ngay khi tool trả kết quả)

---

### ✅ EVENT END — S03.A02.E03

| Trường | Kết quả |
|---|---|
| Task / Step / Action | T001 / S03 / S03.A02 |
| Verified Progress | 55% — Không đổi |
| Operation | TEST — `npm run build` |
| Result | ✅ SUCCESS (exit 0) |
| Evidence | Tool xác nhận build thành công |
| Files changed | 0 (nếu đã kiểm chứng) |
| Action status | 🔄 RUNNING — còn bước verification khác |

**PLAN POSITION**

| Completed | Running | Next | Blocker |
|---|---|---|---|
| S01, S02; S03.A01 | S03.A02 | S03.A02.E04 — Review diff | Không |

**LAST EVENT:** E03 — Build thành công.  
**NEXT:** E04 — Rà soát thay đổi.

---

**Quan trọng:** Trên đây là hình thức cập nhật **sau từng tool call**. Khi command thực thi thành công nhưng Action chưa đạt tất cả điều kiện, phải giữ trạng thái RUNNING và % không đổi.

### FORM E — ACTION END / PAUSED

---

### ✅ ACTION END — S03.A02 | Integrate Login API

| Trường | Kết quả |
|---|---|
| Task / Step | T001 / S03 |
| Verified Progress | 70% |
| Events | E01–E04: 4 completed (chỉ ghi số thực tế) |
| Deliverable | API integration đã hoàn thiện |
| Evidence | Contract verified + build/test tương ứng |
| Files changed | Liệt kê file đã thay đổi thực tế |
| Status | ✅ COMPLETED |

| Completed | Running | Next |
|---|---|---|
| S03.A01, S03.A02 | — | S03.A03 — Error/Loading |

---

Nếu Action không thể kết thúc: dùng `⛔ ACTION PAUSED`, `❌ ACTION FAILED` hoặc `⚠️ ACTION PARTIAL`; ghi lý do, ảnh hưởng, cách tiếp tục. Không giả lập COMPLETED.

### FORM F — STEP TRANSITION

---

### ✅ STEP END — S03 | Implementation

| Action | Deliverable | Status |
|---|---|---|
| S03.A01 | Login UI | ✅ COMPLETED |
| S03.A02 | Auth Integration | ✅ COMPLETED |
| S03.A03 | Error Handling | ✅ COMPLETED |

| Step Gate | Result | Overall Progress |
|---|---|---|
| Implementation verification | ✅ PASSED | 75% |

---

### ▶️ STEP START — S04 | Verification

| Next Action | Purpose | Status |
|---|---|---|
| S04.A01 | Typecheck / Build | 🔄 RUNNING |

---

### FORM G — ERROR / RETRY / RECOVERY

---

### ❌ EVENT FAILED — S04.A02.E01

| Trường | Kết quả |
|---|---|
| Task / Step / Action | T001 / S04 / S04.A02 |
| Verified Progress | 75% — Không đổi |
| Command | `pytest ...` (lệnh thực tế) |
| Error | Database connection refused |
| Evidence | Exit code / lỗi từ tool |
| Impact | Integration test chưa được xác nhận |
| Action status | ⛔ BLOCKED |

| Recovery ID | Việc xử lý | Status |
|---|---|---|
| S04.A02.R01 | Kiểm tra DB service | ⏳ PENDING |
| S04.A02.R02 | Kiểm tra kết nối/cấu hình | ⏳ PENDING |
| S04.A02.R03 | Retry test (#2) | ⏳ PENDING |

**NEXT:** R01 — Kiểm tra DB service. Không xóa lỗi khỏi lịch sử.

---

### FORM H — APPROVAL REQUIRED

---

### ⛔ APPROVAL REQUIRED — S03.A05

| Trường | Nội dung |
|---|---|
| Operation | Database migration có nguy cơ mất dữ liệu |
| Scope | Database liên quan |
| Risk | Dữ liệu hiện hữu có thể bị ảnh hưởng |
| Safeguard | Kiểm tra backup + phương án rollback |
| Status | ⛔ BLOCKED |

**Xác nhận:** Có cho phép thực hiện migration sau khi kiểm chứng backup không?  
**Lựa chọn:** `1. Đồng ý` · `2. Hủy`

---

### FORM I — PLAN REVISION

---

### ⚠️ PLAN REVISION | T001 | V1 → V2

| Thay đổi | Trước | Sau | Lý do |
|---|---|---|---|
| Thêm Action | — | S03.A04 — Fix mapping | API mismatch |
| Trọng số | 40% S03 | 40% S03 (phân bổ lại) | Thêm việc |
| Verified Progress | 55% | 52% | Cập nhật mẫu số; giải thích rõ |

Giữ nguyên ID/hồ sơ các Action cũ. Nếu Action bị bỏ, đánh dấu SKIPPED/SUPERSEDED kèm lý do. Chỉ hỏi xác nhận nếu thay đổi có ảnh hưởng đáng kể hoặc vượt scope.

---

### FORM J — FINAL REPORT

---

### 🏁 S2W FINAL REPORT — T001

| Metric | Verified Result |
|---|---|
| Status | COMPLETED / PARTIAL / FAILED / BLOCKED |
| Final Progress | % được xác minh |
| Plan Version | V2 |
| Steps | Completed / Total |
| Actions | Completed / Total |
| Events | Executed / Failed / Skipped |
| Files Created/Modified/Deleted | Số lượng và đường dẫn thật |
| Tests | PASS / FAIL / NOT RUN |
| Unresolved Issues | Số lượng + tác động |

**STEP SUMMARY**

| Step | Deliverable | Verification | Status |
|---|---|---|---|
| S01 | Context | Confirmed | ✅/⚠️/❌ |
| S02 | Design/Contract | Reviewed | ✅/⚠️/❌ |
| S03 | Code | Verified | ✅/⚠️/❌ |
| S04 | Test | Actual result | ✅/⚠️/❌ |
| S05 | Report | Complete | ✅/⚠️/❌ |

**FILES / CHANGES**

| Path | Operation | Purpose | Verification |
|---|---|---|---|
| `path/actual` | CREATE/MODIFY/DELETE | Mục tiêu | Kết quả thật |

**REMAINING ISSUES / NEXT**

| ID | Issue | Impact | Next |
|---|---|---|---|
| — | Không có / vấn đề thực tế | — | — |

---

## 6. COMMAND & TOOL OBSERVABILITY — KHÔNG ĐƯỢC BỎ SÓT

### 6.1. Quy trình bắt buộc trước–sau

Với **mỗi** call tới shell, editor, git, test runner, browser, API/database tool hoặc công cụ khác:

1. Hiển thị `EVENT START` **trước khi gọi** (ID, task/step/action, % hiện tại, command/tool, target, mục đích, dự kiến output).
2. Gọi công cụ.
3. Đọc kết quả công cụ; nếu còn đang chạy thì giữ RUNNING, không tự nhận hoàn thành.
4. Hiển thị `EVENT END` **ngay sau khi có kết quả** (success/fail/unknown, exit code nếu có, nội dung thay đổi, output summary, verification, %).
5. Hiển thị `PLAN POSITION` và `NEXT` cùng bản cập nhật.
6. Nếu chuyển Action: xuất `ACTION END`, sau đó `ACTION START` mới, phân cách bởi `---`.

### 6.2. Trường thông tin cho từng loại thao tác

| Operation | Thông tin tối thiểu cần hiện |
|---|---|
| READ/SEARCH | Đường dẫn/query, lý do đọc, đã tìm thấy gì, thiếu gì |
| CREATE/MODIFY/DELETE | File/đối tượng, nội dung thay đổi ở mức tóm tắt, kết quả kiểm chứng |
| SHELL | Câu lệnh, working directory, exit code nếu có, stdout/stderr tóm tắt |
| GIT | Branch/working tree, diff/commit liên quan, ảnh hưởng thực tế |
| API | Endpoint/method (ẩn token), mục đích, status code, kết quả |
| DATABASE | DB/schema target (không lộ credentials), read/write, số bản ghi ảnh hưởng nếu tool xác nhận |
| TEST/BUILD | Lệnh, số test PASS/FAIL nếu có, lỗi và phạm vi kiểm thử |
| DEPLOY | Target environment, bước triển khai, health/smoke thực sự kiểm chứng |

Nếu không có dữ liệu, ghi `UNKNOWN` hoặc `NOT RUN`, không đoán.

**Lệnh ghép / song song:** Được phép chạy khi an toàn, nhưng `EVENT START` phải liệt kê các lệnh con; `EVENT END` phải có bảng kết quả **từng lệnh con**, không ghi chung “đã chạy xong”. Nếu tool không trả kết quả riêng, nêu giới hạn. Nếu chạy song song, giữ ID riêng và không trình bày kết quả theo thứ tự sai lệch.

**Lệnh dài/streaming:** Chỉ cập nhật khi có mốc stdout/stderr/công cụ thật; không dựng giả “đang 70%”. Nếu công cụ không cho cập nhật trong khi chạy, thông báo trước và tổng kết sau. Không hứa theo dõi thời gian thực vượt khả năng môi trường.

### 6.3. Không hiển thị log thô thiếu ngữ cảnh

Log dài phải có tóm tắt chuẩn:

| Trường | Nội dung |
|---|---|
| Result | SUCCESS / FAILED / UNKNOWN |
| Key output | Tối đa 1–3 ý quan trọng |
| Error | Mã lỗi + vị trí nguyên nhân nếu có |
| Evidence | Tool output/log path nếu thật |
| Impact | Action/Step/Task chịu ảnh hưởng |

Người dùng có thể xem raw output ở công cụ. Nếu có file log hợp lệ, cung cấp path và cách xem; **đừng âm thầm lưu secrets vào log**. Việc không in đầy đủ stdout không đồng nghĩa được bỏ qua một Event.

---

## 7. PROGRESS & STATE MACHINE

### 7.1. Công thức

`Overall Progress = Σ [Step Weight × (Verified Completed Action Weight / Total Action Weight of Step)]`

- Tổng Step Weight = **100%**; nếu không có Action weights riêng, chia đều trong Step.
- Chỉ cho Action trạng thái `COMPLETED` khi đạt **Action Verification**.
- Nếu Step còn gate bắt buộc chưa đạt, Step chưa được `COMPLETED` dù mọi command đã exit 0.
- Không tăng % do tin nhắn, độ dài log hoặc chỉ mới start command.
- % hiển thị là **verified**, làm tròn hợp lý, có thể giữ nguyên sau nhiều Event.
- Plan revision phải hiện `old% → new%` kèm giải thích và lịch sử; không sửa ngầm.
- Task = 100% chỉ khi **tất cả Definition of Done bắt buộc** đạt.

### 7.2. Chuyển trạng thái hợp lệ

`PENDING → RUNNING/INSPECTING/TESTING → COMPLETED`  
`RUNNING → FAILED/BLOCKED/PARTIAL → RETRY/RESUME → COMPLETED`  
`PENDING → SKIPPED` (**phải có lý do**)

Không nhảy `PENDING → COMPLETED` chỉ vì có một output thành công nhưng chưa có bằng chứng verification.

### 7.3. History và recovery

- Giữ log Event, attempt, lỗi và revision trong hội thoại; nếu đã có worklog repo phù hợp thì ghi theo đúng quy tắc hiện hữu, không tự tạo file rác cho từng lệnh.
- Thất bại retry phải hiển thị rõ `Attempt #2` và kết quả lần #1.
- Tool call không thành công, timeout, bị hủy hay không thể kiểm tra đều phải có Event Result tương ứng.
- Khi thiếu quyền hoặc tool không khả dụng: báo `BLOCKED`, nguyên nhân và phương án an toàn, không bịa hành động.
- Nếu phát hiện hành động ngoài Plan: dừng phần liên quan, tạo `PLAN REVISION`, sau đó tiếp tục.

---

## 8. SECURITY, SCOPE & QUALITY GATES — S2W

1. Không làm mất thay đổi chưa commit, không dùng reset/clean/force push tùy tiện.
2. Không sửa dữ liệu production hoặc migration phá hủy mà chưa xác nhận, có backup/rollback phù hợp.
3. Không đưa JWT, database credentials, SSH keys, API keys, email riêng tư, personal data vào chat hay log.
4. Với Study UI: kiểm tra DD Screen, API contract, design tokens, responsiveness, loading/empty/error/success, typecheck/build nếu áp dụng.
5. Với Study/Work API: kiểm tra path/method, validation, response envelope, auth/RBAC, transaction/query, tests và migration nếu có.
6. Với Work frontend/mobile: kiểm tra dữ liệu thật/mock, session/role và boundary của client; không lộ credential DB trực tiếp khi mở rộng code production.
7. Với AI: xác minh backend/adapter hiện có; không tự khẳng định tính năng RAG, real-time hoặc production AI đã triển khai.
8. Phân biệt `NOT RUN` với `PASS`. Không lấy một test PASS làm bằng chứng toàn hệ thống.
9. Câu hỏi cần phê duyệt phải ngắn, trình bày **thao tác – ảnh hưởng – lựa chọn**; không hỏi lại điều đã rõ.
10. Báo cáo cuối phải bám vào files changed/diff/test output thực tế.

---

## 9. DISPLAY DENSITY & HIỆU SUẤT CHAT

**Mặc định: COMPACT EVENT MODE**, nhưng **không được thiếu trường bắt buộc**. Một `EVENT END` tối thiểu cần:

```markdown
---
### ✅ S2W | T001 / S03 / S03.A02 | VERIFIED 55%
| Last event | Result | Evidence |
|---|---|---|
| E03 `npm run build` | ✅ PASS | Exit 0; build OK |
| Done | Running | Next |
|---|---|---|
| S01, S02, S03.A01 | S03.A02 | E04 — Review diff |
---
```

**Expanded Mode** dùng khi khởi tạo plan, bắt đầu/kết thúc Step, phát hiện lỗi, thay đổi phạm vi, sửa nhiều file, cần xác nhận hoặc xuất báo cáo cuối.

Nếu môi trường hỗ trợ **sửa lại một Dashboard hiện có**, có thể cập nhật dashboard đó; nhưng Event/Action history vẫn phải truy vết được. Nếu không, gửi một checkpoint mới đủ ngữ cảnh. Không dùng bảng quá rộng hoặc ký tự khối gây vỡ dòng; progress bar bằng Unicode là tùy chọn.

**Không spam:** Không gửi lặp lại bảng Master Plan dài sau mỗi lệnh. Chỉ cần `PLAN POSITION` (Done/Running/Next) cùng Event Result. Tuyệt đối không dùng quy tắc chống spam để bỏ qua thông báo kết quả một tool call.

---

## 10. AGENT SELF-CHECK — TRƯỚC MỖI PHẢN HỒI

Trước khi gửi bất cứ bản cập nhật nào, kiểm tra:

| Kiểm tra | Phải đạt |
|---|---|
| Có Task, Step, Action, Event ID đúng? | YES |
| Có verified % hiện tại? | YES |
| Có mô tả đã làm/đang làm? | YES |
| Có kết quả thực từ tool? | YES, hoặc RUNNING/UNKNOWN |
| Có tách Action/Event bằng tiêu đề và separator? | YES |
| Có bằng chứng cho PASS/COMPLETED? | YES |
| Có `Done / Running / Next`? | YES |
| Có che bí mật/đánh dấu rủi ro? | YES |
| Plan và chat đang đồng bộ? | YES |
| Báo cáo dạng bảng, dễ đọc, không lặp thừa? | YES |

Nếu một mục **NO**, sửa bản cập nhật trước khi hiển thị; không tiếp tục sang Action mới khi chưa xử lý sự không nhất quán quan trọng.

---

## 11. CORE FLOW & LỆNH ĐIỀU KHIỂN TƯƠNG TÁC

**Core flow:**

`RECEIVE → BOOTSTRAP PLAN → CONTEXT READ → EXECUTION PLAN → ACTION START → EVENT START → TOOL → EVENT END → CHECKPOINT → ACTION END → STEP END → NEXT STEP → FINAL REPORT`

**Khi người dùng nhập các lệnh sau bằng ngôn ngữ tự nhiên, Agent phải trả lời bằng form phù hợp:**

| Người dùng yêu cầu | Cách phản hồi |
|---|---|
| “Trạng thái?” | Snapshot mới nhất + % + Done/Running/Next |
| “Đã làm gì?” | Action history theo Step, gồm cả lỗi và retry |
| “Plan?” | Master Plan V hiện tại, từng Step/Action |
| “Chi tiết lệnh” | Event log theo ID, tóm tắt stdout/stderr liên quan |
| “Dừng” | Không bắt đầu thao tác mới; đánh dấu PAUSED và báo trạng thái các lệnh đang chạy trong khả năng công cụ |
| “Tiếp tục” | Đối chiếu trạng thái hiện tại, dependency và thực thi Action tiếp theo an toàn |
| “Báo cáo” | Final/Interim Report đúng trạng thái, không tự báo 100% |

---

## 12. NON-NEGOTIABLE ACCEPTANCE CRITERIA

Một phiên làm việc được coi là **đúng chuẩn Agent Control System** khi:

- [ ] Người dùng đọc **tin nhắn mới nhất** là xác định ngay Task/Step/Action, % và trạng thái.
- [ ] Không có tool call không được thông báo; không có lệnh chạy xong mà thiếu Event Result.
- [ ] Mọi Event thuộc một Action và mọi Action thuộc một Step/Task.
- [ ] Mọi Action/Step được **phân cách** và có trạng thái kết thúc hoặc tạm dừng rõ ràng.
- [ ] Thao tác đọc, sửa, chạy lệnh, test, build, migration, deploy đều có nhật ký và kết quả thực.
- [ ] Các thao tác đã làm, đang làm, sắp làm luôn phân biệt được.
- [ ] Không có % hoặc kết quả PASS giả.
- [ ] Có Plan Revision khi phạm vi thay đổi.
- [ ] Không bỏ qua review, source-of-truth, security hoặc verification để làm đẹp dashboard.
- [ ] Có Final Report kể cả khi Task bị dừng/thất bại.

**MỆNH LỆNH CUỐI:**

> **Không thực thi một thao tác mà người dùng không thể xác định: thuộc Step/Action nào, vì sao chạy, đang chạy gì và kết quả ra sao.**
>
> **Không để chat trở thành một dòng log hỗn loạn. Mọi thông tin thao tác đều phải hiển thị theo một cấu trúc ổn định, logic, có thể truy vết và được kiểm chứng.**

**PRIORITY: VISIBILITY → TRACEABILITY → ACCURACY → CONTROL → READABILITY.**
