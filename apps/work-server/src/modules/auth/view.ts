import type { PrismaClient } from "@prisma/client";

import type { WorkConfig } from "../../core/config.js";
import { ApiError } from "../../core/responses.js";
import { signAccessToken } from "../../core/security/access-token.js";
import { hashPassword, verifyPassword } from "../../core/security/password.js";
import type { UseCaseResult } from "../../core/use-case.js";
import { findBusinessCredentials, findStudentCredentials, rehashBusinessPassword, rehashStudentPassword } from "./query.js";
import { assertLoginPassword } from "./validate.js";

type Credentials = { id: bigint; email: string | null; matkhau: string | null };

async function authenticate(
  credentials: Credentials | null,
  password: string,
  config: WorkConfig,
  role: "student" | "business",
  rehash: (id: bigint, password: string) => Promise<unknown>,
): Promise<UseCaseResult<{ token: string; user: { id: number; email: string; role: string } }>> {
  if (!credentials) {
    throw new ApiError({ statusCode: 401, businessCode: "INVALID_CREDENTIALS", message: "Email hoặc mật khẩu không đúng." });
  }
  const verification = await verifyPassword(password, credentials.matkhau);
  if (!verification.valid) {
    throw new ApiError({ statusCode: 401, businessCode: "INVALID_CREDENTIALS", message: "Email hoặc mật khẩu không đúng." });
  }

  if (verification.needsRehash) {
    await rehash(credentials.id, await hashPassword(password)).catch(() => undefined);
  }

  const user = { id: Number(credentials.id), email: credentials.email ?? "", role };
  return {
    statusCode: 200,
    businessCode: "AUTH_LOGIN_SUCCESS",
    message: "Đăng nhập thành công.",
    data: { token: signAccessToken(config, user), user },
  };
}

export async function loginStudent(
  prisma: PrismaClient,
  config: WorkConfig,
  email: string,
  password: string,
): Promise<UseCaseResult<{ token: string; user: { id: number; email: string; role: string } }>> {
  assertLoginPassword(password);
  return authenticate(
    await findStudentCredentials(prisma, email),
    password,
    config,
    "student",
    (id, nextPassword) => rehashStudentPassword(prisma, id, nextPassword),
  );
}

export async function loginBusiness(
  prisma: PrismaClient,
  config: WorkConfig,
  email: string,
  password: string,
): Promise<UseCaseResult<{ token: string; user: { id: number; email: string; role: string } }>> {
  assertLoginPassword(password);
  return authenticate(
    await findBusinessCredentials(prisma, email),
    password,
    config,
    "business",
    (id, nextPassword) => rehashBusinessPassword(prisma, id, nextPassword),
  );
}

export function logout(): UseCaseResult<null> {
  return {
    statusCode: 200,
    businessCode: "AUTH_LOGOUT_SUCCESS",
    message: "Đăng xuất thành công.",
    data: null,
  };
}
