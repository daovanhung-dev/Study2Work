import { TestBed, type ComponentFixture } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { beforeEach, describe, expect, it } from 'vitest';

import { AdminScreenSurface } from './admin-screen-surface';

describe('AdminScreenSurface', () => {
  let fixture: ComponentFixture<AdminScreenSurface>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AdminScreenSurface],
      providers: [provideRouter([])],
    }).compileComponents();

    fixture = TestBed.createComponent(AdminScreenSurface);
    fixture.componentRef.setInput('definition', {
      id: 'AD-04',
      eyebrow: 'USERS',
      title: 'Người dùng',
      description: 'Danh sách người dùng.',
      sourceNote: 'Nguồn dữ liệu hiện tại.',
      apiReferences: ['#68'],
      mode: 'list',
      columns: ['Người dùng'],
    });
    fixture.componentRef.setInput('viewState', {
      status: 'loaded',
      rows: [],
      pagination: { page: 2, totalPages: 3, total: 24 },
    });
    fixture.detectChanges();
  });

  it('exposes the page controls in a named navigation landmark', () => {
    const navigation = (fixture.nativeElement as HTMLElement).querySelector('nav.pagination');

    expect(navigation?.getAttribute('aria-label')).toBe('Phân trang danh sách');
    expect(navigation?.textContent).toContain('Trang 2 / 3 · 24 mục');
    expect(navigation?.querySelectorAll('button')).toHaveLength(2);
  });
});
