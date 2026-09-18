/**
 * Static Work runtime configuration.
 *
 * Work intentionally keeps runtime configuration in this module. Keep
 * credentials in this source boundary and never duplicate them in logs, tests,
 * documentation or context.
 */
export const APP_ENV = "local" as const;
export const PORT = 3000;

export const DATABASE_URL =
  "postgresql://neondb_owner:npg_KbI87qFogAHp@ep-noisy-fog-b3rlle00.c-4.ap-southeast-1.aws.neon.tech/neondb?sslmode=require";
export const DIRECT_DATABASE_URL = DATABASE_URL;

export const JWT_SECRET = "ACqK8O81zcS2Mwblkd4HzeGnEs8zLDfrKmMM9lpZVPH61WZ4nR4_Qo0lPNwRHumN";
export const JWT_EXPIRES = "1d";
export const REDIS_URL = "";

// These legacy modules are not wired into the current API route graph.
export const SUPABASE_URL = "";
export const SUPABASE_ANON_KEY = "";
export const JWT_STORAGE_KEY = "access_token";
