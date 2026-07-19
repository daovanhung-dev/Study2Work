import jwt, { JwtPayload, SignOptions } from "jsonwebtoken";
import { env } from "../config/env.js";

export interface TokenPayload extends JwtPayload {
  id: number;
  email: string;
  role: string;
}

export function signToken(payload: TokenPayload): string {
  const options: SignOptions = {
    expiresIn: env.jwtExpires as SignOptions["expiresIn"],
  };

  return jwt.sign(
    payload,
    env.jwtSecret,
    options
  );
}

export function verifyToken(token: string): TokenPayload {
  return jwt.verify(token, env.jwtSecret) as TokenPayload;
}
