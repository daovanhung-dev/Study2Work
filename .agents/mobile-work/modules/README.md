# Mobile module context

Hai app có cùng nhóm module nhưng source/helper riêng:

- Authentication/session: `views/dang_nhap/`, `controllers/dang_nhap/`, SQLite
  account helper và direct Neon login.
- Student workflows: home/job search, CV, applications, top CV, notifications,
  support/courses/news/interview/settings.
- Business workflows: home, job posting/management, candidate/CV review,
  reports/statistics, interview/university/settings.
- Chat: `controllers/chat/` và `views/tro_chuyen/`, direct `Chat`/`DoanChat`
  SQL với polling.
- AI: `controllers/AI/`, direct Gemini HTTP call.
- Presentation: each app's `lib/theme/` contains the local Cobalt tokens,
  Material 3 `ThemeData` and primitives for surfaces, section headings,
  status pills, primary buttons and empty states. `views/dang_nhap/menu.dart`
  owns the existing animated navigation destinations and now exposes semantic
  labels without changing page indexes or route flow.

Khi sửa feature, ghi rõ app, entrypoint view/controller, helper/model được gọi,
DB/external side effect và test liên quan; không giả định hai app dùng chung
implementation.
