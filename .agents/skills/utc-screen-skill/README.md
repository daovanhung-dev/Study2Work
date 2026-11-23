# UTC Screen Skill — Bộ sinh ca kiểm thử màn hình từ tài liệu DD

**Phiên bản:** 1.0.0 · **Ngôn ngữ:** Tiếng Việt · **Đầu ra:** Excel `.xlsx`

## Mục đích

Bộ skill giúp AI Agent/Codex đọc **DD Screen**, phân tích **toàn màn hình → từng thành phần → từng sự kiện**, lập đặc tả testcase có nguồn truy vết rồi xuất ra Excel đúng biểu mẫu. Bao gồm cơ chế kiểm soát thiếu dữ liệu, không tự suy diễn khi thiết kế chưa được phê duyệt.

## Cấu trúc

```text
utc-screen-skill/
├── SKILL.md                           # Hướng dẫn bắt buộc cho Agent
├── README.md                          # Hướng dẫn cài và sử dụng
├── mau/
│   └── Mau_UTC_Screen.xlsx            # Biểu mẫu Excel sạch, 4 trang tính
├── huong-dan/
│   ├── 01_Quy_trinh_12_buoc.md
│   ├── 02_Quy_tac_sinh_ca.md
│   ├── 03_Anh_xa_Excel_JSON.md
│   └── 04_Mau_lenh_giao_viec_cho_AI.md
├── tham-chieu/
│   └── Nguon_quoc_te.md
├── schema/
│   └── utc-spec.schema.json
├── scripts/
│   ├── chuan_bi_dd.py                 # Kiểm kê và giải nén DD an toàn
│   ├── kiem_tra_utc.py                # Kiểm chứng độ bao phủ và nguồn
│   ├── tao_utc.py                     # Sinh Excel từ JSON
│   └── kiem_tra_excel.py              # Kiểm tra đầu ra XLSX (chỉ đọc)
├── vi-du/GS-01/
│   ├── DD_goc/                        # DD được cung cấp, có ảnh minh họa
│   ├── utc-gs01.json                  # Đặc tả 73 ca có truy vết
│   └── UTC_GS-01_DanhSachKhoaHoc_KeHoach.xlsx
└── bao-cao/
    └── kiem-tra-gs01.json
```

## Cài đặt

Yêu cầu Python 3.10+ và **`artifact_tool` trong môi trường chạy** (động cơ tạo Excel). Công cụ kiểm tra JSON, đọc archive và kiểm tra Excel dùng thư viện chuẩn Python. Bộ mã nguồn không bao gồm binary/không tự cài package.

Với Codex: đặt nguyên thư mục `utc-screen-skill` vào `.agents/skills/` của dự án hoặc thư mục kỹ năng tương thích mà môi trường Agent của bạn đang hỗ trợ; yêu cầu Agent đọc `SKILL.md` trước khi xử lý DD.

## Tạo UTC cho màn hình mới

1. Cung cấp DD Screen ở dạng folder, ZIP hoặc TAR.GZ.
2. Giải nén an toàn bằng `scripts/chuan_bi_dd.py`.
3. Agent đọc toàn bộ tài liệu và ảnh; ghi ra `utc-spec.json` đúng `schema/utc-spec.schema.json` (không thể bỏ qua bước phân tích). Hướng dẫn từng bước tại `huong-dan/01_Quy_trinh_12_buoc.md`.
4. Kiểm tra dữ liệu và độ bao phủ bằng `scripts/kiem_tra_utc.py`.
5. Dùng `scripts/tao_utc.py` để xuất Excel.
6. Chạy `scripts/kiem_tra_excel.py`, người kiểm thử xem xét, phê duyệt khi DD đủ điều kiện.

Ví dụ chạy nhanh từ dữ liệu mẫu GS-01 (bắt đầu từ thư mục gốc của skill):

```bash
python scripts/kiem_tra_utc.py \
  --input vi-du/GS-01/utc-gs01.json \
  --report bao-cao/kiem-tra-gs01.json

python scripts/tao_utc.py \
  --input vi-du/GS-01/utc-gs01.json \
  --output vi-du/GS-01/UTC_GS-01_DanhSachKhoaHoc_KeHoach.xlsx

python scripts/kiem_tra_excel.py \
  --input vi-du/GS-01/UTC_GS-01_DanhSachKhoaHoc_KeHoach.xlsx
```

**Lưu ý GS-01:** 16 thành phần, 11 sự kiện, 2 API, 23 yêu cầu nội bộ suy ra có nguồn, 73 ca kiểm thử; **DD vẫn BLOCKED**, chưa được phép đánh dấu nghiệm thu và mọi ca vẫn **Chưa chạy**. Một số ca UI/API chỉ là kế hoạch chờ quyết định.

## Giới hạn và mở rộng

- Excel: `Tổng quan` cho 60 yêu cầu + 150 ca toàn màn hình + 17 API + 8 blocker; `Thành phần` 50 đối tượng/200 ca; `Sự kiện` 50 đối tượng/200 ca. Nếu vượt giới hạn, mở rộng hàm vùng trong `scripts/tao_utc.py` và kiểm tra lại công thức trước khi dùng.
- Có bảng truy vết phụ trợ ở `02. Tổng quan` cột V:W; **không sửa trực tiếp**. Hãy cập nhật JSON và sinh lại để tự đồng bộ.
- Script không tự hiểu tiếng Việt từ DD: việc trích xuất và thiết kế testcase là trách nhiệm của Agent/người kiểm thử, theo `SKILL.md`.
- Không đưa dữ liệu thật, mật khẩu, khóa truy cập vào ví dụ hoặc fixture.
- Không khẳng định tuân thủ toàn diện ISTQB, ISO, WCAG hoặc OWASP chỉ vì có bộ skill này.
