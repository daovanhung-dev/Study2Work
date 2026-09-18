---
title: "Data Mapping"
order: 5
source_workbook: "【VQ2T-PARAM】API設計_I01_I01SaveRemovalPart_Ver1.0_VN 1.xlsx"
source_sheet: "3. Data mapping"
dd_id: "I01SaveRemovalPart"
format: markdown
---

# Data Mapping

## Metadata kế thừa

| Thuộc tính | Giá trị | Công thức Excel nguồn |
|---|---|---|
| Project | `VQ2T-PARAM` | `=Overview!E1` |
| System | `設定管理` | `=Overview!H1` |
| Người tạo | `FPT AnNVK1` | `='Lịch sử'!C4` |
| Ngày tạo | `2026-04-09` | Giá trị trực tiếp |

## Flow xử lý data

## 1. Get thông tin

### 1.1. Get thông tin sau từ session storage của browser

- Thông tin token.
- Giải mã token, get `user_id` từ thông tin token.

### 1.2. Get thông tin sau từ request data

- `seiskjy_id`: lấy từ `request['seiskjy_id']`.
- `sisnlin_id`: lấy từ `request['sisnlin_id']`.
- `bmn_id`: lấy từ `request['bmn_id']`.
- `parts_list_id`: lấy từ `request['parts_list_id']`.
- `parts_list_nm`: lấy từ `request['parts_list_nm']`.
- `file_nm`: lấy từ `request['file_nm']`.
- `hyjjn_no`: lấy từ `request['hyjjn_no']`.
- `list_pposn_cd`: lấy từ `request['list_pposn_cd']`.

## 2. Check quyền

### 2.1. Get list quyền hạn của user

- Call API: `/auth/claim` (`Claim`).

| No | Parameter gọi ra | Setting Value | Remarks |
|---:|---|---|---|
| 1 | `authorization` | Thông tin token get từ xử lý `1.1` | Truyền trên Header |

**Trường hợp HTTP Status của Claim API bằng `200`**

- Check `Claim.accesses`.
- Nếu có một trong các `function_id` bên dưới, đi tới xử lý `3`.

| Role | function_id | Role quyền |
|---:|---:|---|
| 11 | `10001` | Người tạo Bảng thành tích kiểm tra hoàn thành |
| 14 | `10004` | Userr thông thường |
| 15 | `10005` | User thường (Quyền thao tác xác định) |
| 16 | `10006` | User quản lý (Quản lý quyền) |
| 17 | `10007` | Người kiểm tra hoàn thành |
| 18 | `10008` | Người kiểm tra thông thường |
| 19 | `10009` | Người edit kiểm tra hoàn thành |

- Trường hợp khác:
  - Đi tới xử lý `8.2`.

**Trường hợp HTTP Status của Claim API khác `200`**

- Đi tới xử lý `8.2`.

### Danh sách role quyền của app

| No | Role | id (function_id) | Role quyền |
|---:|---:|---:|---|
| 1 | 11 | `10001` | Người tạo Bảng thành tích kiểm tra hoàn thành |
| 2 | 12 | `10002` | Người confirm Bảng thành tích kiểm tra hoàn thành |
| 3 | 13 | `10003` | Người approve Bảng thành tích kiểm tra hoàn thành |
| 4 | 14 | `10004` | User thông thường |
| 5 | 15 | `10005` | User thường (Quyền thao tác xác định) |
| 6 | 16 | `10006` | User quản lý (Quản lý quyền) |
| 7 | 17 | `10007` | Người kiểm tra hoàn thành |
| 8 | 18 | `10008` | Người kiểm tra thông thường |
| 9 | 19 | `10009` | Người edit kiểm tra hoàn thành |
| 10 | 20 | `10010` | Người approve edit kiểm tra hoàn thành |
| 11 | 21 | `10011` | Người setting re-inspection item kiểm tra hoàn thành |
| 12 | 22 | `10012` | Người phụ trách đối chiếu cấp phát đăng ký phát hành kiểm chứng hoàn thành |
| 13 | 23 | `10013` | Người confirm đối chiếu cấp phát đăng ký phát hành kiểm chứng hoàn thành |
| 14 | 24 | `10014` | Người refer hệ thống bảng thành tích kiểm tra hoàn thành |

## 3. Validate data input

### 3.1. Thực hiện validate thông tin input đã get ở xử lý 1.2

- Trường hợp phát sinh error khi validate:
  - Đi tới xử lý `8.2`.
- Trường hợp khác:
  - Đi tới xử lý `4`.

Chi tiết validation: [06_Error.md](./06_Error.md).

## 4. Check tồn tại プリセット名 trong table 取外部品マスタ

### 4.1. Get thông tin từ table 取外部品マスタ

| Target table | Column get | Chú thích | Remarks |
|---|---|---|---|
| `setting_removal_parts_v` | `parts_list_id` | 取外部品ID | |

**Điều kiện get data**

- `setting_removal_parts_v.skj_flg = '0'`.
- `setting_removal_parts_v.seiskjy_id = seiskjy_id` get từ xử lý `1.2`.
- `setting_removal_parts_v.sisnlin_id = sisnlin_id` get từ xử lý `1.2`.
- `setting_removal_parts_v.bmn_id = bmn_id` get từ xử lý `1.2`.
- `setting_removal_parts_v.parts_list_nm = parts_list_nm` get từ xử lý `1.2`.

### 4.2. Check kết quả xử lý 4.1

- Nếu số record lớn hơn `0`:
  - Đây là trường hợp tồn tại `プリセット名` giống nhau.
  - Đi tới xử lý `8.2`.
- Trường hợp khác:
  - Đi tới xử lý `5`.

## 5. Phán đoán xử lý

- Nếu `parts_list_id` get ở xử lý `1.2` khác `NULL/BLANK`:
  - Đi tới xử lý `6`.
- Trường hợp khác:
  - Đi tới xử lý `7`.

## 6. Trường hợp update data

### 6.1. Get thông tin part tháo ra trong table 取外部品マスタ

| Target table | Column get | Chú thích | Remarks |
|---|---|---|---|
| `setting_removal_parts_v` | `parts_list_id` | 取外部品ID | |
| `↑` | `sdiknr_no` | 世代管理番号 | |

**Điều kiện get data**

- `setting_removal_parts_v.parts_list_id = parts_list_id` get từ xử lý `1.2`.
- `setting_removal_parts_v.skj_flg = '0'`.

### 6.2. Check kết quả xử lý 6.1

- Nếu get được thông tin:
  - Đi tới xử lý `6.3`.
- Trường hợp khác:
  - Coi là xử lý lỗi.
  - Đi tới xử lý `8.2`.

### 6.3. Xóa vật lý table 部品マスタ

**Table đối tượng**

- `setting_removal_parts_sb`.

**Điều kiện xóa theo nguồn**

- `setting_removal_parts.parts_list_id = parts_list_id` get từ xử lý `1.2`.

> Target table là `setting_removal_parts_sb` nhưng điều kiện nguồn tham chiếu `setting_removal_parts.parts_list_id`. Xung đột được giữ nguyên và ghi trong report.

### 6.4. Update data vào table 取外部品マスタ

**Table đối tượng**

- `setting_removal_parts`.

**Điều kiện update**

- `setting_removal_parts.parts_list_id = parts_list_id` get từ xử lý `6.1`.
- `setting_removal_parts.sdiknr_no = sdiknr_no` get từ xử lý `6.1`.
- `setting_removal_parts.seiskjy_id = seiskjy_id` get từ xử lý `1.2`.
- `setting_removal_parts.sisnlin_id = sisnlin_id` get từ xử lý `1.2`.
- `setting_removal_parts.bmn_id = bmn_id` get từ xử lý `1.2`.
- `setting_removal_parts.skj_flg = '0'`.

**Items update**

- Refer [07_setting_removal_parts_update.md](./07_setting_removal_parts_update.md).

**Parameter**

| Param | Giá trị | Remarks |
|---|---|---|
| `file_nm` | `file_nm` get từ xử lý `1.2` | ファイル名 |
| `sishkshnprg_cd` | `user_id` get từ xử lý `1.1` | 更新者コード |
| `parts_list_nm` | `parts_list_nm` get từ xử lý `1.2` | プリセット名 |
| `hyjjn_no` | `hyjjn_no` get từ xử lý `1.2` | 表示順 |

### 6.5. Insert data vào table 部品マスタ

- Lặp từng phần tử `pposn_cd` trong `list_pposn_cd` get ở xử lý `1.2`.

**Table đối tượng**

- `setting_removal_parts_sb`.

**Items insert**

- Refer [10_setting_removal_parts_sb.md](./10_setting_removal_parts_sb.md).

**Parameter**

| Param | Giá trị | Remarks |
|---|---|---|
| `parts_list_id` | `parts_list_id` get từ xử lý `1.2` | 取外部品ID |
| `pposn_cd` | Giá trị phần tử `pposn_cd` trong `list_pposn_cd` | 部品部位コード |

### 6.6. Get thông tin thứ tự hiển thị trong table 取外部品マスタ

| Target table | Column get | Chú thích | Remarks |
|---|---|---|---|
| `setting_removal_parts_v` | `count(parts_list_id)` | 表示順 | |

**Điều kiện get data theo nguồn**

- `setting_removal_parts.seiskjy_id = seiskjy_id` get từ xử lý `1.2`.
- `setting_removal_parts.sisnlin_id = sisnlin_id` get từ xử lý `1.2`.
- `setting_removal_parts.bmn_id = bmn_id` get từ xử lý `1.2`.
- `setting_removal_parts.skj_flg = '0'`.
- `setting_removal_parts.parts_list_id <> parts_list_id` get từ xử lý `1.2`.
- `setting_removal_parts.hyjjn_no = hyjjn_no` get từ xử lý `1.2`.

> Query header dùng view `setting_removal_parts_v`, nhưng điều kiện nguồn dùng `setting_removal_parts`. Nội dung được giữ nguyên.

### 6.7. Check kết quả xử lý 6.6

- Nếu số record get được lớn hơn `0`:
  - Đây là trường hợp thay đổi thứ tự hiển thị thành một số đã tồn tại.
  - Đi tới xử lý `6.8`.
- Trường hợp khác:
  - Kết thúc xử lý.

### 6.8. Update lại thông tin thứ tự hiển thị

**Table đối tượng**

- `setting_removal_parts`.

**Điều kiện update**

- `setting_removal_parts.parts_list_id <> parts_list_id` get từ xử lý `1.2`.
- `setting_removal_parts.hyjjn_no >= hyjjn_no` get từ xử lý `1.2`.
- `setting_removal_parts.seiskjy_id = seiskjy_id` get từ xử lý `1.2`.
- `setting_removal_parts.sisnlin_id = sisnlin_id` get từ xử lý `1.2`.
- `setting_removal_parts.bmn_id = bmn_id` get từ xử lý `1.2`.
- `setting_removal_parts.skj_flg = '0'`.

**Items update**

- Refer [08_setting_removal_parts_upd_hyjjn.md](./08_setting_removal_parts_upd_hyjjn.md).

**Parameter**

| Param | Giá trị | Remarks |
|---|---|---|
| `sishkshnprg_cd` | `user_id` get từ xử lý `1.1` | 更新者コード |

## 7. Trường hợp insert data

### 7.1. Insert data vào table 取外部品マスタ

**Table đối tượng**

- `setting_removal_parts`.

**Items insert**

- Refer [09_setting_removal_parts_insert.md](./09_setting_removal_parts_insert.md).

**Parameter**

| Param | Giá trị | Remarks |
|---|---|---|
| `seiskjy_id` | `seiskjy_id` get từ xử lý `1.2` | 拠点ID |
| `sisnlin_id` | `sisnlin_id` get từ xử lý `1.2` | ラインID |
| `bmn_id` | `bmn_id` get từ xử lý `1.2` | 部門ID |
| `parts_list_nm` | `parts_list_nm` get từ xử lý `1.2` | プリセット名 |
| `file_nm` | `file_nm` get từ xử lý `1.2` | ファイル名 |
| `hyjjn_no` | `hyjjn_no` get từ xử lý `1.2` | 表示順 |
| `sksiprg_cd` | `user_id` get từ xử lý `1.1` | 作成者コード |
| `sishkshnprg_cd` | `user_id` get từ xử lý `1.1` | 更新者コード |

### 7.2. Insert table 部品マスタ

- Lặp từng phần tử `pposn_cd` trong `list_pposn_cd` get ở xử lý `1.2`.

**Table đối tượng**

- `setting_removal_parts_sb`.

**Items insert**

- Refer [10_setting_removal_parts_sb.md](./10_setting_removal_parts_sb.md).

**Parameter**

| Param | Giá trị | Remarks |
|---|---|---|
| `parts_list_id` | `parts_list_id` sinh ra sau xử lý `7.1` | 取外部品ID |
| `pposn_cd` | Giá trị phần tử `pposn_cd` trong `list_pposn_cd` | 部品部位コード |

## 8. Trả về thông tin response

### 8.1. Trường hợp thành công

- `HTTPStatus = 200`.
- `status = 1`.
- `response.parts_list_id`:
  - Update branch: lấy từ xử lý `6.1`.
  - Insert branch: lấy ID sinh ra ở xử lý `7.1`.
- Response tương ứng định nghĩa tại [04_Response.md](./04_Response.md).

### 8.2. Trường hợp validate lỗi

- `HTTPStatus = 400`.
- `status = 2`.
- `response`: thông tin lỗi theo [04_Response.md](./04_Response.md).

### 8.3. Trường hợp phát sinh lỗi hệ thống

- `HTTPStatus = 500`.
- `status = 2`.
- `response`: thông tin lỗi theo [04_Response.md](./04_Response.md).

> Chi tiết lỗi refer [06_Error.md](./06_Error.md).

> Nguồn không mô tả rõ `BEGIN TRANSACTION`, `COMMIT` hoặc `ROLLBACK` cho chuỗi delete/update/insert nhiều bước. Không tự bổ sung trong bản chuyển đổi.

---
## Phụ lục đối chiếu nguồn Excel
- Workbook nguồn: `【VQ2T-PARAM】API設計_I01_I01SaveRemovalPart_Ver1.0_VN 1.xlsx`
- Sheet nguồn: `3. Data mapping`
- Dimension: `A1:BB263`
- Trạng thái: `visible`
- Số ô có dữ liệu/công thức: `476`
- Số vùng merge: `46`

<details>
<summary>Danh sách vùng merge</summary>

- `F54:G54`
- `H54:I54`
- `A1:D1`
- `E1:G1`
- `H1:AL1`
- `A2:D2`
- `E2:G2`
- `H2:M2`
- `N2:S2`
- `T2:Y2`
- `F55:G55`
- `AX2:BA2`
- `AX1:BA1`
- `Z2:AE2`
- `AF2:AL2`
- `AM2:AO2`
- `AP2:AT2`
- `AM1:AO1`
- `AP1:AT1`
- `AU1:AW1`
- `AU2:AW2`
- `H55:I55`
- `F52:G52`
- `H52:I52`
- `F53:G53`
- `H53:I53`
- `F56:G56`
- `H56:I56`
- `F57:G57`
- `H57:I57`
- `F58:G58`
- `H58:I58`
- `F59:G59`
- `H59:I59`
- `F60:G60`
- `H60:I60`
- `F64:G64`
- `H64:I64`
- `F65:G65`
- `H65:I65`
- `F61:G61`
- `H61:I61`
- `F62:G62`
- `H62:I62`
- `F63:G63`
- `H63:I63`

</details>

<details>
<summary>Bản ghi từng ô có dữ liệu hoặc công thức</summary>

| Hàng | Ô | Giá trị nguồn | Công thức nguồn |
|---:|---|---|---|
| 1 | `A1` | Project |  |
| 1 | `E1` | VQ2T-PARAM | Overview!E1 |
| 1 | `H1` | 設定管理 | Overview!H1 |
| 1 | `AM1` | Người tạo |  |
| 1 | `AP1` | FPT AnNVK1 | 'Lịch sử'!C4 |
| 1 | `AU1` | Ngày tạo |  |
| 1 | `AX1` | 46121 |  |
| 2 | `A2` | Loại tài liệu |  |
| 2 | `E2` | DD |  |
| 2 | `H2` | API |  |
| 2 | `N2` | Data mapping |  |
| 2 | `AM2` | Người update |  |
| 2 | `AU2` | Ngày update |  |
| 5 | `B5` | Flow xử lý data |  |
| 7 | `D7` | 1.  |  |
| 7 | `E7` | Get thông tin |  |
| 8 | `E8` | 1.1. |  |
| 8 | `F8` | Get thông tin sau từ session storage của browser. |  |
| 9 | `F9` | ・ |  |
| 9 | `G9` | Thông tin token |  |
| 10 | `F10` | ・ |  |
| 10 | `G10` | Giải mã token, get thông tin user_id từ thông tin token |  |
| 12 | `E12` | 1.2. |  |
| 12 | `F12` | Get thông tin sau từ request data: |  |
| 13 | `F13` | ・ |  |
| 13 | `G13` | seiskjy_id    : lấy từ request['seiskjy_id'] |  |
| 14 | `F14` | ・ |  |
| 14 | `G14` | sisnlin_id    : lấy từ request['sisnlin_id'] |  |
| 15 | `F15` | ・ |  |
| 15 | `G15` | bmn_id        : lấy từ request['bmn_id'] |  |
| 16 | `F16` | ・ |  |
| 16 | `G16` | parts_list_id : lấy từ request['parts_list_id'] |  |
| 17 | `F17` | ・ |  |
| 17 | `G17` | parts_list_nm : lấy từ request['parts_list_nm'] |  |
| 18 | `F18` | ・ |  |
| 18 | `G18` | file_nm       : lấy từ request['file_nm'] |  |
| 19 | `F19` | ・ |  |
| 19 | `G19` | hyjjn_no      : lấy từ request['hyjjn_no'] |  |
| 20 | `F20` | ・ |  |
| 20 | `G20` | list_pposn_cd : lấy từ request['list_pposn_cd'] |  |
| 22 | `D22` | 2. |  |
| 22 | `E22` | Check quyền |  |
| 23 | `E23` | 2.1. |  |
| 23 | `F23` | Get list quyền hạn của user |  |
| 24 | `F24` | ・ |  |
| 24 | `G24` | Call API: /auth/claim (Claim) |  |
| 26 | `G26` | № |  |
| 26 | `H26` | Parameter gọi ra |  |
| 26 | `N26` | Setting Value |  |
| 26 | `Z26` | Remarks |  |
| 27 | `G27` | 1 |  |
| 27 | `H27` | authorization |  |
| 27 | `N27` | Thông tin token get từ xử lý 1.1 |  |
| 27 | `Z27` | Truyền trên Header |  |
| 29 | `G29` | ・ |  |
| 29 | `H29` | Trường hợp  giá trị HTTP Status trả về của API là"200"(成功時) |  |
| 30 | `H30` | ・ |  |
| 30 | `I30` | Trường hợp trong giá trị Claim.accesses trả về khi call API có function_id sau: |  |
| 32 | `I32` | Role |  |
| 32 | `N32` | function_id |  |
| 32 | `Z32` | Role quyền |  |
| 33 | `I33` | 11 |  |
| 33 | `N33` | 10001 |  |
| 33 | `Z33` | Người tạo Bảng thành tích kiểm tra hoàn thành |  |
| 34 | `I34` | 14 |  |
| 34 | `N34` | 10004 |  |
| 34 | `Z34` | Userr thông thường |  |
| 35 | `I35` | 15 |  |
| 35 | `N35` | 10005 |  |
| 35 | `Z35` | User thường (Quyền thao tác xác định) |  |
| 36 | `I36` | 16 |  |
| 36 | `N36` | 10006 |  |
| 36 | `Z36` | User quản lý (Quản lý quyền) |  |
| 37 | `I37` | 17 |  |
| 37 | `N37` | 10007 |  |
| 37 | `Z37` | Người kiểm tra hoàn thành |  |
| 38 | `I38` | 18 |  |
| 38 | `N38` | 10008 |  |
| 38 | `Z38` | Người kiểm tra thông thường |  |
| 39 | `I39` | 19 |  |
| 39 | `N39` | 10009 |  |
| 39 | `Z39` | Người edit kiểm tra hoàn thành |  |
| 41 | `I41` | ・ |  |
| 41 | `J41` | Đi tới xử lý 3. |  |
| 43 | `H43` | ・ |  |
| 43 | `I43` | Trường hợp khác |  |
| 44 | `I44` | ・ |  |
| 44 | `J44` | Đi tới xử lý 8.2 |  |
| 46 | `G46` | ・ |  |
| 46 | `H46` | Trường hợp giá trị HTTP Status trả về của API khác "200"(エラー発生時) |  |
| 47 | `H47` | ・ |  |
| 47 | `I47` | Đi tới xử lý 8.2 |  |
| 49 | `E49` | ※ |  |
| 49 | `F49` | Danh sách role quyền của app như mô tả trong table sau: |  |
| 51 | `F51` | No |  |
| 51 | `H51` | Role |  |
| 51 | `J51` | id（function_id） |  |
| 51 | `P51` | Role quyền |  |
| 52 | `F52` | 1 |  |
| 52 | `H52` | 11 |  |
| 52 | `J52` | 10001 |  |
| 52 | `P52` | Người tạo Bảng thành tích kiểm tra hoàn thành |  |
| 53 | `F53` | 2 |  |
| 53 | `H53` | 12 |  |
| 53 | `J53` | 10002 |  |
| 53 | `P53` | Người confirm Bảng thành tích kiểm tra hoàn thành |  |
| 54 | `F54` | 3 |  |
| 54 | `H54` | 13 |  |
| 54 | `J54` | 10003 |  |
| 54 | `P54` | Người approve Bảng thành tích kiểm tra hoàn thành |  |
| 55 | `F55` | 4 |  |
| 55 | `H55` | 14 |  |
| 55 | `J55` | 10004 |  |
| 55 | `P55` | User thông thường |  |
| 56 | `F56` | 5 |  |
| 56 | `H56` | 15 |  |
| 56 | `J56` | 10005 |  |
| 56 | `P56` | User thường (Quyền thao tác xác định) |  |
| 57 | `F57` | 6 |  |
| 57 | `H57` | 16 |  |
| 57 | `J57` | 10006 |  |
| 57 | `P57` | User quản lý (Quản lý quyền) |  |
| 58 | `F58` | 7 |  |
| 58 | `H58` | 17 |  |
| 58 | `J58` | 10007 |  |
| 58 | `P58` | Người kiểm tra hoàn thành |  |
| 59 | `F59` | 8 |  |
| 59 | `H59` | 18 |  |
| 59 | `J59` | 10008 |  |
| 59 | `P59` | Người kiểm tra thông thường |  |
| 60 | `F60` | 9 |  |
| 60 | `H60` | 19 |  |
| 60 | `J60` | 10009 |  |
| 60 | `P60` | Người edit kiểm tra hoàn thành |  |
| 61 | `F61` | 10 |  |
| 61 | `H61` | 20 |  |
| 61 | `J61` | 10010 |  |
| 61 | `P61` | Người approve edit kiểm tra hoàn thành |  |
| 62 | `F62` | 11 |  |
| 62 | `H62` | 21 |  |
| 62 | `J62` | 10011 |  |
| 62 | `P62` | Người setting re-inspection item kiểm tra hoàn thành |  |
| 63 | `F63` | 12 |  |
| 63 | `H63` | 22 |  |
| 63 | `J63` | 10012 |  |
| 63 | `P63` | Người phụ trách đối chiếu cấp phát đăng ký phát hành kiểm chứng hoàn thành |  |
| 64 | `F64` | 13 |  |
| 64 | `H64` | 23 |  |
| 64 | `J64` | 10013 |  |
| 64 | `P64` | Người confirm đối chiếu cấp phát đăng ký phát hành kiểm chứng hoàn thành |  |
| 65 | `F65` | 14 |  |
| 65 | `H65` | 24 |  |
| 65 | `J65` | 10014 |  |
| 65 | `P65` | Người refer hệ thống bảng thành tích kiểm tra hoàn thành |  |
| 67 | `D67` | 3. |  |
| 67 | `E67` | Validate data input |  |
| 68 | `E68` | 3.1. |  |
| 68 | `F68` | Thực hiện validate thông tin input đã get ở xử lý 1.2 |  |
| 69 | `F69` | ・ |  |
| 69 | `G69` | Trường hợp phát sinh error khi validate |  |
| 70 | `G70` | ・ |  |
| 70 | `H70` | Đi tới xử lý 8.2 |  |
| 72 | `F72` | ・ |  |
| 72 | `G72` | Trường hợp khác |  |
| 73 | `G73` | ・ |  |
| 73 | `H73` | Đi tới xử lý 4. |  |
| 75 | `D75` | 4.  |  |
| 75 | `E75` | Check việc tồn tại thông tin [プリセット名] trong  table 取外部品マスタ |  |
| 76 | `E76` | 4.1. |  |
| 76 | `F76` | Get thông tin từ table 取外部品マスタ |  |
| 78 | `F78` | Target table |  |
| 78 | `N78` | Column get |  |
| 78 | `Z78` | Chú thích |  |
| 78 | `AL78` | Remarks |  |
| 79 | `F79` | setting_removal_parts_v |  |
| 79 | `N79` | parts_list_id |  |
| 79 | `Z79` | 取外部品ID |  |
| 81 | `F81` | ・ |  |
| 81 | `G81` | Điều kiện get data |  |
| 82 | `G82` | ・ |  |
| 82 | `H82` | setting_removal_parts_v.skj_flg ='0' |  |
| 83 | `G83` | ・ |  |
| 83 | `H83` | setting_removal_parts_v.seiskjy_id =  seiskjy_id get từ xử lý 1.2 |  |
| 84 | `G84` | ・ |  |
| 84 | `H84` | setting_removal_parts_v.sisnlin_id =  sisnlin_id get từ xử lý 1.2 |  |
| 85 | `G85` | ・ |  |
| 85 | `H85` | setting_removal_parts_v.bmn_id =   bmn_id get từ xử lý 1.2 |  |
| 86 | `G86` | ・ |  |
| 86 | `H86` | setting_removal_parts_v.parts_list_nm =  parts_list_nm get từ xử lý 1.2 |  |
| 88 | `E88` | 4.2. |  |
| 88 | `F88` | Check kết quả của xử lý 4.1 |  |
| 89 | `F89` | ・ |  |
| 89 | `G89` | Trường hợp số lượng record get ở xử lý 4.1 lớn hơn 0(trường hợp trong table 取外部品マスタ có tồn tại  [プリセット名] giống nhau) |  |
| 90 | `G90` | ・ |  |
| 90 | `H90` | Đi tới xử lý 8.2 |  |
| 92 | `F92` | ・ |  |
| 92 | `G92` | Trường hợp khác |  |
| 93 | `G93` | ・ |  |
| 93 | `H93` | Đi tới xử lý 5. |  |
| 95 | `D95` | 5.  |  |
| 95 | `E95` | Phán đoán xử lý |  |
| 96 | `E96` | ・ |  |
| 96 | `F96` | Trường hợp thông tin parts_list_id đã get ở xử lý 1.2 khác NULL/BLANK |  |
| 97 | `F97` | ・ |  |
| 97 | `G97` | Đi tới xử lý 6. |  |
| 99 | `E99` | ・ |  |
| 99 | `F99` | Trường hợp khác |  |
| 100 | `F100` | ・ |  |
| 100 | `G100` | Đi tới xử lý 7. |  |
| 102 | `D102` | 6. |  |
| 102 | `E102` | Trường hợp update data |  |
| 103 | `E103` | 6.1. |  |
| 103 | `F103` | Get thông tin part tháo ra trong table 取外部品マスタ |  |
| 105 | `F105` | Target table |  |
| 105 | `N105` | Column get |  |
| 105 | `Z105` | Chú thích |  |
| 105 | `AL105` | Remarks |  |
| 106 | `F106` | setting_removal_parts_v |  |
| 106 | `N106` | parts_list_id |  |
| 106 | `Z106` | 取外部品ID |  |
| 107 | `F107` | ↑ |  |
| 107 | `N107` | sdiknr_no |  |
| 107 | `Z107` | 世代管理番号 |  |
| 109 | `F109` | ・ |  |
| 109 | `G109` | Điều kiện get data |  |
| 110 | `G110` | ・ |  |
| 110 | `H110` | setting_removal_parts_v.parts_list_id = parts_list_id get từ xử lý 1.2 |  |
| 111 | `G111` | ・ |  |
| 111 | `H111` | setting_removal_parts_v.skj_flg ='0' |  |
| 113 | `E113` | 6.2. |  |
| 113 | `F113` | Check kết quả của xử lý 6.1 |  |
| 114 | `F114` | ・ |  |
| 114 | `G114` | Trường hợp get được thông tin ở xử lý 6.1(trường hợp tồn tại thông tin [部品部位コード] trong  table 取外部品マスタ) |  |
| 115 | `G115` | ・ |  |
| 115 | `H115` | Đi tới xử lý 6.3 |  |
| 117 | `F117` | ・ |  |
| 117 | `G117` | Trường hợp khác |  |
| 118 | `G118` | ・ |  |
| 118 | `H118` | Coi là xử lý lỗi, thực hiện chuyển đến xử lý 8.2 |  |
| 120 | `E120` | 6.3. |  |
| 120 | `F120` | Thực hiện xóa thông tin (xóa vật lý) của table 部品マスタ (setting_removal_parts_sb) |  |
| 121 | `F121` | ・ |  |
| 121 | `G121` | Table đối tượng |  |
| 122 | `G122` | ・ |  |
| 122 | `H122` | setting_removal_parts_sb |  |
| 124 | `F124` | ・ |  |
| 124 | `G124` | Điều kiện xóa  |  |
| 125 | `G125` | ・ |  |
| 125 | `H125` | setting_removal_parts.parts_list_id = parts_list_id get từ xử lý 1.2 |  |
| 127 | `E127` | 6.4. |  |
| 127 | `F127` | Thực hiện update data vào table 取外部品マスタ |  |
| 128 | `F128` | ・ |  |
| 128 | `G128` | Table đối tượng |  |
| 129 | `G129` | ・ |  |
| 129 | `H129` | setting_removal_parts |  |
| 131 | `F131` | ・ |  |
| 131 | `G131` | Điều kiện update  |  |
| 132 | `G132` | ・ |  |
| 132 | `H132` | setting_removal_parts.parts_list_id = parts_list_id get từ xử lý 6.1 |  |
| 133 | `G133` | ・ |  |
| 133 | `H133` | setting_removal_parts.sdiknr_no = sdiknr_no từ xử lý 6.1 |  |
| 134 | `G134` | ・ |  |
| 134 | `H134` | setting_removal_parts.seiskjy_id = seiskjy_id get từ xử lý 1.2 |  |
| 135 | `G135` | ・ |  |
| 135 | `H135` | setting_removal_parts.sisnlin_id =  sisnlin_id get từ xử lý 1.2 |  |
| 136 | `G136` | ・ |  |
| 136 | `H136` | setting_removal_parts.bmn_id =  bmn_id get từ xử lý 1.2 |  |
| 137 | `G137` | ・ |  |
| 137 | `H137` | setting_removal_parts.skj_flg ='0' |  |
| 139 | `F139` | ・ |  |
| 139 | `G139` | Items update: |  |
| 140 | `G140` | ・ |  |
| 140 | `H140` | Refer sheet 「setting_removal_parts_update」 |  |
| 142 | `F142` | ・ |  |
| 142 | `G142` | Parameter: |  |
| 144 | `G144` | Param |  |
| 144 | `N144` | Giá trị |  |
| 144 | `AL144` | Remarks |  |
| 145 | `G145` | file_nm |  |
| 145 | `N145` | file_nm get từ xử lý 1.2 |  |
| 145 | `AL145` | ファイル名 |  |
| 146 | `G146` | sishkshnprg_cd |  |
| 146 | `N146` | user_id get từ xử lý 1.1 |  |
| 146 | `AL146` | 更新者コード |  |
| 147 | `G147` | parts_list_nm |  |
| 147 | `N147` | parts_list_nm get từ xử lý 1.2 |  |
| 147 | `AL147` | プリセット名 |  |
| 148 | `G148` | hyjjn_no |  |
| 148 | `N148` | hyjjn_no get ở xử lý 1.2 |  |
| 148 | `AL148` | 表示順 |  |
| 150 | `E150` | 6.5. |  |
| 150 | `F150` | Insert data vào table 部品マスタ |  |
| 151 | `F151` | ・ |  |
| 151 | `G151` | Thực hiện lặp lại các xử lý bên dưới với từng phần tử pposn_cd trong list_pposn_cd mà đã được get ở xử lý 1.2 |  |
| 152 | `G152` | ・ |  |
| 152 | `H152` | Table đối tượng |  |
| 153 | `H153` | ・ |  |
| 153 | `I153` | setting_removal_parts_sb |  |
| 155 | `G155` | ・ |  |
| 155 | `H155` | Items insert: |  |
| 156 | `H156` | ・ |  |
| 156 | `I156` | Refer sheet 「setting_removal_parts_sb」 |  |
| 158 | `G158` | ・ |  |
| 158 | `H158` | Parameter: |  |
| 160 | `H160` | Param |  |
| 160 | `N160` | Giá trị |  |
| 160 | `AL160` | Remarks |  |
| 161 | `H161` | parts_list_id |  |
| 161 | `N161` | parts_list_id get từ xử lý 1.2 |  |
| 161 | `AL161` | 取外部品ID |  |
| 162 | `H162` | pposn_cd |  |
| 162 | `N162` | Giá trị của phần tử pposn_cd trong list_pposn_cd |  |
| 162 | `AL162` | 部品部位コード |  |
| 164 | `E164` | 6.6. |  |
| 164 | `F164` | Get thông tin thứ tự hiển thị trong table 取外部品マスタ |  |
| 166 | `F166` | Target table |  |
| 166 | `N166` | Column get |  |
| 166 | `Z166` | Chú thích |  |
| 166 | `AL166` | Remarks |  |
| 167 | `F167` | setting_removal_parts_v |  |
| 167 | `N167` | count(parts_list_id) |  |
| 167 | `Z167` | 表示順 |  |
| 169 | `F169` | ・ |  |
| 169 | `G169` | Điều kiện get data |  |
| 170 | `G170` | ・ |  |
| 170 | `H170` | setting_removal_parts.seiskjy_id = seiskjy_id get từ xử lý 1.2 |  |
| 171 | `G171` | ・ |  |
| 171 | `H171` | setting_removal_parts.sisnlin_id =  sisnlin_id get từ xử lý 1.2 |  |
| 172 | `G172` | ・ |  |
| 172 | `H172` | setting_removal_parts.bmn_id =  bmn_id get từ xử lý 1.2 |  |
| 173 | `G173` | ・ |  |
| 173 | `H173` | setting_removal_parts.skj_flg ='0' |  |
| 174 | `G174` | ・ |  |
| 174 | `H174` | setting_removal_parts.parts_list_id <> parts_list_id get từ xử lý 1.2 |  |
| 175 | `G175` | ・ |  |
| 175 | `H175` | setting_removal_parts.hyjjn_no = hyjjn_no get từ xử lý 1.2 |  |
| 177 | `E177` | 6.7. |  |
| 177 | `F177` | Check kết quả của xử lý 6.6 |  |
| 178 | `F178` | ・ |  |
| 178 | `G178` | Trường hợp số record get được ở xử lý 6.6 > 0(Trường hợp thay đổi thứ tự hiển thị thành một số đã tồn tại) |  |
| 179 | `G179` | ・ |  |
| 179 | `H179` | Đi tới xử lý 6.8 |  |
| 181 | `F181` | ・ |  |
| 181 | `G181` | Trường hợp khác |  |
| 182 | `G182` | ・ |  |
| 182 | `H182` | Kết thúc xử lý |  |
| 184 | `E184` | 6.8. |  |
| 184 | `F184` | Update lại thông tin Thứ tự hiển thị trong table 取外部品マスタ |  |
| 185 | `F185` | ・ |  |
| 185 | `G185` | Table đối tượng |  |
| 186 | `G186` | ・ |  |
| 186 | `H186` | setting_removal_parts |  |
| 188 | `F188` | ・ |  |
| 188 | `G188` | Điều kiện update  |  |
| 189 | `G189` | ・ |  |
| 189 | `H189` | setting_removal_parts.parts_list_id <> parts_list_id get từ xử lý 1.2 |  |
| 190 | `G190` | ・ |  |
| 190 | `H190` | setting_removal_parts.hyjjn_no >= hyjjn_no get từ xử lý 1.2 |  |
| 191 | `G191` | ・ |  |
| 191 | `H191` | setting_removal_parts.seiskjy_id = seiskjy_id get từ xử lý 1.2 |  |
| 192 | `G192` | ・ |  |
| 192 | `H192` | setting_removal_parts.sisnlin_id =  sisnlin_id get từ xử lý 1.2 |  |
| 193 | `G193` | ・ |  |
| 193 | `H193` | setting_removal_parts.bmn_id =  bmn_id get từ xử lý 1.2 |  |
| 194 | `G194` | ・ |  |
| 194 | `H194` | setting_removal_parts.skj_flg ='0' |  |
| 196 | `F196` | ・ |  |
| 196 | `G196` | Items update: |  |
| 197 | `G197` | ・ |  |
| 197 | `H197` | Refer sheet 「setting_removal_parts_upd_hyjjn」 |  |
| 199 | `F199` | ・ |  |
| 199 | `G199` | Parameter: |  |
| 201 | `G201` | Param |  |
| 201 | `N201` | Giá trị |  |
| 201 | `AL201` | Remarks |  |
| 202 | `G202` | sishkshnprg_cd |  |
| 202 | `N202` | user_id get từ xử lý 1.1 |  |
| 202 | `AL202` | 更新者コード |  |
| 204 | `D204` | 7. |  |
| 204 | `E204` | Trường hợp insert data |  |
| 205 | `E205` | 7.1. |  |
| 205 | `F205` | Insert data vào table 取外部品マスタ |  |
| 206 | `F206` | ・ |  |
| 206 | `G206` | Table đối tượng |  |
| 207 | `G207` | ・ |  |
| 207 | `H207` | setting_removal_parts |  |
| 209 | `F209` | ・ |  |
| 209 | `G209` | Items insert: |  |
| 210 | `G210` | ・ |  |
| 210 | `H210` | Refer sheet 「setting_removal_parts_insert」 |  |
| 212 | `F212` | ・ |  |
| 212 | `G212` | Parameter: |  |
| 214 | `G214` | Param |  |
| 214 | `N214` | Giá trị |  |
| 214 | `AL214` | Remarks |  |
| 215 | `G215` | seiskjy_id |  |
| 215 | `N215` | seiskjy_id get từ xử lý 1.2 |  |
| 215 | `AL215` | 拠点ID |  |
| 216 | `G216` | sisnlin_id |  |
| 216 | `N216` | sisnlin_id get từ xử lý 1.2 |  |
| 216 | `AL216` | ラインID |  |
| 217 | `G217` | bmn_id |  |
| 217 | `N217` | bmn_id get từ xử lý 1.2 |  |
| 217 | `AL217` | 部門ID |  |
| 218 | `G218` | parts_list_nm |  |
| 218 | `N218` | parts_list_nm get từ xử lý 1.2 |  |
| 218 | `AL218` | プリセット名 |  |
| 219 | `G219` | file_nm |  |
| 219 | `N219` | file_nm get từ xử lý 1.2 |  |
| 219 | `AL219` | ファイル名 |  |
| 220 | `G220` | hyjjn_no |  |
| 220 | `N220` | hyjjn_no get ở xử lý 1.2 |  |
| 220 | `AL220` | 表示順 |  |
| 221 | `G221` | sksiprg_cd |  |
| 221 | `N221` | user_id get từ xử lý 1.1 |  |
| 221 | `AL221` | 作成者コード |  |
| 222 | `G222` | sishkshnprg_cd |  |
| 222 | `N222` | user_id get từ xử lý 1.1 |  |
| 222 | `AL222` | 更新者コード |  |
| 224 | `E224` | 7.2. |  |
| 224 | `F224` | Insert table 部品マスタ (setting_removal_parts_sb) |  |
| 225 | `F225` | ・ |  |
| 225 | `G225` | Thực hiện lặp lại các xử lý bên dưới với từng phần tử pposn_cd trong list_pposn_cd mà đã được get ở xử lý 1.2 |  |
| 226 | `G226` | ・ |  |
| 226 | `H226` | Table đối tượng |  |
| 227 | `H227` | ・ |  |
| 227 | `I227` | setting_removal_parts_sb |  |
| 229 | `G229` | ・ |  |
| 229 | `H229` | Items insert: |  |
| 230 | `H230` | ・ |  |
| 230 | `I230` | Refer sheet 「setting_removal_parts_sb」 |  |
| 232 | `G232` | ・ |  |
| 232 | `H232` | Parameter: |  |
| 234 | `H234` | Param |  |
| 234 | `N234` | Giá trị |  |
| 234 | `AL234` | Remarks |  |
| 235 | `H235` | parts_list_id |  |
| 235 | `N235` | parts_list_id sinh ra sau xử lý 7.1 |  |
| 235 | `AL235` | 取外部品ID |  |
| 236 | `H236` | pposn_cd |  |
| 236 | `N236` | Giá trị của phần tử pposn_cd trong list_pposn_cd |  |
| 236 | `AL236` | 部品部位コード |  |
| 238 | `D238` | 8. |  |
| 238 | `E238` | Trả về thông tin response |  |
| 239 | `E239` | 8.1. |  |
| 239 | `F239` | Trường hợp thành công |  |
| 240 | `F240` | Trả về response với mô tả như sau: |  |
| 241 | `F241` | ・ |  |
| 241 | `G241` | HTTPStatus = 200 |  |
| 242 | `F242` | ・ |  |
| 242 | `G242` | status = 1 |  |
| 243 | `F243` | ・ |  |
| 243 | `G243` | response |  |
| 244 | `G244` | Trả về giá trị  取外部品ID(parts_list_id) get ở xử lý 6.1 hoặc được sinh ra ở xử lý 7.1 tương ứng  với định nghĩa tại sheet [2.Response] |  |
| 246 | `E246` | 8.2. |  |
| 246 | `F246` | Trường hợp validate lỗi |  |
| 247 | `F247` | Trả về response với mô tả như sau: |  |
| 248 | `F248` | ・ |  |
| 248 | `G248` | HTTPStatus = 400 |  |
| 249 | `F249` | ・ |  |
| 249 | `G249` | status = 2 |  |
| 250 | `F250` | ・ |  |
| 250 | `G250` | response |  |
| 251 | `G251` | Trả về thông tin lỗi tương ứng  với định nghĩa tại sheet [2.Response] |  |
| 253 | `E253` | 8.3. |  |
| 253 | `F253` | Trường hợp phát sinh lỗi hệ thống |  |
| 254 | `F254` | Trả về response với mô tả như sau: |  |
| 255 | `F255` | ・ |  |
| 255 | `G255` | HTTPStatus = 500 |  |
| 256 | `F256` | ・ |  |
| 256 | `G256` | status = 2 |  |
| 257 | `F257` | ・ |  |
| 257 | `G257` | response |  |
| 258 | `G258` | Trả về thông tin lỗi tương ứng  với định nghĩa tại sheet [2.Response] |  |
| 260 | `F260` | ※ |  |
| 260 | `G260` | Trường hợp xảy ra lỗi thì chi tiết lỗi refer nội dung sheet [4.Error] |  |

</details>
