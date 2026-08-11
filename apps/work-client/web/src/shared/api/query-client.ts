import { QueryClient } from "@tanstack/react-query";

import { isRetryableApiError } from "./http";

export function createWorkQueryClient(): QueryClient {
  return new QueryClient({
    defaultOptions: {
      queries: {
        staleTime: 30_000,
        gcTime: 5 * 60_000,
        refetchOnWindowFocus: false,
        retry: (failureCount, error) => isRetryableApiError(error) && failureCount < 2,
        retryDelay: (attempt) => Math.min(1_000 * 2 ** attempt, 10_000),
      },
      mutations: {
        retry: false,
      },
    },
  });
}

export const workQueryClient = createWorkQueryClient();

export const workQueryKeys = {
  session: ["session"] as const,
  publicJobs: (filters: Record<string, unknown>) => ["jobs", "public", filters] as const,
  candidate: (scope: string) => ["candidate", scope] as const,
  enterprise: (enterpriseId: string, scope: string) =>
    ["enterprise", enterpriseId, scope] as const,
  university: (universityId: string, scope: string) =>
    ["university", universityId, scope] as const,
  ops: (scope: string) => ["ops", scope] as const,
};

/** Clears tenant-, candidate-, and operator-scoped data when the active workspace changes. */
export function clearPrivateWorkQueries(): void {
  workQueryClient.removeQueries({
    predicate: (query) => {
      const scope = query.queryKey[0];
      return scope === "candidate" || scope === "enterprise" || scope === "university" || scope === "ops";
    },
  });
}
