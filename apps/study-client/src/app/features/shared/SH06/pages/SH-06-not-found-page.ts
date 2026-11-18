import { Router } from '@angular/router';
import { toSignal } from '@angular/core/rxjs-interop';
import { catchError, map, of } from 'rxjs';
import { LandingApi } from '../../SH01/data-access/SH-01-landing.service';
import type { Course } from '../../SH01/models/SH-01-landing.models';
import { NotFoundService } from '../data-access/SH-06-not-found.service';
import { ChangeDetectionStrategy, Component, inject } from '@angular/core';
import { SystemNotFoundView } from '../ui/SH-06-not-found-view';

@Component({
  selector: 'study-system-not-found-page',
  imports: [SystemNotFoundView],
  templateUrl: './SH-06-not-found-page.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class SystemNotFoundPage {
  private readonly router = inject(Router);
  private readonly landingApi = inject(LandingApi);
  readonly courses = toSignal<Course[] | null>(
    this.landingApi.getCourses().pipe(
      map((items) => items.slice(0, 3)),
      catchError(() => of([] as Course[])),
    ),
    { initialValue: null },
  );
  readonly state = inject(NotFoundService).read(
    this.router.getCurrentNavigation()?.extras.state?.['httpError'],
  );
}
