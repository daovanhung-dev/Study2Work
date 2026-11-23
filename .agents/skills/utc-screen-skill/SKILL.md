---
name: utc-screen
version: 1.0.0
description: Đọc DD Screen (thư mục Markdown, ZIP, TAR.GZ hoặc tài liệu tương đương), thiết kế ca kiểm thử toàn màn hình, từng thành phần và từng sự kiện; sinh UTC Excel tiếng Việt 4 trang tính, truy vết yêu cầu và kiểm tra chất lượng trước phát hành.
---

# Skill: Sinh UTC Screen từ DD

## Khi kích hoạt

Kích hoạt khi người dùng yêu cầu: "tạo UTC Screen", "sinh testcase từ DD màn hình", "kiểm thử UI/UX và sự kiện", "xuất UTC Excel", "đối chiếu coverage DD → testcase".

## Hợp đồng đầu vào/đầu ra

- **Đầu vào bắt buộc:** DD Screen thật (file/thư mục/archive), và hình màn hình nếu DD có ảnh minh họa.
- **Đầu ra:** `utc-spec.json` chứa dữ kiện, nguồn truy vết, trạng thái xác nhận; `UTC_<Mã>_<Tên>.xlsx` với **4 trang tính** `01. Bìa`, `02. Tổng quan`, `03. Thành phần`, `04. Sự kiện`; kết quả `kiem-tra-utc.json` cùng danh sách blocker.
- **Ba lớp testcase bắt buộc:** (1) **đặc tính chung** của toàn màn hình; (2) **đặc tính mỗi thành phần**; (3) **mọi sự kiện** đã được mô tả trong DD. Không được bỏ lớp nào.
- **Ngôn ngữ:** nội dung trình bày 100% tiếng Việt; được giữ nguyên mã kỹ thuật, API, HTTP, URL, route và tên field trong contract.
- **Tình trạng thiết kế/thi công:** trường hợp chưa đủ căn cứ ghi **Chờ xác nhận DD**, không bịa Expected Result; tuyệt đối không gắn **Đạt** khi chưa thực thi.

## Quy trình thực hiện — bắt buộc theo thứ tự

**1. Đọc nguồn DD.** Kiểm kê file, mở ảnh sạch và ảnh đánh số, đọc tổng quan, thành phần, sự kiện, luồng dữ liệu, API, nghiệp vụ, điều hướng, kế hoạch kiểm thử. Với archive chạy `scripts/chuan_bi_dd.py` để giải nén an toàn, không thực thi HTML/script trong DD.

**2. Lập bảng nguồn.** Xác định phiên bản, ngày sửa, người duyệt, trạng thái DD, mức độ đáng tin và các chỗ mâu thuẫn giữa ảnh/prototype/contract/source audit. Không lấy prototype làm bằng chứng runtime. Khi có ghi chú rà soát source mới hơn, ghi rõ phần được thay thế và phần còn chưa được duyệt.

**3. Trích yêu cầu.** Mỗi yêu cầu một mã duy nhất, có mô tả kiểm chứng được, nguồn file+mục, độ ưu tiên và trạng thái đã xác nhận/chờ xác nhận. Nếu nguồn không cung cấp mã yêu cầu, được tạo mã nội bộ `SCREEN-YC-001` nhưng phải nói đó là mã quy ước phục vụ truy vết.

**4. Trích API và luồng.** Không thêm API nằm ngoài DD. Ghi phương thức, URL/path, request, response, điều kiện gọi, trạng thái, lỗi, side-effect, quyền, cache, loading, retry. Đánh dấu tất cả trường chưa có contract.

**5. Lập danh mục thành phần.** Duyệt từng marker ID và mọi thành phần được mô tả không có marker; phân biệt **hiện trên ảnh** và **chỉ nằm trong requirement tương lai**. Không gán marker giả cho control chưa xuất hiện. Ghi thuộc tính, trạng thái, nhãn, visibility, nguồn dữ liệu và sự kiện tác động.

**6. Lập danh mục sự kiện.** Mỗi sự kiện có mã, phần tử kích hoạt, đầu vào, tiền điều kiện, xử lý, API, đầu ra, điều hướng, xử lý lỗi, trạng thái DD. Với một event chứa 4 link, tạo ít nhất 4 ca riêng nếu đích khác nhau.

**7. Thiết kế ca toàn màn hình.** Bao phủ entry/exit, khởi tạo, loading/empty/ready/error, response API, bất đồng bộ, dữ liệu rỗng/biên, bảo mật/phân quyền, điều hướng chung, khả năng tiếp cận/responsive **nếu có tiêu chí nguồn**. Với tiêu chí ngoài DD chỉ tạo ca *đề xuất – chờ duyệt*.

**8. Thiết kế ca theo thành phần.** Mỗi element phải có ít nhất 1 ca; thêm ca cho nhãn, hiển thị, trạng thái, giá trị biên, dữ liệu từ API, tương tác bàn phím, định dạng, lỗi khi có cơ sở. Các trường hợp khác nhau cần kết quả độc lập thì phải tách ca.

**9. Thiết kế ca theo sự kiện.** Mỗi event phải có ít nhất 1 ca; bao phủ trigger, nhánh logic, thứ tự API, payload, phản hồi thành công/lỗi, thao tác lặp, điều hướng, race condition, rollback/retry theo DD. **Không mặc định** một event luôn có cả click/Enter/hover nếu thiết kế chưa quy định.

**10. Viết UTC chuẩn hóa.** Mỗi ca bắt buộc có: mã ca, mã yêu cầu, đối tượng, nhóm, mục tiêu, điều kiện tiên quyết, dữ liệu kiểm thử, bước thực hiện tuần tự, kết quả mong đợi quan sát/đo được, API liên quan, nguồn DD, mức ưu tiên, trạng thái DD. Giữ trống toàn bộ **kết quả thực tế/bằng chứng/ID lỗi/người-ngày chạy** trước thực thi.

**11. Kiểm tra độ bao phủ.** Chạy `scripts/kiem_tra_utc.py`: không được có ID trùng, tham chiếu sai, testcase thiếu dữ kiện, element/event không có ca, yêu cầu không có ca. Không lấy “23/23 yêu cầu có testcase” làm chứng cứ mọi nhánh đã được duyệt hoặc đã chạy.

**12. Sinh Excel và kiểm tra.** Chạy `scripts/tao_utc.py`; sau đó `scripts/kiem_tra_excel.py`, mở kiểm tra bảng Bìa/Tổng quan/Thành phần/Sự kiện. Chỉ tuyên bố **sẵn sàng thực thi** nếu không còn blocker, DD được xác nhận, người review đã phê duyệt; nếu không, ghi **BẢN KẾ HOẠCH UTC – CHỜ XÁC NHẬN**.

## Các lệnh chuẩn

```bash
# 1. Giải nén DD
python scripts/chuan_bi_dd.py --input /duong_dan/GS-01-DanhSachKhoaHoc.tar.gz --output workspace/gs01/dd

# 2. Agent đọc DD và tạo workspace/gs01/utc-spec.json theo schema/utc-spec.schema.json
#    Đây là bước phân tích ngữ nghĩa do AI/người kiểm thử thực hiện, KHÔNG phải trích xuất tự động bởi script.

# 3. Kiểm tra đặc tả
python scripts/kiem_tra_utc.py --input workspace/gs01/utc-spec.json --report workspace/gs01/kiem-tra-utc.json

# 4. Sinh UTC Excel
python scripts/tao_utc.py --input workspace/gs01/utc-spec.json --output workspace/gs01/UTC_GS01.xlsx

# 5. Kiểm tra cấu trúc file Excel
python scripts/kiem_tra_excel.py --input workspace/gs01/UTC_GS01.xlsx

# Tạo một workbook trống cho màn hình mới
python scripts/tao_utc.py --mau --output workspace/Mau_UTC_Screen.xlsx
```

## Điều kiện dừng và yêu cầu báo cáo

- Nếu DD thiếu/không đọc được: nêu file hoặc mục thiếu; **không tự giả định** source.
- Nếu DD `BLOCKED`: vẫn tạo kế hoạch ca kiểm thử có nguồn, phân biệt `Đã xác nhận` và `Chờ xác nhận` từng ca; không công bố đạt nghiệm thu.
- Nếu ảnh và code hoặc ghi chú cũ/mới mâu thuẫn: ghi blocker, đánh dấu ca liên quan, ưu tiên văn bản được phê duyệt; các quan sát source code phải được nhãn **chưa xác minh runtime** khi chưa chạy.
- Nếu script phát hiện lỗi: sửa đặc tả và sinh lại, không “lờ” lỗi kiểm tra.
- Không dùng kết quả của `07-test-cases.md` như bằng chứng test thực thi nếu DD nói rõ đó chỉ là planning references.
- Nếu dữ liệu nhạy cảm xuất hiện: dùng dữ liệu giả lập phù hợp, không đưa token/tài khoản thật vào UTC.

## Tệp cần đọc khi triển khai

1. `huong-dan/01_Quy_trinh_12_buoc.md` — checklist chi tiết và điều kiện nghiệm thu.
2. `huong-dan/02_Quy_tac_sinh_ca.md` — viewpoint và kỹ thuật thiết kế testcase.
3. `huong-dan/03_Anh_xa_Excel_JSON.md` — quy ước field, hàng, cột, giới hạn bảng.
4. `tham-chieu/Nguon_quoc_te.md` — phạm vi áp dụng chuẩn quốc tế, không nhận là chứng nhận.
5. `huong-dan/04_Mau_lenh_giao_viec_cho_AI.md` — lời nhắc tái sử dụng để giao nhiệm vụ cho Codex.
6. `vi-du/GS-01/utc-gs01.json` — mẫu đã truy vết từ DD GS-01, **chưa được phê duyệt**.
