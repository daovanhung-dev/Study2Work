# Review Study2Work DD API Index

- DD nguồn: `docs/DD/Study2Work_DD_API_Index.xlsx`
- Phạm vi: index của 157 API DD
- Kết luận: **CẦN SỬA — index/QA không còn phản ánh repository hiện tại**

## Các điểm cần sửa

| ID | Mức độ | Vị trí index | Nhận xét | Cách sửa |
|---|---|---|---|---|
| IDX-01 | P0 | sheet `Nguồn BD`, `Tổng quan` | Index ghi đã đọc 44 file / 226.913 byte và không có schema. Hiện `docs/BD` có 48 file / 460.105 byte, gồm ba tài liệu `base/*` và `diagram/CLASS/study2work_study_full_schema_seed.sql` không có trong index. | Tái sinh source inventory từ filesystem, thêm path/size/hash; không giữ số đếm thủ công. |
| IDX-02 | P0 | sheet `QA & Giới hạn` | QA ghi “0 placeholder”, nhưng 154/157 API có placeholder `<...>`; `<FK condition>` xuất hiện 219 lần trong 81 API và `_value` xuất hiện trong 154 API. | Thêm quality gate regex và fail index build khi còn placeholder. |
| IDX-03 | P0 | sheet `API Coverage`, `Tổng quan` | 125/157 API có căn cứ `SUY DẪN`, cả 157 vẫn là `VERIFIED`, trong khi Review/Approve của 157 file đều “Chưa chỉ định”. | Tách `DRAFT → IN_REVIEW → APPROVED`; không dùng VERIFIED khi chưa có reviewer/approver và dependency còn PROPOSED. |
| IDX-04 | P0 | sheet `QA & Giới hạn` và toàn bộ coverage | Index không phát hiện mọi API dùng envelope cũ `{data,meta}` / `{error}`, trái convention thay thế tại `docs/BD/base/0. Study2Work_System_Architecture.md:632-700`. | Thêm check exact schema/casing và ưu tiên tài liệu `base/0` khi reconcile nguồn. |
| IDX-05 | P1 | sheet `API Coverage` | Cả 157 success example có `meta.page/page_size`, nhưng chỉ 24 API document request/response pagination; 133 API có pagination thừa. | Validate example field là subset của contract và `meta.pagination` chỉ có ở list. |
| IDX-06 | P0 | sheet `QA & Giới hạn` | DDL hiện có 24 table/0 view trong schema `study_dev0`, còn DD dùng `study.*`; DD tham chiếu 17 relation không tồn tại. Index vẫn tuyên bố mapping đã đủ để review. | Chốt namespace và kiểm relation/column tự động với DDL hoặc waiver/migration có ID. |
| IDX-07 | P0 | coverage mutation | Trong 73 mutation: 13 target relation không tồn tại, 59 có physical column không tồn tại, API-085 thiếu update mapping; không mutation nào qua strict DDL check. | Thêm gate bắt buộc target/column/WHERE/version/transaction khớp DDL trước APPROVED. |

## Điều kiện duyệt lại

- Inventory được sinh lại từ đúng 48 nguồn và có hash chống source drift.
- QA tự động kiểm envelope, example, placeholder, relation/column và approval state.
- Index chỉ tổng hợp trạng thái từ workbook sau khi từng biên bản review đã được xử lý.
