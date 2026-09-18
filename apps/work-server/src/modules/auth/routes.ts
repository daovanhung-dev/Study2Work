import { Router } from "express";

import { asyncHandler } from "../../core/middleware.js";
import { sendSuccess } from "../../core/responses.js";
import type { WorkDependencies } from "../../core/dependencies.js";
import { ensureAuthenticated } from "../../middleware/auth.middleware.js";
import { loginRequestSchema, loginPassword } from "./models.js";
import { loginBusiness, loginStudent, logout } from "./view.js";

export function createAuthRouter(dependencies: WorkDependencies): Router {
  const router = Router();

  router.post("/student/login", asyncHandler(async (request, response) => {
    const input = loginRequestSchema.parse(request.body);
    const result = await loginStudent(dependencies.prisma, dependencies.config, input.email, loginPassword(input));
    return sendSuccess(request, response, result.statusCode, result.businessCode, result.message, result.data, result.meta);
  }));

  router.post("/business/login", asyncHandler(async (request, response) => {
    const input = loginRequestSchema.parse(request.body);
    const result = await loginBusiness(dependencies.prisma, dependencies.config, input.email, loginPassword(input));
    return sendSuccess(request, response, result.statusCode, result.businessCode, result.message, result.data, result.meta);
  }));

  router.post("/logout", ensureAuthenticated, asyncHandler(async (request, response) => {
    const result = logout();
    return sendSuccess(request, response, result.statusCode, result.businessCode, result.message, result.data, result.meta);
  }));

  return router;
}
