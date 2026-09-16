import { provideHttpClient } from "@angular/common/http";
import { HttpTestingController, provideHttpClientTesting } from "@angular/common/http/testing";
import { TestBed } from "@angular/core/testing";

import { AdminApiError, ApiService } from "./api.service";

describe("ApiService", () => {
  let api: ApiService;
  let http: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({ providers: [ApiService, provideHttpClient(), provideHttpClientTesting()] });
    api = TestBed.inject(ApiService);
    http = TestBed.inject(HttpTestingController);
  });

  afterEach(() => http.verify());

  it("loads configured database targets without exposing connection details", () => {
    api.getDatabases().subscribe((value) => expect(value.databases[0].id).toBe("work_server"));

    const request = http.expectOne("/api/v1/admin/databases");
    request.flush({
      success: true,
      businessCode: "DB_ADMIN_DATABASES_LOADED",
      message: "ok",
      data: { databases: [{ id: "work_server", label: "Work Server" }] },
      meta: {},
      traceId: "trace",
    });
  });

  it("sends the selected database when loading its catalog", () => {
    api.getCatalog("study_server").subscribe((value) => expect(value.schemas).toEqual([]));

    const request = http.expectOne((item) => item.urlWithParams === "/api/v1/admin/catalog?database=study_server");
    request.flush({
      success: true,
      businessCode: "DB_ADMIN_CATALOG_LOADED",
      message: "ok",
      data: { schemas: [], tables: [], views: [], routines: [], triggers: [], types: [], sequences: [], indexes: [], constraints: [], grants: [] },
      meta: {},
      traceId: "trace",
    });
  });

  it("sends the selected database and schema for SQL validation and execution", () => {
    api.validateSql({ database: "work_server", schema_name: "public", sql: "SELECT 1" }).subscribe();
    const validateRequest = http.expectOne("/api/v1/admin/sql/validate");
    expect(validateRequest.request.body).toEqual({ database: "work_server", schema_name: "public", sql: "SELECT 1" });
    validateRequest.flush({
      success: true,
      businessCode: "DB_ADMIN_SQL_VALIDATED",
      message: "ok",
      data: { database: "work_server", schemaName: "public", classification: "read_only", statementCount: 1, requiresConfirmation: false, warnings: [], confirmationToken: null },
      meta: {},
      traceId: "trace",
    });

    api.executeSql({ database: "work_server", schema_name: "public", sql: "SELECT 1" }).subscribe();
    const executeRequest = http.expectOne("/api/v1/admin/sql/execute");
    expect(executeRequest.request.body).toEqual({ database: "work_server", schema_name: "public", sql: "SELECT 1" });
    executeRequest.flush({
      success: true,
      businessCode: "DB_ADMIN_SQL_EXECUTED",
      message: "ok",
      data: { classification: "read_only", columns: ["?column?"], rows: [{ "?column?": 1 }], rowCount: 1, truncated: false },
      meta: {},
      traceId: "trace",
    });
  });

  it("unwraps the repository response envelope", () => {
    api.getConnection().subscribe((value) => expect(value.database).toBe("study"));

    const request = http.expectOne("/api/v1/admin/connection");
    request.flush({ success: true, businessCode: "DB_ADMIN_CONNECTION_READY", message: "ok", data: { database: "study" }, meta: {}, traceId: "trace" });
  });

  it("sends local credentials and access-management payloads through the API", () => {
    api.login("admin", "temporary-password").subscribe();
    const login = http.expectOne("/api/v1/admin/auth/login");
    expect(login.request.body).toEqual({ username: "admin", password: "temporary-password" });
    login.flush({ success: true, businessCode: "DB_ADMIN_LOGIN_SUCCESS", message: "ok", data: { accessToken: "token", user: { id: "1", isRoot: true }, permissions: [], roles: [], targets: [], schemaBindings: [], mustChangePassword: true }, meta: {}, traceId: "trace" });

    api.createAccessAccount({ database: "study_server", username: "alice", display_name: "Alice", schema_name: "alice" }).subscribe();
    const create = http.expectOne("/api/v1/admin/access/accounts");
    expect(create.request.body).toEqual({ database: "study_server", username: "alice", display_name: "Alice", schema_name: "alice" });
    create.flush({ success: true, businessCode: "DB_ADMIN_ACCESS_ACCOUNT_CREATED", message: "ok", data: { id: "2", username: "alice", isRoot: false, status: "active", mustChangePassword: true, bindings: [], secret: "one-time" }, meta: {}, traceId: "trace" });
  });

  it("maps envelope errors to AdminApiError", () => {
    api.getCatalog().subscribe({
      next: () => fail("Expected the request to fail"),
      error: (error: unknown) => {
        expect(error).toEqual(jasmine.any(AdminApiError));
        expect((error as AdminApiError).businessCode).toBe("DB_ADMIN_FORBIDDEN");
        expect((error as AdminApiError).status).toBe(403);
      },
    });

    const request = http.expectOne("/api/v1/admin/catalog");
    request.flush({ success: false, businessCode: "DB_ADMIN_FORBIDDEN", message: "Denied", data: null, meta: {}, traceId: "trace" }, { status: 403, statusText: "Forbidden" });
  });
});
