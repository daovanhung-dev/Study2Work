# Review API DD — S2W-STUDY-API-024

- DD nguồn: `docs/DD/Study2Work_DD_API/03_Onboarding/S2W-STUDY-API-024_GET_onboarding_recommended_paths.xlsx`
- Endpoint: `GET /api/v1/onboarding/recommended-paths`
- Verdict: **CẦN SỬA**

## Findings

| Mức | Sheet/cell | Finding | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P0 | `2.Response!A15:H24`, `3.Data mapping!A12:H12`, `A20` | Recommendation bị map toàn bộ từ `onboarding_records`; `title`, reason, audience/prerequisites/duration/outcomes/difficulty/rank` không phải cột của bảng này. | `docs/BD/03. Study2Work_Study_BasicDesign_Onboarding.md:123-137`; SQL `:323-359` | Join learner onboarding với `learning_paths`; định nghĩa derived recommendation reason/score và nguồn từng field. |
| P0 | `3.Data mapping!A12:H13` | WHERE `onboarding_records.limit=:limit` và sort `order_index, created_at` đều dùng cột không tồn tại; không có filter `publish_status` nên có thể gợi ý path không activatable. | `docs/BD/03. Study2Work_Study_BasicDesign_Onboarding.md:123-137,186-194`; SQL `:323-338` | `limit` chỉ là query limiter; query path `PUBLISHED`/activatable, deterministic ranking và fallback khi không match. |
| P1 | `1.Request!A21:J21` | `limit` nhận 0 tới `2^31-1`, không có default/cap nên cho phép response bất thường và DoS. | `docs/BD/base/0. Study2Work_System_Architecture.md:702-721` | Đặt min 1, cap nhỏ, default và deterministic order. |
| P1 | `4.Error!A14:H16` | `ONBOARDING_REQUIRED` và `ACTIVE_PATH_EXISTS` mâu thuẫn mục đích gợi ý trong chính onboarding; thiếu fallback “popular/intro paths”. | `docs/BD/03. Study2Work_Study_BasicDesign_Onboarding.md:121-137,188-194` | Trả recommendation/fallback phù hợp; chỉ error khi profile tối thiểu chưa đủ hoặc account bị chặn. |
| P0 | `2.Response!A9:E11`, `A25:H25` | Envelope và tên field snake_case không canonical. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Canonical envelope, camelCase và `traceId`. |

## Điều kiện duyệt lại

- [ ] Recommendation query dùng nguồn/cột thật và chỉ trả path activatable.
- [ ] Có ranking reason, cap và fallback được định nghĩa/test.
- [ ] Error/response khớp flow onboarding và canonical convention.
