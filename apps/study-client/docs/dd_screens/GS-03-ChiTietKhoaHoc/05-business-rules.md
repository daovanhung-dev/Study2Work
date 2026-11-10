# GS-03 — Business Rules

## 1. Rule index
| Rule ID (package alias) | Tên / source ID | Áp dụng | Thực thi | Tests |
|---|---|---|---|---|
| `GS-03-BR-001` | Source rules/gates bundle (alias only) | See source DD | Not re-inferred | See source acceptance |

## 2. Rules, security, discrepancy và gate từ source
- Inventory purpose: Thông tin khóa học, mentor, giá, tab đề cương/đánh giá, CTA ghi danh.
- Gate/status (giữ nguyên): **R (#08/#09), D (#10)**; **BLOCK:** #08 trả singleton Page<Course>, source LEFT JOIN khác API DD INNER JOIN; int64 course_id chưa khớp validator raw-string không có signed int64 range; AC-05 eager khác F02 lazy; #10 thiếu route/title-rating source; G-01 enrollment handoff; Study Web UNWIRED
- BR IDs trong file này chỉ là alias trỏ tới source rule/gate bundles; không thêm business rule. Không khẳng định rule FE/BE mới khi source chưa xác nhận.

### Trích từ DD nguồn: G. Business rules, security và dependencies

1. Public detail/curriculum chỉ trả dữ liệu course PUBLISHED trong current #08/#09 source. Không render draft/private data, kể cả nếu link đầu vào chứa ID.
2. #08 current API trả 404 cho invalid/missing/unpublished; AC-05 ghi 404/403. Chốt error mapping với API/UI owner trước runtime. Không lộ trạng thái draft qua nội dung lỗi.
3. Catalog #08/#09 khai báo `course_id:int64`; current routes nhận `str` và `parse_integer` không enforce int64/positive range. Chốt giới hạn/validation và oversized-ID error mapping; không gán behavior chưa được xác minh.
4. API #08 current query dùng `LEFT JOIN` nhưng API DD ghi `INNER JOIN`; `mentor_id` có thể nullable trong checked-in DDL, trong khi mapper/model yêu cầu mentor ID/name. Thiếu mentor data được map thành 500. BE cần xác nhận join/data-integrity policy.
5. `price` từ #08 là string; không suy ra free/paid, payment completion, currency hoặc eligibility nếu chưa có price policy. F03 nói giá #08 không đủ xác minh payment.
6. API #09 chỉ lọc lesson `PUBLISHED`; không có field/contract cho preview hoặc access control. Không tự thêm lesson click/open behavior.
7. Không hiển thị review title/rating/average dựa trên `discussions`; API #10 chưa wired và schema hiện thiếu nguồn.
8. #15 enrollment status không thuộc API set của GS-03 và hiện G-01 security blocker. Không thêm anonymous user selection, user_id, enrollment response, request hoặc success state.
9. Remote font/Tailwind CDN trong `code.html` không phải runtime dependency được chốt; design target `.agents/web-study/design.md` yêu cầu no remote fonts, responsive layout, >=44px controls và keyboard/focus treatment. Cần áp dụng khi có thiết kế/UI implementation thực tế.
10. API #08/#09 test source đã đọc để đối chiếu; không chạy test theo giới hạn phiên. Không có live DB/runtime verification.

## 3. Quy tắc chưa xác nhận
- `CẦN_XÁC_NHẬN`: các quyết định/blocker trong inventory và DD nguồn chưa được giải quyết.
- Related IDs/source refs: Không có BR ID nguồn được chuẩn hóa.; xem [API](04-api-integration.md), [Events](02-events.md), [Tests](07-test-cases.md).
