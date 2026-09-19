import { Router } from "express";

import { asyncHandler } from "../../core/middleware.js";
import { sendSuccess } from "../../core/responses.js";
import type { WorkDependencies } from "../../core/dependencies.js";
import { AuthenticatedRequest, checkRole } from "../../middleware/auth.middleware.js";
import { applyToJob, getBusinessApplications, getStudentApplications } from "./view.js";

export function createApplicationsRouter(dependencies: WorkDependencies): Router {
  const router = Router();

  router.post("/jobs/:jobId/applications", checkRole("student"), asyncHandler(async (request, response) => {
    const user = (request as AuthenticatedRequest).user;
    const result = await applyToJob(dependencies.prisma, user.id, request.params.jobId);
    return sendSuccess(request, response, result.statusCode, result.businessCode, result.message, result.data, result.meta);
  }));

  router.get("/students/me/applications", checkRole("student"), asyncHandler(async (request, response) => {
    const user = (request as AuthenticatedRequest).user;
    const result = await getStudentApplications(dependencies.prisma, user.id);
    return sendSuccess(request, response, result.statusCode, result.businessCode, result.message, result.data, result.meta);
  }));

  router.get("/businesses/me/applications", checkRole("business"), asyncHandler(async (request, response) => {
    const user = (request as AuthenticatedRequest).user;
    const result = await getBusinessApplications(dependencies.prisma, user.id);
    return sendSuccess(request, response, result.statusCode, result.businessCode, result.message, result.data, result.meta);
  }));

  return router;
}
