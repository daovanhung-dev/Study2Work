import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { firstValueFrom } from 'rxjs';
import { afterEach, beforeEach, describe, expect, it } from 'vitest';

import { AdminSessionService } from '../../../../core/auth/admin-session.service';
import type { ApiEnvelope } from '../../../../core/http/api-envelope';
import type { AdminLesson } from '../../admin-api.models';
import { AD12ApiService } from '../data-access/ad12-api.service';
import { AD12Page } from './ad12-page';

describe('AD12Page', () => {
  let http: HttpTestingController;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AD12Page],
      providers: [provideHttpClient(), provideHttpClientTesting(), provideRouter([])],
    }).compileComponents();
    http = TestBed.inject(HttpTestingController);
  });

  afterEach(() => http.verify());

  it('renders the API #82 lesson projection without unsupported columns or actions', async () => {
    await signIn();
    const fixture = TestBed.createComponent(AD12Page);
    fixture.detectChanges();
    await fixture.whenStable();

    const request = http.expectOne('/api/v1/admin/lessons');
    expect(request.request.headers.get('Authorization')).toBe('Bearer access-token-1');
    expect(request.request.params.keys()).toEqual([]);
    request.flush(successEnvelope([
      lesson(73, 42, 'Cell Structure', 2, 'ACTIVE'),
      lesson(74, 42, 'Cell Membrane', 3, 'DRAFT'),
    ]));
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    const text = root.textContent ?? '';
    const headers = root.querySelector('thead')?.textContent ?? '';
    expect(text).toContain('Cell Structure');
    expect(text).toContain('Cell Membrane');
    expect(text).toContain('73');
    expect(text).toContain('42');
    expect(text).toContain('2');
    expect(text).toContain('ACTIVE');
    expect(text).toContain('DRAFT');
    expect(text).toContain('2 bài học được trả về trong response');
    expect(headers).toContain('Mã định danh');
    expect(headers).toContain('Mã khóa học');
    expect(headers).toContain('Thứ tự');
    expect(headers).not.toContain('Loại nội dung');
    expect(headers).not.toContain('Tổng');
    expect(text).not.toContain('Secret lesson body');
    expect(text).not.toContain('private-video.example.test');
    expect(root.querySelector('a')).toBeNull();
    expect(Array.from(root.querySelectorAll<HTMLButtonElement>('button')).every((button) => button.disabled)).toBe(true);
  });

  it('renders a successful empty response without claiming synchronization state', async () => {
    await signIn();
    const fixture = TestBed.createComponent(AD12Page);
    fixture.detectChanges();
    await fixture.whenStable();
    http.expectOne('/api/v1/admin/lessons').flush(successEnvelope([]));
    fixture.detectChanges();

    const text = (fixture.nativeElement as HTMLElement).textContent ?? '';
    expect(text).toContain('Chưa có bài học trong phản hồi');
    expect(text).toContain('0 bài học được trả về trong response');
    expect(text).not.toContain('đang được đồng bộ');
  });

  it('sends the course filter under the exact key while preserving signed-int64 text', async () => {
    await signIn();
    const result = firstValueFrom(TestBed.inject(AD12ApiService).getLessons({
      course: '9223372036854775807',
    }));
    const request = http.expectOne('/api/v1/admin/lessons?course=9223372036854775807');
    request.flush(successEnvelope([]));
    await result;
  });

  async function signIn(): Promise<void> {
    const login = firstValueFrom(
      TestBed.inject(AdminSessionService).login('admin@example.test', 'password'),
    );
    http.expectOne('/api/v1/auth/login').flush(successEnvelope({
      full_name: 'Admin User',
      email: 'admin@example.test',
      role: 'ADMIN',
      access_token: 'access-token-1',
      refresh_token: 'refresh-token-1',
      token_type: 'bearer',
      expires_in: 60,
      refresh_expires_in: 3600,
    }));
    await login;
  }
});

function lesson(
  id: number,
  courseId: number,
  title: string,
  order: number,
  status: string,
): AdminLesson {
  return {
    id,
    course_id: courseId,
    title,
    content: 'Secret lesson body',
    video_url: 'https://private-video.example.test/lesson.mp4',
    order,
    status,
  };
}

function successEnvelope<T>(data: T): ApiEnvelope<T> {
  return {
    success: true,
    businessCode: 'DESIGN_RESOURCE_RETRIEVED',
    message: 'ok',
    data,
    meta: {},
    traceId: 'test-trace',
  };
}
