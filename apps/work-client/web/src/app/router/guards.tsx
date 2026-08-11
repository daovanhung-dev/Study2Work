import { Outlet, useLocation, useParams } from "react-router-dom";

import {
  AccessRequiredPage,
  AccountRestrictedPage,
  ForbiddenPage,
  MfaRequiredPage,
} from "@/pages/StatePages";
import { useSessionStore } from "@/shared/session/store";
import type { TenantType } from "@/shared/session/types";
import { LoadingState } from "@/shared/ui/LoadingState";

export interface AccessRequirement {
  authenticated?: boolean;
  permissions?: string[];
  requireFreshMfa?: boolean;
  requireVerifiedEmail?: boolean;
  roles?: string[];
  tenantType?: TenantType;
}

function normalized(values: string[]): Set<string> {
  return new Set(values.map((value) => value.toUpperCase()));
}

function hasEveryPermission(granted: string[], required: string[]): boolean {
  const grantedPermissions = normalized(granted);
  return required.every((permission) => grantedPermissions.has(permission.toUpperCase()));
}

function hasAnyRole(granted: string[], required: string[]): boolean {
  const grantedRoles = normalized(granted);
  return required.some((role) => grantedRoles.has(role.toUpperCase()));
}

function isFreshMfa(mfaFreshUntil?: string): boolean {
  if (!mfaFreshUntil) {
    return false;
  }

  const expiresAt = Date.parse(mfaFreshUntil);
  return Number.isFinite(expiresAt) && expiresAt > Date.now();
}

function tenantIdFor(
  type: TenantType,
  params: { enterpriseId?: string; universityId?: string },
): string | undefined {
  return type === "ENTERPRISE" ? params.enterpriseId : params.universityId;
}

export function RequireAccess({ requirement }: { requirement: AccessRequirement }) {
  const location = useLocation();
  const params = useParams();
  const session = useSessionStore((state) => state.session);
  const status = useSessionStore((state) => state.status);

  if (status === "checking") {
    return (
      <div className="grid min-h-[65vh] place-items-center px-4 py-12">
        <LoadingState label="Đang kiểm tra phiên làm việc…" />
      </div>
    );
  }

  if (requirement.authenticated && !session) {
    return <AccessRequiredPage returnTo={`${location.pathname}${location.search}`} />;
  }

  if (!session) {
    return <Outlet />;
  }

  const identity = session.identity;
  if (identity.accountStatus !== "ACTIVE") {
    return <AccountRestrictedPage status={identity.accountStatus} />;
  }

  if (requirement.requireVerifiedEmail && !identity.emailVerified) {
    return <ForbiddenPage code="EMAIL_VERIFICATION_REQUIRED" />;
  }

  if (requirement.requireFreshMfa && !isFreshMfa(identity.mfaFreshUntil)) {
    return <MfaRequiredPage />;
  }

  if (requirement.roles && !hasAnyRole(identity.roles, requirement.roles)) {
    return <ForbiddenPage />;
  }

  const tenantId = requirement.tenantType ? tenantIdFor(requirement.tenantType, params) : undefined;
  const membership = requirement.tenantType
    ? identity.memberships.find(
        (item) =>
          item.tenantType === requirement.tenantType &&
          item.tenantId === tenantId &&
          item.status === "ACTIVE",
      )
    : undefined;

  if (requirement.tenantType && !membership) {
    return <ForbiddenPage />;
  }

  if (
    requirement.permissions &&
    !hasEveryPermission([...identity.permissions, ...(membership?.permissions ?? [])], requirement.permissions)
  ) {
    return <ForbiddenPage />;
  }

  return <Outlet />;
}
