import { TestBed } from '@angular/core/testing';
import { ActivatedRoute, convertToParamMap } from '@angular/router';
import { HttpErrorResponse } from '@angular/common/http';
import { of, throwError } from 'rxjs';
import { describe, expect, it, vi } from 'vitest';

import { St04CourseApi } from '../data-access/ST-04-enroll-course.service';
import { StudentEnrollCheckPage } from './ST-04-enroll-check-page';

describe('ST-04 enrollment check page', () => {
  it('loads the requested course', async () => {
    const course = { id: 12, title: 'Angular', description: null, price: '100', status: 'published' };
    const getCourse = vi.fn(() => of(course));
    await TestBed.configureTestingModule({
      imports: [StudentEnrollCheckPage],
      providers: [
        { provide: ActivatedRoute, useValue: { snapshot: { paramMap: convertToParamMap({ courseId: '12' }) } } },
        { provide: St04CourseApi, useValue: { getCourse } },
      ],
    }).compileComponents();
    const fixture = TestBed.createComponent(StudentEnrollCheckPage);
    fixture.detectChanges();

    expect(getCourse).toHaveBeenCalledWith('12');
    expect(fixture.componentInstance.loadState()).toBe('ready');
    expect(fixture.componentInstance.course()).toEqual(course);
  });

  it('shows missing when the course API returns 404', async () => {
    await TestBed.configureTestingModule({
      imports: [StudentEnrollCheckPage],
      providers: [
        { provide: ActivatedRoute, useValue: { snapshot: { paramMap: convertToParamMap({ courseId: '12' }) } } },
        { provide: St04CourseApi, useValue: { getCourse: () => throwError(() => new HttpErrorResponse({ status: 404 })) } },
      ],
    }).compileComponents();
    const fixture = TestBed.createComponent(StudentEnrollCheckPage);
    fixture.detectChanges();

    expect(fixture.componentInstance.loadState()).toBe('missing');
    expect(fixture.componentInstance.course()).toBeNull();
  });

  it('does not call the course API without a courseId', async () => {
    const getCourse = vi.fn();
    await TestBed.configureTestingModule({
      imports: [StudentEnrollCheckPage],
      providers: [
        { provide: ActivatedRoute, useValue: { snapshot: { paramMap: convertToParamMap({}) } } },
        { provide: St04CourseApi, useValue: { getCourse } },
      ],
    }).compileComponents();
    const fixture = TestBed.createComponent(StudentEnrollCheckPage);
    fixture.detectChanges();

    expect(fixture.componentInstance.loadState()).toBe('missing');
    expect(getCourse).not.toHaveBeenCalled();
  });
});
