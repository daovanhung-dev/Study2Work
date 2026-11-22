import { ActivatedRoute, Navigation, Router, convertToParamMap, provideRouter } from '@angular/router';
import { TestBed } from '@angular/core/testing';
import { of } from 'rxjs';
import { afterEach, describe, expect, it, vi } from 'vitest';

import { AD07ApiService } from '../data-access/ad07-api.service';
import { AD07Page } from './ad07-page';

describe('AD07Page', () => {
  afterEach(() => vi.restoreAllMocks());

  async function createPage(courseCreated: boolean) {
    const paramMap = convertToParamMap({ courseId: '77' });
    await TestBed.configureTestingModule({
      imports: [AD07Page],
      providers: [
        provideRouter([]),
        {
          provide: ActivatedRoute,
          useValue: { paramMap: of(paramMap), snapshot: { paramMap } },
        },
        {
          provide: AD07ApiService,
          useValue: {
            getCourse: vi.fn().mockReturnValue(of({
              success: true,
              businessCode: 'DESIGN_RESOURCE_RETRIEVED',
              data: {
                items: [{
                  id: 77,
                  title: 'Created course',
                  description: null,
                  thumbnail_url: null,
                  price: '250000.00',
                  status: 'DRAFT',
                  mentor: { id: 8, full_name: 'Active Mentor', avatar_url: null },
                }],
                pagination: { page: 1, size: 1, total: 1, total_pages: 1 },
              },
              message: 'Course retrieved.',
              meta: {},
              traceId: 'test-trace',
            })),
          },
        },
      ],
    }).compileComponents();

    const router = TestBed.inject(Router);
    vi.spyOn(router, 'getCurrentNavigation').mockReturnValue(
      (courseCreated ? { extras: { state: { courseCreated: true } } } : null) as unknown as Navigation | null,
    );
    const fixture = TestBed.createComponent(AD07Page);
    fixture.detectChanges();
    await fixture.whenStable();
    fixture.detectChanges();
    return fixture;
  }

  it('announces that a newly created draft course opened from AD-06', async () => {
    const fixture = await createPage(true);
    const notice = (fixture.nativeElement as HTMLElement).querySelector('[role="status"]');

    expect(notice?.textContent).toContain('Khóa học đã được tạo thành công ở trạng thái Nháp.');
  });

  it('does not show the create notice when the navigation has no create state', async () => {
    const fixture = await createPage(false);

    expect((fixture.nativeElement as HTMLElement).textContent).not.toContain(
      'Khóa học đã được tạo thành công ở trạng thái Nháp.',
    );
  });
});
