export interface SH04RegistrationHandoff {
  readonly userId: number;
  readonly email: string;
}

export type SH04VerificationScreenState =
  | { readonly status: 'missing-handoff' }
  | { readonly status: 'ready'; readonly email: string }
  | { readonly status: 'submitting'; readonly email: string }
  | { readonly status: 'accepted'; readonly email: string }
  | { readonly status: 'provider-status-unknown'; readonly email: string }
  | { readonly status: 'invalid-request' }
  | { readonly status: 'request-error' }
  | { readonly status: 'outcome-unknown' };
