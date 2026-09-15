import { TestBed } from "@angular/core/testing";

import { AuthService } from "./auth.service";

describe("AuthService", () => {
  it("keeps local development access in memory", () => {
    const service = TestBed.configureTestingModule({ providers: [AuthService] }).inject(AuthService);

    expect(service.isLocalDevAccess).toBeTrue();
    expect(service.can("db_admin:read")).toBeTrue();
    expect(service.token()).toBeNull();
  });

  it("maps DB_ADMIN role claims to all admin permissions", () => {
    const service = TestBed.configureTestingModule({ providers: [AuthService] }).inject(AuthService);
    const header = btoa(JSON.stringify({ alg: "none", typ: "JWT" }));
    const payload = btoa(JSON.stringify({ sub: "admin", roles: ["DB_ADMIN"] }));

    service.setToken(`${header}.${payload}.signature`);

    expect(service.can("db_admin:read")).toBeTrue();
    expect(service.can("db_admin:write")).toBeTrue();
    expect(service.can("db_admin:sql")).toBeTrue();
  });
});
