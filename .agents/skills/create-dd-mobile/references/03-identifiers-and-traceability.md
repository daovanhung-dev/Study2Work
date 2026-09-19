# 03 — Identifier và Traceability

## Quy ước ID

| Loại | Pattern |
|---|---|
| Module | `MODULE_CODE` |
| Feature | `MODULE-Fxx` |
| Function | `MODULE-FNxx` |
| View | `MODULE-Vxx` |
| Business rule | `MODULE-BRxx` |
| API | `MODULE-APIxx` |
| Entity | `MODULE-E-name` |
| Event | `MODULE-EVxx` |
| ADR | `MODULE-ADRxx` |
| Test case | `MODULE-TCxx` |

ID phải ổn định qua revision. Không tái sử dụng ID cũ cho nội dung khác; nếu
item bị loại bỏ, ghi lịch sử hoặc deprecated thay vì renumber toàn bộ.

## Traceability matrix

Mỗi requirement có đường đi tối thiểu:

```text
BD requirement
  → feature
  → function/API/business rule
  → view/component
  → source/import dependency
  → test case
```

Cross-link ở cả inventory và phần chi tiết. Không để bảng traceability chỉ chứa
ID không được định nghĩa ở file tương ứng.

## Review nhanh

- Không trùng ID trong cùng module.
- Mỗi feature có actor, trigger, precondition, postcondition và AC.
- Mỗi function có input/output, rule, permission, transaction/idempotency, lỗi và test.
- Mỗi view có action mapping và Loading/Empty/Error/Success/Forbidden.
- Open question liên kết tới item bị ảnh hưởng.
