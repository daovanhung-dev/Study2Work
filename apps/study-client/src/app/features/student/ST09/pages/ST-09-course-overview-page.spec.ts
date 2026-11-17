import { TestBed } from '@angular/core/testing';
import { ActivatedRoute, convertToParamMap } from '@angular/router';
import { of } from 'rxjs';
import { describe, expect, it } from 'vitest';

import { StudentCourseOverviewPage } from './ST-09-course-overview-page';

describe('ST-09 course overview page', () => {
  it('does not load a course overview without a courseId', async () => {
    const paramMap = convertToParamMap({});
    await TestBed.configureTestingModule({
      imports: [StudentCourseOverviewPage],
      providers: [{ provide: ActivatedRoute, useValue: { paramMap: of(paramMap), snapshot: { paramMap } } }],
    }).compileComponents();
    const fixture = TestBed.createComponent(StudentCourseOverviewPage);
    fixture.detectChanges();

    expect(fixture.componentInstance.state().kind).toBe('missing-context');
    expect((fixture.nativeElement as HTMLElement).textContent).toContain('Thiếu thông tin');
  });
});
