import { Component, inject, signal } from '@angular/core';
import { toSignal } from '@angular/core/rxjs-interop';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { catchError, map, of, startWith, switchMap } from 'rxjs';

import { StudyIcon } from '../../../../shared/ui/study-icon';
import type { AdminUserProfile } from '../../admin-api.models';
import { adminDataError } from '../../admin-screen-state';
import { AD05ApiService } from '../data-access/ad05-api.service';
import { AD05_SCREEN } from '../models/ad05-screen.model';

type AD05PageState =
  | { readonly status: 'loading' }
  | { readonly status: 'loaded'; readonly user: AdminUserProfile }
  | { readonly status: 'error'; readonly message: string };

const LOADING_STATE: AD05PageState = { status: 'loading' };

@Component({
  imports: [RouterLink, StudyIcon],
  selector: 'study-ad05-page',
  templateUrl: './ad05-page.html',
})
export class AD05Page {
  readonly definition = AD05_SCREEN;
  private readonly route = inject(ActivatedRoute);
  private readonly api = inject(AD05ApiService);
  readonly userId = signal('');

  readonly pageState = toSignal(
    this.route.paramMap.pipe(
      switchMap((params) => {
        const userId = params.get('userId');
        this.userId.set(userId ?? '');

        if (!userId) {
          return of<AD05PageState>({ status: 'error', message: 'Thiếu mã người dùng trên đường dẫn.' });
        }

        return this.api.getUser(userId).pipe(
          map((envelope): AD05PageState => {
            if (!envelope.success) {
              return { status: 'error', message: 'Study Server không thể tải hồ sơ lúc này.' };
            }
            return { status: 'loaded', user: envelope.data };
          }),
          startWith(LOADING_STATE),
          catchError((error: unknown) => of(toPageError(error))),
        );
      }),
    ),
    { initialValue: LOADING_STATE },
  );
}

function toPageError(error: unknown): AD05PageState {
  const state = adminDataError(error);
  return {
    status: 'error',
    message: state.status === 'error' && state.message
      ? state.message
      : 'Study Server không thể tải hồ sơ lúc này.',
  };
}
