-- Bcrypt hashes are longer than the legacy plaintext column limits.
ALTER TABLE "SinhVien"
    ALTER COLUMN "matkhau" TYPE VARCHAR(255);

ALTER TABLE "DoanhNghiep"
    ALTER COLUMN "matkhau" TYPE VARCHAR(255);
