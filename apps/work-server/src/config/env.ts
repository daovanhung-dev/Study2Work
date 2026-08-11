import { config as loadDotenv } from "dotenv";
import { z } from "zod";

loadDotenv({ quiet: true });

const APP_ENVIRONMENTS = ["local", "test", "staging", "production"] as const;

function hasAllowedProtocol(value: string, protocols: string[]): boolean {
  try {
    return protocols.includes(new URL(value).protocol);
  } catch {
    return false;
  }
}

const booleanFromEnvironment = z.preprocess((value) => {
  if (typeof value !== "string") {
    return value;
  }

  const normalized = value.trim().toLowerCase();
  if (normalized === "true") {
    return true;
  }
  if (normalized === "false") {
    return false;
  }

  return value;
}, z.boolean());

const environmentSchema = z.object({
  appEnv: z.enum(APP_ENVIRONMENTS).default("local"),
  host: z.string().min(1).default("0.0.0.0"),
  port: z.coerce.number().int().min(1).max(65_535).default(8001),
  databaseUrl: z
    .string({ required_error: "WORK_DATABASE_URL is required" })
    .url()
    .refine(
      (value) => hasAllowedProtocol(value, ["postgres:", "postgresql:"]),
      "WORK_DATABASE_URL must use the postgres:// or postgresql:// protocol",
    ),
  redisUrl: z
    .string()
    .url()
    .refine(
      (value) => hasAllowedProtocol(value, ["redis:", "rediss:"]),
      "WORK_REDIS_URL must use the redis:// or rediss:// protocol",
    )
    .optional(),
  corsOrigins: z.array(z.string().url()).default([]),
  jwksUrl: z.string().url().optional(),
  jwtIssuer: z.string().min(1).default("study2work"),
  jwtAudience: z.string().min(1).default("work-api"),
  enableDocs: booleanFromEnvironment.default(true),
});

export type WorkEnvironment = Readonly<z.infer<typeof environmentSchema>>;

export const WORK_ENV = Symbol("WORK_ENV");

function trimToUndefined(value: string | undefined): string | undefined {
  const trimmed = value?.trim();
  return trimmed || undefined;
}

function parseCorsOrigins(value: string | undefined): string[] {
  if (!value) {
    return [];
  }

  return value
    .split(",")
    .map((origin) => origin.trim())
    .filter(Boolean)
    .map((origin) => {
      if (origin === "*") {
        throw new Error("WORK_CORS_ORIGINS must list explicit origins; '*' is not allowed.");
      }

      const parsed = new URL(origin);
      if (parsed.protocol !== "http:" && parsed.protocol !== "https:") {
        throw new Error("WORK_CORS_ORIGINS entries must use http:// or https://.");
      }

      return parsed.origin;
    });
}

function isInsecureJwksUrlAllowed(appEnv: string, jwksUrl: string | undefined): boolean {
  if (!jwksUrl) {
    return true;
  }

  const protocol = new URL(jwksUrl).protocol;
  return protocol === "https:" || ((appEnv === "local" || appEnv === "test") && protocol === "http:");
}

/** Parse only Work-owned runtime settings before the Nest application starts. */
export function parseWorkEnvironment(source: NodeJS.ProcessEnv = process.env): WorkEnvironment {
  const appEnv = trimToUndefined(source.WORK_APP_ENV) ?? "local";
  let corsOrigins: string[];

  try {
    corsOrigins = parseCorsOrigins(trimToUndefined(source.WORK_CORS_ORIGINS));
  } catch (error) {
    throw new Error(
      `Invalid Work API configuration: ${error instanceof Error ? error.message : "invalid CORS origins"}`,
    );
  }

  const result = environmentSchema.safeParse({
    appEnv,
    host: trimToUndefined(source.WORK_HOST),
    port: trimToUndefined(source.WORK_PORT),
    databaseUrl: trimToUndefined(source.WORK_DATABASE_URL),
    redisUrl: trimToUndefined(source.WORK_REDIS_URL),
    corsOrigins,
    jwksUrl: trimToUndefined(source.WORK_JWKS_URL),
    jwtIssuer: trimToUndefined(source.WORK_JWT_ISSUER),
    jwtAudience: trimToUndefined(source.WORK_JWT_AUDIENCE),
    enableDocs: trimToUndefined(source.WORK_ENABLE_DOCS),
  });

  if (!result.success) {
    const details = result.error.issues
      .map((issue) => `${issue.path.join(".") || "environment"}: ${issue.message}`)
      .join("; ");
    throw new Error(`Invalid Work API configuration: ${details}`);
  }

  if (
    (result.data.appEnv === "staging" || result.data.appEnv === "production") &&
    !result.data.jwksUrl
  ) {
    throw new Error(
      "Invalid Work API configuration: WORK_JWKS_URL is required outside local/test.",
    );
  }

  if (!isInsecureJwksUrlAllowed(result.data.appEnv, result.data.jwksUrl)) {
    throw new Error("Invalid Work API configuration: WORK_JWKS_URL must use HTTPS outside local/test.");
  }

  return Object.freeze(result.data);
}

export function loadWorkEnvironment(): WorkEnvironment {
  return parseWorkEnvironment();
}
