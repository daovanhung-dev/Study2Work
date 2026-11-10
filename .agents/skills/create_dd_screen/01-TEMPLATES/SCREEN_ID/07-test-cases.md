# {{SCREEN_ID}} — Test Cases

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `{{SCREEN_ID}}-TC-001` | {{TEST_TYPE}} | `{{SCREEN_ID}}-EV-001` | `{{SCREEN_ID}}-BR-001` | P1 |

## 2. {{SCREEN_ID}}-TC-001 — {{TEST_NAME}}
- **Mục tiêu:** {{TEST_PURPOSE}}
- **Precondition:** {{TEST_PRECONDITION}}
- **Mock/test data:** {{TEST_DATA}}
- **Steps:**
  1. {{TEST_STEP_1}}
  2. {{TEST_STEP_2}}
- **Expected UI/state:** {{EXPECTED_UI}}
- **Expected API/data:** {{EXPECTED_API}}
- **Failure / edge assertion:** {{EDGE_ASSERTION}}
- **References:** `{{SCREEN_ID}}-EV-001`, `{{SCREEN_ID}}-BR-001`, `{{SCREEN_ID}}-API-001`

## 3. Coverage tối thiểu
- [ ] Initial load success
- [ ] Input validation / boundary
- [ ] Empty result
- [ ] API error, timeout, retry
- [ ] Unauthorized/forbidden (nếu có)
- [ ] Duplicate submit / race / stale response (nếu có)
- [ ] Navigation / deep link / back
