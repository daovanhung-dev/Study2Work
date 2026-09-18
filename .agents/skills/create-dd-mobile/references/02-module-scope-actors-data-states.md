# 02 — Scope, Actor, Data, State và Rule

## Chốt ranh giới trước feature

`Overall.md` phải trả lời rõ:

- Module giải quyết vấn đề gì?
- Module sở hữu capability nào?
- Capability nào thuộc module khác?
- Role nào được làm gì và bị giới hạn gì?
- Dữ liệu nào module sở hữu, đọc, ghi hoặc chỉ hiển thị?
- Entity có state nào và điều kiện chuyển state là gì?
- Side effect nào xảy ra sau commit?

## Scope table

| Nhóm | In scope | Out of scope | Owner ngoài module |
|---|---|---|---|
| Business | Capability module sở hữu | Capability khác | Module/system phụ trách |
| Data | Entity/module-owned data | Data chỉ đọc hoặc nhạy cảm ngoài quyền | Data owner |
| UI | View và action thuộc flow | Màn hình dependency | Module UI owner |
| Integration | Contract module gọi | Internal implementation của dependency | Integration owner |

## State rule

Mỗi state transition cần có:

- State hiện tại.
- Action/event.
- State mới.
- Role/system được phép.
- Điều kiện và business rule.
- Dữ liệu thay đổi.
- Failure/rollback behavior.

Không dùng các từ mơ hồ như “xử lý”, “hợp lệ”, “đủ” nếu không có điều kiện
đo được hoặc cách kiểm tra.
