# 12 — Agent Runbook

## Prompt contract

Agent phải nhận được:

- BD/BRD path hoặc explicit business request.
- Module code/name và target DD path.
- Dependent modules nếu đã biết.
- Current source baseline nếu claim implementation.

## Execution order

1. Đọc `SKILL.md` và reference cần thiết.
2. Tạo extraction sheet và liệt kê open questions.
3. Tạo skeleton từ `template/`.
4. Viết `Overall.md` trước.
5. Viết Features → Functions → Views → Import/File.
6. Thêm diagrams/assets/history khi có giá trị.
7. Chạy validator và review checklist.
8. Tạo worklog, refresh history và chạy docs validation.

## Stop conditions

Agent phải dừng trước khi tự quyết nếu thiếu quyết định làm thay đổi business
behavior, access/security, schema/RLS, payment/quota, AI safety hoặc acceptance.
Agent có thể tiếp tục bằng cách ghi `OPEN QUESTION`, `ASSUMPTION` hoặc `PROPOSAL`
ở đúng ID và không claim Approved.

## Handoff sau DD

Khi DD được chấp nhận, chuyển sang workflow `coding`. Coding agent phải đọc toàn
bộ DD module, liệt kê affected IDs, bám Import_File và cập nhật changelog nếu
implementation làm thay đổi design.
