import { Router } from "express";

import { upload } from "../../config/multer.js";
import { asyncHandler } from "../../core/middleware.js";
import { sendSuccess } from "../../core/responses.js";
import type { WorkDependencies } from "../../core/dependencies.js";
import { AuthenticatedRequest, checkRole } from "../../middleware/auth.middleware.js";
import { cvMutationSchema } from "./models.js";
import { createCv, getMyCv, getStudentCv, updateCv } from "./view.js";

export function createStudentCvRouter(dependencies: WorkDependencies): Router {
  const router = Router();

  router.get("/", asyncHandler(async (request, response) => {
    const user = (request as AuthenticatedRequest).user;
    const result = await getMyCv(dependencies.prisma, user.id);
    return sendSuccess(request, response, result.statusCode, result.businessCode, result.message, result.data, result.meta);
  }));

  router.post("/", upload.single("avt"), asyncHandler(async (request, response) => {
    const body = cvMutationSchema.parse(request.body);
    const user = (request as AuthenticatedRequest).user;
    const result = await createCv(dependencies.prisma, user.id, body, request.file?.filename);
    return sendSuccess(request, response, result.statusCode, result.businessCode, result.message, result.data, result.meta);
  }));

  router.put("/:cvId", upload.single("avt"), asyncHandler(async (request, response) => {
    const body = cvMutationSchema.parse(request.body);
    const user = (request as AuthenticatedRequest).user;
    const result = await updateCv(dependencies.prisma, user.id, request.params.cvId, body, request.file?.filename);
    return sendSuccess(request, response, result.statusCode, result.businessCode, result.message, result.data, result.meta);
  }));

  return router;
}

export function createBusinessStudentCvRouter(dependencies: WorkDependencies): Router {
  const router = Router();

  router.get("/:studentId/cv", checkRole("business"), asyncHandler(async (request, response) => {
    const result = await getStudentCv(dependencies.prisma, request.params.studentId);
    return sendSuccess(request, response, result.statusCode, result.businessCode, result.message, result.data, result.meta);
  }));

  return router;
}
