# Hoàn tất implementation các Study screens

> Ngày lập: 2026-11-17 · Repo: `/home/daovh/develop/Study2Work`
> Worklog gốc: [T038](../../../../.agents/worklog/2026-11-17/implement-remaining-study-screens-T038.md) · Ma trận 83 screen: [T038-screen-gap-matrix.md](../../../../.agents/worklog/2026-11-17/T038-screen-gap-matrix.md)

Bạn đang tiếp quản task implementation đang dở trong repo Study2Work. Hãy
đọc toàn bộ tài liệu này trước khi sửa code, sau đó tiếp tục task T038 theo
trạng thái source thật hiện tại. User yêu cầu hoàn thiện các màn hình Study còn
thiếu theo DD, gán và gọi API Study Server có source phù hợp, giữ đúng logic và
UI/UX; dùng `apps/study-client/docs/screen_stitch/` làm visual reference khi
cần.

Đừng dựng lại những phần đã có. Đối chiếu từng screen/API với source mới nhất,
hoàn thiện phần còn dở, giữ an toàn các action bị contract/security/schema
block, đồng bộ tài liệu/worklog và kết thúc bằng verification phù hợp. Không
chỉnh Study Server, DB schema hay tạo API mới để ép UI chạy; nếu một behavior
cần contract mới, giữ gate và ghi rõ blocker.

## Mục tiêu và phạm vi

- Web chính: `apps/study-client/` — Angular 22 standalone app.
- Backend đối chiếu: `apps/study-server/` — FastAPI; source endpoint hiện tại
  là bằng chứng cho behavior, không phải bằng chứng deploy/live DB.
- Danh mục: 83 ID screen trong `apps/study-client/docs/list_screen.md` và
  `docs/dd_screens/screen-index.md`: Shared, Guest, Student, Mentor, Admin;
  Page/Tab/Dialog/Panel/Transition không đồng nghĩa 83 URL.
- Yêu cầu đầu ra: từng ID có page/component/route phù hợp; behavior được nối
  với caller API thật khi source hỗ trợ, nếu không thì UI phải thể hiện gate
  rõ ràng. Route metadata/API ID trong danh sách không tự chứng minh có caller.
- Ưu tiên bằng chứng: yêu cầu mới nhất → current source và executable config
  → runnable tests đã thực sự chạy → DD/API contract. Expected và current
  behavior khác nhau phải được ghi `DISCREPANCY`, không tự sửa contract.

## Tiến độ tại thời điểm bàn giao

| Cách tính                                                     |                 Trạng thái | Cách hiểu                                                                                                                                                                                                                                                                                                                                                                    |
| --------------------------------------------------------------- | ---------------------------: | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Tiến độ chính thức trong T038 ở lần ghi gần nhất       |                **25%** | Mốc 10% preflight và 15% hoàn tất slice T037/AD-12 đã được ghi DONE; milestone implementation 60% còn `IN_PROGRESS`, milestone final 15% là `PENDING`. Con số trong worklog chưa được cập nhật sau các đợt coding tiếp theo.                                                                                                                         |
| Ước lượng phần implementation T038 đã có trong worktree |    **khoảng 80–85%** | Ước lượng bàn giao, chưa được kiểm kê lại toàn bộ bởi máy tiếp theo. Dựa trên ma trận 83 ID, route/page coverage, Student ST01/ST08/ST09/ST10 mới được nối API và các wave Student ST11–tạiST25/Mentor ME01–ME18 đã được thực hiện. Nhiều màn hình vẫn partial/gated; không đồng nghĩa 80–85% màn hình đã đạt nghiệm thu. |
| Phần còn lại ước tính                                     |    **khoảng 15–20%** | Rà source/diff và gap còn sót, xử lý status auth/profile không còn đúng, kiểm tra UI/DD, hoàn thiện current-source docs/worklog, chạy build/diff/context validation và ghi giới hạn runtime. Nếu audit phát hiện thêm gap, hãy cập nhật phần trăm và milestone, không giữ cứng 85%.                                                              |
| Tiến độ dự án rộng hơn                                   | **khoảng 20% ACTIVE** | Đây là estimate coarse trong tracker/worklog; khác hoàn toàn tiến độ task T038 và không phải tỷ lệ screen hoàn tất.                                                                                                                                                                                                                                            |

**Lưu ý snapshot:** các số T038=25% và estimate 80–85% trong bảng trên là dữ liệu lịch sử tại thời điểm bàn giao; checkpoint T040 dưới đây là tiến độ phiên hiện tại và không phải tỷ lệ hoàn thành 83 screen.

## Checkpoint tiếp tục T040 — 2026-11-18

| Trạng thái | Chi tiết |
|---|---|
| Tiến độ phiên T040 | **90%** — hoàn tất audit và sửa các gap code source-backed đã xác định; đây là tiến độ theo milestone phiên, không phải tỷ lệ nghiệm thu 83 screen. Mốc cuối chưa đạt vì nhiều screen vẫn bị gate bởi contract/schema. |
| Đã xác nhận | T039 đã xử lý các gap caller an toàn được tìm thấy ở ST10, ME07, ME08; audit trước đó không tìm thấy gap caller an toàn mới ở Shared/Guest, Student ngoài ST10, Mentor ngoài ME07/ME08, hoặc Admin. |
| Đã sửa | ST06 copy không còn khẳng định giao dịch đã kết thúc và card đúng 512px; ST07 copy trung tính, card 672×390px, icon clipboard-check SVG. Không thêm API hoặc success state. |
| Phạm vi coding | Các gap code source-backed trong audit hiện tại đã sửa. Các screen cần payment/enrollment result, notification data, mentor mutations và admin report vẫn chưa hoàn tất cho tới khi contract/schema/product policy tương ứng được cung cấp. |
| Verification | Theo yêu cầu coding-only của user, không chạy test/build/lint/browser trong phiên này; phiên khác sẽ test. |
| Blocker | ST06 payment cần Order/provider/gateway/Operation contract; ST07 cần trusted paid/order/entitlement, #19 identity/eligibility/idempotency và #20 course-list response. ST26 phụ thuộc notification recipient schema; ME04 upload/create mapping và AD-23/AD-25 report APIs còn thiếu. Các gate khác giữ theo matrix. |

**Worklog phiên:** [T040](../../../../.agents/worklog/2026-11-18/implement-remaining-study-screens-T040.md).

**Điểm cần lưu ý:** không lấy số `0 not started` trong gap matrix làm số screen
đã hoàn tất. Matrix phân loại cấu trúc; route/page có thể chỉ là gate hoặc
partial. Mức 25% trong T038 là snapshot lịch sử của worklog đó; 90% trong T040
là tiến độ các milestone coding đã làm ở phiên này. Cả hai đều không phải tỷ lệ
screen đã nghiệm thu; giữ riêng lịch sử T038 cho tới khi có đợt reconcile đầy đủ.

## Bối cảnh repo và quy tắc phải giữ

1. Đọc root `AGENTS.md`, `.agents/AGENTS.md`, `.agents/context-map.md`,
   `.agents/project/agent-control.md`, manifest và worklog README. Phân loại
   task `coding`, scopes `web-work` + `server-study`, dependency Study Client
   caller ↔ Study Server API source. Chạy
   `node scripts/select-worklogs.mjs --type coding --limit 3`, đọc hết các log
   được chọn và ghi `PRIOR_WORKLOG_REVIEW`.
2. Đọc `.agents/web-work/study/AGENTS.md`, `INDEX.md`, workflow đã đăng ký
   `study-web-screen-coding`, `.agents/web-study/frontend-rules.md` và
   `.agents/web-study/design.md`. Với từng API cần dùng, đọc đúng trang
   `.agents/server-study/` và module/router/query/model/test source tương ứng;
   không load server scope sâu không liên quan.
3. Study Web dùng Angular 22, standalone components, lazy route groups. Screen
   feature dùng đúng bốn direct folders `data-access/`, `models/`, `pages/`,
   `ui/`; service screen gọi `StudentApiService`/`MentorApiService` phù hợp.
   Shared feature/session API không được bypass bằng `StudyApiService` cho
   protected call.
4. Mọi tool action phải có Task/Step/Action/Event receipt theo Agent Control.
   Ghi milestone vào worklog và chỉ tăng progress khi tiêu chí đã xác minh.
5. Worktree vốn rất dirty. T038 ghi nhận 664 entries ở baseline trước các wave;
   hiện có nhiều modified/untracked files trên Study Client/DD/context. Trước
   mọi sửa đổi hãy chạy `git status --short --branch` và xem đúng target diff.
   **Không** reset, clean, checkout file để khôi phục, rebase, hoặc xóa/thay
   đổi file ngoài scope. `task_finish.md` khi lập tài liệu này là file untracked
   0 dòng; tiếp tục cập nhật nội dung hiện có.
6. `screen_stitch` HTML/ảnh là design evidence, không phải Angular runtime.
   Mỗi screen còn cần UI work: đọc đủ 8 DD page, `images/README.md`, clean và
   numbered PNG, Stitch HTML, marker/plan liên quan; mở ảnh để so sánh. Giữ
   nguyên assets. Không đưa dữ liệu mẫu, KPI giả, dữ liệu fixture hoặc endpoint
   mock vào giao diện như dữ liệu thật.
7. Không tự tạo field, validation, business code, API, table, permission,
   authentication behavior hay HTTP behavior. Không thay đổi server/schema để
   né gate; dùng DTO/response hiện tại và bảo toàn discrepancy. Token không vào
   localStorage, URL hay log.
8. Tuân theo test/verification restrictions của runtime đang thực hiện. Lần
   coding trước không chạy test sau các thay đổi cuối; không báo tests pass nếu
   chưa chạy. Không tuyên bố browser/live API/live DB/deployment đã xác minh từ
   build hoặc fake-session tests.

## Trạng thái source đã làm — xác minh lại trước khi sửa

### Inventory và coverage

Ma trận T038 ghi đủ 83 ID với API assignment, cấu trúc frontend, numbered
server route source và FE caller/gate. Snapshot cấu trúc hiện ghi:

- 79 `route+page` (bao gồm partial/gated), 3 parent tabs, 1 page-only,
  0 `not started` về mặt cấu trúc.
- Student route group có ST01–ST26; Mentor group có ME01–ME18. Các route này
  không chứng minh screen acceptance/deployment.
- Dùng [gap matrix](../../../../.agents/worklog/2026-11-17/T038-screen-gap-matrix.md)
  làm chỉ mục ban đầu; kiểm tra code hiện tại trước khi sửa vì matrix cũng là
  snapshot.

### Shared, Guest và Admin đã có trước/cùng các wave

- Shared: SH01 `/`; SH02 presentation-only `/login`; SH03 gọi #01 ở
  `/register`; SH04 static email information, không gọi #02; SH05 có page nhưng
  chưa route; SH06 xử lý not-found; SH07 là operation gate, chưa gọi #18.
- Guest: GS01 #05/#06; GS02 #07; GS03 #08 và lazy curriculum #09/reviews #10;
  GS04–GS06 là tab của GS03; GS07 route resource gate. Category filtering,tại
  resource collection/access, review và một số loaded states còn partial.
  #11 hiện trả singleton/first row dù DD mong collection; #12 hiện chưa có
  entitlement/access policy đủ an toàn.
- Admin: có nhiều API-backed list/detail screens; xem rows AD01–AD25 trong
  ma trận trước khi kết luận. AD01/AD24/AD25 phụ thuộc APIs #99–#103 hoặc
  report/export sources chưa có; các mutation/API còn thiếu contract tiếp tục
  phải disabled/gated. T037 đã xử lý slice AD12/#82 nhưng các filter,
  cardinality, permission và live-schema limits còn mở.

### Student

| Screen     | Caller/source đã ghi nhận trong T038                                                                                              | Còn phải làm/giữ gate                                                                                                                                                                                                                                                                                                                                                   |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ST01       | #20 ACTIVE courses + #38 recorded awards; dashboard có widget states.                                                               | #21 trả `UserProfile`, không phải progress; #43–#45 còn `SOURCE_ONLY`/DDL dependency; không giả KPI, chứng nhận hoặc notification. Xem Stitch và đảm bảo card độc lập/error state đúng.                                                                                                                                                              |
| ST02       | Route `/student/profile`; route metadata #04; hiện page còn sign-in gate.                                                        | StudentLayout đã có login #03 và token, nên copy “chưa có Student session” là lỗi thời. KiPrompt bàn giao: hểm tra #04 và DD/ảnh để quyết định cách hiển thị safe UserProfile; nếu loaded design chưa đủ thì giữ gate với lý do đúng, không bịa layout/data.                                                                            |
| ST03       | Route `/student/profile/edit`; metadata #04/#13/#14; G-03 gate.                                                                    | Session #03 hiện có; #04 có thể là GET/read source-backed nhưng phải xác minh UI mapping. Giữ upload/save/phone/bio gates đến khi discrepancy #13/#14 được giải quyết: #13 nhận JSON Data URL, trả `avatar_url` nhưng không update DB; #14 nhận `full_name`, nullable `phone`/`avatar_url`, bỏ qua `bio`; reload/update policy chưa chốt. |
| ST04       | #08 public course detail được gọi trước gate.                                                                                  | Không gọi #15: request có fallback khi thiếu/invalid auth có thể lấy enrollment user khác.                                                                                                                                                                                                                                                                          |
| ST05       | #08 được gọi; unavailable checkout state.                                                                                        | Không gọi #16: `orders` không có trong checked-in DDL; test/amount/provider/idempotency/persistence chưa đủ.                                                                                                                                                                                                                                                       |
| ST06       | Page/route gán #17/#18 nhưng payment gate.                                                                                         | #17 fail-closed 503 trước persistence; #18 là notification operation, không phải payment tracking. Không tạo payment/result giả.                                                                                                                                                                                                                                    |
| ST07       | Result gate với #18/#19/#20 metadata.                                                                                               | #19 phụ thuộc PAID `orders`; #18 notification-only; #20 projection khôngtại chứng minh entitlement/payment. Không tự suy ra enrollment success.                                                                                                                                                                                                                    |
| ST08       | #20 paged course list; hiển thị response fields và pagination; ACTIVE row mới link ST09.                                         | #21 không dùng vì trả `UserProfile`; filter/progress merge theo DD chưa có contract.                                                                                                                                                                                                                                                                                |
| ST09       | Tìm course `ACTIVE` bằng page traversal #20 rồi lấy aggregate #37.                                                             | #09 là public curriculum, không chứng minh entitlement; không đưa media/course tree/lesson picker chưa có source an toàn. Chưa có lessonId handoff đến ST10.                                                                                                                                                                                                   |
| ST10       | #22 khi vào; explicit #23 chỉ khi #22 trả cùng lesson ID và `status=PUBLISHED`; sau start điều hướng ST11, ST11 gọi #24. | #22 không lọc lesson status; #23 không tự kiểm tra lesson/course publication. Client gate không sửa được backend discrepancy.                                                                                                                                                                                                                                     |
| ST11–ST25 | Có screen-local callers trong code cho behavior giới hạn theo source.                                                             | Rà theo từng hàng matrix/DD: #25 không lưu được vị trí DD yêu cầu; #26 URL/resource access policy, #27 next/terminal semantics còn mở; quiz/assignment/discussion APIs có request/response gaps; #40 text `course_id` vs catalog int64. Không tự bật behavior vượt source.                                                                            |
| ST26       | Metadata #43/#44/#45, không có caller.                                                                                             | Giữ gate: query phụ thuộc `notification_recipients` không tồn tại trong checked-in DDL; không gọi descriptor `SOURCE_ONLY`.                                                                                                                                                                                                                                     |

### Student session hiện tại

`StudentLayout` gọi API #03, chấp nhận role STUDENT, giữ access/refresh token
trong tab memory; `StudentApiService` gắn Bearer và kết thúc local session khi
protected call trả 401. Refresh `R-X01` là source-only route. Session hiện có
thể thay đổi các giả định cũ về ST02/ST03, nhưng không tự giải quyết screen
design hoặc API mutation contract.

### Mentor

ME01–ME18 đã có group route/layout/session và screen-local service/page cho
behavior source-backed; route metadata được gắn theo từng screen. API mapping
chính ghi trong T038: ME01 #46/#54/#58; ME02 #46; ME03 #46/#49/#65; ME04
#46 (lecture create #34/#47 còn gated); ME05 #48; ME06 #49; ME07 #49/#50/#51;
ME08 #49/#52/#53; ME09 #54; ME10 #55/#56/#57; ME11 #58; ME12 #59/#60/#61;
ME13 #46/#62; ME14 #62/#63 (dispatch chưa gọi); ME15 #64 (không dùng #18);
ME16 #65; ME17 #67; ME18 #66. Rà current templates/actions; giữ gates ở những
chỗ DD/request khác nhau. Không dùng sample identity/KPI/chart/SLA như dữ liệu
server. Local focused server tests từng được ghi cho #46–#67 nhưng không chứng
minh deployed schema hoặc browser runtime.

## API/server discrepancies cần giữ nguyên

| API/source    | Ảnh hưởng tới screen                                                                 | Hành động an toàn                                                                     |
| ------------- | ---------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| #20           | Runtime trả paged `CourseSummary`; catalog cũ nói `UserProfile`.                  | Map theo source DTO hiện tại; không tự đổi response hoặc thêm fields.             |
| #21           | Handler trả UserProfile, không tính progress.                                         | Không dùng cho ST01/ST08/ST20 progress.                                                 |
| #22/#23       | #22 không lọc lesson status; #23 upsert progress nhưng không check publication.      | ST10 chỉ explicit start sau #22 cùng ID + PUBLISHED; ghi server-side discrepancy.       |
| #37           | Course aggregate counts/percent only.                                                    | Không suy ra lesson list hoặc per-lesson state.                                         |
| #38           | Đọc achievement records, không có producer.                                          | Hiển thị bản ghi trả về; không gọi là certificate/verified award ngoài contract. |
| #43–#45      | Source-only ở FE; query phụ thuộc bảng thiếu trong checked-in DDL.                  | Không gọi cho tới khi source/DDL/contract đủ bằng chứng.                           |
| #15           | Optional/invalid auth fallback có thể trả enrollment của người khác.              | Không gọi từ ST04.                                                                     |
| #16/#19       | Dùng `orders` không có trong checked-in DDL; #16 thiếu focused tests.              | Không tạo order/enrollment hoặc tuyên bố mua thành công.                           |
| #17/#18       | #17 fail-closed; #18 notification-specific, không phải operation tracking tổng quát. | ST06/SH07/AD25 không giả paymenttại lifecycle.                                         |
| #25–#27      | Position/resource URL/lesson sequencing khác hoặc chưa đủ DD.                       | Gắn UI đúng phần source-supported; disabled phần còn lại.                          |
| #31, #35–#45 | Một số route/module không có focused test package.                                   | Ghi rõ bằng chứng; không biến route presence thành verified runtime.                |
| #99–#103     | Chưa có route source.                                                                  | Screen phụ thuộc chúng giữ unavailable state; không tạo endpoint trong frontend.    |

Các trạng thái `R/P/SOURCE_ONLY/D` trong matrix chỉ mô tả source/test evidence;
không xác nhận migration/live DB, production deployment hoặc API đang chạy.

## Công việc còn lại — thực hiện theo thứ tự

Các trọng số dưới đây là plan takeover ban đầu, tổng 100%. Sau bước takeover,
hãy giữ/điều chỉnh bằng evidence thực; không cộng lại công việc đã làm.

| Step                             | Trọng số | Deliverable và tiêu chí hoàn tất                                                                                                                                                               |
| -------------------------------- | ---------: | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| R0 — Takeover/preflight         |        10% | Kiểm tra branch/status/diff và bảo toàn dirty tree; đọc router/context/workflow/worklog; xác định screen/API scope thật.                                                                  |
| R1 — Reconcile gap và contract |        15% | Duyệt 83-ID matrix so với route/page/caller hiện tại; chọn các `PARTIAL/GATE_ONLY/UNWIRED`; đọc DD/Stitch/server source chính xác cho phần định sửa; cập nhật discrepancy ledger. |
| R2 — Hoàn thiện screen/caller |        45% | Sửa các screen còn thiếu/không nhất quán; ưu tiên ST02/ST03 session/profile mismatch, rồi các screen partial có API source-backed. Không xây lại page đã wired/gated đúng.       |
| R3 — UI và documentation sync  |        15% | Rà ST01/ST08/ST09/ST10 visual states và các target thực sự sửa; đồng bộ screen inventory, DD current-caller notes, source architecture, gap matrix và T038 changes/handoff.               |
| R4 — Verification/closeout      |        15% | Production build, diff check, context validator khi phù hợp; cập nhật T038 milestones/worklog và ghi rõ test/browser/live DB status.                                                          |

### R0 — Takeover/preflight (10%)

1. Gửi chat task classification/milestones theo repository rules; tạo hoặc cập
   nhật worklog coding. Worklog T038 đang `IN_PROGRESS`; chọn tiếp tục log này
   hay tạo log continuation theo convention hiện tại và ghi link giữa hai log.
2. Kiểm tra `git status --short --branch`, branch/HEAD, package scripts và
   status các target. Tuyệt đối không clean/reset/restore user changes.
3. Đọc 3 worklog `coding` gần nhất do selector hiện tại trả về, rồi đọc T038,
   gap matrix, các phần relevant của T037 và task tracker. Selector result từ
   2026-11-17 là lịch sử; chạy lại trên checkout tiếp quản.
4. Đọc root/global/scope rules và registry; `web-work/study` screen workflow
   là workflow bắt buộc. `server-study` chỉ load API pages/modules cần thiết.

### R1 — Reconcile 83 screen IDs và API contracts (15%)

1. Đối chiếu `list_screen.md`, `screen-index.md`, T038 matrix với router groups,
   component selectors, route data API IDs, screen services và callsites. Phân
   biệt request thật với metadata/wrapper chỉ tồn tại.
2. Lập current checkpoint cho từng ID theo `COMPLETE`, `PARTIAL`, `GATE_ONLY`,
   `UNWIRED` hoặc `NOT_STARTED`, kèm file/path và API caller evidence.
3. Tập trung các status đã có dấu hiệu stale: ST02/ST03 không còn đúng khi nói
   “Student session/token chưa có”; T038 handoff nói tiếp ST01/ST06–10/Mentor
   dù các code waves đã thực hiện; `gui/architech.md` có ST02/03 cũ và mô tả
   ST11 fallback cũ; kiểm tra các đoạn current-source trong `list_screen.md`,
   `.agents/web-work/`, DD ST01–ST26 và server `declared-routes.md`.
4. Với mỗi API target, trace route → view → validator/query/model → side effect
   → response → focused test source, đặc biệt các discrepancies ở bảng API.
   Không mở rộng server scope nếu FE không cần endpoint đó.

### R2 — Hoàn thiện screen/caller (45%)

**Ưu tiên A — ST02/ST03:**

- Student auth #03 đã có trong `StudentLayout`, nên bỏ copy sai yêu cầu đăng
  nhập nếu page đã nằm bên trong authenticated layout.
- #04 GET `/users/me` có source và `StudentApiService`; DTO an toàn hiện gồm
  `id`, `full_name`, `email`, `role`, nullable `avatar_url`, nullable `phone`,
  `status`, `created_at`, `updated_at`; không có `bio`/`permissions`.
- Kiểm tra DD ST02/ST03, ảnh và source Stitch để chỉ hiển thị field/state được
  phép. Nếu xây ready state tối thiểu từ response, dùng loading/error/retry và
  không giả avatar/profile. Nếu visual contract thực sự chưa cho phép ready
  state, giữ gate nhưng sửa lý do cho đúng: chưa chốt design/mapping, không phải
  session thiếu; ghi source gate rõ trong row/document.
- ST03 có thể đọc hồ sơ qua #04; giữ #13 upload và #14 save, phone/bio controls
  an toàn cho tới khi request/mapping được xác nhận. Không tự quyết định policy
  chỉ vì request model hiện có fields.

**Ưu tiên B — verify các screen mới nối API:**

- ST01: #20/#38 độc lập, widget errors/empty; #21/#43 gate thật.
- ST08: #20 page results; pagination không vượt `total_pages`; chỉ ACTIVE mở
  ST09; không tính progress giả.
- ST09: #20 ACTIVE membership trước #37; no access via public #09; không có
  lesson picker/handoff nếu không có safe lesson ID.
- ST10: #22 ID match/status check, chỉ explicit #23 khi PUBLISHED, sau success
  sang ST11 #24. Giữ content/video ngoài preview.

**Ưu tiên C — kiểm tra screen partial/gated trong ma trận:**

- ST04–ST07: hiện có #08 revalidation/gate; giữ #15/#16, payment và result
  gates theo bảng server discrepancies.
- ST11–ST25 và ME01–ME18: giữ source callers hiện có, rà exact API DTO và các
  nút/action bị disable. Sửa trường hợp caller/UI sai hoặc thiếu mà có source
  evidence; không viết lại cả group.
- ST26, SH07, GS06/GS07, AD01/AD24/AD25: tiếp tục gate cho source/schema/contract
  còn thiếu.
- SH/GS/Admin còn lại: dùng ma trận để xác định các state/API discrepancies
  thật; chỉ thực hiện behavior có source/contract hỗ trợ, ưu tiên không trùng
  các slice đã nghiệm thu trước đó.

### R3 — UI và documentation sync (15%)

1. So sánh screen cần sửa với clean/numbered Stitch assets và DD states; giữ
   semantic tokens, responsive behavior, focus/keyboard/ARIA. Không thay đổi
   design system ở phạm vi toàn app nếu không cần.
2. Đồng bộ API reverse index/caller table trong `docs/list_screen.md`,
   package `00-overview.md`/`04-api-integration.md`, `screen-index.md`,
   `.agents/web-work/` hoặc `.agents/server-study/apis/declared-routes.md` chỉ
   khi source status thật sự đổi.
3. Cập nhật `T038-screen-gap-matrix.md` và active worklog. Trong T038, nối
   event sau E34 với ID mới; cập nhật `CURRENT_BEHAVIOR`, `CHANGES`,
   `DISCREPANCIES_AND_STATUSES`, `VERIFICATION`, `HANDOFF`, `MILESTONES`.
   Handoff cuối phải ghi chỉ còn gates/runtime chưa resolve, không ghi code đã
   làm là “next action”.
4. Giữ expected DD/API text khác với current caller note. Nếu contract chưa
   đổi, đừng sửa expected behavior để khớp UI.

### R4 — Verification và closeout (15%)

- Từ `apps/study-client/`, chạy `npm run build`. Ghi exit status và warning
  thật; trước đó build đã pass nhưng có bundle/CSS budget warnings. Hai rule nhỏ
  trong ST09/ST10 được bỏ sau lần build gần nhất, vì vậy chưa có bằng chứng
  build sau lần sửa cuối.
- Chạy `git diff --check` cho tracked diffs và kiểm tra whitespace/link trong
  tài liệu untracked bằng cách phù hợp; xác nhận không vô tình xóa/đè dirty file.
- Vì `.agents`/canonical pages từng thay đổi, chạy
  `node scripts/validate-agent-context.mjs`; so findings theo identity/path
  với recorded baseline (T038: `AGENT_CONTEXT_INVALID`, 1,431 output lines,
  SHA-256 `7496126958d348bb35ec8a7df9ca7228326ba4735b79536b28119e6d26afe9e0`).
  Số finding cũ từng được ghi ở các worklog khác nhau; rerun là bắt buộc, không
  gọi baseline invalid là pass và sửa finding mới do task gây ra.
- Không báo tests/browser/live API/DB pass khi chưa thực chạy. Worklog trước
  ghi không chạy tests; browser CUA không có surface; authenticated deployed
  UI, live schema/API và production deploy chưa xác minh. Tuân theo lệnh cấp
  cao hơn về việc có được chạy test hay không.
- Đạt Definition of Done bên dưới rồi mới đặt T038 `100%`/`DONE`; nếu còn gate
  nghiệp vụ, report implementation partial với gates cụ thể chứ không đợi gate
  external để hoàn thiện những phần độc lập.

## Definition of Done

- Từng 83 ID đã được rà theo source hiện hành và có trạng thái có bằng chứng;
  API metadata được phân biệt với caller thật.
- Mọi behavior có nguồn client/server đủ rõ được hiển thị/call đúng; các API
  không an toàn, unavailable, source-only hoặc contract mismatch tiếp tục gate
  với copy có lý do chính xác.
- ST02/ST03 không còn mâu thuẫn auth copy với StudentLayout; các profile fields
  chỉ lấy từ #04 và không bịa bio/permission.
- ST01/ST08/ST09/ST10 caller, error/loading/empty/navigation và visual intent
  khớp current source/DD; các caller Student/Mentor khác không bị regression.
- UI không chứa sample data như dữ liệu thật, mọi route IDs được parse an toàn,
  protected calls dùng role session/Bearer wrapper, token không persistent.
- `list_screen`, screen DD caller notes, gap matrix, canonical context và
  worklog không tự mâu thuẫn nhau; test/build/validator/browser/API/DB status
  được ghi đúng thực tế.
- `npm run build` và `git diff --check` đạt; validator kết quả được phân loại
  so với baseline; không có user-owned changes bị reset hoặc xóa.

## Bằng chứng có sẵn trước takeover

- T038 đọc 83-ID inventory, DD, screen_stitch, route/API/data-access và source
  Study Server; ma trận là structural crosswalk.
- ST01/ST08/ST09/ST10 đã thêm screen-local services/pages/templates/styles
  cho #20/#38, #20, #20/#37, #22/#23; ST11 dùng #24 sau ST10 handoff.
- T038 đã cập nhật current caller notes ở 20 API-integration DD pages
  `ST-01` và `ST-08..ST-26`, overview ST01/ST08/ST09/ST10, list screen,
  matrix, web/server context và API #22–#24 discrepancy.
- Build gần nhất chạy trước khi cắt bớt một CSS rule ở ST09 và một ở ST10:
  exit 0; trước cleanup có initial bundle khoảng 536.68 KB so với 500 KB,
  ST09 4.09 KB và ST10 4.07 KB vượt component budget nhẹ. Các warning cũ
  gồm Student layout, ST22, Student static shell và một số Mentor page. Build
  cuối chưa chạy.
- Tests không chạy trong lượt coding cuối; browser/live API/live DB chưa xác
  minh. Build compile thành công không xác nhận behavior/auth/deployment.

## Handoff kết thúc

Khi xong, cập nhật T038 worklog và gap matrix với trạng thái thực, milestone
progress và event receipts; ghi danh sách gates còn tồn tại (ST02/03 design/API
read rules nếu chưa chốt, ST04/#15, ST05/#16, ST06/07 payment/result,
ST09→ST10 lesson selection, #21, #22/#23 server discrepancy, #43–45,
resource/lesson progression, Mentor/Guest/Admin API gaps, live DB/deploy). Báo
ngắn gọn các file trọng tâm đã đổi, verification đã chạy, warnings còn lại và
những điều chưa thể xác minh. Không gọi task hoàn tất 100% nếu còn required
implementation/verification action chưa xong.
