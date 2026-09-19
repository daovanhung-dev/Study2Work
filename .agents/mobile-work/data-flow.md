# Mobile data-flow and boundary context

`CONTEXT_STATUS: SOURCE_BACKED`

## Global runtime shape

The two apps are direct-data Flutter clients. They do not call
`apps/work-server` HTTP routes and do not share a Dart package, even though both
packages are named `work_server`.

```text
Flutter View
  -> controller or compatibility helper
      -> NeonDatabase.query/execute -> Neon PostgreSQL
      -> SQLite helper -> local account/major cache
      -> AIService -> Gemini HTTP API
```

Remote access is direct, parameterized PostgreSQL SQL through
`lib/helper_db/neon_db.dart` in each app. The helper validates SSL mode,
removes `channel_binding` for the Dart driver, supplies pool/timeout defaults,
normalizes `BIGINT` values and owns pool shutdown.

## Local SQLite schemas

| App | Database | Tables | Lifecycle |
|---|---|---|---|
| Student | `sinhvien.db` | `sinhvien(id, hoten, email, matkhau, chuyennganh, avt)`; `bannganh(id, nganh)` | Login deletes/replaces cached student, writes majors; logout deletes student rows. |
| Business | `doanhnghiep.db` | `doanhnghiep(id, hoten, email, matkhau, diachi, sodienthoai)`; `bannganh(id, nganh)` | Login saves company and majors; logout clears company rows. |

SQLite is a local session/cache mechanism, not a JWT store. Cached credentials
are re-used by the student `autoLogin` function; the business app has no
equivalent startup auto-login flow in current source.

## Neon tables and consumers

| Table | Student consumers | Business consumers | Main operations |
|---|---|---|---|
| `SinhVien` | Login/profile, participant name, profile helper | Chat partner/name lookup | Login, profile read/write/delete, name lookup. |
| `DoanhNghiep` | Login-independent company lookup, chat partner/name, JD company resolution | Login/profile, student chat partner/name | Credential check, profile read, name/avatar lookup. |
| `JD` | Top jobs, search, detail, application company resolution | Job list, posting, detail/update compatibility paths | Select, insert, update/delete in legacy controller. |
| `Cv` | Student CV management, TopCV and candidate projections | TopCV, candidate list/detail, CV helper | CRUD/search/select with JSONB `social` and dates. |
| `UngVien` | Duplicate check and application insert | Candidate list, status update/delete/status list | Student applies; business changes/removes application. |
| `DoanChat` | Partner list and conversation model/helper | Partner list and conversation creation | Relation between one student and one business. |
| `Chat` | History and send in student chat | History and send in business chat | Message rows ordered by timestamp/id. |
| `TopCV` | Dedicated helper query exists; no active caller found | Home TopCV query | Select ids, then project `Cv` rows. |
| `TopJD` | Home top-JD query | Not used by current business controller | Join to `JD` ordered by `created_at`. |
| `bannganh` | Major lookup/cache path | Major lookup/cache path | Ordered major lookup; local helper also stores copies. |

The exact case-sensitive table and column names above come from current SQL in
the mobile helpers. Do not replace them with inferred REST fields or
Supabase-generated names.

## Feature flows

### Student login

```text
DangNhap
  -> dangNhapDN(email, matKhau)
  -> SinhVienSupabaseHelper.login
  -> Neon SELECT SinhVien
  -> getByEmail -> SinhVien.fromMap
  -> SinhVienSQLiteHelper.insertSinhVien
  -> getNganh -> saveNganh
  -> Menu
```

Errors are caught in the login controller and represented as `false`. Debug
logging currently exists in source; context must not reproduce credentials or
row payloads.

### Business login

```text
DangNhap
  -> dangNhapDN(gmail, matKhau)
  -> DNSupabase.ktDangNhap
  -> DNSupabase.getDN -> DoanhNghiep.fromMap
  -> HelperDB.saveDoanhNghiep
  -> DNSupabase.getNganh -> HelperDB.saveNganh
  -> Menu
```

### Job and application

```text
Student: search/home/detail
  -> JD model
  -> resolve doanhnghiep_id
  -> UngTuyenCtrl
  -> duplicate check UngVien
  -> INSERT UngVien

Business: post/manage/detail
  -> form Map
  -> DNSupabase.insertJD
  -> INSERT JD
  -> getJob scoped by cached doanhnghiep id
```

### CV and candidate actions

Student CV editing uses the cached student id and updates `Cv`. Business
candidate management joins `UngVien` to `Cv`, maps candidate rows, updates or
deletes application status, creates a `DoanChat` relation and inserts a
notification message into `Chat`.

### Chat polling

Both apps use the same polling algorithm but separate helper instances:

1. Start a `Timer.periodic` with a default three-second interval.
2. Run one immediate fetch.
3. Seed existing integer message ids without emitting them.
4. On later polls, emit only ids newly added to `seenIds`.
5. Skip overlapping fetches while one poll is running.
6. Cancel the timer from each `ChatView.dispose()`.

No realtime channel, WebSocket or `LISTEN/NOTIFY` contract is wired.

### Gemini AI

Each app has a duplicated `AIService` that posts prompt text directly to
`generativelanguage.googleapis.com` using the `GEMINI_API_KEY` symbol from
`constants.dart`. `timkiemctrl.dart` constructs a fixed major-list prompt but
currently discards the returned text. This integration is independent of
`apps/ai-server` and `apps/work-server`.

## Naming and wiring discrepancies

| Item | Evidence | Current status |
|---|---|---|
| Supabase names | `helper_supabase.dart`, `DNSupabase`, `SinhVienSupabaseHelper` import `postgres`/`NeonDatabase`, not `supabase_flutter`. | Compatibility naming; do not document as a Supabase runtime. |
| Direct secrets | Both `constants.dart` files contain Neon/Gemini constants. | Prototype-only security boundary; context redacts values. |
| Duplicate helper/model trees | Student has `sinh_vien/` and `out_meta/`; business has root helpers/models. | Parallel compatibility shapes; do not merge without contract evidence. |
| Static/legacy screens | Several files exist beside active page variants. | Marked `UNWIRED`, `LEGACY` or `PLACEHOLDER` in app pages/inventory. |
| HTTP API boundary | No mobile import targets Work server routes. | Direct Neon/Gemini current behavior; backend boundary is future architecture, not current wiring. |
| README platform claims | READMEs mention `web/`, but current tracked source inventory has no tracked web source. | Documentation discrepancy; source wins. |

## Security boundary

The current APK/client can expose compiled database and AI credentials and the
Neon role is broader than a least-privilege mobile credential should be. This
context records the risk and the exact current direct-data flow, but does not
copy secret literals. Production work must move database/AI access behind a
backend boundary, rotate exposed credentials and remove direct client access.

