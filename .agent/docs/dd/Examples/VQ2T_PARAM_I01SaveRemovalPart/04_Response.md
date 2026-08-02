---
title: "Response"
order: 4
source_workbook: "【VQ2T-PARAM】API設計_I01_I01SaveRemovalPart_Ver1.0_VN 1.xlsx"
source_sheet: "2.Response"
dd_id: "I01SaveRemovalPart"
format: markdown
---

# Response

## Metadata kế thừa

| Thuộc tính | Giá trị | Công thức Excel nguồn |
|---|---|---|
| Project | `VQ2T-PARAM` | `=Overview!E1` |
| System | `設定管理` | `=Overview!H1` |
| Người tạo | `FPT AnNVK1` | Giá trị trực tiếp |
| Ngày tạo | `2026-04-09` | `='Lịch sử'!E2` |

## Giải thích

Giá trị trả về khi call API.

## Format

| Thuộc tính | Giá trị |
|---|---|
| Format | `JSON` |
| Code ký tự | `UTF-8` |
| Content-Type | `application/json` |

## Response fields

| No | Nhánh | Tên logic | Tên vật lý | Table nguồn get | Field nguồn get | Remarks |
|---:|---|---|---|---|---|---|
| 1 | Common | HTTP Status | `HTTPStatus` | `N/A` | `N/A` | Thành công: `200`; phát sinh lỗi: `500`; validate lỗi: `400` |
| 2 | Common | Status | `status` | `N/A` | `N/A` | Thành công: `1`; phát sinh error: `2` |
| 3 | Common | Nội dung response | `response` | `N/A` | `N/A` | |
| 3.1 | Success | 取外部品ID | `parts_list_id` | `setting_removal_parts` | `parts_list_id` | |
| 3.1 | Error | Error code | `error_code` | `N/A` | `N/A` | |
| 3.2 | Error | Error Message id | `error_message_id` | `N/A` | `N/A` | |

## Ví dụ thành công

> Ví dụ nguồn không phải JSON hợp lệ vì `HTTPStatus` nằm ngoài object, `parts_list_id` không có double quote và dùng single quote. Nội dung được giữ nguyên.

```text
HTTPStatus: 200

{
  "status": 1,
  "response": {
    parts_list_id:'1',
  }
}
```

## Ví dụ lỗi

> Ví dụ nguồn có `HTTPStatus` nằm ngoài object. Nội dung được giữ nguyên.

```text
"HTTPStatus": 500

{
  "status": 2,
  "response": {
    "error_code": "9999",
    "error_message_id": "DLG0001"
  }
}
```

---
## Phụ lục đối chiếu nguồn Excel
- Workbook nguồn: `【VQ2T-PARAM】API設計_I01_I01SaveRemovalPart_Ver1.0_VN 1.xlsx`
- Sheet nguồn: `2.Response`
- Dimension: `A1:BR49`
- Trạng thái: `visible`
- Số ô có dữ liệu/công thức: `71`
- Số vùng merge: `31`

<details>
<summary>Danh sách vùng merge</summary>

- `B17:C18`
- `AU1:AW1`
- `AU2:AW2`
- `AX2:BA2`
- `AX1:BA1`
- `A2:D2`
- `AP2:AT2`
- `A1:D1`
- `E1:G1`
- `H1:AL1`
- `AM1:AO1`
- `AP1:AT1`
- `E2:G2`
- `D17:S17`
- `T17:AK17`
- `AL17:BA18`
- `AM2:AO2`
- `T2:Y2`
- `Z2:AE2`
- `AF2:AL2`
- `H2:M2`
- `N2:S2`
- `B19:C19`
- `B20:C20`
- `B26:C26`
- `B25:C25`
- `B22:BA22`
- `B24:BA24`
- `B21:C21`
- `T21:AB21`
- `AC21:AK21`

</details>

<details>
<summary>Bản ghi từng ô có dữ liệu hoặc công thức</summary>

| Hàng | Ô | Giá trị nguồn | Công thức nguồn |
|---:|---|---|---|
| 1 | `A1` | Project |  |
| 1 | `E1` | VQ2T-PARAM | Overview!E1 |
| 1 | `H1` | 設定管理 | Overview!H1 |
| 1 | `AM1` | Người tạo |  |
| 1 | `AP1` | FPT AnNVK1 |  |
| 1 | `AU1` | Ngày tạo |  |
| 1 | `AX1` | 46121 | 'Lịch sử'!E2 |
| 2 | `A2` | Loại tài liệu |  |
| 2 | `E2` | DD |  |
| 2 | `H2` | API |  |
| 2 | `N2` | Response |  |
| 2 | `AM2` | Người update |  |
| 2 | `AU2` | Ngày update |  |
| 5 | `B5` | Giải thích |  |
| 7 | `C7` | Giá trị trả về khi call API |  |
| 12 | `B12` | Format |  |
| 12 | `L12` | JSON |  |
| 13 | `B13` | Code ký tự |  |
| 13 | `L13` | UTF-8 |  |
| 14 | `B14` | Content-Type |  |
| 14 | `L14` | application/json |  |
| 17 | `B17` | No |  |
| 17 | `D17` | Response item name |  |
| 17 | `T17` | Refer DB |  |
| 17 | `AL17` | Remarks |  |
| 18 | `D18` | Tên logic |  |
| 18 | `L18` | Tên vật lý |  |
| 18 | `T18` | Table nguồn get |  |
| 18 | `AC18` | Field nguồn get |  |
| 19 | `B19` | 1 |  |
| 19 | `D19` | HTTP Status |  |
| 19 | `L19` | HTTPStatus |  |
| 19 | `AL19` | Thành công: 200/ Phát sinh lỗi: 500/ Validate lỗi: 400 |  |
| 20 | `B20` | 2 |  |
| 20 | `D20` | Status |  |
| 20 | `L20` | status |  |
| 20 | `AL20` | Thành công: 1/phát sinh error: 2 |  |
| 21 | `B21` | 3 |  |
| 21 | `D21` | Nội dung response |  |
| 21 | `L21` | response |  |
| 22 | `B22` | Trường hợp thành công |  |
| 23 | `C23` | 3.1 |  |
| 23 | `E23` | 取外部品ID |  |
| 23 | `M23` | parts_list_id |  |
| 23 | `T23` | setting_removal_parts |  |
| 23 | `AC23` | parts_list_id |  |
| 24 | `B24` | Các trường hợp lỗi của API |  |
| 25 | `B25` | 3.1 |  |
| 25 | `E25` | Error code |  |
| 25 | `M25` | error_code |  |
| 26 | `B26` | 3.2 |  |
| 26 | `E26` | Error Message id |  |
| 26 | `M26` | error_message_id |  |
| 28 | `B28` | Ví dụ |  |
| 29 | `M29` | Trường hợp thành công |  |
| 30 | `N30` | HTTPStatus: 200 |  |
| 32 | `N32` | { |  |
| 33 | `O33` |   "status": 1 , |  |
| 34 | `O34` |   "response":{ |  |
| 35 | `Q35` | parts_list_id:'1', |  |
| 36 | `O36` | } |  |
| 37 | `N37` | } |  |
| 39 | `M39` | Trường hợp lỗi |  |
| 40 | `N40` | "HTTPStatus": 500 |  |
| 42 | `N42` | { |  |
| 43 | `O43` | "status" : 2 , |  |
| 44 | `O44` | "response" : {  |  |
| 45 | `P45` | "error_code" : "9999", |  |
| 46 | `P46` | "error_message_id" : "DLG0001" |  |
| 47 | `O47` |  } |  |
| 48 | `N48` |  } |  |

</details>
