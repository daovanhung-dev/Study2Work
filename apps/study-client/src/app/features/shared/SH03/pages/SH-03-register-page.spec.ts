import { TestBed } from '@angular/core/testing';
import { Router } from '@angular/router';
import { HttpErrorResponse } from '@angular/common/http';
import { of, throwError } from 'rxjs';
import { describe, expect, it, vi } from 'vitest';

import { RegisterApi } from '../data-access/SH-03-register.service';
import { VerificationHandoffStore } from '../../verification-handoff';
import { RegisterPage } from './SH-03-register-page';

describe('SH-03 register page', () => {
  it('hands a verified 201 response to SH-04 exactly once', async () => {
    const register = vi.fn(() =>
      of({
        status: 201,
        body: {
          success: true,
          businessCode: 'DESIGN_RESOURCE_CREATED',
          data: { id: 42, email: 'student@example.com' },
        },
      }),
    );
    const navigateByUrl = vi.fn(() => Promise.resolve(true));
    const set = vi.fn();
    await TestBed.configureTestingModule({
      imports: [RegisterPage],
      providers: [
        { provide: RegisterApi, useValue: { register } },
        { provide: Router, useValue: { navigateByUrl } },
        { provide: VerificationHandoffStore, useValue: { set } },
      ],
    }).compileComponents();
    const fixture = TestBed.createComponent(RegisterPage);
    fixture.detectChanges();
    const input = { fullName: '  Mai Nguyen  ', email: '  student@example.com  ', password: 'secret' };
    fixture.componentInstance.submit(input);
    fixture.componentInstance.submit(input);

    expect(register).toHaveBeenCalledOnce();
    expect(register).toHaveBeenCalledWith({ full_name: 'Mai Nguyen', email: 'student@example.com', password: 'secret' });
    expect(set).toHaveBeenCalledWith({ userId: 42, email: 'student@example.com' });
    expect(navigateByUrl).toHaveBeenCalledWith('/register/verification');
  });

  it('keeps a duplicate-email conflict on the form', async () => {
    const register = vi.fn(() =>
      throwError(() => new HttpErrorResponse({ status: 409, error: { businessCode: 'DESIGN_STATE_CONFLICT' } })),
    );
    await TestBed.configureTestingModule({
      imports: [RegisterPage],
      providers: [
        { provide: RegisterApi, useValue: { register } },
        { provide: Router, useValue: { navigateByUrl: vi.fn() } },
      ],
    }).compileComponents();
    const fixture = TestBed.createComponent(RegisterPage);
    fixture.detectChanges();
    fixture.componentInstance.submit({ fullName: 'Mai Nguyen', email: 'student@example.com', password: 'secret' });

    expect(fixture.componentInstance.created()).toBe(false);
    expect(fixture.componentInstance.fieldErrors().email).toBe('Email đã tồn tại.');
  });

  it('blocks invalid input before an API request or navigation', async () => {
    const register = vi.fn();
    const navigateByUrl = vi.fn();
    await TestBed.configureTestingModule({
      imports: [RegisterPage],
      providers: [
        { provide: RegisterApi, useValue: { register } },
        { provide: Router, useValue: { navigateByUrl } },
      ],
    }).compileComponents();

    const fixture = TestBed.createComponent(RegisterPage);
    fixture.detectChanges();
    fixture.componentInstance.submit({ fullName: '', email: 'bad', password: '' });

    expect(register).not.toHaveBeenCalled();
    expect(navigateByUrl).not.toHaveBeenCalled();
    expect(fixture.componentInstance.fieldErrors().email).toBeTruthy();
  });
});
