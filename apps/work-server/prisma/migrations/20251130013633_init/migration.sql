-- CreateTable
CREATE TABLE `SinhVien` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `hoten` VARCHAR(50) NULL,
    `email` VARCHAR(50) NULL,
    `matkhau` VARCHAR(20) NULL,
    `chuyennganh` VARCHAR(50) NULL,
    `avt` VARCHAR(191) NULL,

    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `DoanhNghiep` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `hoten` VARCHAR(50) NULL,
    `email` VARCHAR(50) NULL,
    `matkhau` VARCHAR(50) NULL,
    `diachi` VARCHAR(100) NULL,
    `sodienthoai` VARCHAR(20) NULL,
    `avt` VARCHAR(191) NULL,

    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
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
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
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
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `DoanChat` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `sinhvien_id` BIGINT NOT NULL,
    `doanhnghiep_id` BIGINT NOT NULL,
    `created_at` DATETIME(3) NULL DEFAULT CURRENT_TIMESTAMP(3),

    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
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
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
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
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
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
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `TopJD` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `created_at` DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    `jd_id` BIGINT NULL,

    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `TopCV` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,

    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `UngVien` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `created_at` DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    `sinhvien_id` BIGINT NULL,
    `doanhnghiep_id` BIGINT NULL,
    `trangthai` VARCHAR(191) NULL DEFAULT 'chưa ứng tuyển',
    `jd_id` BIGINT NULL,

    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- AddForeignKey
ALTER TABLE `Chat` ADD CONSTRAINT `Chat_sinhvien_id_fkey` FOREIGN KEY (`sinhvien_id`) REFERENCES `SinhVien`(`id`) ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `Chat` ADD CONSTRAINT `Chat_doanhnghiep_id_fkey` FOREIGN KEY (`doanhnghiep_id`) REFERENCES `DoanhNghiep`(`id`) ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `Cv` ADD CONSTRAINT `Cv_sinhvien_id_fkey` FOREIGN KEY (`sinhvien_id`) REFERENCES `SinhVien`(`id`) ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `DoanChat` ADD CONSTRAINT `DoanChat_sinhvien_id_fkey` FOREIGN KEY (`sinhvien_id`) REFERENCES `SinhVien`(`id`) ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `DoanChat` ADD CONSTRAINT `DoanChat_doanhnghiep_id_fkey` FOREIGN KEY (`doanhnghiep_id`) REFERENCES `DoanhNghiep`(`id`) ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `JD` ADD CONSTRAINT `JD_doanhnghiep_id_fkey` FOREIGN KEY (`doanhnghiep_id`) REFERENCES `DoanhNghiep`(`id`) ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `ThongBaoDN` ADD CONSTRAINT `ThongBaoDN_doanhnghiep_id_fkey` FOREIGN KEY (`doanhnghiep_id`) REFERENCES `DoanhNghiep`(`id`) ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `ThongBaoSV` ADD CONSTRAINT `ThongBaoSV_sinhvien_id_fkey` FOREIGN KEY (`sinhvien_id`) REFERENCES `SinhVien`(`id`) ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `TopJD` ADD CONSTRAINT `TopJD_jd_id_fkey` FOREIGN KEY (`jd_id`) REFERENCES `JD`(`id`) ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `UngVien` ADD CONSTRAINT `UngVien_sinhvien_id_fkey` FOREIGN KEY (`sinhvien_id`) REFERENCES `SinhVien`(`id`) ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `UngVien` ADD CONSTRAINT `UngVien_doanhnghiep_id_fkey` FOREIGN KEY (`doanhnghiep_id`) REFERENCES `DoanhNghiep`(`id`) ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `UngVien` ADD CONSTRAINT `UngVien_jd_id_fkey` FOREIGN KEY (`jd_id`) REFERENCES `JD`(`id`) ON DELETE SET NULL ON UPDATE CASCADE;
