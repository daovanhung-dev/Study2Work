# Agent Control và theo dõi target

Áp dụng cho mọi task và mọi scope trong Study2Work. File này bổ sung quy tắc
repo; không thể ghi đè system/developer, bảo mật, quyền hạn hoặc giới hạn công
cụ cấp cao hơn.

## 1. Nguồn tiến độ duy nhất

`.agents/target.md` là nguồn duy nhất cho target đang hoạt động và chỉ chứa một
bảng Markdown với đúng ba cột theo thứ tự:

```markdown
| STT | Tên target | Tiến độ hoàn thiện |
|---:|---|---:|
```

- Mỗi hàng là một mục tiêu lá ở tầng thao tác: một hành động nhỏ nhất có thể
  hoàn tất và xác minh độc lập, có kết quả quan sát được và tiêu chí nghiệm thu
  riêng. Dùng tên tiếng Việt dạng hành động + kết quả. Tách thao tác độc lập;
  không tạo hàng bao trùm như “hoàn thiện feature/screen/module”. Không chia
  một thao tác không thể nghiệm thu thành các bước hình thức.
- Trước khi thực thi, lập `LEAF_TARGET_PLAN` trong worklog; mỗi hàng ghi một
  target, một thao tác và evidence nghiệm thu. `.agents/target.md` chỉ hiển thị
  target lá đang mở, không có parent/epic. Task đơn giản có thể có một hàng.
- Target mới bắt đầu ở `0%`. Tiến độ là số nguyên từ 0 đến 99 khi target còn mở;
  cập nhật khi bằng chứng xác minh làm tiến độ thay đổi, không ước lượng theo
  thời gian hoặc số thao tác.
- Nếu bị chặn, giữ tiến độ đã xác minh. Nếu phạm vi task thay đổi đáng kể, tạo
  target phù hợp và không chuyển tiến độ cũ sang mục tiêu mới.
- Khi hoàn thành, ghi bằng chứng cùng kết quả xác minh vào worklog, sau đó xóa
  hàng target khỏi `target.md`. Không giữ hàng 100% hoặc lịch sử trong file này.
- Không có target đang hoạt động thì giữ header và dòng phân cách, không thêm
  phần giải thích.

## 2. Giao tiếp im lặng

Sau khi nhận task, không gửi nội dung assistant-authored vào chat: không
commentary, tiến độ, receipt, milestone, kế hoạch, tóm tắt file đã đọc, thao
tác, lỗi, kết quả hoặc báo cáo hoàn tất. Dùng target/worklog làm nơi lưu tiến
độ và evidence. Chỉ phản hồi nếu người dùng yêu cầu câu trả lời cụ thể, cần một
câu hỏi tối thiểu để gỡ blocker không thể tự suy ra, hoặc system/developer/tool
cấp cao hơn bắt buộc. Không dùng quy tắc này để che giấu blocker ảnh hưởng an
toàn hoặc thay đổi phạm vi.

## 3. Thực hiện và bảo vệ source

- Phân loại task, scope và dependency theo `AGENTS.md`; ghi chúng vào worklog,
  không công bố kế hoạch milestone trong chat.
- Khai báo mọi path, phần cần đọc và lý do trong `READ_PLAN` trước khi mở nội
  dung. Search chỉ chạy trên path đã khai báo. Nếu phát hiện dependency mới, thêm
  path trước khi đọc; dùng đoạn dòng hẹp, dừng khi đủ evidence, tránh đọc lặp.
- Chạy `scripts/select-worklogs.mjs` đúng `primary_task_type`; ghi các path được
  chọn vào `READ_PLAN` trước khi đọc nội dung, rồi ghi carry-forward vào
  `PRIOR_WORKLOG_REVIEW`.
- Đọc context scope/skill/workflow/contract đã đăng ký trong
  `.agents/context-manifest.json`; xác minh source hiện tại trước khi sửa.
- Trước khi sửa behavior, trace caller, callee, persistence hoặc side effect,
  response, business code và test liên quan. Tách expected behavior khỏi current
  behavior; ghi `DISCREPANCY` khi bằng chứng không khớp.
- Không tự tạo API, field, table, validation, service, business code hoặc HTTP
  behavior khi chưa có bằng chứng. Chỉ sửa file tối thiểu; không refactor ngoài
  phạm vi và không áp kiến trúc của một server lên server khác.
- Giữ nguyên thay đổi chưa commit của người dùng. Không đưa credentials, token,
  dữ liệu cá nhân hoặc bí mật vào chat hay worklog. Không thực hiện thao tác phá
  hủy hoặc vượt phạm vi được ủy quyền.
- Code review chỉ đọc: không sửa code, chạy test, đổi Git state hoặc đăng nhận
  xét lên PR.

## 4. Worklog và xác minh

Mọi task có worklog theo `.agents/worklog/README.md` và `TEMPLATE.md`. Worklog
lưu `READ_PLAN`, `LEAF_TARGET_PLAN`, nguồn, phân tích, thay đổi, lệnh xác minh
và lịch sử `TARGET_UPDATES`; không lưu `MILESTONES` hay bản sao tiến độ thường
trực. Giữ nguyên worklog lịch sử; chỉ áp dụng định dạng mới cho task mới.

Chỉ chạy kiểm tra phù hợp yêu cầu và convention scope. Không ghi lệnh chưa chạy
là đã xác minh. Nếu thay đổi context hoặc registry, chạy
`node scripts/validate-agent-context.mjs`, so sánh với baseline trước chỉnh sửa,
và ghi rõ lỗi baseline còn tồn tại thay vì nhận là pass. Cập nhật target khi có
thay đổi tiến độ đã xác minh; khi đạt hoàn tất, lưu bằng chứng trong worklog rồi
xóa hàng target.
