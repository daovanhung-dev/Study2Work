# 01. Overview – {{API_NAME}}

> **Mục đích:** chốt toàn bộ danh tính, phạm vi, hợp đồng cấp cao, actor/quyền, dependency và tiêu chí vận hành của API. `Overview` phải cho người đọc biết API này **có tồn tại để làm gì**, **ai gọi**, **khi nào được gọi**, **được phép làm gì**, **ảnh hưởng dữ liệu nào**.

---

## 1. Document metadata

| Thuộc tính | Giá trị |
|---|---|
| Project | `Study2Work` |
| API document ID | `DD-API-{{MODULE_CODE}}-{{ACTION}}-{{NNN}}` |
| API business code | `{{MODULE_CODE}}-{{ACTION}}-{{NNN}}` |
| API name | `{{API_NAME}}` |
| API version | `v{{API_VERSION}}` |
| Document version | `{{DOCUMENT_VERSION}}` |
| Document status | `Draft / In Review / Approved / Deprecated` |
| Module | `{{MODULE_NAME}}` |
| Bounded context | `{{BOUNDED_CONTEXT}}` |
| Sub-module / Feature | `{{SUB_MODULE_OR_FEATURE}}` |
| Owner team | `{{OWNER_TEAM}}` |
| Technical owner | `{{TECHNICAL_OWNER}}` |
| Business owner | `{{BUSINESS_OWNER}}` |
| Reviewer / Approver | `{{REVIEWER}} / {{APPROVER}}` |
| Created at (UTC) | `{{CREATED_AT}}` |
| Last updated at (UTC) | `{{UPDATED_AT}}` |
| Related release / epic / ticket | `{{TRACKING_REFERENCE}}` |

## 2. API identity and protocol

| Thuộc tính | Giá trị | Quy tắc / ghi chú |
|---|---|---|
| HTTP method | `{{HTTP_METHOD}}` | `GET`, `POST`, `PUT`, `PATCH`, `DELETE`... |
| Endpoint | `/api/v{{API_VERSION}}/{{RESOURCE_PATH}}` | Không chứa base domain. |
| API visibility | `Public / Authenticated / Internal / Admin / Partner` | Quyết định logging/rate limit/authorization. |
| Base URL by environment | `{{DEV_URL}}`, `{{STAGING_URL}}`, `{{PROD_URL}}` | Không ghi secret. |
| Content-Type | `application/json; charset=utf-8` | Đổi khi upload/download multipart/binary. |
| Accept | `application/json` | Nêu versioned media type nếu có. |
| Authentication | `None / Bearer JWT / OAuth callback / API key / mTLS` | Mô tả token/cookie/header tại `Request`. |
| Authorization policy | `{{POLICY_NAME}}` | Ví dụ `StudentOwnSubmissionPolicy`. |
| Required roles | `{{ROLES}}` | Ví dụ `Student`, `Mentor`, `Admin`. |
| Required permissions | `{{PERMISSIONS}}` | Ví dụ `assignment.submission.create`. |
| Data classification | `Public / Internal / PII / Sensitive` | Đánh giá toàn payload. |
| Idempotency | `Required / Optional / Not applicable` | Nêu header/key/TTL nếu required. |
| Rate limit | `{{RATE_LIMIT}}` | Ví dụ `30 requests/minute/user`. |
| Timeout target | `{{TIMEOUT_MS}} ms` | Chỉ timeout API sync; background job phải có SLA riêng. |
| Cache policy | `No cache / Private / Shared / {{CACHE_KEY}}` | Nêu TTL/invalidation nếu áp dụng. |
| Transaction expectation | `Read-only / Single transaction / Saga / Async workflow` | Chi tiết ở `DataMapping`. |

## 3. Business overview

### 3.1. Business purpose

`{{BUSINESS_PURPOSE}}`

Mô tả bằng 3–6 câu, trả lời đầy đủ:

1. API giải quyết hành vi nghiệp vụ nào trong hành trình `Learn → Practice → Evaluate → Build Portfolio → Connect Employer`?
2. Đối tượng nào nhận giá trị từ API?
3. API tạo/đổi/truy vấn artifact nghiệp vụ nào?
4. Kết quả thành công được dùng tiếp ở màn hình/flow nào?
5. API không có trách nhiệm làm điều gì?

### 3.2. Business outcome and success condition

| Nội dung | Mô tả |
|---|---|
| Outcome mong muốn | `{{EXPECTED_BUSINESS_OUTCOME}}` |
| Điều kiện thành công | `{{SUCCESS_CRITERIA}}` |
| Artifact tạo/cập nhật | `{{PRIMARY_BUSINESS_ARTIFACT}}` |
| Data source chính | `{{SOURCE_OF_TRUTH}}` |
| Derived/snapshot data | `{{DERIVED_OR_SNAPSHOT_DATA}}` |
| Event/notification phát sinh | `{{DOMAIN_EVENT_OR_NOTIFICATION}}` |
| UI/consumer nhận kết quả | `{{TARGET_SCREEN_OR_CONSUMER}}` |

### 3.3. Actor, caller and trigger

| Thuộc tính | Giá trị | Chi tiết |
|---|---|---|
| Primary actor | `{{PRIMARY_ACTOR}}` | `Guest`, `Student`, `Mentor`, `Employer`, `Admin`, System. |
| Secondary actor | `{{SECONDARY_ACTOR}}` | Người/Service bị ảnh hưởng hoặc nhận notification. |
| Technical caller | `{{CALLER_APP}}` | `web-student`, `web-mentor`, `web-employer`, `web-admin`, `mobile-app`, backend job... |
| Trigger | `{{TRIGGER}}` | Hành động UI, scheduler, webhook, event. |
| Frequency / volume assumption | `{{TRAFFIC_ASSUMPTION}}` | Dùng để chọn cache/rate limit/query strategy. |
| Synchronous result required? | `Yes / No` | Nếu `No`, mô tả `202 Accepted`, jobId và polling/webhook. |

### 3.4. Preconditions, postconditions and invariants

| Loại | Điều kiện | Owner kiểm tra | Nếu không thỏa |
|---|---|---|---|
| Precondition | `{{PRECONDITION_1}}` | `{{LAYER_OR_COMPONENT}}` | `{{ERROR_CODE}}` |
| Precondition | `{{PRECONDITION_2}}` | `{{LAYER_OR_COMPONENT}}` | `{{ERROR_CODE}}` |
| Domain invariant | `{{INVARIANT_1}}` | Domain service / aggregate | `{{ERROR_CODE}}` |
| Authorization condition | `{{AUTHORIZATION_CONDITION}}` | Guard / policy | `{{ERROR_CODE}}` |
| Postcondition | `{{POSTCONDITION_1}}` | Service / transaction | N/A |
| Postcondition | `{{POSTCONDITION_2}}` | Async handler / outbox | N/A |

> Không ghi chung chung “user có quyền”. Viết điều kiện kiểm tra cụ thể, ví dụ: `Mentor chỉ được review assignment_submission khi mentorId được phân công cho class/team chứa submission đó`.

## 4. Scope

### 4.1. In scope

- `{{IN_SCOPE_ITEM_1}}`
- `{{IN_SCOPE_ITEM_2}}`
- `{{IN_SCOPE_ITEM_3}}`

### 4.2. Out of scope

- `{{OUT_OF_SCOPE_ITEM_1}}`
- `{{OUT_OF_SCOPE_ITEM_2}}`

### 4.3. Assumptions and constraints

| ID | Assumption / constraint | Tác động nếu sai | Owner / mitigation |
|---|---|---|---|
| `ASM-01` | `{{ASSUMPTION_OR_CONSTRAINT}}` | `{{IMPACT}}` | `{{OWNER_AND_MITIGATION}}` |

## 5. Functional references and traceability

| Loại tài liệu / artefact | ID / path | Mối liên hệ |
|---|---|---|
| Product / Requirement | `{{REQUIREMENT_ID}}` | Nguồn yêu cầu. |
| Use case | `{{UC_ID}}` | Use case mà API phục vụ. |
| Activity diagram | `{{ACTIVITY_ID_OR_PATH}}` | Luồng nghiệp vụ cấp process. |
| Sequence diagram | `{{SEQUENCE_ID_OR_PATH}}` | Tương tác runtime giữa component. |
| Domain aggregate | `{{AGGREGATE_OR_DOMAIN_ENTITY}}` | Aggregate/invariant sở hữu nghiệp vụ. |
| Business rule catalog | `{{BR_IDS}}` | Rule phải được enforce. |
| Permission matrix | `{{PERMISSION_MATRIX_REFERENCE}}` | Role/permission source. |
| ERD / table design | `{{ERD_REFERENCE}}` | Source of truth dữ liệu. |
| OpenAPI / Swagger | `{{OPENAPI_OPERATION_ID}}` | Contract machine-readable. |
| Backend source expected | `{{CONTROLLER_SERVICE_DTO}}` | Controller/service/DTO dự kiến. |
| Test suite | `{{TEST_REFERENCE}}` | Unit/integration/e2e coverage. |

## 6. Impacted components and dependencies

### 6.1. Internal components

| Layer / component | Tên dự kiến | Trách nhiệm trong API | Sync / Async |
|---|---|---|---|
| Controller / handler | `{{CONTROLLER}}` | Parse transport input, call use case, map HTTP response. | Sync |
| DTO / schema | `{{REQUEST_DTO}}`, `{{RESPONSE_DTO}}` | Syntax validation / serialization. | Sync |
| Application service | `{{APPLICATION_SERVICE}}` | Orchestrate use case. | Sync |
| Domain service / aggregate | `{{DOMAIN_SERVICE_OR_AGGREGATE}}` | Enforce business invariant. | Sync |
| Repository / read model | `{{REPOSITORY_OR_QUERY_SERVICE}}` | Persist/query data. | Sync |
| Cache | `{{CACHE_COMPONENT}}` | Cache lookup/invalidation. | Sync |
| Event / job handler | `{{EVENT_OR_JOB_HANDLER}}` | Non-critical follow-up work. | Async |

### 6.2. External dependencies

| Dependency | Mục đích | Protocol | Timeout | Failure policy | Data shared |
|---|---|---|---|---|---|
| `{{EXTERNAL_SERVICE}}` | `{{PURPOSE}}` | `HTTP/gRPC/Queue/Storage` | `{{TIMEOUT}}` | `Fail fast / fallback / async retry` | `{{DATA_CLASSIFICATION}}` |

## 7. Data impact summary

| Data object / table | Operation | Ownership | Lý do truy cập | PII/Sensitive? |
|---|---|---|---|---|
| `{{TABLE_OR_READ_MODEL_1}}` | `READ` | `{{CONTEXT_OWNER}}` | `{{READ_PURPOSE}}` | `{{CLASSIFICATION}}` |
| `{{TABLE_OR_READ_MODEL_2}}` | `INSERT / UPDATE / DELETE` | `{{CONTEXT_OWNER}}` | `{{WRITE_PURPOSE}}` | `{{CLASSIFICATION}}` |
| `audit_log` | `INSERT` | Platform | Audit action quan trọng. | Internal |

> Chi tiết cột, predicate, transaction, repository method và source/destination mapping bắt buộc nằm trong `05_DataMapping/DataMapping.md`.

## 8. Non-functional requirements

| Khía cạnh | Requirement | Cách đo / acceptance criteria |
|---|---|---|
| Performance | `{{PERFORMANCE_TARGET}}` | Ví dụ p95 < 500 ms ở {{RPS}} RPS. |
| Availability | `{{AVAILABILITY_TARGET}}` | Ví dụ graceful degradation khi AI service unavailable. |
| Consistency | `{{CONSISTENCY_RULE}}` | Strong/eventual; read-after-write expectation. |
| Concurrency | `{{CONCURRENCY_RULE}}` | Optimistic version / unique constraint / row lock. |
| Security | `{{SECURITY_REQUIREMENT}}` | RBAC, ownership, masking, encryption. |
| Observability | `{{OBSERVABILITY_REQUIREMENT}}` | traceId, metric, log checkpoint, dashboard. |
| Accessibility / i18n | `{{CLIENT_REQUIREMENT}}` | Message key/localization behavior. |
| Data retention | `{{RETENTION_REQUIREMENT}}` | Audit, PII, deletion policy. |

## 9. High-level flow

```mermaid
sequenceDiagram
    autonumber
    actor Actor as {{PRIMARY_ACTOR}}
    participant Client as {{CALLER_APP}}
    participant API as {{CONTROLLER}}
    participant App as {{APPLICATION_SERVICE}}
    participant Domain as {{DOMAIN_SERVICE_OR_AGGREGATE}}
    participant DB as PostgreSQL
    participant Ext as {{EXTERNAL_SERVICE_OR_NONE}}

    Actor->>Client: {{TRIGGER}}
    Client->>API: {{HTTP_METHOD}} {{ENDPOINT}}
    API->>API: Parse + validate request
    API->>App: Execute use case
    App->>App: Authenticate + authorize
    App->>Domain: Apply business rules
    Domain->>DB: Read / write source of truth
    opt External dependency required
        App->>Ext: Call service / publish event
    end
    App-->>API: Result or business exception
    API-->>Client: HTTP response + businessCode + traceId
```

## 10. Acceptance scenarios overview

| Scenario ID | Scenario | Given | When | Then | Expected HTTP | Expected business code |
|---|---|---|---|---|---|---|
| `{{API_CODE}}-S01` | Happy path | `{{GIVEN}}` | `{{WHEN}}` | `{{THEN}}` | `{{HTTP_STATUS}}` | `{{SUCCESS_CODE}}` |
| `{{API_CODE}}-S02` | Empty result | `{{GIVEN}}` | `{{WHEN}}` | Trả cấu trúc rỗng hợp lệ. | `200` | `{{SUCCESS_CODE}}` |
| `{{API_CODE}}-S03` | Invalid input | `{{GIVEN}}` | `{{WHEN}}` | Không xử lý nghiệp vụ/ghi DB. | `400/422` | `{{VALIDATION_CODE}}` |
| `{{API_CODE}}-S04` | Permission denied | `{{GIVEN}}` | `{{WHEN}}` | Không lộ dữ liệu không thuộc quyền. | `403` | `{{FORBIDDEN_CODE}}` |
| `{{API_CODE}}-S05` | State conflict | `{{GIVEN}}` | `{{WHEN}}` | Không thay đổi state. | `409` | `{{CONFLICT_CODE}}` |

## 11. Overview review checklist

- [ ] Tên API, endpoint, method, version, owner và status đã thống nhất.
- [ ] API có đúng một mục tiêu nghiệp vụ chính.
- [ ] Actor/caller/trigger/pre-postcondition/invariant cụ thể.
- [ ] Authentication, authorization và ownership cụ thể.
- [ ] Table/domain/external dependency bị ảnh hưởng đã liệt kê.
- [ ] NFR, timeout, rate limit, idempotency, cache/transaction đã được quyết định.
- [ ] Truy vết đến UC/Activity/Sequence/ERD/Business Rules đã có.
