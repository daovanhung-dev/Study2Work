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
  const payload = jwt.verify(token, JWT_SECRET, { algorithms: ["HS256"] });
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

  return payload as TokenPayload;
}
