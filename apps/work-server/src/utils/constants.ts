function requiredEnv(name: string): string {
  const value = process.env[name]?.trim();
  if (!value) throw new Error(`Missing required environment variable: ${name}`);
  return value;
}

function optionalEnv(name: string, fallback: string): string {
  return process.env[name]?.trim() || fallback;
}

function portEnv(): number {
  const value = Number(optionalEnv("PORT", "3000"));
  if (!Number.isInteger(value) || value < 1 || value > 65535) {
    throw new Error("PORT must be an integer between 1 and 65535");
  }
  return value;
}

export const DATABASE_URL = requiredEnv("DATABASE_URL");
export const DIRECT_DATABASE_URL = requiredEnv("DIRECT_DATABASE_URL");
export const PORT = portEnv();

export const JWT_SECRET = requiredEnv("JWT_SECRET");
if (JWT_SECRET.length < 32) {
  throw new Error("JWT_SECRET must contain at least 32 characters");
}

export const JWT_EXPIRES = optionalEnv("JWT_EXPIRES", "1d");
export const JWT_STORAGE_KEY = "access_token";

// Supabase is retained only for legacy, currently unwired modules.
export const SUPABASE_URL = optionalEnv("SUPABASE_URL", "");
export const SUPABASE_ANON_KEY = optionalEnv("SUPABASE_ANON_KEY", "");
