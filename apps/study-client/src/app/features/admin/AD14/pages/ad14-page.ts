import { HttpErrorResponse } from '@angular/common/http';
import { Component, computed, inject, signal } from '@angular/core';
import { toSignal } from '@angular/core/rxjs-interop';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { catchError, map, of, startWith, switchMap } from 'rxjs';

import { AdminSessionError } from '../../../../core/auth/admin-session.service';
import { StudyIcon } from '../../../../shared/ui/study-icon';
import { isAdminLesson } from '../../admin-api-guards';
import type { AdminLesson } from '../../admin-api.models';
import { isSignedInt64RouteId } from '../../admin-screen-state';
import { AD14ApiService } from '../data-access/ad14-api.service';
import { AD14_SCREEN } from '../models/ad14-screen.model';

interface LessonDraft {
  readonly title: string;
  readonly content: string | null;
  readonly order: string;
}

type AD14PageState =
  | { readonly status: 'loading' }
  | { readonly status: 'loaded'; readonly lesson: AdminLesson }
  | { readonly status: 'error'; readonly message: string };

const LOADING_STATE: AD14PageState = { status: 'loading' };

@Component({
  imports: [RouterLink, StudyIcon],
  selector: 'study-ad14-page',
  templateUrl: './ad14-page.html',
})
export class AD14Page {
  readonly definition = AD14_SCREEN;
  private readonly route = inject(ActivatedRoute);
  private readonly api = inject(AD14ApiService);
  readonly lessonId = signal('');
  readonly draft = signal<LessonDraft | null>(null);

  readonly pageState = toSignal(
    this.route.paramMap.pipe(
      switchMap((params) => {
        const lessonId = params.get('lessonId');
        this.lessonId.set(lessonId ?? '');
        this.draft.set(null);

        if (!lessonId) {
          return of<AD14PageState>({ status: 'error', message: 'Thiếu mã bài học trên đường dẫn.' });
        }

        if (!isSignedInt64RouteId(lessonId)) {
          return of<AD14PageState>({
            status: 'error',
            message: 'Mã bài học phải là số nguyên signed 64-bit.',
          });
        }

        return this.api.getLesson(lessonId).pipe(
          map((envelope): AD14PageState => {
            if (
              envelope.success !== true
              || envelope.businessCode !== 'DESIGN_RESOURCE_RETRIEVED'
              || !isAdminLesson(envelope.data)
            ) {
              return { status: 'error', message: 'Study Server trả về dữ liệu bài học không hợp lệ.' };
            }
            const lesson = envelope.data;
            this.draft.set({
              title: lesson.title,
              content: lesson.content,
              order: String(lesson.order),
            });
            return { status: 'loaded', lesson };
          }),
          startWith(LOADING_STATE),
          catchError((error: unknown) => of(toPageError(error))),
        );
      }),
    ),
    { initialValue: LOADING_STATE },
  );

  readonly loadedLesson = computed(() => {
    const state = this.pageState();
    return state.status === 'loaded' ? state.lesson : null;
  });

  readonly errorMessage = computed(() => {
    const state = this.pageState();
    return state.status === 'error' ? state.message : null;
  });

  readonly isLoading = computed(() => this.pageState().status === 'loading');

  updateDraft(field: keyof LessonDraft, event: Event): void {
    const target = event.target;
    const current = this.draft();
    if (!current || !(target instanceof HTMLInputElement || target instanceof HTMLTextAreaElement)) return;
    this.draft.set({ ...current, [field]: target.value });
  }

  displayCourseId(value: number): string {
    return Number.isSafeInteger(value) ? String(value) : 'Không thể hiển thị chính xác';
  }
}

function toPageError(error: unknown): AD14PageState {
  if (error instanceof AdminSessionError && error.code === 'LOGIN_REQUIRED') {
    return { status: 'error', message: 'Phiên Admin không còn hiệu lực. Hãy đăng nhập lại.' };
  }
  if (error instanceof HttpErrorResponse) {
    if (error.status === 401) return { status: 'error', message: 'Phiên Admin đã hết hiệu lực. Hãy đăng nhập lại.' };
    if (error.status === 403) return { status: 'error', message: 'Tài khoản không được phép xem dữ liệu này.' };
    if (error.status === 404) return { status: 'error', message: 'Không tìm thấy dữ liệu được yêu cầu.' };
    if (error.status === 0) return { status: 'error', message: 'Không thể kết nối tới Study Server.' };
  }
  return { status: 'error', message: 'Study Server không thể tải dữ liệu lúc này.' };
}
