-- CẢNH BÁO: Xóa toàn bộ dữ liệu trong schema study_dev0.
-- Chỉ sử dụng ở môi trường development/test.

TRUNCATE TABLE
    study_dev0.audit_logs,
    study_dev0.support_requests,
    study_dev0.community_join_events,
    study_dev0.community_groups,
    study_dev0.notifications,
    study_dev0.notification_settings,
    study_dev0.completion_rules,
    study_dev0.lesson_progress,
    study_dev0.exercise_submissions,
    study_dev0.exercises,
    study_dev0.course_materials,
    study_dev0.lessons,
    study_dev0.chapters,
    study_dev0.course_enrollments,
    study_dev0.learning_path_enrollments,
    study_dev0.learning_path_courses,
    study_dev0.courses,
    study_dev0.onboarding_records,
    study_dev0.learning_paths,
    study_dev0.user_roles,
    study_dev0.roles,
    study_dev0.user_profiles,
    study_dev0.users
RESTART IDENTITY CASCADE;
