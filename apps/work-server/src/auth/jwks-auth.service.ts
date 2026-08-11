import { HttpStatus, Inject, Injectable } from "@nestjs/common";
import { createRemoteJWKSet, errors, jwtVerify } from "jose";

import { ApiException } from "../common/http/api-exception.js";
import { WORK_ENV, type WorkEnvironment } from "../config/env.js";
import type { AuthenticatedPrincipal } from "./authenticated-principal.js";

@Injectable()
export class JwksAuthService {
  private readonly jwks: ReturnType<typeof createRemoteJWKSet> | undefined;

  constructor(@Inject(WORK_ENV) private readonly environment: WorkEnvironment) {
    this.jwks = environment.jwksUrl
      ? createRemoteJWKSet(new URL(environment.jwksUrl), {
          cacheMaxAge: 300_000,
          cooldownDuration: 30_000,
          timeoutDuration: 5_000,
        })
      : undefined;
  }

  async verifyAccessToken(token: string): Promise<AuthenticatedPrincipal> {
    if (!this.jwks) {
      throw new ApiException(
        HttpStatus.SERVICE_UNAVAILABLE,
        "DEPENDENCY_UNAVAILABLE",
        "Authentication verification is not configured.",
      );
    }

    try {
      const { payload } = await jwtVerify(token, this.jwks, {
        issuer: this.environment.jwtIssuer,
        audience: this.environment.jwtAudience,
        algorithms: ["ES256"],
      });

      if (
        payload.type !== "access" ||
        typeof payload.sub !== "string" ||
        !payload.sub ||
        typeof payload.jti !== "string" ||
        !payload.jti ||
        typeof payload.sid !== "string" ||
        !payload.sid ||
        typeof payload.authVersion !== "number"
      ) {
        throw new ApiException(
          HttpStatus.UNAUTHORIZED,
          "INVALID_ACCESS_TOKEN",
          "The access token is invalid.",
        );
      }

      return {
        subject: payload.sub,
        sessionId: payload.sid,
        tokenId: payload.jti,
        authVersion: payload.authVersion,
        scopes: this.scopesOf(payload.scope),
      };
    } catch (error) {
      if (error instanceof ApiException) {
        throw error;
      }

      if (error instanceof errors.JWTExpired) {
        throw new ApiException(
          HttpStatus.UNAUTHORIZED,
          "ACCESS_TOKEN_EXPIRED",
          "The access token has expired.",
        );
      }

      if (this.isJwksUnavailable(error)) {
        throw new ApiException(
          HttpStatus.SERVICE_UNAVAILABLE,
          "DEPENDENCY_UNAVAILABLE",
          "Authentication verification is temporarily unavailable.",
        );
      }

      throw new ApiException(
        HttpStatus.UNAUTHORIZED,
        "INVALID_ACCESS_TOKEN",
        "The access token is invalid.",
      );
    }
  }

  private scopesOf(scope: unknown): string[] {
    if (typeof scope === "string") {
      return scope.split(" ").filter(Boolean);
    }

    if (Array.isArray(scope) && scope.every((value) => typeof value === "string")) {
      return scope;
    }

    return [];
  }

  private isJwksUnavailable(error: unknown): boolean {
    if (error instanceof TypeError) {
      return true;
    }

    if (!error || typeof error !== "object" || !("code" in error)) {
      return false;
    }

    return (
      error.code === "ERR_JWKS_TIMEOUT" ||
      error.code === "ERR_JWKS_INVALID" ||
      error.code === "ERR_JWKS_UNEXPECTED"
    );
  }
}
