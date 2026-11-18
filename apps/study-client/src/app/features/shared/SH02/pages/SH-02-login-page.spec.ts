import { TestBed } from '@angular/core/testing';
import { provideRouter, Router } from '@angular/router';
import { of, Subject, throwError } from 'rxjs';
import { HttpErrorResponse } from '@angular/common/http';
import { describe, expect, it, vi } from 'vitest';

import { AuthSessionService } from '../../../../core/auth/auth-session.service';
import { LoginApi } from '../data-access/SH-02-login.service';
import { LoginPage } from './SH-02-login-page';

describe('SH-02 login page', () => {
  it('saves a valid session and navigates to the student portal once', async () => {
    const pending = new Subject<{ success: boolean; data: { access_token: string } }>();
    const login = vi.fn(() => pending);
    const currentStudent = vi.fn(() => of({ success: true, data: { id: 1 } }));
    const setSession = vi.fn(() => true);
    await TestBed.configureTestingModule({
      imports: [LoginPage],
      providers: [
        provideRouter([]),
        { provide: LoginApi, useValue: { login, currentStudent } },
        { provide: AuthSessionService, useValue: { setSession, role: () => 'STUDENT' } },
      ],
    }).compileComponents();
    const navigate = vi.spyOn(TestBed.inject(Router), 'navigateByUrl').mockResolvedValue(true);
    const fixture = TestBed.createComponent(LoginPage);
    fixture.detectChanges();
    const credentials = { email: ' student@example.com ', password: 'secret' };
    fixture.componentInstance.submit(credentials);
    fixture.componentInstance.submit(credentials);
    expect(login).toHaveBeenCalledOnce();
    expect(login).toHaveBeenCalledWith({ email: 'student@example.com', password: 'secret' });

    pending.next({ success: true, data: { access_token: 'access' } });
    expect(setSession).toHaveBeenCalledWith({ access_token: 'access' });
    expect(currentStudent).toHaveBeenCalledOnce();
    expect(navigate).toHaveBeenCalledWith('/student');
    expect(fixture.componentInstance.submitting()).toBe(false);
  });

  it('maps a 401 response to the credential error', async () => {
    await TestBed.configureTestingModule({
      imports: [LoginPage],
      providers: [
        provideRouter([]),
        { provide: LoginApi, useValue: { login: () => throwError(() => new HttpErrorResponse({ status: 401 })) } },
        { provide: AuthSessionService, useValue: { setSession: vi.fn(), role: () => null } },
      ],
    }).compileComponents();
    const fixture = TestBed.createComponent(LoginPage);
    fixture.detectChanges();
    fixture.componentInstance.submit({ email: 'student@example.com', password: 'wrong' });
    expect(fixture.componentInstance.alert()?.description).toBe('Email hoặc mật khẩu không đúng.');
  });

  it('does not navigate for an invalid response', async () => {
    const setSession = vi.fn();
    await TestBed.configureTestingModule({
      imports: [LoginPage],
      providers: [
        provideRouter([]),
        { provide: LoginApi, useValue: { login: () => of({ success: false, data: null }) } },
        { provide: AuthSessionService, useValue: { setSession, role: () => null } },
      ],
    }).compileComponents();
    const navigate = vi.spyOn(TestBed.inject(Router), 'navigateByUrl');
    const fixture = TestBed.createComponent(LoginPage);
    fixture.detectChanges();
    fixture.componentInstance.submit({ email: 'student@example.com', password: 'secret' });
    expect(setSession).not.toHaveBeenCalled();
    expect(navigate).not.toHaveBeenCalled();
    expect(fixture.componentInstance.alert()?.kind).toBe('error');
  });
});
