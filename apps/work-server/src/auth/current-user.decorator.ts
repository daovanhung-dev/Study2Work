import { createParamDecorator, type ExecutionContext } from "@nestjs/common";
import type { FastifyRequest } from "fastify";

import type { AuthenticatedPrincipal } from "./authenticated-principal.js";

/** Read the verified JWT principal populated by JwksAuthGuard. */
export const CurrentUser = createParamDecorator(
  (_data: unknown, context: ExecutionContext): AuthenticatedPrincipal | undefined =>
    context.switchToHttp().getRequest<FastifyRequest>().user,
);
