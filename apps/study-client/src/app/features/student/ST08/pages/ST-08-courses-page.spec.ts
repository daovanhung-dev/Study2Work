import { TestBed } from '@angular/core/testing';
import { describe, expect, it } from 'vitest';

import { StudentCoursesPage } from './ST-08-courses-page';

describe('ST-08 courses page', () => {
  it('shows an honest blocked state until enrollment data is available', async () => {
    await TestBed.configureTestingModule({ imports: [StudentCoursesPage] }).compileComponents();
    const fixture = TestBed.createComponent(StudentCoursesPage);
    fixture.detectChanges();

    expect(fixture.componentInstance.state.kind).toBe('blocked');
    expect((fixture.nativeElement as HTMLElement).textContent).toContain('Chưa thể tải khóa học');
  });
});
