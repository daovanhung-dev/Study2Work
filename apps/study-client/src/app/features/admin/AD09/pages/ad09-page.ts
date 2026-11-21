import { Component, inject, signal } from '@angular/core';
import { toSignal } from '@angular/core/rxjs-interop';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { catchError, map, of, startWith, switchMap } from 'rxjs';

import { StudyIcon } from '../../../../shared/ui/study-icon';
import { isAdminCourseDetailPage } from '../../admin-api-guards';
import type { AdminCourse } from '../../admin-api.models';
import { adminDataError, isSignedInt64RouteId } from '../../admin-screen-state';
import { AD09ApiService } from '../data-access/ad09-api.service';
import { AD09_SCREEN } from '../models/ad09-screen.model';

type AD09PageState =
  | { readonly status: 'loading' }
  | { readonly status: 'loaded'; readonly course: AdminCourse }
  | { readonly status: 'error'; readonly message: string };

const LOADING_STATE: AD09PageState = { status: 'loading' };

@Component({
  imports: [RouterLink, StudyIcon],
  selector: 'study-ad09-page',
  templateUrl: './ad09-page.html',
})
export class AD09Page {
  readonly definition = AD09_SCREEN;
  private readonly route = inject(ActivatedRoute);
  private readonly api = inject(AD09ApiService);
  readonly courseId = signal('');
  readonly isCourseIdValid = signal(false);

  readonly pageState = toSignal(
    this.route.paramMap.pipe(
      switchMap((params) => {
        const courseId = params.get('courseId');
        this.courseId.set(courseId ?? '');

        if (!courseId) {
          this.isCourseIdValid.set(false);
          return of<AD09PageState>({ status: 'error', message: 'Thiếu mã khóa học trên đường dẫn.' });
        }

        if (!isSignedInt64RouteId(courseId)) {
          this.isCourseIdValid.set(false);
          return of<AD09PageState>({ status: 'error', message: 'Mã khóa học phải là số nguyên signed 64-bit.' });
        }

        this.isCourseIdValid.set(true);
        return this.api.getCourse(courseId).pipe(
          map((envelope): AD09PageState => {
            if (
              envelope.success !== true
              || envelope.businessCode !== 'DESIGN_RESOURCE_RETRIEVED'
            ) {
              return { status: 'error', message: 'Study Server trả về dữ liệu khóa học không hợp lệ.' };
            }
            const page = envelope.data;
            return isAdminCourseDetailPage(page)
              ? { status: 'loaded', course: page.items[0] }
              : { status: 'error', message: 'API #74 không trả khóa học cho mã đã yêu cầu.' };
          }),
          startWith(LOADING_STATE),
          catchError((error: unknown) => of(toPageError(error))),
        );
      }),
    ),
    { initialValue: LOADING_STATE },
  );
}

function toPageError(error: unknown): AD09PageState {
  const state = adminDataError(error);
  return {
    status: 'error',
    message: state.status === 'error' && state.message
      ? state.message
      : 'Study Server không thể tải dữ liệu lúc này.',
  };
}
