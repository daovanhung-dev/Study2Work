---
task_id: "2026-11-05-study-screen-dd-sh-04"
date: "2026-11-05"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies:
  - "SH-04 bàn giao xác thực thư điện tử -> API Study #02 gửi yêu cầu xác thực"
status: "VERIFIED"
---

# Nhật ký công việc: Soạn tài liệu thiết kế chi tiết màn hình SH-04

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `/home/daovanhung/.local/opt/node-v22.23.4/bin/node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; đã đọc đủ 3 worklog được chọn trong danh sách worklog `docs`.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-05/check-study-screen-stitch-coverage.md`
    - carry_forward: Danh mục màn hình có 83 mã duy nhất và mọi mã đều có `screen.png` cùng `code.html`; đây là kiểm kê tài sản tĩnh, không xác nhận giao diện chạy thật.
  - path: `.agents/worklog/2026-11-05/load-study2work-context.md`
    - carry_forward: Cây hiện tại không có mã Study Web được nối khi chạy hoặc ngữ cảnh con Study Web; kiểm tra mã nguồn hiện có và giữ ranh giới giữa tài liệu thiết kế với triển khai.
  - path: `.agents/worklog/2026-11-05/organize-study-screen-stitch.md`
    - carry_forward: Tài sản được nhóm theo danh mục màn hình; giữ nguyên tệp gốc, thư mục tham chiếu `90_reference/` và các biến thể SH-01.
- shortage: `none` (đã đọc đủ 3 worklog được chọn)

## EXPECTED_BEHAVIOR

- Yêu cầu: Soạn trong phiên này riêng DD cho SH-04 bằng tiếng Việt, gồm kế hoạch chi tiết viết trước DD, chú thích ảnh đánh số, đặc tả thành phần/sự kiện/trạng thái và luồng API có căn cứ; cập nhật bảng theo dõi tổng.
- Hợp đồng/tài liệu DD được duyệt: `apps/study-client/docs/list_screen.md` và tài liệu hệ thống thiết kế trong `90_reference/`; phải giữ riêng yêu cầu thiết kế với hành vi API hiện hành.

## CURRENT_BEHAVIOR

- Mã nguồn/cấu hình: Đã đọc `list_screen.md` (hàng SH-04, F01, chỉ mục API và mẫu DD), `DESIGN.md`, HTML/PNG SH-04, hướng dẫn thiết kế Study, khai báo API #02 và mã kiểm thử liên quan. API #02 nhận `user_id` nguyên và `email`, chuẩn hóa địa chỉ, gọi bộ gửi thư được tiêm phụ thuộc mà không mở cơ sở dữ liệu; bộ gửi thư mặc định bỏ dữ liệu đầu vào và trả `accepted`. API trả HTTP 202, `DESIGN_OPERATION_ACCEPTED`, `data.status="accepted"`; lỗi dữ liệu trả 422, lỗi bộ gửi thư trả 500 `DESIGN_INTERNAL_ERROR`. API #01 trả hồ sơ có `id`/`email` sau khi xác nhận giao dịch; API #01 không gọi API #02.
- Kiểm thử có thể chạy: Không chạy. Chỉ đọc mã kiểm thử: xác nhận API #02 được gọi công khai, chấp nhận yêu cầu không có `Authorization`, không mở cơ sở dữ liệu, trả 202 khi bộ gửi thư chấp nhận, 500 khi bộ gửi thư lỗi và 422 khi phần thân yêu cầu thiếu.
- Nối môi trường khi chạy: `apps/study-client/` hiện chỉ có `docs/list_screen.md`; không có mã giao diện (`src`), bộ định tuyến hay gói cấu hình. `.agents/web-work/study/` cũng vắng mặt dù bộ định tuyến/tệp kê khai khai báo ngữ cảnh con. Màn hình và đường dẫn `/register/verification` vì vậy chỉ là thiết kế đích, chưa được nối trong bản làm việc.

## SOURCE_TRACE

```text
SH-03 POST /api/v1/auth/register -> xác nhận giao dịch và trả data.id/data.email -> SH-04 dự kiến ánh xạ sang user_id/email -> POST /api/v1/auth/verify-email/send -> bộ kiểm tra dữ liệu -> VerificationEmailProvider mặc định bỏ dữ liệu đầu vào và trả accepted -> HTTP 202 + data.status=accepted -> SH-02 là màn hình kế tiếp theo danh mục
```

## DISCREPANCIES_AND_STATUSES

| Hạng mục | Bằng chứng | Trạng thái | Tác động |
|---|---|---|---|
| Bộ gửi thư | Mã nguồn bộ gửi thư mặc định bỏ `user_id`, `email`, `trace_id` khỏi luồng và chỉ trả `status="accepted"`; không gửi thư, ghi hàng đợi hoặc tạo mã xác minh. | ĐÃ_XÁC_MINH | Chỉ hiển thị “đã được bộ thử nghiệm tiếp nhận”; không nói đã xếp hàng, gửi thư hay xác minh. |
| Các trạng thái mô phỏng trong HTML | `stub` dùng HTTP 200, `no-delivery` tự dựng dữ liệu, `error` dùng HTTP 503; API hiện tại trả 202 khi chấp nhận và 500 nếu bộ gửi thư phát sinh lỗi. | SAI_KHÁC | Không coi các trạng thái/mã mô phỏng là hành vi máy chủ; ghi rõ cần thay bằng trạng thái dựa trên phản hồi thật. |
| Mẫu cURL | HTML dùng URL ngoài thiếu tiền tố `/api/v1` và phần thân yêu cầu chỉ có `email`, trong khi API #02 bắt buộc cả `user_id` và `email`. | SAI_KHÁC | Không dùng mẫu cURL này làm ví dụ gọi API; tránh phát hành nút sao chép sai hợp đồng. |
| Nội dung hàng đợi | Mô tả HTML nói yêu cầu vào hàng đợi; bộ gửi thư stub chỉ bỏ qua dữ liệu và trả `accepted`. | SAI_KHÁC | Sửa nội dung trong đặc tả đích; không sửa HTML nguồn trong phạm vi phiên. |
| Study Web chưa được nối khi chạy | Cây có tài liệu `apps/study-client/docs` nhưng không có `src`/bộ định tuyến/gói cấu hình; `.agents/web-work/study/` không tồn tại. | ĐÃ_XÁC_MINH_TĨNH | DD chỉ là tài liệu thiết kế; đường dẫn trang và tương tác chưa được chứng minh khi chạy. |
| Hệ thống màu | `DESIGN.md` có màu YAML khác văn xuôi; HTML lại dùng `primary #004ac6` và `primary-container #2563eb`. Hướng dẫn Study `.agents/web-study/design.md` là đích riêng với `ocean-primary #0B5F8A`. | SAI_KHÁC | Ghi đúng màu quan sát được; khi triển khai Study phải theo hướng dẫn Study, không âm thầm đổi nguồn ảnh/HTML. |
| Nút tuyên bố WCAG | Ảnh có nhãn `PASS WCAG AA`, nhưng phiên này chưa đo độ tương phản hay kiểm tra tiếp cận. | CHƯA_XÁC_MINH | Không kế thừa nhãn chất lượng như kết quả kiểm định. |

## CHANGES

- Tài liệu SH-04 hiện nằm tại `apps/study-client/docs/screen_stitch/01_shared_auth_system/SH-04_handoff-xac-thuc-email/SH-04.md`, `SH-04_PLAN.md` và `SH-04_markers.json`; ảnh chú thích nằm cùng thư mục. Nhật ký di chuyển: `.agents/worklog/2026-11-05/co-locate-study-screen-documents.md`.
- Tệp được cập nhật: `apps/study-client/docs/screen_stitch/dd_screens/PLAN.md` (hàng SH-04) và nhật ký công việc này.
- CONTEXT_UPDATES: Không có.
- Trang ngữ cảnh được sửa: Không có.
- Ngôn ngữ: Phần diễn giải, tiêu đề và nhãn do phiên này soạn đều bằng tiếng Việt. Giữ nguyên tên định danh kỹ thuật, API, trường dữ liệu, giá trị/mã phản hồi và đường dẫn để bảo toàn khả năng đối chiếu. Mẫu lệnh cURL và các nút mô phỏng được ghi là nội dung tĩnh, không phải chức năng đã nối.
- Tệp `screen.png` và `code.html` nguồn không bị sửa.

## VERIFICATION

| Lệnh/đọc tài liệu | Kết quả | Trạng thái |
|---|---|---|
| `scripts/select-worklogs.mjs --type docs --limit 3` và đọc ba kết quả | Ba worklog cùng loại đã được đọc đầy đủ; không thiếu mục được chọn. | ĐÃ_XÁC_MINH |
| `AGENTS.md` cấp gốc, `.agents/AGENTS.md`, `.agents/context-map.md`, `.agents/worklog/TEMPLATE.md` | Đã nạp trước khi mở mã nguồn sâu. | ĐÃ_XÁC_MINH |
| `.agents/project/INDEX.md`, `.agents/web-work/AGENTS.md`, `.agents/web-work/INDEX.md`, `.agents/web-study/design.md`, ngữ cảnh máy chủ Study | Đã đọc sơ đồ quan hệ phạm vi; `.agents/web-work/study/` vắng mặt; `createDD-markdown` không áp dụng vì mục tiêu là DD giao diện, không phải DD API. | ĐÃ_XÁC_MINH |
| API #02 đường dẫn API/model/validator/view/bộ gửi thư và mã kiểm thử; API #01 view/query/mã kiểm thử | Đã mã truy vết đường dẫn API, đầu vào, tác động ngoài, envelope/mã lỗi, dữ liệu bàn giao; chỉ đọc kiểm thử, không chạy. | ĐÃ_XÁC_MINH_TĨNH |
| Ảnh/HTML SH-04 và tệp nguồn | Ảnh 1600×1280; PNG SHA-256 `07f88cb51f0c31a990b5f553a828b4f1cba3b3d7e648286f70e3604528aed396`; HTML SHA-256 `a524d7d9d5b5640273d9d84900f9ba6a68df8a434d1f0ff189d989e4a2575684`. | ĐÃ_XÁC_MINH_TĨNH |
| Kế hoạch, DD, bản đồ chú thích và ảnh chú thích | Đã tạo kế hoạch trước DD; có 12 nhãn số bằng tiếng Việt khớp giữa ảnh, DD và JSON. Ảnh chú thích được xem lại trực quan. | ĐÃ_XÁC_MINH |
| Đối soát tĩnh các tài liệu SH-04 | 19 liên kết tương đối trong DD mở được; kế hoạch/DD có đủ 12 hàng phần tử; PNG nguồn 1600×1280 và ảnh chú thích 3200×2560; các nhãn nằm trong giới hạn ảnh nguồn. | ĐÃ_XÁC_MINH_TĨNH |
| Đối chiếu nội dung nguồn và bảng tổng | SHA-256 PNG/HTML khớp trước và sau; bảng tổng có 83 mã duy nhất, gồm 4 mục `BẢN_NHÁP_ĐÃ_XONG` và 79 mục `CHƯA_BẮT_ĐẦU`; hàng SH-04 đã cập nhật. | ĐÃ_XÁC_MINH_TĨNH |
| Tính nhất quán tệp văn bản | Năm tệp văn bản có dòng kết thúc và không có khoảng trắng cuối dòng. | ĐÃ_XÁC_MINH_TĨNH |
| Chạy kiểm thử dự án | Không chạy theo giới hạn của phiên; chỉ đọc mã kiểm thử liên quan. | KHÔNG_CHẠY |

## HANDOFF

- Điều kiện còn chặn: Bộ gửi thư thật và điểm cuối xác nhận OTP/liên kết chưa có; môi trường chạy giao diện Study và ngữ cảnh con Study Web đang thiếu; các trạng thái lỗi/không giao thư trên HTML là mô phỏng sai hợp đồng; cơ chế truyền dữ liệu từ SH-03 sang SH-04 chưa được hiện thực hóa.
- Bước tiếp theo: Soạn tài liệu cho SH-05 trong phiên kế tiếp, sau khi kiểm tra lại thứ tự và nguồn hiện hành; SH-04 chỉ được hoàn tất ở mức tài liệu thiết kế, chưa đủ điều kiện triển khai.
