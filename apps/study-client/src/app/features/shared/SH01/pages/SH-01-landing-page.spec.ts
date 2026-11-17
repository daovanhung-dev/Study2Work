import { TestBed } from '@angular/core/testing';
import { of, throwError } from 'rxjs';
import { describe, expect, it, vi } from 'vitest';

import { LandingApi } from '../data-access/SH-01-landing.service';
import { GuestLandingPage } from './SH-01-landing-page';

describe('SH-01 landing page', () => {
  it('shows validated category and course data when both requests succeed', async () => {
    const category = { id: 1, name: 'Design', slug: 'design', description: null };
    const course = {
      id: 2,
      title: 'UX basics',
      description: null,
      thumbnail_url: null,
      price: '0.00',
      status: 'PUBLISHED',
      mentor: { id: 3, full_name: 'Mentor', avatar_url: null },
    };
    await TestBed.configureTestingModule({
      imports: [GuestLandingPage],
      providers: [
        { provide: LandingApi, useValue: { getCategories: () => of([category]), getCourses: () => of([course]) } },
      ],
    }).compileComponents();

    const fixture = TestBed.createComponent(GuestLandingPage);
    fixture.detectChanges();

    expect(fixture.componentInstance.categoryState()).toBe('ready');
    expect(fixture.componentInstance.courseState()).toBe('ready');
    expect(fixture.componentInstance.courses()[0]?.title).toBe('UX basics');
  });

  it('shows an empty category state and a course error without inventing data', async () => {
    const getCategories = vi.fn(() => of([]));
    const getCourses = vi.fn(() => throwError(() => new Error('offline')));
    await TestBed.configureTestingModule({
      imports: [GuestLandingPage],
      providers: [{ provide: LandingApi, useValue: { getCategories, getCourses } }],
    }).compileComponents();

    const fixture = TestBed.createComponent(GuestLandingPage);
    fixture.detectChanges();

    expect(getCategories).toHaveBeenCalledOnce();
    expect(getCourses).toHaveBeenCalledOnce();
    expect(fixture.componentInstance.categoryState()).toBe('empty');
    expect(fixture.componentInstance.courseState()).toBe('error');
    expect(fixture.componentInstance.courses()).toEqual([]);
  });
});
