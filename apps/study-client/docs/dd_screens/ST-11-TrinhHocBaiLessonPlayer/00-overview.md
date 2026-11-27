# ST-11 — Trình học bài/lesson player · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `ST-11` |
| Module | Student |
| Route | `/student/lessons/:lessonId` — khai báo trong Study Client; live runtime chưa xác minh |
| Actor/role | Student; client dùng Student Bearer service và API #24 kiểm tra role/enrollment |
| DD status | Draft/contract còn mở; **Implementation:** PARTIAL · **Runtime:** NOT VERIFIED |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.2 / 2026-11-20 |
| Nguồn đối chiếu | [ST-11.md](../../screen_stitch/03_student/ST-11_trinh-hoc-bai-lesson-player/ST-11.md), [ST-11_PLAN.md](../../screen_stitch/03_student/ST-11_trinh-hoc-bai-lesson-player/ST-11_PLAN.md), [ST-11_markers.json](../../screen_stitch/03_student/ST-11_trinh-hoc-bai-lesson-player/ST-11_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Video/nội dung, mục lục, nút complete, vị trí học, bài tiếp theo.
- In-scope: GET #24; GET #26 lazy; PATCH #25 khi có biến cố progress hợp lệ; GET #27 sau completed.
- Out-of-scope: Xem gate bên dưới; không kết luận Study Web route/UI đã wired hoặc runtime đã chạy.

### Current implementation — 2026-11-27

- Study Client có route và page ST-11. ST-10 truyền `lessonId`; ST-11 gọi API #24 bằng Student Bearer, hủy request cũ khi route đổi ID, kiểm tra business code, payload và ID trả về, rồi hiển thị nội dung văn bản.
- Response guard chỉ chấp nhận lesson `PUBLISHED`; nhãn trạng thái hiển thị là “Đã xuất bản”, không phải raw enum.
- ST-11 có loading, lỗi có thể thử lại, nội dung và liên kết sang ST-12. Player/video, progress (#25), bài kế tiếp (#27), mục lục và completed state chưa được triển khai vì nguồn phát và progress/terminal contract còn thiếu hoặc khác catalog.
- Backend #24 kiểm tra lesson/course `PUBLISHED` và enrollment `ACTIVE` hoặc `COMPLETED`. #25, #26 và #27 có source route/module; ST-11 hiện không gọi #25/#27 và tải ST-12 theo thao tác người học.
- Local verification: five routed page tests cover #24 loading, invalid route/business-code/ID handling, gated player/progress UI, and retry; one service test verifies the exact #24 `lesson_id` mapping. The full Study Web suite passes 97 spec files / 345 tests. These use local mocks; browser/live runtime remains unverified. The source-DD paragraphs below continue to describe the original design, not current runtime behavior.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-14,AC-15 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Video/nội dung, mục lục, nút complete, vị trí học, bài tiếp theo. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #24, #25, #26, #27
- Liên kết màn hình dự kiến: [ST-12](../ST-12-TaiLieuKemBaiHoc/00-overview.md), [ST-09](../ST-09-TongQuanKhoaDangHoc/00-overview.md), [ST-13](../ST-13-GioiThieuBaiKiemTra/00-overview.md), [ST-17](../ST-17-ChiTietBaiTap/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | loading/playing/paused/progress-saving/finished |
| Current source | Study Client ST-11 | `loading / error+retry / lesson text`; player/progress/next chưa có · runtime chưa xác minh |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [ST-11 source screen.png](../../screen_stitch/03_student/ST-11_trinh-hoc-bai-lesson-player/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/03_student/ST-11_trinh-hoc-bai-lesson-player/screen_annotated.png))
- Expected flow: GET #24; GET #26 lazy; PATCH #25 on an approved progress event; GET #27 after completion. Current screen flow calls #24 and links to ST-12; it does not call #25/#27.
- Priority: P1; Gate/source status: **DD BLOCKED; IMPLEMENTATION PARTIAL; RUNTIME NOT VERIFIED:** Stitch player states and controls are not implemented; the #25 catalog asks for `position` while current request model only has `percent`/`completed`, aggregate and completion trigger remain open; #27 terminal behavior and enrollment check remain open; #26 is called by ST-12 and resource rows have no current producer; API DDs remain Draft; live DB/runtime not verified.

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.
- 2026-11-20 — Cập nhật trạng thái source hiện tại: route/#24 đã wired; request route-reactive, có validation/retry; player/progress/next và runtime vẫn chưa xác minh.

## Trạng thái và ranh giới bằng chứng

# ST-11 — Trình học bài / lesson player

> **DD status:** BLOCKED · **Implementation:** BLOCKED · **Runtime:** NOT VERIFIED<br>
> **Phạm vi phiên:** chỉ ST-11. Ảnh/HTML hiện có là fallback báo nội dung chưa sẵn sàng, không phải bằng chứng về lesson player đang chạy.

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: A. Tổng quan màn hình

| Thuộc tính | Đặc tả |
|---|---|
| Screen ID / tên | ST-11 — Trình học bài / lesson player |
| Mục tiêu kỳ vọng | Mở nội dung lesson mà Student có quyền xem; hiển thị nội dung/media, lưu progress theo contract, cung cấp tài nguyên và bài tiếp theo khi được hỗ trợ. |
| Actor | Student. API catalog #24–#27 yêu cầu Bearer JWT và role Student; actor/session hiện không được bind từ UI source. |
| Điều kiện trước (expected) | Route có `lessonId:int64` và Student context theo catalog; AC-14 yêu cầu đã enrolled, AC-15 yêu cầu có quyền xem. Identity binding, enrollment status/prerequisite và publish predicate chưa được chốt. |
| Điều kiện sau (expected) | AC-14 mô tả progress và course aggregate được cập nhật, completed lesson được đánh dấu, rồi có thể xác định lesson kế; trigger, aggregate, response và terminal behavior chưa có contract hoàn chỉnh. Current asset chỉ hiển thị fallback tĩnh. |
| Route kỳ vọng | `/student/lessons/:lessonId` theo `list_screen.md`; Study Web không có editable route/router trong checkout. |
| Input | `lessonId` từ ST-10; catalog #24–#27 khai báo `lesson_id:int64!`. ST-10/ST-09 handoff hiện chưa có lessonId source. |
| Điều kiện nghiệp vụ | AC-14: Student đã enrolled vào course chứa lesson; AC-15: Student có quyền xem lesson. Predicate, JWT identity binding và publish policy chưa được API owner xác nhận. |
| API thiết kế | #24 GET lesson; #25 PATCH progress; #26 GET resources; #27 GET next. Cả bốn trả `ApiEnvelope<Lesson>` theo catalog; #25/#26/#27 có discrepancy/open questions riêng. |
| Màn hình liên quan | ST-10 trước đó; ST-09 tổng quan khóa học; ST-12 tài liệu kèm bài học; ST-13 quiz; ST-17 assignment. Các route/transition cụ thể ngoài href trong static HTML chưa được wire. |
| Asset hiện tại | `screen.png` 1280×1024 và `code.html` là unavailable-content fallback tĩnh. Không có player/media/progress/resource/Next controls. |
| Trạng thái | DD BLOCKED bởi fallback/player design gap, #24–#27 design-only/open, #24 fetch ownership giữa ST-10/ST-11, progress policy và thiếu lessonId. Implementation BLOCKED do Study Web/API wiring chưa có. Runtime NOT VERIFIED. |

### Nguồn và mức độ bằng chứng

| Nguồn | Nội dung được dùng | Trạng thái |
|---|---|---|
| [Screen inventory](../../list_screen.md) và [global plan](../../screen_stitch/dd_screens/PLAN.md) | Route, actor, AC-14/15, #24–#27, expected states và linked screens. | Expected design |
| [AC API index](../../../../study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md) và [AC-14/15 diagram](../../../../study-server/docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) | Enrollment/access precondition, progress update/completion intent, lesson/resources/next sequence. | Business design; predicate/order/detail open |
| [API catalog](../../../../../docs/lists/list_api.md) | Request/response/auth/status declaration cho #24–#27. | Declared design |
| [API #24 DD](../../../../study-server/docs/dd/24_lessons_detail/00_Cover.md) và [open questions](../../../../study-server/docs/dd/24_lessons_detail/OPEN_QUESTIONS.md) | Entitlement, publish, errors, projection/null/path. | Draft — Needs Confirmation |
| [API #25 DD](../../../../study-server/docs/dd/25_lessons_progress/00_Cover.md) và [open questions](../../../../study-server/docs/dd/25_lessons_progress/OPEN_QUESTIONS.md) | Position, percent, state, update identity, aggregate, transaction, retry. | Draft — Needs Confirmation |
| [API #26 DD](../../../../study-server/docs/dd/26_lessons_resources/00_Cover.md) và [open questions](../../../../study-server/docs/dd/26_lessons_resources/OPEN_QUESTIONS.md) | Resource response/cardinality/access/visibility/URL/error. | Draft — Needs Confirmation |
| [API #27 DD](../../../../study-server/docs/dd/27_lessons_next/00_Cover.md) và [open questions](../../../../study-server/docs/dd/27_lessons_next/OPEN_QUESTIONS.md) | Curriculum order/tie-break, terminal result, auth, payload/path. | Draft — Needs Confirmation |
| Study Server [current router](../../../../study-server/app/api/v1.py), modules and tests | Exact current route/module/test search for Student lesson APIs. | #24–#27 NOT_FOUND; Admin #82–#86 are distinct |
| [Candidate DDL](../../../../../infra/postgres/study-server/DB.sql) and [DB design](../../../../study-server/docs/diagrams/DB_UNICA_TABLES.md) | Candidate lessons/resources/lesson_progress fields only. | Design artifact; live schema NOT VERIFIED |
| [Study Web context](../../../../../.agents/web-work/study/INDEX.md) and [Study UI guide](../../../../../.agents/web-study/design.md) | Current source status and intended UI/accessibility target. | Study Web UNWIRED; guide is not runtime evidence |
| [Source PNG](../../screen_stitch/03_student/ST-11_trinh-hoc-bai-lesson-player/screen.png), [source HTML](../../screen_stitch/03_student/ST-11_trinh-hoc-bai-lesson-player/code.html), [marker map](../../screen_stitch/03_student/ST-11_trinh-hoc-bai-lesson-player/ST-11_markers.json), [annotated PNG](../../screen_stitch/03_student/ST-11_trinh-hoc-bai-lesson-player/screen_annotated.png) | Visible fallback and static markup. | Design assets only |

### Discrepancies cần giữ rõ

1. Inventory gọi đây là lesson player nhưng screenshot/HTML chỉ hiển thị “Nội dung bài học hiện chưa sẵn sàng.” Không có loaded, playing, paused, progress-saving hoặc finished interface.
2. ST-10 inventory/DD gọi #24 trước handoff; ST-11 inventory cũng gọi #24 khi mở player. Chưa rõ màn nào sở hữu lần đọc, dữ liệu nào được handoff và có cần gọi hai lần không.
3. AC-15 diagram mô tả #26 trước #27 trước render; ST-11 inventory nói #26 lazy và #27 sau completed; không có source để chọn một orchestration.
4. API #26 khai báo `ApiEnvelope<Lesson>` dù tên/use case là resources. Reusable `Resource` là schema khác; không tự thay response.
5. API #25 yêu cầu `position`, nhưng candidate `lesson_progress` không có cột này; range, unit, state, update identity, autosave/throttle, aggregate và retry chưa chốt.
6. Candidate `resources` DDL không có visibility; URL stored-vs-signed và access policy không rõ. Không mở resource URL từ UI theo suy đoán.
7. ST-10/ST-09 hiện chưa truyền lessonId tới ST-11; current client route/runtime cũng không có.
8. HTML có các path href trực tiếp nhưng Study Web router/serving/deployment chưa xác minh; path string trong HTML không phải runtime navigation evidence.
