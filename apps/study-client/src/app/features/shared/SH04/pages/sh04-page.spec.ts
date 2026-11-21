import { HttpResponse } from '@angular/common/http';
import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { of } from 'rxjs';
import { describe, expect, it, vi } from 'vitest';

import { SH04RegistrationHandoffService } from '../data-access/sh04-registration-handoff.service';
import { SH04VerificationService } from '../data-access/sh04-verification.service';
import { SH04Page } from './sh04-page';

describe('SH04Page', () => {
  it('explains the unavailable verification flow when registration handoff is missing', async () => {
    const fixture = await createPage(null, vi.fn());
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.querySelector('[data-screen-id="SH-04"]')).not.toBeNull();
    expect(root.querySelector('h1')?.textContent?.trim()).toBe('Chưa thể gửi yêu cầu xác minh');
    expect(root.querySelector('[role="status"]')?.textContent).toContain('Chưa có yêu cầu nào được gửi');
    expect(root.textContent).toContain('Gửi thư thật');
    expect(root.textContent).toContain('Chưa được xác nhận');
    expect(root.querySelector('input, form, button')).toBeNull();
    expect(root.querySelector('a[href="/login"]')?.textContent).toContain('Quay lại đăng nhập');
  });

  it('calls API #02 only after an explicit click and reports accepted without claiming delivery', async () => {
    const sendRequest = vi.fn(() => of(new HttpResponse({
      status: 202,
      body: {
        success: true,
        businessCode: 'DESIGN_OPERATION_ACCEPTED',
        message: 'Email verification request accepted.',
        data: { status: 'accepted' },
        meta: {},
        traceId: 'trace-test',
      },
    })));
    const fixture = await createPage({ userId: 73, email: 'student@example.test' }, sendRequest);
    fixture.detectChanges();
    expect(sendRequest).not.toHaveBeenCalled();

    (fixture.nativeElement as HTMLElement).querySelector<HTMLButtonElement>('.verification-action')!.click();
    fixture.detectChanges();

    expect(sendRequest).toHaveBeenCalledTimes(1);
    expect(sendRequest).toHaveBeenCalledWith(73, 'student@example.test');
    const root = fixture.nativeElement as HTMLElement;
    expect(root.textContent).toContain('đã được API #02 chấp nhận');
    expect(root.textContent).toContain('Email chưa được gửi thật');
    expect(root.textContent).toContain('địa chỉ chưa được xác minh');
  });

  it('does not treat an unrecognized provider status as successful delivery or retry automatically', async () => {
    const sendRequest = vi.fn(() => of(new HttpResponse({
      status: 202,
      body: {
        success: true,
        businessCode: 'DESIGN_OPERATION_ACCEPTED',
        message: 'accepted',
        data: { status: 'queued' },
        meta: {},
        traceId: 'trace-test',
      },
    })));
    const fixture = await createPage({ userId: 73, email: 'student@example.test' }, sendRequest);
    fixture.detectChanges();
    (fixture.nativeElement as HTMLElement).querySelector<HTMLButtonElement>('.verification-action')!.click();
    fixture.detectChanges();

    expect(sendRequest).toHaveBeenCalledTimes(1);
    expect((fixture.nativeElement as HTMLElement).textContent).toContain('Trạng thái chưa ánh xạ');
  });
});

async function createPage(
  handoff: { userId: number; email: string } | null,
  sendRequest: ReturnType<typeof vi.fn>,
) {
  await TestBed.configureTestingModule({
    imports: [SH04Page],
    providers: [
      provideRouter([]),
      { provide: SH04RegistrationHandoffService, useValue: { consume: () => handoff } },
      { provide: SH04VerificationService, useValue: { sendRequest } },
    ],
  }).compileComponents();
  return TestBed.createComponent(SH04Page);
}
