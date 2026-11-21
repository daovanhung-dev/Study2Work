import { TestBed } from '@angular/core/testing';
import { describe, expect, it } from 'vitest';
import { of } from 'rxjs';
import { provideRouter } from '@angular/router';

import { StudentCoursesPage } from './ST-08-courses-page';
import { StudentCoursesService } from '../data-access/ST-08-courses.service';

describe('ST-08 courses page', () => {
  it('shows an enrolled course returned by API #20', async () => {
    await TestBed.configureTestingModule({
      imports: [StudentCoursesPage],
      providers: [provideRouter([]), {provide: StudentCoursesService, useValue: {getCourses: () => of({
        success: true,
        data: {items: [{course_id: 6, name: 'React Fundamentals', description: null, thumbnail_url: null, price: '0.00', course_status: 'PUBLISHED', enrollment_status: 'ACTIVE', enrolled_at: '2026-11-21'}]},
      })}}],
    }).compileComponents();
    const fixture = TestBed.createComponent(StudentCoursesPage);
    fixture.detectChanges();

    expect(fixture.componentInstance.state().kind).toBe('ready');
    expect((fixture.nativeElement as HTMLElement).textContent).toContain('React Fundamentals');
  });
});
