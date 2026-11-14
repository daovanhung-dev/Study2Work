import {
  ChangeDetectionStrategy,
  Component,
  ElementRef,
  EventEmitter,
  Input,
  Output,
  ViewChild,
} from '@angular/core';
import { FormsModule } from '@angular/forms';

import type { LoginAlert, LoginCredentials, LoginFieldErrors } from '../models/SH-02-login.models';

@Component({
  selector: 'study-login-view',
  imports: [FormsModule],
  templateUrl: './SH-02-login-view.html',
  styleUrl: './SH-02-login-view.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class LoginView {
  @Input() submitting = false;
  @Input() alert: LoginAlert | null = null;
  @Input() fieldErrors: LoginFieldErrors = {};
  @Output() readonly login = new EventEmitter<LoginCredentials>();
  @Output() readonly edit = new EventEmitter<void>();

  @ViewChild('emailInput') private emailInput?: ElementRef<HTMLInputElement>;
  @ViewChild('passwordInput') private passwordInput?: ElementRef<HTMLInputElement>;

  email = '';
  password = '';
  passwordVisible = false;

  submit(): void {
    if (this.submitting) return;
    this.login.emit({ email: this.email, password: this.password });
  }

  focusField(field: 'email' | 'password'): void {
    (field === 'email' ? this.emailInput : this.passwordInput)?.nativeElement.focus();
  }
}
