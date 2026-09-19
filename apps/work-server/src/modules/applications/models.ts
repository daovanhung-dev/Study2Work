import { z } from "zod";

export const emptyApplicationBodySchema = z.record(z.unknown());

export const applicationJobIdSchema = z.string()
  .regex(/^\d+$/, "ID việc làm không hợp lệ.")
  .transform(Number)
  .refine((value) => Number.isSafeInteger(value) && value > 0, "ID việc làm không hợp lệ.");
