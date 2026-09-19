import bcrypt from "bcrypt";

export const PASSWORD_HASH_ROUNDS = 12;

function isBcryptHash(value: string | null | undefined): boolean {
  return typeof value === "string" && /^\$2[abxy]\$\d{2}\$/.test(value);
}

export async function hashPassword(password: string): Promise<string> {
  return bcrypt.hash(password, PASSWORD_HASH_ROUNDS);
}

export async function verifyPassword(
  password: string,
  storedPassword: string | null,
): Promise<{ valid: boolean; needsRehash: boolean }> {
  if (!storedPassword) return { valid: false, needsRehash: false };

  if (isBcryptHash(storedPassword)) {
    return {
      valid: await bcrypt.compare(password, storedPassword),
      needsRehash: false,
    };
  }

  return {
    valid: storedPassword === password,
    needsRehash: storedPassword === password,
  };
}
