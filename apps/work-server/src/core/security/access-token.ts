import jwt, { type JwtPayload, type SignOptions } from "jsonwebtoken";

import type { WorkConfig } from "../config.js";

export interface WorkTokenPayload extends JwtPayload {
  id: number;
  email: string;
  role: "student" | "business" | string;
}

export function signAccessToken(config: WorkConfig, payload: WorkTokenPayload): string {
  const options: SignOptions = { expiresIn: config.jwtExpires as SignOptions["expiresIn"] };
  return jwt.sign(payload, config.jwtSecret, options);
}

export function decodeAccessToken(config: WorkConfig, token: string): WorkTokenPayload {
  const payload = jwt.verify(token, config.jwtSecret, { algorithms: ["HS256"] });
  if (
    typeof payload !== "object" ||
    payload === null ||
    typeof payload.id !== "number" ||
    !Number.isSafeInteger(payload.id) ||
    payload.id < 1 ||
    typeof payload.email !== "string" ||
    !["student", "business"].includes(String(payload.role))
  ) {
    throw new Error("Invalid JWT payload");
  }
  return payload as WorkTokenPayload;
}
