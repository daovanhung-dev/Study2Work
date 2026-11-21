# {{SCREEN_ID}} — UI Elements

## 1. Quy tắc ảnh & mapping
- [Ảnh gốc](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)
- Marker `#N` trên ảnh → `{{SCREEN_ID}}-EL-NNN`. Một item lặp sử dụng một EL template.

## 2. Danh sách phần tử
| Marker | Element ID | Loại / tên | Dữ liệu / source | Tương tác (EV ID) |
|---|---|---|---|---|
| #1 | `{{SCREEN_ID}}-EL-001` | {{ELEMENT_TYPE}} / {{ELEMENT_NAME}} | {{BINDING}} | `{{SCREEN_ID}}-EV-001` |

## 3. Đặc tả từng element
### {{SCREEN_ID}}-EL-001 — {{ELEMENT_NAME}}
- Loại + vị trí/parent: {{TYPE_AND_LOCATION}}
- Visual: {{LABEL_ICON_LAYOUT}}
- Binding và source: {{BINDING_AND_SOURCE}}
- State: default {{DEFAULT}}; loading {{LOADING}}; disabled {{DISABLED}}; error {{ERROR}}
- Visible/enabled conditions: {{CONDITIONS}}
- Interaction: `{{SCREEN_ID}}-EV-001` — {{TRIGGER}}
- Accessibility/responsive: {{A11Y_RESPONSIVE}}

## 4. Conditional UI & state variations
- Loading: {{LOADING_ELEMENTS}}
- Empty: {{EMPTY_ELEMENTS}}
- Error: {{ERROR_ELEMENTS}}
- Modal/Toast (nếu có): {{OVERLAYS}}

## 5. Link
- [Events](02-events.md) · [Data Flow](03-data-flow.md) · [Tests](07-test-cases.md)
