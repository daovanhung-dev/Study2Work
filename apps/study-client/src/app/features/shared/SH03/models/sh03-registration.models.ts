export interface SH03RegistrationRequest {
  email: string;
  password: string;
  full_name: string;
}

export interface SH03RegistrationResult {
  id: number;
  email: string;
}

export type SH03RegistrationField = 'fullName' | 'email' | 'password';

export type SH03RegistrationFieldErrors = Partial<
  Record<SH03RegistrationField, string>
>;
