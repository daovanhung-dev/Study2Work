export interface LoginCredentials {
  email: string;
  password: string;
}

export interface LoginAlert {
  title: string;
  description: string;
  kind: 'error' | 'info';
}

export interface LoginFieldErrors {
  email?: string;
  password?: string;
}
