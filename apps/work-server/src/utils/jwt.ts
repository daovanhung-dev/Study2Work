import jwt, { JwtPayload, SignOptions } from "jsonwebtoken";
import { JWT_EXPIRES, JWT_SECRET } from "./constants.js";

export interface TokenPayload extends JwtPayload {
  id: number;
  email: string;
  role: "student" | "business" | string;
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
  const payload = jwt.verify(token, JWT_SECRET);
  if (
    typeof payload !== "object" ||
    payload === null ||
    typeof payload.id !== "number" ||
    typeof payload.email !== "string" ||
    typeof payload.role !== "string"
  ) {
    throw new Error("Invalid JWT payload");
  }

  return payload as TokenPayload;
}
