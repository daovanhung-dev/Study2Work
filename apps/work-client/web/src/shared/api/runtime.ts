const defaultWorkApiBaseUrl = "http://localhost:8001/api/v1";

function withoutTrailingSlash(value: string): string {
  return value.replace(/\/+$/, "");
}

export const workApiBaseUrl = withoutTrailingSlash(
  import.meta.env.VITE_WORK_API_URL?.trim() || defaultWorkApiBaseUrl,
);

export const identityApiBaseUrl = (() => {
  const value = import.meta.env.VITE_IDENTITY_API_URL?.trim();
  return value ? withoutTrailingSlash(value) : undefined;
})();

export const identityLoginUrl =
  import.meta.env.VITE_IDENTITY_LOGIN_URL?.trim() || "https://identity.study2work.vn/login";
