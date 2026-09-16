import jwt, { JwtPayload, SignOptions } from "jsonwebtoken";
import { JWT_EXPIRES, JWT_SECRET } from "./constants.js";

export interface TokenPayload extends JwtPayload {
  id: number;
  email: string;
  role: string;
}

export function signToken(payload: TokenPayload): string {
  const options: SignOptions = {
    expiresIn: JWT_EXPIRES as SignOptions["expiresIn"],
  };

  return jwt.sign(
    payload,
    JWT_SECRET,
    options
  );
}

export function verifyToken(token: string): TokenPayload {
  return jwt.verify(token, JWT_SECRET) as TokenPayload;
}
