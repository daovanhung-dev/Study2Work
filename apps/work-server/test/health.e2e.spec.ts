import { afterAll, beforeAll, describe, expect, it, vi } from "vitest";

import { createWorkApplication } from "../src/bootstrap.js";
import type { WorkEnvironment } from "../src/config/env.js";
import type { PrismaService } from "../src/database/prisma.service.js";
import { HealthService } from "../src/health/health.service.js";

const testEnvironment: WorkEnvironment = {
  appEnv: "test",
  host: "127.0.0.1",
  port: 0,
  databaseUrl: "postgresql://study2work:study2work@127.0.0.1:5434/study2work_work",
  redisUrl: undefined,
  corsOrigins: ["http://localhost:5174"],
  jwksUrl: undefined,
  jwtIssuer: "study2work",
  jwtAudience: "work-api",
  enableDocs: false,
};

describe("Work API health foundation", () => {
  let app: Awaited<ReturnType<typeof createWorkApplication>>;

  beforeAll(async () => {
    app = await createWorkApplication(testEnvironment);
    await app.init();
  });

  afterAll(async () => {
    await app.close();
  });

  it("returns the canonical live envelope and trace header", async () => {
    const response = await app.inject({ method: "GET", url: "/health/live" });
    const body = response.json() as {
      success: boolean;
      businessCode: string;
      message: string;
      data: { service: string; environment: string };
      meta: Record<string, unknown>;
      traceId: string;
    };

    expect(response.statusCode).toBe(200);
    expect(body).toMatchObject({
      success: true,
      businessCode: "SYSTEM_HEALTH_LIVE",
      message: "Work API is live.",
      data: { service: "work-api", environment: "test" },
      meta: {},
    });
    expect(response.headers["x-trace-id"]).toBe(body.traceId);
  });

  it("keeps a valid caller trace ID", async () => {
    const traceId = "7c3a2f1b-31c5-4a21-9b3e-7d1745c4748a";
    const response = await app.inject({
      method: "GET",
      url: "/health/live",
      headers: { "x-trace-id": traceId },
    });

    expect((response.json() as { traceId: string }).traceId).toBe(traceId);
    expect(response.headers["x-trace-id"]).toBe(traceId);
  });

  it("permits the client mutation headers during a browser preflight", async () => {
    const response = await app.inject({
      method: "OPTIONS",
      url: "/api/v1/work-metadata",
      headers: {
        origin: "http://localhost:5174",
        "access-control-request-method": "PATCH",
        "access-control-request-headers": "authorization,content-type,idempotency-key,if-match,x-client-request-id",
      },
    });

    expect(response.statusCode).toBe(204);
    expect(response.headers["access-control-allow-origin"]).toBe("http://localhost:5174");
    expect(response.headers["access-control-allow-headers"]).toContain("If-Match");
    expect(response.headers["access-control-allow-headers"]).toContain("X-Client-Request-Id");
  });

  it("returns the configured dependency baseline after the database probe succeeds", async () => {
    const prisma = {
      $queryRaw: vi.fn().mockResolvedValue([{ "?column?": 1 }]),
    } as unknown as PrismaService;
    const healthService = new HealthService(testEnvironment, prisma);

    await expect(healthService.ready()).resolves.toMatchObject({
      service: "work-api",
      environment: "test",
      dependencies: { database: "configured", redis: "not_configured" },
    });
  });

  it("uses the safe error envelope for unknown routes", async () => {
    const response = await app.inject({ method: "GET", url: "/does-not-exist" });
    const body = response.json() as {
      success: boolean;
      businessCode: string;
      message: string;
      data: null;
      meta: { fieldErrors: unknown[] };
      traceId: string;
    };

    expect(response.statusCode).toBe(404);
    expect(body.success).toBe(false);
    expect(body.businessCode).toBe("HTTP_ERROR");
    expect(body.data).toBeNull();
    expect(body.meta.fieldErrors).toEqual([]);
    expect(response.headers["x-trace-id"]).toBe(body.traceId);
  });
});
