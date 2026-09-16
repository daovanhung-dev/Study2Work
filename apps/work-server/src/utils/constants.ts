const NEON_POOLER_URL =
  "postgresql://neondb_owner:npg_KbI87qFogAHp@ep-noisy-fog-b3rlle00-pooler.c-4.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require";

/** Runtime connection through Neon's transaction pooler. */
export const DATABASE_URL = `${NEON_POOLER_URL}&pgbouncer=true&connect_timeout=30`;

/** Direct endpoint used by Prisma CLI migration and schema commands. */
export const DIRECT_DATABASE_URL = `${NEON_POOLER_URL.replace(
  "-pooler.",
  "."
)}&connect_timeout=30`;

export const PORT = 3000;

export const JWT_SECRET = "replace-with-a-local-jwt-secret";
export const JWT_EXPIRES = "1d";
export const JWT_STORAGE_KEY = "access_token";

export const SUPABASE_URL = "https://example.supabase.co";
export const SUPABASE_ANON_KEY = "replace-with-a-local-supabase-anon-key";
