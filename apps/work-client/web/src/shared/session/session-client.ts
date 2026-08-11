import axios from "axios";

import { isSuccessEnvelope, parseApiEnvelope } from "../api/envelope";
import { identityApiBaseUrl } from "../api/runtime";
import type { AuthSession, SessionIdentity, TenantMembership, TenantType } from "./types";

interface RefreshPayload {
  accessToken: string;
  expiresAt?: string;
}

function asRecord(value: unknown): Record<string, unknown> | undefined {
  return typeof value === "object" && value !== null && !Array.isArray(value)
    ? (value as Record<string, unknown>)
    : undefined;
}

function asString(value: unknown): string | undefined {
  return typeof value === "string" && value.trim() ? value : undefined;
}

function asStringArray(value: unknown): string[] {
  return Array.isArray(value) ? value.filter((item): item is string => typeof item === "string") : [];
}

function mapMembership(value: unknown): TenantMembership | undefined {
  const source = asRecord(value);
  const tenantId = asString(source?.tenantId);
  const tenantType = asString(source?.tenantType);

  if (!tenantId || (tenantType !== "ENTERPRISE" && tenantType !== "UNIVERSITY")) {
    return undefined;
  }

  return {
    tenantId,
    tenantType: tenantType as TenantType,
    permissions: asStringArray(source?.permissions),
    roleCodes: asStringArray(source?.roleCodes),
    status: toMembershipStatus(asString(source?.status)),
  };
}

function toMembershipStatus(value: string | undefined): TenantMembership["status"] {
  return value === "INVITED" || value === "SUSPENDED" || value === "REVOKED" ? value : "ACTIVE";
}

function mapIdentity(value: unknown): SessionIdentity | undefined {
  const source = asRecord(value);
  const subjectId = asString(source?.subjectId) ?? asString(source?.userId) ?? asString(source?.id);

  if (!subjectId) {
    return undefined;
  }

  const accountStatus = asString(source?.accountStatus);
  const membershipValues = source?.memberships;
  const memberships = Array.isArray(membershipValues)
    ? membershipValues
        .map(mapMembership)
        .filter((membership): membership is TenantMembership => Boolean(membership))
    : [];

  return {
    subjectId,
    displayName: asString(source?.displayName) ?? asString(source?.name),
    email: asString(source?.email),
    roles: asStringArray(source?.roles),
    permissions: asStringArray(source?.permissions),
    accountStatus:
      accountStatus === "SUSPENDED" || accountStatus === "DELETION_PENDING" ? accountStatus : "ACTIVE",
    emailVerified: source?.emailVerified === true,
    mfaFreshUntil: asString(source?.mfaFreshUntil),
    memberships,
  };
}

function mapRefreshPayload(value: unknown): RefreshPayload | undefined {
  const source = asRecord(value);
  const accessToken = asString(source?.accessToken);

  return accessToken
    ? {
        accessToken,
        expiresAt: asString(source?.expiresAt),
      }
    : undefined;
}

/**
 * Restores only the short-lived access token held by the app. The rotating refresh token remains
 * in the Identity service's HttpOnly cookie and is never written to browser storage.
 */
let restoreInFlight: Promise<AuthSession | null> | undefined;

async function requestSessionRestore(): Promise<AuthSession | null> {
  if (!identityApiBaseUrl) {
    return null;
  }

  try {
    const refreshResponse = await axios.post<unknown>(
      `${identityApiBaseUrl}/auth/refresh`,
      undefined,
      {
        timeout: 10_000,
        withCredentials: true,
        headers: { Accept: "application/json" },
      },
    );
    const refreshEnvelope = parseApiEnvelope<unknown>(refreshResponse.data);

    if (!isSuccessEnvelope(refreshEnvelope)) {
      return null;
    }

    const refresh = mapRefreshPayload(refreshEnvelope.data);
    if (!refresh) {
      return null;
    }

    const meResponse = await axios.get<unknown>(`${identityApiBaseUrl}/me`, {
      timeout: 10_000,
      withCredentials: true,
      headers: {
        Accept: "application/json",
        Authorization: `Bearer ${refresh.accessToken}`,
      },
    });
    const meEnvelope = parseApiEnvelope<unknown>(meResponse.data);

    if (!isSuccessEnvelope(meEnvelope)) {
      return null;
    }

    const identity = mapIdentity(meEnvelope.data);
    return identity ? { ...refresh, identity } : null;
  } catch {
    return null;
  }
}

export function restoreWorkSession(): Promise<AuthSession | null> {
  if (!restoreInFlight) {
    restoreInFlight = requestSessionRestore().finally(() => {
      restoreInFlight = undefined;
    });
  }

  return restoreInFlight;
}
