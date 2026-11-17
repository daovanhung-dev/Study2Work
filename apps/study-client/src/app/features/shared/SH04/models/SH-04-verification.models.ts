export type VerificationState =
  'missing' | 'pending' | 'accepted' | 'invalid' | 'provider-error' | 'unknown' | 'unmapped';

export interface VerificationRequest {
  user_id: number;
  email: string;
}

export interface VerificationResponse {
  status: string;
  reason?: string;
}

export interface VerificationResult {
  state: VerificationState;
  httpStatus: number | null;
}
