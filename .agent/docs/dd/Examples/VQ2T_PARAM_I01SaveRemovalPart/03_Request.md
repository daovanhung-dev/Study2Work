---
title: "Request"
order: 3
source_workbook: "【VQ2T-PARAM】API設計_I01_I01SaveRemovalPart_Ver1.0_VN 1.xlsx"
source_sheet: "1.Request"
dd_id: "I01SaveRemovalPart"
format: markdown
---

# Request

## Metadata kế thừa

| Thuộc tính | Giá trị | Công thức Excel nguồn |
|---|---|---|
| Project | `VQ2T-PARAM` | `=Overview!E1` |
| System | `設定管理` | `=Overview!H1` |
| Người tạo | `FPT AnNVK1` | `='Lịch sử'!C4` |
| Ngày tạo | `2026-04-09` | `='Lịch sử'!E2` |

## API endpoint

| Thuộc tính | Giá trị |
|---|---|
| HTTP method | `POST` |
| URI | `/api/i01/I01SaveRemovalPart` |
| Code ký tự | `UTF-8` |

## Request header

| No | Name | Field name | Giá trị | Giải thích |
|---:|---|---|---|---|
| 1 | Contents type | `Content-Type` | `form-data` | Thực hiện request bằng json data |
| 2 | Basic authen | `Authorization` | `Token` | |

> Nguồn có xung đột giữa `form-data` và mô tả “request bằng json data”. Nội dung được giữ nguyên khi chuyển đổi.

## Request data

| No | Tên logic | Tên vật lý | Bắt buộc | Tối thiểu | Tối đa | Loại ký tự / Type | Format | Giá trị hợp lệ | Giải thích |
|---:|---|---|---:|---:|---:|---|---|---|---|
| 1 | 拠点ID | `seiskjy_id` | `○` | `-` | `5` | `String` | | | |
| 2 | ラインID | `sisnlin_id` | `○` | `-` | `5` | `String` | | | |
| 3 | 部門ID | `bmn_id` | `○` | `-` | `3` | `String` | | | |
| 4 | 取外部品ID | `parts_list_id` | `○` | `-` | `5` | `String` | | | |
| 5 | プリセット名 | `parts_list_nm` | `○` | `-` | `50` | `String` | | | |
| 6 | ファイル名 | `file_nm` | `○` | `-` | `50` | `String` | | | |
| 7 | 表示順 | `hyjjn_no` | `○` | `-` | `-` | `Integer` | | | |
| 8 | Danh sách 部品部位コード | `list_pposn_cd` | `○` | `-` | `-` | `Mảng ký tự` | | | |

## Ví dụ Request data

> `hyjjn_no` được định nghĩa là Integer nhưng ví dụ nguồn dùng chuỗi `"1"`. Nội dung được giữ nguyên.

```json
{
  "seiskjy_id": "10001",
  "sisnlin_id": "20001",
  "bmn_id": "101",
  "parts_list_id": "1",
  "parts_list_nm": "取外部品プリセットA",
  "file_nm": "removal_parts_preset_a.csv",
  "hyjjn_no": "1",
  "list_pposn_cd": [
    "PP001",
    "PP002",
    "PP003"
  ]
}
```

---
## Phụ lục đối chiếu nguồn Excel
- Workbook nguồn: `【VQ2T-PARAM】API設計_I01_I01SaveRemovalPart_Ver1.0_VN 1.xlsx`
- Sheet nguồn: `1.Request`
- Dimension: `A1:BR42`
- Trạng thái: `visible`
- Số ô có dữ liệu/công thức: `116`
- Số vùng merge: `60`

<details>
<summary>Danh sách vùng merge</summary>

- `S21:T21`
- `U21:V21`
- `W21:X21`
- `Y21:AA21`
- `S23:T23`
- `U23:V23`
- `W23:X23`
- `Y23:AA23`
- `W20:X20`
- `Y20:AA20`
- `U17:V17`
- `W17:X17`
- `S18:T18`
- `U18:V18`
- `W18:X18`
- `Y18:AA18`
- `S19:T19`
- `U19:V19`
- `W19:X19`
- `Y19:AA19`
- `AB17:AD17`
- `AE17:AG17`
- `S25:T25`
- `U25:V25`
- `W25:X25`
- `Y25:AA25`
- `S24:T24`
- `U24:V24`
- `W24:X24`
- `Y24:AA24`
- `S22:T22`
- `U22:V22`
- `W22:X22`
- `Y22:AA22`
- `S20:T20`
- `U20:V20`
- `AU1:AW1`
- `AX1:BA1`
- `AX2:BA2`
- `AU2:AW2`
- `AM1:AO1`
- `AP2:AT2`
- `AP1:AT1`
- `AM2:AO2`
- `S26:T26`
- `A1:D1`
- `E1:G1`
- `H1:AL1`
- `Z2:AE2`
- `AF2:AL2`
- `T2:Y2`
- `A2:D2`
- `E2:G2`
- `H2:M2`
- `N2:S2`
- `S16:T17`
- `U16:X16`
- `Y16:AA17`
- `AB16:AG16`
- `AH16:AJ17`

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
| 1 | `AX1` | 46121 | 'Lịch sử'!E2 |
| 2 | `A2` | Loại tài liệu |  |
| 2 | `E2` | DD |  |
| 2 | `H2` | API |  |
| 2 | `N2` | Request |  |
| 2 | `AM2` | Người update |  |
| 2 | `AU2` | Ngày update |  |
| 5 | `B5` | HTTP method |  |
| 5 | `L5` | POST |  |
| 6 | `B6` | URI |  |
| 6 | `L6` | /api/i01/I01SaveRemovalPart |  |
| 7 | `B7` | Code ký tự |  |
| 7 | `L7` | UTF-8 |  |
| 9 | `B9` | Request header |  |
| 10 | `B10` | Name |  |
| 10 | `J10` | Field name |  |
| 10 | `V10` | Giá trị |  |
| 10 | `AK10` | Giải thích |  |
| 11 | `B11` | Contents type |  |
| 11 | `J11` | Content-Type |  |
| 11 | `V11` | form-data |  |
| 11 | `AK11` | Thực hiện request bằng json data |  |
| 12 | `B12` | Basic authen |  |
| 12 | `J12` | Authorization |  |
| 12 | `V12` | Token |  |
| 14 | `B14` | Request data |  |
| 15 | `B15` | No |  |
| 15 | `C15` | Key name |  |
| 15 | `S15` | Nội dung check |  |
| 15 | `AK15` | Giải thích |  |
| 16 | `S16` | Bắt buộc |  |
| 16 | `U16` | Số ký tự |  |
| 16 | `Y16` | Loại ký tự |  |
| 16 | `AB16` | Format |  |
| 16 | `AH16` | Giá trị hợp lệ |  |
| 17 | `C17` | Logic |  |
| 17 | `K17` | Vật lý |  |
| 17 | `U17` | Tối thiểu |  |
| 17 | `W17` | Tối đa |  |
| 18 | `B18` | 1 |  |
| 18 | `C18` | 拠点ID |  |
| 18 | `K18` | seiskjy_id |  |
| 18 | `S18` | ○ |  |
| 18 | `U18` | - |  |
| 18 | `W18` | 5 |  |
| 18 | `Y18` | String |  |
| 19 | `B19` | 2 |  |
| 19 | `C19` | ラインID |  |
| 19 | `K19` | sisnlin_id |  |
| 19 | `S19` | ○ |  |
| 19 | `U19` | - |  |
| 19 | `W19` | 5 |  |
| 19 | `Y19` | String |  |
| 20 | `B20` | 3 |  |
| 20 | `C20` | 部門ID |  |
| 20 | `K20` | bmn_id |  |
| 20 | `S20` | ○ |  |
| 20 | `U20` | - |  |
| 20 | `W20` | 3 |  |
| 20 | `Y20` | String |  |
| 21 | `B21` | 4 |  |
| 21 | `C21` | 取外部品ID |  |
| 21 | `K21` | parts_list_id |  |
| 21 | `S21` | ○ |  |
| 21 | `U21` | - |  |
| 21 | `W21` | 5 |  |
| 21 | `Y21` | String |  |
| 22 | `B22` | 5 |  |
| 22 | `C22` | プリセット名 |  |
| 22 | `K22` | parts_list_nm |  |
| 22 | `S22` | ○ |  |
| 22 | `U22` | - |  |
| 22 | `W22` | 50 |  |
| 22 | `Y22` | String |  |
| 23 | `B23` | 6 |  |
| 23 | `C23` | ファイル名 |  |
| 23 | `K23` | file_nm |  |
| 23 | `S23` | ○ |  |
| 23 | `U23` | - |  |
| 23 | `W23` | 50 |  |
| 23 | `Y23` | String |  |
| 24 | `B24` | 7 |  |
| 24 | `C24` | 表示順 |  |
| 24 | `K24` | hyjjn_no  |  |
| 24 | `S24` | ○ |  |
| 24 | `U24` | - |  |
| 24 | `W24` | - |  |
| 24 | `Y24` | Integer |  |
| 25 | `B25` | 8 |  |
| 25 | `C25` | Danh sách 部品部位コード |  |
| 25 | `K25` | list_pposn_cd |  |
| 25 | `S25` | ○ |  |
| 25 | `U25` | - |  |
| 25 | `W25` | - |  |
| 25 | `Y25` | Mảng ký tự |  |
| 27 | `B27` | Ví dụ về Request data |  |
| 28 | `L28` | { |  |
| 29 | `L29` |   "seiskjy_id": "10001", |  |
| 30 | `L30` |   "sisnlin_id": "20001", |  |
| 31 | `L31` |   "bmn_id": "101", |  |
| 32 | `L32` |   "parts_list_id": "1", |  |
| 33 | `L33` |   "parts_list_nm": "取外部品プリセットA", |  |
| 34 | `L34` |   "file_nm": "removal_parts_preset_a.csv", |  |
| 35 | `L35` |   "hyjjn_no": "1", |  |
| 36 | `L36` |   "list_pposn_cd": [ |  |
| 37 | `L37` |     "PP001", |  |
| 38 | `L38` |     "PP002", |  |
| 39 | `L39` |     "PP003" |  |
| 40 | `L40` |   ] |  |
| 41 | `L41` | } |  |

</details>
