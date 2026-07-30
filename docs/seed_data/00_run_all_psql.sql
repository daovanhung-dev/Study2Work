\set ON_ERROR_STOP on
\echo 'Seeding Study2Work fake data into study_dev0...'
\ir 01_users.sql
\ir 02_user_profiles.sql
\ir 03_roles.sql
\ir 04_user_roles.sql
\ir 05_learning_paths.sql
\ir 06_onboarding_records.sql
\ir 07_courses.sql
\ir 08_learning_path_courses.sql
\ir 09_learning_path_enrollments.sql
\ir 10_course_enrollments.sql
\ir 11_chapters.sql
\ir 12_lessons.sql
\ir 13_course_materials.sql
\ir 14_exercises.sql
\ir 15_exercise_submissions.sql
\ir 16_lesson_progress.sql
\ir 17_completion_rules.sql
\ir 18_notification_settings.sql
\ir 19_notifications.sql
\ir 20_community_groups.sql
\ir 21_community_join_events.sql
\ir 22_support_requests.sql
\ir 23_audit_logs.sql
\echo 'Seed completed.'
