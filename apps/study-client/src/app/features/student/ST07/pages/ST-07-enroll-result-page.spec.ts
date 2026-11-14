import { TestBed } from '@angular/core/testing';
import { ActivatedRoute, convertToParamMap } from '@angular/router';
import { of } from 'rxjs';
import { describe, expect, it } from 'vitest';

import { StudentEnrollResultPage } from './ST-07-enroll-result-page';

describe('ST-07 enrollment result page', () => {
  it('does not claim an enrollment result without a courseId', async () => {
    const paramMap = convertToParamMap({});
    await TestBed.configureTestingModule({
      imports: [StudentEnrollResultPage],
      providers: [{ provide: ActivatedRoute, useValue: { paramMap: of(paramMap), snapshot: { paramMap } } }],
    }).compileComponents();
    const fixture = TestBed.createComponent(StudentEnrollResultPage);
    fixture.detectChanges();

    expect(fixture.componentInstance.state().kind).toBe('missing-context');
    expect((fixture.nativeElement as HTMLElement).textContent).toContain('Thiếu thông tin');
  });
});
