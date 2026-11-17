import { HttpErrorResponse } from '@angular/common/http';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { StudentProfileEditService } from '../data-access/ST-03-profile-edit.service';
import type {
  StudentProfileEditDto,
  StudentProfileEditState,
} from '../models/ST-03-profile-edit.models';
import {
  ChangeDetectionStrategy,
  Component,
  DestroyRef,
  OnInit,
  inject,
  signal,
} from '@angular/core';
import { StudentProfileEditView } from '../ui/ST-03-profile-edit-view';

@Component({
  selector: 'study-student-profile-edit-page',
  imports: [StudentProfileEditView],
  templateUrl: './ST-03-profile-edit-page.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class StudentProfileEditPage implements OnInit {
  private readonly service = inject(StudentProfileEditService);
  private readonly destroyRef = inject(DestroyRef);
  readonly profile = signal<StudentProfileEditDto | null>(null);
  readonly state = signal<StudentProfileEditState>('loading');
  ngOnInit(): void {
    this.load();
  }
  load(): void {
    if (this.state() === 'loading' && this.requested) return;
    this.requested = true;
    this.profile.set(null);
    this.state.set('loading');
    this.service
      .getProfile()
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: (profile) => {
          this.profile.set(profile);
          this.state.set('ready');
        },
        error: (error: unknown) =>
          this.state.set(
            error instanceof HttpErrorResponse
              ? error.status === 401
                ? 'unauthorized'
                : error.status === 403
                  ? 'forbidden'
                  : 'error'
              : 'error',
          ),
      });
  }
  private requested = false;
}
