import { describe, expect, it } from "vitest";

import { parseWorkEnvironment } from "../src/config/env.js";

describe("Work API configuration", () => {
  it("uses the prefixed runtime configuration and parses CORS origins", () => {
    const environment = parseWorkEnvironment({
      WORK_APP_ENV: "test",
      WORK_DATABASE_URL: "postgresql://user:password@localhost:5434/work",
      WORK_CORS_ORIGINS: "http://localhost:5174, https://work.example.test",
      WORK_JWKS_URL: "http://localhost:8080/.well-known/jwks.json",
    });

    expect(environment).toMatchObject({
      appEnv: "test",
      port: 8001,
      databaseUrl: "postgresql://user:password@localhost:5434/work",
      corsOrigins: ["http://localhost:5174", "https://work.example.test"],
      jwtIssuer: "study2work",
      jwtAudience: "work-api",
    });
  });

  it("rejects an insecure JWKS URL outside local and test", () => {
    expect(() =>
      parseWorkEnvironment({
        WORK_APP_ENV: "production",
        WORK_DATABASE_URL: "postgresql://user:password@localhost:5434/work",
        WORK_JWKS_URL: "http://identity.example.test/.well-known/jwks.json",
      }),
    ).toThrow("WORK_JWKS_URL must use HTTPS");
  });

  it("requires a JWKS URL outside local and test", () => {
    expect(() =>
      parseWorkEnvironment({
        WORK_APP_ENV: "staging",
        WORK_DATABASE_URL: "postgresql://user:password@localhost:5434/work",
      }),
    ).toThrow("WORK_JWKS_URL is required outside local/test");
  });
});
