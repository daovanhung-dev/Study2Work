import { Router } from '@angular/router';
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
  readonly state = inject(NotFoundService).read(
    this.router.getCurrentNavigation()?.extras.state?.['httpError'],
  );
}
