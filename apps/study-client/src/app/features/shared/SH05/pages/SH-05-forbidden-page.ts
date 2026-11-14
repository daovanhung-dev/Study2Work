import { Router } from '@angular/router';
import { AccessFailureService } from '../data-access/SH-05-forbidden.service';
import { ChangeDetectionStrategy, Component, inject } from '@angular/core';
import { SystemForbiddenView } from '../ui/SH-05-forbidden-view';

@Component({
  selector: 'study-system-forbidden-page',
  imports: [SystemForbiddenView],
  templateUrl: './SH-05-forbidden-page.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class SystemForbiddenPage {
  private readonly router = inject(Router);
  readonly state = inject(AccessFailureService).read(
    this.router.getCurrentNavigation()?.extras.state?.['httpError'],
  );
}
