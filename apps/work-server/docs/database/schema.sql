-- Study2Work / Work server database schema
-- Source: apps/work-server/prisma/schema.prisma
-- Database engine: MySQL

CREATE DATABASE IF NOT EXISTS `work_server`
  DEFAULT CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE `work_server`;

CREATE TABLE `SinhVien` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `hoten` VARCHAR(50) NULL,
    `email` VARCHAR(50) NULL,
    `matkhau` VARCHAR(255) NULL,
    `chuyennganh` VARCHAR(50) NULL,
    `avt` VARCHAR(191) NULL,

    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE `DoanhNghiep` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `hoten` VARCHAR(50) NULL,
    `email` VARCHAR(50) NULL,
    `matkhau` VARCHAR(255) NULL,
    `diachi` VARCHAR(100) NULL,
    `sodienthoai` VARCHAR(20) NULL,
    `avt` VARCHAR(191) NULL,

    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE `Chat` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `sinhvien_id` BIGINT NULL,
    `doanhnghiep_id` BIGINT NULL,
    `nguoigui` VARCHAR(191) NULL,
    `nguoinhan` VARCHAR(191) NULL,
    `noidung` VARCHAR(191) NULL,
    `ngaygui` DATETIME(3) NULL DEFAULT CURRENT_TIMESTAMP(3),
    `trangthai` BOOLEAN NULL,

    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE `Cv` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `avt` VARCHAR(191) NULL,
    `hoten` VARCHAR(191) NOT NULL,
    `ngaysinh` DATETIME(3) NULL,
    `gioitinh` VARCHAR(191) NULL,
    `email` VARCHAR(191) NOT NULL,
    `sdt` VARCHAR(191) NULL,
    `diachi` VARCHAR(191) NULL,
    `vitri` VARCHAR(191) NULL,
    `nganh` VARCHAR(191) NULL,
    `muctieunghiep` VARCHAR(191) NULL,
    `hocvan` VARCHAR(191) NULL,
    `kinhnghiem` VARCHAR(191) NULL,
    `kynang` VARCHAR(191) NULL,
    `ngoaingu` VARCHAR(191) NULL,
    `chungchi` VARCHAR(191) NULL,
    `duan` VARCHAR(191) NULL,
    `giaithuong` VARCHAR(191) NULL,
    `hoatdong` VARCHAR(191) NULL,
    `social` JSON NULL,
    `portfolio` VARCHAR(191) NULL,
    `luongmongmuon` VARCHAR(191) NULL,
    `created_at` DATETIME(3) NULL DEFAULT CURRENT_TIMESTAMP(3),
    `sinhvien_id` BIGINT NULL,

    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE `DoanChat` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `sinhvien_id` BIGINT NOT NULL,
    `doanhnghiep_id` BIGINT NOT NULL,
    `created_at` DATETIME(3) NULL DEFAULT CURRENT_TIMESTAMP(3),

    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE `JD` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `ten_vi_tri` VARCHAR(191) NOT NULL,
    `phong_ban` VARCHAR(191) NULL,
    `cap_bac` VARCHAR(191) NULL,
    `bao_cao_cho` VARCHAR(191) NULL,
    `nhiem_vu` VARCHAR(191) NULL,
    `trinh_do` VARCHAR(191) NULL,
    `kinh_nghiem` VARCHAR(191) NULL,
    `ky_nang` VARCHAR(191) NULL,
    `ky_nang_mem` VARCHAR(191) NULL,
    `uu_tien` VARCHAR(191) NULL,
    `muc_luong` VARCHAR(191) NULL,
    `phuc_loi` VARCHAR(191) NULL,
    `moi_truong` VARCHAR(191) NULL,
    `dia_diem` VARCHAR(191) NULL,
    `thoi_gian` VARCHAR(191) NULL,
    `han_nop` VARCHAR(191) NULL,
    `cach_ung_tuyen` VARCHAR(191) NULL,
    `ngay_tao` DATETIME(3) NULL DEFAULT CURRENT_TIMESTAMP(3),
    `mo_ta` VARCHAR(191) NULL,
    `doanhnghiep_id` BIGINT NULL,
    `ten_cong_ty` VARCHAR(191) NULL,
    `nganh` VARCHAR(191) NULL,
    `avt` VARCHAR(191) NULL,

    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE `ThongBaoDN` (
    `id_dn` BIGINT NOT NULL AUTO_INCREMENT,
    `ten_dn` VARCHAR(191) NULL,
    `email` VARCHAR(191) NULL,
    `mat_khau` VARCHAR(191) NULL,
    `sdt` VARCHAR(191) NULL,
    `logo` VARCHAR(191) NULL,
    `trang_thai` VARCHAR(191) NULL,
    `ngay_tao` VARCHAR(191) NULL,
    `doanhnghiep_id` BIGINT NULL,

    PRIMARY KEY (`id_dn`)
) ENGINE=InnoDB DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE `ThongBaoSV` (
    `id_sv` BIGINT NOT NULL AUTO_INCREMENT,
    `ho_ten` VARCHAR(191) NULL,
    `email` VARCHAR(191) NULL,
    `mat_khau` VARCHAR(191) NULL,
    `sdt` VARCHAR(191) NULL,
    `avt_sv` VARCHAR(191) NULL,
    `trang_thai` VARCHAR(191) NULL,
    `ngay_tao` VARCHAR(191) NULL,
    `sinhvien_id` BIGINT NULL,

    PRIMARY KEY (`id_sv`)
) ENGINE=InnoDB DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE `TopJD` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `created_at` DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    `jd_id` BIGINT NULL,

    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE `TopCV` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,

    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE `UngVien` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `created_at` DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    `sinhvien_id` BIGINT NULL,
    `doanhnghiep_id` BIGINT NULL,
    `trangthai` VARCHAR(191) NULL DEFAULT 'chưa ứng tuyển',
    `jd_id` BIGINT NULL,

    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE UNIQUE INDEX `DoanhNghiep_email_key`
    ON `DoanhNghiep` (`email`);

CREATE UNIQUE INDEX `SinhVien_email_key`
    ON `SinhVien` (`email`);

CREATE UNIQUE INDEX `Cv_sinhvien_id_key`
    ON `Cv` (`sinhvien_id`);

ALTER TABLE `Chat`
    ADD CONSTRAINT `Chat_sinhvien_id_fkey`
    FOREIGN KEY (`sinhvien_id`) REFERENCES `SinhVien` (`id`)
    ON DELETE SET NULL ON UPDATE CASCADE;

ALTER TABLE `Chat`
    ADD CONSTRAINT `Chat_doanhnghiep_id_fkey`
    FOREIGN KEY (`doanhnghiep_id`) REFERENCES `DoanhNghiep` (`id`)
    ON DELETE SET NULL ON UPDATE CASCADE;

ALTER TABLE `Cv`
    ADD CONSTRAINT `Cv_sinhvien_id_fkey`
    FOREIGN KEY (`sinhvien_id`) REFERENCES `SinhVien` (`id`)
    ON DELETE SET NULL ON UPDATE CASCADE;

ALTER TABLE `DoanChat`
    ADD CONSTRAINT `DoanChat_sinhvien_id_fkey`
    FOREIGN KEY (`sinhvien_id`) REFERENCES `SinhVien` (`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE;

ALTER TABLE `DoanChat`
    ADD CONSTRAINT `DoanChat_doanhnghiep_id_fkey`
    FOREIGN KEY (`doanhnghiep_id`) REFERENCES `DoanhNghiep` (`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE;

ALTER TABLE `JD`
    ADD CONSTRAINT `JD_doanhnghiep_id_fkey`
    FOREIGN KEY (`doanhnghiep_id`) REFERENCES `DoanhNghiep` (`id`)
    ON DELETE SET NULL ON UPDATE CASCADE;

ALTER TABLE `ThongBaoDN`
    ADD CONSTRAINT `ThongBaoDN_doanhnghiep_id_fkey`
    FOREIGN KEY (`doanhnghiep_id`) REFERENCES `DoanhNghiep` (`id`)
    ON DELETE SET NULL ON UPDATE CASCADE;

ALTER TABLE `ThongBaoSV`
    ADD CONSTRAINT `ThongBaoSV_sinhvien_id_fkey`
    FOREIGN KEY (`sinhvien_id`) REFERENCES `SinhVien` (`id`)
    ON DELETE SET NULL ON UPDATE CASCADE;

ALTER TABLE `TopJD`
    ADD CONSTRAINT `TopJD_jd_id_fkey`
    FOREIGN KEY (`jd_id`) REFERENCES `JD` (`id`)
    ON DELETE SET NULL ON UPDATE CASCADE;

ALTER TABLE `UngVien`
    ADD CONSTRAINT `UngVien_sinhvien_id_fkey`
    FOREIGN KEY (`sinhvien_id`) REFERENCES `SinhVien` (`id`)
    ON DELETE SET NULL ON UPDATE CASCADE;

ALTER TABLE `UngVien`
    ADD CONSTRAINT `UngVien_doanhnghiep_id_fkey`
    FOREIGN KEY (`doanhnghiep_id`) REFERENCES `DoanhNghiep` (`id`)
    ON DELETE SET NULL ON UPDATE CASCADE;

ALTER TABLE `UngVien`
    ADD CONSTRAINT `UngVien_jd_id_fkey`
    FOREIGN KEY (`jd_id`) REFERENCES `JD` (`id`)
    ON DELETE SET NULL ON UPDATE CASCADE;
