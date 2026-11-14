import { TestBed } from '@angular/core/testing';
import { ActivatedRoute, convertToParamMap } from '@angular/router';
import { of } from 'rxjs';
import { describe, expect, it } from 'vitest';

import { StudentLessonAccessPage } from './ST-10-lesson-access-page';

describe('ST-10 lesson access page', () => {
  it('does not imply lesson access without a lessonId', async () => {
    const paramMap = convertToParamMap({});
    await TestBed.configureTestingModule({
      imports: [StudentLessonAccessPage],
      providers: [{ provide: ActivatedRoute, useValue: { paramMap: of(paramMap), snapshot: { paramMap } } }],
    }).compileComponents();
    const fixture = TestBed.createComponent(StudentLessonAccessPage);
    fixture.detectChanges();

    expect(fixture.componentInstance.state().kind).toBe('missing-context');
    expect((fixture.nativeElement as HTMLElement).textContent).toContain('Thiếu thông tin');
  });
});
