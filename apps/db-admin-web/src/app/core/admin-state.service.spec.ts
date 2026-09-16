import { of } from "rxjs";

import { AdminStateService } from "./admin-state.service";
import { ApiService } from "./api.service";

describe("AdminStateService", () => {
  let api: jasmine.SpyObj<ApiService>;
  let state: AdminStateService;
  const catalog = {
    schemas: [{ name: "public" }],
    tables: [],
    views: [],
    routines: [],
    triggers: [],
    types: [],
    sequences: [],
    indexes: [],
    constraints: [],
    grants: [],
  };

  beforeEach(() => {
    api = jasmine.createSpyObj<ApiService>("ApiService", ["getDatabases", "getCatalog"]);
    api.getDatabases.and.returnValue(of({ databases: [{ id: "work_server", label: "Work Server" }] }));
    api.getCatalog.and.returnValue(of(catalog));
    state = new AdminStateService(api);
  });

  it("starts without a selected database, schema, or catalog", () => {
    expect(state.selectedDatabase()).toBeNull();
    expect(state.selectedSchema()).toBeNull();
    expect(state.catalog()).toBeNull();
  });

  it("loads the selected database and clears the previous schema/catalog", () => {
    state.selectSchema("public");
    state.selectDatabase("work_server");

    expect(api.getCatalog).toHaveBeenCalledWith("work_server");
    expect(state.selectedDatabase()).toBe("work_server");
    expect(state.selectedSchema()).toBeNull();
    expect(state.catalog()).toEqual(catalog);
  });

  it("clears catalog state when the database selection is cleared", () => {
    state.selectDatabase("work_server");
    state.selectSchema("public");
    state.selectDatabase(null);

    expect(state.selectedDatabase()).toBeNull();
    expect(state.selectedSchema()).toBeNull();
    expect(state.catalog()).toBeNull();
    expect(state.loading()).toBeFalse();
  });
});
