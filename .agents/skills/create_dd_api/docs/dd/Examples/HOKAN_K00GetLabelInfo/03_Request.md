---
title: "Request"
order: 3
source_workbook: "【HOKAN】API設計_K00_K00GetLabelInfo_Ver1.0_VN(2).xlsx"
source_sheet: "1.Request"
dd_id: "K00GetLabelInfo"
format: markdown
---

# Request

## Metadata kế thừa

| Thuộc tính | Giá trị | Công thức Excel nguồn |
|---|---|---|
| Project | `HOKAN` | `=Overview!E1` |
| System | `保管管理` | `=Overview!H1` |
| Người tạo | `FPT HongLT10` | `=Overview!AP1` |
| Ngày tạo | `2026-05-15` | `=Overview!AX1` |

## API endpoint

| Thuộc tính | Giá trị |
|---|---|
| HTTP method | `GET` |
| URI | `/api/k00/K00GetLabelInfo` |
| Code ký tự | `UTF-8` |

## Request header

| No | Name | Field name | Giá trị | Giải thích |
|---:|---|---|---|---|
| 1 | Contents type | `Content-Type` | `application/json` | Thực hiện request bằng json data |
| 2 | Basic authen | `Authorization` | `Token` | |

## Request data

| No | Key name | Nội dung |
|---:|---|---|
| 1 | `N/A` | API không có request data |

## Ví dụ Request data

```json
{
}
```

---
## Phụ lục đối chiếu nguồn Excel
- Workbook nguồn: `【HOKAN】API設計_K00_K00GetLabelInfo_Ver1.0_VN(2).xlsx`
- Sheet nguồn: `1.Request`
- Dimension: `A1:BR28`
- Trạng thái: `visible`
- Số ô có dữ liệu/công thức: `50`
- Số vùng merge: `30`

<details>
<summary>Danh sách vùng merge</summary>

- `A1:D1`
- `E1:G1`
- `H1:AL1`
- `AM1:AO1`
- `AP2:AT2`
- `A2:D2`
- `E2:G2`
- `H2:M2`
- `N2:S2`
- `AP1:AT1`
- `AU1:AW1`
- `AX1:BA1`
- `AX2:BA2`
- `AU2:AW2`
- `T2:Y2`
- `Z2:AE2`
- `AF2:AL2`
- `AM2:AO2`
- `Y16:AA17`
- `AB16:AG16`
- `AH16:AJ17`
- `U17:V17`
- `W17:X17`
- `AB17:AD17`
- `AE17:AG17`
- `S18:T18`
- `U18:V18`
- `W18:X18`
- `S16:T17`
- `U16:X16`

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
| 2 | `N2` | Request |  |
| 2 | `AM2` | Người update |  |
| 2 | `AU2` | Ngày update |  |
| 5 | `B5` | HTTP method |  |
| 5 | `L5` | GET |  |
| 6 | `B6` | URI |  |
| 6 | `L6` | /api/k00/K00GetLabelInfo |  |
| 7 | `B7` | Code ký tự |  |
| 7 | `L7` | UTF-8 |  |
| 9 | `B9` | Request header |  |
| 10 | `B10` | Name |  |
| 10 | `J10` | Field name |  |
| 10 | `V10` | Giá trị |  |
| 10 | `AK10` | Giải thích |  |
| 11 | `B11` | Contents type |  |
| 11 | `J11` | Content-Type |  |
| 11 | `V11` | application/json |  |
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
| 18 | `C18` | N/A |  |
| 20 | `B20` | Ví dụ về Request data |  |
| 23 | `L23` | { |  |
| 25 | `L25` | } |  |

</details>
