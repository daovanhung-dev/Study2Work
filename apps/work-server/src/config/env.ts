import dotenv from "dotenv";

dotenv.config({ quiet: true });

function required(name: string): string {
  const value = process.env[name]?.trim();

  if (!value) {
    throw new Error(
      `Missing required environment variable ${name}. Copy .env.example to .env and set a valid value.`
    );
  }

  return value;
}

function validateDatabaseUrl(value: string): string {
  if (value.includes("USER:PASSWORD")) {
    throw new Error(
      "DATABASE_URL still uses placeholder credentials. Use mysql://study2work:study2work@127.0.0.1:3307/learn2earn for the local Docker database, or set your real MySQL credentials."
    );
  }

  let url: URL;
  try {
    url = new URL(value);
  } catch {
    throw new Error("DATABASE_URL must be a valid MySQL connection URL.");
  }

  if (url.protocol !== "mysql:") {
    throw new Error("DATABASE_URL must use the mysql:// protocol for work-server.");
  }

  return value;
}

const databaseUrl = validateDatabaseUrl(required("DATABASE_URL"));
const sessionSecret = process.env.SESSION_SECRET || process.env.JWT_SECRET;

if (!sessionSecret) {
  throw new Error("SESSION_SECRET or JWT_SECRET must be configured.");
}

export const env = {
  databaseUrl,
  jwtExpires: process.env.JWT_EXPIRES,
  jwtSecret: process.env.JWT_SECRET || sessionSecret,
  port: process.env.PORT || "3000",
  sessionSecret,
};
