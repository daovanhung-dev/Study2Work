# ST-13 — Giới thiệu bài kiểm tra · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `ST-13` |
| Module | Student |
| Route | `/student/quizzes/:quizId` — route trong inventory, không phải xác nhận router runtime |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source status: **Trạng thái:** `DD BLOCKED` · `IMPLEMENTATION BLOCKED` · `RUNTIME NOT VERIFIED` |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
| Nguồn đối chiếu | [ST-13.md](../../screen_stitch/03_student/ST-13_gioi-thieu-bai-kiem-tra/ST-13.md), [ST-13_PLAN.md](../../screen_stitch/03_student/ST-13_gioi-thieu-bai-kiem-tra/ST-13_PLAN.md), [ST-13_markers.json](../../screen_stitch/03_student/ST-13_gioi-thieu-bai-kiem-tra/ST-13_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Tiêu đề, thời hạn và quy định chấm; xác nhận bắt đầu.
- In-scope: GET #28 theo thiết kế; ST-13 row kỳ vọng POST #29 sau explicit Start, nhưng F05/ST-14 row/DD mâu thuẫn về screen owner và GET/POST order; ST-14 path còn yêu cầu `attemptId` trước entry nếu #29 được dời sang đó. Owner phải chốt một call-site/entry route, không gọi lặp.
- Out-of-scope: Xem gate bên dưới; không kết luận Study Web route/UI đã wired hoặc runtime đã chạy.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-16 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Tiêu đề, thời hạn và quy định chấm; xác nhận bắt đầu. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #28
- Liên kết màn hình dự kiến: [ST-14](../ST-14-LamBaiKiemTra/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | loading/closed/available/denied |
| Current runtime | Worklog/context Study Web | `UNWIRED` / `RUNTIME NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [ST-13 source screen.png](../../screen_stitch/03_student/ST-13_gioi-thieu-bai-kiem-tra/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/03_student/ST-13_gioi-thieu-bai-kiem-tra/screen_annotated.png))
- Luồng: GET #28 theo thiết kế; ST-13 row kỳ vọng POST #29 sau explicit Start, nhưng F05/ST-14 row/DD mâu thuẫn về screen owner và GET/POST order; ST-14 path còn yêu cầu `attemptId` trước entry nếu #29 được dời sang đó. Owner phải chốt một call-site/entry route, không gọi lặp.
- Priority: P1; Gate/source status: **D; DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED:** #28/#29 Student route/module/test NOT_FOUND; PNG/HTML mismatch; eligibility, answer exposure, timing, attempt limit/resume/idempotency và CTA destinations open; #29 owner/order/entry route conflicts across ST-13/F05/ST-14; legacy BIGINT Quiz/Attempt differs from V1-PILOT UUID Assessment model; sample history/proctoring/scoring/certificate claims unsupported; Study Web UNWIRED

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

# ST-13 — Giới thiệu bài kiểm tra

> **Trạng thái:** `DD BLOCKED` · `IMPLEMENTATION BLOCKED` · `RUNTIME NOT VERIFIED`
> Tài liệu đối chiếu ảnh/HTML và contract thiết kế. Không có bằng chứng Study Web đang render route hoặc gọi API #28/#29.

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: A. Tổng quan màn hình

| Thuộc tính | Đặc tả |
|---|---|
| Screen ID / tên | `ST-13` — Giới thiệu bài kiểm tra (Page) |
| Mục tiêu | Cho Student xem thông tin quiz được phép hiển thị, kiểm tra điều kiện trước khi bắt đầu, xác nhận bắt đầu và chuyển sang ST-14 khi tạo attempt thành công. |
| Actor / quyền | Student. API catalog #28/#29 yêu cầu Bearer JWT, role `Student`; AC-16 yêu cầu Student có quyền làm quiz và quiz đang mở. Predicate, claim và nơi kiểm tra cuối cùng chưa được chốt. |
| Route thiết kế | `/student/quizzes/:quizId`, theo [screen inventory](../../list_screen.md). Chưa có Study Web route/source để xác minh. |
| Input route | `quizId` ánh xạ tới API `quiz_id:int64!`; min/max, positivity và lỗi path parse chưa được quy định. Không tự tạo mã lỗi client/server. |
| Màn hình trước | Inventory/F05 liên kết tới ST-13 từ luồng học/quiz, nhưng không có hợp đồng hiện tại truyền lesson/course context đủ để xác định breadcrumb. |
| Màn hình sau | ST-14 — Làm bài kiểm tra, route thiết kế `/student/quizzes/:quizId/attempts/:attemptId`; cần `quizId` và `attemptId` hợp lệ. Screen owner/order của POST #29 còn mâu thuẫn giữa ST-13, F05 và ST-14; nếu #29 thuộc ST-14 thì entry route cần có `attemptId` trước khi attempt được tạo, nhưng chưa có route/handoff contract giải quyết điểm này. |
| API thiết kế | GET #28 theo inventory; ST-13 row đặt POST #29 sau thao tác Start, nhưng F05/ST-14 đặt call-site/order khác. API #28/#29 đều chưa có Student route/module/test hiện hành; chờ owner chốt call-site trước implementation. |
| Tài sản | [PNG nguyên trạng](../../screen_stitch/03_student/ST-13_gioi-thieu-bai-kiem-tra/screen.png), [HTML](../../screen_stitch/03_student/ST-13_gioi-thieu-bai-kiem-tra/code.html), [PNG đánh số](../../screen_stitch/03_student/ST-13_gioi-thieu-bai-kiem-tra/screen_annotated.png), [marker map](../../screen_stitch/03_student/ST-13_gioi-thieu-bai-kiem-tra/ST-13_markers.json), [SVG overlay](../../screen_stitch/03_student/ST-13_gioi-thieu-bai-kiem-tra/ST-13_markers_overlay.svg), [kế hoạch](../../screen_stitch/03_student/ST-13_gioi-thieu-bai-kiem-tra/ST-13_PLAN.md). |
| Kết quả tải vào/ra | Tải: không có payload màn hình trước được đặc tả ngoài `quizId`. Ra ST-14: cần `quizId` và `attemptId` từ kết quả POST #29; không truyền đáp án hoặc tự sinh attempt ID. |

### Phân biệt expected behavior và current behavior

**Expected theo inventory/AC/API design**

- ST-13 gọi GET #28 để đọc metadata/câu hỏi được phép hiển thị.
- ST-13 inventory row đặt POST #29 sau thao tác “Bắt đầu”; F05 shorthand và ST-14 inventory/DD lại đặt #29 ở ST-14 và còn khác thứ tự #28/#29. Đây là `DISCREPANCY`, chưa phải trigger đã thống nhất.
- Student chỉ được làm quiz khi đủ quyền và quiz đang mở. AC-16 ghi đây là precondition nhưng chưa định nghĩa predicate.
- Student projection không được lộ `quiz_choices.is_correct`. API #28 DD giữ field này ngoài response.
- Inventory mô tả các trạng thái `loading`, `closed`, `available`, `denied`; API #28 không có 409 và chưa định nghĩa cách biến đổi trạng thái quiz thành các response này.

**Current source/artifact**

- `screen.png` là mockup tĩnh 1349×1600. Nó hiển thị dữ liệu mẫu như 20 câu, 30 phút, 80%, 2/3 lượt, “Attempt 2”, kết quả lần trước, proctoring, realtime autosave, auto-submit, quy tắc chấm và chứng chỉ.
- `code.html` là HTML tĩnh khác hẳn: chỉ có fallback “Thông tin bài kiểm tra hiện chưa sẵn sàng” cùng link “Quay lại khóa học”. HTML nạp Tailwind qua CDN và có inline theme config, nhưng không có fetch, state handler, timer, API call hoặc router handler. CDN/config chỉ phục vụ prototype styling; không chứng minh Study Web runtime. Các anchor tĩnh không chứng minh route đang hoạt động.
- Không tìm thấy Student API #28/#29 trong [Study router](../../../../study-server/app/api/v1.py), module hoặc tests. Router/context hiện có API #87–#91 là **Admin quiz**, khác endpoint Student #28/#29.
- Schema candidate không thống nhất: legacy `DB.sql` dùng `BIGINT quizzes/quiz_attempts`, còn V1-PILOT `02_study_db.sql` dùng UUID `assessments/assessment_attempts`, `quiz_questions.assessment_id` và `quiz_options`. Không có bằng chứng live schema hoặc mapping `quiz_id:int64` sang UUID assessment.
- Không có bằng chứng chạy browser, triển khai Study Web hoặc live database/schema. Các claim trong ảnh không được ghi thành behavior hiện tại.
