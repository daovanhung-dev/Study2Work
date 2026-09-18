# DD Review Checklist

## BA/PO

- [ ] Business goal, scope/out-of-scope và actor permission đúng.
- [ ] Business rules, state transitions và acceptance criteria không mơ hồ.
- [ ] Open questions có owner và không bị ẩn trong technical default.

## Tech Lead

- [ ] Data ownership, API/event, transaction/idempotency và dependency map rõ.
- [ ] Import direction đúng kiến trúc; không có circular/forbidden import.
- [ ] Implementation/verification claims có source evidence.

## QA

- [ ] Happy, alternate, validation, permission, conflict, retry và system-error cases có test.
- [ ] View states và error copy có thể kiểm tra.
- [ ] Traceability từ requirement tới test đầy đủ.

## Static gate

- [ ] Validator PASS.
- [ ] Markdown links hợp lệ.
- [ ] `git diff --check` PASS.
- [ ] Worklog và changelog đã cập nhật.
