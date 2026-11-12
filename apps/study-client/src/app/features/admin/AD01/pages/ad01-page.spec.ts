import { TestBed } from '@angular/core/testing';
import { beforeEach, describe, expect, it } from 'vitest';

import { AD01Page } from './ad01-page';

describe('AD01Page', () => {
  beforeEach(async () => {
    await TestBed.configureTestingModule({ imports: [AD01Page] }).compileComponents();
  });

  it('renders the dashboard sections and four KPI cards', () => {
    const fixture = TestBed.createComponent(AD01Page);
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.querySelector('h1')?.textContent).toContain('Bảng điều khiển quản trị hệ thống');
    expect(root.querySelectorAll('.metric-card')).toHaveLength(4);
    expect(root.querySelector('#activity-title')?.textContent).toContain('Hoạt động hệ thống');
    expect(root.querySelector('#services-title')?.textContent).toContain('vận hành máy chủ');
    expect(root.querySelector('#shortcuts-title')?.textContent).toContain('Lối tắt quản lý');
  });

  it('shows unavailable values without unsupported health, identity, or audit claims', () => {
    const fixture = TestBed.createComponent(AD01Page);
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    const text = root.textContent ?? '';
    const values = Array.from(root.querySelectorAll('.metric-value'));

    expect(values).toHaveLength(4);
    expect(values.every((value) => value.textContent?.trim() === '—')).toBe(true);
    expect(text).toContain('Chưa có dữ liệu tích hợp');
    expect(text).toContain('Nguồn nhật ký chưa được kết nối');
    expect(text).toContain('Chưa có nguồn trạng thái được kết nối');
    expect(text).toContain('Thông tin phiên');
    expect(text).not.toMatch(/System Normal|Trực tuyến|Sẵn sàng|Quản Trị Viên|ISO\/IEC 27001/);
    expect(
      Array.from(root.querySelectorAll('.service-state')).every(
        (state) => state.textContent?.trim() === 'Chưa khả dụng',
      ),
    ).toBe(true);
  });

  it('keeps controls and shortcut destinations unavailable', () => {
    const fixture = TestBed.createComponent(AD01Page);
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    const buttons = Array.from(root.querySelectorAll('button'));

    expect(buttons).toHaveLength(9);
    expect(buttons.every((button) => button.disabled)).toBe(true);
    expect(root.querySelectorAll('a[href]')).toHaveLength(0);
  });
});
