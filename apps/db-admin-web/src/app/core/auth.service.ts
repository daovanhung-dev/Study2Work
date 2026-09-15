import { Injectable, signal } from "@angular/core";

import { environment } from "./environment";
import { Permission } from "./models";

interface JwtPayload {
  sub?: string;
  permissions?: string[] | string;
  scope?: string;
  roles?: string[] | string;
}

function asSet(value: string[] | string | undefined): Set<string> {
  if (typeof value === "string") return new Set(value.split(" ").filter(Boolean));
  return new Set(value ?? []);
}

@Injectable({ providedIn: "root" })
export class AuthService {
  readonly token = signal<string | null>(null);
  readonly permissions = signal<Set<string>>(new Set());

  constructor() {
    this.restoreTokenFromRedirect();
  }

  get isLocalDevAccess(): boolean {
    return environment.localDevAccess;
  }

  can(permission: Permission): boolean {
    return environment.localDevAccess || this.permissions().has(permission);
  }

  login(): void {
    window.location.assign(environment.identityLoginUrl);
  }

  logout(): void {
    this.token.set(null);
    this.permissions.set(new Set());
  }

  setToken(token: string): void {
    this.token.set(token);
    const payload = this.decodePayload(token);
    const values = asSet(payload?.permissions);
    payload?.scope?.split(" ").filter(Boolean).forEach((value) => values.add(value));
    if (asSet(payload?.roles).has("DB_ADMIN")) {
      ["db_admin:read", "db_admin:write", "db_admin:sql"].forEach((value) => values.add(value));
    }
    this.permissions.set(values);
  }

  private restoreTokenFromRedirect(): void {
    const hash = window.location.hash.replace(/^#/, "");
    const token = new URLSearchParams(hash).get("access_token");
    if (!token) return;
    this.setToken(token);
    window.history.replaceState({}, document.title, window.location.pathname + window.location.search);
  }

  private decodePayload(token: string): JwtPayload | undefined {
    try {
      const encoded = token.split(".")[1];
      if (!encoded) return undefined;
      const json = decodeURIComponent(
        atob(encoded.replace(/-/g, "+").replace(/_/g, "/"))
          .split("")
          .map((char) => `%${`00${char.charCodeAt(0).toString(16)}`.slice(-2)}`)
          .join(""),
      );
      return JSON.parse(json) as JwtPayload;
    } catch {
      return undefined;
    }
  }
}
