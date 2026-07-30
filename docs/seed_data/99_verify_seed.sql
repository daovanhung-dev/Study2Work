-- Kiểm tra số lượng dữ liệu sau khi seed.
SET search_path TO study_dev0, public;

SELECT * FROM (
    SELECT 'users'::TEXT AS table_name, COUNT(*)::BIGINT AS actual_count, 12::BIGINT AS minimum_expected FROM study_dev0.users
    UNION ALL
    SELECT 'user_profiles'::TEXT AS table_name, COUNT(*)::BIGINT AS actual_count, 12::BIGINT AS minimum_expected FROM study_dev0.user_profiles
    UNION ALL
    SELECT 'roles'::TEXT AS table_name, COUNT(*)::BIGINT AS actual_count, 6::BIGINT AS minimum_expected FROM study_dev0.roles
    UNION ALL
    SELECT 'user_roles'::TEXT AS table_name, COUNT(*)::BIGINT AS actual_count, 16::BIGINT AS minimum_expected FROM study_dev0.user_roles
    UNION ALL
    SELECT 'learning_paths'::TEXT AS table_name, COUNT(*)::BIGINT AS actual_count, 4::BIGINT AS minimum_expected FROM study_dev0.learning_paths
    UNION ALL
    SELECT 'onboarding_records'::TEXT AS table_name, COUNT(*)::BIGINT AS actual_count, 10::BIGINT AS minimum_expected FROM study_dev0.onboarding_records
    UNION ALL
    SELECT 'courses'::TEXT AS table_name, COUNT(*)::BIGINT AS actual_count, 8::BIGINT AS minimum_expected FROM study_dev0.courses
    UNION ALL
    SELECT 'learning_path_courses'::TEXT AS table_name, COUNT(*)::BIGINT AS actual_count, 16::BIGINT AS minimum_expected FROM study_dev0.learning_path_courses
    UNION ALL
    SELECT 'learning_path_enrollments'::TEXT AS table_name, COUNT(*)::BIGINT AS actual_count, 10::BIGINT AS minimum_expected FROM study_dev0.learning_path_enrollments
    UNION ALL
    SELECT 'course_enrollments'::TEXT AS table_name, COUNT(*)::BIGINT AS actual_count, 16::BIGINT AS minimum_expected FROM study_dev0.course_enrollments
    UNION ALL
    SELECT 'chapters'::TEXT AS table_name, COUNT(*)::BIGINT AS actual_count, 16::BIGINT AS minimum_expected FROM study_dev0.chapters
    UNION ALL
    SELECT 'lessons'::TEXT AS table_name, COUNT(*)::BIGINT AS actual_count, 32::BIGINT AS minimum_expected FROM study_dev0.lessons
    UNION ALL
    SELECT 'course_materials'::TEXT AS table_name, COUNT(*)::BIGINT AS actual_count, 32::BIGINT AS minimum_expected FROM study_dev0.course_materials
    UNION ALL
    SELECT 'exercises'::TEXT AS table_name, COUNT(*)::BIGINT AS actual_count, 14::BIGINT AS minimum_expected FROM study_dev0.exercises
    UNION ALL
    SELECT 'exercise_submissions'::TEXT AS table_name, COUNT(*)::BIGINT AS actual_count, 14::BIGINT AS minimum_expected FROM study_dev0.exercise_submissions
    UNION ALL
    SELECT 'lesson_progress'::TEXT AS table_name, COUNT(*)::BIGINT AS actual_count, 24::BIGINT AS minimum_expected FROM study_dev0.lesson_progress
    UNION ALL
    SELECT 'completion_rules'::TEXT AS table_name, COUNT(*)::BIGINT AS actual_count, 12::BIGINT AS minimum_expected FROM study_dev0.completion_rules
    UNION ALL
    SELECT 'notification_settings'::TEXT AS table_name, COUNT(*)::BIGINT AS actual_count, 12::BIGINT AS minimum_expected FROM study_dev0.notification_settings
    UNION ALL
    SELECT 'notifications'::TEXT AS table_name, COUNT(*)::BIGINT AS actual_count, 20::BIGINT AS minimum_expected FROM study_dev0.notifications
    UNION ALL
    SELECT 'community_groups'::TEXT AS table_name, COUNT(*)::BIGINT AS actual_count, 6::BIGINT AS minimum_expected FROM study_dev0.community_groups
    UNION ALL
    SELECT 'community_join_events'::TEXT AS table_name, COUNT(*)::BIGINT AS actual_count, 12::BIGINT AS minimum_expected FROM study_dev0.community_join_events
    UNION ALL
    SELECT 'support_requests'::TEXT AS table_name, COUNT(*)::BIGINT AS actual_count, 6::BIGINT AS minimum_expected FROM study_dev0.support_requests
    UNION ALL
    SELECT 'audit_logs'::TEXT AS table_name, COUNT(*)::BIGINT AS actual_count, 12::BIGINT AS minimum_expected FROM study_dev0.audit_logs
) AS counts
ORDER BY table_name;

-- Kiểm tra khóa ngoại mồ côi cơ bản.
SELECT 'user_profiles_without_user' AS check_name, COUNT(*) AS issue_count
FROM study_dev0.user_profiles p
LEFT JOIN study_dev0.users u ON u.id = p.user_id
WHERE u.id IS NULL
UNION ALL
SELECT 'lessons_without_chapter', COUNT(*)
FROM study_dev0.lessons l
LEFT JOIN study_dev0.chapters c ON c.id = l.chapter_id
WHERE c.id IS NULL
UNION ALL
SELECT 'submissions_without_exercise', COUNT(*)
FROM study_dev0.exercise_submissions s
LEFT JOIN study_dev0.exercises e ON e.id = s.exercise_id
WHERE e.id IS NULL;
