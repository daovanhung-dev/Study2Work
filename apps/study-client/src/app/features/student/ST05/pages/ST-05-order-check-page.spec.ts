import { TestBed } from '@angular/core/testing';
import { ActivatedRoute, convertToParamMap } from '@angular/router';
import { HttpErrorResponse } from '@angular/common/http';
import { of, throwError } from 'rxjs';
import { describe, expect, it, vi } from 'vitest';

import { St05CourseApi } from '../data-access/ST-05-checkout-course.service';
import { StudentOrderCheckPage } from './ST-05-order-check-page';

describe('ST-05 checkout page', () => {
  it('loads the requested course and links back to its enrollment page', async () => {
    const course = { id: 12, title: 'Angular', description: null, price: '100', status: 'published' };
    const getCourse = vi.fn(() => of(course));
    await TestBed.configureTestingModule({
      imports: [StudentOrderCheckPage],
      providers: [
        { provide: ActivatedRoute, useValue: { snapshot: { paramMap: convertToParamMap({ courseId: '12' }) } } },
        { provide: St05CourseApi, useValue: { getCourse } },
      ],
    }).compileComponents();
    const fixture = TestBed.createComponent(StudentOrderCheckPage);
    fixture.detectChanges();

    expect(getCourse).toHaveBeenCalledWith('12');
    expect(fixture.componentInstance.loadState()).toBe('ready');
    expect(fixture.componentInstance.course()).toEqual(course);
    expect(fixture.componentInstance.backToEnrollUrl).toBe('/student/enroll/12');
  });

  it('shows missing when the course API returns 404', async () => {
    await TestBed.configureTestingModule({
      imports: [StudentOrderCheckPage],
      providers: [
        { provide: ActivatedRoute, useValue: { snapshot: { paramMap: convertToParamMap({ courseId: '12' }) } } },
        { provide: St05CourseApi, useValue: { getCourse: () => throwError(() => new HttpErrorResponse({ status: 404 })) } },
      ],
    }).compileComponents();
    const fixture = TestBed.createComponent(StudentOrderCheckPage);
    fixture.detectChanges();

    expect(fixture.componentInstance.loadState()).toBe('missing');
    expect(fixture.componentInstance.course()).toBeNull();
  });

  it('does not create an order or call the course API without a courseId', async () => {
    const getCourse = vi.fn();
    await TestBed.configureTestingModule({
      imports: [StudentOrderCheckPage],
      providers: [
        { provide: ActivatedRoute, useValue: { snapshot: { paramMap: convertToParamMap({}) } } },
        { provide: St05CourseApi, useValue: { getCourse } },
      ],
    }).compileComponents();
    const fixture = TestBed.createComponent(StudentOrderCheckPage);
    fixture.detectChanges();

    expect(fixture.componentInstance.loadState()).toBe('missing');
    expect(getCourse).not.toHaveBeenCalled();
    expect(fixture.componentInstance.backToEnrollUrl).toBe('/student');
  });
});
