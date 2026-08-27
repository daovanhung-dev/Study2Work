---
title: "setting_removal_parts_insert"
order: 9
source_workbook: "【VQ2T-PARAM】API設計_I01_I01SaveRemovalPart_Ver1.0_VN 1.xlsx"
source_sheet: "setting_removal_parts_insert"
dd_id: "I01SaveRemovalPart"
format: markdown
---
# setting_removal_parts_insert

## Metadata

| Thuộc tính | Giá trị |
|---|---|
| Project | `VQ2T-PARAM` |
| System | `設定管理` |
| Loại tài liệu | `Detail Design` |
| Phân loại | `User interface` |
| Section | `Định nghĩa table` |
| Operation | `Đăng ký DB` |
| Physical table | `setting_removal_parts` |
| Logical table | `取外部品マスタ` |
| Người tạo | `FPT AnNVK1` |
| Ngày tạo | `2026-04-09` |

## Column mapping

| No | Item ID | Item name | Kiểu | Độ dài | Dấu phẩy thập phân | Bắt buộc | Main key | Nội dung setting |
|---:|---|---|---|---:|---:|---:|---:|---|
| 1 | `parts_list_id` | 取外部品ID | `character varying` | 5 |  | Y | ● | nextval('setting_removal_parts_seq') |
| 2 | `sdiknr_no` | 世代管理番号 | `integer` | - |  | Y | ● | 1 |
| 3 | `seiskjy_id` | 拠点ID | `character varying` | 5 |  |  |  | Param['seiskjy_id'] |
| 4 | `sisnlin_id` | ラインID | `character varying` | 5 |  |  |  | Param['seiskjy_id'] |
| 5 | `bmn_id` | 部門ID | `character varying` | 3 |  |  |  | Param['bmn_id'] |
| 6 | `parts_list_nm` | プリセット名 | `character varying` | 50 |  |  |  | Param['parts_list_nm'] |
| 7 | `file_nm` | ファイル名 | `character varying` | 50 |  |  |  | Param['file_nm'] |
| 8 | `sksi_dt` | 作成日時 | `timestamp with time zone` | - |  |  |  | NOW() |
| 9 | `sksiprg_cd` | 作成者コード | `character varying` | 32 |  |  |  | Param['sksiprg_cd'] |
| 10 | `sishkshn_dt` | 更新日時 | `timestamp with time zone` | - |  |  |  | NOW() |
| 11 | `sishkshnprg_cd` | 更新者コード | `character varying` | 32 |  |  |  | Param['sishkshnprg_cd'] |
| 12 | `skj_flg` | 削除フラグ | `character varying` | 1 |  |  |  | '0' |
| 13 | `hyjjn_no` | 表示順 | `integer` | - |  |  |  | Param['hyjjn_no'] |

---
## Phụ lục đối chiếu nguồn Excel
- Workbook nguồn: `【VQ2T-PARAM】API設計_I01_I01SaveRemovalPart_Ver1.0_VN 1.xlsx`
- Sheet nguồn: `setting_removal_parts_insert`
- Dimension: `A1:BR20`
- Trạng thái: `visible`
- Số ô có dữ liệu/công thức: `111`
- Số vùng merge: `18`

<details>
<summary>Danh sách vùng merge</summary>

- `A1:D1`
- `E1:G1`
- `H1:AL1`
- `AM1:AO1`
- `A2:D2`
- `E2:G2`
- `H2:M2`
- `N2:S2`
- `T2:Y2`
- `AU1:AW1`
- `AU2:AW2`
- `AX2:BA2`
- `AX1:BA1`
- `Z2:AE2`
- `AF2:AL2`
- `AM2:AO2`
- `AP2:AT2`
- `AP1:AT1`

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
| 1 | `AX1` | 46121 |  |
| 2 | `A2` | Loại tài liệu |  |
| 2 | `E2` | Detail Design |  |
| 2 | `H2` | User interface |  |
| 2 | `N2` | Định nghĩa table |  |
| 2 | `T2` | Đăng ký DB |  |
| 2 | `AM2` | Người update |  |
| 2 | `AU2` | Ngày update |  |
| 4 | `A4` | № |  |
| 4 | `B4` | Tên table |  |
| 5 | `B5` | SB |  |
| 5 | `S5` | Độ dài |  |
| 5 | `T5` | Dấu phẩy thập phân |  |
| 5 | `U5` | Bắt buộc |  |
| 5 | `V5` | Main key |  |
| 5 | `W5` | Nội dung setting |  |
| 6 | `B6` | № |  |
| 6 | `C6` | Item ID |  |
| 6 | `I6` | Item name |  |
| 6 | `O6` | Kiểu |  |
| 7 | `A7` | 1 |  |
| 7 | `B7` | setting_removal_parts |  |
| 7 | `I7` | 取外部品マスタ |  |
| 8 | `B8` | 1 |  |
| 8 | `C8` | parts_list_id |  |
| 8 | `I8` | 取外部品ID |  |
| 8 | `O8` | character varying |  |
| 8 | `S8` | 5 |  |
| 8 | `U8` | Y |  |
| 8 | `V8` | ● |  |
| 8 | `W8` | nextval('setting_removal_parts_seq') |  |
| 9 | `B9` | 2 |  |
| 9 | `C9` | sdiknr_no |  |
| 9 | `I9` | 世代管理番号 |  |
| 9 | `O9` | integer |  |
| 9 | `S9` | - |  |
| 9 | `U9` | Y |  |
| 9 | `V9` | ● |  |
| 9 | `W9` | 1 |  |
| 10 | `B10` | 3 |  |
| 10 | `C10` | seiskjy_id |  |
| 10 | `I10` | 拠点ID |  |
| 10 | `O10` | character varying |  |
| 10 | `S10` | 5 |  |
| 10 | `W10` | Param['seiskjy_id'] |  |
| 11 | `B11` | 4 |  |
| 11 | `C11` | sisnlin_id |  |
| 11 | `I11` | ラインID |  |
| 11 | `O11` | character varying |  |
| 11 | `S11` | 5 |  |
| 11 | `W11` | Param['seiskjy_id'] |  |
| 12 | `B12` | 5 |  |
| 12 | `C12` | bmn_id |  |
| 12 | `I12` | 部門ID |  |
| 12 | `O12` | character varying |  |
| 12 | `S12` | 3 |  |
| 12 | `W12` | Param['bmn_id'] |  |
| 13 | `B13` | 6 |  |
| 13 | `C13` | parts_list_nm |  |
| 13 | `I13` | プリセット名 |  |
| 13 | `O13` | character varying |  |
| 13 | `S13` | 50 |  |
| 13 | `W13` | Param['parts_list_nm'] |  |
| 14 | `B14` | 7 |  |
| 14 | `C14` | file_nm |  |
| 14 | `I14` | ファイル名 |  |
| 14 | `O14` | character varying |  |
| 14 | `S14` | 50 |  |
| 14 | `W14` | Param['file_nm'] |  |
| 15 | `B15` | 8 |  |
| 15 | `C15` | sksi_dt |  |
| 15 | `I15` | 作成日時 |  |
| 15 | `O15` | timestamp with time zone |  |
| 15 | `S15` | - |  |
| 15 | `W15` | NOW() |  |
| 16 | `B16` | 9 |  |
| 16 | `C16` | sksiprg_cd |  |
| 16 | `I16` | 作成者コード |  |
| 16 | `O16` | character varying |  |
| 16 | `S16` | 32 |  |
| 16 | `W16` | Param['sksiprg_cd'] |  |
| 17 | `B17` | 10 |  |
| 17 | `C17` | sishkshn_dt |  |
| 17 | `I17` | 更新日時 |  |
| 17 | `O17` | timestamp with time zone |  |
| 17 | `S17` | - |  |
| 17 | `W17` | NOW() |  |
| 18 | `B18` | 11 |  |
| 18 | `C18` | sishkshnprg_cd |  |
| 18 | `I18` | 更新者コード |  |
| 18 | `O18` | character varying |  |
| 18 | `S18` | 32 |  |
| 18 | `W18` | Param['sishkshnprg_cd'] |  |
| 19 | `B19` | 12 |  |
| 19 | `C19` | skj_flg |  |
| 19 | `I19` | 削除フラグ |  |
| 19 | `O19` | character varying |  |
| 19 | `S19` | 1 |  |
| 19 | `W19` | '0' |  |
| 20 | `B20` | 13 |  |
| 20 | `C20` | hyjjn_no |  |
| 20 | `I20` | 表示順 |  |
| 20 | `O20` | integer |  |
| 20 | `S20` | - |  |
| 20 | `W20` | Param['hyjjn_no'] |  |

</details>
