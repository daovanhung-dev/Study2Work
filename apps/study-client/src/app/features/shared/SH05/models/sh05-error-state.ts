export type SH05ErrorState =
  | {
      kind: 'authentication-required';
      status: 401;
      message: string;
      traceId: string | null;
      traceIdConflict: boolean;
    }
  | {
      kind: 'access-denied';
      status: 403;
      message: string;
      traceId: string | null;
      traceIdConflict: boolean;
    };
