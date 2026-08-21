# 06. Báo cáo rà soát tính hợp lý của tài liệu BD V1-PILOT

## 1. Mục đích và phạm vi

Báo cáo này ghi lại kết quả rà soát bộ tài liệu nghiệp vụ Study2Work V1-PILOT. Mục tiêu là giúp các nhóm Sản phẩm, BA, QA và kỹ thuật phân biệt rõ:

- Những khác biệt đã được chuẩn hóa vì đã có nguồn quyết định rõ ràng.
- Những khoảng trống cần chủ sở hữu nghiệp vụ hoặc kiến trúc ra quyết định trước khi triển khai.

Báo cáo không bổ sung chức năng, API, bảng, cột hay kiểu liệt kê (`enum`) mới. Các mã định danh như `API-*`, `TBL-*`, `SCR-*`, `UC-*`, `BR-*`, `EVT-*` và `ERR-*` được giữ nguyên để truy vết.

## 2. Cách xác định nguồn chuẩn

Thứ tự ưu tiên được áp dụng đúng theo `01_TONG_QUAN_DU_AN.md`:

1. Quyết định nghiệp vụ trong tài liệu `01`.
2. Hợp đồng API và sự kiện trong tài liệu `04`.
3. Mô hình dữ liệu, tên bảng, cột và kiểu liệt kê trong tài liệu `03`.
4. Biểu đồ trong tài liệu `02`.
5. Đặc tả màn hình trong tài liệu `05`.

Khi chỉ khác tên vật lý của bảng, cột hoặc kiểu liệt kê, tài liệu `03` là chuẩn danh pháp nếu không làm thay đổi quyết định nghiệp vụ ở tầng cao hơn. Khi chưa có nguồn đủ rõ để chọn một thiết kế, mục đó được ghi là tồn đọng thay vì tự suy diễn.

## 3. Các điểm đã chuẩn hóa

| Vấn đề | Chuẩn đã áp dụng | Tài liệu bị ảnh hưởng |
|---|---|---|
| Quyền sở hữu `UC-*` | Tài liệu `01` sở hữu danh mục và quyết định nghiệp vụ của `UC-*`; tài liệu `02` chỉ diễn giải bằng biểu đồ và ma trận bao phủ. | `01`, `02` |
| Trạng thái minh chứng tại Dịch vụ Việc làm | Rút sự đồng ý chuyển bản chụp sang `HIDDEN`; thu hồi minh chứng từ Dịch vụ Học tập chuyển sang `REVOKED`. `HIDDEN` vẫn có thể chuyển sang `REVOKED` khi Dịch vụ Học tập thu hồi sau đó. Không dùng `WITHDRAWN` cho trạng thái này. | `01`, `02`, `03`, `04`, `05` |
| Hoàn tiền và tranh chấp thanh toán ngược | `SETTLED` của đơn thanh toán không bị ghi đè. Hoàn tiền, tranh chấp thanh toán ngược và điều chỉnh quyền lợi được ghi bằng hồ sơ và sổ cái riêng. | `01`, `02`, `03`, `04`, `05` |
| Tác vụ AI và duyệt đầu ra | Tác vụ AI dùng `QUEUED`, `RUNNING`, `SUCCEEDED`, `FAILED`, `CANCELLED`; trạng thái duyệt đầu ra là vòng đời riêng. Không dùng `READY` hoặc `REVIEW_REQUIRED` thay cho trạng thái tác vụ. | `01`, `02`, `03`, `04` |
| Đổi lịch phỏng vấn | Ứng viên xác nhận, từ chối hoặc gửi yêu cầu đổi lịch theo phiên bản lịch hiện tại; bên tuyển dụng quyết định và tạo phiên bản lịch mới. | `01`, `02`, `04`, `05` |
| Tạo và xuất bản việc làm | Luồng tạo `DRAFT`, kiểm duyệt và xuất bản được tách khỏi luồng ứng tuyển; bản nháp có thể sửa, còn bản đã xuất bản là bất biến. | `01`, `02`, `03`, `04` |
| Giới thiệu và hồ sơ ứng tuyển | Lời giới thiệu không tự tạo hồ sơ ứng tuyển. Bản ghi giới thiệu chỉ có thể liên kết với hồ sơ ứng tuyển sau khi ứng viên tự ứng tuyển. | `01`, `02`, `03` |
| Truy vết xóa dữ liệu | Sự kiện liên dịch vụ dùng `platformUserId` bất biến hoặc khóa giả danh có mô tả ánh xạ rõ ràng; không dùng hai khóa như thể chúng thay thế trực tiếp cho nhau. | `01`, `02`, `03`, `04` |
| Danh pháp Định danh nền tảng | Chuẩn hóa các tên bảng/cột có một ánh xạ rõ ràng: `users`, `email_verification_tokens`, `outbox_events`, `consumed_at`, `rotated_to_id` và mục đích `CHANGE_EMAIL`. | `03`, `04` |
| Điều hướng và bề mặt màn hình | Sơ đồ trang bổ sung `/reset-password`, `/account/mfa`, `/learn/assessments/:assessmentId/attempts` và `/billing/return/:provider`. `API-IAM-025` chỉ gắn với `SCR-WRK-017`; `API-STU-049` chỉ gắn với màn vận hành. | `05` |

## 4. Tồn đọng cần quyết định

### 4.1. Dịch vụ Danh tính và quyền truy cập

| Mức ảnh hưởng | Tồn đọng | Vì sao chưa tự sửa | Quyết định cần có |
|---|---|---|---|
| Cao | API phụ thuộc `authVersion`, trong khi mô hình `users` chưa mô tả cột hoặc nguồn dữ liệu tương ứng. | Cần quyết định nơi lưu, cách tăng phiên bản và chính sách lan truyền thu hồi phiên. | Bổ sung mô hình dữ liệu hoặc đổi hợp đồng xác thực. |
| Trung bình | Luồng ghi danh MFA có thời hạn nhưng `mfa_methods` chưa mô tả trạng thái ghi danh chờ xác nhận. | Có thể là trạng thái riêng, bản ghi tạm hoặc cách tính từ thời gian; các lựa chọn cho hành vi khác nhau. | Chọn mô hình ghi danh MFA và thời hạn. |
| Thấp | Một số tên nội bộ cũ của Dịch vụ Danh tính khác tên bảng và cột hiện hành. | Các tên có thể là bí danh kỹ thuật; chỉ những ánh xạ một nghĩa đã được chuẩn hóa. | Xác nhận danh mục tên nội bộ trước khi sinh mã hoặc tạo tệp chuyển đổi cơ sở dữ liệu. |

### 4.2. Dịch vụ Học tập và hồ sơ người học

| Mức ảnh hưởng | Tồn đọng | Vì sao chưa tự sửa | Quyết định cần có |
|---|---|---|---|
| Cao | Thiết lập ban đầu cho phép lưu nháp, trạng thái và bộ câu hỏi cấu hình, nhưng mô hình chỉ có `onboarding_submissions` bất biến. | Cần chọn lưu nháp riêng, mở rộng bản ghi hiện có hoặc bỏ khả năng lưu nháp. | Chốt phạm vi thiết lập ban đầu V1 và mô hình lưu dữ liệu. |
| Trung bình | API cập nhật kỹ năng người học và lịch sử học tập chưa có nguồn dữ liệu tương ứng rõ ràng. | Không thể suy ra bảng liên kết, lịch sử hay chính sách lưu giữ mà không thêm thiết kế. | Chốt mô hình kỹ năng và lịch sử học tập. |
| Trung bình | API minh chứng có tệp đính kèm, nhưng `evidence_records` chưa thể hiện liên kết tệp. | Cần quyết định tệp là một phần của minh chứng hay chỉ là tài nguyên xuất tạm thời. | Chốt quan hệ giữa minh chứng và `file_objects`. |

### 4.3. Dịch vụ Việc làm, Trường đại học và màn vận hành

| Mức ảnh hưởng | Tồn đọng | Vì sao chưa tự sửa | Quyết định cần có |
|---|---|---|---|
| Cao | Sự đồng ý cho phép tìm kiếm ứng viên cần phiên bản chính sách, thời hạn và các trường được hiển thị, nhưng chưa có mô hình lịch sử phù hợp. | Không thể dùng `data_consent_grants` của trường đại học/doanh nghiệp mà không đổi ý nghĩa dữ liệu. | Thiết kế bản ghi sự đồng ý riêng cho tìm kiếm ứng viên. |
| Cao | Mã định danh URL `slug` của việc làm chỉ được bảo đảm duy nhất trong không gian dữ liệu, trong khi tuyến công khai dùng `/jobs/:slug`. | Cần chọn `slug` toàn cục, định danh công khai khác, hoặc mở rộng tuyến bằng ngữ cảnh không gian dữ liệu. | Chốt cách định danh việc làm công khai. |
| Trung bình | Một số màn vận hành cần xem danh sách, chi tiết hoặc từ chối, nhưng API chỉ có thao tác ghi hoặc thiếu hợp đồng đối ứng. | Thêm API mới là mở rộng phạm vi ngoài đợt chuẩn hóa. | Bổ sung hợp đồng đọc/duyệt cho xác minh, hỗ trợ, hoàn tiền, AI và quyền truy cập khẩn cấp. |
| Trung bình | Lời mời liên kết trường, phản hồi đề nghị tuyển dụng của ứng viên và dữ liệu báo cáo trường đại học chưa có mô hình/API đầy đủ. | Đây là luồng nghiệp vụ mới hoặc còn thiếu thực thể nguồn. | Chốt phạm vi trường đại học V1 và các thực thể còn thiếu. |

### 4.4. Thanh toán, khuyến mại và AI

| Mức ảnh hưởng | Tồn đọng | Vì sao chưa tự sửa | Quyết định cần có |
|---|---|---|---|
| Cao | Cơ chế giữ chỗ và hoàn quyền lợi xuất hiện trong luồng xuất CV/AI, nhưng chưa có mô hình rõ ràng. | Không thể xác định thời điểm trừ, hoàn và chống chi tiêu trùng chỉ bằng văn xuôi hiện có. | Thiết kế cơ chế giữ chỗ và bút toán sổ cái tương ứng. |
| Trung bình | Tài liệu thanh toán nhắc `PAYMENT_SETTLED` nhưng kiểu liệt kê sổ cái hiện hành không có giá trị này. | Có thể là loại sự kiện, loại bút toán hoặc mô tả; ba cách có ý nghĩa khác nhau. | Chốt từ vựng sổ cái và kiểu liệt kê chính thức. |
| Trung bình | Dữ liệu lượt hiển thị/lượt nhấp được mô tả theo sự kiện, nhưng mô hình chỉ có bộ đếm thay đổi trực tiếp. | Cần quyết định có lưu sự kiện gốc hay chỉ giữ bộ đếm tổng hợp. | Chốt yêu cầu kiểm toán và mô hình đo lường quảng bá. |
| Trung bình | API AI yêu cầu tập dữ liệu, lần chạy đánh giá, kết quả đánh giá và phạm vi công tắc vô hiệu hóa chi tiết hơn mô hình dữ liệu. | Cần thêm thực thể hoặc thu hẹp hợp đồng AI. | Chốt mô hình đánh giá AI và phạm vi công tắc vô hiệu hóa. |

## 5. Điều kiện hoàn tất của đợt chuẩn hóa

- Phần văn xuôi, nhãn bảng, tiêu đề và nhãn người đọc trong Mermaid dùng tiếng Việt; định danh máy đọc được và chuẩn kỹ thuật được giữ nguyên.
- Không còn khác biệt trạng thái đã nêu tại mục 3.
- Mọi tham chiếu `UC`, `API`, `SCR`, `TBL`, `BR`, `EVT` và `ERR` trong bộ tài liệu đều có đích hợp lệ.
- Các khoảng trống tại mục 4 vẫn được giữ rõ ràng, không bị diễn đạt như thể chức năng đã có hợp đồng triển khai hoàn chỉnh.
- Không có thay đổi mã nguồn, tệp chuyển đổi cơ sở dữ liệu hoặc hợp đồng công khai ngoài việc sửa mô tả tài liệu đã có nguồn chuẩn rõ ràng.
