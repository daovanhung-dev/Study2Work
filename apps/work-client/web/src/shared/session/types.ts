export type AccountStatus = "ACTIVE" | "DELETION_PENDING" | "SUSPENDED";

export type TenantType = "ENTERPRISE" | "UNIVERSITY";

export interface TenantMembership {
  tenantId: string;
  tenantType: TenantType;
  permissions: string[];
  roleCodes: string[];
  status: "ACTIVE" | "INVITED" | "SUSPENDED" | "REVOKED";
}

export interface SessionIdentity {
  subjectId: string;
  displayName?: string;
  email?: string;
  roles: string[];
  permissions: string[];
  accountStatus: AccountStatus;
  emailVerified: boolean;
  mfaFreshUntil?: string;
  memberships: TenantMembership[];
}

export interface AuthSession {
  accessToken: string;
  expiresAt?: string;
  identity: SessionIdentity;
}

export type SessionStatus = "checking" | "anonymous" | "authenticated";
