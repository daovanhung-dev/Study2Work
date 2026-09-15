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

  it("unwraps the repository response envelope", () => {
    api.getConnection().subscribe((value) => expect(value.database).toBe("study"));

    const request = http.expectOne("/api/v1/admin/connection");
    request.flush({ success: true, businessCode: "DB_ADMIN_CONNECTION_READY", message: "ok", data: { database: "study" }, meta: {}, traceId: "trace" });
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
