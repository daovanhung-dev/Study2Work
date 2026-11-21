# Verification Report — API #46

## Phạm vi

DD Markdown-only cho API #46. Không thay đổi app runtime, API catalog, schema, diagrams hay source DB. Không chạy application tests.

## Kết quả

| Check | Kết quả | Trạng thái |
|---|---|---|
| Preflight `docs` worklogs | Đọc worklogs #41–#43 theo selector. | `VERIFIED` |
| Context/skill/workflow | `createDD-markdown` được registry wire; Study workflow yêu cầu Markdown-only. | `VERIFIED` |
| API catalog | #46 là `GET /api/v1/mentor/courses`, Mentor JWT, status/page/size, `ApiEnvelope<Page<Course>>`, HTTP/error set 200/401/403/422/500. | `VERIFIED` |
| AC-21 | Flow #46 list/ownership → upload → #47 create lecture → #48 reload. | `VERIFIED` |
| Current route/module/test source | Không tìm thấy route/module/view/focused test #46. | `UNWIRED / NOT_FOUND` |
| Schema sources | Legacy DDL và V1-PILOT DDL khác mô hình; live schema chưa kiểm tra. | `DISCREPANCY / NOT_VERIFIED` |
| DD file set | Đủ 8 sheet + 3 report; toàn bộ sheet có API ID 46 và status đúng. | `PASS` |
| Template appendices | Appendix của cả 8 sheet khớp byte-for-byte với 8 file trong `DD_API_Template_MD`. | `PASS` |
| Contract/status/error set | Method/path, actor, query, response và 4 error business codes khớp dòng catalog #46. | `PASS` |
| Relative links, JSON, tables, code fences | 11 file qua kiểm tra JSON, fence, chiều rộng bảng, đường dẫn nội bộ và anchor. | `PASS` |
| Runtime tests | Không chạy; docs-only. | `NOT_RUN` |
| Context validator | `deno run --allow-read --allow-env scripts/validate-agent-context.mjs` báo thiếu context/source DB Admin và baseline commit `9a70eb6764a6587093a92d3bd7e4cc0bea1651c4`; lỗi ngoài scope Study DD. | `BLOCKED_UNRELATED_REPO_CONTEXT` |
| AC-21 group review | Đã so #46–#48: direct-owner candidate thống nhất; assignment/identity còn mở; #48 không lọc PUBLISHED để hỗ trợ đọc DRAFT sau #47; asset resolver và live schema vẫn là blocker/gap. | `PASS_WITH_OPEN_QUESTIONS` |


## SHA-256 fingerprints — 8 DD sheets

| File | SHA-256 |
|---|---|
| `00_Cover.md` | `f4087b68784f7ad22fb610769446a7a51f0b79f704a576388642cbbea7eff4ce` |
| `01_Lich_su.md` | `0daf52d6194d632887112799c335ed0bda6d06f50ab226c7f665e7738f4fce87` |
| `02_Overview.md` | `5bfb48ccce842c1fc2e89e0e6764bcca3df636eda0ae3047cb4322b90204cda4` |
| `03_Request.md` | `0df4da60ba5dff787ba35800c8bd60b1f43dd7ee528bd6fbe088a7057e2ff0a6` |
| `04_Response.md` | `630db618117d7260832128d4ac6bdb0ec32eb88de6f4ad80667909643010d94b` |
| `05_Data_Mapping.md` | `9dc7719549243258b030224bcfcbd143234a8648f73d5b586a0eef59a64f5603` |
| `06_Error.md` | `c14588b2e55727eefe465ed090eca416e73ad9b6fb9596348e24a5bb8b51f089` |
| `07_table.md` | `8f364e71b8eff733586e8cc4bb196bb9a78335102b7a00498a5583613cd24b05` |

## Giới hạn bằng chứng

- Static validation chỉ chứng minh cấu trúc tài liệu và đối chiếu contract/source đã đọc.
- Không chứng minh handler chạy, DB schema tồn tại, quyền Mentor được triển khai, hay API #47/#48 nhất quán runtime.

