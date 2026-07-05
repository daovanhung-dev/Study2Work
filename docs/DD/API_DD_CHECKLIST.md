# API DD Checklist

Mỗi API đã có:
- [x] README: contract, mục tiêu, quick links
- [x] Overview: luồng, authorization, business rules, traceability
- [x] History: version và thay đổi
- [x] Request: headers, path/query/body, validation
- [x] Response: envelope, field contract, mẫu
- [x] Data Mapping: command/query, bảng/aggregate, transaction/audit
- [x] Error: HTTP mapping và domain errors

Trước khi code, team cần chốt ERD, authentication provider, enum master data, retention policy và SLA của external services.
