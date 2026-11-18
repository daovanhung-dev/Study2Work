import { TestBed } from '@angular/core/testing';
import { of } from 'rxjs';
import { describe, expect, it } from 'vitest';

import { StudentOverviewService } from '../data-access/ST-01-overview.service';
import { StudentOverviewPage } from './ST-01-overview-page';

describe('ST-01 overview page', () => {
  it('keeps a real course and missing progress contract separate', async () => {
    await TestBed.configureTestingModule({
      imports: [StudentOverviewPage],
      providers: [{
        provide: StudentOverviewService,
        useValue: {
          getCourses: () => of({ items: [{ course_id: 4, name: 'Khóa React', enrollment_status: 'ACTIVE', enrolled_at: '2026-01-01' }], total: 1 }),
          getProgressContract: () => of('API #21 chỉ cung cấp hồ sơ.'),
          getAchievements: () => of({ items: [], total: 0 }),
          getNotifications: () => of({ items: [], total: 0 }),
        },
      }],
    }).compileComponents();
    const fixture = TestBed.createComponent(StudentOverviewPage);
    fixture.detectChanges();

    const content = (fixture.nativeElement as HTMLElement).textContent ?? '';
    expect(content).toContain('Khóa React');
    expect(content).toContain('API #21 chỉ cung cấp hồ sơ.');
    expect(content).toContain('Chưa có thành tích được ghi nhận');
    expect(content).toContain('Chưa có thông báo');
  });
});
