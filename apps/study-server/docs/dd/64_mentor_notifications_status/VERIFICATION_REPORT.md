# VERIFICATION_REPORT — Study API #64

## Kết quả

- DD status: `Draft — Needs Confirmation`; contract direct của catalog được giữ nguyên, discrepancy được nêu riêng.
- Deliverable: 8 sheet template + 3 report Markdown; package được kiểm tra tĩnh.
- Runtime API #64: `UNWIRED / NOT_FOUND`; không có route/query/module/provider/test để xác nhận behavior.
- Macro-review AC-25 #62–#64 và operation handoff #18: `VERIFIED_WITH_OPEN_QUESTIONS` ở mức tài liệu; chưa sửa hay xác nhận contract/schema/runtime.

## Kiểm tra

| Check | Kết quả | Trạng thái |
|---|---|---|
| Skill/template | `createDD-markdown` registry-wired; hash template và appendix byte match 8/8. | VERIFIED |
| Manifest/front matter | Đủ 11/11 file; 8/8 sheet có `dd_id: 64` và trạng thái Draft. | VERIFIED |
| Contract/request/error | Đúng GET/path/auth/no body/query; 200 `ApiEnvelope<Operation>`; đúng bốn error code 401/403/404/500. | VERIFIED_STATIC_ONLY |
| Response/Data Mapping coverage | Đủ 22 field Operation/envelope, gồm Payment nested fields; tất cả có dòng mapping, không bịa physical source. | VERIFIED_STATIC_ONLY |
| AC-25 trace | Đã đọc node/edge #62 → #63 → Push/Email → #64; node #18 tồn tại nhưng detached. | VERIFIED_STATIC_ONLY |
| Macro-review nhóm | So sánh #62 roster → #63 create/Operation → #64 delivery lookup và API #18; giữ các ID/schema/permission gap ở trạng thái mở. | VERIFIED_WITH_OPEN_QUESTIONS |
| JSON/Markdown | Parse 2 JSON; 35 relative-link paths resolve; 456 table rows nhất quán; internal anchors, code fences và whitespace hợp lệ. | VERIFIED_STATIC_ONLY |
| `git diff --check` | Không có whitespace diagnostics; custom check cũng kiểm tra toàn bộ 11 file DD chưa theo dõi. | PASS |
| Runtime tests | Không chạy; docs-only và API #64 chưa wired. | NOT_RUN |
| Context validator | Không áp dụng; không đổi context page/registry. | NOT_APPLICABLE |

## Macro-review AC-25 — kết luận và việc còn mở

- #62 trả `Page<Course>` trong khi flow cần learner roster; chưa có item ID ổn định và không có pagination input.
- #63 chưa chốt recipient encoding/course scope; `content:int64` lệch nội dung text; response Operation không cung cấp `notification_id:int64` cho #64.
- #64 nhận notification ID nhưng trả Operation, không có delivery status/counts; `NotificationDelivery` gần với mục tiêu hơn nhưng chưa phải contract direct.
- #18 là job polling riêng nhưng node diagram AC-25 detached; ID int64/UUID, owner rule, persistence và result còn open.
- Legacy schema có read flag nhưng không có delivery rows; V1-PILOT có UUID attempt rows, không có recipient ID. Không dùng `is_read` làm delivery status hoặc đếm retry attempts như recipient counts.
- Đề xuất đồng bộ contract theo sequence #62 learner page → #63 trả riêng notification ID và operation ID → #64 trả delivery summary → #18 poll job UUID. Đây là `DERIVED`, không phải contract đã duyệt.

## Output fingerprints — 8 sheet

```text
00_Cover.md        5aae395d6f4356442a34085647a43ed4aab0f30443466aa679d9c341a8dca77d
01_Lich_su.md      bf425d9132b2871846a23e76a94b7bbfa9c22fad9ddae9dacffc87d8679f0ca2
02_Overview.md     eb09fb4d1af22156c55eead38168794cd2999d4a4a46e59ebd1f52c697aa152d
03_Request.md      5a9126cd2b39e755d06ca2c4b937893d47779489b688dd1962a9fb324b83a48a
04_Response.md     c37462f7e8726b5042bf7ac81cbed3ce8d5c855a200d5ecdd020a6ccc2c35c3d
05_Data_Mapping.md ff0fba6ce76815d36bacbbe9c159cec500d63db63a6cc15c5461bc97ce985ddb
06_Error.md        6a5d10fbf0a7a47d1b3a0501989d95f0cbe93fea40329113312ef4fb4f74e0e2
07_table.md        60690be98cc3630cb2b643d5032997d30daa685db29c401876cce59b5447b652
```

## Open blockers

- #62 learner response/key, #63 recipient/course/content/channel contract, #63-to-#64 notification ID handoff, #64 delivery query/aggregate/status, and Mentor access relation need owner/schema decisions.
- Operation job polling #18 remains distinct and unresolved; future implementation must align response envelope with middleware allowlist and error-body guideline.

Xem [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md), [PLAN_RESULT.md](./PLAN_RESULT.md), [API #62 report](../62_mentor_course_students/VERIFICATION_REPORT.md) và [API #63 report](../63_mentor_notifications_create/VERIFICATION_REPORT.md).
