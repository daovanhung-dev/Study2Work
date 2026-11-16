import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { afterEach, beforeEach, describe, expect, it } from 'vitest';

import { AD20Page } from './ad20-page';

describe('AD20Page', () => {
  let http: HttpTestingController;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AD20Page],
      providers: [provideHttpClient(), provideHttpClientTesting(), provideRouter([])],
    }).compileComponents();
    http = TestBed.inject(HttpTestingController);
  });

  afterEach(() => http.verify());

  it('updates the local preview as title and content are edited', () => {
    const fixture = TestBed.createComponent(AD20Page);
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    const title = root.querySelector<HTMLInputElement>('#notice-title');
    const content = root.querySelector<HTMLTextAreaElement>('#notice-content');
    expect(title).not.toBeNull();
    expect(content).not.toBeNull();

    title!.value = 'Bảo trì hệ thống';
    title!.dispatchEvent(new Event('input'));
    content!.value = 'Dịch vụ sẽ tạm dừng vào 22:00.';
    content!.dispatchEvent(new Event('input'));
    fixture.detectChanges();

    expect(root.querySelector('.notification-preview h3')?.textContent).toContain('Bảo trì hệ thống');
    expect(root.querySelector('.preview-content')?.textContent).toContain('Dịch vụ sẽ tạm dừng vào 22:00.');
    http.expectNone((request) => request.url === '/api/v1/admin/notifications');
  });

  it('keeps audience, channels, priority, draft and send unavailable without calling #93', () => {
    const fixture = TestBed.createComponent(AD20Page);
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.querySelector<HTMLTextAreaElement>('#recipient-ids')?.matches(':disabled')).toBe(true);
    expect([...root.querySelectorAll<HTMLInputElement>('.channel-options input, .priority-options input')]
      .every((input) => input.matches(':disabled'))).toBe(true);
    const actions = root.querySelectorAll<HTMLButtonElement>('.compose-action button');
    expect(actions).toHaveLength(2);
    expect([...actions].every((button) => button.disabled)).toBe(true);
    expect(root.textContent).toContain('Local API #93 ghi notification và delivery row ở trạng thái QUEUED rồi trả 202');
    expect(root.textContent).toContain('API #18 hiện không có local route');
    expect(root.querySelector('a[href="/admin/notifications"]')).not.toBeNull();
    http.expectNone((request) => request.url === '/api/v1/admin/notifications');
  });
});
