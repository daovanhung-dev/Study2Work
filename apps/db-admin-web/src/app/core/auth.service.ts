import { Injectable, Injector, inject, signal } from "@angular/core";
import { Observable, tap } from "rxjs";

import { environment } from "./environment";
import { AdminAuthSession, AdminUserProfile, Permission, SchemaBinding } from "./models";
import { ApiService } from "./api.service";

interface JwtPayload {
  sub?: string;
  permissions?: string[] | string;
  scope?: string;
  roles?: string[] | string;
  userId?: string;
  username?: string;
  isRoot?: boolean;
  mustChangePassword?: boolean;
  targets?: string[];
  schemaBindings?: SchemaBinding[];
}

function asSet(value: string[] | string | undefined): Set<string> {
  if (typeof value === "string") return new Set(value.split(" ").filter(Boolean));
  return new Set(value ?? []);
}

@Injectable({ providedIn: "root" })
export class AuthService {
  readonly token = signal<string | null>(null);
  readonly permissions = signal<Set<string>>(new Set());
  readonly profile = signal<AdminUserProfile | null>(null);
  readonly targets = signal<string[]>([]);
  readonly schemaBindings = signal<SchemaBinding[]>([]);
  readonly mustChangePassword = signal(false);
  readonly isRoot = signal(false);

  private readonly injector = inject(Injector);

  constructor() {
    this.restoreTokenFromRedirect();
  }

  get isLocalDevAccess(): boolean {
    return environment.localDevAccess;
  }

  get localAuthEnabled(): boolean {
    return environment.localAuthEnabled;
  }

  can(permission: Permission): boolean {
    return environment.localDevAccess || this.permissions().has(permission);
  }

  loginLocal(username: string, password: string): Observable<AdminAuthSession> {
    return this.injector.get(ApiService).login(username, password).pipe(tap((session) => this.setSession(session)));
  }

  changePassword(currentPassword: string, newPassword: string): Observable<AdminAuthSession> {
    return this.injector
      .get(ApiService)
      .changePassword({ current_password: currentPassword, new_password: newPassword })
      .pipe(tap((session) => this.setSession(session)));
  }

  login(): void {
    window.location.assign(environment.identityLoginUrl);
  }

  logout(): void {
    this.token.set(null);
    this.permissions.set(new Set());
    this.profile.set(null);
    this.targets.set([]);
    this.schemaBindings.set([]);
    this.mustChangePassword.set(false);
    this.isRoot.set(false);
  }

  setSession(session: AdminAuthSession): void {
    this.setToken(session.accessToken);
    this.permissions.set(new Set(session.permissions));
    this.profile.set(session.user);
    this.targets.set(session.targets);
    this.schemaBindings.set(session.schemaBindings);
    this.mustChangePassword.set(session.mustChangePassword);
    this.isRoot.set(session.user.isRoot);
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
    this.profile.set({
      id: payload?.userId ?? payload?.sub ?? "unknown",
      username: payload?.username,
      isRoot: Boolean(payload?.isRoot),
    });
    this.targets.set(payload?.targets ?? []);
    this.schemaBindings.set(payload?.schemaBindings ?? []);
    this.mustChangePassword.set(Boolean(payload?.mustChangePassword));
    this.isRoot.set(Boolean(payload?.isRoot));
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
