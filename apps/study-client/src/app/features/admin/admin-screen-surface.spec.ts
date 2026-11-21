import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { beforeEach, describe, expect, it } from 'vitest';

import { AdminScreenSurface } from '../../shared/ui/admin-screen-surface';
import type { AdminScreenDefinition } from '../../shared/ui/admin-screen.model';
import { AD06Page } from './AD06/pages/ad06-page';

describe('AdminScreenSurface', () => {
  let http: HttpTestingController;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AdminScreenSurface, AD06Page],
      providers: [provideHttpClient(), provideHttpClientTesting(), provideRouter([])],
    }).compileComponents();
    http = TestBed.inject(HttpTestingController);
  });

  it('renders a successful empty response separately from an unavailable/error state', () => {
    const fixture = TestBed.createComponent(AdminScreenSurface);
    fixture.componentRef.setInput('definition', listDefinition);
    fixture.componentRef.setInput('viewState', {
      status: 'loaded',
      rows: [],
      pagination: { page: 1, total: 0, totalPages: 0 },
    });
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    const text = root.textContent ?? '';
    expect(text).toContain('Dữ liệu đã tải từ Study Server');
    expect(text).toContain('Không có kết quả phù hợp');
    expect(text).not.toContain('Trạng thái này không có nghĩa là danh sách đang trống');
    expect(root.querySelector('.pagination')).toBeNull();
    http.expectNone((request) => request.url.startsWith('/api/v1'));
  });

  it('keeps an API error distinct from a successful empty list', () => {
    const fixture = TestBed.createComponent(AdminScreenSurface);
    fixture.componentRef.setInput('definition', listDefinition);
    fixture.componentRef.setInput('viewState', {
      status: 'error',
      message: 'Study Server từ chối bộ lọc.',
    });
    fixture.detectChanges();

    const text = (fixture.nativeElement as HTMLElement).textContent ?? '';
    expect(text).toContain('Không thể tải dữ liệu');
    expect(text).toContain('Study Server từ chối bộ lọc.');
    expect(text).not.toContain('Không có kết quả phù hợp');
    expect(text).toContain('Trạng thái này không có nghĩa là danh sách đang trống');
  });

  it('previews local notification drafts without enabling send', () => {
    const fixture = TestBed.createComponent(AdminScreenSurface);
    fixture.componentRef.setInput('definition', composeDefinition);
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    const title = root.querySelector<HTMLInputElement>('input[type="text"]');
    const content = root.querySelector<HTMLTextAreaElement>('textarea');
    expect(title).not.toBeNull();
    expect(content).not.toBeNull();

    title!.value = 'Thông báo thử';
    title!.dispatchEvent(new Event('input'));
    content!.value = 'Bản nháp chưa gửi';
    content!.dispatchEvent(new Event('input'));
    fixture.detectChanges();

    expect(root.textContent).toContain('Thông báo thử');
    expect(root.textContent).toContain('Bản nháp chưa gửi');
    expect(root.querySelector<HTMLButtonElement>('.form-actions .button--primary')?.disabled).toBe(true);
    http.expectNone((request) => request.url.startsWith('/api/v1'));
  });

  it('does not report the protected course list as empty when there is no Admin session', () => {
    const fixture = TestBed.createComponent(AD06Page);
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    const text = root.textContent ?? '';
    expect(root.querySelectorAll('thead th')).toHaveLength(6);
    expect(text).toContain('Phiên Admin không còn hiệu lực');
    expect(text).not.toContain('Không có kết quả phù hợp');
    http.expectNone('/api/v1/admin/courses');
  });
});

const listDefinition: AdminScreenDefinition = {
  id: 'AD06',
  title: 'Danh sách khóa học',
  eyebrow: 'Quản lý khóa học',
  description: 'Danh sách từ API #73.',
  mode: 'list',
  apiReferences: ['#73'],
  sourceState: 'data-backed',
  sourceNote: 'API #73 trả Page<Course>.',
  columns: ['Mã khóa học', 'Tên khóa học'],
};

const composeDefinition: AdminScreenDefinition = {
  id: 'AD20',
  title: 'Tạo thông báo',
  eyebrow: 'Thông báo',
  description: 'Bản nháp local.',
  mode: 'compose',
  apiReferences: ['#93'],
  sourceState: 'contract-blocked',
  sourceNote: 'API #93 chưa có request đủ contract.',
};
