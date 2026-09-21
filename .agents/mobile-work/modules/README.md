# Mobile module context

Một project có hai flavor Student/Business; role-specific source/helper vẫn
được tách dưới feature boundary:

Detailed file/module maps:

- [`flutter-student.md`](../flutter-student.md)
- [`flutter-business.md`](../flutter-business.md)
- [`data-flow.md`](../data-flow.md)
- [`file-inventory.md`](../file-inventory.md)

- Authentication/session: `views/dang_nhap/`, `controllers/dang_nhap/`, SQLite
  account helper và direct Neon login.
- Student workflows: home/job search, CV, applications, top CV, notifications,
  support/courses/news/interview/settings.
- Business workflows: home, job posting/management, candidate/CV review,
  reports/statistics, interview/university/settings.
- Chat: `controllers/chat/` và `views/tro_chuyen/`, direct `Chat`/`DoanChat`
  SQL với polling.
- AI: `controllers/AI/`, direct Gemini HTTP call.
- Presentation: shared `lib/app/theme/` contains the Cobalt tokens,
  Material 3 `ThemeData` and primitives for surfaces, section headings,
  status pills, primary buttons and empty states. `views/dang_nhap/menu.dart`
  owns the existing animated navigation destinations and now exposes semantic
  labels without changing page indexes or route flow.

Khi sửa feature, ghi rõ flavor, entrypoint view/controller, helper/model được
gọi, DB/external side effect và test liên quan; chỉ dùng shared implementation
khi contract tương thích.

Các utility/view có code nhưng không có caller hiện tại phải giữ trạng thái
`UNWIRED` hoặc `LEGACY`; không tự xoá hoặc tự nối route trong task context-only.
