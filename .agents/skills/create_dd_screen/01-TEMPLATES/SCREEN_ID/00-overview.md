# {{SCREEN_ID}} — {{SCREEN_TITLE}} · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `{{SCREEN_ID}}` |
| Module | `{{MODULE}}` |
| Route | `{{ROUTE}}` |
| Actor/role | {{ACTORS}} |
| DD status | Draft |
| Owner | {{OWNER}} |
| Version / last updated | 0.1 / {{DATE}} |
| Nguồn đối chiếu | {{SOURCES}} |

## 1. Mục tiêu & phạm vi
- Mục tiêu: {{GOAL}}
- In-scope: {{IN_SCOPE}}
- Out-of-scope: {{OUT_SCOPE}}

## 2. Use cases chính
| Use case | Actor | Kết quả |
|---|---|---|
| UC-01 | {{ACTORS}} | {{RESULT}} |

## 3. Precondition / Entry / Dependencies
- Điều kiện đầu vào: {{PRECONDITIONS}}
- Screen/API phụ thuộc: {{DEPENDENCIES}}
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Điều kiện | UI |
|---|---|---|
| Initial/Loading | {{LOAD_CONDITION}} | {{LOAD_UI}} |
| Success | {{SUCCESS_CONDITION}} | {{SUCCESS_UI}} |
| Empty | {{EMPTY_CONDITION}} | {{EMPTY_UI}} |
| Error | {{ERROR_CONDITION}} | {{ERROR_UI}} |

## 5. Luồng chính và hình ảnh
- Ảnh gốc: [screen-clean.png](images/screen-clean.png)
- Ảnh đánh số: [screen-numbered.png](images/screen-numbered.png)
- Luồng tóm tắt: {{MAIN_FLOW}}

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN [Q-01]`: {{QUESTION_AND_SOURCE}}
- {{DATE}} — Tạo DD bản nháp.
