# ME-02 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `ME-02-TC-001` | Planning ref / not run | `AC-21` | See source acceptance section | P1 |

## 2. Test planning references

### ME-02-TC-001 — Acceptance planning reference (AC-21)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [ME-02](../../screen_stitch/04_mentor/ME-02_cac-khoa-hoc-phu-trach/ME-02.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-21`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/04_mentor/ME-02_cac-khoa-hoc-phu-trach/ME-02.md).

## 3. Source acceptance / test plan (not run)

### Trích từ DD nguồn: 9. Blockers and acceptance

| ID | Required decision/source | Impact |
|---|---|---|
| ME02-B01 | Confirm course scope: direct ownership vs assignment, identity/schema and matching access policy across #46/#47/#48/#49/#65/#66. | Main list may omit legitimately assigned courses or downstream routes may disagree. |
| ME02-B02 | Implement/identify Study Web Mentor shell, role/session lifecycle and `/mentor/courses` route. | No frontend runtime or implementation route. |
| ME02-B03 | Provide/approve KPI definitions and data sources for course/learner totals, average completion, Capstone, rating and submission counts. | Screenshot shows sample values without current screen response fields. |
| ME02-B04 | Decide search, course-code, level, semester and sort contracts. | #46 cannot support these controls. |
| ME02-B05 | Define mapping between UI status labels and `DRAFT|PUBLISHED`; decide whether all statuses display by default. | Current labels cannot be safely serialized as #46 status. |
| ME02-B06 | Reconcile API #46 DD snapshot/catalog status with current route/module/test source; confirm source is intended API contract. | Existing DD says API is absent; current source says present. Deployment remains unverified. |
| ME02-B07 | Confirm direct CTA targets for ME-06/ME-09/ME-16/ME-18 and global report; decide card-level context and access handoff. | Image links disagree with ME-02 inventory; report route lacks source. |
| ME02-B08 | Decide page-size initial value, reset behavior on filter/sort, out-of-range handling, timeout/retry/stale-response/cache policy. | Screenshot selects 10; API default is 20. |
| ME02-B09 | Approve Study design-token/accessibility reconciliation or provide revised screen assets. | Current mockup conflicts with intended Study Web guide. |
| ME02-B10 | Confirm all data fields/content claims such as code, level, ratings, lesson/lab counts, module labels, partner/academic/footer claims. | Do not expose sample/mock data as live product content. |

### Acceptance checklist

- [x] 47 marker JSON entries are sequential/unique and each has a corresponding `ME02-EL-xx` row.
- [x] Source image and HTML preserved; annotated image and marker overlay visually inspected.
- [x] #46 route → guard → validation → query/count → mapping → response/error and relevant test source traced; tests were not run.
- [x] Expected behavior and current source differences are kept separate; `DISCREPANCY`, `UNWIRED` and `NOT_FOUND` claims are explicit.
- [x] Element/event/state/navigation matrix links every source marker to the DD.
- [ ] Resolve ME02-B01–B10 and review the resulting approved behavior before marking `DD READY`.
- [ ] Frontend implementation/runtime verification; not performed in this documentation session.

#### Kế hoạch kiểm chứng từ source PLAN

### Trích từ DD nguồn: 5. Verification plan và sequencing

1. **Plan first:** hoàn tất file này trước DD, JSON marker map hoặc ảnh chú thích.
2. Tạo `ME-02_markers.json` với 47 marker duy nhất, source pixel coordinates, element labels và mapping IDs.
3. Tạo SVG overlay + `screen_annotated.png` từ `screen.png`; kiểm tra kích thước/ratio, marker bounds, số marker và bố cục không che nội dung chính; mở ảnh kiểm tra trực quan.
4. Viết `ME-02.md`: overview/preconditions, expected/current separation, caller→guard→query/count/page→mapper→response/errors→test source trace, 47 element rows, event-by-event input/process/output/blocker, API mapping, states, navigation, security/accessibility, acceptance checklist.
5. Cập nhật đúng ME-02 row và current progress section trong `dd_screens/PLAN.md`; chỉ tăng số bộ file hiện diện, không đếm thành `DD READY`.
6. Ghi worklog preflight paths, source evidence, discrepancies, files và verification; chạy static artifact/link/whitespace checks. Không chạy app tests hoặc runtime.

### Static pass criteria

- Original PNG/HTML hashes không đổi; new annotated image đúng tỷ lệ với source.
- JSON chứa đủ marker #1–#47, ID `ME02-EL-01..47` duy nhất và tọa độ trong ảnh.
- DD có đúng 47 element ID rows ánh xạ marker; mỗi event có trigger/input/preconditions/steps/output/errors hoặc blocker.
- SVG và annotated image cùng thể hiện 47 markers; ảnh được xem trực tiếp.
- Relative Markdown links resolve; status trong DD/plan/worklog nhất quán.

### Status at plan completion

- `DD`: chưa soạn; dự kiến **BLOCKED** bởi các quyết định dữ liệu/route/filter trong B01–B10.
- `IMPLEMENTATION`: **BLOCKED** bởi source/UI wiring absent và unsupported fields/actions.
- `RUNTIME`: **NOT VERIFIED**.
- No source/API/DB implementation changes are in scope.

- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
