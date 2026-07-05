export interface WorkEnv {
  appEnv: string;
  port: number;
  corsOrigins: string[];
  databaseUrl: string;
  redisUrl: string;
}

function splitList(value: string | undefined, fallback: string[]): string[] {
  if (!value) {
    return fallback;
  }

  return value
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);
}

export function loadEnv(): WorkEnv {
  return {
    appEnv: process.env.WORK_APP_ENV ?? "local",
    port: Number(process.env.PORT ?? process.env.WORK_PORT ?? 8001),
    corsOrigins: splitList(process.env.WORK_CORS_ORIGINS, ["http://localhost:5174"]),
    databaseUrl:
      process.env.WORK_DATABASE_URL ??
      "postgresql://study2work:study2work@localhost:5434/study2work_work",
    redisUrl: process.env.WORK_REDIS_URL ?? "redis://localhost:6381/0",
  };
}
