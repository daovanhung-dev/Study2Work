# 00. API DD PLAN INDEX

## 1. Tổng quan

- Tổng API: **212**.
- Tổng plan: **58**.
- Mỗi API xuất hiện đúng một lần trong plan owner.
- Mỗi plan giới hạn 1–5 API, tương đương 8–40 file lõi trước DB Mapping.
- Plan được chia theo transaction boundary và business flow, không chỉ theo số lượng.

## 2. Danh sách plan

| Plan | Phạm vi | API | Read/Mutation | Rủi ro | File |
|---:|---|---:|---:|---|---|
| 01 | IAM — Đăng ký và xác minh email | 3 | 0/3 | Cao | [PLAN_01_IAM_IAM_ang_ky_va_xac_minh_email.md](./plans/PLAN_01_IAM_IAM_ang_ky_va_xac_minh_email.md) |
| 02 | IAM — Đăng nhập, MFA, refresh và logout | 5 | 0/5 | Rất cao | [PLAN_02_IAM_IAM_ang_nhap_MFA_refresh_va_logout.md](./plans/PLAN_02_IAM_IAM_ang_nhap_MFA_refresh_va_logout.md) |
| 03 | IAM — Khôi phục mật khẩu, đổi mật khẩu và đổi email | 6 | 1/5 | Cao | [PLAN_03_IAM_IAM_Khoi_phuc_mat_khau_oi_mat_khau_va_oi_email.md](./plans/PLAN_03_IAM_IAM_Khoi_phuc_mat_khau_oi_mat_khau_va_oi_email.md) |
| 04 | IAM — Quản lý session và đăng ký MFA | 4 | 1/3 | Cao | [PLAN_04_IAM_IAM_Quan_ly_session_va_ang_ky_MFA.md](./plans/PLAN_04_IAM_IAM_Quan_ly_session_va_ang_ky_MFA.md) |
| 05 | IAM — Yêu cầu xóa tài khoản và hủy yêu cầu | 2 | 0/2 | Rất cao | [PLAN_05_IAM_IAM_Yeu_cau_xoa_tai_khoan_va_huy_yeu_cau.md](./plans/PLAN_05_IAM_IAM_Yeu_cau_xoa_tai_khoan_va_huy_yeu_cau.md) |
| 06 | IAM — Quản trị user, global role và JWKS | 4 | 2/2 | Rất cao | [PLAN_06_IAM_IAM_Quan_tri_user_global_role_va_JWKS.md](./plans/PLAN_06_IAM_IAM_Quan_tri_user_global_role_va_JWKS.md) |
| 07 | Study — Public catalog và metadata | 6 | 6/0 | Trung bình | [PLAN_07_STU_Study_Public_catalog_va_metadata.md](./plans/PLAN_07_STU_Study_Public_catalog_va_metadata.md) |
| 08 | Study — Hồ sơ học tập và onboarding | 5 | 2/3 | Cao | [PLAN_08_STU_Study_Ho_so_hoc_tap_va_onboarding.md](./plans/PLAN_08_STU_Study_Ho_so_hoc_tap_va_onboarding.md) |
| 09 | Study — Gợi ý và primary path | 4 | 3/1 | Rất cao | [PLAN_09_STU_Study_Goi_y_va_primary_path.md](./plans/PLAN_09_STU_Study_Goi_y_va_primary_path.md) |
| 10 | Study — Đăng ký khóa học và course study context | 3 | 2/1 | Cao | [PLAN_10_STU_Study_ang_ky_khoa_hoc_va_course_study_context.md](./plans/PLAN_10_STU_Study_ang_ky_khoa_hoc_va_course_study_context.md) |
| 11 | Study — Lesson study, tiến độ và lịch sử học | 4 | 3/1 | Cao | [PLAN_11_STU_Study_Lesson_study_tien_o_va_lich_su_hoc.md](./plans/PLAN_11_STU_Study_Lesson_study_tien_o_va_lich_su_hoc.md) |
| 12 | Study — Assessment definition và draft | 4 | 2/2 | Cao | [PLAN_12_STU_Study_Assessment_definition_va_draft.md](./plans/PLAN_12_STU_Study_Assessment_definition_va_draft.md) |
| 13 | Study — Assessment attempt, kết quả và review view | 3 | 2/1 | Rất cao | [PLAN_13_STU_Study_Assessment_attempt_ket_qua_va_review_view.md](./plans/PLAN_13_STU_Study_Assessment_attempt_ket_qua_va_review_view.md) |
| 14 | Study — File upload, scan và download URL | 4 | 1/3 | Rất cao | [PLAN_14_STU_Study_File_upload_scan_va_download_URL.md](./plans/PLAN_14_STU_Study_File_upload_scan_va_download_URL.md) |
| 15 | Study — Notification và preferences | 5 | 2/3 | Trung bình | [PLAN_15_STU_Study_Notification_va_preferences.md](./plans/PLAN_15_STU_Study_Notification_va_preferences.md) |
| 16 | Study — Community groups và report | 4 | 1/3 | Cao | [PLAN_16_STU_Study_Community_groups_va_report.md](./plans/PLAN_16_STU_Study_Community_groups_va_report.md) |
| 17 | Study — Support request lifecycle | 4 | 2/2 | Trung bình | [PLAN_17_STU_Study_Support_request_lifecycle.md](./plans/PLAN_17_STU_Study_Support_request_lifecycle.md) |
| 18 | Study — Assessment review, learner adjustment và local role | 5 | 1/4 | Rất cao | [PLAN_18_STU_Study_Assessment_review_learner_adjustment_va_local_role.md](./plans/PLAN_18_STU_Study_Assessment_review_learner_adjustment_va_local_role.md) |
| 19 | Study — Tạo content và quản lý draft version | 4 | 1/3 | Rất cao | [PLAN_19_STU_Study_Tao_content_va_quan_ly_draft_version.md](./plans/PLAN_19_STU_Study_Tao_content_va_quan_ly_draft_version.md) |
| 20 | Study — Pre-publish, publish, archive và content issue | 5 | 1/4 | Rất cao | [PLAN_20_STU_Study_Pre_publish_publish_archive_va_content_issue.md](./plans/PLAN_20_STU_Study_Pre_publish_publish_archive_va_content_issue.md) |
| 21 | Study Evidence — Token hạ quyền và self evidence | 3 | 2/1 | Rất cao | [PLAN_21_IAM_Study_Evidence_Token_ha_quyen_va_self_evidence.md](./plans/PLAN_21_IAM_Study_Evidence_Token_ha_quyen_va_self_evidence.md) |
| 22 | Work — Public job catalog | 4 | 4/0 | Cao | [PLAN_22_WRK_Work_Public_job_catalog.md](./plans/PLAN_22_WRK_Work_Public_job_catalog.md) |
| 23 | Work — Candidate profile và search consent | 3 | 1/2 | Rất cao | [PLAN_23_WRK_Work_Candidate_profile_va_search_consent.md](./plans/PLAN_23_WRK_Work_Candidate_profile_va_search_consent.md) |
| 24 | Work — CV draft, edit và publish | 4 | 1/3 | Rất cao | [PLAN_24_WRK_Work_CV_draft_edit_va_publish.md](./plans/PLAN_24_WRK_Work_CV_draft_edit_va_publish.md) |
| 25 | Work — CV export và default CV | 2 | 0/2 | Cao | [PLAN_25_WRK_Work_CV_export_va_default_CV.md](./plans/PLAN_25_WRK_Work_CV_export_va_default_CV.md) |
| 26 | Work — Portfolio lifecycle | 4 | 1/3 | Cao | [PLAN_26_WRK_Work_Portfolio_lifecycle.md](./plans/PLAN_26_WRK_Work_Portfolio_lifecycle.md) |
| 27 | Work — Recommendation, saved job và invitation response | 4 | 2/2 | Cao | [PLAN_27_WRK_Work_Recommendation_saved_job_va_invitation_response.md](./plans/PLAN_27_WRK_Work_Recommendation_saved_job_va_invitation_response.md) |
| 28 | Work — Application context và submit application | 2 | 1/1 | Rất cao | [PLAN_28_WRK_Work_Application_context_va_submit_application.md](./plans/PLAN_28_WRK_Work_Application_context_va_submit_application.md) |
| 29 | Work — Candidate application read, withdraw và evidence consent withdrawal | 4 | 2/2 | Rất cao | [PLAN_29_WRK_Work_Candidate_application_read_withdraw_va_evidence_consent_withdrawal.md](./plans/PLAN_29_WRK_Work_Candidate_application_read_withdraw_va_evidence_consent_withdrawal.md) |
| 30 | Work — Candidate interview response và ICS | 3 | 2/1 | Rất cao | [PLAN_30_WRK_Work_Candidate_interview_response_va_ICS.md](./plans/PLAN_30_WRK_Work_Candidate_interview_response_va_ICS.md) |
| 31 | Work — Chat REST và moderation | 4 | 1/3 | Rất cao | [PLAN_31_WRK_Work_Chat_REST_va_moderation.md](./plans/PLAN_31_WRK_Work_Chat_REST_va_moderation.md) |
| 32 | Work — Enterprise tenant, workspace, profile và verification submission | 4 | 1/3 | Rất cao | [PLAN_32_WRK_Work_Enterprise_tenant_workspace_profile_va_verification_submission.md](./plans/PLAN_32_WRK_Work_Enterprise_tenant_workspace_profile_va_verification_submission.md) |
| 33 | Work — Enterprise member list, invite và role update | 3 | 1/2 | Rất cao | [PLAN_33_WRK_Work_Enterprise_member_list_invite_va_role_update.md](./plans/PLAN_33_WRK_Work_Enterprise_member_list_invite_va_role_update.md) |
| 34 | Work — Job stable entity và draft revision | 4 | 1/3 | Rất cao | [PLAN_34_WRK_Work_Job_stable_entity_va_draft_revision.md](./plans/PLAN_34_WRK_Work_Job_stable_entity_va_draft_revision.md) |
| 35 | Work — Job review submission và publish | 2 | 0/2 | Rất cao | [PLAN_35_WRK_Work_Job_review_submission_va_publish.md](./plans/PLAN_35_WRK_Work_Job_review_submission_va_publish.md) |
| 36 | Work — Job pause, resume và close | 3 | 0/3 | Rất cao | [PLAN_36_WRK_Work_Job_pause_resume_va_close.md](./plans/PLAN_36_WRK_Work_Job_pause_resume_va_close.md) |
| 37 | Work — Candidate search và invitation phía Enterprise | 3 | 1/2 | Rất cao | [PLAN_37_WRK_Work_Candidate_search_va_invitation_phia_Enterprise.md](./plans/PLAN_37_WRK_Work_Candidate_search_va_invitation_phia_Enterprise.md) |
| 38 | Work ATS — List/detail, assignee và note | 4 | 2/2 | Rất cao | [PLAN_38_WRK_Work_ATS_List_detail_assignee_va_note.md](./plans/PLAN_38_WRK_Work_ATS_List_detail_assignee_va_note.md) |
| 39 | Work ATS — Status transition và offer | 2 | 0/2 | Rất cao | [PLAN_39_WRK_Work_ATS_Status_transition_va_offer.md](./plans/PLAN_39_WRK_Work_ATS_Status_transition_va_offer.md) |
| 40 | Work — Enterprise interview scheduling | 3 | 0/3 | Rất cao | [PLAN_40_WRK_Work_Enterprise_interview_scheduling.md](./plans/PLAN_40_WRK_Work_Enterprise_interview_scheduling.md) |
| 41 | University — Tenant, verification và membership | 4 | 1/3 | Rất cao | [PLAN_41_UNI_University_Tenant_verification_va_membership.md](./plans/PLAN_41_UNI_University_Tenant_verification_va_membership.md) |
| 42 | University — Affiliation invitation, consent và cohort | 5 | 0/5 | Rất cao | [PLAN_42_UNI_University_Affiliation_invitation_consent_va_cohort.md](./plans/PLAN_42_UNI_University_Affiliation_invitation_consent_va_cohort.md) |
| 43 | University — Internship, campus distribution, partnership và referral | 5 | 0/5 | Rất cao | [PLAN_43_UNI_University_Internship_campus_distribution_partnership_va_referral.md](./plans/PLAN_43_UNI_University_Internship_campus_distribution_partnership_va_referral.md) |
| 44 | University — Outcome report và affiliation detail | 2 | 2/0 | Rất cao | [PLAN_44_UNI_University_Outcome_report_va_affiliation_detail.md](./plans/PLAN_44_UNI_University_Outcome_report_va_affiliation_detail.md) |
| 45 | Payment — Product, order, retry và return URL | 5 | 3/2 | Rất cao | [PLAN_45_PAY_Payment_Product_order_retry_va_return_URL.md](./plans/PLAN_45_PAY_Payment_Product_order_retry_va_return_URL.md) |
| 46 | Payment — Entitlement, refund và reconciliation | 5 | 2/3 | Rất cao | [PLAN_46_PAY_Payment_Entitlement_refund_va_reconciliation.md](./plans/PLAN_46_PAY_Payment_Entitlement_refund_va_reconciliation.md) |
| 47 | Payment — Sponsored promotion và tracking | 4 | 0/4 | Cao | [PLAN_47_PAY_Payment_Sponsored_promotion_va_tracking.md](./plans/PLAN_47_PAY_Payment_Sponsored_promotion_va_tracking.md) |
| 48 | Payment — VNPAY/MoMo webhook settlement | 2 | 0/2 | Rất cao | [PLAN_48_PAY_Payment_VNPAY_MoMo_webhook_settlement.md](./plans/PLAN_48_PAY_Payment_VNPAY_MoMo_webhook_settlement.md) |
| 49 | AI — CV/JD generation, job status và human review | 4 | 1/3 | Rất cao | [PLAN_49_AIX_AI_CV_JD_generation_job_status_va_human_review.md](./plans/PLAN_49_AIX_AI_CV_JD_generation_job_status_va_human_review.md) |
| 50 | AI — Match explanation và shortlist suggestion | 2 | 0/2 | Rất cao | [PLAN_50_AIX_AI_Match_explanation_va_shortlist_suggestion.md](./plans/PLAN_50_AIX_AI_Match_explanation_va_shortlist_suggestion.md) |
| 51 | AI — Kill switch, model config, prompt policy và evaluation | 4 | 0/4 | Rất cao | [PLAN_51_AIX_AI_Kill_switch_model_config_prompt_policy_va_evaluation.md](./plans/PLAN_51_AIX_AI_Kill_switch_model_config_prompt_policy_va_evaluation.md) |
| 52 | Operations — Verification case queue và decision | 2 | 1/1 | Rất cao | [PLAN_52_OPS_Operations_Verification_case_queue_va_decision.md](./plans/PLAN_52_OPS_Operations_Verification_case_queue_va_decision.md) |
| 53 | Operations — Job review và trusted publisher grant | 4 | 1/3 | Rất cao | [PLAN_53_OPS_Operations_Job_review_va_trusted_publisher_grant.md](./plans/PLAN_53_OPS_Operations_Job_review_va_trusted_publisher_grant.md) |
| 54 | Operations — Audit export, break-glass và operational report | 4 | 2/2 | Rất cao | [PLAN_54_OPS_Operations_Audit_export_break_glass_va_operational_report.md](./plans/PLAN_54_OPS_Operations_Audit_export_break_glass_va_operational_report.md) |
| 55 | Internal — Identity projection và identity event ingestion | 3 | 1/2 | Rất cao | [PLAN_55_INT_Internal_Identity_projection_va_identity_event_ingestion.md](./plans/PLAN_55_INT_Internal_Identity_projection_va_identity_event_ingestion.md) |
| 56 | Internal — Evidence export request/result/revocation | 4 | 1/3 | Rất cao | [PLAN_56_INT_Internal_Evidence_export_request_result_revocation.md](./plans/PLAN_56_INT_Internal_Evidence_export_request_result_revocation.md) |
| 57 | Internal — AI callback, progress rebuild và search removal | 3 | 0/3 | Rất cao | [PLAN_57_INT_Internal_AI_callback_progress_rebuild_va_search_removal.md](./plans/PLAN_57_INT_Internal_AI_callback_progress_rebuild_va_search_removal.md) |
| 58 | Realtime — Work WebSocket contract | 1 | 1/0 | Rất cao | [PLAN_58_INT_Realtime_Work_WebSocket_contract.md](./plans/PLAN_58_INT_Realtime_Work_WebSocket_contract.md) |

## 3. Thứ tự thực thi khuyến nghị

1. IAM và internal identity projection.
2. Study catalog/profile/enrollment/progress/assessment/file/content/evidence.
3. Work candidate/job/application/ATS/interview/chat.
4. University.
5. Payment và promotion.
6. AI và governance.
7. Operations, internal jobs và realtime; sau đó chạy batch reconciliation toàn bộ.

## 4. Tài liệu điều khiển

- [Source Read Report](./00_SOURCE_READ_REPORT.md)
- [API Coverage Matrix](./API_COVERAGE_MATRIX.md)
- [Source Gaps and Conflicts](./SOURCE_GAPS_AND_CONFLICTS.md)
- [Verification Report](./VERIFICATION_REPORT.md)
- [Plan Result](./PLAN_RESULT.md)
