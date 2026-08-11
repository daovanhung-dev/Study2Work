import { SetMetadata } from "@nestjs/common";

import type { ApiMeta } from "../http/api-envelope.js";

export interface ApiSuccessMetadata {
  businessCode: string;
  message: string;
  meta?: ApiMeta;
}

export const API_SUCCESS_KEY = "work:apiSuccess";

/** Supply the stable success contract used by the global envelope interceptor. */
export function ApiSuccess(
  businessCode: string,
  message: string,
  meta?: ApiMeta,
): ReturnType<typeof SetMetadata> {
  return SetMetadata(API_SUCCESS_KEY, { businessCode, message, meta } satisfies ApiSuccessMetadata);
}
