-- ============================================================================
-- Fake data: study_dev0.course_materials
-- Có thể chạy lại nhiều lần nhờ ON CONFLICT DO NOTHING.
-- ============================================================================

SET search_path TO study_dev0, public;

INSERT INTO study_dev0.course_materials (
    id,
    lesson_id,
    title,
    type,
    resource_url,
    required,
    source,
    usage_right_status
) VALUES
    ('42000000-0000-0000-0000-000000000001', '41000000-0000-0000-0000-000000000001', 'Tài liệu bài 01', 'VIDEO', 'https://cdn.s2w.dev/materials/lesson-01.mp4', TRUE, 'Study2Work Learning Team', 'OWNED'),
    ('42000000-0000-0000-0000-000000000002', '41000000-0000-0000-0000-000000000002', 'Tài liệu bài 02', 'PDF', 'https://cdn.s2w.dev/materials/lesson-02.pdf', TRUE, 'Study2Work Learning Team', 'OWNED'),
    ('42000000-0000-0000-0000-000000000003', '41000000-0000-0000-0000-000000000003', 'Tài liệu bài 03', 'MARKDOWN', 'https://cdn.s2w.dev/materials/lesson-03.md', FALSE, 'Study2Work Learning Team', 'OWNED'),
    ('42000000-0000-0000-0000-000000000004', '41000000-0000-0000-0000-000000000004', 'Tài liệu bài 04', 'CODE', 'https://cdn.s2w.dev/materials/lesson-04.zip', TRUE, 'Study2Work Learning Team', 'OWNED'),
    ('42000000-0000-0000-0000-000000000005', '41000000-0000-0000-0000-000000000005', 'Tài liệu bài 05', 'VIDEO', 'https://cdn.s2w.dev/materials/lesson-05.mp4', TRUE, 'Study2Work Learning Team', 'OWNED'),
    ('42000000-0000-0000-0000-000000000006', '41000000-0000-0000-0000-000000000006', 'Tài liệu bài 06', 'PDF', 'https://cdn.s2w.dev/materials/lesson-06.pdf', FALSE, 'Study2Work Learning Team', 'OWNED'),
    ('42000000-0000-0000-0000-000000000007', '41000000-0000-0000-0000-000000000007', 'Tài liệu bài 07', 'MARKDOWN', 'https://cdn.s2w.dev/materials/lesson-07.md', TRUE, 'Study2Work Learning Team', 'OWNED'),
    ('42000000-0000-0000-0000-000000000008', '41000000-0000-0000-0000-000000000008', 'Tài liệu bài 08', 'CODE', 'https://cdn.s2w.dev/materials/lesson-08.zip', TRUE, 'Study2Work Learning Team', 'OWNED'),
    ('42000000-0000-0000-0000-000000000009', '41000000-0000-0000-0000-000000000009', 'Tài liệu bài 09', 'VIDEO', 'https://cdn.s2w.dev/materials/lesson-09.mp4', FALSE, 'Study2Work Learning Team', 'OWNED'),
    ('42000000-0000-0000-0000-000000000010', '41000000-0000-0000-0000-000000000010', 'Tài liệu bài 10', 'PDF', 'https://cdn.s2w.dev/materials/lesson-10.pdf', TRUE, 'Study2Work Learning Team', 'OWNED'),
    ('42000000-0000-0000-0000-000000000011', '41000000-0000-0000-0000-000000000011', 'Tài liệu bài 11', 'MARKDOWN', 'https://cdn.s2w.dev/materials/lesson-11.md', TRUE, 'Study2Work Learning Team', 'OWNED'),
    ('42000000-0000-0000-0000-000000000012', '41000000-0000-0000-0000-000000000012', 'Tài liệu bài 12', 'CODE', 'https://cdn.s2w.dev/materials/lesson-12.zip', FALSE, 'Study2Work Learning Team', 'OWNED'),
    ('42000000-0000-0000-0000-000000000013', '41000000-0000-0000-0000-000000000013', 'Tài liệu bài 13', 'VIDEO', 'https://cdn.s2w.dev/materials/lesson-13.mp4', TRUE, 'Study2Work Learning Team', 'OWNED'),
    ('42000000-0000-0000-0000-000000000014', '41000000-0000-0000-0000-000000000014', 'Tài liệu bài 14', 'PDF', 'https://cdn.s2w.dev/materials/lesson-14.pdf', TRUE, 'Study2Work Learning Team', 'OWNED'),
    ('42000000-0000-0000-0000-000000000015', '41000000-0000-0000-0000-000000000015', 'Tài liệu bài 15', 'MARKDOWN', 'https://cdn.s2w.dev/materials/lesson-15.md', FALSE, 'Study2Work Learning Team', 'OWNED'),
    ('42000000-0000-0000-0000-000000000016', '41000000-0000-0000-0000-000000000016', 'Tài liệu bài 16', 'CODE', 'https://cdn.s2w.dev/materials/lesson-16.zip', TRUE, 'Study2Work Learning Team', 'OWNED'),
    ('42000000-0000-0000-0000-000000000017', '41000000-0000-0000-0000-000000000017', 'Tài liệu bài 17', 'VIDEO', 'https://cdn.s2w.dev/materials/lesson-17.mp4', TRUE, 'Study2Work Learning Team', 'OWNED'),
    ('42000000-0000-0000-0000-000000000018', '41000000-0000-0000-0000-000000000018', 'Tài liệu bài 18', 'PDF', 'https://cdn.s2w.dev/materials/lesson-18.pdf', FALSE, 'Study2Work Learning Team', 'OWNED'),
    ('42000000-0000-0000-0000-000000000019', '41000000-0000-0000-0000-000000000019', 'Tài liệu bài 19', 'MARKDOWN', 'https://cdn.s2w.dev/materials/lesson-19.md', TRUE, 'Study2Work Learning Team', 'OWNED'),
    ('42000000-0000-0000-0000-000000000020', '41000000-0000-0000-0000-000000000020', 'Tài liệu bài 20', 'CODE', 'https://cdn.s2w.dev/materials/lesson-20.zip', TRUE, 'Study2Work Learning Team', 'OWNED'),
    ('42000000-0000-0000-0000-000000000021', '41000000-0000-0000-0000-000000000021', 'Tài liệu bài 21', 'VIDEO', 'https://cdn.s2w.dev/materials/lesson-21.mp4', FALSE, 'Study2Work Learning Team', 'OWNED'),
    ('42000000-0000-0000-0000-000000000022', '41000000-0000-0000-0000-000000000022', 'Tài liệu bài 22', 'PDF', 'https://cdn.s2w.dev/materials/lesson-22.pdf', TRUE, 'Study2Work Learning Team', 'OWNED'),
    ('42000000-0000-0000-0000-000000000023', '41000000-0000-0000-0000-000000000023', 'Tài liệu bài 23', 'MARKDOWN', 'https://cdn.s2w.dev/materials/lesson-23.md', TRUE, 'Study2Work Learning Team', 'OWNED'),
    ('42000000-0000-0000-0000-000000000024', '41000000-0000-0000-0000-000000000024', 'Tài liệu bài 24', 'CODE', 'https://cdn.s2w.dev/materials/lesson-24.zip', FALSE, 'Study2Work Learning Team', 'OWNED'),
    ('42000000-0000-0000-0000-000000000025', '41000000-0000-0000-0000-000000000025', 'Tài liệu bài 25', 'VIDEO', 'https://cdn.s2w.dev/materials/lesson-25.mp4', TRUE, 'Study2Work Learning Team', 'OWNED'),
    ('42000000-0000-0000-0000-000000000026', '41000000-0000-0000-0000-000000000026', 'Tài liệu bài 26', 'PDF', 'https://cdn.s2w.dev/materials/lesson-26.pdf', TRUE, 'Study2Work Learning Team', 'OWNED'),
    ('42000000-0000-0000-0000-000000000027', '41000000-0000-0000-0000-000000000027', 'Tài liệu bài 27', 'MARKDOWN', 'https://cdn.s2w.dev/materials/lesson-27.md', FALSE, 'Study2Work Learning Team', 'OWNED'),
    ('42000000-0000-0000-0000-000000000028', '41000000-0000-0000-0000-000000000028', 'Tài liệu bài 28', 'CODE', 'https://cdn.s2w.dev/materials/lesson-28.zip', TRUE, 'Study2Work Learning Team', 'OWNED'),
    ('42000000-0000-0000-0000-000000000029', '41000000-0000-0000-0000-000000000029', 'Tài liệu bài 29', 'VIDEO', 'https://cdn.s2w.dev/materials/lesson-29.mp4', TRUE, 'Study2Work Learning Team', 'OWNED'),
    ('42000000-0000-0000-0000-000000000030', '41000000-0000-0000-0000-000000000030', 'Tài liệu bài 30', 'PDF', 'https://cdn.s2w.dev/materials/lesson-30.pdf', FALSE, 'Study2Work Learning Team', 'OWNED'),
    ('42000000-0000-0000-0000-000000000031', '41000000-0000-0000-0000-000000000031', 'Tài liệu bài 31', 'MARKDOWN', 'https://cdn.s2w.dev/materials/lesson-31.md', TRUE, 'Study2Work Learning Team', 'OWNED'),
    ('42000000-0000-0000-0000-000000000032', '41000000-0000-0000-0000-000000000032', 'Tài liệu bài 32', 'CODE', 'https://cdn.s2w.dev/materials/lesson-32.zip', TRUE, 'Study2Work Learning Team', 'OWNED')
ON CONFLICT DO NOTHING;

SELECT COUNT(*) AS course_materials_row_count
FROM study_dev0.course_materials;
