import { HttpStatus } from "@nestjs/common";
import type { ValidationError } from "class-validator";

import type { ApiErrorDetail } from "./api-envelope.js";
import { ApiException } from "./api-exception.js";

function collectValidationErrors(
  validationErrors: ValidationError[],
  parentPath = "",
): ApiErrorDetail[] {
  return validationErrors.flatMap((validationError) => {
    const path = [parentPath, validationError.property].filter(Boolean).join(".");
    const ownErrors = validationError.constraints
      ? Object.keys(validationError.constraints).map((constraint) => ({
          field: path || undefined,
          code: constraint.toUpperCase(),
          message: "Invalid value.",
        }))
      : [];

    return [...ownErrors, ...collectValidationErrors(validationError.children ?? [], path)];
  });
}

export function validationExceptionFactory(validationErrors: ValidationError[]): ApiException {
  return new ApiException(
    HttpStatus.UNPROCESSABLE_ENTITY,
    "VALIDATION_ERROR",
    "Request validation failed.",
    collectValidationErrors(validationErrors),
  );
}
