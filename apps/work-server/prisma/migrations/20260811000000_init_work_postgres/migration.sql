-- Clean PostgreSQL foundation for the separated Work API.
-- Legacy Learn2Earn MySQL tables are intentionally not migrated into this database.

CREATE TABLE "system_records" (
    "id" UUID NOT NULL,
    "key" VARCHAR(120) NOT NULL,
    "value" TEXT,
    "created_at" TIMESTAMPTZ(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ(6) NOT NULL,

    CONSTRAINT "system_records_pkey" PRIMARY KEY ("id")
);

CREATE UNIQUE INDEX "system_records_key_key" ON "system_records"("key");
