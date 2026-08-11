import type { AuthenticatedPrincipal } from "../../auth/authenticated-principal.js";

declare module "fastify" {
  interface FastifyRequest {
    traceId?: string;
    user?: AuthenticatedPrincipal;
  }
}

export {};
