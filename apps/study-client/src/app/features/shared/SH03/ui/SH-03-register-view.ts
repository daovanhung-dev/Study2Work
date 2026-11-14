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

import type {
  RegistrationAlert,
  RegistrationField,
  RegistrationFieldErrors,
  RegistrationInput,
} from '../models/SH-03-register.models';

@Component({
  selector: 'study-register-view',
  imports: [FormsModule],
  templateUrl: './SH-03-register-view.html',
  styleUrl: './SH-03-register-view.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class RegisterView {
  @Input() submitting = false;
  @Input() created = false;
  @Input() alert: RegistrationAlert | null = null;
  @Input() fieldErrors: RegistrationFieldErrors = {};
  @Output() readonly register = new EventEmitter<RegistrationInput>();
  @Output() readonly edit = new EventEmitter<RegistrationField>();

  @ViewChild('fullNameInput') private fullNameInput?: ElementRef<HTMLInputElement>;
  @ViewChild('emailInput') private emailInput?: ElementRef<HTMLInputElement>;
  @ViewChild('passwordInput') private passwordInput?: ElementRef<HTMLInputElement>;

  fullName = '';
  email = '';
  password = '';

  submit(): void {
    if (this.submitting || this.created) return;
    this.register.emit({
      fullName: this.fullName,
      email: this.email,
      password: this.password,
    });
  }

  focusField(field: RegistrationField): void {
    const input =
      field === 'fullName'
        ? this.fullNameInput
        : field === 'email'
          ? this.emailInput
          : this.passwordInput;
    input?.nativeElement.focus();
  }
}
