import { identityLoginUrl } from "../api/runtime";

export function safeInternalReturnPath(value: string): string {
  return value.startsWith("/") && !value.startsWith("//") ? value : "/jobs";
}

export function buildIdentityLoginUrl(returnTo: string): string {
  const safeReturnTo = safeInternalReturnPath(returnTo);

  try {
    const url = new URL(identityLoginUrl);
    url.searchParams.set("returnTo", safeReturnTo);
    return url.toString();
  } catch {
    return identityLoginUrl;
  }
}
