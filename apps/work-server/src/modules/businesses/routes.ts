import { Router } from "express";

import { asyncHandler } from "../../core/middleware.js";
import { sendSuccess } from "../../core/responses.js";
import type { WorkDependencies } from "../../core/dependencies.js";
import { AuthenticatedRequest } from "../../middleware/auth.middleware.js";
import { getBusinessMe } from "./view.js";

export function createBusinessRouter(dependencies: WorkDependencies): Router {
  const router = Router();

  router.get("/me", asyncHandler(async (request, response) => {
    const user = (request as AuthenticatedRequest).user;
    const result = await getBusinessMe(dependencies.prisma, user.id);
    return sendSuccess(request, response, result.statusCode, result.businessCode, result.message, result.data, result.meta);
  }));

  return router;
}
