# Skills Index

Skill là hướng dẫn tái sử dụng cho quy trình/lỗi lặp lại. Không tạo skill khi chưa có evidence từ worklog.

## Creation Rule

Kiểm tra 10 worklog gần nhất. Tạo `docs/skills/<SKILL_ID>.md` khi có ít nhất một điều kiện:

- Cùng quy trình thủ công xuất hiện từ 2 phiên trở lên.
- Cùng lỗi hoặc cách fix lặp lại từ 2 lần trở lên.
- Thao tác phức tạp, nhiều bước và tái sử dụng được cho module khác.
- Một lỗi từng tốn nhiều token hoặc gây sai lệch kiến trúc đáng kể.

Không tạo skill cho việc quá nhỏ, chỉ dùng một lần hoặc không tái sử dụng.

## Skill Table

| Skill ID | Status | Created | Updated | Related modules | Trigger | Worklog evidence | File |
|---|---|---|---|---|---|---|---|
| _none_ | `NOT_STARTED` | 2026-07-01 | 2026-07-01 | _none_ | No repeated worklog evidence yet. | _none_ | _none_ |

## Required Skill Template

```md
# Skill — <SKILL_ID>

## Mục Tiêu

<What this skill helps repeat safely.>

## Khi Nào Dùng

<Trigger conditions.>

## Điều Kiện Đầu Vào

- <Input/precondition>

## File/Tài Liệu Cần Đọc

- <Path>

## Các Bước Thực Hiện

1. <Step>

## Quy Tắc Không Được Vi Phạm

- <Rule>

## Cách Kiểm Tra Kết Quả

- <Check/evidence>

## Ví Dụ Ngắn

<Example>

## Liên Kết Worklog/Bug

- <Worklog or bug link>
```

## Update Rule

Sau khi tạo hoặc sửa skill, cập nhật bảng `Skill Table` và link skill trong checklist module liên quan.
