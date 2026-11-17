import { TestBed } from '@angular/core/testing';
import { of, Subject, throwError } from 'rxjs';
import { HttpErrorResponse } from '@angular/common/http';
import { describe, expect, it, vi } from 'vitest';

import { LoginApi } from '../data-access/SH-02-login.service';
import { LoginPage } from './SH-02-login-page';

describe('SH-02 login page', () => {
  it('sends only one request while pending and does not open an unapproved session', async () => {
    const pending = new Subject<{ success: boolean; data: { id: number } }>();
    const login = vi.fn(() => pending);
    await TestBed.configureTestingModule({
      imports: [LoginPage],
      providers: [{ provide: LoginApi, useValue: { login } }],
    }).compileComponents();

    const fixture = TestBed.createComponent(LoginPage);
    fixture.detectChanges();
    const credentials = { email: 'student@example.com', password: 'secret' };
    fixture.componentInstance.submit(credentials);
    fixture.componentInstance.submit(credentials);
    expect(login).toHaveBeenCalledOnce();

    pending.next({ success: true, data: { id: 1 } });
    expect(fixture.componentInstance.submitting()).toBe(false);
    expect(fixture.componentInstance.alert()?.kind).toBe('info');
  });

  it('maps a 401 response to the generic credential error', async () => {
    await TestBed.configureTestingModule({
      imports: [LoginPage],
      providers: [
        { provide: LoginApi, useValue: { login: () => throwError(() => new HttpErrorResponse({ status: 401 })) } },
      ],
    }).compileComponents();
    const fixture = TestBed.createComponent(LoginPage);
    fixture.detectChanges();
    fixture.componentInstance.submit({ email: 'student@example.com', password: 'wrong' });

    expect(fixture.componentInstance.alert()?.description).toBe('Email hoặc mật khẩu không đúng.');
  });

  it('trims the email and does not open a session for an invalid response', async () => {
    const login = vi.fn(() => of({ success: false, data: null }));
    await TestBed.configureTestingModule({
      imports: [LoginPage],
      providers: [{ provide: LoginApi, useValue: { login } }],
    }).compileComponents();

    const fixture = TestBed.createComponent(LoginPage);
    fixture.detectChanges();
    fixture.componentInstance.submit({ email: '  student@example.com  ', password: 'secret' });

    expect(login).toHaveBeenCalledWith({ email: 'student@example.com', password: 'secret' });
    expect(fixture.componentInstance.submitting()).toBe(false);
    expect(fixture.componentInstance.alert()?.kind).toBe('error');
  });
});
