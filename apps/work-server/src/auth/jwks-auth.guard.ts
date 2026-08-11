import {
  HttpStatus,
  Inject,
  Injectable,
  type CanActivate,
  type ExecutionContext,
} from "@nestjs/common";
import { Reflector } from "@nestjs/core";
import type { FastifyRequest } from "fastify";

import { IS_PUBLIC_KEY } from "../common/decorators/public.decorator.js";
import { ApiException } from "../common/http/api-exception.js";
import { JwksAuthService } from "./jwks-auth.service.js";

function bearerToken(authorization: string | undefined): string | undefined {
  if (!authorization) {
    return undefined;
  }

  const [scheme, token, ...rest] = authorization.trim().split(/\s+/);
  return scheme?.toLowerCase() === "bearer" && token && rest.length === 0 ? token : undefined;
}

@Injectable()
export class JwksAuthGuard implements CanActivate {
  constructor(
    @Inject(Reflector) private readonly reflector: Reflector,
    @Inject(JwksAuthService) private readonly jwksAuthService: JwksAuthService,
  ) {}

  async canActivate(context: ExecutionContext): Promise<boolean> {
    const isPublic = this.reflector.getAllAndOverride<boolean>(IS_PUBLIC_KEY, [
      context.getHandler(),
      context.getClass(),
    ]);

    if (isPublic) {
      return true;
    }

    const request = context.switchToHttp().getRequest<FastifyRequest>();
    const token = bearerToken(request.headers.authorization);
    if (!token) {
      throw new ApiException(
        HttpStatus.UNAUTHORIZED,
        "AUTHENTICATION_REQUIRED",
        "Authentication is required.",
      );
    }

    request.user = await this.jwksAuthService.verifyAccessToken(token);
    return true;
  }
}

export { Public } from "../common/decorators/public.decorator.js";
