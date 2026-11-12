import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { RouterTestingHarness } from '@angular/router/testing';
import { beforeEach, describe, expect, it } from 'vitest';

import { App } from './app';
import { routes } from './app.routes';
import { AD01Page } from './features/admin/AD01/pages/ad01-page';
import { SystemReadinessPage } from './features/system/pages/system-readiness-page';
import { AdminLayout } from './layouts/admin/admin-layout';
import { SystemLayout } from './layouts/system/system-layout';

describe('Study app routes', () => {
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [App],
      providers: [provideRouter(routes)],
    }).compileComponents();
  });

  it('renders the readiness scaffold at the root route', async () => {
    const harness = await RouterTestingHarness.create();

    await harness.navigateByUrl('/', SystemLayout);

    expect(harness.routeNativeElement?.textContent).toContain('Khung ứng dụng đã sẵn sàng');
  });

  it('renders AD-01 at /admin without the root scaffold', async () => {
    const harness = await RouterTestingHarness.create();

    await harness.navigateByUrl('/admin', AdminLayout);

    const routedText = harness.routeNativeElement?.textContent ?? '';
    expect(routedText).toContain('Bảng điều khiển quản trị hệ thống');
    expect(routedText).not.toContain('Khung ứng dụng đã sẵn sàng');
  });

  it('renders AD-02 at /admin/users and marks its navigation link current', async () => {
    const harness = await RouterTestingHarness.create();

    await harness.navigateByUrl('/admin/users', AdminLayout);

    const routedRoot = harness.routeNativeElement as HTMLElement;
    expect(routedRoot.querySelector('h1')?.textContent).toContain('Danh sách người dùng');
    expect(routedRoot.querySelector('a[routerLink="/admin/users"]')?.getAttribute('aria-current')).toBe(
      'page',
    );
    expect(routedRoot.querySelector('a[routerLink="/admin"]')?.getAttribute('aria-current')).toBeNull();
    expect(routedRoot.querySelectorAll('tbody .user-record')).toHaveLength(0);
  });

  it('keeps the root component as a router outlet only', () => {
    const fixture = TestBed.createComponent(App);
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.querySelector('router-outlet')).not.toBeNull();
    expect(root.textContent).not.toContain('Khung ứng dụng đã sẵn sàng');
  });
});
