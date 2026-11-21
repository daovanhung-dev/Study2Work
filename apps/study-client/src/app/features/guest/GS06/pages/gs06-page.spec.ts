import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import type { ComponentFixture } from '@angular/core/testing';
import { afterEach, beforeEach, describe, expect, it } from 'vitest';

import type { ApiEnvelope } from '../../../../core/http/api-envelope';
import { GS06Page } from './gs06-page';

describe('GS06Page', () => {
  let fixture: ComponentFixture<GS06Page>;
  let http: HttpTestingController;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [GS06Page],
      providers: [provideHttpClient(), provideHttpClientTesting(), provideRouter([])],
    }).compileComponents();
    http = TestBed.inject(HttpTestingController);
  });

  afterEach(() => http.verify());

  it('loads public resources in API order and links each item to GS-07 by ID', () => {
    fixture = TestBed.createComponent(GS06Page);
    fixture.componentRef.setInput('courseId', '42');
    fixture.detectChanges();

    const request = http.expectOne('/api/v1/courses/42/resources');
    expect(request.request.method).toBe('GET');
    expect(request.request.headers.has('Authorization')).toBe(false);
    request.flush(
      successEnvelope([
        resource(4, 'Bài đọc PDF'),
        resource(9, 'Tài liệu tham khảo'),
      ]),
    );
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    const names = [...root.querySelectorAll('h3')].map((element) => element.textContent?.trim());
    expect(names).toEqual(['Bài đọc PDF', 'Tài liệu tham khảo']);
    const links = [...root.querySelectorAll<HTMLAnchorElement>('.resource-list__item a')];
    expect(links.map((link) => link.getAttribute('href'))).toEqual([
      '/resources/4?from=course&courseId=42',
      '/resources/9?from=course&courseId=42',
    ]);
    expect(links[0]?.getAttribute('aria-label')).toBe('Mở tài liệu: Bài đọc PDF');
  });

  it('shows the public empty state for an empty API #11 array', () => {
    fixture = TestBed.createComponent(GS06Page);
    fixture.componentRef.setInput('courseId', '42');
    fixture.detectChanges();

    http.expectOne('/api/v1/courses/42/resources').flush(successEnvelope([]));
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.textContent).toContain('Khóa học chưa có tài liệu công khai.');
    expect(root.querySelector('.resource-list')).toBeNull();
  });

  it('offers retry after a service error and renders the retried resource', () => {
    fixture = TestBed.createComponent(GS06Page);
    fixture.componentRef.setInput('courseId', '42');
    fixture.detectChanges();

    http
      .expectOne('/api/v1/courses/42/resources')
      .flush({ message: 'private server detail' }, { status: 500, statusText: 'Server Error' });
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.textContent).toContain('Không thể tải tài liệu lúc này.');
    expect(root.textContent).not.toContain('private server detail');
    root.querySelector<HTMLButtonElement>('button')?.click();
    fixture.detectChanges();

    http.expectOne('/api/v1/courses/42/resources').flush(successEnvelope([resource(4, 'Tệp mới')]));
    fixture.detectChanges();
    expect(root.textContent).toContain('Tệp mới');
  });

  it('does not call API #11 for an invalid course ID', () => {
    fixture = TestBed.createComponent(GS06Page);
    fixture.componentRef.setInput('courseId', '0');
    fixture.detectChanges();

    expect((fixture.nativeElement as HTMLElement).textContent).toContain(
      'Mã khóa học không hợp lệ.',
    );
    http.expectNone('/api/v1/courses/0/resources');
  });
});

function resource(id: number, name: string) {
  return {
    id,
    name,
    type: 'DOCUMENT',
    url: `https://cdn.example.test/resources/${id}.pdf`,
    visibility: 'PUBLIC',
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
    traceId: 'gs06-test',
  };
}
