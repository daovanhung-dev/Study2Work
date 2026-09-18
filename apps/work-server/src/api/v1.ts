import { Router } from "express";

import { createApplicationsRouter } from "../modules/applications/routes.js";
import { createAuthRouter } from "../modules/auth/routes.js";
import { createBusinessJobsRouter, createJobsRouter } from "../modules/jobs/routes.js";
import { createBusinessStudentCvRouter, createStudentCvRouter } from "../modules/cv/routes.js";
import { createStudentRouter } from "../modules/students/routes.js";
import { asyncHandler } from "../core/middleware.js";
import { sendSuccess } from "../core/responses.js";
import type { WorkDependencies } from "../core/dependencies.js";
import { checkRole, ensureAuthenticated, type AuthenticatedRequest } from "../middleware/auth.middleware.js";
import { getBusinessMe } from "../modules/businesses/view.js";
import { getStudentMe } from "../modules/students/view.js";

export function createV1Router(dependencies: WorkDependencies): Router {
  const router = Router();

  router.get("/", (request, response) => sendSuccess(
    request,
    response,
    200,
    "SYSTEM_ROOT_LOADED",
    "Welcome to Study2Work.",
    { service: "work-api" },
  ));

  router.use("/auth", createAuthRouter(dependencies));
  router.use("/students", createStudentRouter(dependencies));
  router.use("/jobs", createJobsRouter(dependencies));

  router.use(ensureAuthenticated);

  router.get("/me", asyncHandler(async (request, response) => {
    const user = (request as AuthenticatedRequest).user;
    const result = user.role === "student"
      ? await getStudentMe(dependencies.prisma, user.id)
      : await getBusinessMe(dependencies.prisma, user.id);
    return sendSuccess(request, response, result.statusCode, result.businessCode, result.message, result.data, result.meta);
  }));

  router.use("/students/me/cv", checkRole("student"), createStudentCvRouter(dependencies));
  router.use("/students", createBusinessStudentCvRouter(dependencies));
  router.use("/businesses/me/jobs", checkRole("business"), createBusinessJobsRouter(dependencies));
  router.use("/", createApplicationsRouter(dependencies));

  return router;
}
