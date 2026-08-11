import { SetMetadata } from "@nestjs/common";

export const IS_PUBLIC_KEY = "work:isPublic";

/** Mark a route as intentionally reachable without an access token. */
export const Public = (): ReturnType<typeof SetMetadata> => SetMetadata(IS_PUBLIC_KEY, true);
