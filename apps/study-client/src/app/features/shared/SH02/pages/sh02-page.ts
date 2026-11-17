import { Component, signal } from '@angular/core';

import { StudyIcon } from '../../../../shared/ui/study-icon';

@Component({
  imports: [StudyIcon],
  selector: 'study-sh02-page',
  templateUrl: './sh02-page.html',
  styleUrl: './sh02-page.css',
})
export class SH02Page {
  readonly passwordVisible = signal(false);

  togglePasswordVisibility(): void {
    this.passwordVisible.update((visible) => !visible);
  }

  preventSubmit(event: SubmitEvent): void {
    event.preventDefault();
  }
}
