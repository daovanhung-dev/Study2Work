import { TestBed } from '@angular/core/testing';
import { ActivatedRoute, convertToParamMap } from '@angular/router';
import { HttpErrorResponse } from '@angular/common/http';
import { of, throwError } from 'rxjs';
import { describe, expect, it, vi } from 'vitest';

import { St05CourseApi } from '../data-access/ST-05-checkout-course.service';
import { StudentOrderCheckPage } from './ST-05-order-check-page';

describe('ST-05 checkout page', () => {
  async function render(courseId: string | undefined, getCourse: ReturnType<typeof vi.fn>) {
    await TestBed.configureTestingModule({
      imports: [StudentOrderCheckPage],
      providers: [
        { provide: ActivatedRoute, useValue: { snapshot: { paramMap: convertToParamMap(courseId ? { courseId } : {}) } } },
        { provide: St05CourseApi, useValue: { getCourse } },
      ],
    }).compileComponents();
    const fixture = TestBed.createComponent(StudentOrderCheckPage);
    fixture.detectChanges();
    return fixture;
  }

  it('renders server course and price while withholding order creation', async () => {
    const course = { id: 12, title: 'Angular', description: 'Du lieu seed de test API #10', price: '100.00', status: 'PUBLISHED' };
    const getCourse = vi.fn(() => of(course));
    const fixture = await render('12', getCourse);
    const element = fixture.nativeElement as HTMLElement;

    expect(getCourse).toHaveBeenCalledWith('12');
    expect(fixture.componentInstance.loadState()).toBe('ready');
    expect(element.textContent).toContain('Angular');
    expect(element.textContent).toContain('100.00');
    expect(element.textContent).not.toContain('Du lieu seed de test API #10');
    expect(element.querySelector('.create-order')).toBeNull();
    expect(element.querySelector<HTMLAnchorElement>('.return-link')?.getAttribute('href')).toBe('/student/enroll/12');
  });

  it('shows missing when the course API returns 404', async () => {
    const fixture = await render('12', vi.fn(() => throwError(() => new HttpErrorResponse({ status: 404 }))));
    expect(fixture.componentInstance.loadState()).toBe('missing');
  });

  it('does not query the API or construct an invalid return URL for malformed courseId', async () => {
    const getCourse = vi.fn();
    const fixture = await render('abc', getCourse);
    const element = fixture.nativeElement as HTMLElement;

    expect(fixture.componentInstance.loadState()).toBe('missing');
    expect(getCourse).not.toHaveBeenCalled();
    expect(element.querySelector<HTMLAnchorElement>('.return-link')?.getAttribute('href')).toBe('/student');
    expect(element.querySelector<HTMLAnchorElement>('.crumb-row a[href*="/student/enroll/"]')).toBeNull();
  });

  it('does not query the API without a courseId', async () => {
    const getCourse = vi.fn();
    const fixture = await render(undefined, getCourse);
    expect(fixture.componentInstance.loadState()).toBe('missing');
    expect(getCourse).not.toHaveBeenCalled();
  });
});
