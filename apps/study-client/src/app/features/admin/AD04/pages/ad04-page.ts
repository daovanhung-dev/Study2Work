import { Component, inject, signal } from '@angular/core';
import { toSignal } from '@angular/core/rxjs-interop';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { catchError, map, of, startWith, switchMap } from 'rxjs';

import { StudyIcon } from '../../../../shared/ui/study-icon';
import type { AdminUserProfile } from '../../admin-api.models';
import { adminDataError } from '../../admin-screen-state';
import { AD04ApiService } from '../data-access/ad04-api.service';
import { AD04_SCREEN } from '../models/ad04-screen.model';

type AD04PageState =
  | { readonly status: 'loading' }
  | { readonly status: 'loaded'; readonly user: AdminUserProfile }
  | { readonly status: 'error'; readonly message: string };

const LOADING_STATE: AD04PageState = { status: 'loading' };

@Component({
  imports: [RouterLink, StudyIcon],
  selector: 'study-ad04-page',
  templateUrl: './ad04-page.html',
})
export class AD04Page {
  readonly definition = AD04_SCREEN;
  private readonly route = inject(ActivatedRoute);
  private readonly api = inject(AD04ApiService);
  readonly userId = signal('');

  readonly pageState = toSignal(
    this.route.paramMap.pipe(
      switchMap((params) => {
        const userId = params.get('userId');
        this.userId.set(userId ?? '');

        if (!userId) {
          return of<AD04PageState>({ status: 'error', message: 'Thiếu mã người dùng trên đường dẫn.' });
        }

        return this.api.getUser(userId).pipe(
          map((envelope): AD04PageState => {
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

function toPageError(error: unknown): AD04PageState {
  const state = adminDataError(error);
  return {
    status: 'error',
    message: state.status === 'error' && state.message
      ? state.message
      : 'Study Server không thể tải hồ sơ lúc này.',
  };
}
