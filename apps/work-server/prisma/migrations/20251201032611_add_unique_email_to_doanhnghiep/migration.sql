/*
  Warnings:

  - A unique constraint covering the columns `[email]` on the table `DoanhNghiep` will be added. If there are existing duplicate values, this will fail.
  - A unique constraint covering the columns `[email]` on the table `SinhVien` will be added. If there are existing duplicate values, this will fail.

*/
-- CreateIndex
CREATE UNIQUE INDEX `DoanhNghiep_email_key` ON `DoanhNghiep`(`email`);

-- CreateIndex
CREATE UNIQUE INDEX `SinhVien_email_key` ON `SinhVien`(`email`);
