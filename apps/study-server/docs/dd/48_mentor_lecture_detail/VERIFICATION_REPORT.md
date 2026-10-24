# Verification Report — API #48 Tải lại lecture vừa tạo

## Phạm vi

Kiểm tra tĩnh bộ DD Markdown cho API #48, catalog, AC-21/AC-22, schema candidate, source boundary và macro review nhóm #46–#48. Không thay đổi Study runtime, catalog, schema hoặc diagrams. Không chạy application tests.

## Deliverable manifest

| File | Vai trò | Trạng thái |
|---|---|---|
| 00_Cover.md | Cover | PASS |
| 01_Lich_su.md | Lịch sử | PASS |
| 02_Overview.md | Overview | PASS |
| 03_Request.md | Request | PASS |
| 04_Response.md | Response | PASS |
| 05_Data_Mapping.md | Flow và ma trận | PASS |
| 06_Error.md | Error cases | PASS |
| 07_table.md | Read-only source mapping | PASS |
| PLAN_RESULT.md | Plan và pre-authoring matrices | PASS |
| OPEN_QUESTIONS.md | Gaps/blockers | PASS |
| VERIFICATION_REPORT.md | Verification record | PASS |

## Contract/source checks

| Check | Kết quả | Trạng thái |
|---|---|---|
| Worklog preflight | Selector `docs` chọn #41–#43; cả ba worklogs được đọc đầy đủ. | VERIFIED |
| API catalog #48 | GET path, Mentor Bearer, lecture_id:int64!, ApiEnvelope<Lecture>, 200 và exact errors 401/403/404/500 khớp dòng catalog. | PASS |
| AC-21 activity diagram | Parse đủ node/edge của luồng; xác nhận #47 create → #48 GET detail → hiển thị lecture. | PASS |
| AC-22 boundary | Content CRUD vẫn là workflow riêng; không thêm Content query/table vào #48. | PASS |
| Current Study source | Không có #48 route, module hoặc Python test source; trạng thái UNWIRED / NOT_FOUND. | VERIFIED_STATIC_ONLY |
| Schema boundary | Legacy BIGINT lessons/courses chỉ là candidate; V1-PILOT UUID/versioned giữ riêng; live schema chưa xác minh. | PASS WITH OPEN QUESTIONS |
| Response projection | Tất cả Lecture fields và UploadAsset nested fields được liệt kê; assets[] không bị giả lập. | PASS WITH BLOCKING SOURCE_REQUIRED |
| AC-21 macro review #46–#48 | Owner candidate, DRAFT/read-after-create, schema split, asset gap, Content boundary và error-envelope discrepancy được so sánh; blockers còn mở. | PASS WITH OPEN QUESTIONS |
| Template appendices | Appendix của 8/8 sheet khớp byte-for-byte với registered Markdown templates. | PASS |
| Static Markdown checks | 11/11 file, front matter, JSON example, local links, table widths và fences hợp lệ; lượt đầu phát hiện rồi đã xóa trailing spaces ở metadata OPEN_QUESTIONS, lượt kiểm tra lại sạch. | PASS |
| Archive gate | Không tìm thấy ZIP/XLSX/XLSM trong apps/study-server/docs. | VERIFIED |
| Runtime tests | Không chạy; docs-only và API #48 chưa wired. | NOT_RUN |

## SHA-256 fingerprints — 8 DD sheets

| File | SHA-256 |
|---|---|
| 00_Cover.md | e1937a70e7829e87ae1a7c1ce5de504ad37831efe0f45503615600ada4c7ac2d |
| 01_Lich_su.md | aa3494fe38b26c56a8522ea458a036850d8314fc2245aaa74b774425682d324b |
| 02_Overview.md | 1c6d5efb1900ee884bef1da421831cc43fe143bfb6fad5de05649e6e456f832e |
| 03_Request.md | 0bee7c5861d158967b7a44168068792d1aef8c59eac5deb8252c68c6f7b29c23 |
| 04_Response.md | 3385b3806d5d67bcc365ca7a5adf808cb914afa2a3bad19783192de7185f97a8 |
| 05_Data_Mapping.md | b153b2c6d8751e2310cff8e7a6f0622c5d9aac1f42bd5a5e3a033969ee250698 |
| 06_Error.md | cb3512f09a1a2aad51f8a3fee46a7c4169f9122563081a8fbaa370178700aae8 |
| 07_table.md | 5da53d5807f5e13342b624a80484ab072efa211b0aebc893413ec8a63b282d9b |

## Giới hạn bằng chứng

- Kiểm tra tĩnh không chứng minh handler chạy, live DB schema, Mentor authorization hoặc UploadAsset lookup.
- assets[] là field bắt buộc nhưng chưa có source resolver/persistence; DD giữ Draft — Needs Confirmation và chưa đủ làm implementation approval.
- Runtime/API tests không được chạy vì scope chỉ là tài liệu.
- Macro review xác nhận tính nhất quán của candidate và chỉ rõ gap; không xác nhận business owner đã phê duyệt các candidate.
