# Study2Work agent router

Đây là điểm vào bắt buộc cho coding agent. File này chỉ định tuyến; context chi tiết nằm trong `.agents/`. Source hiện tại luôn phải được kiểm tra lại trước khi sửa.

## 1. Phân loại task

Trước khi đọc sâu, ghi ngắn vào worklog của task; không đăng phân loại này lên chat:

```text
primary_task_type: coding | fix | docs | test | review
secondary_task_types:
  - <loại khác, nếu có>
project_scopes:
  - mobile-work | web-work | server-work | server-study | server-ai | db-admin
cross_scope_dependencies:
  - <contract/path nối các scope, nếu có>
```

- `coding`: requirement/contract -> pattern hiện có -> implementation -> test.
- `fix`: reproduce -> trace caller/callee/effect -> root cause -> smallest fix -> regression test.
- `docs`: source -> verified tests/contracts -> tài liệu hiện có -> cập nhật.
- `test`: requirement/contract -> implementation -> edge cases -> convention test.
- `review`: yêu cầu -> diff hoặc path được nêu -> rule/contract/source/test
  evidence của scope -> báo cáo chỉ đọc; không sửa code hoặc chạy test.

Một task có thể có nhiều `project_scopes`. Không ép task cross-scope vào một scope duy nhất.

## 1.1. Theo dõi target và giao tiếp

`.agents/target.md` là nguồn tiến độ duy nhất và chỉ chứa bảng ba cột `STT`,
`Tên target`, `Tiến độ hoàn thiện`. Mỗi hàng phải là một mục tiêu lá: một thao
tác nhỏ nhất có thể xác minh độc lập, diễn đạt bằng một hành động và một kết
quả. Tách riêng các thao tác có thể hoàn thành hoặc xác minh riêng; không dùng
mục tiêu bao trùm như “hoàn thiện màn hình/module”. Kế hoạch lá và bằng chứng
nghiệm thu nằm trong worklog. Xem `.agents/project/agent-control.md`.

Sau khi nhận task, không tự gửi nội dung vào chat: không bình luận, tiến độ,
receipt, kế hoạch, tóm tắt đọc/thao tác, kết quả hay báo cáo hoàn tất. Chỉ phản
hồi khi người dùng yêu cầu trả lời cụ thể, cần câu hỏi tối thiểu để gỡ blocker,
hoặc system/developer/tool cấp cao hơn bắt buộc.

Phân loại task, lựa chọn scope và bằng chứng công việc được ghi trong worklog,
không công bố thành milestone chat. Worklog lưu nguồn, thay đổi, xác minh và
lịch sử cập nhật target; không dùng `MILESTONES` làm nguồn tiến độ thứ hai.

## 2. Định tuyến scope

| Scope | Source chính | Đọc tiếp |
|---|---|---|
| `mobile-work` | `apps/work-client/mobile/` | `.agents/mobile-work/AGENTS.md` |
| `web-work` | `apps/study-client/`, `apps/work-client/web/` | `.agents/web-work/AGENTS.md` |
| `server-work` | `apps/work-server/` | `.agents/server-work/AGENTS.md` |
| `server-study` | `apps/study-server/` | `.agents/server-study/AGENTS.md` |
| `server-ai` | `apps/ai-server/` | `.agents/server-ai/AGENTS.md` |
| `db-admin` | `apps/db-admin-web/`, `apps/db-admin-server/` | `.agents/db-admin/AGENTS.md` |

Không nạp scope khác nếu chưa có dependency thật. Task qua nhiều scope phải ghi contract nối giữa chúng; ví dụ Study -> Work event dùng `contracts/events/study-work/`.

## 2.1. Khai báo read-set trước khi đọc

Mọi nội dung file được agent mở hoặc tìm kiếm phải có trong `READ_PLAN` trước
khi đọc, kèm path, phần cần đọc và lý do gắn với task. Read-set khởi động gồm
các path router bắt buộc; ghi lại chúng vào worklog ngay khi worklog được tạo.
Root `AGENTS.md` đã được cấp trong task context nên không đọc lại trừ khi task
sửa chính file này. Bootstrap allowlist: `.agents/AGENTS.md`,
`.agents/context-map.md`, `.agents/context-manifest.json`,
`.agents/project/agent-control.md`, `.agents/target.md`,
`.agents/worklog/README.md`, `.agents/worklog/TEMPLATE.md`,
`scripts/select-worklogs.mjs`. Chỉ đọc phần liên quan trong từng path; sau đó
không đọc path ngoài danh sách nếu chưa thêm vào `READ_PLAN`.

Selector worklog chỉ trả metadata/path. Thêm path được chọn vào `READ_PLAN`
trước khi mở nội dung log. Khi context map/manifest phát hiện dependency mới,
thêm path và mục đích trước khi đọc. Mọi lệnh tìm kiếm nội dung cũng phải giới
hạn trong path đã khai báo. Không quét repository rộng, không đọc trọn file lớn
khi chỉ cần đoạn liên quan, và dừng khi đã đủ bằng chứng.

## 2.2. Luồng context chuẩn

```text
AGENTS.md
  -> classify task from request and supplied router context
  -> declare the bootstrap read-set before opening repository file content
  -> .agents/AGENTS.md
  -> .agents/context-map.md
  -> .agents/context-manifest.json and agent-control sections in read-set
  -> tạo worklog có READ_PLAN + LEAF_TARGET_PLAN
  -> scripts/select-worklogs.mjs --type <primary_task_type> --limit 3
  -> thêm path worklog được chọn vào READ_PLAN trước khi đọc nội dung
  -> đọc worklog được chọn; nếu thiếu thì ghi shortage, không mở log khác type
  -> .agents/project/INDEX.md (chỉ khi có boundary/contract cross-scope)
  -> scope AGENTS.md
  -> scope INDEX.md hoặc subcontext INDEX.md
  -> khai báo path source + contract/config/test trước khi đọc đoạn cần thiết
  -> worklog cập nhật trước và sau verification
```

`context-map.md` là bước load bắt buộc để hiểu page graph, scope boundary,
skill/workflow/contract wiring trước khi chọn context cụ thể. Worklog phải chứa
`READ_PLAN` và `LEAF_TARGET_PLAN`. Selector chỉ chọn đường dẫn; sau khi ghi các
path vào `READ_PLAN`, agent đọc đúng các log được chọn và ghi carry-forward facts
trong `PRIOR_WORKLOG_REVIEW`. Quy tắc match dùng `primary_task_type` chính xác;
nếu thiếu log thì ghi số lượng thiếu, không đọc log loại khác.

Skill, workflow và contract phải được tra trong machine-readable registry của
`.agents/context-manifest.json`; không coi file tồn tại là bằng chứng đã được
wire. Task DD phải chọn skill theo boundary: `create-dd-from-bd-mobile` cho
Mobile/Flutter module DD, `createDD-markdown` cho Web/API DD. Web UI-only DD
chưa có skill canonical. Với yêu cầu review code/PR/diff hoặc audit path/module,
chỉ kích hoạt theo yêu cầu của người dùng và load `code-review` cùng workflow
tương ứng trước khi review; skill này áp dụng cho cả sáu code scope và không
được sửa code, chạy test, đổi Git state hoặc đăng nhận xét lên PR.

## 3. Progressive loading

```text
AGENTS.md
  -> .agents/<scope>/AGENTS.md
  -> module/API/core/service context được scope chỉ định
  -> exact source + tests + config/contract liên quan
```

Không đọc toàn repository cho task cục bộ. Chỉ mở `.agents/project/*` khi task qua nhiều app, cần ownership/global convention, hoặc đang bảo trì chính context.

## 4. Expected behavior và current behavior

Hai loại bằng chứng phải được giữ tách biệt.

### Expected behavior

1. Yêu cầu mới nhất của người dùng.
2. Canonical DD/API contract còn tồn tại.
3. Approved business rule / implementation plan.

### Current behavior

1. Runtime/source code hiện tại.
2. Test đã thực sự xác minh/runnable.
3. Executable contract/config hiện hành.

Nếu hai phía khác nhau, ghi `DISCREPANCY`; không tự reconcile bằng suy đoán. Khi mô tả hiện trạng, ưu tiên `current source > verified runnable tests > documentation`.

## 5. Luật bắt buộc

- Không tự tạo API, field, table, validation, service, business code hoặc HTTP behavior khi chưa có bằng chứng.
- Trước khi sửa function, trace caller, callee, DB/side effect, response, business code và test bị ảnh hưởng.
- Chỉ sửa file tối thiểu; không refactor ngoài phạm vi.
- Không ép architecture của một server lên server khác.
- `VERIFIED`, `UNWIRED`, `DECLARED_NOT_RUNNABLE`, `NOT_FOUND` là trạng thái có nghĩa; file tồn tại không đồng nghĩa runtime dùng file đó.
- Nếu code/contract/DB/convention thay đổi theo cách làm context sai, cập nhật đúng page `.agents/` trong cùng task.
- Mọi task phải có preflight đọc worklog cùng `primary_task_type` trước khi làm việc; dùng `.agents/worklog/README.md` và `scripts/select-worklogs.mjs`.
- Trước khi kết thúc task có thay đổi context, chạy `node scripts/validate-agent-context.mjs`.
