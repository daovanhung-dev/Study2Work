import { HttpErrorResponse } from '@angular/common/http';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { StudentProfileService } from '../data-access/ST-02-profile.service';
import type { StudentProfileDto, StudentProfileState } from '../models/ST-02-profile.models';
import {
  ChangeDetectionStrategy,
  Component,
  DestroyRef,
  OnInit,
  inject,
  signal,
} from '@angular/core';
import { StudentProfileView } from '../ui/ST-02-profile-view';

@Component({
  selector: 'study-student-profile-page',
  imports: [StudentProfileView],
  templateUrl: './ST-02-profile-page.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class StudentProfilePage implements OnInit {
  private readonly service = inject(StudentProfileService);
  private readonly destroyRef = inject(DestroyRef);
  readonly profile = signal<StudentProfileDto | null>(null);
  readonly state = signal<StudentProfileState>('loading');
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
