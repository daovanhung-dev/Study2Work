-- Lookup table for the two direct-Neon mobile clients.
-- The legacy Supabase endpoint is no longer resolvable, so the migration
-- backfills every distinct major already present in the Neon JD/SinhVien data.

CREATE TABLE IF NOT EXISTS bannganh (
    "nganh" VARCHAR(191) NOT NULL,
    CONSTRAINT bannganh_pkey PRIMARY KEY ("nganh")
);

INSERT INTO bannganh ("nganh")
SELECT DISTINCT btrim(value)
FROM (
    SELECT "nganh" AS value FROM "JD"
    UNION
    SELECT "chuyennganh" AS value FROM "SinhVien"
) AS source_values
WHERE value IS NOT NULL AND btrim(value) <> ''
ON CONFLICT ("nganh") DO NOTHING;

CREATE UNIQUE INDEX IF NOT EXISTS "UngVien_jd_sinhvien_key"
    ON "UngVien" ("jd_id", "sinhvien_id");
