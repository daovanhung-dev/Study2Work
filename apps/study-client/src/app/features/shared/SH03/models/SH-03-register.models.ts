export interface RegistrationInput {
  fullName: string;
  email: string;
  password: string;
}

export interface RegistrationRequest {
  full_name: string;
  email: string;
  password: string;
}

export interface CreatedUser {
  id: number;
  email: string;
}

export type RegistrationField = 'fullName' | 'email' | 'password';

export interface RegistrationFieldErrors {
  fullName?: string;
  email?: string;
  password?: string;
}

export interface RegistrationAlert {
  title: string;
  description: string;
  kind: 'error' | 'warning' | 'success';
}
