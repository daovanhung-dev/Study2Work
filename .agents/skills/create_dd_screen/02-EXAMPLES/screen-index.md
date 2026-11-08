# Screen Index — Examples (Demo)

| Screen | Tên | Route | Module | Trạng thái | Liên kết |
|---|---|---|---|---|---|
| `SH-01` | Danh sách khóa học | `/courses` | Study | Đầy đủ minh họa, chưa xác minh sản phẩm | [Overview](SH-01-CourseList/00-overview.md) |
| `SH-02` | Chi tiết khóa học | `/courses/:courseId` | Study | Đầy đủ minh họa, chưa xác minh sản phẩm | [Overview](SH-02-CourseDetail/00-overview.md) |

## Quan hệ

```mermaid
flowchart LR
  A[SH-01 Course List] -->|EV-004 / courseId| B[SH-02 Course Detail]
  B -->|EV-002 / back| A
  B -->|EV-004 anonymous| C[Login - ngoài bộ demo]
  C -->|returnUrl| B
```

**Chú ý:** bộ 2 screen demo minh họa cách viết DD, **không phải** thiết kế đã xác nhận từ code/base sản phẩm thật.
