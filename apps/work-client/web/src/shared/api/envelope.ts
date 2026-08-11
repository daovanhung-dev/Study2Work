import { z } from "zod";

export const apiFieldErrorSchema = z.object({
  field: z.string().min(1).optional(),
  code: z.string().min(1),
  message: z.string().min(1),
});

export const apiMetaSchema = z
  .object({
    fieldErrors: z.array(apiFieldErrorSchema).optional(),
  })
  .catchall(z.unknown());

export const apiSuccessEnvelopeSchema = z.object({
  success: z.literal(true),
  businessCode: z.string().min(1),
  message: z.string(),
  data: z.unknown(),
  meta: apiMetaSchema,
  traceId: z.string().min(1),
});

export const apiErrorEnvelopeSchema = z.object({
  success: z.literal(false),
  businessCode: z.string().min(1),
  message: z.string(),
  data: z.null(),
  meta: apiMetaSchema,
  traceId: z.string().min(1),
});

export const apiEnvelopeSchema = z.union([apiSuccessEnvelopeSchema, apiErrorEnvelopeSchema]);

export type ApiFieldError = z.infer<typeof apiFieldErrorSchema>;
export type ApiMeta = z.infer<typeof apiMetaSchema>;

export interface ApiSuccessEnvelope<TData, TMeta extends ApiMeta = ApiMeta> {
  success: true;
  businessCode: string;
  message: string;
  data: TData;
  meta: TMeta;
  traceId: string;
}

export interface ApiErrorEnvelope<TMeta extends ApiMeta = ApiMeta> {
  success: false;
  businessCode: string;
  message: string;
  data: null;
  meta: TMeta;
  traceId: string;
}

export type ApiEnvelope<TData, TMeta extends ApiMeta = ApiMeta> =
  | ApiSuccessEnvelope<TData, TMeta>
  | ApiErrorEnvelope<TMeta>;

export function isSuccessEnvelope<TData>(
  envelope: ApiEnvelope<TData> | unknown,
): envelope is ApiSuccessEnvelope<TData> {
  return apiSuccessEnvelopeSchema.safeParse(envelope).success;
}

export function parseApiEnvelope<TData>(payload: unknown): ApiEnvelope<TData> {
  const result = apiEnvelopeSchema.safeParse(payload);

  if (!result.success) {
    throw new Error("The Work API returned an invalid response envelope.");
  }

  return result.data as ApiEnvelope<TData>;
}

export function getFieldErrors(envelope: ApiErrorEnvelope): ApiFieldError[] {
  return envelope.meta.fieldErrors ?? [];
}
