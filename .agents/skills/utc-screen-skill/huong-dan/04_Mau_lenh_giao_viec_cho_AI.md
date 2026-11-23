# MẪU LỆNH GIAO VIỆC CHO CODEX / AI AGENT

## Lệnh ngắn (có thể dùng ngay)

> Hãy kích hoạt skill `utc-screen` và đọc toàn bộ `SKILL.md`. Đầu vào là thư mục/gói DD Screen tôi cung cấp. Hãy tạo bộ UTC Screen Excel **4 trang tính tiếng Việt** (Bìa, Tổng quan, Thành phần, Sự kiện), có ca kiểm thử **toàn màn hình, cho từng element, và cho từng event**. Với mỗi ca ghi nguồn DD, dữ liệu, các bước và kỳ vọng cụ thể; không tự phát minh API/luồng nghiệp vụ. Chưa chạy ứng dụng thì để trạng thái “Chưa chạy”; DD chưa duyệt phải ghi “Chờ xác nhận”. Xuất `utc-spec.json`, `UTC_<screen>.xlsx`, báo cáo validator và danh sách blocker. Chạy kiểm tra cấu trúc trước khi bàn giao.

## Lệnh kiểm soát chất lượng cao

> Đọc `SKILL.md` và `huong-dan/01_Quy_trinh_12_buoc.md` của skill `utc-screen`. Kiểm kê tất cả file DD, mở ảnh được đánh số, đọc đặc tả luồng/API và ghi lại phần không nhất quán. Trích danh mục yêu cầu, element, event, API với mã và nguồn; sinh testcase từng lớp theo đúng DD. Đừng coi source code hoặc prototype là bằng chứng runtime. Ưu tiên: không thiếu element/event; không trùng ID; không để expected chung chung; không bỏ qua lỗi, rỗng, trạng thái có dữ liệu, navigation và bất đồng bộ nếu DD quy định. Dùng JSON schema làm dữ liệu trung gian. Sau khi viết JSON hãy chạy `kiem_tra_utc.py` rồi `tao_utc.py` và `kiem_tra_excel.py`. Nếu DD BLOCKED, vẫn xuất **bản kế hoạch UTC**, kèm blocker và ca chờ xác nhận, tuyệt đối không đánh dấu là sản phẩm đã nghiệm thu.

## Khi yêu cầu cập nhật một màn hình

> Mở bộ `utc-spec.json` cũ, đọc DD bản mới, lập báo cáo khác biệt về yêu cầu/element/event/API/expected, giữ ID testcase cũ khi nội dung chưa thay đổi; đánh dấu ca không còn áp dụng theo quy trình quản trị. Cập nhật đặc tả, chạy validator, sinh lại file Excel và giải thích những thay đổi ảnh hưởng coverage. Không sửa trực tiếp cột phụ trợ V:W trong Excel.
