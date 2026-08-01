# Review S2W-STUDY-API-144 — GET onboarding report

- DD nguồn: `docs/DD/Study2Work_DD_API/12_Bao_cao_van_hanh/S2W-STUDY-API-144_GET_admin_reports_onboarding.xlsx`
- Endpoint: `GET /api/v1/admin/reports/onboarding`
- Kết luận: **CẦN SỬA — metric/query/error chưa đặc thù onboarding**

## Các điểm cần sửa

| ID | Mức độ | Vị trí DD | Nhận xét và căn cứ BD | Cách sửa |
|---|---|---|---|---|
| 144-01 | P0 | `3.Data mapping!A12:H20` | `vw_report_onboarding` không tồn tại; query dùng bộ filter copy chung và coi `from/to/granularity` là cột. Không có định nghĩa “started”, “completed”, từng funnel step hay chọn theo gợi ý. | Định nghĩa event/cohort/denominator cho từng metric tại `BD-12:95-110`; viết aggregate query/view thật. |
| 144-02 | P1 | `2.Response!A16:H21` | Rates để String; `funnel_by_step`, goals và levels chỉ ghi Array không item schema. | Dùng decimal rate và object item `{step, entrants, completed, dropoffRate}`; chốt goal/level enum và unknown handling. |
| 144-03 | P0 | `4.Error!A13:H16`, `3.Data mapping!A17:H17` | Error `ACCOUNT_NOT_VERIFIED`, `ONBOARDING_REQUIRED`, `ACTIVE_PATH_EXISTS`, `PATH_NOT_PUBLISHED` thuộc luồng learner activation, không phù hợp API admin đọc báo cáo. | Xóa lỗi template; thêm invalid date range/filter, report unavailable/stale và permission denied nếu cần. |
| 144-04 | P1 | `1.Request!A23:J29` | `course_id`, `level`, learner group, account/path status được copy vào mọi report nhưng không nêu quan hệ với funnel onboarding; filter có thể làm sai denominator. | Chỉ giữ filter có ý nghĩa hoặc mô tả rõ cohort intersection và denominator sau filter. |
| 144-05 | P0 | `2.Response!A9:E11` | Envelope cũ/pagination giả trái `System_Architecture.md:632-700`. | Dùng envelope chuẩn camelCase, traceId; bỏ pagination. |

## Điều kiện duyệt lại

- Funnel/event definitions có thể tái tạo bằng fixture.
- Error/filter/response chỉ chứa nội dung phù hợp báo cáo onboarding.
