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
  private readonly curriculumCourseIds = new Subject<string | null>();

  @ViewChildren('courseTab') private readonly courseTabs!: QueryList<ElementRef<HTMLButtonElement>>;

  readonly state = signal<DetailState>({ status: 'loading' });
  readonly selectedTab = signal<CourseDetailTab>('overview');
  readonly curriculumState = signal<GuestCurriculumState>({ status: 'idle' });
  private activeCourseId = '';

  constructor() {
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
        map((params) => params.get('courseId') ?? ''),
        distinctUntilChanged(),
        tap((courseId) => {
          this.activeCourseId = courseId;
          this.state.set({ status: 'loading' });
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
    if (!response.success || response.businessCode !== 'DESIGN_RESOURCE_RETRIEVED') {
      return { status: 'error' };
    }

    const course = response.data.items[0];
    if (!course || course.status !== 'PUBLISHED') return { status: 'not-found' };

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
    if (!response.success || response.businessCode !== 'DESIGN_RESOURCE_RETRIEVED') {
      return { status: 'error' };
    }

    const lessons = toGuestCurriculumLessonSummaries(response.data.items);
    return lessons.length > 0 ? { status: 'ready', lessons } : { status: 'empty' };
  }

  private mapCurriculumHttpError(error: unknown): GuestCurriculumState {
    return error instanceof HttpErrorResponse && error.status === 404
      ? { status: 'not-found' }
      : { status: 'error' };
  }
}
