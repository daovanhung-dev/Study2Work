import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { firstValueFrom } from 'rxjs';
import { describe, expect, it } from 'vitest';

import { HANDLE_FORBIDDEN_LOCALLY } from '../../../../core/auth/auth.interceptor';
import { StudentLessonAccessService } from './ST-10-lesson-access.service';

describe('ST-10 lesson access API', () => {
  it('calls #22 and retains only safe metadata', async () => {
    TestBed.configureTestingModule({ providers: [provideHttpClient(), provideHttpClientTesting()] });
    const source = TestBed.inject(StudentLessonAccessService);
    const http = TestBed.inject(HttpTestingController);
    const result = firstValueFrom(source.checkAccess('7'));
    const request = http.expectOne('/api/v1/lessons/7/access');
    expect(request.request.method).toBe('GET');
    expect(request.request.context.get(HANDLE_FORBIDDEN_LOCALLY)).toBe(true);
    request.flush({ success: true, businessCode: 'DESIGN_RESOURCE_RETRIEVED', data: {
      id: 7, course_id: 3, title: 'Bài học', status: 'PUBLISHED', content: '<secret>', video_url: 'https://secret.test/media',
    } });
    await expect(result).resolves.toEqual({ lessonId: 7, courseId: 3, title: 'Bài học' });
    http.verify();
  });
});
