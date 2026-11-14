import type {
  RegistrationFieldErrors,
  RegistrationInput,
  RegistrationRequest,
} from '../models/SH-03-register.models';

export function validateRegistration(input: RegistrationInput): {
  request: RegistrationRequest;
  errors: RegistrationFieldErrors;
} {
  const fullName = input.fullName.trim();
  const email = input.email.trim();
  const errors: RegistrationFieldErrors = {};

  if (!fullName) {
    errors.fullName = 'Vui lòng nhập họ và tên.';
  } else if (fullName.length > 150) {
    errors.fullName = 'Họ và tên không được vượt quá 150 ký tự.';
  }

  if (!email || email.length > 255 || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    errors.email = 'Địa chỉ email không hợp lệ.';
  }

  if (!input.password.trim()) {
    errors.password = 'Vui lòng nhập mật khẩu.';
  }

  return {
    request: { full_name: fullName, email, password: input.password },
    errors,
  };
}
