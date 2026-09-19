import { loadConfig } from "../core/config.js";
import { decodeAccessToken, signAccessToken, type WorkTokenPayload } from "../core/security/access-token.js";

export type TokenPayload = WorkTokenPayload;

export function signToken(payload: TokenPayload): string {
  return signAccessToken(loadConfig(), payload);
}

export function verifyToken(token: string): TokenPayload {
  return decodeAccessToken(loadConfig(), token);
}
