# 00 — Read First và Routing

## Mục tiêu

Xác định đúng loại công việc, nguồn đầu vào và mức context cần đọc trước khi
chạm vào DD. Mục tiêu là đủ bằng chứng để viết đúng, không đọc lan sang toàn bộ
source không liên quan.

## Preflight

1. Xác nhận workspace NanoBio/BioAI và branch hiện tại.
2. Xác định người dùng muốn tạo mới, cập nhật, review hay chỉ đọc DD.
3. Chọn một workflow chính: `docs-dd`; không trộn coding nếu chưa được yêu cầu.
4. Xác định module code, BD/BRD path và dependent modules.
5. Đọc project map, DD guide, template, checklist và domain cần thiết.
6. Nếu chỉ có tên module, tìm trong `docs/BD/`; chỉ hỏi khi còn nhiều nguồn hợp lý.

## Khi tạo mới DD

Đọc theo thứ tự:

1. BD/BRD nguồn.
2. Acceptance criteria, use case và requirement liên quan.
3. DD của dependency trực tiếp.
4. Source/schema/API hiện hành nếu cần xác nhận implementation boundary.
5. Issue, worklog hoặc ADR chỉ khi cần giải thích quyết định.

## Khi update DD

Bắt đầu từ thay đổi mới nhất, rồi lần ngược tới `Overall.md`, feature/function/view
và Import/File map bị ảnh hưởng. Không viết lại các phần không chịu ảnh hưởng.

## Điểm dừng an toàn

Dừng viết và ghi open question khi thiếu một trong các thông tin ảnh hưởng
trực tiếp tới scope, quyền, state transition, dữ liệu nhạy cảm, thanh toán,
quota, RLS, AI safety hoặc acceptance criteria.
