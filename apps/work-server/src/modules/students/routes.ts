import { Router } from "express";

import { upload } from "../../config/multer.js";
import { asyncHandler } from "../../core/middleware.js";
import { sendSuccess } from "../../core/responses.js";
import type { WorkDependencies } from "../../core/dependencies.js";
import { studentRegistrationSchema } from "./models.js";
import { registerStudent } from "./view.js";

export function createStudentRouter(dependencies: WorkDependencies): Router {
  const router = Router();

  router.post("/", upload.single("avt"), asyncHandler(async (request, response) => {
    const input = studentRegistrationSchema.parse(request.body);
    const result = await registerStudent(dependencies.prisma, { ...input, avt: request.file?.filename ?? null });
    return sendSuccess(request, response, result.statusCode, result.businessCode, result.message, result.data, result.meta);
  }));

  return router;
}
