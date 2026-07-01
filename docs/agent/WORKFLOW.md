# Agent Workflow

Tài liệu này chuẩn hóa cách AI coding agent bắt đầu phiên, đọc context, coding, test, fix bug và ghi lại dấu vết.

## 1. Bắt Đầu Mỗi Phiên

1. Đọc `AGENTS.md`.
2. Đọc `docs/agent/CONTEXT_INDEX.md`.
3. Đọc `docs/worklog/INDEX.md`.
4. Xác định module, feature/function và loại task: BD, DD, coding, test, fix bug, refactor, docs.
5. Chọn tối đa 10 worklog gần nhất theo index.
6. Chỉ mở đầy đủ tối đa 5 worklog liên quan trực tiếp đến module/bug hiện tại.
7. Kiểm tra checklist module tương ứng trong `docs/checklists/`.
8. Đọc BD, DD, skill và file code liên quan theo docs map.
9. Tóm tắt ngắn trước khi coding: module, BD/DD nguồn, trạng thái, rủi ro, file dự kiến sửa, test dự kiến chạy.

## 2. Trước Khi Coding

Không bắt đầu coding nếu chưa có đủ:

- Module, feature/function và user role bị ảnh hưởng.
- BD liên quan, tối thiểu `docs/BD/Study2Work_Study_BD_Codex_Ready.md`.
- DD liên quan nếu task triển khai theo DD; không coding DD `DRAFT`/`IN_REVIEW` nếu chưa được yêu cầu prototype.
- Checklist module.
- Skill liên quan nếu `docs/skills/INDEX.md` chỉ ra.
- File code, database/API/UI/test bị ảnh hưởng.
- Plan ngắn theo dependency.
- Test/check dự kiến chạy.

Nếu thiếu business rule hoặc có mâu thuẫn tài liệu, ghi `OPEN_QUESTION` hoặc `CONFLICT`; không tự bịa yêu cầu.

## 3. Sau Khi Coding

Sau mọi thay đổi code:

1. Chạy test/lint/build hoặc kiểm tra phù hợp với môi trường hiện có.
2. Không tuyên bố đã test nếu không có output/evidence.
3. Tạo worklog mới tại `docs/worklog/YYYY-MM/<SESSION_NO>_<TASK_SLUG>.md`.
4. Cập nhật `docs/worklog/INDEX.md`.
5. Cập nhật checklist module: coding status, test status, bug status, worklog link, evidence.
6. Nếu thiết kế đổi, cập nhật DD changelog hoặc tạo `OPEN_QUESTION`.
7. Nếu phát hiện lặp lại, đánh giá có cần tạo/cập nhật skill.

## 4. Worklog Bắt Buộc

Mỗi worklog phải có:

- Session number.
- Thời gian.
- Module/feature/function.
- Mục tiêu phiên làm việc.
- BD/DD/checklist/skill đã đọc.
- File đã tạo hoặc sửa.
- Logic đã thay đổi.
- Test đã chạy và kết quả.
- Bug phát hiện.
- Rủi ro hoặc điểm chưa xác minh.
- Việc tiếp theo.
- Commit message đề xuất.

## 5. Tạo DD Và Checklist

Khi tạo DD mới cho module:

1. Xác định `MODULE_CODE`.
2. Dùng `docs/DD/DD_Module_Creation_Guide_EN.md` và `docs/DD/DD_Module_Template/`.
3. Tạo hoặc cập nhật `docs/checklists/<MODULE_CODE>.md`.
4. Checklist phải có ID, status, updated date và link đến DD/worklog/issue/evidence cho từng hạng mục.
5. Không tạo checklist trùng module.

## 6. Tạo Skill

Kiểm tra 10 worklog gần nhất. Tạo skill tại `docs/skills/<SKILL_ID>.md` khi có ít nhất một điều kiện:

- Cùng quy trình thủ công xuất hiện từ 2 phiên trở lên.
- Cùng lỗi hoặc cách fix lặp lại từ 2 lần trở lên.
- Thao tác phức tạp, nhiều bước, có thể tái sử dụng.
- Lỗi từng tốn nhiều token hoặc gây lệch kiến trúc đáng kể.

Không tạo skill cho việc nhỏ, một lần hoặc không tái sử dụng.

## 7. Retrospective

Sau mỗi 30 session mới kể từ retrospective gần nhất:

1. Tạo `docs/retrospectives/RETRO_<START_SESSION>_<END_SESSION>.md`.
2. Tổng hợp từ `docs/worklog/INDEX.md`, checklist module và các worklog có risk.
3. Không đọc lại toàn bộ 30 worklog đầy đủ nếu không cần.
4. Cập nhật `AGENTS.md` hoặc `docs/agent/` chỉ khi cải tiến ổn định và tái sử dụng.

## 8. Evidence Rules

- `VERIFIED` yêu cầu evidence rõ: command output, test report, screenshot, reviewer confirmation, issue link hoặc worklog ghi rõ kiểm tra.
- `DONE` yêu cầu code/test/docs/checklist/worklog hoàn tất cho phạm vi task.
- Nếu command không tồn tại do repo chưa cấu hình, ghi `BLOCKED` hoặc `OPEN_QUESTION`, không bịa command thay thế.
