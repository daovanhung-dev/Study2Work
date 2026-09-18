# 05 — Viết List_Features.md

## Tiêu chí tách feature

Tách thành feature riêng khi có ít nhất một điều kiện:

- Business goal khác.
- Actor hoặc permission khác.
- Primary view/flow khác.
- Business rule khác đáng kể.
- Có thể test, release hoặc feature-flag độc lập.
- Có event/side effect độc lập.

Một nút nhỏ dùng chung goal và flow không tự động trở thành feature mới.

## Mỗi feature phải có

- Goal và boundary.
- Actor chính/phụ, trigger.
- Preconditions/postconditions.
- Related requirement, rule, function, view, entity, API/event.
- Happy path theo bước.
- Alternate và error flows.
- Validation và authorization.
- Acceptance criteria có thể test.
- Dependency, risk và open question.

## Acceptance criteria

Viết theo dạng điều kiện–hành động–kết quả. Nêu rõ khi rule vi phạm thì dữ liệu
có được ghi hay rollback, UI/API trả gì và test nào chứng minh.
