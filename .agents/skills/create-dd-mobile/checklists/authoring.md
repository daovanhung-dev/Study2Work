# DD Authoring Checklist

- [ ] Đủ README, Overall, List_Features, Function_List, Views, Import_File.
- [ ] Có `diagrams/README.md`, `assets/README.md`, `history/CHANGELOG.md`.
- [ ] Overall có goal, scope, roles, data, states, rules, flows, NFR và traceability.
- [ ] Mỗi feature có pre/postcondition, happy/error flow, validation, authorization và AC.
- [ ] Mỗi function có input/output, rule, transaction/idempotency, side effect và test.
- [ ] Mỗi view có action mapping và các UI states cần thiết.
- [ ] Import map không vi phạm dependency direction.
- [ ] Không biến assumption/proposal thành business rule.
- [ ] Không có secret, PII hoặc raw sensitive payload.
