-- LEGACY / DESIGN-ONLY — Study2Work Work clean MySQL schema bootstrap.
--
-- This file is retained as a legacy design artifact. It is derived from the
-- Work web route/domain declarations and is intentionally independent from the
-- PostgreSQL/Prisma runtime in apps/work-server. It is not a Prisma migration
-- and must not be used to initialize the Work runtime.
-- Authentication remains owned by the external Identity service: no password,
-- access token, or refresh token is stored here.
--
-- Target: MySQL 8.0.16+.
-- Run this file against an empty MySQL instance/database. It contains no seed
-- data, trigger, stored procedure, user grant, or destructive DROP statement.

CREATE DATABASE IF NOT EXISTS `study2work_work`
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_0900_ai_ci;

USE `study2work_work`;

SET NAMES utf8mb4 COLLATE utf8mb4_0900_ai_ci;
SET time_zone = '+00:00';

-- ---------------------------------------------------------------------------
-- Foundation and tenancy
-- ---------------------------------------------------------------------------

CREATE TABLE `system_records` (
  `id` CHAR(36) NOT NULL,
  `key` VARCHAR(120) NOT NULL,
  `value` TEXT NULL,
  `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
    ON UPDATE CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_system_records_key` (`key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `work_users` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `identity_subject_id` VARCHAR(191) NOT NULL,
  `email` VARCHAR(320) NULL,
  `full_name` VARCHAR(150) NULL,
  `avatar_url` VARCHAR(2048) NULL,
  `bio` TEXT NULL,
  `phone` VARCHAR(32) NULL,
  `account_status` VARCHAR(32) NOT NULL DEFAULT 'ACTIVE',
  `email_verified` TINYINT(1) NOT NULL DEFAULT 0,
  `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
    ON UPDATE CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_work_users_identity_subject_id` (`identity_subject_id`),
  KEY `ix_work_users_account_status` (`account_status`),
  KEY `ix_work_users_email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `tenants` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `tenant_type` VARCHAR(32) NOT NULL,
  `slug` VARCHAR(191) NOT NULL,
  `display_name` VARCHAR(200) NOT NULL,
  `status` VARCHAR(32) NOT NULL DEFAULT 'PENDING',
  `verification_status` VARCHAR(32) NOT NULL DEFAULT 'UNVERIFIED',
  `created_by_user_id` BIGINT UNSIGNED NULL,
  `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
    ON UPDATE CURRENT_TIMESTAMP(6),
  `deleted_at` DATETIME(6) NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_tenants_slug` (`slug`),
  KEY `ix_tenants_type_status` (`tenant_type`, `status`),
  CONSTRAINT `fk_tenants_created_by_user`
    FOREIGN KEY (`created_by_user_id`) REFERENCES `work_users` (`id`)
    ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `chk_tenants_type`
    CHECK (`tenant_type` IN ('ENTERPRISE', 'UNIVERSITY'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `enterprise_profiles` (
  `tenant_id` BIGINT UNSIGNED NOT NULL,
  `legal_name` VARCHAR(255) NOT NULL,
  `public_name` VARCHAR(255) NULL,
  `registration_number` VARCHAR(120) NULL,
  `description` TEXT NULL,
  `website_url` VARCHAR(2048) NULL,
  `contact_email` VARCHAR(320) NULL,
  `contact_phone` VARCHAR(32) NULL,
  `address_line` VARCHAR(255) NULL,
  `city` VARCHAR(120) NULL,
  `country_code` CHAR(2) NULL,
  `verified_at` DATETIME(6) NULL,
  `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
    ON UPDATE CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`tenant_id`),
  UNIQUE KEY `uq_enterprise_profiles_registration_number` (`registration_number`),
  CONSTRAINT `fk_enterprise_profiles_tenant`
    FOREIGN KEY (`tenant_id`) REFERENCES `tenants` (`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `university_profiles` (
  `tenant_id` BIGINT UNSIGNED NOT NULL,
  `legal_name` VARCHAR(255) NOT NULL,
  `public_name` VARCHAR(255) NULL,
  `campus_code` VARCHAR(120) NULL,
  `description` TEXT NULL,
  `website_url` VARCHAR(2048) NULL,
  `contact_email` VARCHAR(320) NULL,
  `contact_phone` VARCHAR(32) NULL,
  `address_line` VARCHAR(255) NULL,
  `city` VARCHAR(120) NULL,
  `country_code` CHAR(2) NULL,
  `verified_at` DATETIME(6) NULL,
  `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
    ON UPDATE CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`tenant_id`),
  UNIQUE KEY `uq_university_profiles_campus_code` (`campus_code`),
  CONSTRAINT `fk_university_profiles_tenant`
    FOREIGN KEY (`tenant_id`) REFERENCES `tenants` (`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `tenant_memberships` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `tenant_id` BIGINT UNSIGNED NOT NULL,
  `user_id` BIGINT UNSIGNED NOT NULL,
  `status` VARCHAR(32) NOT NULL DEFAULT 'INVITED',
  `membership_version` INT UNSIGNED NOT NULL DEFAULT 1,
  `permission_codes_json` JSON NULL,
  `invited_by_user_id` BIGINT UNSIGNED NULL,
  `invited_at` DATETIME(6) NULL,
  `accepted_at` DATETIME(6) NULL,
  `revoked_at` DATETIME(6) NULL,
  `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
    ON UPDATE CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_tenant_memberships_tenant_user` (`tenant_id`, `user_id`),
  KEY `ix_tenant_memberships_user_status` (`user_id`, `status`),
  CONSTRAINT `fk_tenant_memberships_tenant`
    FOREIGN KEY (`tenant_id`) REFERENCES `tenants` (`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_tenant_memberships_user`
    FOREIGN KEY (`user_id`) REFERENCES `work_users` (`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_tenant_memberships_invited_by_user`
    FOREIGN KEY (`invited_by_user_id`) REFERENCES `work_users` (`id`)
    ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `chk_tenant_memberships_version`
    CHECK (`membership_version` > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `membership_roles` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `membership_id` BIGINT UNSIGNED NOT NULL,
  `role_code` VARCHAR(64) NOT NULL,
  `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_membership_roles_membership_role` (`membership_id`, `role_code`),
  CONSTRAINT `fk_membership_roles_membership`
    FOREIGN KEY (`membership_id`) REFERENCES `tenant_memberships` (`id`)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ---------------------------------------------------------------------------
-- Candidate profile, privacy, skill and file data
-- ---------------------------------------------------------------------------

CREATE TABLE `candidate_profiles` (
  `user_id` BIGINT UNSIGNED NOT NULL,
  `headline` VARCHAR(255) NULL,
  `summary` TEXT NULL,
  `location_text` VARCHAR(255) NULL,
  `website_url` VARCHAR(2048) NULL,
  `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
    ON UPDATE CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`user_id`),
  CONSTRAINT `fk_candidate_profiles_user`
    FOREIGN KEY (`user_id`) REFERENCES `work_users` (`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `candidate_privacy` (
  `user_id` BIGINT UNSIGNED NOT NULL,
  `searchable` TINYINT(1) NOT NULL DEFAULT 0,
  `contact_visible` TINYINT(1) NOT NULL DEFAULT 0,
  `cv_visible` TINYINT(1) NOT NULL DEFAULT 0,
  `study_evidence_visible` TINYINT(1) NOT NULL DEFAULT 0,
  `updated_by_user_id` BIGINT UNSIGNED NULL,
  `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
    ON UPDATE CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`user_id`),
  CONSTRAINT `fk_candidate_privacy_user`
    FOREIGN KEY (`user_id`) REFERENCES `work_users` (`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_candidate_privacy_updated_by_user`
    FOREIGN KEY (`updated_by_user_id`) REFERENCES `work_users` (`id`)
    ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `skills` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(160) NOT NULL,
  `slug` VARCHAR(191) NOT NULL,
  `taxonomy_code` VARCHAR(120) NULL,
  `status` VARCHAR(32) NOT NULL DEFAULT 'ACTIVE',
  `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
    ON UPDATE CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_skills_slug` (`slug`),
  KEY `ix_skills_taxonomy_code` (`taxonomy_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `candidate_skills` (
  `candidate_user_id` BIGINT UNSIGNED NOT NULL,
  `skill_id` BIGINT UNSIGNED NOT NULL,
  `proficiency_level` VARCHAR(64) NULL,
  `years_experience` DECIMAL(5,2) NULL,
  `display_order` INT UNSIGNED NOT NULL DEFAULT 0,
  `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`candidate_user_id`, `skill_id`),
  KEY `ix_candidate_skills_skill` (`skill_id`),
  CONSTRAINT `fk_candidate_skills_candidate`
    FOREIGN KEY (`candidate_user_id`) REFERENCES `candidate_profiles` (`user_id`)
    ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_candidate_skills_skill`
    FOREIGN KEY (`skill_id`) REFERENCES `skills` (`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `chk_candidate_skills_years_experience`
    CHECK (`years_experience` IS NULL OR `years_experience` >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `candidate_education` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `candidate_user_id` BIGINT UNSIGNED NOT NULL,
  `institution_name` VARCHAR(255) NOT NULL,
  `degree` VARCHAR(160) NULL,
  `field_of_study` VARCHAR(160) NULL,
  `start_date` DATE NULL,
  `end_date` DATE NULL,
  `description` TEXT NULL,
  `display_order` INT UNSIGNED NOT NULL DEFAULT 0,
  `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
    ON UPDATE CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`),
  KEY `ix_candidate_education_candidate_order` (`candidate_user_id`, `display_order`),
  CONSTRAINT `fk_candidate_education_candidate`
    FOREIGN KEY (`candidate_user_id`) REFERENCES `candidate_profiles` (`user_id`)
    ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `chk_candidate_education_dates`
    CHECK (`end_date` IS NULL OR `start_date` IS NULL OR `end_date` >= `start_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `candidate_experiences` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `candidate_user_id` BIGINT UNSIGNED NOT NULL,
  `employer_name` VARCHAR(255) NOT NULL,
  `job_title` VARCHAR(200) NOT NULL,
  `description` TEXT NULL,
  `start_date` DATE NULL,
  `end_date` DATE NULL,
  `is_current` TINYINT(1) NOT NULL DEFAULT 0,
  `display_order` INT UNSIGNED NOT NULL DEFAULT 0,
  `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
    ON UPDATE CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`),
  KEY `ix_candidate_experiences_candidate_order` (`candidate_user_id`, `display_order`),
  CONSTRAINT `fk_candidate_experiences_candidate`
    FOREIGN KEY (`candidate_user_id`) REFERENCES `candidate_profiles` (`user_id`)
    ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `chk_candidate_experiences_dates`
    CHECK (`end_date` IS NULL OR `start_date` IS NULL OR `end_date` >= `start_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `search_consents` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `candidate_user_id` BIGINT UNSIGNED NOT NULL,
  `purpose` VARCHAR(120) NOT NULL,
  `consent_status` VARCHAR(32) NOT NULL,
  `consent_version` VARCHAR(64) NOT NULL,
  `visible_fields_json` JSON NULL,
  `effective_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `expires_at` DATETIME(6) NULL,
  `withdrawn_at` DATETIME(6) NULL,
  `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`),
  KEY `ix_search_consents_candidate_status` (`candidate_user_id`, `consent_status`),
  CONSTRAINT `fk_search_consents_candidate`
    FOREIGN KEY (`candidate_user_id`) REFERENCES `candidate_profiles` (`user_id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `chk_search_consents_dates`
    CHECK (`expires_at` IS NULL OR `expires_at` >= `effective_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `file_assets` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `owner_user_id` BIGINT UNSIGNED NULL,
  `owner_tenant_id` BIGINT UNSIGNED NULL,
  `storage_provider` VARCHAR(32) NOT NULL,
  -- 700 * 4 bytes leaves headroom below InnoDB's 3072-byte index limit.
  `object_key` VARCHAR(700) NOT NULL,
  `original_name` VARCHAR(255) NOT NULL,
  `content_type` VARCHAR(160) NOT NULL,
  `size_bytes` BIGINT UNSIGNED NOT NULL,
  `checksum_sha256` CHAR(64) NULL,
  `purpose` VARCHAR(64) NOT NULL,
  `clean_status` VARCHAR(32) NOT NULL DEFAULT 'PENDING',
  `visibility` VARCHAR(32) NOT NULL DEFAULT 'PRIVATE',
  `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
    ON UPDATE CURRENT_TIMESTAMP(6),
  `deleted_at` DATETIME(6) NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_file_assets_object_key` (`object_key`),
  KEY `ix_file_assets_user_status` (`owner_user_id`, `clean_status`),
  KEY `ix_file_assets_tenant_status` (`owner_tenant_id`, `clean_status`),
  CONSTRAINT `fk_file_assets_owner_user`
    FOREIGN KEY (`owner_user_id`) REFERENCES `work_users` (`id`)
    ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_file_assets_owner_tenant`
    FOREIGN KEY (`owner_tenant_id`) REFERENCES `tenants` (`id`)
    ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `chk_file_assets_owner`
    CHECK (`owner_user_id` IS NOT NULL OR `owner_tenant_id` IS NOT NULL)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ---------------------------------------------------------------------------
-- CV and portfolio
-- ---------------------------------------------------------------------------

CREATE TABLE `cvs` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `candidate_user_id` BIGINT UNSIGNED NOT NULL,
  `title` VARCHAR(200) NOT NULL,
  `status` VARCHAR(32) NOT NULL DEFAULT 'DRAFT',
  `is_default` TINYINT(1) NOT NULL DEFAULT 0,
  `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
    ON UPDATE CURRENT_TIMESTAMP(6),
  `deleted_at` DATETIME(6) NULL,
  PRIMARY KEY (`id`),
  KEY `ix_cvs_candidate_status` (`candidate_user_id`, `status`),
  CONSTRAINT `fk_cvs_candidate`
    FOREIGN KEY (`candidate_user_id`) REFERENCES `candidate_profiles` (`user_id`)
    ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `cv_revisions` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `cv_id` BIGINT UNSIGNED NOT NULL,
  `revision_number` INT UNSIGNED NOT NULL,
  `version` INT UNSIGNED NOT NULL DEFAULT 1,
  `status` VARCHAR(32) NOT NULL DEFAULT 'DRAFT',
  `content_json` JSON NULL,
  `created_by_user_id` BIGINT UNSIGNED NOT NULL,
  `published_at` DATETIME(6) NULL,
  `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
    ON UPDATE CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_cv_revisions_cv_revision` (`cv_id`, `revision_number`),
  KEY `ix_cv_revisions_status` (`cv_id`, `status`),
  CONSTRAINT `fk_cv_revisions_cv`
    FOREIGN KEY (`cv_id`) REFERENCES `cvs` (`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_cv_revisions_created_by_user`
    FOREIGN KEY (`created_by_user_id`) REFERENCES `work_users` (`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `chk_cv_revisions_numbers`
    CHECK (`revision_number` > 0 AND `version` > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `cv_revision_sections` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `cv_revision_id` BIGINT UNSIGNED NOT NULL,
  `section_type` VARCHAR(64) NOT NULL,
  `section_order` INT UNSIGNED NOT NULL DEFAULT 0,
  `payload_json` JSON NOT NULL,
  `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_cv_revision_sections_order` (`cv_revision_id`, `section_order`),
  KEY `ix_cv_revision_sections_type` (`cv_revision_id`, `section_type`),
  CONSTRAINT `fk_cv_revision_sections_revision`
    FOREIGN KEY (`cv_revision_id`) REFERENCES `cv_revisions` (`id`)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `portfolio_items` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `candidate_user_id` BIGINT UNSIGNED NOT NULL,
  `file_asset_id` BIGINT UNSIGNED NULL,
  `title` VARCHAR(200) NOT NULL,
  `description` TEXT NULL,
  `item_type` VARCHAR(32) NOT NULL,
  `url` VARCHAR(2048) NULL,
  `visibility` VARCHAR(32) NOT NULL DEFAULT 'PRIVATE',
  `status` VARCHAR(32) NOT NULL DEFAULT 'ACTIVE',
  `display_order` INT UNSIGNED NOT NULL DEFAULT 0,
  `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
    ON UPDATE CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`),
  KEY `ix_portfolio_items_candidate_visibility` (`candidate_user_id`, `visibility`, `status`),
  CONSTRAINT `fk_portfolio_items_candidate`
    FOREIGN KEY (`candidate_user_id`) REFERENCES `candidate_profiles` (`user_id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_portfolio_items_file_asset`
    FOREIGN KEY (`file_asset_id`) REFERENCES `file_assets` (`id`)
    ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ---------------------------------------------------------------------------
-- Jobs and recruitment
-- ---------------------------------------------------------------------------

CREATE TABLE `jobs` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `tenant_id` BIGINT UNSIGNED NOT NULL,
  `public_slug` VARCHAR(191) NULL,
  `status` VARCHAR(32) NOT NULL DEFAULT 'DRAFT',
  `visibility` VARCHAR(32) NOT NULL DEFAULT 'PRIVATE',
  `published_revision_id` BIGINT UNSIGNED NULL,
  `created_by_user_id` BIGINT UNSIGNED NOT NULL,
  `published_at` DATETIME(6) NULL,
  `closed_at` DATETIME(6) NULL,
  `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
    ON UPDATE CURRENT_TIMESTAMP(6),
  `deleted_at` DATETIME(6) NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_jobs_public_slug` (`public_slug`),
  KEY `ix_jobs_tenant_status` (`tenant_id`, `status`),
  KEY `ix_jobs_public_listing` (`status`, `visibility`, `published_at`),
  CONSTRAINT `fk_jobs_tenant`
    FOREIGN KEY (`tenant_id`) REFERENCES `tenants` (`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_jobs_created_by_user`
    FOREIGN KEY (`created_by_user_id`) REFERENCES `work_users` (`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `job_revisions` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `job_id` BIGINT UNSIGNED NOT NULL,
  `revision_number` INT UNSIGNED NOT NULL,
  `version` INT UNSIGNED NOT NULL DEFAULT 1,
  `status` VARCHAR(32) NOT NULL DEFAULT 'DRAFT',
  `title` VARCHAR(255) NOT NULL,
  `summary` TEXT NULL,
  `description` LONGTEXT NULL,
  `employment_type` VARCHAR(64) NULL,
  `seniority` VARCHAR(64) NULL,
  `salary_min` DECIMAL(20,4) NULL,
  `salary_max` DECIMAL(20,4) NULL,
  `salary_currency` CHAR(3) NULL,
  `location_mode` VARCHAR(32) NULL,
  `application_deadline` DATETIME(6) NULL,
  `requirements_json` JSON NULL,
  `benefits_json` JSON NULL,
  `application_questions_json` JSON NULL,
  `created_by_user_id` BIGINT UNSIGNED NOT NULL,
  `published_at` DATETIME(6) NULL,
  `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
    ON UPDATE CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_job_revisions_job_revision` (`job_id`, `revision_number`),
  KEY `ix_job_revisions_job_status` (`job_id`, `status`),
  CONSTRAINT `fk_job_revisions_job`
    FOREIGN KEY (`job_id`) REFERENCES `jobs` (`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_job_revisions_created_by_user`
    FOREIGN KEY (`created_by_user_id`) REFERENCES `work_users` (`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `chk_job_revisions_numbers`
    CHECK (`revision_number` > 0 AND `version` > 0),
  CONSTRAINT `chk_job_revisions_salary`
    CHECK (
      (`salary_min` IS NULL OR `salary_min` >= 0)
      AND (`salary_max` IS NULL OR `salary_max` >= 0)
      AND (
        `salary_min` IS NULL OR `salary_max` IS NULL OR `salary_max` >= `salary_min`
      )
    )
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

ALTER TABLE `jobs`
  ADD CONSTRAINT `fk_jobs_published_revision`
    FOREIGN KEY (`published_revision_id`) REFERENCES `job_revisions` (`id`)
    ON DELETE SET NULL ON UPDATE CASCADE;

CREATE TABLE `job_revision_skills` (
  `job_revision_id` BIGINT UNSIGNED NOT NULL,
  `skill_id` BIGINT UNSIGNED NOT NULL,
  `is_required` TINYINT(1) NOT NULL DEFAULT 0,
  `display_order` INT UNSIGNED NOT NULL DEFAULT 0,
  PRIMARY KEY (`job_revision_id`, `skill_id`),
  KEY `ix_job_revision_skills_skill` (`skill_id`),
  CONSTRAINT `fk_job_revision_skills_revision`
    FOREIGN KEY (`job_revision_id`) REFERENCES `job_revisions` (`id`)
    ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_job_revision_skills_skill`
    FOREIGN KEY (`skill_id`) REFERENCES `skills` (`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `job_revision_locations` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `job_revision_id` BIGINT UNSIGNED NOT NULL,
  `country_code` CHAR(2) NULL,
  `region` VARCHAR(120) NULL,
  `city` VARCHAR(120) NULL,
  `address_line` VARCHAR(255) NULL,
  `remote_allowed` TINYINT(1) NOT NULL DEFAULT 0,
  `display_order` INT UNSIGNED NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  KEY `ix_job_revision_locations_revision_order` (`job_revision_id`, `display_order`),
  KEY `ix_job_revision_locations_city` (`city`),
  CONSTRAINT `fk_job_revision_locations_revision`
    FOREIGN KEY (`job_revision_id`) REFERENCES `job_revisions` (`id`)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `saved_jobs` (
  `candidate_user_id` BIGINT UNSIGNED NOT NULL,
  `job_id` BIGINT UNSIGNED NOT NULL,
  `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`candidate_user_id`, `job_id`),
  KEY `ix_saved_jobs_job` (`job_id`),
  CONSTRAINT `fk_saved_jobs_candidate`
    FOREIGN KEY (`candidate_user_id`) REFERENCES `candidate_profiles` (`user_id`)
    ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_saved_jobs_job`
    FOREIGN KEY (`job_id`) REFERENCES `jobs` (`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `candidate_invitations` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `tenant_id` BIGINT UNSIGNED NOT NULL,
  `job_id` BIGINT UNSIGNED NOT NULL,
  `candidate_user_id` BIGINT UNSIGNED NOT NULL,
  `invited_by_user_id` BIGINT UNSIGNED NOT NULL,
  `status` VARCHAR(32) NOT NULL DEFAULT 'PENDING',
  `message` TEXT NULL,
  `expires_at` DATETIME(6) NULL,
  `responded_at` DATETIME(6) NULL,
  `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
    ON UPDATE CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`),
  KEY `ix_candidate_invitations_candidate_status` (`candidate_user_id`, `status`),
  KEY `ix_candidate_invitations_job_status` (`job_id`, `status`),
  CONSTRAINT `fk_candidate_invitations_tenant`
    FOREIGN KEY (`tenant_id`) REFERENCES `tenants` (`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_candidate_invitations_job`
    FOREIGN KEY (`job_id`) REFERENCES `jobs` (`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_candidate_invitations_candidate`
    FOREIGN KEY (`candidate_user_id`) REFERENCES `candidate_profiles` (`user_id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_candidate_invitations_invited_by_user`
    FOREIGN KEY (`invited_by_user_id`) REFERENCES `work_users` (`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `chk_candidate_invitations_expiry`
    CHECK (`expires_at` IS NULL OR `expires_at` >= `created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ---------------------------------------------------------------------------
-- Study evidence integration and applications
-- ---------------------------------------------------------------------------

CREATE TABLE `study_evidence_records` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `candidate_user_id` BIGINT UNSIGNED NULL,
  `external_evidence_id` VARCHAR(191) NOT NULL,
  `source_event_id` CHAR(36) NOT NULL,
  `status` VARCHAR(32) NOT NULL DEFAULT 'PENDING',
  `payload_hash` CHAR(64) NOT NULL,
  `payload_json` JSON NULL,
  `received_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `revoked_at` DATETIME(6) NULL,
  `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
    ON UPDATE CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_study_evidence_external_id` (`external_evidence_id`),
  UNIQUE KEY `uq_study_evidence_source_event_id` (`source_event_id`),
  KEY `ix_study_evidence_candidate_status` (`candidate_user_id`, `status`),
  CONSTRAINT `fk_study_evidence_candidate`
    FOREIGN KEY (`candidate_user_id`) REFERENCES `candidate_profiles` (`user_id`)
    ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `applications` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `job_id` BIGINT UNSIGNED NOT NULL,
  `candidate_user_id` BIGINT UNSIGNED NOT NULL,
  `job_revision_id` BIGINT UNSIGNED NOT NULL,
  `cv_id` BIGINT UNSIGNED NOT NULL,
  `cv_revision_id` BIGINT UNSIGNED NOT NULL,
  `invitation_id` BIGINT UNSIGNED NULL,
  `status` VARCHAR(32) NOT NULL DEFAULT 'SUBMITTED',
  `source` VARCHAR(64) NULL,
  `job_snapshot_json` JSON NOT NULL,
  `cv_snapshot_json` JSON NOT NULL,
  `answers_snapshot_json` JSON NULL,
  `evidence_status` VARCHAR(32) NOT NULL DEFAULT 'UNAVAILABLE',
  `submitted_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `withdrawn_at` DATETIME(6) NULL,
  `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
    ON UPDATE CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_applications_job_candidate` (`job_id`, `candidate_user_id`),
  KEY `ix_applications_candidate_status` (`candidate_user_id`, `status`),
  KEY `ix_applications_job_status` (`job_id`, `status`),
  KEY `ix_applications_invitation` (`invitation_id`),
  CONSTRAINT `fk_applications_job`
    FOREIGN KEY (`job_id`) REFERENCES `jobs` (`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_applications_candidate`
    FOREIGN KEY (`candidate_user_id`) REFERENCES `candidate_profiles` (`user_id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_applications_job_revision`
    FOREIGN KEY (`job_revision_id`) REFERENCES `job_revisions` (`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_applications_cv`
    FOREIGN KEY (`cv_id`) REFERENCES `cvs` (`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_applications_cv_revision`
    FOREIGN KEY (`cv_revision_id`) REFERENCES `cv_revisions` (`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_applications_invitation`
    FOREIGN KEY (`invitation_id`) REFERENCES `candidate_invitations` (`id`)
    ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `application_answers` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `application_id` BIGINT UNSIGNED NOT NULL,
  `question_key` VARCHAR(120) NOT NULL,
  `answer_json` JSON NOT NULL,
  `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_application_answers_question` (`application_id`, `question_key`),
  CONSTRAINT `fk_application_answers_application`
    FOREIGN KEY (`application_id`) REFERENCES `applications` (`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `application_status_history` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `application_id` BIGINT UNSIGNED NOT NULL,
  `from_status` VARCHAR(32) NULL,
  `to_status` VARCHAR(32) NOT NULL,
  `changed_by_user_id` BIGINT UNSIGNED NOT NULL,
  `reason` TEXT NULL,
  `metadata_json` JSON NULL,
  `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`),
  KEY `ix_application_status_history_application_time` (`application_id`, `created_at`),
  CONSTRAINT `fk_application_status_history_application`
    FOREIGN KEY (`application_id`) REFERENCES `applications` (`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_application_status_history_changed_by_user`
    FOREIGN KEY (`changed_by_user_id`) REFERENCES `work_users` (`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `application_assignments` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `application_id` BIGINT UNSIGNED NOT NULL,
  `recruiter_user_id` BIGINT UNSIGNED NOT NULL,
  `assigned_by_user_id` BIGINT UNSIGNED NOT NULL,
  `status` VARCHAR(32) NOT NULL DEFAULT 'ACTIVE',
  `assigned_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `removed_at` DATETIME(6) NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_application_assignments_application_recruiter` (`application_id`, `recruiter_user_id`),
  KEY `ix_application_assignments_recruiter_status` (`recruiter_user_id`, `status`),
  CONSTRAINT `fk_application_assignments_application`
    FOREIGN KEY (`application_id`) REFERENCES `applications` (`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_application_assignments_recruiter`
    FOREIGN KEY (`recruiter_user_id`) REFERENCES `work_users` (`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_application_assignments_assigned_by_user`
    FOREIGN KEY (`assigned_by_user_id`) REFERENCES `work_users` (`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `application_evidence` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `application_id` BIGINT UNSIGNED NOT NULL,
  `study_evidence_record_id` BIGINT UNSIGNED NULL,
  `external_evidence_id` VARCHAR(191) NOT NULL,
  `evidence_type` VARCHAR(64) NOT NULL,
  `status` VARCHAR(32) NOT NULL DEFAULT 'PENDING',
  `payload_hash` CHAR(64) NULL,
  `consent_status` VARCHAR(32) NOT NULL DEFAULT 'PENDING',
  `metadata_json` JSON NULL,
  `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
    ON UPDATE CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_application_evidence_application_external`
    (`application_id`, `external_evidence_id`),
  KEY `ix_application_evidence_application_status` (`application_id`, `status`),
  CONSTRAINT `fk_application_evidence_application`
    FOREIGN KEY (`application_id`) REFERENCES `applications` (`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_application_evidence_study_record`
    FOREIGN KEY (`study_evidence_record_id`) REFERENCES `study_evidence_records` (`id`)
    ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ---------------------------------------------------------------------------
-- Job review and operations support
-- ---------------------------------------------------------------------------

CREATE TABLE `job_review_cases` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `job_id` BIGINT UNSIGNED NOT NULL,
  `job_revision_id` BIGINT UNSIGNED NOT NULL,
  `status` VARCHAR(32) NOT NULL DEFAULT 'PENDING',
  `opened_by_user_id` BIGINT UNSIGNED NOT NULL,
  `resolved_by_user_id` BIGINT UNSIGNED NULL,
  `decision` VARCHAR(64) NULL,
  `decision_reason` TEXT NULL,
  `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
    ON UPDATE CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`),
  KEY `ix_job_review_cases_job_status` (`job_id`, `status`),
  KEY `ix_job_review_cases_revision` (`job_revision_id`),
  CONSTRAINT `fk_job_review_cases_job`
    FOREIGN KEY (`job_id`) REFERENCES `jobs` (`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_job_review_cases_revision`
    FOREIGN KEY (`job_revision_id`) REFERENCES `job_revisions` (`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_job_review_cases_opened_by_user`
    FOREIGN KEY (`opened_by_user_id`) REFERENCES `work_users` (`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_job_review_cases_resolved_by_user`
    FOREIGN KEY (`resolved_by_user_id`) REFERENCES `work_users` (`id`)
    ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `job_review_decisions` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `review_case_id` BIGINT UNSIGNED NOT NULL,
  `actor_user_id` BIGINT UNSIGNED NOT NULL,
  `decision` VARCHAR(64) NOT NULL,
  `reason` TEXT NULL,
  `metadata_json` JSON NULL,
  `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`),
  KEY `ix_job_review_decisions_case_time` (`review_case_id`, `created_at`),
  CONSTRAINT `fk_job_review_decisions_case`
    FOREIGN KEY (`review_case_id`) REFERENCES `job_review_cases` (`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_job_review_decisions_actor_user`
    FOREIGN KEY (`actor_user_id`) REFERENCES `work_users` (`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ---------------------------------------------------------------------------
-- University affiliations and partnerships
-- ---------------------------------------------------------------------------

CREATE TABLE `university_affiliation_invitations` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `university_tenant_id` BIGINT UNSIGNED NOT NULL,
  `candidate_user_id` BIGINT UNSIGNED NOT NULL,
  `invited_by_user_id` BIGINT UNSIGNED NOT NULL,
  `purpose` VARCHAR(255) NOT NULL,
  `scope_json` JSON NOT NULL,
  `status` VARCHAR(32) NOT NULL DEFAULT 'PENDING',
  `expires_at` DATETIME(6) NULL,
  `responded_at` DATETIME(6) NULL,
  `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
    ON UPDATE CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`),
  KEY `ix_university_affiliation_invitations_candidate_status`
    (`candidate_user_id`, `status`),
  KEY `ix_university_affiliation_invitations_tenant_status`
    (`university_tenant_id`, `status`),
  CONSTRAINT `fk_university_affiliation_invitations_tenant`
    FOREIGN KEY (`university_tenant_id`) REFERENCES `tenants` (`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_university_affiliation_invitations_candidate`
    FOREIGN KEY (`candidate_user_id`) REFERENCES `candidate_profiles` (`user_id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_university_affiliation_invitations_invited_by_user`
    FOREIGN KEY (`invited_by_user_id`) REFERENCES `work_users` (`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `chk_university_affiliation_invitations_expiry`
    CHECK (`expires_at` IS NULL OR `expires_at` >= `created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `university_affiliations` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `university_tenant_id` BIGINT UNSIGNED NOT NULL,
  `candidate_user_id` BIGINT UNSIGNED NOT NULL,
  `invitation_id` BIGINT UNSIGNED NULL,
  `status` VARCHAR(32) NOT NULL DEFAULT 'PENDING',
  `consent_scope_json` JSON NOT NULL,
  `consent_version` VARCHAR(64) NOT NULL,
  `starts_at` DATETIME(6) NULL,
  `ends_at` DATETIME(6) NULL,
  `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
    ON UPDATE CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`),
  KEY `ix_university_affiliations_candidate_status` (`candidate_user_id`, `status`),
  KEY `ix_university_affiliations_tenant_status` (`university_tenant_id`, `status`),
  CONSTRAINT `fk_university_affiliations_tenant`
    FOREIGN KEY (`university_tenant_id`) REFERENCES `tenants` (`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_university_affiliations_candidate`
    FOREIGN KEY (`candidate_user_id`) REFERENCES `candidate_profiles` (`user_id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_university_affiliations_invitation`
    FOREIGN KEY (`invitation_id`) REFERENCES `university_affiliation_invitations` (`id`)
    ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `chk_university_affiliations_dates`
    CHECK (`ends_at` IS NULL OR `starts_at` IS NULL OR `ends_at` >= `starts_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `tenant_partnerships` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `tenant_a_id` BIGINT UNSIGNED NOT NULL,
  `tenant_b_id` BIGINT UNSIGNED NOT NULL,
  `requested_by_user_id` BIGINT UNSIGNED NOT NULL,
  `purpose` VARCHAR(255) NOT NULL,
  `scope_json` JSON NOT NULL,
  `status` VARCHAR(32) NOT NULL DEFAULT 'PENDING',
  `starts_at` DATETIME(6) NULL,
  `ends_at` DATETIME(6) NULL,
  `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
    ON UPDATE CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_tenant_partnership_pair` (`tenant_a_id`, `tenant_b_id`),
  KEY `ix_tenant_partnerships_status` (`status`),
  CONSTRAINT `fk_tenant_partnerships_tenant_a`
    FOREIGN KEY (`tenant_a_id`) REFERENCES `tenants` (`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_tenant_partnerships_tenant_b`
    FOREIGN KEY (`tenant_b_id`) REFERENCES `tenants` (`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_tenant_partnerships_requested_by_user`
    FOREIGN KEY (`requested_by_user_id`) REFERENCES `work_users` (`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `chk_tenant_partnerships_distinct_tenants`
    CHECK (`tenant_a_id` <> `tenant_b_id`),
  CONSTRAINT `chk_tenant_partnerships_dates`
    CHECK (`ends_at` IS NULL OR `starts_at` IS NULL OR `ends_at` >= `starts_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ---------------------------------------------------------------------------
-- Conversation and interview scheduling
-- ---------------------------------------------------------------------------

CREATE TABLE `conversations` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `application_id` BIGINT UNSIGNED NOT NULL,
  `status` VARCHAR(32) NOT NULL DEFAULT 'OPEN',
  `last_message_sequence` BIGINT UNSIGNED NOT NULL DEFAULT 0,
  `closed_at` DATETIME(6) NULL,
  `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
    ON UPDATE CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_conversations_application` (`application_id`),
  CONSTRAINT `fk_conversations_application`
    FOREIGN KEY (`application_id`) REFERENCES `applications` (`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `conversation_participants` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `conversation_id` BIGINT UNSIGNED NOT NULL,
  `user_id` BIGINT UNSIGNED NOT NULL,
  `participant_role` VARCHAR(32) NOT NULL,
  `status` VARCHAR(32) NOT NULL DEFAULT 'ACTIVE',
  `joined_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `removed_at` DATETIME(6) NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_conversation_participants_conversation_user`
    (`conversation_id`, `user_id`),
  KEY `ix_conversation_participants_user_status` (`user_id`, `status`),
  CONSTRAINT `fk_conversation_participants_conversation`
    FOREIGN KEY (`conversation_id`) REFERENCES `conversations` (`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_conversation_participants_user`
    FOREIGN KEY (`user_id`) REFERENCES `work_users` (`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `messages` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `conversation_id` BIGINT UNSIGNED NOT NULL,
  `sender_user_id` BIGINT UNSIGNED NOT NULL,
  `client_message_id` VARCHAR(191) NOT NULL,
  `sequence_number` BIGINT UNSIGNED NOT NULL,
  `body` TEXT NOT NULL,
  `status` VARCHAR(32) NOT NULL DEFAULT 'SENT',
  `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `edited_at` DATETIME(6) NULL,
  `deleted_at` DATETIME(6) NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_messages_conversation_client_id`
    (`conversation_id`, `client_message_id`),
  UNIQUE KEY `uq_messages_conversation_sequence`
    (`conversation_id`, `sequence_number`),
  KEY `ix_messages_conversation_time` (`conversation_id`, `created_at`),
  CONSTRAINT `fk_messages_conversation`
    FOREIGN KEY (`conversation_id`) REFERENCES `conversations` (`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_messages_sender_user`
    FOREIGN KEY (`sender_user_id`) REFERENCES `work_users` (`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `interviews` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `application_id` BIGINT UNSIGNED NOT NULL,
  `created_by_user_id` BIGINT UNSIGNED NOT NULL,
  `status` VARCHAR(32) NOT NULL DEFAULT 'PROPOSED',
  `current_schedule_version` INT UNSIGNED NOT NULL DEFAULT 1,
  `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
    ON UPDATE CURRENT_TIMESTAMP(6),
  `cancelled_at` DATETIME(6) NULL,
  PRIMARY KEY (`id`),
  KEY `ix_interviews_application_status` (`application_id`, `status`),
  CONSTRAINT `fk_interviews_application`
    FOREIGN KEY (`application_id`) REFERENCES `applications` (`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_interviews_created_by_user`
    FOREIGN KEY (`created_by_user_id`) REFERENCES `work_users` (`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `chk_interviews_schedule_version`
    CHECK (`current_schedule_version` > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `interview_schedule_versions` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `interview_id` BIGINT UNSIGNED NOT NULL,
  `version_number` INT UNSIGNED NOT NULL,
  `starts_at_utc` DATETIME(6) NOT NULL,
  `ends_at_utc` DATETIME(6) NOT NULL,
  `timezone` VARCHAR(64) NOT NULL,
  `location_text` VARCHAR(255) NULL,
  `meeting_provider` VARCHAR(64) NULL,
  `meeting_reference` VARCHAR(255) NULL,
  `created_by_user_id` BIGINT UNSIGNED NOT NULL,
  `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_interview_schedule_versions_interview_version`
    (`interview_id`, `version_number`),
  KEY `ix_interview_schedule_versions_time` (`starts_at_utc`, `ends_at_utc`),
  CONSTRAINT `fk_interview_schedule_versions_interview`
    FOREIGN KEY (`interview_id`) REFERENCES `interviews` (`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_interview_schedule_versions_created_by_user`
    FOREIGN KEY (`created_by_user_id`) REFERENCES `work_users` (`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `chk_interview_schedule_versions_numbers`
    CHECK (`version_number` > 0),
  CONSTRAINT `chk_interview_schedule_versions_time`
    CHECK (`ends_at_utc` > `starts_at_utc`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `interview_participants` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `interview_id` BIGINT UNSIGNED NOT NULL,
  `user_id` BIGINT UNSIGNED NOT NULL,
  `participant_role` VARCHAR(32) NOT NULL,
  `response_status` VARCHAR(32) NOT NULL DEFAULT 'PENDING',
  `responded_at` DATETIME(6) NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_interview_participants_interview_user` (`interview_id`, `user_id`),
  CONSTRAINT `fk_interview_participants_interview`
    FOREIGN KEY (`interview_id`) REFERENCES `interviews` (`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_interview_participants_user`
    FOREIGN KEY (`user_id`) REFERENCES `work_users` (`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ---------------------------------------------------------------------------
-- Payment and entitlement data
-- ---------------------------------------------------------------------------

CREATE TABLE `products` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `product_code` VARCHAR(120) NOT NULL,
  `product_type` VARCHAR(64) NOT NULL,
  `name` VARCHAR(255) NOT NULL,
  `description` TEXT NULL,
  `amount` DECIMAL(20,4) NOT NULL,
  `currency` CHAR(3) NOT NULL,
  `is_active` TINYINT(1) NOT NULL DEFAULT 1,
  `metadata_json` JSON NULL,
  `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
    ON UPDATE CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_products_product_code` (`product_code`),
  KEY `ix_products_type_active` (`product_type`, `is_active`),
  CONSTRAINT `chk_products_amount`
    CHECK (`amount` >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `orders` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `buyer_user_id` BIGINT UNSIGNED NOT NULL,
  `tenant_id` BIGINT UNSIGNED NULL,
  `external_order_reference` VARCHAR(191) NOT NULL,
  `payment_provider` VARCHAR(64) NULL,
  `status` VARCHAR(32) NOT NULL DEFAULT 'PENDING',
  `subtotal_amount` DECIMAL(20,4) NOT NULL,
  `total_amount` DECIMAL(20,4) NOT NULL,
  `currency` CHAR(3) NOT NULL,
  `expires_at` DATETIME(6) NULL,
  `settled_at` DATETIME(6) NULL,
  `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
    ON UPDATE CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_orders_external_reference` (`external_order_reference`),
  KEY `ix_orders_buyer_status` (`buyer_user_id`, `status`),
  KEY `ix_orders_tenant_status` (`tenant_id`, `status`),
  CONSTRAINT `fk_orders_buyer_user`
    FOREIGN KEY (`buyer_user_id`) REFERENCES `work_users` (`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_orders_tenant`
    FOREIGN KEY (`tenant_id`) REFERENCES `tenants` (`id`)
    ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `chk_orders_amounts`
    CHECK (`subtotal_amount` >= 0 AND `total_amount` >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `order_items` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `order_id` BIGINT UNSIGNED NOT NULL,
  `product_id` BIGINT UNSIGNED NOT NULL,
  `quantity` INT UNSIGNED NOT NULL DEFAULT 1,
  `unit_amount` DECIMAL(20,4) NOT NULL,
  `line_amount` DECIMAL(20,4) NOT NULL,
  `metadata_json` JSON NULL,
  PRIMARY KEY (`id`),
  KEY `ix_order_items_order` (`order_id`),
  CONSTRAINT `fk_order_items_order`
    FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_order_items_product`
    FOREIGN KEY (`product_id`) REFERENCES `products` (`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `chk_order_items_amounts`
    CHECK (`quantity` > 0 AND `unit_amount` >= 0 AND `line_amount` >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `payments` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `order_id` BIGINT UNSIGNED NOT NULL,
  `provider` VARCHAR(64) NOT NULL,
  `provider_payment_id` VARCHAR(191) NULL,
  `amount` DECIMAL(20,4) NOT NULL,
  `currency` CHAR(3) NOT NULL,
  `status` VARCHAR(32) NOT NULL DEFAULT 'PENDING',
  `transaction_code` VARCHAR(191) NULL,
  `provider_payload_json` JSON NULL,
  `paid_at` DATETIME(6) NULL,
  `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
    ON UPDATE CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_payments_provider_payment` (`provider`, `provider_payment_id`),
  KEY `ix_payments_order_status` (`order_id`, `status`),
  CONSTRAINT `fk_payments_order`
    FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `chk_payments_amount`
    CHECK (`amount` >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `entitlements` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `owner_user_id` BIGINT UNSIGNED NULL,
  `owner_tenant_id` BIGINT UNSIGNED NULL,
  `product_id` BIGINT UNSIGNED NULL,
  `source_order_id` BIGINT UNSIGNED NULL,
  `entitlement_type` VARCHAR(64) NOT NULL,
  `quantity_remaining` DECIMAL(20,4) NOT NULL DEFAULT 0,
  `status` VARCHAR(32) NOT NULL DEFAULT 'ACTIVE',
  `starts_at` DATETIME(6) NULL,
  `ends_at` DATETIME(6) NULL,
  `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
    ON UPDATE CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`),
  KEY `ix_entitlements_user_status` (`owner_user_id`, `status`),
  KEY `ix_entitlements_tenant_status` (`owner_tenant_id`, `status`),
  CONSTRAINT `fk_entitlements_owner_user`
    FOREIGN KEY (`owner_user_id`) REFERENCES `work_users` (`id`)
    ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_entitlements_owner_tenant`
    FOREIGN KEY (`owner_tenant_id`) REFERENCES `tenants` (`id`)
    ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_entitlements_product`
    FOREIGN KEY (`product_id`) REFERENCES `products` (`id`)
    ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_entitlements_source_order`
    FOREIGN KEY (`source_order_id`) REFERENCES `orders` (`id`)
    ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `chk_entitlements_owner`
    CHECK (`owner_user_id` IS NOT NULL OR `owner_tenant_id` IS NOT NULL),
  CONSTRAINT `chk_entitlements_quantity`
    CHECK (`quantity_remaining` >= 0),
  CONSTRAINT `chk_entitlements_dates`
    CHECK (`ends_at` IS NULL OR `starts_at` IS NULL OR `ends_at` >= `starts_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `credit_ledger` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `owner_user_id` BIGINT UNSIGNED NULL,
  `owner_tenant_id` BIGINT UNSIGNED NULL,
  `entitlement_id` BIGINT UNSIGNED NULL,
  `delta_amount` DECIMAL(20,4) NOT NULL,
  `balance_after` DECIMAL(20,4) NOT NULL,
  `reason` VARCHAR(160) NOT NULL,
  `reference_type` VARCHAR(64) NULL,
  `reference_id` VARCHAR(191) NULL,
  `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`),
  KEY `ix_credit_ledger_user_time` (`owner_user_id`, `created_at`),
  KEY `ix_credit_ledger_tenant_time` (`owner_tenant_id`, `created_at`),
  CONSTRAINT `fk_credit_ledger_owner_user`
    FOREIGN KEY (`owner_user_id`) REFERENCES `work_users` (`id`)
    ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_credit_ledger_owner_tenant`
    FOREIGN KEY (`owner_tenant_id`) REFERENCES `tenants` (`id`)
    ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_credit_ledger_entitlement`
    FOREIGN KEY (`entitlement_id`) REFERENCES `entitlements` (`id`)
    ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `chk_credit_ledger_owner`
    CHECK (`owner_user_id` IS NOT NULL OR `owner_tenant_id` IS NOT NULL)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `promotions` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `code` VARCHAR(120) NOT NULL,
  `name` VARCHAR(255) NOT NULL,
  `discount_type` VARCHAR(32) NOT NULL,
  `discount_value` DECIMAL(20,4) NOT NULL,
  `starts_at` DATETIME(6) NULL,
  `ends_at` DATETIME(6) NULL,
  `max_uses` INT UNSIGNED NULL,
  `used_count` INT UNSIGNED NOT NULL DEFAULT 0,
  `status` VARCHAR(32) NOT NULL DEFAULT 'ACTIVE',
  `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
    ON UPDATE CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_promotions_code` (`code`),
  KEY `ix_promotions_status_window` (`status`, `starts_at`, `ends_at`),
  CONSTRAINT `chk_promotions_discount`
    CHECK (`discount_value` >= 0),
  CONSTRAINT `chk_promotions_usage`
    CHECK (`max_uses` IS NULL OR `used_count` <= `max_uses`),
  CONSTRAINT `chk_promotions_dates`
    CHECK (`ends_at` IS NULL OR `starts_at` IS NULL OR `ends_at` >= `starts_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `sponsored_job_slots` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `job_id` BIGINT UNSIGNED NOT NULL,
  `order_id` BIGINT UNSIGNED NULL,
  `promotion_id` BIGINT UNSIGNED NULL,
  `placement` VARCHAR(64) NOT NULL,
  `starts_at` DATETIME(6) NOT NULL,
  `ends_at` DATETIME(6) NOT NULL,
  `status` VARCHAR(32) NOT NULL DEFAULT 'PENDING',
  `impressions_count` BIGINT UNSIGNED NOT NULL DEFAULT 0,
  `clicks_count` BIGINT UNSIGNED NOT NULL DEFAULT 0,
  `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`),
  KEY `ix_sponsored_job_slots_job_window` (`job_id`, `status`, `starts_at`, `ends_at`),
  CONSTRAINT `fk_sponsored_job_slots_job`
    FOREIGN KEY (`job_id`) REFERENCES `jobs` (`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_sponsored_job_slots_order`
    FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`)
    ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_sponsored_job_slots_promotion`
    FOREIGN KEY (`promotion_id`) REFERENCES `promotions` (`id`)
    ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `chk_sponsored_job_slots_window`
    CHECK (`ends_at` > `starts_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ---------------------------------------------------------------------------
-- Async operations, idempotency and operations/audit data
-- ---------------------------------------------------------------------------

CREATE TABLE `operations` (
  `id` CHAR(36) NOT NULL,
  `owner_user_id` BIGINT UNSIGNED NULL,
  `kind` VARCHAR(64) NOT NULL,
  `status` VARCHAR(32) NOT NULL DEFAULT 'QUEUED',
  `result_json` JSON NULL,
  `error_reason` VARCHAR(160) NULL,
  `error_message` TEXT NULL,
  `submitted_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
    ON UPDATE CURRENT_TIMESTAMP(6),
  `completed_at` DATETIME(6) NULL,
  PRIMARY KEY (`id`),
  KEY `ix_operations_owner_status` (`owner_user_id`, `status`),
  KEY `ix_operations_status_updated` (`status`, `updated_at`),
  CONSTRAINT `fk_operations_owner_user`
    FOREIGN KEY (`owner_user_id`) REFERENCES `work_users` (`id`)
    ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `idempotency_keys` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `scope_key` VARCHAR(255) NOT NULL,
  `endpoint` VARCHAR(255) NOT NULL,
  `idempotency_key` VARCHAR(191) NOT NULL,
  `request_hash` CHAR(64) NOT NULL,
  `response_status` SMALLINT UNSIGNED NULL,
  `response_body_json` JSON NULL,
  `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `expires_at` DATETIME(6) NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_idempotency_scope_endpoint_key`
    (`scope_key`, `endpoint`, `idempotency_key`),
  KEY `ix_idempotency_keys_expiry` (`expires_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `audit_events` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `actor_user_id` BIGINT UNSIGNED NULL,
  `tenant_id` BIGINT UNSIGNED NULL,
  `action` VARCHAR(120) NOT NULL,
  `resource_type` VARCHAR(64) NOT NULL,
  `resource_id` BIGINT UNSIGNED NULL,
  `reason` TEXT NULL,
  `metadata_json` JSON NULL,
  `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`),
  KEY `ix_audit_events_tenant_time` (`tenant_id`, `created_at`),
  KEY `ix_audit_events_actor_time` (`actor_user_id`, `created_at`),
  KEY `ix_audit_events_resource_time` (`resource_type`, `resource_id`, `created_at`),
  CONSTRAINT `fk_audit_events_actor_user`
    FOREIGN KEY (`actor_user_id`) REFERENCES `work_users` (`id`)
    ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_audit_events_tenant`
    FOREIGN KEY (`tenant_id`) REFERENCES `tenants` (`id`)
    ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `tenant_risk_events` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `tenant_id` BIGINT UNSIGNED NOT NULL,
  `event_type` VARCHAR(120) NOT NULL,
  `severity` VARCHAR(32) NOT NULL,
  `status` VARCHAR(32) NOT NULL DEFAULT 'OPEN',
  `details_json` JSON NULL,
  `opened_by_user_id` BIGINT UNSIGNED NULL,
  `resolved_by_user_id` BIGINT UNSIGNED NULL,
  `resolved_at` DATETIME(6) NULL,
  `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
    ON UPDATE CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`),
  KEY `ix_tenant_risk_events_tenant_status` (`tenant_id`, `status`),
  KEY `ix_tenant_risk_events_severity_status` (`severity`, `status`),
  CONSTRAINT `fk_tenant_risk_events_tenant`
    FOREIGN KEY (`tenant_id`) REFERENCES `tenants` (`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_tenant_risk_events_opened_by_user`
    FOREIGN KEY (`opened_by_user_id`) REFERENCES `work_users` (`id`)
    ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_tenant_risk_events_resolved_by_user`
    FOREIGN KEY (`resolved_by_user_id`) REFERENCES `work_users` (`id`)
    ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `webhook_events` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `provider` VARCHAR(64) NOT NULL,
  `provider_event_id` VARCHAR(191) NOT NULL,
  `event_type` VARCHAR(120) NOT NULL,
  `payload_hash` CHAR(64) NOT NULL,
  `payload_json` JSON NULL,
  `status` VARCHAR(32) NOT NULL DEFAULT 'RECEIVED',
  `received_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `processed_at` DATETIME(6) NULL,
  `error_message` TEXT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_webhook_events_provider_event` (`provider`, `provider_event_id`),
  KEY `ix_webhook_events_status_received` (`status`, `received_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
