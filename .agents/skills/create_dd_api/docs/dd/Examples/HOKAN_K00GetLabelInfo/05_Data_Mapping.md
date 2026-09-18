---
title: "Data Mapping"
order: 5
source_workbook: "【HOKAN】API設計_K00_K00GetLabelInfo_Ver1.0_VN(2).xlsx"
source_sheet: "3.Data mapping"
dd_id: "K00GetLabelInfo"
format: markdown
---

# Data Mapping

## Metadata kế thừa

| Thuộc tính | Giá trị | Công thức Excel nguồn |
|---|---|---|
| Project | `HOKAN` | `=Overview!E1` |
| System | `保管管理` | `=Overview!H1` |
| Người tạo | `FPT HongLT10` | `=Overview!AP1` |
| Ngày tạo | `2026-05-15` | `=Overview!AX1` |

## Flow xử lý data

## 1. Get thông tin

### 1.1. Get thông tin sau từ session storage của browser

- `N/A`.

### 1.2. Get thông tin sau từ request data

- `N/A`.

## 2. Check quyền

- `N/A`.

## 3. Validate data input

### 3.1. Thực hiện validate thông tin input đã get ở xử lý 1.2

- `N/A`.

## 4. Get thông tin label

### 4.1. Get danh sách Label ID theo từng màn hình

- Get list Label ID đã được define trong file CONSTANT tương ứng từng màn hình.
- Chi tiết list label ID theo từng màn hình refer các file Markdown tương ứng.

| No | Screen ID | Refer file | Remarks |
|---:|---|---|---|
| 1 | `K00-01` | [07_K00-01.md](./07_K00-01.md) | 共通機能選択 |
| 2 | `K01-01` | [08_K01-01.md](./08_K01-01.md) | 保管管理 |
| 3 | `K01-02` | [09_K01-02.md](./09_K01-02.md) | 検査詳細 |
| 4 | `K01-03` | [10_K01-03.md](./10_K01-03.md) | 不具合詳細 |
| 5 | `K01-04` | [11_K01-04.md](./11_K01-04.md) | 発行一覧 |
| 6 | `K01-05` | [12_K01-05.md](./12_K01-05.md) | 部品脱着情報 |
| 7 | `K01-06` | [13_K01-06.md](./13_K01-06.md) | 履歴修正 |
| 8 | `K02-01` | [14_K02-01.md](./14_K02-01.md) | 過去実績管理 |
| 9 | `K02-02` | [15_K02-02.md](./15_K02-02.md) | 削除一覧 |
| 10 | `Error message` | [16_Error_Message.md](./16_Error_Message.md) | |

### 4.2. Get thông tin label từ table 項目名称(ラベル)マスタ

| Table get | Column get | Chú thích | Remarks |
|---|---|---|---|
| `txn_prm_t0107` | `kmk_lbl_id` | 項目ラベルID | |
| `↑` | `kmk_lbl_nm` | 項目ラベル名称 | |

**Điều kiện get data**

- `txn_prm_t0107.kmk_lbl_id IN <list label id get từ xử lý 4.1>`.
- `txn_prm_t0107.skj_flg = '0'`.

**Điều kiện sort**

- `txn_prm_t0107.kmk_lbl_id ASC`.

## 5. Trả về thông tin response

### 5.1. Trường hợp thành công

- `HTTPStatus = 200`.
- `status = 1`.
- `response`: trả về thông tin label get ở xử lý `4.2`, tương ứng định nghĩa tại [04_Response.md](./04_Response.md).

### 5.2. Trường hợp validate lỗi

- `HTTPStatus = 400`.
- `status = 2`.
- `response`: trả về thông tin lỗi tương ứng định nghĩa tại [04_Response.md](./04_Response.md).

### 5.3. Trường hợp phát sinh lỗi hệ thống

- `HTTPStatus = 500`.
- `status = 2`.
- `response`: trả về thông tin lỗi tương ứng định nghĩa tại [04_Response.md](./04_Response.md).

> Trường hợp xảy ra lỗi, chi tiết refer [06_Error.md](./06_Error.md).

---
## Phụ lục đối chiếu nguồn Excel
- Workbook nguồn: `【HOKAN】API設計_K00_K00GetLabelInfo_Ver1.0_VN(2).xlsx`
- Sheet nguồn: `3.Data mapping`
- Dimension: `A1:BA75`
- Trạng thái: `visible`
- Số ô có dữ liệu/công thức: `142`
- Số vùng merge: `18`

<details>
<summary>Danh sách vùng merge</summary>

- `AU1:AW1`
- `AU2:AW2`
- `AX2:BA2`
- `AX1:BA1`
- `Z2:AE2`
- `AF2:AL2`
- `AM2:AO2`
- `AP2:AT2`
- `AM1:AO1`
- `AP1:AT1`
- `A1:D1`
- `E1:G1`
- `H1:AL1`
- `A2:D2`
- `E2:G2`
- `H2:M2`
- `N2:S2`
- `T2:Y2`

</details>

<details>
<summary>Bản ghi từng ô có dữ liệu hoặc công thức</summary>

| Hàng | Ô | Giá trị nguồn | Công thức nguồn |
|---:|---|---|---|
| 1 | `A1` | Project |  |
| 1 | `E1` | HOKAN | Overview!E1 |
| 1 | `H1` | 保管管理 | Overview!H1 |
| 1 | `AM1` | Người tạo |  |
| 1 | `AP1` | FPT HongLT10 | Overview!AP1 |
| 1 | `AU1` | Ngày tạo |  |
| 1 | `AX1` | 46157 | Overview!AX1 |
| 2 | `A2` | Loại tài liệu |  |
| 2 | `E2` | Detail Design |  |
| 2 | `H2` | API |  |
| 2 | `N2` | Data mapping |  |
| 2 | `AM2` | Người update |  |
| 2 | `AU2` | Ngày update |  |
| 5 | `B5` | Flow xử lý data |  |
| 7 | `D7` | 1. |  |
| 7 | `E7` | Get thông tin |  |
| 8 | `E8` | 1.1. |  |
| 8 | `F8` | Get thông tin sau từ session storage của browser. |  |
| 9 | `F9` | ・ |  |
| 9 | `G9` | N/A |  |
| 11 | `E11` | 1.2. |  |
| 11 | `F11` | Get thông tin sau từ request data: |  |
| 12 | `F12` | ・ |  |
| 12 | `G12` | N/A |  |
| 14 | `D14` | 2. |  |
| 14 | `E14` | Check quyền |  |
| 15 | `E15` | ・ |  |
| 15 | `F15` | N/A |  |
| 17 | `D17` | 3. |  |
| 17 | `E17` | Validate data input |  |
| 18 | `E18` | 3.1. |  |
| 18 | `F18` | Thực hiện validate thông tin input đã get ở xử lý 1.2 |  |
| 19 | `F19` | ・ |  |
| 19 | `G19` | N/A |  |
| 21 | `D21` | 4. |  |
| 21 | `E21` | Get thông tin label |  |
| 22 | `E22` | 4.1. |  |
| 22 | `F22` | Get ra danh sách Label ID theo từng màn hình |  |
| 23 | `F23` | ・ |  |
| 23 | `G23` | Get ra list Label ID đã đươc define trong file CONSTANT tương ứng từng màn hình |  |
| 25 | `F25` | ※ |  |
| 25 | `G25` | Chi tiết list label ID theo từng màn hình refer các sheet sau: |  |
| 27 | `G27` | № |  |
| 27 | `H27` | Screen ID |  |
| 27 | `N27` | Refer sheet |  |
| 27 | `Z27` | Remarks |  |
| 28 | `G28` | 1 |  |
| 28 | `H28` | K00-01 |  |
| 28 | `N28` | K00-01 |  |
| 28 | `Z28` | 共通機能選択 |  |
| 29 | `G29` | 2 |  |
| 29 | `H29` | K01-01 |  |
| 29 | `N29` | K01-01 |  |
| 29 | `Z29` | 保管管理 |  |
| 30 | `G30` | 3 |  |
| 30 | `H30` | K01-02 |  |
| 30 | `N30` | K01-02 |  |
| 30 | `Z30` | 検査詳細 |  |
| 31 | `G31` | 4 |  |
| 31 | `H31` | K01-03 |  |
| 31 | `N31` | K01-03 |  |
| 31 | `Z31` | 不具合詳細 |  |
| 32 | `G32` | 5 |  |
| 32 | `H32` | K01-04 |  |
| 32 | `N32` | K01-04 |  |
| 32 | `Z32` | 発行一覧 |  |
| 33 | `G33` | 6 |  |
| 33 | `H33` | K01-05 |  |
| 33 | `N33` | K01-05 |  |
| 33 | `Z33` | 部品脱着情報 |  |
| 34 | `G34` | 7 |  |
| 34 | `H34` | K01-06 |  |
| 34 | `N34` | K01-06 |  |
| 34 | `Z34` | 履歴修正 |  |
| 35 | `G35` | 8 |  |
| 35 | `H35` | K02-01 |  |
| 35 | `N35` | K02-01 |  |
| 35 | `Z35` | 過去実績管理 |  |
| 36 | `G36` | 9 |  |
| 36 | `H36` | K02-02 |  |
| 36 | `N36` | K02-02 |  |
| 36 | `Z36` | 削除一覧 |  |
| 37 | `G37` | 10 |  |
| 37 | `H37` | Error message |  |
| 37 | `N37` | Error_Message |  |
| 39 | `E39` | 4.2. |  |
| 39 | `F39` | Get thông tin label từ table 項目名称(ラベル)マスタ |  |
| 41 | `F41` | Table get |  |
| 41 | `N41` | Column get |  |
| 41 | `Z41` | Chú thích |  |
| 41 | `AL41` | Remarks |  |
| 42 | `F42` | txn_prm_t0107 |  |
| 42 | `N42` | kmk_lbl_id |  |
| 42 | `Z42` | 項目ラベルID |  |
| 43 | `F43` | ↑ |  |
| 43 | `N43` | kmk_lbl_nm |  |
| 43 | `Z43` | 項目ラベル名称 |  |
| 45 | `F45` | ・ |  |
| 45 | `G45` | Điều kiện get data |  |
| 46 | `G46` | ・ |  |
| 46 | `H46` | txn_prm_t0107.kmk_lbl_id IN < list label id get từ xử lý 4.1>  |  |
| 47 | `G47` | ・ |  |
| 47 | `H47` | txn_prm_t0107.skj_flg = '0' |  |
| 49 | `F49` | ・ |  |
| 49 | `G49` | Điều kiện sort |  |
| 50 | `G50` | ・ |  |
| 50 | `H50` | txn_prm_t0107.kmk_lbl_id |  |
| 50 | `P50` | ASC |  |
| 52 | `D52` | 5.   |  |
| 52 | `E52` | Trả về thông tin response |  |
| 53 | `E53` | 5.1.  |  |
| 53 | `F53` | Trường hợp thành công |  |
| 54 | `F54` | Trả về response với mô tả như sau: |  |
| 55 | `F55` | ・ |  |
| 55 | `G55` | HTTPStatus = 200 |  |
| 56 | `F56` | ・ |  |
| 56 | `G56` | status = 1 |  |
| 57 | `F57` | ・ |  |
| 57 | `G57` | response |  |
| 58 | `G58` | Trả về thông tin label đã get ở xử lý 4.2 tương ứng với định nghĩa tại sheet [2.Response] |  |
| 60 | `E60` | 5.2. |  |
| 60 | `F60` | Trường hợp validate lỗi |  |
| 61 | `F61` | Trả về response với mô tả như sau: |  |
| 62 | `F62` | ・ |  |
| 62 | `G62` | HTTPStatus = 400 |  |
| 63 | `F63` | ・ |  |
| 63 | `G63` | status = 2 |  |
| 64 | `F64` | ・ |  |
| 64 | `G64` | response |  |
| 65 | `G65` | Trả về thông tin lỗi tương ứng với định nghĩa tại sheet [2.Response] |  |
| 67 | `E67` | 5.3. |  |
| 67 | `F67` | Trường hợp phát sinh lỗi hệ thống |  |
| 68 | `F68` | Trả về response với mô tả như sau: |  |
| 69 | `F69` | ・ |  |
| 69 | `G69` | HTTPStatus = 500 |  |
| 70 | `F70` | ・ |  |
| 70 | `G70` | status = 2 |  |
| 71 | `F71` | ・ |  |
| 71 | `G71` | response |  |
| 72 | `G72` | Trả về thông tin lỗi tương ứng với định nghĩa tại sheet [2.Response] |  |
| 74 | `E74` | ※ |  |
| 74 | `F74` | Trường hợp xảy ra lỗi thì chi tiết lỗi refer nội dung sheet [4.Error] |  |

</details>
