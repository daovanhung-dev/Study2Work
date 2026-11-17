import { Component, computed, inject, signal } from '@angular/core';
import { toSignal } from '@angular/core/rxjs-interop';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { catchError, map, of, startWith, switchMap } from 'rxjs';

import { StudyIcon } from '../../../../shared/ui/study-icon';
import type { AdminCourse } from '../../admin-api.models';
import { adminDataError } from '../../admin-screen-state';
import { AD08ApiService } from '../data-access/ad08-api.service';
import { AD08_SCREEN } from '../models/ad08-screen.model';

interface CourseDraft {
  readonly title: string;
  readonly description: string;
  readonly price: string;
}

type AD08PageState =
  | { readonly status: 'loading' }
  | { readonly status: 'loaded'; readonly course: AdminCourse }
  | { readonly status: 'error'; readonly message: string };

const LOADING_STATE: AD08PageState = { status: 'loading' };

@Component({
  imports: [RouterLink, StudyIcon],
  selector: 'study-ad08-page',
  templateUrl: './ad08-page.html',
})
export class AD08Page {
  readonly definition = AD08_SCREEN;
  private readonly route = inject(ActivatedRoute);
  private readonly api = inject(AD08ApiService);
  readonly courseId = signal('');
  readonly draft = signal<CourseDraft | null>(null);

  readonly pageState = toSignal(
    this.route.paramMap.pipe(
      switchMap((params) => {
        const courseId = params.get('courseId');
        this.courseId.set(courseId ?? '');
        this.draft.set(null);

        if (!courseId) {
          return of<AD08PageState>({ status: 'error', message: 'Thiếu mã khóa học trên đường dẫn.' });
        }

        return this.api.getCourse(courseId).pipe(
          map((envelope): AD08PageState => {
            if (!envelope.success) {
              return { status: 'error', message: 'Study Server không thể tải dữ liệu lúc này.' };
            }
            const course = envelope.data.items[0];
            if (!course) {
              return { status: 'error', message: 'API #74 không trả khóa học cho mã đã yêu cầu.' };
            }
            this.draft.set({
              title: course.title,
              description: course.description ?? '',
              price: course.price,
            });
            return { status: 'loaded', course };
          }),
          startWith(LOADING_STATE),
          catchError((error: unknown) => of(toPageError(error))),
        );
      }),
    ),
    { initialValue: LOADING_STATE },
  );

  readonly isLoading = computed(() => this.pageState().status === 'loading');
  readonly errorMessage = computed(() => {
    const state = this.pageState();
    return state.status === 'error' ? state.message : null;
  });

  updateDraft(field: keyof CourseDraft, event: Event): void {
    const target = event.target;
    const current = this.draft();
    if (!current || !(target instanceof HTMLInputElement || target instanceof HTMLTextAreaElement)) return;
    this.draft.set({ ...current, [field]: target.value });
  }

}

function toPageError(error: unknown): AD08PageState {
  const state = adminDataError(error);
  return {
    status: 'error',
    message: state.status === 'error' && state.message
      ? state.message
      : 'Study Server không thể tải dữ liệu lúc này.',
  };
}
