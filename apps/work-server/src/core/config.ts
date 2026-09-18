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

type EnvironmentLike = Record<string, string | undefined>;

function required(environment: EnvironmentLike, name: string): string {
  const value = environment[name]?.trim();
  if (!value) throw new Error(`Missing required environment variable: ${name}`);
  return value;
}

function optional(environment: EnvironmentLike, name: string, fallback: string): string {
  return environment[name]?.trim() || fallback;
}

function parsePort(environment: EnvironmentLike): number {
  const value = Number(optional(environment, "PORT", "3000"));
  if (!Number.isInteger(value) || value < 1 || value > 65535) {
    throw new Error("PORT must be an integer between 1 and 65535");
  }
  return value;
}

function parseEnvironment(environment: EnvironmentLike): WorkEnvironment {
  const value = optional(environment, "APP_ENV", "local");
  if (!["local", "test", "staging", "production"].includes(value)) {
    throw new Error("APP_ENV must be local, test, staging or production");
  }
  return value as WorkEnvironment;
}

export function loadConfig(environment: EnvironmentLike = process.env): WorkConfig {
  const jwtSecret = required(environment, "JWT_SECRET");
  if (jwtSecret.length < 32) throw new Error("JWT_SECRET must contain at least 32 characters");

  return {
    appEnv: parseEnvironment(environment),
    port: parsePort(environment),
    databaseUrl: required(environment, "DATABASE_URL"),
    directDatabaseUrl: required(environment, "DIRECT_DATABASE_URL"),
    jwtSecret,
    jwtExpires: optional(environment, "JWT_EXPIRES", "1d"),
    redisUrl: environment.REDIS_URL?.trim() || undefined,
    supabaseUrl: optional(environment, "SUPABASE_URL", ""),
    supabaseAnonKey: optional(environment, "SUPABASE_ANON_KEY", ""),
  };
}
