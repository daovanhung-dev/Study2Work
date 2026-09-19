import express, { type Express } from "express";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { createV1Router } from "./api/v1.js";
import { loadConfig, type WorkConfig } from "./core/config.js";
import { createDependencies, type WorkDependencies } from "./core/dependencies.js";
import { asyncHandler, traceMiddleware } from "./core/middleware.js";
import { errorHandler, notFoundHandler } from "./core/exceptions.js";
import { ApiError, sendSuccess } from "./core/responses.js";
import { probeDatabase } from "./core/database.js";
import { authenticateToken } from "./middleware/auth.middleware.js";

export interface CreateAppOptions {
  config?: WorkConfig;
  dependencies?: WorkDependencies;
}

export function createApp(options: CreateAppOptions = {}): Express {
  const config = options.config ?? loadConfig();
  const dependencies = options.dependencies ?? createDependencies(config);
  const app = express();
  const currentFile = fileURLToPath(import.meta.url);
  const currentDirectory = path.dirname(currentFile);

  app.use(traceMiddleware);
  app.use(express.json());
  app.use(express.static(path.join(currentDirectory, "../public")));
  app.use("/uploads", express.static(path.join(process.cwd(), "uploads")));
  app.use(authenticateToken(config));

  app.get("/health/live", (request, response) => sendSuccess(
    request,
    response,
    200,
    "SYSTEM_HEALTH_LIVE",
    "Work API is live.",
    { service: "work-api", environment: config.appEnv },
  ));

  app.get("/health/ready", asyncHandler(async (request, response) => {
    try {
      await probeDatabase(dependencies.prisma);
    } catch {
      throw new ApiError({
        statusCode: 503,
        businessCode: "DEPENDENCY_UNAVAILABLE",
        message: "Work API is not ready.",
      });
    }
    return sendSuccess(
      request,
      response,
      200,
      "SYSTEM_HEALTH_READY",
      "Work API is ready.",
      {
        service: "work-api",
        environment: config.appEnv,
        dependencies: {
          database: "configured",
          redis: config.redisUrl ? "configured" : "not_configured",
        },
      },
    );
  }));

  app.use("/api/v1", createV1Router(dependencies));
  app.use(notFoundHandler);
  app.use(errorHandler);
  return app;
}

export default createApp;
