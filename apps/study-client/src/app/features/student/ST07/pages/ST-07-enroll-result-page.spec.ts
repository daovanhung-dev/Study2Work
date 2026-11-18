import { TestBed } from '@angular/core/testing';
import { ActivatedRoute, convertToParamMap } from '@angular/router';
import { of } from 'rxjs';
import { describe, expect, it } from 'vitest';

import { StudentEnrollResultPage } from './ST-07-enroll-result-page';

async function renderPage(courseId?: string) {
  const paramMap = convertToParamMap(courseId === undefined ? {} : { courseId });
  await TestBed.configureTestingModule({
    imports: [StudentEnrollResultPage],
    providers: [{ provide: ActivatedRoute, useValue: { paramMap: of(paramMap), snapshot: { paramMap } } }],
  }).compileComponents();
  const fixture = TestBed.createComponent(StudentEnrollResultPage);
  fixture.detectChanges();
  return fixture;
}

describe('ST-07 enrollment result page', () => {
  it('does not claim an enrollment result without a courseId', async () => {
    const fixture = await renderPage();

    expect(fixture.componentInstance.state().kind).toBe('missing-context');
    expect((fixture.nativeElement as HTMLElement).textContent).toContain('Thiếu thông tin');
  });

  it.each(['abc', '0', '-1', '01', '9223372036854775808'])(
    'shows an invalid course ID for %s',
    async (courseId) => {
      const fixture = await renderPage(courseId);

      expect(fixture.componentInstance.state().kind).toBe('missing-context');
      expect((fixture.nativeElement as HTMLElement).textContent).toContain('Mã khóa học không hợp lệ');
      expect((fixture.nativeElement as HTMLElement).textContent).not.toContain('Chưa thể truy vấn');
    },
  );

  it('keeps the DD-gated result for a valid course ID', async () => {
    const fixture = await renderPage('1');

    expect(fixture.componentInstance.state().kind).toBe('blocked');
    expect((fixture.nativeElement as HTMLElement).textContent).toContain('Chưa thể xác nhận kết quả đăng ký');
  });
});
