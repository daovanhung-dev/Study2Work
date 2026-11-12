import { TestBed } from '@angular/core/testing';
import { beforeEach, describe, expect, it } from 'vitest';

import { AD02Page } from './ad02-page';

describe('AD02Page', () => {
  beforeEach(async () => {
    await TestBed.configureTestingModule({ imports: [AD02Page] }).compileComponents();
  });

  it('shows an honest disconnected empty state without user records or totals', () => {
    const fixture = TestBed.createComponent(AD02Page);
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    const text = root.textContent ?? '';

    expect(root.querySelector('h1')?.textContent).toContain('Danh sách người dùng');
    expect(text).toContain('Dữ liệu người dùng chưa được kết nối');
    expect(root.querySelectorAll('tbody .user-record')).toHaveLength(0);
    expect(root.querySelectorAll('thead th')).toHaveLength(6);
    expect(text).not.toMatch(/\b\d+\s*\/\s*\d+\b|Tổng số|System Normal|ISO\/IEC 27001/i);
  });

  it('keeps search, filters, reset, and pagination disabled without enum values', () => {
    const fixture = TestBed.createComponent(AD02Page);
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    const input = root.querySelector('input[type="search"]') as HTMLInputElement;
    const selects = Array.from(root.querySelectorAll('select')) as HTMLSelectElement[];
    const buttons = Array.from(root.querySelectorAll('button')) as HTMLButtonElement[];

    expect(input.disabled).toBe(true);
    expect(selects).toHaveLength(2);
    expect(selects.every((select) => select.disabled && select.options.length === 1)).toBe(true);
    expect(buttons.length).toBeGreaterThanOrEqual(3);
    expect(buttons.every((button) => button.disabled)).toBe(true);
    expect(root.querySelectorAll('a[href="#"]')).toHaveLength(0);
  });

  it('does not render unsupported actions or security, health, sync, or audit claims', () => {
    const fixture = TestBed.createComponent(AD02Page);
    fixture.detectChanges();

    const text = (fixture.nativeElement as HTMLElement).textContent ?? '';

    expect(text).not.toMatch(/Thêm người dùng|Xuất dữ liệu|RBAC|bảo mật|đồng bộ|nhật ký kiểm toán|health/i);
  });
});
