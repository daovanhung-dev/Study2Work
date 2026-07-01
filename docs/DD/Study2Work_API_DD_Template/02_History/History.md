# 02. History – {{API_NAME}}

> **Mục đích:** duy trì lịch sử thay đổi có thể audit cho tài liệu DD và API contract. Mọi thay đổi ảnh hưởng client, database, rule nghiệp vụ, quyền, error code, performance hoặc bảo mật phải có một dòng history.

---

## 1. Document control

| Thuộc tính | Giá trị |
|---|---|
| Project | `Study2Work` |
| API business code | `{{API_CODE}}` |
| API name | `{{API_NAME}}` |
| Current document version | `{{DOCUMENT_VERSION}}` |
| Current API contract version | `v{{API_VERSION}}` |
| Status | `Draft / In Review / Approved / Deprecated` |
| Repository path | `{{REPOSITORY_PATH}}` |
| Source of truth | `Git repository / Docs repository / Wiki` |
| Created by | `{{CREATED_BY}}` |
| Created at (UTC) | `{{CREATED_AT}}` |
| Last changed by | `{{LAST_CHANGED_BY}}` |
| Last changed at (UTC) | `{{UPDATED_AT}}` |
| Review cadence | `{{REVIEW_CADENCE}}` |

## 2. Versioning policy

| Change type | Bump | Ví dụ | Required action |
|---|---|---|---|
| Editorial | Patch document, ví dụ `1.0.1` | Sửa câu chữ / link / typo, không đổi behavior. | Update History, không cần client migration. |
| Non-breaking contract change | Minor, ví dụ `1.1.0` | Thêm optional field response, thêm endpoint query optional. | Release note, update schema/test. |
| Behavior/rule change | Minor hoặc Major theo tác động | Thay đổi scoring, eligibility, sorting default. | Ghi rõ affected scenarios/client. |
| Breaking contract change | Major, ví dụ `2.0.0` | Đổi/remove field required, đổi semantic HTTP/error code, endpoint/method. | Migration plan, deprecation date, compatibility window. |
| Security hotfix | Patch + security label | Siết authorization/masking, rotate scheme. | Security review, incident/change record. |
| Performance/operation change | Patch/Minor | Đổi rate limit, async behavior, timeout/cache. | SLO/monitoring impact, communication nếu client bị ảnh hưởng. |

## 3. Change log

| Version | Date (UTC) | Change type | Area changed | Summary | Reason / ticket | Breaking? | Client action | DB / migration impact | Author | Reviewer | Approver |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `{{DOC_VERSION}}` | `{{YYYY-MM-DD}}` | `Initial / Editorial / Non-breaking / Behavior / Breaking / Security` | `Overview / Request / Response / DataMapping / Error` | `{{CHANGE_SUMMARY}}` | `{{TICKET_OR_REASON}}` | `Yes / No` | `{{CLIENT_ACTION}}` | `{{MIGRATION_OR_NA}}` | `{{AUTHOR}}` | `{{REVIEWER}}` | `{{APPROVER}}` |
| `1.0.0` | `{{INITIAL_APPROVAL_DATE}}` | `Initial` | `All` | Initial approved API DD. | `{{TICKET}}` | `No` | `N/A` | `{{MIGRATION_OR_NA}}` | `{{AUTHOR}}` | `{{REVIEWER}}` | `{{APPROVER}}` |

### 3.1. Change detail record

> Thêm một khối này cho mỗi thay đổi quan trọng, breaking, security, migration hoặc khi review cần thêm context.

#### `CHG-{{NNN}} – {{SHORT_CHANGE_TITLE}}`

| Mục | Nội dung |
|---|---|
| Change date (UTC) | `{{DATE_TIME}}` |
| Version before → after | `{{OLD_VERSION}} → {{NEW_VERSION}}` |
| Change owner | `{{OWNER}}` |
| Category | `{{CATEGORY}}` |
| Related ticket / PR / incident | `{{REFERENCE}}` |
| Affected consumers | `{{WEB_STUDENT / MOBILE / WEB_MENTOR / ...}}` |
| Backward compatible? | `Yes / No / Partial` |
| Effective date | `{{EFFECTIVE_DATE}}` |
| Deprecation deadline | `{{DEPRECATION_DATE_OR_NA}}` |
| Rollback owner / method | `{{ROLLBACK_OWNER_AND_METHOD}}` |

**What changed**

- `{{DETAILED_CHANGE_1}}`
- `{{DETAILED_CHANGE_2}}`

**Why it changed**

`{{BUSINESS_OR_TECHNICAL_REASON}}`

**Compatibility impact**

`{{COMPATIBILITY_IMPACT}}`

**Required deployment order**

1. `{{STEP_1}}`
2. `{{STEP_2}}`
3. `{{STEP_3}}`

**Verification after deployment**

- `{{VERIFICATION_1}}`
- `{{VERIFICATION_2}}`

## 4. Decision log / ADR references

| Decision ID | Date | Decision | Options considered | Chosen rationale | Consequence | Owner | Reference |
|---|---|---|---|---|---|---|---|
| `ADR-{{API_CODE}}-001` | `{{YYYY-MM-DD}}` | `{{DECISION}}` | `{{OPTIONS}}` | `{{RATIONALE}}` | `{{CONSEQUENCE}}` | `{{OWNER}}` | `{{ADR_OR_TICKET_LINK}}` |

## 5. Review and approval trail

| Stage | Role | Person | Date (UTC) | Result | Review notes / required actions |
|---|---|---|---|---|---|
| Business review | Product Owner / BA | `{{NAME}}` | `{{DATE}}` | `Pending / Approved / Rejected` | `{{NOTES}}` |
| Domain review | Tech Lead / Architect | `{{NAME}}` | `{{DATE}}` | `Pending / Approved / Rejected` | `{{NOTES}}` |
| API contract review | Backend + Frontend/Mobile | `{{NAME}}` | `{{DATE}}` | `Pending / Approved / Rejected` | `{{NOTES}}` |
| Data/security review | DBA / Security | `{{NAME}}` | `{{DATE}}` | `Pending / Approved / Rejected` | `{{NOTES}}` |
| Test review | QA | `{{NAME}}` | `{{DATE}}` | `Pending / Approved / Rejected` | `{{NOTES}}` |
| Final approval | Designated approver | `{{NAME}}` | `{{DATE}}` | `Pending / Approved / Rejected` | `{{NOTES}}` |

## 6. Deprecation and migration plan

> Chỉ điền khi API/field/behavior cũ bị thay thế hoặc loại bỏ.

| Mục | Nội dung |
|---|---|
| Deprecated item | `{{ENDPOINT_OR_FIELD_OR_ERROR_CODE}}` |
| Replacement | `{{NEW_ENDPOINT_OR_FIELD_OR_BEHAVIOR}}` |
| First deprecated in | `{{VERSION_AND_DATE}}` |
| Removal date | `{{DATE}}` |
| Affected consumer list | `{{CONSUMERS}}` |
| Migration steps | `{{MIGRATION_STEPS}}` |
| Compatibility behavior | `{{DUAL_READ_DUAL_WRITE_ALIAS_OR_NA}}` |
| Telemetry to verify migration | `{{METRIC_OR_LOG_QUERY}}` |
| Communication owner | `{{OWNER}}` |
| Rollback plan | `{{ROLLBACK_PLAN}}` |

## 7. Open items and risks

| ID | Type | Description | Impact | Owner | Target date | Status | Decision needed |
|---|---|---|---|---|---|---|---|
| `OPEN-{{NNN}}` | `Question / Risk / Dependency / Technical debt` | `{{DESCRIPTION}}` | `{{IMPACT}}` | `{{OWNER}}` | `{{DATE}}` | `Open / Resolved / Accepted` | `{{DECISION_OR_ACTION}}` |

## 8. History quality gate

- [ ] Initial version identifies author, reviewer, approver, date and source ticket.
- [ ] Every contract/rule/security/data behavior change has a line in Change log.
- [ ] Breaking changes contain effective date, migration, release/rollback and client impact.
- [ ] Deprecation never removes old API/field without a tracked compatibility plan.
- [ ] Decision log captures non-obvious architecture/business choices.
- [ ] Current status/version is consistent across Overview, OpenAPI, release notes and source code.
