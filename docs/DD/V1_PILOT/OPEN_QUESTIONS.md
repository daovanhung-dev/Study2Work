# Open Questions

Only source-backed unresolved issues are recorded. This document does not propose new API IDs, routes, tables, columns, enums, roles or business codes.

<a id="oq-iam-authversion"></a>
## OQ-IAM-AUTHVERSION — Nguồn lưu authVersion

- Domain: `IAM`.
- Evidence: `06_BAO_CAO_RAO_SOAT_LOGIC.md §4.1`.
- Gap: users và identity projection chưa mô tả cột hoặc nguồn dữ liệu cho authVersion dùng trong JWT/sự kiện.
- Handling: affected DDs remain `Draft — Needs Confirmation` and use `SOURCE_REQUIRED` or `TBD`.

<a id="oq-iam-mfa-enrollment"></a>
## OQ-IAM-MFA-ENROLLMENT — Mô hình MFA chờ xác nhận

- Domain: `IAM`.
- Evidence: `06_BAO_CAO_RAO_SOAT_LOGIC.md §4.1`.
- Gap: mfa_methods chưa mô tả trạng thái ghi danh MFA đang chờ xác nhận và thời hạn.
- Handling: affected DDs remain `Draft — Needs Confirmation` and use `SOURCE_REQUIRED` or `TBD`.

<a id="oq-stu-onboarding"></a>
## OQ-STU-ONBOARDING — Bản nháp và cấu hình onboarding

- Domain: `STU`.
- Evidence: `06_BAO_CAO_RAO_SOAT_LOGIC.md §4.2`.
- Gap: Hợp đồng lưu nháp, trạng thái và câu hỏi onboarding chưa khớp mô hình onboarding_submissions bất biến.
- Handling: affected DDs remain `Draft — Needs Confirmation` and use `SOURCE_REQUIRED` or `TBD`.

<a id="oq-stu-skills-history"></a>
## OQ-STU-SKILLS-HISTORY — Nguồn kỹ năng và lịch sử học

- Domain: `STU`.
- Evidence: `06_BAO_CAO_RAO_SOAT_LOGIC.md §4.2`.
- Gap: Một số API kỹ năng và lịch sử học chưa có bảng liên kết, lịch sử hoặc chính sách lưu giữ rõ ràng.
- Handling: affected DDs remain `Draft — Needs Confirmation` and use `SOURCE_REQUIRED` or `TBD`.

<a id="oq-stu-evidence-files"></a>
## OQ-STU-EVIDENCE-FILES — Quan hệ minh chứng và tệp

- Domain: `STU`.
- Evidence: `06_BAO_CAO_RAO_SOAT_LOGIC.md §4.2`.
- Gap: evidence_records chưa thể hiện rõ quan hệ với file_objects cho hợp đồng minh chứng có tệp.
- Handling: affected DDs remain `Draft — Needs Confirmation` and use `SOURCE_REQUIRED` or `TBD`.

<a id="oq-wrk-search-consent"></a>
## OQ-WRK-SEARCH-CONSENT — Đồng ý tìm kiếm ứng viên

- Domain: `WRK`.
- Evidence: `06_BAO_CAO_RAO_SOAT_LOGIC.md §4.3`.
- Gap: Lịch sử chính sách, thời hạn và trường hiển thị của search consent chưa có mô hình riêng phù hợp.
- Handling: affected DDs remain `Draft — Needs Confirmation` and use `SOURCE_REQUIRED` or `TBD`.

<a id="oq-wrk-public-job-slug"></a>
## OQ-WRK-PUBLIC-JOB-SLUG — Định danh jobSlug công khai

- Domain: `WRK`.
- Evidence: `06_BAO_CAO_RAO_SOAT_LOGIC.md §4.3`.
- Gap: Tuyến công khai dùng job slug nhưng schema chỉ bảo đảm duy nhất trong không gian dữ liệu.
- Handling: affected DDs remain `Draft — Needs Confirmation` and use `SOURCE_REQUIRED` or `TBD`.

<a id="oq-uni-incomplete-flows"></a>
## OQ-UNI-INCOMPLETE-FLOWS — Luồng University chưa đủ mô hình/API

- Domain: `UNI`.
- Evidence: `06_BAO_CAO_RAO_SOAT_LOGIC.md §4.3`.
- Gap: Affiliation invitation, phản hồi đề nghị và dữ liệu báo cáo chưa có mô hình hoặc API đầy đủ.
- Handling: affected DDs remain `Draft — Needs Confirmation` and use `SOURCE_REQUIRED` or `TBD`.

<a id="oq-pay-entitlement-hold"></a>
## OQ-PAY-ENTITLEMENT-HOLD — Giữ chỗ và hoàn quyền lợi

- Domain: `PAY`.
- Evidence: `06_BAO_CAO_RAO_SOAT_LOGIC.md §4.4`.
- Gap: Thời điểm trừ, hoàn và chống chi tiêu trùng cho quyền lợi chưa được mô hình hóa đầy đủ.
- Handling: affected DDs remain `Draft — Needs Confirmation` and use `SOURCE_REQUIRED` or `TBD`.

<a id="oq-pay-promotion-metrics"></a>
## OQ-PAY-PROMOTION-METRICS — Mô hình đo lường quảng bá

- Domain: `PAY`.
- Evidence: `06_BAO_CAO_RAO_SOAT_LOGIC.md §4.4`.
- Gap: Thiết kế chưa chốt giữa lưu sự kiện hiển thị/nhấp gốc và chỉ giữ bộ đếm tổng hợp.
- Handling: affected DDs remain `Draft — Needs Confirmation` and use `SOURCE_REQUIRED` or `TBD`.

<a id="oq-aix-evaluation-kill-switch"></a>
## OQ-AIX-EVALUATION-KILL-SWITCH — Đánh giá AI và kill switch

- Domain: `AIX`.
- Evidence: `06_BAO_CAO_RAO_SOAT_LOGIC.md §4.4`.
- Gap: Dataset, evaluation run/result và phạm vi kill switch chi tiết hơn mô hình hiện hành.
- Handling: affected DDs remain `Draft — Needs Confirmation` and use `SOURCE_REQUIRED` or `TBD`.

<a id="oq-ops-missing-read-contracts"></a>
## OQ-OPS-MISSING-READ-CONTRACTS — Các hợp đồng vận hành còn thiếu

- Domain: `OPS`.
- Evidence: `06_BAO_CAO_RAO_SOAT_LOGIC.md §4.3–§4.4`.
- Gap: Một số màn vận hành cần queue, detail hoặc approval counterpart nhưng catalog chỉ có mutation hoặc thiếu API đối ứng.
- Handling: affected DDs remain `Draft — Needs Confirmation` and use `SOURCE_REQUIRED` or `TBD`.

## Unapproved screen-derived candidates

- No DD is created for a screen surface without an approved API ID and route.

### Operations read/approval counterparts

- SCR-OPS-014 requires a support queue, internal-note and resolution-event surface while the catalog names only an existing support detail API (docs/BD/05_DAC_TA_MAN_HINH.md:L188).
- SCR-OPS-018 requires verification detail/read context while the catalog names a list and a decision action (docs/BD/05_DAC_TA_MAN_HINH.md:L191-L192).
- SCR-OPS-020 requires refund queue/detail and reject/decision context beyond the currently named request and approve actions (docs/BD/05_DAC_TA_MAN_HINH.md:L194).
- SCR-OPS-022 and SCR-OPS-023 require runtime/policy/evaluation read and activation context beyond mutation-oriented AI catalog entries (docs/BD/05_DAC_TA_MAN_HINH.md:L196-L197).
- SCR-OPS-025 requires break-glass status and second-approval context beyond session creation (docs/BD/05_DAC_TA_MAN_HINH.md:L199).

### Other screen read surfaces requiring reconciliation

- University affiliation invitation/list, cohort/program/distribution/partnership/referral reads and outcome reporting have screen coverage but must use only approved catalog contracts (docs/BD/05_DAC_TA_MAN_HINH.md:L159-L162).
- Candidate and enterprise views describe CV revision, job revision/history, interview detail and payment/refund-list reads that must not be converted into DDs without an approved API contract (docs/BD/05_DAC_TA_MAN_HINH.md:L127-L148).
- Study support/content screens may require draft/version reads; those remain screen requirements until the API catalog approves a contract (docs/BD/05_DAC_TA_MAN_HINH.md:L187-L190).
