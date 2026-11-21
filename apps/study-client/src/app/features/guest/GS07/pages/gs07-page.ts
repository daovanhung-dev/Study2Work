import { HttpErrorResponse } from '@angular/common/http';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { Component, DestroyRef, OnDestroy, computed, inject, signal } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import type { Subscription } from 'rxjs';

import { StudyIcon } from '../../../../shared/ui/study-icon';
import { GuestSiteLayout } from '../../shared/ui/guest-site-layout';
import { isGuestResourceSuccessEnvelope } from '../../shared/models/guest-course.models';
import { GS07ResourceService } from '../data-access/gs07-resource.service';
import type {
  GS07ResourceDetail,
  GS07ResourceScreenState,
} from '../models/gs07-resource-screen-state.model';

@Component({
  imports: [GuestSiteLayout, RouterLink, StudyIcon],
  selector: 'study-gs07-page',
  styleUrl: './gs07-page.css',
  templateUrl: './gs07-page.html',
})
export class GS07Page implements OnDestroy {
  private readonly route = inject(ActivatedRoute);
  private readonly destroyRef = inject(DestroyRef);
  private readonly data = inject(GS07ResourceService);
  private request?: Subscription;
  readonly resourceId = signal<string | null>(null);
  readonly courseId = signal<string | null>(null);
  readonly lessonId = signal<string | null>(null);
  readonly returnPath = computed<(string | number)[]>(() => {
    const courseId = this.courseId();
    const lessonId = this.lessonId();
    if (courseId) return ['/courses', courseId];
    if (lessonId) return ['/student', 'lessons', lessonId, 'resources'];
    return ['/courses'];
  });
  readonly returnQueryParams = computed(() => (this.courseId() ? { tab: 'resources' } : {}));
  readonly state = signal<GS07ResourceScreenState>({ status: 'loading' });

  constructor() {
    this.route.queryParamMap.pipe(takeUntilDestroyed(this.destroyRef)).subscribe((params) => {
      this.courseId.set(toSafeId(params.get('courseId')));
      this.lessonId.set(toSafeId(params.get('lessonId')));
    });
    this.route.paramMap
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe((params) => {
        this.resourceId.set(toSafeId(params.get('resourceId')));
        this.loadResource();
      });
  }

  loadResource(): void {
    this.request?.unsubscribe();
    const resourceId = this.resourceId();
    if (!resourceId) {
      this.state.set({ status: 'invalid-resource' });
      return;
    }
    this.state.set({ status: 'loading' });
    this.request = this.data.resource(resourceId).subscribe({
      next: (response) => {
        const candidate: unknown = response;
        if (
          !isGuestResourceSuccessEnvelope(candidate) ||
          candidate.businessCode !== 'DESIGN_RESOURCE_RETRIEVED'
        ) {
          this.state.set({ status: 'error', message: 'Không thể xác nhận dữ liệu tài liệu từ máy chủ.' });
          return;
        }
        const resource = parseResourceDetail(candidate.data, resourceId);
        if (!resource) {
          this.state.set({ status: 'error', message: 'Không thể xác nhận dữ liệu tài liệu từ máy chủ.' });
          return;
        }
        const safeUrl = toSafeHttpUrl(resource.url);
        this.state.set({ status: 'ready', resource, safeUrl });
      },
      error: (error: unknown) => this.state.set(mapResourceError(error)),
    });
  }

  ngOnDestroy(): void {
    this.request?.unsubscribe();
  }
}

function mapResourceError(error: unknown): GS07ResourceScreenState {
  if (error instanceof HttpErrorResponse) {
    if (error.status === 401) return { status: 'login-required' };
    if (error.status === 403) return { status: 'forbidden' };
    if (error.status === 404) return { status: 'not-found' };
  }
  return { status: 'error', message: resourceErrorMessage(error) };
}

function toSafeId(value: unknown): string | null {
  if (typeof value !== 'string' || !/^\d+$/.test(value) || value.length > 19) return null;
  try {
    const parsed = BigInt(value);
    return parsed > 0n && parsed <= 9_223_372_036_854_775_807n ? value : null;
  } catch {
    return null;
  }
}

function parseResourceDetail(value: unknown, requestedId: string): GS07ResourceDetail | null {
  if (!isRecord(value)) return null;
  const id = value['id'];
  const name = value['name'];
  const type = value['type'];
  const url = value['url'];
  const visibility = value['visibility'];
  const lessonId = value['lesson_id'];

  if (
    !isPositiveSafeInteger(id) ||
    BigInt(id) !== BigInt(requestedId) ||
    typeof name !== 'string' ||
    !name.trim() ||
    typeof type !== 'string' ||
    !type.trim() ||
    typeof url !== 'string' ||
    !url.trim() ||
    (visibility !== 'PUBLIC' && visibility !== 'PRIVATE') ||
    (lessonId !== null && !isPositiveInteger(lessonId))
  ) {
    return null;
  }

  return { id, name, type, url, visibility, lesson_id: lessonId };
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

function isPositiveSafeInteger(value: unknown): value is number {
  return typeof value === 'number' && Number.isSafeInteger(value) && value > 0;
}

function isPositiveInteger(value: unknown): value is number {
  return typeof value === 'number' && Number.isInteger(value) && value > 0;
}

function resourceErrorMessage(error: unknown): string {
  // Server messages can contain implementation details; present a stable safe
  // message and keep the original error out of the rendered UI.
  void error;
  return 'Không thể tải tài liệu từ Study Server. Vui lòng thử lại.';
}

function toSafeHttpUrl(value: unknown): string | null {
  if (typeof value !== 'string' || !value.trim() || value !== value.trim()) return null;
  try {
    const url = new URL(value);
    return (url.protocol === 'https:' || url.protocol === 'http:') &&
      !!url.hostname &&
      !url.username &&
      !url.password
      ? value
      : null;
  } catch {
    return null;
  }
}
