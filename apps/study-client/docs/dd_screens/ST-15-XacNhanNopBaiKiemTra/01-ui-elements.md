# ST-15 — UI Elements

## 1. Quy tắc ảnh & mapping
- [Ảnh gốc](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)
- Ảnh numbered được sao chép nguyên trạng từ `screen_annotated.png`; mapping lấy từ JSON marker và DD nguồn. Không đổi ID marker nguồn trong lần chuyển đổi này.
- Marker JSON nguồn: [ST-15_markers.json](../../screen_stitch/03_student/ST-15_xac-nhan-nop-bai-kiem-tra/ST-15_markers.json).

## 2. Danh sách phần tử
| Marker | Element ID trong package | Source Element ID | Nhãn từ marker JSON |
|---|---|---|---|
| #1 | `ST-15-EL-001` | `ST15-EL-01` | Header exit from quiz |
| #2 | `ST-15-EL-002` | `ST15-EL-02` | Study2Work Exam brand |
| #3 | `ST-15-EL-003` | `ST15-EL-03` | Header remaining-time pill |
| #4 | `ST-15-EL-004` | `ST15-EL-04` | Student profile |
| #5 | `ST-15-EL-005` | `ST15-EL-05` | Dimmed quiz backdrop |
| #6 | `ST-15-EL-006` | `ST15-EL-06` | Confirmation dialog surface |
| #7 | `ST-15-EL-007` | `ST15-EL-07` | Quiz icon tile |
| #8 | `ST-15-EL-008` | `ST15-EL-08` | Confirmation eyebrow |
| #9 | `ST-15-EL-009` | `ST15-EL-09` | Confirmation heading |
| #10 | `ST-15-EL-010` | `ST15-EL-10` | Submission explanation |
| #11 | `ST-15-EL-011` | `ST15-EL-11` | Answered count and progress |
| #12 | `ST-15-EL-012` | `ST15-EL-12` | Unanswered count and question chips |
| #13 | `ST-15-EL-013` | `ST15-EL-13` | Flagged count and question chip |
| #14 | `ST-15-EL-014` | `ST15-EL-14` | Remaining-time strip |
| #15 | `ST-15-EL-015` | `ST15-EL-15` | Synced-answer status chip |
| #16 | `ST-15-EL-016` | `ST15-EL-16` | Exam rules and attempt text |
| #17 | `ST-15-EL-017` | `ST15-EL-17` | Continue test button |
| #18 | `ST-15-EL-018` | `ST15-EL-18` | Submit now button |

## 3. Đặc tả từng element

### Trích từ DD nguồn: C. Đặc tả element

Marker tọa độ được tính trên ảnh nguồn 1600×1280; ảnh `screen_annotated.png` được xuất ở scale 2. Vùng/giá trị là quan sát ảnh mẫu, không phải dữ liệu production.

| # / Element ID | Tên, loại, vị trí và mục đích | Thuộc tính, nguồn, điều kiện và trạng thái | Sự kiện |
|---|---|---|---|
| 1 / `ST15-EL-01` | “Thoát bài thi”, điều hướng header, góc trái trên. | Label tĩnh trong mẫu. Destination, dirty-state guard và enabled policy chưa có contract; visible trong PNG. Focus/hover chưa có runtime. | `EV-07` |
| 2 / `ST15-EL-02` | Brand “Study2Work Exam”, header trái. | Brand asset/copy mẫu; nguồn brand toàn app chưa đối chiếu trong Study Web vì app UNWIRED. Display-only, không có sự kiện. | — |
| 3 / `ST15-EL-03` | Timer header `45:20 còn lại`. | Chuỗi mẫu, không có timer/deadline source hoặc format/expiry policy. Không dùng để khóa/nộp tự động. | `EV-06` |
| 4 / `ST15-EL-04` | Avatar/tên “Nguyen Hanh”, header phải. | Identity mẫu; không có profile mapping/context contract cho màn hình. Click destination không xác định; không coi tên/avatar là xác thực. | `EV-07` |
| 5 / `ST15-EL-05` | Backdrop tối/làm mờ quiz phía sau modal. | Trang nền bị làm mờ trong PNG; không phải tập controls riêng. Click-outside/escape close behavior chưa đặc tả; không được làm mất dirty answer state. | `EV-07` |
| 6 / `ST15-EL-06` | Modal/card xác nhận, bề mặt trung tâm. | Container mẫu, không phải data input. Dialog semantics, focus trap/restore, close affordance và responsive bounds cần chốt theo UI implementation. Visible ở confirm. | `EV-01`, `EV-07` |
| 7 / `ST15-EL-07` | Icon mũ tốt nghiệp trong tile. | Icon trang trí trong PNG; không encode trạng thái bằng icon đơn lẻ; decorative/aria-hidden khi triển khai nếu không bổ sung meaning. | — |
| 8 / `ST15-EL-08` | Eyebrow “XÁC NHẬN NỘP BÀI KIỂM TRA”. | Copy tĩnh trong asset. Visible ở confirm; không có validation/state riêng. | — |
| 9 / `ST15-EL-09` | Heading “Bạn đã sẵn sàng hoàn thành?”. | Copy tĩnh trong asset; heading của confirmation. Không tự thay bằng success copy trước #31 200. | — |
| 10 / `ST15-EL-10` | Giải thích sẽ chốt điểm và không sửa được câu trả lời. | Copy mẫu tuyên bố chấm tức thì. Phải sửa theo policy duyệt: AC-16 có thể `PENDING_GRADE`; không cam kết điểm tức thì. Sau submit, lock chỉ khi server accept. | — |
| 11 / `ST15-EL-11` | Card “Đã trả lời 18/20”, progress bar và 90%. | Tất cả số là mẫu. Formula answered/total, progress precision, source, freshness và empty/loading behavior chưa chốt. Không tính từ screenshot. | `EV-01` |
| 12 / `ST15-EL-12` | Card “Chưa làm 02 câu” với chip C.19/C.20. | Chưa có summary schema/definition cho unanswered. Chip click không được giả định là question navigation; danh sách IDs và click behavior chưa xác nhận. | `EV-01` |
| 13 / `ST15-EL-13` | Card “Cờ xem lại 01 câu”, chip Câu 15. | Flag là sample; không có field/API flag hoặc persistence contract trong #30. Không suy ra click navigation/toggle. | `EV-01` |
| 14 / `ST15-EL-14` | Strip “Thời gian làm bài còn lại 12 phút 15 giây”. | Thời gian mẫu, mâu thuẫn timer header. Không có server clock/deadline source; không auto-submit/expire dựa trên strip này. | `EV-06` |
| 15 / `ST15-EL-15` | Chip “Đã đồng bộ 18/20”. | Saved count/copy mẫu; chỉ được hiển thị từ trạng thái xác nhận của #30 sau khi contract có response/source. Không coi là barrier success chỉ dựa trên text. | `EV-01`, `EV-02` |
| 16 / `ST15-EL-16` | Card quy chế và lịch sử lần làm: tự chấm, attempt 2/3, còn 1 lượt. | Policy/ordinal/limit là copy mẫu, không có source ở #31 contract. Không hiển thị dynamic claim trước khi business rule/schema được duyệt. | `EV-01` |
| 17 / `ST15-EL-17` | Button “Tiếp tục kiểm tra”. | Action button trong modal. Enabled ở confirm theo mockup; loading/disabled behavior khi flush/submit chưa được thiết kế. Intended destination ST-14 cùng attemptId là suy luận từ tên và graph, route restore chưa chốt. | `EV-02` |
| 18 / `ST15-EL-18` | Primary button “Nộp bài ngay”. | Submit action. Chỉ bật khi route/context hợp lệ theo contract; khi operation đang chạy phải ngăn click gửi trùng ở UI. Loading/disabled and error copy cần chốt; button click không đồng nghĩa submitted. | `EV-03` |

## 4. Conditional UI & state variations
- States theo inventory: confirm/submitting/submitted/ambiguous-network
- Detail/conditional visibility: xem section elements/state của [DD nguồn](../../screen_stitch/03_student/ST-15_xac-nhan-nop-bai-kiem-tra/ST-15.md); không diễn giải ảnh tĩnh thành behavior runtime.

## 5. Link
- [Events](02-events.md) · [Data Flow](03-data-flow.md) · [Tests](07-test-cases.md)
