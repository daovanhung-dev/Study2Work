import {
  APP_ENV,
  DATABASE_URL,
  DIRECT_DATABASE_URL,
  JWT_EXPIRES,
  JWT_SECRET,
  PORT,
  REDIS_URL,
  SUPABASE_ANON_KEY,
  SUPABASE_URL,
} from "../utils/constants.js";

export type WorkEnvironment = "local" | "test" | "staging" | "production";

export interface WorkConfig {
  appEnv: WorkEnvironment;
  port: number;
  databaseUrl: string;
  directDatabaseUrl: string;
  jwtSecret: string;
  jwtExpires: string;
  redisUrl?: string;
  supabaseUrl: string;
  supabaseAnonKey: string;
}

export type WorkConfigOverrides = Partial<WorkConfig>;

function required(value: string | undefined, name: string): string {
  const normalized = value?.trim();
  if (!normalized) throw new Error(`Missing required Work constant: ${name}`);
  if (normalized.includes("USER:PASSWORD@HOST") || normalized.startsWith("replace-with-")) {
    throw new Error(`Work constant ${name} still contains a placeholder value`);
  }
  return normalized;
}

function optional(value: string | undefined, fallback: string): string {
  const normalized = value?.trim();
  return normalized || fallback;
}

function parsePort(value: number | undefined): number {
  const normalized = value ?? 3000;
  if (!Number.isInteger(normalized) || normalized < 1 || normalized > 65535) {
    throw new Error("PORT must be an integer between 1 and 65535");
  }
  return normalized;
}

function parseEnvironment(value: string | undefined): WorkEnvironment {
  const normalized = value?.trim() || "local";
  if (!["local", "test", "staging", "production"].includes(normalized)) {
    throw new Error("APP_ENV must be local, test, staging or production");
  }
  return normalized as WorkEnvironment;
}

const STATIC_CONFIG: WorkConfig = {
  appEnv: APP_ENV,
  port: PORT,
  databaseUrl: DATABASE_URL,
  directDatabaseUrl: DIRECT_DATABASE_URL,
  jwtSecret: JWT_SECRET,
  jwtExpires: JWT_EXPIRES,
  redisUrl: REDIS_URL || undefined,
  supabaseUrl: SUPABASE_URL,
  supabaseAnonKey: SUPABASE_ANON_KEY,
};

export function loadConfig(overrides: WorkConfigOverrides = {}): WorkConfig {
  const configured = { ...STATIC_CONFIG, ...overrides };
  const jwtSecret = required(configured.jwtSecret, "JWT_SECRET");
  if (jwtSecret.length < 32) throw new Error("JWT_SECRET must contain at least 32 characters");

  return {
    appEnv: parseEnvironment(configured.appEnv),
    port: parsePort(configured.port),
    databaseUrl: required(configured.databaseUrl, "DATABASE_URL"),
    directDatabaseUrl: required(configured.directDatabaseUrl, "DIRECT_DATABASE_URL"),
    jwtSecret,
    jwtExpires: optional(configured.jwtExpires, "1d"),
    redisUrl: configured.redisUrl?.trim() || undefined,
    supabaseUrl: configured.supabaseUrl.trim(),
    supabaseAnonKey: configured.supabaseAnonKey.trim(),
  };
}
