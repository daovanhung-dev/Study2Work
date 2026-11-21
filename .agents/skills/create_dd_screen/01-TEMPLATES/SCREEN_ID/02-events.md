# {{SCREEN_ID}} — Events (đặc tả xử lý)

## 1. Event index
| ID | Event | Trigger | Element | API | Test |
|---|---|---|---|---|---|
| `{{SCREEN_ID}}-EV-001` | {{EVENT_NAME}} | {{TRIGGER}} | `{{SCREEN_ID}}-EL-001` | `{{SCREEN_ID}}-API-001` | `{{SCREEN_ID}}-TC-001` |

## 2. {{SCREEN_ID}}-EV-001 — {{EVENT_NAME}}
**Mục tiêu:** {{EVENT_GOAL}}

**Trigger:** {{TRIGGER}}

**Preconditions / Guard:** {{GUARDS}}

**Input & nguồn:**
| Dữ liệu | Kiểu | Lấy từ đâu | Default |
|---|---|---|---|
| {{INPUT}} | {{TYPE}} | {{SOURCE}} | {{DEFAULT}} |

**Quy trình từng bước:**
1. {{STEP_1}}
2. {{STEP_2}}
3. {{STEP_3}}
4. {{STEP_4}}

**API:** `{{SCREEN_ID}}-API-001` — chi tiết tại [API Integration](04-api-integration.md).

**Data mapping/state:** {{DATA_EFFECTS}} — xem [Data Flow](03-data-flow.md).

**UI sau xử lý:** {{UI_EFFECTS}}

**Điều hướng:** {{NAV_EFFECTS}} — xem [Navigation](06-navigation.md).

**Lỗi/ngoại lệ:**
- Input invalid: {{INPUT_ERROR}}
- API timeout/network: {{NETWORK_ERROR}}
- Business error/permission: {{BUSINESS_ERROR}}
- Duplicate/race: {{RACE_ERROR}}

**Rules:** `{{SCREEN_ID}}-BR-001` · **Tests:** `{{SCREEN_ID}}-TC-001`.

> Tạo một section theo format này cho **mọi** event (lifecycle, click, input, submit, retry, back...).
