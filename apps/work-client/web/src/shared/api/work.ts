import { z } from "zod";

import { getAccessToken, clearAuthToken } from "../auth/store";

export const apiBase = "/api/v1";

export const userSchema = z.object({
  id: z.number(),
  email: z.string(),
  role: z.string(),
}).passthrough();

export const authResponseSchema = z.object({
  token: z.string(),
  user: userSchema,
});

export const apiEnvelopeSchema = z.object({
  success: z.boolean(),
  businessCode: z.string(),
  message: z.string(),
  data: z.unknown(),
  meta: z.record(z.string(), z.unknown()),
  traceId: z.string(),
});

export type User = z.infer<typeof userSchema>;
export type AuthResponse = z.infer<typeof authResponseSchema>;
export type Job = Record<string, unknown> & { id?: number | string; ten_vi_tri?: string };
export type Cv = Record<string, unknown> & { id?: number | string; hoten?: string; email?: string };

export class WorkApiError extends Error {
  constructor(public readonly status: number, public readonly businessCode: string, message: string) {
    super(message);
    this.name = "WorkApiError";
  }
}

function asApiError(value: unknown, status: number): WorkApiError {
  const parsed = apiEnvelopeSchema.safeParse(value);
  return parsed.success
    ? new WorkApiError(status, parsed.data.businessCode, parsed.data.message)
    : new WorkApiError(status, "HTTP_ERROR", "Không thể kết nối Work server.");
}

export async function apiRequest<T>(
  path: string,
  options: { method?: string; body?: BodyInit; query?: Record<string, string | number | undefined> } = {},
  schema: z.ZodType<T> = z.unknown() as z.ZodType<T>,
): Promise<{ data: T; meta: Record<string, unknown> }> {
  const url = new URL(`${apiBase}${path}`, window.location.origin);
  for (const [key, value] of Object.entries(options.query || {})) {
    if (value !== undefined) url.searchParams.set(key, String(value));
  }
  const headers = new Headers({ Accept: "application/json" });
  const token = getAccessToken();
  if (token) headers.set("Authorization", `Bearer ${token}`);
  if (options.body instanceof URLSearchParams) headers.set("Content-Type", "application/x-www-form-urlencoded;charset=UTF-8");
  else if (options.body && !(options.body instanceof FormData)) headers.set("Content-Type", "application/json");

  const response = await fetch(url, {
    method: options.method || "GET",
    headers,
    body: options.body,
    credentials: "omit",
  });
  const payload: unknown = await response.json().catch(() => null);
  if (!response.ok) {
    if (response.status === 401) clearAuthToken();
    throw asApiError(payload, response.status);
  }
  const envelope = apiEnvelopeSchema.safeParse(payload);
  if (!envelope.success || !envelope.data.success) {
    throw asApiError(payload, response.status);
  }
  return { data: schema.parse(envelope.data.data), meta: envelope.data.meta };
}

export function loginStudent(email: string, password: string) {
  return apiRequest("/auth/student/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  }, authResponseSchema);
}

export function loginBusiness(email: string, password: string) {
  return apiRequest("/auth/business/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  }, authResponseSchema);
}

export function registerStudent(form: FormData) {
  return apiRequest("/students", { method: "POST", body: form });
}

export function getMe() {
  return apiRequest("/me", {}, z.record(z.string(), z.unknown()));
}

export function getJobs(page = 1, limit = 6) {
  return apiRequest("/jobs", { query: { page, limit } }, z.array(z.record(z.string(), z.unknown())));
}

export function getJob(id: string) {
  return apiRequest(`/jobs/${encodeURIComponent(id)}`, {}, z.record(z.string(), z.unknown()));
}

export function getMyCv() {
  return apiRequest("/students/me/cv", {}, z.record(z.string(), z.unknown()));
}

export function createCv(form: FormData) {
  return apiRequest("/students/me/cv", { method: "POST", body: form });
}

export function updateCv(id: string | number, form: FormData) {
  return apiRequest(`/students/me/cv/${encodeURIComponent(id)}`, { method: "PUT", body: form });
}

export function getMyApplications() {
  return apiRequest("/students/me/applications", {}, z.array(z.record(z.string(), z.unknown())));
}

export function applyToJob(id: string | number) {
  return apiRequest(`/jobs/${encodeURIComponent(id)}/applications`, { method: "POST", body: JSON.stringify({}) });
}

export function getBusinessJobs() {
  return apiRequest("/businesses/me/jobs", {}, z.array(z.record(z.string(), z.unknown())));
}

export function createBusinessJob(form: FormData) {
  return apiRequest("/businesses/me/jobs", { method: "POST", body: form });
}

export function updateBusinessJob(id: string | number, form: FormData) {
  return apiRequest(`/businesses/me/jobs/${encodeURIComponent(id)}`, { method: "PUT", body: form });
}

export function deleteBusinessJob(id: string | number) {
  return apiRequest(`/businesses/me/jobs/${encodeURIComponent(id)}`, { method: "DELETE" });
}

export function getBusinessApplications() {
  return apiRequest("/businesses/me/applications", {}, z.array(z.record(z.string(), z.unknown())));
}

export function getStudentCv(id: string) {
  return apiRequest(`/students/${encodeURIComponent(id)}/cv`, {}, z.record(z.string(), z.unknown()));
}

export function logout() {
  return apiRequest("/auth/logout", { method: "POST" });
}
