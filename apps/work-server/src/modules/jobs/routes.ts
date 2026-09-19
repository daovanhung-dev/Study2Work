import { Router } from "express";

import { upload } from "../../config/multer.js";
import { asyncHandler } from "../../core/middleware.js";
import { sendSuccess } from "../../core/responses.js";
import type { WorkDependencies } from "../../core/dependencies.js";
import { AuthenticatedRequest } from "../../middleware/auth.middleware.js";
import { jobsQuerySchema, jobMutationSchema } from "./models.js";
import { createBusinessJob, deleteBusinessJob, getBusinessJobs, getJob, getJobs, updateBusinessJob } from "./view.js";

export function createJobsRouter(dependencies: WorkDependencies): Router {
  const router = Router();

  router.get("/", asyncHandler(async (request, response) => {
    const query = jobsQuerySchema.parse({ page: request.query.page, limit: request.query.limit });
    const result = await getJobs(dependencies.prisma, query.page ?? 1, query.limit ?? 6);
    return sendSuccess(request, response, result.statusCode, result.businessCode, result.message, result.data, result.meta);
  }));

  router.get("/:id", asyncHandler(async (request, response) => {
    const result = await getJob(dependencies.prisma, request.params.id);
    return sendSuccess(request, response, result.statusCode, result.businessCode, result.message, result.data, result.meta);
  }));

  return router;
}

export function createBusinessJobsRouter(dependencies: WorkDependencies): Router {
  const router = Router();

  router.get("/", asyncHandler(async (request, response) => {
    const user = (request as AuthenticatedRequest).user;
    const result = await getBusinessJobs(dependencies.prisma, user.id);
    return sendSuccess(request, response, result.statusCode, result.businessCode, result.message, result.data, result.meta);
  }));

  router.post("/", upload.single("avt"), asyncHandler(async (request, response) => {
    const body = jobMutationSchema.parse(request.body) as Record<string, unknown>;
    const user = (request as AuthenticatedRequest).user;
    const result = await createBusinessJob(dependencies.prisma, user.id, body, request.file?.filename);
    return sendSuccess(request, response, result.statusCode, result.businessCode, result.message, result.data, result.meta);
  }));

  router.put("/:jobId", upload.single("avt"), asyncHandler(async (request, response) => {
    const body = jobMutationSchema.parse(request.body) as Record<string, unknown>;
    const user = (request as AuthenticatedRequest).user;
    const result = await updateBusinessJob(dependencies.prisma, user.id, request.params.jobId, body, request.file?.filename);
    return sendSuccess(request, response, result.statusCode, result.businessCode, result.message, result.data, result.meta);
  }));

  router.delete("/:jobId", asyncHandler(async (request, response) => {
    const user = (request as AuthenticatedRequest).user;
    const result = await deleteBusinessJob(dependencies.prisma, user.id, request.params.jobId);
    return sendSuccess(request, response, result.statusCode, result.businessCode, result.message, result.data, result.meta);
  }));

  return router;
}
