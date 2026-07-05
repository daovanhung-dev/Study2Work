import "reflect-metadata";

import { NestFactory } from "@nestjs/core";
import { FastifyAdapter, type NestFastifyApplication } from "@nestjs/platform-fastify";

import { AppModule } from "./app.module";
import { EnvelopeInterceptor } from "./common/api/envelope.interceptor";
import { ApiExceptionFilter } from "./common/api/http-exception.filter";
import { loadEnv } from "./common/config/env";
import { normalizeTraceId, TRACE_HEADER } from "./common/trace/trace-id";

async function bootstrap(): Promise<void> {
  const env = loadEnv();
  const adapter = new FastifyAdapter({ logger: false });
  const app = await NestFactory.create<NestFastifyApplication>(AppModule, adapter);
  const fastify = app.getHttpAdapter().getInstance();

  fastify.addHook("onRequest", (request, reply, done) => {
    const incomingTraceId = request.headers["x-trace-id"];
    const traceId = normalizeTraceId(
      Array.isArray(incomingTraceId) ? incomingTraceId[0] : incomingTraceId,
    );
    (request as typeof request & { traceId?: string }).traceId = traceId;
    reply.header(TRACE_HEADER, traceId);
    done();
  });

  app.enableCors({
    origin: env.corsOrigins,
    credentials: true,
  });
  app.useGlobalInterceptors(new EnvelopeInterceptor());
  app.useGlobalFilters(new ApiExceptionFilter());

  await app.listen({ port: env.port, host: "0.0.0.0" });
}

void bootstrap();
