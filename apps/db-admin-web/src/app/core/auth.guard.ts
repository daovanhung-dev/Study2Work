import { CanActivateFn, Router } from "@angular/router";
import { inject } from "@angular/core";

import { AuthService } from "./auth.service";
import { Permission } from "./models";

export const authGuard: CanActivateFn = () => {
  const auth = inject(AuthService);
  return auth.isLocalDevAccess || auth.token() ? true : inject(Router).parseUrl("/login");
};

export const permissionGuard = (permission: Permission): CanActivateFn => () => {
  const auth = inject(AuthService);
  if (auth.can(permission)) return true;
  return inject(Router).parseUrl(auth.can("db_admin:read") ? "/dashboard" : "/login");
};
