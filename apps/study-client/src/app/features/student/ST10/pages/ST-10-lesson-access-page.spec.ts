import { HttpErrorResponse } from '@angular/common/http';
import { TestBed } from '@angular/core/testing';
import { ActivatedRoute, convertToParamMap } from '@angular/router';
import { of, throwError } from 'rxjs';
import { describe, expect, it, vi } from 'vitest';

import { StudentLessonAccessService } from '../data-access/ST-10-lesson-access.service';
import { StudentLessonAccessPage } from './ST-10-lesson-access-page';

async function render(lessonId: string | undefined, response: ReturnType<StudentLessonAccessService['checkAccess']>) {
  const paramMap = convertToParamMap(lessonId ? { lessonId } : {});
  const checkAccess = vi.fn(() => response);
  await TestBed.configureTestingModule({
    imports: [StudentLessonAccessPage],
    providers: [
      { provide: ActivatedRoute, useValue: { paramMap: of(paramMap), snapshot: { paramMap } } },
      { provide: StudentLessonAccessService, useValue: { checkAccess } },
    ],
  }).compileComponents();
  const fixture = TestBed.createComponent(StudentLessonAccessPage);
  fixture.detectChanges();
  return { fixture, checkAccess, element: fixture.nativeElement as HTMLElement };
}

describe('ST-10 lesson access page', () => {
  it('does not request access without a valid lessonId', async () => {
    const { fixture, checkAccess, element } = await render(undefined, of({ lessonId: 1, courseId: 2, title: 'A' }));
    expect(fixture.componentInstance.state().kind).toBe('missing-context');
    expect(checkAccess).not.toHaveBeenCalled();
    expect(element.querySelector<HTMLButtonElement>('.btn-locked')?.disabled).toBe(true);
  });

  it('keeps protected content locked even after access is verified', async () => {
    const { fixture, checkAccess, element } = await render('1', of({ lessonId: 1, courseId: 2, title: 'Bài học' }));
    expect(checkAccess).toHaveBeenCalledWith('1');
    expect(fixture.componentInstance.state().kind).toBe('allowed');
    expect(element.textContent).toContain('ĐÃ XÁC MINH');
    expect(element.textContent).toContain('Bài học');
    expect(element.querySelector<HTMLAnchorElement>('.btn-white')?.getAttribute('href')).toBe('/student/courses/2');
    expect(element.querySelector<HTMLButtonElement>('.btn-locked')?.disabled).toBe(true);
    expect(element.querySelector('video, audio, iframe')).toBeNull();
    expect(element.querySelectorAll('.api-row')).toHaveLength(3);
  });

  it.each([403, 404, 500])('shows a local gated state for HTTP %i', async (status) => {
    const error = new HttpErrorResponse({ status, statusText: 'Failure' });
    const { fixture, element } = await render('1', throwError(() => error));
    expect(fixture.componentInstance.state().kind).toBe(status === 403 ? 'denied' : status === 404 ? 'not-found' : 'blocked');
    expect(element.querySelector<HTMLButtonElement>('.btn-locked')?.disabled).toBe(true);
    expect(element.querySelector('video, audio, iframe')).toBeNull();
  });
});
