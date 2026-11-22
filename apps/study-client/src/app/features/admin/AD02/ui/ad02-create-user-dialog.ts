import { Component, ElementRef, EventEmitter, Input, Output, ViewChild } from '@angular/core';

import type { AdminCreateUserRequest, AdminUserRole } from '../../admin-api.models';

interface CreateUserForm {
  full_name: string;
  email: string;
  password: string;
  role: AdminUserRole | '';
}

@Component({
  selector: 'study-ad02-create-user-dialog',
  styleUrl: './ad02-create-user-dialog.css',
  templateUrl: './ad02-create-user-dialog.html',
})
export class AD02CreateUserDialog {
  @Input() pending = false;
  @Input() errorMessage = '';
  @Output() readonly submitted = new EventEmitter<AdminCreateUserRequest>();
  @Output() readonly dismissed = new EventEmitter<void>();
  @Output() readonly edited = new EventEmitter<void>();
  @ViewChild('dialog') private dialog?: ElementRef<HTMLDialogElement>;
  @ViewChild('formElement') private formElement?: ElementRef<HTMLFormElement>;

  readonly roles: ReadonlyArray<{ value: AdminUserRole; label: string }> = [
    { value: 'STUDENT', label: 'Học viên' },
    { value: 'MENTOR', label: 'Giảng viên' },
    { value: 'ADMIN', label: 'Quản trị viên' },
  ];
  form: CreateUserForm = this.emptyForm();
  passwordError = '';

  ngAfterViewInit(): void {
    const dialog = this.dialog?.nativeElement;
    if (!dialog) return;
    if (typeof dialog.showModal === 'function') {
      dialog.showModal();
    } else {
      dialog.setAttribute('open', '');
    }
  }

  submitForm(event: Event): void {
    event.preventDefault();
    if (this.pending) return;
    const formElement = this.formElement?.nativeElement;
    if (formElement && !formElement.checkValidity()) {
      formElement.reportValidity();
      return;
    }
    if (!this.form.password.trim()) {
      this.passwordError = 'Mật khẩu không được để trống.';
      return;
    }
    if (!this.form.role) return;

    this.passwordError = '';
    this.submitted.emit({
      full_name: this.form.full_name,
      email: this.form.email,
      password: this.form.password,
      role: this.form.role,
    });
  }

  closeDialog(): void {
    if (this.pending) return;
    const dialog = this.dialog?.nativeElement;
    if (dialog?.open && typeof dialog.close === 'function') {
      dialog.close();
    } else {
      dialog?.removeAttribute('open');
      this.dismissed.emit();
    }
  }

  handleCancel(event: Event): void {
    if (this.pending) event.preventDefault();
  }

  handleClosed(): void {
    if (!this.pending) this.dismissed.emit();
  }

  updateTextField(field: 'full_name' | 'email', value: string): void {
    this.form[field] = value;
    this.edited.emit();
  }

  updatePassword(value: string): void {
    this.form.password = value;
    this.passwordError = '';
    this.edited.emit();
  }

  updateRole(value: string): void {
    this.form.role = this.roles.find((role) => role.value === value)?.value ?? '';
    this.edited.emit();
  }

  private emptyForm(): CreateUserForm {
    return { full_name: '', email: '', password: '', role: '' };
  }
}
