import { HttpErrorResponse, HttpHeaders } from '@angular/common/http';
import { describe, expect, it } from 'vitest';

import { SH05ErrorContextService } from './sh05-error-context.service';

describe('SH05ErrorContextService', () => {
  const service = new SH05ErrorContextService();

  it('normalizes API #04 authentication errors without claiming the session expired', () => {
    const result = service.normalize(
      errorResponse(401, 'DESIGN_AUTHENTICATION_REQUIRED', 'Authentication required.', {
        traceId: 'trace-401',
      }),
    );

    expect(result).toEqual({
      kind: 'authentication-required',
      status: 401,
      message: 'Authentication required.',
      traceId: 'trace-401',
      traceIdConflict: false,
    });
  });

  it('normalizes role denial and accepts the real response header trace when body trace is absent', () => {
    const result = service.normalize(
      errorResponse(403, 'DESIGN_ACCESS_DENIED', 'Access denied.', {}, 'trace-header'),
    );

    expect(result).toEqual({
      kind: 'access-denied',
      status: 403,
      message: 'Access denied.',
      traceId: 'trace-header',
      traceIdConflict: false,
    });
  });

  it('drops conflicting trace sources instead of choosing one', () => {
    const result = service.normalize(
      errorResponse(
        403,
        'DESIGN_ACCESS_DENIED',
        'Access denied.',
        { traceId: 'trace-body' },
        'trace-header',
      ),
    );

    expect(result?.traceId).toBeNull();
    expect(result?.traceIdConflict).toBe(true);
  });

  it('rejects status/code mismatches, malformed envelopes and service errors', () => {
    expect(
      service.normalize(errorResponse(401, 'DESIGN_ACCESS_DENIED', 'Access denied.')),
    ).toBeNull();
    expect(
      service.normalize(
        errorResponse(403, 'DESIGN_AUTHENTICATION_REQUIRED', 'Authentication required.'),
      ),
    ).toBeNull();
    expect(
      service.normalize(errorResponse(500, 'DESIGN_INTERNAL_ERROR', 'Request failed.')),
    ).toBeNull();
    expect(
      service.normalize(
        new HttpErrorResponse({
          status: 401,
          error: { success: true, businessCode: 'DESIGN_AUTHENTICATION_REQUIRED', message: 'No.' },
        }),
      ),
    ).toBeNull();
    expect(service.normalize(new Error('not an HTTP error'))).toBeNull();
  });

  it('does not copy profile or diagnostic payload fields into presentation state', () => {
    const result = service.normalize(
      errorResponse(403, 'DESIGN_ACCESS_DENIED', 'Access denied.', {
        data: { email: 'private@example.test', profile: 'private-profile' },
        stack: 'private-stack',
        reason: 'internal-role-detail',
      }),
    );

    expect(result).toEqual({
      kind: 'access-denied',
      status: 403,
      message: 'Access denied.',
      traceId: null,
      traceIdConflict: false,
    });
    expect(JSON.stringify(result)).not.toContain('private');
    expect(JSON.stringify(result)).not.toContain('internal-role-detail');
  });
});

function errorResponse(
  status: number,
  businessCode: string,
  message: string,
  extra: Record<string, unknown> = {},
  headerTraceId?: string,
): HttpErrorResponse {
  const headers = headerTraceId
    ? new HttpHeaders({ 'X-Trace-Id': headerTraceId })
    : new HttpHeaders();
  return new HttpErrorResponse({
    status,
    headers,
    error: {
      success: false,
      businessCode,
      message,
      data: null,
      meta: {},
      ...extra,
    },
  });
}
