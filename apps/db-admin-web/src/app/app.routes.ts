import { Routes } from "@angular/router";

import { authGuard, permissionGuard } from "./core/auth.guard";
import { ShellComponent } from "./core/shell.component";
import { AuditPageComponent } from "./features/audit/audit-page.component";
import { CatalogPageComponent } from "./features/catalog/catalog-page.component";
import { DashboardPageComponent } from "./features/dashboard/dashboard-page.component";
import { LoginPageComponent } from "./features/login/login-page.component";
import { SqlEditorPageComponent } from "./features/sql-editor/sql-editor-page.component";
import { TablePageComponent } from "./features/table/table-page.component";

export const appRoutes: Routes = [
  { path: "login", component: LoginPageComponent },
  {
    path: "",
    component: ShellComponent,
    canActivate: [authGuard],
    children: [
      { path: "", pathMatch: "full", redirectTo: "dashboard" },
      { path: "dashboard", component: DashboardPageComponent, canActivate: [permissionGuard("db_admin:read")] },
      { path: "catalog", component: CatalogPageComponent, canActivate: [permissionGuard("db_admin:read")] },
      { path: "tables/:schema/:table", component: TablePageComponent, canActivate: [permissionGuard("db_admin:read")] },
      { path: "sql", component: SqlEditorPageComponent, canActivate: [permissionGuard("db_admin:sql")] },
      { path: "audit", component: AuditPageComponent, canActivate: [permissionGuard("db_admin:read")] },
    ],
  },
  { path: "**", redirectTo: "dashboard" },
];
