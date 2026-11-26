import { HttpErrorResponse } from '@angular/common/http';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import {
  Component,
  DestroyRef,
  ElementRef,
  inject,
  QueryList,
  signal,
  ViewChildren,
} from '@angular/core';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { catchError, distinctUntilChanged, map, of, Subject, switchMap, tap } from 'rxjs';

import type { ApiEnvelope } from '../../../../core/http/api-envelope';
import { StudyIcon } from '../../../../shared/ui/study-icon';
import type {
  GuestPublicCourse,
  GuestPublicCoursePage,
} from '../../shared/models/guest-course.models';
import {
  isGuestPublicCoursePage,
  isGuestResourceSuccessEnvelope,
} from '../../shared/models/guest-course.models';
import { GuestSiteLayout } from '../../shared/ui/guest-site-layout';
import { GS03CurriculumService } from '../data-access/gs03-curriculum.service';
import { GS03CourseDetailService } from '../data-access/gs03-course-detail.service';
import { GS05Page } from '../../GS05/pages/gs05-page';
import { GS06Page } from '../../GS06/pages/gs06-page';
import {
  toGuestCurriculumLessonSummaries,
  type GuestCourseCurriculumPage,
  type GuestCurriculumState,
} from '../models/gs03-curriculum.models';
import { GS03CurriculumPanel } from '../ui/gs03-curriculum-panel';

type DetailState =
  | { status: 'loading' }
  | { status: 'ready'; course: GuestPublicCourse }
  | { status: 'not-found' }
  | { status: 'error' };

type CourseDetailTab = 'overview' | 'curriculum' | 'reviews' | 'resources';

@Component({
  imports: [GuestSiteLayout, GS03CurriculumPanel, GS05Page, GS06Page, RouterLink, StudyIcon],
  selector: 'study-gs03-page',
  styleUrl: './gs03-page.css',
  templateUrl: './gs03-page.html',
})
export class GS03Page {
  private readonly route = inject(ActivatedRoute);
  private readonly destroyRef = inject(DestroyRef);
  private readonly router = inject(Router);
  private readonly detailService = inject(GS03CourseDetailService);
  private readonly curriculumService = inject(GS03CurriculumService);
  private readonly detailCourseIds = new Subject<string | null>();
  private readonly curriculumCourseIds = new Subject<string | null>();

  @ViewChildren('courseTab') private readonly courseTabs!: QueryList<ElementRef<HTMLButtonElement>>;

  readonly state = signal<DetailState>({ status: 'loading' });
  readonly selectedTab = signal<CourseDetailTab>('overview');
  readonly curriculumState = signal<GuestCurriculumState>({ status: 'idle' });
  readonly courseImageFailed = signal(false);
  readonly mentorAvatarFailed = signal(false);
  private activeCourseId = '';

  constructor() {
    this.detailCourseIds
      .pipe(
        tap(() => {
          this.state.set({ status: 'loading' });
          this.courseImageFailed.set(false);
          this.mentorAvatarFailed.set(false);
          this.curriculumCourseIds.next(null);
        }),
        switchMap((courseId) => {
          if (!courseId) return of<DetailState>({ status: 'not-found' });

          return this.detailService.getCourse(courseId).pipe(
            map((response) => this.mapResponse(response)),
            catchError((error: unknown) => of(this.mapHttpError(error))),
          );
        }),
        takeUntilDestroyed(this.destroyRef),
      )
      .subscribe((state) => {
        this.state.set(state);
        this.syncCurriculumRequest();
        if (state.status === 'not-found') {
          void this.router.navigateByUrl('/not-found', { replaceUrl: true });
        }
      });

    this.curriculumCourseIds
      .pipe(
        distinctUntilChanged(),
        tap((courseId) =>
          this.curriculumState.set(courseId ? { status: 'loading' } : { status: 'idle' }),
        ),
        switchMap((courseId) => {
          if (!courseId) return of<GuestCurriculumState>({ status: 'idle' });

          return this.curriculumService.getCourseCurriculum(courseId).pipe(
            map((response) => this.mapCurriculumResponse(response)),
            catchError((error: unknown) => of(this.mapCurriculumHttpError(error))),
          );
        }),
        takeUntilDestroyed(this.destroyRef),
      )
      .subscribe((state) => this.curriculumState.set(state));

    this.route.queryParamMap
      .pipe(
        map((params): CourseDetailTab => {
          const tab = params.get('tab');
          return tab === 'curriculum' || tab === 'reviews' || tab === 'resources'
            ? tab
            : 'overview';
        }),
        distinctUntilChanged(),
        takeUntilDestroyed(this.destroyRef),
      )
      .subscribe((tab) => {
        this.selectedTab.set(tab);
        this.syncCurriculumRequest();
      });

    this.route.paramMap
      .pipe(
        map((params) => toSafeCourseId(params.get('courseId'))),
        distinctUntilChanged(),
        takeUntilDestroyed(this.destroyRef),
      )
      .subscribe((courseId) => {
        this.activeCourseId = courseId ?? '';
        this.detailCourseIds.next(courseId);
      });
  }

  retryCourse(): void {
    if (this.activeCourseId) this.detailCourseIds.next(this.activeCourseId);
  }

  onCourseImageError(): void {
    this.courseImageFailed.set(true);
  }

  onMentorAvatarError(): void {
    this.mentorAvatarFailed.set(true);
  }

  retryCurriculum(): void {
    if (this.state().status !== 'ready' || this.selectedTab() !== 'curriculum') return;
    this.curriculumCourseIds.next(null);
    this.syncCurriculumRequest();
  }

  selectTab(tab: CourseDetailTab): void {
    void this.router.navigate([], {
      relativeTo: this.route,
      queryParams: { tab: tab === 'overview' ? null : tab },
      queryParamsHandling: 'merge',
    });
  }

  onTabKeydown(event: KeyboardEvent): void {
    const tabs = this.courseTabs?.toArray() ?? [];
    const currentIndex = tabs.findIndex((tab) => tab.nativeElement === event.currentTarget);
    if (currentIndex < 0 || tabs.length === 0) return;

    let nextIndex: number;
    switch (event.key) {
      case 'ArrowRight':
        nextIndex = (currentIndex + 1) % tabs.length;
        break;
      case 'ArrowLeft':
        nextIndex = (currentIndex - 1 + tabs.length) % tabs.length;
        break;
      case 'Home':
        nextIndex = 0;
        break;
      case 'End':
        nextIndex = tabs.length - 1;
        break;
      default:
        return;
    }

    event.preventDefault();
    tabs[nextIndex].nativeElement.focus();
    const tabOrder: CourseDetailTab[] = ['overview', 'curriculum', 'reviews', 'resources'];
    this.selectTab(tabOrder[nextIndex]);
  }

  private syncCurriculumRequest(): void {
    if (
      this.state().status === 'ready' &&
      this.selectedTab() === 'curriculum' &&
      this.activeCourseId
    ) {
      this.curriculumCourseIds.next(this.activeCourseId);
      return;
    }

    this.curriculumCourseIds.next(null);
  }

  private mapResponse(response: ApiEnvelope<GuestPublicCoursePage>): DetailState {
    const candidate: unknown = response;
    if (
      !isGuestResourceSuccessEnvelope(candidate) ||
      candidate.businessCode !== 'DESIGN_RESOURCE_RETRIEVED' ||
      !isGuestPublicCoursePage(candidate.data)
    ) {
      return { status: 'error' };
    }

    const result = candidate.data;
    if (
      result.items.length !== 1 ||
      result.pagination.page !== 1 ||
      result.pagination.size !== 1 ||
      result.pagination.total !== 1 ||
      result.pagination.total_pages !== 1
    ) {
      return { status: 'error' };
    }

    const course = result.items[0];
    if (course.status !== 'PUBLISHED') return { status: 'not-found' };

    return { status: 'ready', course };
  }

  private mapHttpError(error: unknown): DetailState {
    return error instanceof HttpErrorResponse && error.status === 404
      ? { status: 'not-found' }
      : { status: 'error' };
  }

  private mapCurriculumResponse(
    response: ApiEnvelope<GuestCourseCurriculumPage>,
  ): GuestCurriculumState {
    const candidate: unknown = response;
    if (
      !isGuestResourceSuccessEnvelope(candidate) ||
      candidate.businessCode !== 'DESIGN_RESOURCE_RETRIEVED' ||
      !isGuestCourseCurriculumPage(candidate.data)
    ) {
      return { status: 'error' };
    }

    const lessons = toGuestCurriculumLessonSummaries(candidate.data.items).sort(
      (left, right) => left.order - right.order,
    );
    return lessons.length > 0 ? { status: 'ready', lessons } : { status: 'empty' };
  }

  private mapCurriculumHttpError(error: unknown): GuestCurriculumState {
    return error instanceof HttpErrorResponse && error.status === 404
      ? { status: 'not-found' }
      : { status: 'error' };
  }
}

function isGuestCourseCurriculumPage(value: unknown): value is GuestCourseCurriculumPage {
  if (!isRecord(value) || !Array.isArray(value['items']) || !isRecord(value['pagination'])) {
    return false;
  }

  const items = value['items'];
  const pagination = value['pagination'];
  if (
    !isPositiveInteger(pagination['page']) ||
    !isNonnegativeInteger(pagination['size']) ||
    !isNonnegativeInteger(pagination['total']) ||
    !isNonnegativeInteger(pagination['total_pages'])
  ) {
    return false;
  }

  return (
    items.every(isGuestCurriculumLesson) &&
    pagination['page'] === 1 &&
    pagination['size'] === items.length &&
    pagination['total'] === items.length &&
    pagination['total_pages'] === (items.length > 0 ? 1 : 0)
  );
}

function isGuestCurriculumLesson(value: unknown): value is GuestCourseCurriculumPage['items'][number] {
  if (!isRecord(value)) return false;
  return (
    isPositiveInteger(value['id']) &&
    isPositiveInteger(value['course_id']) &&
    typeof value['title'] === 'string' &&
    isNullableString(value['content']) &&
    isNullableString(value['video_url']) &&
    typeof value['order'] === 'number' &&
    Number.isInteger(value['order']) &&
    value['status'] === 'PUBLISHED'
  );
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

function isPositiveInteger(value: unknown): value is number {
  return typeof value === 'number' && Number.isInteger(value) && value > 0;
}

function isNonnegativeInteger(value: unknown): value is number {
  return typeof value === 'number' && Number.isInteger(value) && value >= 0;
}

function isNullableString(value: unknown): value is string | null {
  return value === null || typeof value === 'string';
}

function toSafeCourseId(value: string | null): string | null {
  if (!value || !/^\d+$/.test(value) || value.length > 19) return null;
  try {
    const id = BigInt(value);
    return id > 0n && id <= 9_223_372_036_854_775_807n ? value : null;
  } catch {
    return null;
  }
}
