import { afterEach, describe, expect, it } from "vitest";

import { loadConfig, type WorkConfig } from "../src/core/config.js";

const originalEnvironment = {
  APP_ENV: process.env.APP_ENV,
  DATABASE_URL: process.env.DATABASE_URL,
  DIRECT_DATABASE_URL: process.env.DIRECT_DATABASE_URL,
  JWT_SECRET: process.env.JWT_SECRET,
};

const validOverrides: WorkConfig = {
  appEnv: "test",
  port: 3100,
  databaseUrl: "postgresql://test/runtime",
  directDatabaseUrl: "postgresql://test/direct",
  jwtSecret: "test-secret-that-is-long-enough-for-work-api",
  jwtExpires: "1h",
  redisUrl: undefined,
  supabaseUrl: "",
  supabaseAnonKey: "",
};

afterEach(() => {
  for (const [name, value] of Object.entries(originalEnvironment)) {
    if (value === undefined) delete process.env[name];
    else process.env[name] = value;
  }
});

describe("Work static configuration", () => {
  it("loads the tracked static constants as the default configuration source", () => {
    process.env.DATABASE_URL = "postgresql://environment/should-not-win";
    process.env.DIRECT_DATABASE_URL = "postgresql://environment/direct-should-not-win";
    process.env.JWT_SECRET = "environment-secret-that-must-not-win";

    const config = loadConfig();

    expect(config.appEnv).toBe("local");
    expect(config.port).toBe(3000);
    expect(config.databaseUrl).toContain("neon.tech");
    expect(config.directDatabaseUrl).toBe(config.databaseUrl);
    expect(config.jwtSecret).not.toBe(process.env.JWT_SECRET);
    expect(config.jwtSecret.length).toBeGreaterThanOrEqual(32);
  });

  it("uses explicit typed overrides instead of process.env", () => {
    process.env.APP_ENV = "production";
    process.env.DATABASE_URL = "postgresql://environment/should-not-win";
    process.env.DIRECT_DATABASE_URL = "postgresql://environment/direct-should-not-win";
    process.env.JWT_SECRET = "environment-secret-that-must-not-win";

    expect(loadConfig(validOverrides)).toEqual(validOverrides);
  });

  it("rejects placeholder database constants without exposing their value", () => {
    expect(() => loadConfig({ ...validOverrides, databaseUrl: "postgresql://USER:PASSWORD@HOST/db" }))
      .toThrow("Work constant DATABASE_URL still contains a placeholder value");
  });

  it("rejects placeholder JWT constants without exposing their value", () => {
    expect(() => loadConfig({ ...validOverrides, jwtSecret: "replace-with-a-local-secret" }))
      .toThrow("Work constant JWT_SECRET still contains a placeholder value");
  });

  it("does not include secret material in validation errors", () => {
    const placeholder = "replace-with-a-local-secret-that-must-not-be-printed";

    try {
      loadConfig({ ...validOverrides, jwtSecret: placeholder });
      throw new Error("expected placeholder validation to fail");
    } catch (error) {
      expect((error as Error).message).not.toContain(placeholder);
    }
  });
});
