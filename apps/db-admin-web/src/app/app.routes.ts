import { Routes } from "@angular/router";

import { authGuard, permissionGuard } from "./core/auth.guard";
import { ShellComponent } from "./core/shell.component";
import { LoginPageComponent } from "./features/login/login-page.component";
import { WorkspacePageComponent } from "./features/workspace/workspace-page.component";

export const appRoutes: Routes = [
  { path: "login", component: LoginPageComponent },
  {
    path: "",
    component: ShellComponent,
    canActivate: [authGuard],
    children: [
      { path: "", pathMatch: "full", component: WorkspacePageComponent, canActivate: [permissionGuard("db_admin:read")] },
    ],
  },
  { path: "**", redirectTo: "" },
];
