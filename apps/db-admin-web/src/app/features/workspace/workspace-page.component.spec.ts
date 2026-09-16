import { buildObjectSql, quoteSqlIdentifier } from "./workspace-page.component";

describe("workspace SQL helpers", () => {
  it("quotes PostgreSQL identifiers safely", () => {
    expect(quoteSqlIdentifier('user"data')).toBe('"user""data"');
  });

  it("creates a bounded preview query for tables and views", () => {
    expect(buildObjectSql("tables", "public", "events")).toBe('SELECT * FROM "public"."events" LIMIT 100;');
    expect(buildObjectSql("views", "analytics", "recent_users")).toBe('SELECT * FROM "analytics"."recent_users" LIMIT 100;');
  });

  it("only inserts a qualified identifier for routines and other objects", () => {
    expect(buildObjectSql("routines", "public", "rebuild_index")).toBe('"public"."rebuild_index"');
    expect(buildObjectSql("triggers", "public", "audit_insert")).toBe('"public"."audit_insert"');
  });
});
