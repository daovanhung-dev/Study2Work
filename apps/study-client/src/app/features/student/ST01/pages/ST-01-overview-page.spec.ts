import { TestBed } from '@angular/core/testing';
import { describe, expect, it } from 'vitest';

import { StudentOverviewPage } from './ST-01-overview-page';

describe('ST-01 overview page', () => {
  it('shows the blocked state instead of invented learning metrics', async () => {
    await TestBed.configureTestingModule({ imports: [StudentOverviewPage] }).compileComponents();
    const fixture = TestBed.createComponent(StudentOverviewPage);
    fixture.detectChanges();

    expect(fixture.componentInstance.state.kind).toBe('blocked');
    expect((fixture.nativeElement as HTMLElement).textContent).toContain('Không có dữ liệu tiến độ thực tế');
  });
});
