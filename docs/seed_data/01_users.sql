-- ============================================================================
-- Fake data: study_dev0.users
-- Có thể chạy lại nhiều lần nhờ ON CONFLICT DO NOTHING.
-- ============================================================================

SET search_path TO study_dev0, public;

INSERT INTO study_dev0.users (
    id,
    display_name,
    email,
    phone,
    account_status,
    contact_verified,
    created_at,
    updated_at
) VALUES
    ('10000000-0000-0000-0000-000000000001', 'Đào Văn Hùng', 'hung.dao@s2w.dev', '0901000001', 'READY_TO_LEARN', TRUE, '2026-06-01 08:00:00+07', '2026-07-20 09:00:00+07'),
    ('10000000-0000-0000-0000-000000000002', 'Nguyễn Minh Anh', 'minhanh.nguyen@s2w.dev', '0901000002', 'ACTIVE', TRUE, '2026-06-02 08:15:00+07', '2026-07-20 09:10:00+07'),
    ('10000000-0000-0000-0000-000000000003', 'Trần Quang Nam', 'quangnam.tran@s2w.dev', '0901000003', 'ACTIVE', TRUE, '2026-06-03 09:00:00+07', '2026-07-19 18:30:00+07'),
    ('10000000-0000-0000-0000-000000000004', 'Lê Thu Trang', 'thutrang.le@s2w.dev', '0901000004', 'ONBOARDING_IN_PROGRESS', TRUE, '2026-06-04 10:00:00+07', '2026-07-18 11:00:00+07'),
    ('10000000-0000-0000-0000-000000000005', 'Phạm Gia Bảo', 'giabao.pham@s2w.dev', '0901000005', 'VERIFIED', TRUE, '2026-06-05 11:00:00+07', '2026-07-17 13:20:00+07'),
    ('10000000-0000-0000-0000-000000000006', 'Đỗ Hoàng Long', 'hoanglong.do@s2w.dev', '0901000006', 'SUSPENDED', TRUE, '2026-06-06 13:00:00+07', '2026-07-16 15:00:00+07'),
    ('10000000-0000-0000-0000-000000000007', 'Vũ Ngọc Mai', 'ngocmai.vu@s2w.dev', '0901000007', 'ACTIVE', TRUE, '2026-06-07 14:00:00+07', '2026-07-20 19:00:00+07'),
    ('10000000-0000-0000-0000-000000000008', 'Bùi Đức Huy', 'duchuy.bui@s2w.dev', '0901000008', 'READY_TO_LEARN', TRUE, '2026-06-08 15:00:00+07', '2026-07-18 08:00:00+07'),
    ('10000000-0000-0000-0000-000000000009', 'Hoàng Khánh Linh', 'khanhlinh.hoang@s2w.dev', '0901000009', 'REGISTERED_PENDING_VERIFICATION', FALSE, '2026-07-10 08:30:00+07', '2026-07-10 08:30:00+07'),
    ('10000000-0000-0000-0000-000000000010', 'Nguyễn Hải Yến', 'haiyen.nguyen@s2w.dev', '0901000010', 'ACTIVE', TRUE, '2026-06-10 16:00:00+07', '2026-07-21 07:45:00+07'),
    ('10000000-0000-0000-0000-000000000011', 'Admin Study2Work', 'admin@s2w.dev', '0901000011', 'ACTIVE', TRUE, '2026-05-01 08:00:00+07', '2026-07-21 08:00:00+07'),
    ('10000000-0000-0000-0000-000000000012', 'Mentor Study2Work', 'mentor@s2w.dev', '0901000012', 'ACTIVE', TRUE, '2026-05-02 08:00:00+07', '2026-07-21 08:10:00+07')
ON CONFLICT DO NOTHING;

SELECT COUNT(*) AS users_row_count
FROM study_dev0.users;
