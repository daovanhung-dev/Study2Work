import { TestBed } from '@angular/core/testing';

import { SH02Page } from './sh02-page';

describe('SH02Page', () => {
  beforeEach(async () => {
    await TestBed.configureTestingModule({ imports: [SH02Page] }).compileComponents();
  });

  it('renders the labeled required fields with login available', () => {
    const fixture = TestBed.createComponent(SH02Page);
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    const email = root.querySelector<HTMLInputElement>('#login-email');
    const password = root.querySelector<HTMLInputElement>('#login-password');
    const submit = root.querySelector<HTMLButtonElement>('.submit-button');

    expect(root.querySelector('h1')?.textContent?.trim()).toBe('Đăng nhập');
    expect(email?.required).toBe(true);
    expect(email?.type).toBe('email');
    expect(password?.required).toBe(true);
    expect(password?.type).toBe('password');
    expect(submit?.disabled).toBe(false);
  });

  it('toggles password visibility without changing its value', () => {
    const fixture = TestBed.createComponent(SH02Page);
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    const password = root.querySelector<HTMLInputElement>('#login-password')!;
    const toggle = root.querySelector<HTMLButtonElement>('.password-toggle')!;
    password.value = 'unchanged-secret';

    toggle.click();
    fixture.detectChanges();

    expect(password.type).toBe('text');
    expect(password.value).toBe('unchanged-secret');
    expect(toggle.getAttribute('aria-pressed')).toBe('true');
    expect(toggle.getAttribute('aria-label')).toBe('Ẩn mật khẩu');

    toggle.click();
    fixture.detectChanges();

    expect(password.type).toBe('password');
    expect(password.value).toBe('unchanged-secret');
    expect(toggle.getAttribute('aria-pressed')).toBe('false');
  });

  it('prevents native form submission from sending credentials in the URL', () => {
    const fixture = TestBed.createComponent(SH02Page);
    fixture.detectChanges();

    const form = fixture.nativeElement.querySelector('form') as HTMLFormElement;
    const submitEvent = new Event('submit', { bubbles: true, cancelable: true });
    form.dispatchEvent(submitEvent);

    expect(submitEvent.defaultPrevented).toBe(true);
  });
});
