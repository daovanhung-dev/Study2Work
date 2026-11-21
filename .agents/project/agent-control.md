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

- Mỗi hàng là một task độc lập, có tên tiếng Việt rõ nghĩa và STT liên tục từ 1.
- Target mới bắt đầu ở `0%`. Tiến độ là số nguyên từ 0 đến 99 khi target còn mở;
  cập nhật khi bằng chứng xác minh làm tiến độ thay đổi, không ước lượng theo
  thời gian hoặc số thao tác.
- Nếu bị chặn, giữ tiến độ đã xác minh. Nếu phạm vi task thay đổi đáng kể, tạo
  target phù hợp và không chuyển tiến độ cũ sang mục tiêu mới.
- Khi hoàn thành, ghi bằng chứng cùng kết quả xác minh vào worklog, sau đó xóa
  hàng target khỏi `target.md`. Không giữ hàng 100% hoặc lịch sử trong file này.
- Không có target đang hoạt động thì giữ header và dòng phân cách, không thêm
  phần giải thích.

## 2. Giao tiếp

Không tự gửi cập nhật tiến độ, Event receipt, milestone, tóm tắt đọc/thao tác,
hoặc báo cáo hoàn tất vào chat. Chỉ phản hồi khi người dùng hỏi, cần làm rõ
blocker để tiếp tục, hoặc quy tắc cấp cao hơn bắt buộc. Khi phản hồi về danh
sách target, dùng đúng nội dung bảng hiện tại. Quy tắc này không hạn chế thông
báo bắt buộc do nền tảng hoặc công cụ yêu cầu.

## 3. Thực hiện và bảo vệ source

- Phân loại task, scope và dependency theo `AGENTS.md`; ghi chúng vào worklog,
  không công bố kế hoạch milestone trong chat.
- Trước khi đọc sâu hoặc sửa, chạy `scripts/select-worklogs.mjs` đúng
  `primary_task_type`, đọc mọi worklog được chọn và ghi `PRIOR_WORKLOG_REVIEW`.
- Đọc context scope/skill/workflow/contract đã đăng ký trong
  `.agents/context-manifest.json`; xác minh source hiện tại trước khi sửa.
- Trước khi sửa behavior, trace caller, callee, persistence hoặc side effect,
  response, business code và test liên quan. Tách expected behavior khỏi current
  behavior; ghi `DISCREPANCY` khi bằng chứng không khớp.
- Không tự tạo API, field, table, validation, service, business code hoặc HTTP
  behavior khi chưa có bằng chứng. Chỉ sửa phạm vi tối thiểu; không áp kiến trúc
  của một server lên server khác.
- Giữ nguyên thay đổi chưa commit của người dùng. Không đưa credentials, token,
  dữ liệu cá nhân hoặc bí mật vào chat hay worklog. Không thực hiện thao tác phá
  hủy hoặc vượt phạm vi được ủy quyền.
- Code review chỉ đọc: không sửa code, chạy test, đổi Git state hoặc đăng nhận
  xét lên PR.

## 4. Worklog và xác minh

Mọi task có worklog theo `.agents/worklog/README.md` và `TEMPLATE.md`. Worklog
lưu nguồn, phân tích, thay đổi, lệnh xác minh và lịch sử `TARGET_UPDATES`; không
lưu `MILESTONES` hay một bản sao tiến độ thường trực. Giữ nguyên worklog lịch sử;
chỉ áp dụng định dạng mới cho task mới.

Chỉ chạy kiểm tra phù hợp yêu cầu và convention scope. Không ghi lệnh chưa chạy
là đã xác minh. Nếu thay đổi context hoặc registry, chạy
`node scripts/validate-agent-context.mjs`, so sánh với baseline trước chỉnh sửa,
và ghi rõ lỗi baseline còn tồn tại thay vì nhận là pass. Cập nhật target khi có
thay đổi tiến độ đã xác minh; khi đạt hoàn tất, lưu bằng chứng trong worklog rồi
xóa hàng target.
