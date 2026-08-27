---
title: "Response"
order: 4
source_workbook: "【HOKAN】API設計_K00_K00GetLabelInfo_Ver1.0_VN(2).xlsx"
source_sheet: "2.Response"
dd_id: "K00GetLabelInfo"
format: markdown
---

# Response

## Metadata kế thừa

| Thuộc tính | Giá trị | Công thức Excel nguồn |
|---|---|---|
| Project | `HOKAN` | `=Overview!E1` |
| System | `保管管理` | `=Overview!H1` |
| Người tạo | `FPT HongLT10` | `=Overview!AP1` |
| Ngày tạo | `2026-05-15` | `=Overview!AX1` |

## Introduction

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
| 1 | Common | HTTP Status | `HTTP Status` | `N/A` | `N/A` | Thành công: `200`; phát sinh lỗi: `500`; validate lỗi: `400` |
| 2 | Common | Status | `Status` | `N/A` | `N/A` | Thành công: `1`; phát sinh error: `2` |
| 3 | Common | Nội dung response | `response` | `N/A` | `N/A` | |
| 3.1 | Success | Thông tin Labels | `list_item` | `N/A` | `N/A` | |
| 3.1.1 | Success | 項目ラベルID | `kmk_lbl_id` | `txn_prm_t0107` | `kmk_lbl_id` | |
| 3.1.2 | Success | 項目ラベル名称 | `kmk_lbl_nm` | `txn_prm_t0107` | `kmk_lbl_nm` | |
| 3.1 | Error | Error code | `error_code` | `N/A` | `N/A` | |
| 3.2 | Error | Error Message id | `error_message_id` | `N/A` | `N/A` | |

## Ví dụ thành công

> Nguồn Excel định nghĩa field là `list_item`, `kmk_lbl_id`, `kmk_lbl_nm` nhưng ví dụ sử dụng `label_data` dạng object. Nội dung được giữ nguyên để bảo toàn nguồn.

```text
"HTTPStatus": 200

{
  "status": "1",
  "response": {
    "label_data": {
      "K010901": "配置管理",
      "K010902": "配置計画",
      "K010903": "配置ダッシュボード",
      "K010904": "承認・参照"
    }
  }
}
```

## Ví dụ lỗi

```text
"HTTPStatus": 400

{
  "status": 2,
  "response": {
    "error_code": "9999",
    "error_message_id": "DLG000000"
  }
}
```

---
## Phụ lục đối chiếu nguồn Excel
- Workbook nguồn: `【HOKAN】API設計_K00_K00GetLabelInfo_Ver1.0_VN(2).xlsx`
- Sheet nguồn: `2.Response`
- Dimension: `A1:BQ56`
- Trạng thái: `visible`
- Số ô có dữ liệu/công thức: `82`
- Số vùng merge: `36`

<details>
<summary>Danh sách vùng merge</summary>

- `B22:BA22`
- `E2:G2`
- `AM2:AO2`
- `T2:Y2`
- `Z2:AE2`
- `AF2:AL2`
- `H2:M2`
- `N2:S2`
- `B19:C19`
- `T19:AB19`
- `AC19:AK19`
- `B20:C20`
- `B21:C21`
- `T21:AB21`
- `AC21:AK21`
- `B28:C28`
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
- `B17:C18`
- `D17:S17`
- `T17:AK17`
- `AL17:BA18`
- `B24:C24`
- `B25:C25`
- `B23:C23`
- `B26:BA26`
- `B27:C27`

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
| 2 | `N2` | Response |  |
| 2 | `AM2` | Người update |  |
| 2 | `AU2` | Ngày update |  |
| 5 | `B5` | 説明/Introduction |  |
| 7 | `C7` | Giá trị trả về khi call API |  |
| 12 | `B12` | 形式 |  |
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
| 19 | `L19` | HTTP Status |  |
| 19 | `AL19` | Thành công: 200/ Phát sinh lỗi: 500/ Validate lỗi: 400 |  |
| 20 | `B20` | 2 |  |
| 20 | `D20` | Status |  |
| 20 | `L20` | Status |  |
| 20 | `AL20` | Thành công: 1/phát sinh error: 2 |  |
| 21 | `B21` | 3 |  |
| 21 | `D21` | Nội dung response |  |
| 21 | `L21` | response |  |
| 22 | `B22` | Trường hợp thành công |  |
| 23 | `B23` | 3.1 |  |
| 23 | `E23` | Thông tin Labels |  |
| 23 | `M23` | list_item |  |
| 24 | `F24` | 項目ラベルID |  |
| 24 | `N24` | kmk_lbl_id |  |
| 24 | `T24` | txn_prm_t0107 |  |
| 24 | `AC24` | kmk_lbl_id |  |
| 25 | `F25` | 項目ラベル名称 |  |
| 25 | `N25` | kmk_lbl_nm |  |
| 25 | `T25` | txn_prm_t0107 |  |
| 25 | `AC25` | kmk_lbl_nm |  |
| 26 | `B26` | Trường hợp lỗi |  |
| 27 | `B27` | 3.1 |  |
| 27 | `E27` | Error code |  |
| 27 | `M27` | error_code |  |
| 28 | `B28` | 3.2 |  |
| 28 | `E28` | Error Message id |  |
| 28 | `M28` | error_message_id |  |
| 30 | `B30` | Ví dụ |  |
| 31 | `M31` | Trường hợp thành công |  |
| 32 | `N32` | "HTTPStatus": 200 |  |
| 34 | `N34` | { |  |
| 35 | `O35` | "status": "1", |  |
| 36 | `O36` | "response": { |  |
| 37 | `P37` | "label_data": { |  |
| 38 | `Q38` | "K010901": "配置管理", |  |
| 39 | `Q39` | "K010902": "配置計画", |  |
| 40 | `Q40` | "K010903": "配置ダッシュボード", |  |
| 41 | `Q41` | "K010904": "承認・参照" |  |
| 42 | `P42` | } |  |
| 43 | `O43` | } |  |
| 44 | `N44` | } |  |
| 46 | `M46` | Trường hợp lỗi |  |
| 47 | `N47` | "HTTPStatus": 400 |  |
| 49 | `N49` | { |  |
| 50 | `O50` | "status" : 2 , |  |
| 51 | `O51` | "response" : {  |  |
| 52 | `P52` | "error_code" : "9999", |  |
| 53 | `P53` | "error_message_id" : "DLG000000" |  |
| 54 | `O54` |  } |  |
| 55 | `N55` |  } |  |

</details>
