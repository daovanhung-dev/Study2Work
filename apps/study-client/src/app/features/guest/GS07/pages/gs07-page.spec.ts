import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { RouterTestingHarness } from '@angular/router/testing';
import { afterEach, beforeEach, describe, expect, it } from 'vitest';

import type { ApiEnvelope } from '../../../../core/http/api-envelope';
import { StudentSessionService } from '../../../../core/auth/student-session.service';
import { GS07Page } from './gs07-page';

describe('GS07Page', () => {
  let http: HttpTestingController;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [GS07Page],
      providers: [
        provideHttpClient(),
        provideHttpClientTesting(),
        provideRouter([{ path: 'resources/:resourceId', component: GS07Page }]),
      ],
    }).compileComponents();
    http = TestBed.inject(HttpTestingController);
  });

  afterEach(() => http.verify());

  it('loads a public resource without auth and returns to its course resource tab', async () => {
    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/resources/7?from=course&courseId=42', GS07Page);

    const request = http.expectOne('/api/v1/resources/7');
    expect(request.request.method).toBe('GET');
    expect(request.request.headers.has('Authorization')).toBe(false);
    request.flush(successEnvelope(resource(7, 'Bài đọc công khai', 'PUBLIC')));
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement as HTMLElement;
    expect(root.querySelector('.resource-header__eyebrow')?.textContent?.trim()).toBe(
      'Tài nguyên khóa học',
    );
    expect(root.textContent).not.toContain('GS-07');
    expect(root.textContent).toContain('Bài đọc công khai');
    const openLink = root.querySelector<HTMLAnchorElement>('.resource-action[target="_blank"]');
    expect(openLink?.href).toBe('https://cdn.example.test/resources/7.pdf');
    expect(openLink?.rel).toBe('noopener noreferrer');
    expect(root.querySelector('iframe, video, object, embed')).toBeNull();
    expect(root.querySelector('.resource-crumbs a:nth-of-type(2)')?.getAttribute('href')).toBe(
      '/courses/42?tab=resources',
    );
  });

  it('sends a Student bearer for a private resource and opens the short-lived signed URL', async () => {
    TestBed.inject(StudentSessionService).acceptLoginEnvelope(
      successEnvelope({
        full_name: 'Student One',
        email: 'student@example.test',
        role: 'STUDENT',
        access_token: 'student-access-token',
        refresh_token: 'student-refresh-token',
        token_type: 'Bearer',
        expires_in: 3600,
        refresh_expires_in: 7200,
      }),
    );

    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/resources/8', GS07Page);

    const request = http.expectOne('/api/v1/resources/8');
    expect(request.request.headers.get('Authorization')).toBe('Bearer student-access-token');
    request.flush(successEnvelope(resource(8, 'Tài liệu riêng tư', 'PRIVATE')));
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement as HTMLElement;
    expect(root.textContent).toContain('Tài liệu riêng tư');
    expect(root.textContent).toContain('Tài liệu riêng tư');
    expect(root.querySelector<HTMLAnchorElement>('.resource-action[target="_blank"]')?.href).toBe(
      'https://signed.example.test/resources/8?ttl=300',
    );
  });

  it('prompts for login after the server denies an unauthenticated private resource', async () => {
    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/resources/9', GS07Page);

    http
      .expectOne('/api/v1/resources/9')
      .flush({ message: 'private resource detail' }, { status: 401, statusText: 'Unauthorized' });
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement as HTMLElement;
    expect(root.textContent).toContain('Đăng nhập để xem tài liệu');
    expect(root.textContent).toContain('Tài liệu riêng tư chỉ dành cho học viên đã ghi danh');
    expect(root.textContent).not.toContain('private resource detail');
    expect(root.querySelector('a[routerLink="/login"]')).not.toBeNull();
  });

  it('distinguishes access denied and not found responses', async () => {
    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/resources/10', GS07Page);

    http
      .expectOne('/api/v1/resources/10')
      .flush({}, { status: 403, statusText: 'Forbidden' });
    harness.fixture.detectChanges();
    expect((harness.routeNativeElement as HTMLElement).textContent).toContain(
      'Bạn chưa có quyền truy cập',
    );

    await harness.navigateByUrl('/resources/11', GS07Page);
    http.expectOne('/api/v1/resources/11').flush({}, { status: 404, statusText: 'Not Found' });
    harness.fixture.detectChanges();
    expect((harness.routeNativeElement as HTMLElement).textContent).toContain(
      'Không tìm thấy tài liệu',
    );
  });

  it('retries transient failures and never displays a server error message', async () => {
    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/resources/12', GS07Page);

    http
      .expectOne('/api/v1/resources/12')
      .flush({ message: 'storage credentials leaked' }, { status: 503, statusText: 'Unavailable' });
    harness.fixture.detectChanges();

    const root = harness.routeNativeElement as HTMLElement;
    expect(root.textContent).toContain('Không thể tải tài liệu từ Study Server.');
    expect(root.textContent).not.toContain('storage credentials leaked');
    root.querySelector<HTMLButtonElement>('button')?.click();
    harness.fixture.detectChanges();

    http.expectOne('/api/v1/resources/12').flush(successEnvelope(resource(12, 'Đã tải lại', 'PUBLIC')));
    harness.fixture.detectChanges();
    expect(root.textContent).toContain('Đã tải lại');
  });

  it('does not request a malformed resource ID', async () => {
    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/resources/0', GS07Page);

    expect((harness.routeNativeElement as HTMLElement).textContent).toContain(
      'Không tìm thấy tài liệu',
    );
    http.expectNone('/api/v1/resources/0');
  });
});

function resource(id: number, name: string, visibility: 'PUBLIC' | 'PRIVATE') {
  return {
    id,
    name,
    type: 'DOCUMENT',
    url:
      visibility === 'PRIVATE'
        ? `https://signed.example.test/resources/${id}?ttl=300`
        : `https://cdn.example.test/resources/${id}.pdf`,
    visibility,
    lesson_id: 12,
  };
}

function successEnvelope<T>(data: T): ApiEnvelope<T> {
  return {
    success: true,
    businessCode: 'DESIGN_RESOURCE_RETRIEVED',
    message: 'ok',
    data,
    meta: {},
    traceId: 'gs07-test',
  };
}
