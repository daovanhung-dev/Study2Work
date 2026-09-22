# Study2Work

Study2Work là monorepo polyglot cho hai miền sản phẩm:

- **Study**: nền tảng học tập, tài khoản người học, khóa học, bài học, đánh giá và tiến độ.
- **Work**: nền tảng việc làm gồm hồ sơ sinh viên, CV, tin tuyển dụng, ứng tuyển và quy trình dành cho doanh nghiệp.

Repository hiện có tám deployable độc lập: Study Web/API, Work Web/API/Mobile,
AI API và DB Admin Web/API. Các trạng thái trong README này phản ánh source
hiện tại; file tồn tại nhưng chưa được import hoặc đăng ký runtime không được
coi là chức năng đã chạy.

## Lưu ý về working tree hiện tại

Tại thời điểm cập nhật, một số file orchestration/config ở root đang ở trạng
thái bị xóa nhưng chưa commit: `package.json`, `pnpm-workspace.yaml`,
`docker-compose.yml`, `.env.example`, `pyproject.toml`, các lockfile và config
liên quan. Vì vậy các lệnh root và Docker Compose dưới đây mô tả workflow của
repository nhưng chỉ chạy được sau khi các file đó được khôi phục.

Ngoài ra, Study Web hiện có source blocker trong
[`vite.config.ts`](apps/study-client/vite.config.ts) ở token đầu file. README
không tuyên bố build/runtime đã pass khi toolchain hoặc source hiện tại chưa
cho phép xác minh.

## Kiến trúc tổng thể

```text
Study Web (Vue) ── configured API boundary ──> Study API (FastAPI) ──> PostgreSQL/Neon

Work Web (React) ── relative /api/v1 ──> Work API (Express) ──> Prisma ──> PostgreSQL/Neon

Work Mobile (Flutter student/business) ── direct PostgreSQL/Neon + SQLite cache
                                      └─ direct Gemini HTTP API

AI API (FastAPI) ──> Ollama HTTP API

DB Admin Web (Angular) ── same-origin /api/v1/admin ──> DB Admin API (FastAPI)
                                                               └─> named Neon targets
```

Boundary quan trọng:

- Work Web là browser client của Work API, dùng JWT Bearer trong `access_token` và không kết nối Neon trực tiếp.
- Work Mobile hiện là direct-data client, không gọi HTTP route của Work API; direct Neon/Gemini là boundary prototype cần harden trước production.
- DB Admin là control plane local độc lập, không import business module/schema của Study, Work hoặc AI.
- AI API dùng Ollama; nó độc lập với Gemini client trong Work Mobile.
- Study Web hiện là static home shell; Study OpenAPI vẫn là placeholder nên không suy diễn request/response từ Work.

## Mini projects

| Mini project | Đường dẫn | Công nghệ và kiến trúc | Trạng thái runtime hiện tại |
|---|---|---|---|
| Study Web | [`apps/study-client`](apps/study-client) | Vue 3, TypeScript, Vite, Vue Router, Pinia, Vue Query, Zod | Static home shell; chưa có live API request; Study OpenAPI chưa có contract đầy đủ |
| Study API | [`apps/study-server`](apps/study-server) | FastAPI, Python 3.12+, SQLAlchemy sync core, PostgreSQL/Neon, JWT/refresh token, Ollama adapter | Health, register, login và refresh được compose; các module khác chỉ là DD/design hoặc chưa wired |
| Work Web | [`apps/work-client/web`](apps/work-client/web) | React, TypeScript, Vite, React Query, Zustand, Zod | Dùng relative `/api/v1`; Vite proxy `/api`, `/uploads`, `/img` tới Work API |
| Work API | [`apps/work-server`](apps/work-server) | Express 4, TypeScript, Prisma, PostgreSQL/Neon, JWT Bearer, Multer | JSON API; student/business auth, jobs, CV và applications hiện có route; nhiều target domain routes chưa wired |
| Work Mobile | [`apps/work-client/mobile`](apps/work-client/mobile) | Flutter/Dart, Riverpod, go_router, `postgres`, SQLite, Gemini HTTP; Android flavors `student` và `business` | Một Flutter package với hai app ID; direct Neon/SQLite/Gemini; chat polling 3 giây |
| AI API | [`apps/ai-server`](apps/ai-server) | FastAPI, Python, httpx, Ollama | `POST /api/v1/chat_log_ai` gọi Ollama `/api/generate`; không có DB runtime và chưa có test suite tracked |
| DB Admin Web | [`apps/db-admin-web`](apps/db-admin-web) | Angular standalone, Angular Material, CodeMirror | Local admin UI; launcher tự khởi động DB Admin API và proxy same-origin `/api` |
| DB Admin API | [`apps/db-admin-server`](apps/db-admin-server) | FastAPI, SQLAlchemy, psycopg3, Argon2id/JWT/JWKS | Local-only database control plane; catalog, SQL, access và audit được bảo vệ ở backend |

### Shared contracts và local infrastructure

- [`contracts/api-guidelines`](contracts/api-guidelines/README.md): envelope, trace ID và quy ước API chung.
- [`contracts/openapi/work`](contracts/openapi/work/README.md): system/health contract đã xác minh; target domain OpenAPI và Express route hiện còn discrepancy.
- [`contracts/openapi/study`](contracts/openapi/study/README.md): placeholder, chưa phải Study API contract đầy đủ.
- [`contracts/events/study-work`](contracts/events/study-work/README.md): event schemas có nhưng consumer Work chưa wired.
- [`infra/README.md`](infra/README.md): local PostgreSQL, Redis, MinIO, Mailhog và Study/Work Compose stack.

## Chuẩn bị môi trường

Toolchain đề nghị:

- Node.js và Corepack/pnpm cho các app TypeScript/JavaScript.
- Python 3.12+ và `uv` cho các app FastAPI.
- Flutter/Dart SDK cho Work Mobile.
- Docker Compose cho local infrastructure stack.
- Ollama nếu chạy AI API; mặc định adapter dùng `http://127.0.0.1:11434`.

Khi root manifests còn đầy đủ, cài dependency JavaScript từ root:

```bash
corepack pnpm install
```

Không đưa credential thật vào README, source, log hoặc file tracked. Study,
Work và DB Admin hiện đọc phần lớn cấu hình runtime từ constants/config của
từng app; kiểm tra README của app trước khi chạy local.

## Lệnh tổng hợp

Chạy từ root sau khi khôi phục root `package.json` và workspace files:

```bash
corepack pnpm build
corepack pnpm lint
corepack pnpm typecheck
corepack pnpm test
```

Các lệnh trên áp dụng cho JavaScript workspace packages và contract validation
được khai báo ở root. `corepack pnpm docs:validate` hiện không thể xác minh vì
`docs/BD` không tồn tại trong working tree.

Local Study/Work infrastructure stack theo Compose:

```bash
docker compose up --build
```

Dừng stack:

```bash
docker compose down
```

Compose chỉ bao phủ local infrastructure cùng Study API, Work API và Work Web
theo file hiện có; không tự khởi động AI API, DB Admin hoặc Flutter Mobile.
Không có một lệnh duy nhất chạy toàn bộ tám deployable. AI, DB Admin và Mobile
cần khởi động bằng các lệnh riêng bên dưới.

## Lệnh chạy từng mini project

### 1. Study Web

Package: [`apps/study-client/package.json`](apps/study-client/package.json).

```bash
corepack pnpm --filter study-web dev
corepack pnpm --filter study-web typecheck
corepack pnpm --filter study-web test
corepack pnpm --filter study-web build
corepack pnpm --filter study-web exec vite preview --host 127.0.0.2 --port 3002
```

Build output là `apps/study-client/dist/`; Vite dev/preview bind tại
`http://127.0.0.2:3002`. Build hiện bị chặn bởi malformed token trong
`vite.config.ts` cho tới khi source được sửa.

### 2. Study API

Đọc thêm [`apps/study-server/README.md`](apps/study-server/README.md).

```bash
cd apps/study-server
uv sync
uv run ruff check .
uv run ruff format --check .
uv run mypy app
uv run pytest
uv run uvicorn app.main:app --reload --host 127.0.0.1 --port 3003
```

Study API chạy tại `http://127.0.0.1:3003`.

Health endpoints:

- `GET /health/live`
- `GET /health/ready`

### 3. Work Web

Package: [`apps/work-client/web/package.json`](apps/work-client/web/package.json).

```bash
corepack pnpm --filter work-web dev
corepack pnpm --filter work-web typecheck
corepack pnpm --filter work-web test
corepack pnpm --filter work-web build
corepack pnpm --filter work-web preview
```

Vite tạo `apps/work-client/web/dist/` và phục vụ dev/preview tại
`http://127.0.0.2:3001`. Khi dev, `/api`, `/uploads` và `/img` được proxy tới
`http://127.0.0.1:3002`.

### 4. Work API

Đọc thêm [`apps/work-server/README.md`](apps/work-server/README.md).

```bash
corepack pnpm --filter work_server prisma:validate
corepack pnpm --filter work_server prisma:generate
corepack pnpm --filter work_server typecheck
corepack pnpm --filter work_server test
corepack pnpm --filter work_server s2w
```

Work API chạy tại `http://127.0.0.1:3002`. Package hiện không có script
`build`; runtime TypeScript được khởi động qua `ts-node/esm`, vì vậy không ghi
nhận một thư mục build riêng cho Work API.

API hiện dùng JWT Bearer, không dùng cookie/session. Contract browser hiện tại
là [`legacy-web.openapi.json`](contracts/openapi/work/legacy-web.openapi.json);
`openapi.json` là target/health baseline chưa đại diện toàn bộ route runtime.

### 5. Work Mobile

Đọc thêm [`apps/work-client/mobile/README.md`](apps/work-client/mobile/README.md).

```bash
cd apps/work-client/mobile
flutter pub get
flutter analyze
flutter test

flutter run --flavor student
flutter run --flavor business

flutter build apk --flavor student
flutter build apk --flavor business
flutter build appbundle --flavor student
flutter build appbundle --flavor business
```

Flavor và application ID:

| Flavor | Application ID | APK mặc định | AAB mặc định |
|---|---|---|---|
| `student` | `com.s2w.work.students` | `build/app/outputs/flutter-apk/app-student-release.apk` | `build/app/outputs/bundle/studentRelease/app-student-release.aab` |
| `business` | `com.s2w.work.business` | `build/app/outputs/flutter-apk/app-business-release.apk` | `build/app/outputs/bundle/businessRelease/app-business-release.aab` |

Mobile không có HTTP address sau build; kết quả là APK/AAB cài trên Android.
Neon network smoke test là opt-in:

```bash
flutter test --dart-define=RUN_NEON_SMOKE=true
```

### 6. AI API

Đọc thêm [`apps/ai-server/README.md`](apps/ai-server/README.md).

```bash
cd apps/ai-server
uv sync
uv run uvicorn app.main:app --host 127.0.0.1 --port 3000
```

AI API chạy tại `http://127.0.0.1:3000`; endpoint chat hiện tại là
`POST /api/v1/chat_log_ai` với body `{"prompt":"..."}`. Ollama phải chạy
riêng, mặc định tại `http://127.0.0.1:11434`. AI server chưa có test suite
tracked và copied core chưa được `app.main` đăng ký.

### 7. DB Admin Web và DB Admin API

DB Admin Web launcher khởi động cả FastAPI backend và Angular dev server.
Trước lần chạy đầu tiên, tạo file constants local:

```bash
cp apps/db-admin-server/app/core/constants.example.py \\
   apps/db-admin-server/app/core/constants.py
```

Chạy toàn bộ local flow từ root:

```bash
corepack pnpm --filter db-admin-web dev
```

Hoặc chạy backend trực tiếp:

```bash
cd apps/db-admin-server
uv sync
uv run ruff check app tests
uv run mypy app
PYTHONPATH=. uv run pytest -q
uv run --no-env-file --no-dev uvicorn app.main:app --reload \\
  --host 127.0.0.1 --port 3001
```

Build và test Angular:

```bash
corepack pnpm --filter db-admin-web build
corepack pnpm --filter db-admin-web test
```

DB Admin Web chạy tại `http://127.0.0.2:3000`, build output mặc định dưới
`apps/db-admin-web/dist/`. DB Admin API nội bộ chạy tại
`http://127.0.0.1:3001`; browser chỉ gọi API qua same-origin proxy và không
nhận Neon credential.

## Địa chỉ local sau khi chạy/build

| Thành phần | Địa chỉ hoặc artifact |
|---|---|
| Study Web dev/preview | `http://127.0.0.2:3002` |
| Study API | `http://127.0.0.1:3003` |
| Work Web dev/preview | `http://127.0.0.2:3001` |
| Work API | `http://127.0.0.1:3002` |
| AI API | `http://127.0.0.1:3000` |
| DB Admin Web dev | `http://127.0.0.2:3000` |
| DB Admin API nội bộ | `http://127.0.0.1:3001` |
| Work Mobile student | APK/AAB và ID `com.s2w.work.students` |
| Work Mobile business | APK/AAB và ID `com.s2w.work.business` |

Các loopback address dùng `127.0.0.1` và `127.0.0.2` có chủ đích để tránh
đụng port giữa API và frontend.

### Local infrastructure ports

Khi `docker-compose.yml` được khôi phục và Compose stack chạy:

| Dependency | Address |
|---|---|
| Study PostgreSQL | `127.0.0.1:5433` |
| Study Redis | `127.0.0.1:6380` |
| Work PostgreSQL | `127.0.0.1:5434` |
| Work Redis | `127.0.0.1:6381` |
| MinIO API/console | `127.0.0.1:9000` / `127.0.0.1:9001` |
| Mailhog SMTP/UI | `127.0.0.1:1025` / `http://127.0.0.1:8025` |

## Tài liệu và trạng thái contract

- [Agent context map](.agents/context-map.md): ownership, page graph và boundary đã được registry hóa.
- [Project architecture](.agents/project/architecture.md): deployable map và local address map.
- [Work API guidelines](contracts/api-guidelines/README.md): envelope và trace convention.
- [Work OpenAPI status](contracts/openapi/work/README.md): phân biệt contract legacy đang dùng với target surface chưa wired.
- [Study OpenAPI status](contracts/openapi/study/README.md): placeholder, chưa có public contract đầy đủ.
- [Mobile module documentation](apps/work-client/mobile/docs/mobile_business/README.md) và [Student mobile documentation](apps/work-client/mobile/docs/mobile_student/README.md).

Không có thư mục `docs/BD` trong source hiện tại, vì vậy các tài liệu DD/design
không được dùng để khẳng định runtime behavior khi mâu thuẫn với source.
