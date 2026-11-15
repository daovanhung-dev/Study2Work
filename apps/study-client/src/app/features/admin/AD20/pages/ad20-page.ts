import { Component, signal } from '@angular/core';
import { RouterLink } from '@angular/router';

import { StudyIcon } from '../../../../shared/ui/study-icon';
import { AD20_SCREEN } from '../models/ad20-screen.model';

@Component({
  imports: [RouterLink, StudyIcon],
  selector: 'study-ad20-page',
  templateUrl: './ad20-page.html',
})
export class AD20Page {
  readonly definition = AD20_SCREEN;
  readonly title = signal('');
  readonly content = signal('');

  updateTitle(event: Event): void {
    if (event.target instanceof HTMLInputElement) {
      this.title.set(event.target.value);
    }
  }

  updateContent(event: Event): void {
    if (event.target instanceof HTMLTextAreaElement) {
      this.content.set(event.target.value);
    }
  }
}
