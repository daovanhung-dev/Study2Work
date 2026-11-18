import { TestBed } from '@angular/core/testing';
import { firstValueFrom, of } from 'rxjs';
import { describe, expect, it, vi } from 'vitest';

import type { ApiEnvelope } from '../../../../core/http/api-envelope';
import { StudyApiService } from '../../../../core/http/study-api.service';
import { StudentCourseOverviewService } from './ST-09-course-overview.service';

function envelope(data: unknown): ApiEnvelope<unknown> {
  return { success: true, businessCode: 'DESIGN_RESOURCE_RETRIEVED', message: '', data, meta: {}, traceId: '' };
}

function setup(request: ReturnType<typeof vi.fn>) {
  TestBed.configureTestingModule({ providers: [{ provide: StudyApiService, useValue: { request } }] });
  return TestBed.inject(StudentCourseOverviewService);
}

describe('ST-09 read-only API connection', () => {
  it('stops after #20 when the course is not actively enrolled', async () => {
    const request = vi.fn((_descriptor: { id: number }) => of(envelope({ items: [], pagination: { page: 1, total_pages: 0 } })));
    const service = setup(request);
    expect(await firstValueFrom(service.getOverview('42'))).toBeNull();
    expect(request).toHaveBeenCalledTimes(1);
    expect(request.mock.calls[0]?.[0].id).toBe(20);
  });

  it('finds enrollment across pages, then reads #37 and #09 without exposing lesson media', async () => {
    const request = vi.fn((descriptor: { id: number }, options?: { params?: { get(key: string): string | null } }) => {
      if (descriptor.id === 20) return of(envelope({
        items: options?.params?.get('page') === '1' ? [] : [{ course_id: 42, name: 'Khóa Angular', enrollment_status: 'ACTIVE' }],
        pagination: { page: Number(options?.params?.get('page')), total_pages: 2 },
      }));
      if (descriptor.id === 37) return of(envelope({ course_id: 42, completed_lessons: 1,
        total_lessons: 2, progress_percent: 50, has_content: true }));
      return of(envelope({ items: [{ id: 7, course_id: 42, title: 'Bài 1', order: 0,
        status: 'PUBLISHED', content: 'private content', video_url: 'private media' }] }));
    });
    const service = setup(request);
    const overview = await firstValueFrom(service.getOverview('42'));
    expect(request.mock.calls.map((call) => call[0].id)).toEqual([20, 20, 37, 9]);
    expect(request.mock.calls[0][1]?.params?.get('status')).toBe('ACTIVE');
    expect(overview).toEqual({ courseId: 42, name: 'Khóa Angular', completedLessons: 1,
      totalLessons: 2, progressPercent: 50, publicLessons: [{ id: 7, title: 'Bài 1', order: 0 }] });
    expect(JSON.stringify(overview)).not.toContain('private media');
  });

  it('rejects malformed progress instead of inventing a value', async () => {
    const request = vi.fn((descriptor: { id: number }) => of(envelope(descriptor.id === 20
      ? { items: [{ course_id: 42, name: 'Khóa Angular', enrollment_status: 'ACTIVE' }], pagination: { page: 1, total_pages: 1 } }
      : descriptor.id === 37 ? { course_id: 42, progress_percent: 50 } : { items: [] })));
    const service = setup(request);
    await expect(firstValueFrom(service.getOverview('42'))).rejects.toThrow('Dữ liệu tiến độ');
  });
});
