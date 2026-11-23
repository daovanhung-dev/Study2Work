# QUY TRÌNH CHÍNH THỨC — TẠO UTC SCREEN TỪ DD (12 BƯỚC)

**Mục đích:** cho phép bất kỳ người kiểm thử hoặc AI Agent nào có cùng DD tạo lại bộ UTC có kết quả tương đương về phạm vi, mã, nguồn và trạng thái. Đây là quy trình **thiết kế và lập hồ sơ**, không thực hiện ứng dụng/test runtime.

## Bước 1 — Tiếp nhận và bảo toàn DD

- Nhận DD dạng `.tar.gz`, `.zip`, folder hoặc file. Chạy `python scripts/chuan_bi_dd.py --input <archive> --output <workspace>/dd`.
- Ghi tên, phiên bản, ngày, nguồn; giữ nguyên ảnh, file gốc. Khi nguồn có HTML chỉ đọc mã như bằng chứng thiết kế/prototype, **không chạy script trong HTML**.
- Đọc toàn bộ các file (ví dụ GS-01: `00-overview.md`, `01-ui-elements.md`, `02-events.md`, `03-data-flow.md`, `04-api-integration.md`, `05-business-rules.md`, `06-navigation.md`, `07-test-cases.md`), không chỉ đọc overview.
- Xem ảnh `screen-clean.png` và `screen-numbered.png` nếu có; nhận diện từng marker trước khi lập ca.

**Hoàn thành khi:** có danh mục nguồn với SHA256, danh sách file đã đọc, không có file bắt buộc bị bỏ sót.

## Bước 2 — Phân biệt nguồn xác nhận và phần chưa được duyệt

Tách bốn lớp: (i) thiết kế/AC được duyệt; (ii) DD dự thảo; (iii) quan sát mã nguồn thực tế; (iv) trạng thái runtime đã chạy. **Không suy từ (iii) thành (iv)**. Một ảnh chỉ chứng minh bố cục trong ảnh, không chứng minh event hoặc responsive.

Với DD GS-01, mục “Current Study Web source re-audit (2026-11-21)” ghi nhận route/caller hiện có và ghi đè nhận định cũ “UNWIRED” ở phạm vi source; nhưng chính addendum vẫn nói runtime/browser chưa xác minh và loaded-state design chưa được duyệt. Khi gặp mâu thuẫn tương tự, ghi chú rõ từng phạm vi, không tự kết luận DD READY.

**Hoàn thành khi:** có `metadata.dd_status`, `runtime_status`, danh mục blocker và quyết định cần bổ sung.

## Bước 3 — Trích yêu cầu để truy vết

- Tạo một mã nội bộ cho mỗi yêu cầu kiểm chứng được, vd `GS-01-YC-001`; nếu DD có mã gốc thì giữ thêm mã đó trong nguồn/ghi chú.
- Mỗi yêu cầu phải có nội dung, phân nhóm, nguồn file + mục, trạng thái DD, mức ưu tiên.
- Không gom nhiều mục đích độc lập thành một yêu cầu quá rộng, khiến coverage không đo được.
- Tách “đã có source code” với “đã có giao diện duyệt” nếu hai căn cứ khác nhau.

**Hoàn thành khi:** không có yêu cầu thiếu nguồn hoặc trùng mã.

## Bước 4 — Lập luồng màn hình và bảng API

Ghi actor, route, input, output, tiền/hậu điều kiện, danh sách state, chuỗi gọi API và bảng:

| Trường | Nội dung phải lấy từ DD |
|---|---|
| Mã API | Mã catalog / alias có truy vết |
| Phương thức, đường dẫn | GET/POST/PATCH/DELETE, endpoint xác định |
| Request | path/query/body, mặc định, validation, quyền |
| Response | HTTP, business code, envelope, trường dữ liệu |
| Nhánh lỗi | timeout, 4xx/5xx, lỗi hợp đồng, mapping hiển thị nếu đã chốt |
| Gắn sự kiện | Event gây gọi API, điều kiện/thứ tự |
| Nguồn | File DD, mục/ID tương ứng |

**Hoàn thành khi:** mỗi API được nhắc trong testcase tồn tại trong danh mục API; không có API suy đoán.

## Bước 5 — Liệt kê thành phần

- Đọc marker và đặc tả: mã, tên/nhãn, loại, vị trí, text, nguồn dữ liệu, default, trạng thái có điều kiện, event, trường hợp không xuất hiện trên ảnh.
- Một marker có thể chứa icon và input trong cùng vùng: nếu DD phân biệt hành vi hãy chia thành mục kiểm tra tương ứng nhưng giữ liên kết marker.
- Nếu DD nói cần thẻ sản phẩm, sort hoặc pagination nhưng ảnh không có, ghi yêu cầu thiết kế chờ duyệt **không tạo marker giả**.

**Hoàn thành khi:** toàn bộ marker có element ID duy nhất; mỗi element có nguồn.

## Bước 6 — Liệt kê sự kiện

Mỗi event cần: trigger, element nguồn, tiền điều kiện, dữ liệu vào, hành vi/API, thành công, lỗi, điều hướng, trạng thái. Bao gồm event hệ thống (onLoad, async response) dù không có element kích hoạt. Sự kiện “click 4 liên kết chân trang” là một event tổng nhưng tối thiểu 4 testcase đích khác nhau nếu được quy định.

**Hoàn thành khi:** toàn bộ event DD được ánh xạ và tất cả mã element/API trỏ đúng danh mục.

## Bước 7 — Sinh ca ĐẶC TÍNH CHUNG TOÀN MÀN HÌNH

Bảng ca ở `02. Tổng quan` bao gồm entry/permission, thứ tự API, trạng thái loading/empty/ready/error, dữ liệu đồng bộ, route, side effect, trường hợp 0/n/biên, stale request, lỗi/khôi phục, bảo mật, usability và accessibility nếu yêu cầu có căn cứ.

Ví dụ GS-01: `items=[] & total=0` là catalog trống; `items=[] & total>0` là trang ngoài phạm vi. Hai điều kiện **không được gộp**.

**Hoàn thành khi:** mỗi trạng thái/luồng trong DD có ít nhất một ca tương ứng hoặc lý do chưa kiểm thử được.

## Bước 8 — Sinh ca TỪNG THÀNH PHẦN

Với **mỗi element**: một ca nhận diện hiển thị/cấu trúc; thêm ca nhãn/giá trị, trạng thái enable/disable, valid/invalid, giới hạn dữ liệu, placeholder, lỗi/nhãn, hover/focus, bàn phím, tương phản, responsive nếu DD có tiêu chí. Kết quả mong đợi không được chỉ ghi “đúng DD”.

**Hoàn thành khi:** đối chiếu `element ID → ≥1 TC`, không có element bị quên.

## Bước 9 — Sinh ca TỪNG SỰ KIỆN

Với **mỗi event**: ca luồng chuẩn, kết quả độc lập của từng nhánh, lỗi API, dữ liệu biên, thao tác lặp, bất đồng bộ, phân quyền, chuyển màn, xử lý response. Dùng phân hoạch tương đương/giá trị biên/bảng quyết định/chuyển trạng thái khi hợp lý và có dữ kiện.

**Hoàn thành khi:** đối chiếu `event ID → ≥1 TC`; các trường hợp 400/401/403/500 nếu khác hành vi phải thành ca riêng, không nhét một ca chung.

## Bước 10 — Viết testcase có thể lặp lại

Mỗi TC phải ghi:

1. Mã ca và loại (MH/TP/SK), mã yêu cầu và đối tượng.
2. Điều kiện tiên quyết tái tạo được (trạng thái, account giả lập, fixture, quyền, network).
3. Dữ liệu đầu vào cụ thể hoặc chính sách fixture (nếu chưa được duyệt thì ghi rõ).
4. Bước thực hiện có thứ tự, động từ hành động và điểm quan sát.
5. Kết quả mong đợi kiểm chứng được ở UI/URL/API/state, tách biệt kết quả thật.
6. Mã API (nếu có), file DD/mục nguồn, mức ưu tiên, trạng thái DD.
7. Trạng thái thực thi luôn “Chưa chạy” khi mới sinh; không phát sinh người chạy/ngày chạy/bằng chứng giả.

**Hoàn thành khi:** không có “đúng thiết kế/theo yêu cầu” chung chung thay cho expected result.

## Bước 11 — Kiểm tra ma trận coverage và blocker

Chạy:

```bash
python scripts/kiem_tra_utc.py --input workspace/utc-spec.json --report workspace/kiem-tra-utc.json
```

Báo cáo cần phân biệt `hợp lệ về cấu trúc` và `đủ điều kiện phê duyệt`; ví dụ mẫu GS-01 đúng toàn bộ mã và 23/23 yêu cầu có ca nhưng **không đủ điều kiện phê duyệt** vì DD BLOCKED.

## Bước 12 — Xuất Excel, kiểm tra và bàn giao

```bash
python scripts/tao_utc.py --input workspace/utc-spec.json --output workspace/UTC_<SCREEN>.xlsx
python scripts/kiem_tra_excel.py --input workspace/UTC_<SCREEN>.xlsx
```

Mở Excel, kiểm tra 4 sheet, số ca ở Bìa, ma trận yêu cầu, trạng thái “Chưa chạy”, danh sách lỗi và nguồn DD. Người review xác nhận nhánh kiểm thử còn thiếu, bản DD được chốt, mới chuyển từng ca “Chờ xác nhận” thành “Đã xác nhận”. Không sửa cột phụ trợ V:W; cập nhật JSON và sinh lại.

## Điều kiện nghiệm thu hồ sơ

| Loại | Chấp nhận khi |
|---|---|
| Đầu vào | DD có nguồn, phiên bản, dấu vết mâu thuẫn |
| Cấu trúc | 4 sheet; trường UTC đầy đủ, đúng tiếng Việt |
| Tính toàn diện | 100% yêu cầu có ca; 100% element/event có ca **hoặc được ghi ngoại lệ lý do** |
| Testcase | Bước và expected cụ thể; có link DD; không trùng mã |
| Tình trạng | Chờ xác nhận không bị giả là đã duyệt hoặc đã test |
| Excel | Có công thức, dropdown, không lỗi tham chiếu, báo cáo đã kiểm tra |
| Phê duyệt | Có người review/approve và DD không còn blocker áp dụng |
