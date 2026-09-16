import { TestBed } from "@angular/core/testing";

import { AuthService } from "./auth.service";

describe("AuthService", () => {
  it("does not bypass login in the workspace", () => {
    const service = TestBed.configureTestingModule({ providers: [AuthService] }).inject(AuthService);

    expect(service.isLocalDevAccess).toBeFalse();
    expect(service.can("db_admin:read")).toBeFalse();
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

  it("keeps the local session metadata in memory", () => {
    const service = TestBed.configureTestingModule({ providers: [AuthService] }).inject(AuthService);

    service.setSession({
      accessToken: "header.eyJzdWIiOiJyb290In0.signature",
      user: { id: "root", username: "admin", isRoot: true },
      permissions: ["db_admin:read", "db_admin:manage"],
      roles: ["root"],
      targets: ["study_server", "work_server"],
      schemaBindings: [],
      mustChangePassword: true,
    });

    expect(service.token()).toContain("header.");
    expect(service.isRoot()).toBeTrue();
    expect(service.mustChangePassword()).toBeTrue();
    expect(service.targets()).toEqual(["study_server", "work_server"]);
  });
});
