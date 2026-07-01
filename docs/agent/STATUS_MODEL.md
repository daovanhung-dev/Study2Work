# Status Model

Tài liệu này là nguồn chuẩn cho trạng thái trong DD, checklist, worklog và retrospective. Không tự thêm trạng thái mới nếu chưa cập nhật tài liệu này.

## DD Status

| Status | Meaning |
|---|---|
| `NOT_STARTED` | Chưa tạo DD hoặc chưa bắt đầu phân tích. |
| `DRAFT` | Đang viết, chưa đủ điều kiện coding chính thức. |
| `IN_REVIEW` | Đang chờ BA/PO/Tech Lead/QA review. |
| `APPROVED` | Đã được phê duyệt để coding theo phạm vi DD. |
| `BLOCKED` | Không thể hoàn tất do thiếu thông tin/quyết định. |
| `SUPERSEDED` | Đã bị thay thế bởi DD/ADR/tài liệu mới hơn. |

## Coding Status

| Status | Meaning |
|---|---|
| `NOT_STARTED` | Chưa bắt đầu coding. |
| `IN_PROGRESS` | Đang triển khai. |
| `READY_FOR_TEST` | Code đã sẵn sàng kiểm thử, nhưng chưa có kết quả đạt. |
| `TEST_FAILED` | Test/check thất bại hoặc có lỗi cần fix. |
| `VERIFIED` | Đã có bằng chứng kiểm tra rõ ràng cho phạm vi cần verify. |
| `DONE` | Hoàn tất coding, test, docs/worklog/checklist cho phạm vi task. |
| `BLOCKED` | Không thể tiếp tục do thiếu quyết định, dependency hoặc môi trường. |

## Bug Status

| Status | Meaning |
|---|---|
| `NONE` | Chưa ghi nhận bug cho hạng mục. |
| `OPEN` | Bug đã phát hiện, chưa điều tra đầy đủ. |
| `INVESTIGATING` | Đang phân tích nguyên nhân. |
| `FIXED` | Đã sửa, chưa verify đầy đủ. |
| `VERIFIED` | Đã có evidence xác nhận bug không còn tái hiện. |
| `WONT_FIX` | Không sửa theo quyết định có trace. |

## Test Status For Checklists

Checklist dùng cùng tập trạng thái với coding khi tracking test:

| Status | Rule |
|---|---|
| `NOT_STARTED` | Chưa chạy test/check. |
| `IN_PROGRESS` | Đang kiểm tra. |
| `READY_FOR_TEST` | Đã sẵn sàng kiểm tra nhưng chưa chạy. |
| `TEST_FAILED` | Có test/check fail hoặc chưa đạt acceptance. |
| `VERIFIED` | Chỉ dùng khi có command/output, screenshot, review evidence hoặc link test report. |
| `BLOCKED` | Không chạy được do thiếu môi trường/dependency/quyết định. |

Không dùng `VERIFIED` hoặc `DONE` nếu không có evidence cụ thể trong checklist/worklog.
