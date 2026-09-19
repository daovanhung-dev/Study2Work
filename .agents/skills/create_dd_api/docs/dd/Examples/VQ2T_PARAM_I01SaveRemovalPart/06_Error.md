---
title: "Error"
order: 6
source_workbook: "【VQ2T-PARAM】API設計_I01_I01SaveRemovalPart_Ver1.0_VN 1.xlsx"
source_sheet: "4.Error"
dd_id: "I01SaveRemovalPart"
format: markdown
---

# Error

## Metadata kế thừa

| Thuộc tính | Giá trị | Công thức Excel nguồn |
|---|---|---|
| Project | `VQ2T-PARAM` | `=Overview!E1` |
| System | `設定管理` | `=Overview!H1` |
| Người tạo | `FPT AnNVK1` | `='Lịch sử'!C4` |
| Ngày tạo | `2026-04-09` | Giá trị trực tiếp |

## Giải thích

Các trường hợp lỗi của API.

## Error cases

| No | Category | Verify check | Tên item | Nội dung check | Error code | Error message ID | Remarks |
|---:|---|---|---|---|---|---|---|
| 1 | system error | `-` | `-` | Trường hợp lỗi truy cập DB | `9999` | `DLG000000` | |
| 2 | check quyền | `○` | `-` | Trường hợp user login không có quyền | `1000` | `SMES00005` | |
| 3 | Check bắt buộc | `○` | 拠点ID | Request data không có parameter `拠点ID` | `1001` | `DLG000003` | |
| 4 | Check bắt buộc | `○` | ラインID | Request data không có parameter `ラインID` | `1002` | `DLG000003` | |
| 5 | Check bắt buộc | `○` | 部門ID | Request data không có parameter `部門ID` | `1003` | `DLG000003` | |
| 6 | Check bắt buộc | `○` | 取外部品ID | Request data không có parameter `取外部品ID` | `1004` | `DLG000003` | |
| 6 | Check bắt buộc | `○` | プリセット名 | Request data không có parameter `プリセット名` | `1005` | `DLG000003` | |
| 7 | Check bắt buộc | `○` | ファイル名 | Request data không có parameter `ファイル名` | `1006` | `DLG000003` | |
| 8 | Check bắt buộc | `○` | 表示順 | Request data không có parameter `表示順` | `1007` | `DLG000003` | |
| 9 | Check bắt buộc | `○` | Danh sách 部品部位コード | Request data không có parameter `Danh sách 部品部位コード` | `1008` | `DLG000003` | |
| 10 | Check length | `○` | 拠点ID | `length(拠点ID) > 5` | `1009` | `DLG000003` | |
| 11 | Check length | `○` | ラインID | `length(ラインID) > 5` | `1010` | `DLG000003` | |
| 12 | Check length | `○` | 部門ID | `length(部門ID) > 3` | `1011` | `DLG000003` | |
| 13 | Check length | `○` | 取外部品ID | `length(取外部品ID) > 5` | `1012` | `DLG000003` | |
| 13 | Check length | `○` | プリセット名 | `length(プリセット名) > 50` | `1013` | `DLG000003` | |
| 14 | Check length | `○` | ファイル名 | `length(ファイル名) > 50` | `1014` | `DLG000003` | |
| 15 | Check length | `○` | 部品部位コード | Tồn tại phần tử trong danh sách có `length > 17` | `1015` | `DLG000003` | |
| 16 | Check format | `○` | 表示順 | Có `表示順` nhưng format không phải integer | `1016` | `DLG000003` | |
| 17 | Check giá trị hợp lệ | `○` | 表示順 | `表示順 > 999` | `1017` | `DLG000003` | |
| 18 | Check duplicate | `-` | `-` | Master đã đăng ký có `プリセット名` giống nhau | `1018` | `DLG000042` | Refer xử lý `4` |
| 19 | Check tồn tại | `-` | `-` | Master đã đăng ký không tồn tại thông tin part tháo ra | `1019` | `DLG000003` | Refer xử lý `6` |

---
## Phụ lục đối chiếu nguồn Excel
- Workbook nguồn: `【VQ2T-PARAM】API設計_I01_I01SaveRemovalPart_Ver1.0_VN 1.xlsx`
- Sheet nguồn: `4.Error`
- Dimension: `A1:BR32`
- Trạng thái: `visible`
- Số ô có dữ liệu/công thức: `172`
- Số vùng merge: `69`

<details>
<summary>Danh sách vùng merge</summary>

- `C25:F25`
- `G25:I25`
- `C17:F17`
- `G17:I17`
- `AX1:BA1`
- `A2:D2`
- `E2:G2`
- `H2:M2`
- `N2:S2`
- `T2:Y2`
- `AU1:AW1`
- `A1:D1`
- `E1:G1`
- `H1:AL1`
- `AM1:AO1`
- `AP1:AT1`
- `AU2:AW2`
- `Z2:AE2`
- `AF2:AL2`
- `AX2:BA2`
- `C11:F11`
- `G11:I11`
- `J11:N11`
- `O11:X11`
- `Y11:AA11`
- `G21:I21`
- `G22:I22`
- `O21:X21`
- `O29:X29`
- `O30:X30`
- `O28:X28`
- `AP2:AT2`
- `G13:I13`
- `G18:I18`
- `G19:I19`
- `G20:I20`
- `G16:I16`
- `AM2:AO2`
- `AB11:AF11`
- `AG11:BA11`
- `G12:I12`
- `G14:I14`
- `G15:I15`
- `C18:F18`
- `C19:F19`
- `C20:F20`
- `C21:F21`
- `C22:F22`
- `C12:F12`
- `C13:F13`
- `C14:F14`
- `C15:F15`
- `C16:F16`
- `C31:F31`
- `C32:F32`
- `G23:I23`
- `G24:I24`
- `G26:I26`
- `G27:I27`
- `C23:F23`
- `C24:F24`
- `G32:I32`
- `C28:F28`
- `C26:F26`
- `C27:F27`
- `G29:I29`
- `G30:I30`
- `G28:I28`
- `G31:I31`

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
| 2 | `N2` | Error |  |
| 2 | `AM2` | Người update |  |
| 2 | `AU2` | Ngày update |  |
| 4 | `B4` | Giải thích |  |
| 6 | `C6` | Các trường hợp lỗi của API |  |
| 11 | `B11` | № |  |
| 11 | `C11` | Category |  |
| 11 | `G11` | Verify check |  |
| 11 | `J11` | Tên item |  |
| 11 | `O11` | Nội dung check |  |
| 11 | `Y11` | Error code |  |
| 11 | `AB11` | Error message ID |  |
| 11 | `AG11` | Remarks |  |
| 12 | `B12` | 1 |  |
| 12 | `C12` | system error |  |
| 12 | `G12` | - |  |
| 12 | `J12` | - |  |
| 12 | `O12` | Trường hợp lỗi truy cập DB |  |
| 12 | `Y12` | 9999 |  |
| 12 | `AB12` | DLG000000 |  |
| 13 | `B13` | 2 |  |
| 13 | `C13` | check quyền |  |
| 13 | `G13` | ○ |  |
| 13 | `J13` | - |  |
| 13 | `O13` | Trường hợp user login không có quyền |  |
| 13 | `Y13` | 1000 |  |
| 13 | `AB13` | SMES00005 |  |
| 14 | `B14` | 3 |  |
| 14 | `C14` | Check bắt buộc |  |
| 14 | `G14` | ○ |  |
| 14 | `J14` | 拠点ID |  |
| 14 | `O14` | Trường hợp trong request data không có parameter [拠点ID] |  |
| 14 | `Y14` | 1001 |  |
| 14 | `AB14` | DLG000003 |  |
| 15 | `B15` | 4 |  |
| 15 | `C15` | Check bắt buộc |  |
| 15 | `G15` | ○ |  |
| 15 | `J15` | ラインID |  |
| 15 | `O15` | Trường hợp trong request data không có parameter [ラインID] |  |
| 15 | `Y15` | 1002 |  |
| 15 | `AB15` | DLG000003 |  |
| 16 | `B16` | 5 |  |
| 16 | `C16` | Check bắt buộc |  |
| 16 | `G16` | ○ |  |
| 16 | `J16` | 部門ID |  |
| 16 | `O16` | Trường hợp trong request data không có parameter [部門ID] |  |
| 16 | `Y16` | 1003 |  |
| 16 | `AB16` | DLG000003 |  |
| 17 | `B17` | 6 |  |
| 17 | `C17` | Check bắt buộc |  |
| 17 | `G17` | ○ |  |
| 17 | `J17` | 取外部品ID |  |
| 17 | `O17` | Trường hợp trong request data không có parameter [取外部品ID] |  |
| 17 | `Y17` | 1004 |  |
| 17 | `AB17` | DLG000003 |  |
| 18 | `B18` | 6 |  |
| 18 | `C18` | Check bắt buộc |  |
| 18 | `G18` | ○ |  |
| 18 | `J18` | プリセット名 |  |
| 18 | `O18` | Trường hợp trong request data không có parameter [プリセット名] |  |
| 18 | `Y18` | 1005 |  |
| 18 | `AB18` | DLG000003 |  |
| 19 | `B19` | 7 |  |
| 19 | `C19` | Check bắt buộc |  |
| 19 | `G19` | ○ |  |
| 19 | `J19` | ファイル名 |  |
| 19 | `O19` | Trường hợp trong request data không có parameter [ファイル名] |  |
| 19 | `Y19` | 1006 |  |
| 19 | `AB19` | DLG000003 |  |
| 20 | `B20` | 8 |  |
| 20 | `C20` | Check bắt buộc |  |
| 20 | `G20` | ○ |  |
| 20 | `J20` | 表示順 |  |
| 20 | `O20` | Trường hợp trong request data không có parameter [表示順] |  |
| 20 | `Y20` | 1007 |  |
| 20 | `AB20` | DLG000003 |  |
| 21 | `B21` | 9 |  |
| 21 | `C21` | Check bắt buộc |  |
| 21 | `G21` | ○ |  |
| 21 | `J21` | Danh sách 部品部位コード |  |
| 21 | `O21` | Trường hợp trong request data không có parameter [Danh sách 部品部位コード] |  |
| 21 | `Y21` | 1008 |  |
| 21 | `AB21` | DLG000003 |  |
| 22 | `B22` | 10 |  |
| 22 | `C22` | Check length |  |
| 22 | `G22` | ○ |  |
| 22 | `J22` | 拠点ID |  |
| 22 | `O22` | Trường hợp length của parameter [拠点ID] trong request data > 5 |  |
| 22 | `Y22` | 1009 |  |
| 22 | `AB22` | DLG000003 |  |
| 23 | `B23` | 11 |  |
| 23 | `C23` | Check length |  |
| 23 | `G23` | ○ |  |
| 23 | `J23` | ラインID |  |
| 23 | `O23` | Trường hợp length của parameter [ラインID] trong request data > 5 |  |
| 23 | `Y23` | 1010 |  |
| 23 | `AB23` | DLG000003 |  |
| 24 | `B24` | 12 |  |
| 24 | `C24` | Check length |  |
| 24 | `G24` | ○ |  |
| 24 | `J24` | 部門ID |  |
| 24 | `O24` | Trường hợp length của parameter [部門ID] trong request data > 3 |  |
| 24 | `Y24` | 1011 |  |
| 24 | `AB24` | DLG000003 |  |
| 25 | `B25` | 13 |  |
| 25 | `C25` | Check length |  |
| 25 | `G25` | ○ |  |
| 25 | `J25` | 取外部品ID |  |
| 25 | `O25` | Trường hợp length của parameter [取外部品ID] trong request data > 5 |  |
| 25 | `Y25` | 1012 |  |
| 25 | `AB25` | DLG000003 |  |
| 26 | `B26` | 13 |  |
| 26 | `C26` | Check length |  |
| 26 | `G26` | ○ |  |
| 26 | `J26` | プリセット名 |  |
| 26 | `O26` | Trường hợp length của parameter [プリセット名] trong request data > 50 |  |
| 26 | `Y26` | 1013 |  |
| 26 | `AB26` | DLG000003 |  |
| 27 | `B27` | 14 |  |
| 27 | `C27` | Check length |  |
| 27 | `G27` | ○ |  |
| 27 | `J27` | ファイル名 |  |
| 27 | `O27` | Trường hợp length của parameter [ファイル名] trong request data > 50 |  |
| 27 | `Y27` | 1014 |  |
| 27 | `AB27` | DLG000003 |  |
| 28 | `B28` | 15 |  |
| 28 | `C28` | Check length |  |
| 28 | `G28` | ○ |  |
| 28 | `J28` | 部品部位コード |  |
| 28 | `O28` | Trường hợp tồn tại phần tử [部品部位コード] trong [Danh sách 部品部位コード] của request data có lenth > 17 |  |
| 28 | `Y28` | 1015 |  |
| 28 | `AB28` | DLG000003 |  |
| 29 | `B29` | 16 |  |
| 29 | `C29` | Check format |  |
| 29 | `G29` | ○ |  |
| 29 | `J29` | 表示順 |  |
| 29 | `O29` | Trường hợp trong request data có thông tin [表示順] nhưng format không phải integer |  |
| 29 | `Y29` | 1016 |  |
| 29 | `AB29` | DLG000003 |  |
| 30 | `B30` | 17 |  |
| 30 | `C30` | Check giá trị hợp lệ |  |
| 30 | `G30` | ○ |  |
| 30 | `J30` | 表示順 |  |
| 30 | `O30` | Trường hợp thông tin [表示順] trong request data có giá trị > 999 |  |
| 30 | `Y30` | 1017 |  |
| 30 | `AB30` | DLG000003 |  |
| 31 | `B31` | 18 |  |
| 31 | `C31` | Check duplicate |  |
| 31 | `G31` | - |  |
| 31 | `J31` | - |  |
| 31 | `O31` | Trường hợp trong master đã đăng ký có tồn tại [プリセット名] giống nhau |  |
| 31 | `Y31` | 1018 |  |
| 31 | `AB31` | DLG000042 |  |
| 31 | `AG31` | Refer xử lý 4. |  |
| 32 | `B32` | 19 |  |
| 32 | `C32` | Check tồn tại |  |
| 32 | `G32` | - |  |
| 32 | `J32` | - |  |
| 32 | `O32` | Trường hợp trong master đã đăng ký không tồn tại thông tin part tháo ra |  |
| 32 | `Y32` | 1019 |  |
| 32 | `AB32` | DLG000003 |  |
| 32 | `AG32` | Refer xử lý 6. |  |

</details>
