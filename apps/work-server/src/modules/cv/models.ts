import { z } from "zod";

export const cvMutationSchema = z.record(z.unknown());
export const cvIdSchema = z.string()
  .regex(/^\d+$/, "ID CV không hợp lệ.")
  .transform(Number)
  .refine((value) => Number.isSafeInteger(value) && value > 0, "ID CV không hợp lệ.");
export type CvMutation = z.infer<typeof cvMutationSchema>;
