import "reflect-metadata";

import { ValidationPipe } from "@nestjs/common";
import { NestFactory } from "@nestjs/core";
import { FastifyAdapter, type NestFastifyApplication } from "@nestjs/platform-fastify";
import fastifyCors from "@fastify/cors";
import type { FastifyInstance, FastifyReply, FastifyRequest } from "fastify";

import { AppModule } from "./app.module.js";
import { validationExceptionFactory } from "./common/http/validation-exception.js";
import { createTraceId, normalizeTraceId, TRACE_ID_HEADER } from "./common/trace/trace-id.js";
import { loadWorkEnvironment, type WorkEnvironment } from "./config/env.js";

async function configureFastify(
  app: NestFastifyApplication,
  environment: WorkEnvironment,
): Promise<void> {
  const fastify = app.getHttpAdapter().getInstance() as FastifyInstance;
  fastify.decorateRequest("traceId", "");

  fastify.addHook("onRequest", (request: FastifyRequest, reply: FastifyReply, done) => {
    const incomingTraceId = request.headers[TRACE_ID_HEADER.toLowerCase()];
    const traceId = normalizeTraceId(
      Array.isArray(incomingTraceId) ? incomingTraceId[0] : incomingTraceId,
    ) ?? createTraceId();

    request.traceId = traceId;
    reply.header(TRACE_ID_HEADER, traceId);
    done();
  });

  await app.register(fastifyCors, {
    origin: environment.corsOrigins.length > 0 ? environment.corsOrigins : false,
    // Work never authenticates a browser through cookies: it accepts only an
    // Identity-issued Bearer token. Keeping credentials disabled prevents a
    // Work-origin cookie from becoming an accidental auth boundary.
    credentials: false,
    methods: ["GET", "HEAD", "PUT", "PATCH", "POST", "DELETE", "OPTIONS"],
    allowedHeaders: [
      "Authorization",
      "Content-Type",
      "Idempotency-Key",
      "If-Match",
      "X-Client-Request-Id",
      TRACE_ID_HEADER,
    ],
    exposedHeaders: [TRACE_ID_HEADER],
  });
}

export async function createWorkApplication(
  environment: WorkEnvironment = loadWorkEnvironment(),
): Promise<NestFastifyApplication> {
  const app = await NestFactory.create<NestFastifyApplication>(
    AppModule.forRoot(environment),
    new FastifyAdapter(),
    { bufferLogs: true },
  );

  await configureFastify(app, environment);
  app.setGlobalPrefix("api/v1", {
    exclude: ["health/live", "health/ready"],
  });
  app.useGlobalPipes(
    new ValidationPipe({
      transform: true,
      whitelist: true,
      forbidNonWhitelisted: true,
      exceptionFactory: validationExceptionFactory,
    }),
  );
  app.enableShutdownHooks();

  return app;
}

export async function bootstrap(): Promise<void> {
  const environment = loadWorkEnvironment();
  const app = await createWorkApplication(environment);
  await app.listen(environment.port, environment.host);
}
