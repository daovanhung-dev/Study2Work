import jwt, { JwtPayload, SignOptions } from "jsonwebtoken";

export interface TokenPayload extends JwtPayload {
  id: number;
  email: string;
  role: string;
}

export function signToken(payload: TokenPayload): string {
  const options: SignOptions = {
    expiresIn: process.env.JWT_EXPIRES as SignOptions["expiresIn"],
  };

  return jwt.sign(
    payload,
    process.env.JWT_SECRET as string,
    options
  );
}

export function verifyToken(token: string): TokenPayload {
  return jwt.verify(token, process.env.JWT_SECRET as string) as TokenPayload;
}
