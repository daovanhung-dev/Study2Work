import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { ActivatedRoute, convertToParamMap, provideRouter, type ParamMap } from '@angular/router';
import { BehaviorSubject, firstValueFrom } from 'rxjs';
import { afterEach, beforeEach, describe, expect, it } from 'vitest';

import { AdminSessionService } from '../../../../core/auth/admin-session.service';
import type { ApiEnvelope } from '../../../../core/http/api-envelope';
import type { AdminDiscussion, AdminDiscussionComment, AdminPage } from '../../admin-api.models';
import { AD23Page } from './ad23-page';

describe('AD23Page', () => {
  let http: HttpTestingController;
  let routeParams: BehaviorSubject<ParamMap>;

  beforeEach(async () => {
    routeParams = new BehaviorSubject(convertToParamMap({ discussionId: '701' }));
    await TestBed.configureTestingModule({
      imports: [AD23Page],
      providers: [
        provideHttpClient(),
        provideHttpClientTesting(),
        provideRouter([]),
        { provide: ActivatedRoute, useValue: { paramMap: routeParams.asObservable() } },
      ],
    }).compileComponents();
    http = TestBed.inject(HttpTestingController);
  });

  afterEach(() => http.verify());

  it('renders the #98 discussion and direct comments while keeping moderation actions disabled', async () => {
    await signIn();
    const fixture = TestBed.createComponent(AD23Page);
    fixture.detectChanges();
    await fixture.whenStable();

    const request = http.expectOne('/api/v1/admin/discussions/701');
    expect(request.request.headers.get('Authorization')).toBe('Bearer access-token-1');
    request.flush(
      successEnvelope(
        page(
          [
            discussion(701, 'Nội dung thảo luận cần xem xét.', [
              comment(
                702,
                701,
                'Trần Bình',
                'Tôi xin bổ sung một chi tiết.',
                '2026-11-13T10:30:00Z',
              ),
            ]),
          ],
          1,
          1,
          1,
        ),
      ),
    );
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    const text = root.textContent ?? '';
    expect(text).toContain('Tiêu đề được dựng từ nội dung');
    expect(text).toContain('Nội dung thảo luận cần xem xét.');
    expect(text).toContain('Tác giả');
    expect(text).toContain('Mã khóa học');
    expect(text).toContain('Trần Bình: Tôi xin bổ sung một chi tiết. (13/11/2026)');
    expect(text).toContain('Không có report relation');
    expect(root.querySelector('a[href="/admin/discussions/reported"]')).not.toBeNull();
    const actions = root.querySelectorAll<HTMLButtonElement>('.action-item button');
    expect(actions.length).toBe(3);
    expect([...actions].every((button) => button.disabled)).toBe(true);
    for (const button of actions) {
      const reasonId = button.getAttribute('aria-describedby');
      const reason = reasonId ? root.querySelector<HTMLElement>(`#${reasonId}`) : null;

      expect(reasonId).toBeTruthy();
      expect(reason).not.toBeNull();
      expect(button.closest('.action-item')?.contains(reason)).toBe(true);
      expect(reason?.textContent?.trim()).not.toBe('');
    }
  });

  it('preserves the int64 route ID as text and avoids displaying it inaccurately', async () => {
    await signIn();
    routeParams.next(convertToParamMap({ discussionId: '9007199254740992' }));
    const fixture = TestBed.createComponent(AD23Page);
    fixture.detectChanges();
    await fixture.whenStable();

    const request = http.expectOne('/api/v1/admin/discussions/9007199254740992');
    request.flush(
      successEnvelope(page([discussion(9007199254740992, 'Nội dung mã lớn', [])], 1, 1, 1)),
    );
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.textContent).toContain('Không thể tải thảo luận');
    expect(root.textContent).not.toContain('9007199254740992');
    expect(root.querySelector('.action-item')).toBeNull();
  });

  it('shows the actual API 404 state for an unknown discussion', async () => {
    await signIn();
    const fixture = TestBed.createComponent(AD23Page);
    fixture.detectChanges();
    await fixture.whenStable();

    http
      .expectOne('/api/v1/admin/discussions/701')
      .flush({}, { status: 404, statusText: 'Not Found' });
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.textContent).toContain('Không thể tải thảo luận');
    expect(root.textContent).toContain('Không tìm thấy dữ liệu được yêu cầu.');
    expect(root.querySelector('.action-item')).toBeNull();
  });

  async function signIn(): Promise<void> {
    const login = firstValueFrom(
      TestBed.inject(AdminSessionService).login('admin@example.test', 'password'),
    );
    http.expectOne('/api/v1/auth/login').flush(
      successEnvelope({
        full_name: 'Admin User',
        email: 'admin@example.test',
        role: 'ADMIN',
        access_token: 'access-token-1',
        refresh_token: 'refresh-token-1',
        token_type: 'bearer',
        expires_in: 60,
        refresh_expires_in: 3600,
      }),
    );
    await login;
  }
});

function discussion(
  id: number,
  content: string,
  comments: readonly AdminDiscussionComment[],
): AdminDiscussion {
  return {
    id,
    course_id: 55,
    title: content.slice(0, 120),
    content,
    author: { id: 8, full_name: 'Nguyễn An', avatar_url: null },
    status: 'ACTIVE',
    comments,
  };
}

function comment(
  id: number,
  discussionId: number,
  fullName: string,
  content: string,
  createdAt: string,
): AdminDiscussionComment {
  return {
    id,
    discussion_id: discussionId,
    content,
    author: { id: 9, full_name: fullName, avatar_url: null },
    created_at: createdAt,
  };
}

function page(
  items: readonly AdminDiscussion[],
  pageNumber: number,
  total: number,
  totalPages: number,
): AdminPage<AdminDiscussion> {
  return {
    items,
    pagination: { page: pageNumber, size: 1, total, total_pages: totalPages },
  };
}

function successEnvelope<T>(data: T): ApiEnvelope<T> {
  return {
    success: true,
    businessCode: 'DESIGN_RESOURCE_RETRIEVED',
    message: 'ok',
    data,
    meta: {},
    traceId: 'test-trace',
  };
}
