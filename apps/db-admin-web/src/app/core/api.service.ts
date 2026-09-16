import { HttpClient, HttpErrorResponse, HttpParams } from "@angular/common/http";
import { Injectable, inject } from "@angular/core";
import { catchError, map, throwError } from "rxjs";

import { environment } from "./environment";
import {
  ApiEnvelope,
  AccessAccountsResult,
  AccessAccount,
  AccessAuditResult,
  AdminAuthSession,
  AuditResult,
  CatalogData,
  ConnectionInfo,
  DatabaseTargetResult,
  RowPreview,
  RowResult,
  SqlRequest,
  SqlResult,
  SqlValidation,
} from "./models";

export class AdminApiError extends Error {
  constructor(
    message: string,
    readonly status: number,
    readonly businessCode?: string,
    readonly traceId?: string,
  ) {
    super(message);
    this.name = "AdminApiError";
  }
}

@Injectable({ providedIn: "root" })
export class ApiService {
  private readonly http = inject(HttpClient);

  login(username: string, password: string) {
    return this.request<AdminAuthSession>("POST", "/auth/login", { username, password });
  }
  changePassword(payload: { current_password: string; new_password: string }) {
    return this.request<AdminAuthSession>("POST", "/auth/change-password", payload);
  }
  getMe() { return this.request<AdminAuthSession>("GET", "/auth/me"); }
  getDatabases() { return this.request<DatabaseTargetResult>("GET", "/databases"); }
  getConnection() { return this.request<ConnectionInfo>("GET", "/connection"); }
  getCatalog(database?: string) {
    const params = database ? new HttpParams().set("database", database) : undefined;
    return this.request<CatalogData>("GET", "/catalog", undefined, params);
  }
  getAudit(limit = 100) { return this.request<AuditResult>("GET", `/audit?limit=${limit}`); }
  getAccessAccounts(database?: string) {
    const params = database ? new HttpParams().set("database", database) : undefined;
    return this.request<AccessAccountsResult>("GET", "/access/accounts", undefined, params);
  }
  createAccessAccount(payload: { database: string; username: string; display_name: string; schema_name: string }) {
    return this.request<AccessAccount>("POST", "/access/accounts", payload);
  }
  updateAccessAccount(userId: string, payload: { display_name?: string; status?: "active" | "disabled" }) {
    return this.request<AccessAccount>("PATCH", `/access/accounts/${encodeURIComponent(userId)}`, payload);
  }
  changeAccessSchema(userId: string, payload: { database: string; schema_name: string }) {
    return this.request<AccessAccount>("PUT", `/access/accounts/${encodeURIComponent(userId)}/schema`, payload);
  }
  rotateAccessPassword(userId: string) {
    return this.request<AccessAccount>("POST", `/access/accounts/${encodeURIComponent(userId)}/rotate-password`);
  }
  getAccessAudit(options: { database?: string; actor?: string; action?: string; limit?: number } = {}) {
    let params = new HttpParams().set("limit", String(options.limit ?? 100));
    if (options.database) params = params.set("database", options.database);
    if (options.actor) params = params.set("actor", options.actor);
    if (options.action) params = params.set("action", options.action);
    return this.request<AccessAuditResult>("GET", "/access/audit", undefined, params);
  }
  previewDdl(payload: unknown) { return this.request<unknown>("POST", "/ddl/preview", payload); }
  applyDdl(payload: unknown) { return this.request<unknown>("POST", "/ddl/apply", payload); }
  validateSql(payload: SqlRequest | string) {
    const body = typeof payload === "string" ? { sql: payload } : payload;
    return this.request<SqlValidation>("POST", "/sql/validate", body);
  }
  executeSql(payload: Partial<SqlRequest> & { sql: string; confirmation_token?: string | null; max_rows?: number }) {
    return this.request<SqlResult>("POST", "/sql/execute", payload);
  }
  getRows(schema: string, table: string, options: { limit?: number; offset?: number; sortColumn?: string; sortDirection?: string; filters?: unknown[] } = {}) {
    let params = new HttpParams()
      .set("limit", String(options.limit ?? 100))
      .set("offset", String(options.offset ?? 0));
    if (options.sortColumn) params = params.set("sort_column", options.sortColumn);
    if (options.sortDirection) params = params.set("sort_direction", options.sortDirection);
    if (options.filters?.length) params = params.set("filters", JSON.stringify(options.filters));
    return this.request<RowResult>("GET", `/tables/${encodeURIComponent(schema)}/${encodeURIComponent(table)}/rows`, undefined, params);
  }
  previewRowMutation(schema: string, table: string, payload: { operation: "insert" | "update" | "delete"; values?: Record<string, unknown>; primary_key?: Record<string, unknown> }) {
    return this.request<RowPreview>("POST", `/tables/${encodeURIComponent(schema)}/${encodeURIComponent(table)}/rows/preview`, payload);
  }
  insertRow(schema: string, table: string, values: Record<string, unknown>, confirmation_token: string) {
    return this.request<Record<string, unknown>>("POST", `/tables/${encodeURIComponent(schema)}/${encodeURIComponent(table)}/rows`, { values, confirmation_token });
  }
  updateRow(schema: string, table: string, primary_key: Record<string, unknown>, values: Record<string, unknown>, confirmation_token: string) {
    return this.request<Record<string, unknown>>("PATCH", `/tables/${encodeURIComponent(schema)}/${encodeURIComponent(table)}/rows`, { primary_key, values, confirmation_token });
  }
  deleteRow(schema: string, table: string, primary_key: Record<string, unknown>, confirmation_token: string) {
    return this.request<null>("DELETE", `/tables/${encodeURIComponent(schema)}/${encodeURIComponent(table)}/rows`, { primary_key, confirmation_token });
  }

  private request<T>(method: string, path: string, body?: unknown, params?: HttpParams) {
    return this.http.request<ApiEnvelope<T>>(method, `${environment.apiBaseUrl}${path}`, {
      body,
      params,
      headers: { Accept: "application/json", "Content-Type": "application/json" },
    }).pipe(
      map((envelope) => {
        if (!envelope.success) {
          throw new AdminApiError(envelope.message, 400, envelope.businessCode, envelope.traceId);
        }
        return envelope.data;
      }),
      catchError((error: unknown) => {
        if (error instanceof AdminApiError) return throwError(() => error);
        if (error instanceof HttpErrorResponse) {
          const payload = error.error as Partial<ApiEnvelope<unknown>> | undefined;
          return throwError(() => new AdminApiError(payload?.message ?? "Không thể kết nối DB Admin.", error.status, payload?.businessCode, payload?.traceId));
        }
        return throwError(() => error);
      }),
    );
  }
}
