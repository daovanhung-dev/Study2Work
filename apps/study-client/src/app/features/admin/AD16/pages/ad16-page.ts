import { Component, inject } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';

import { StudyIcon } from '../../../../shared/ui/study-icon';
import { AD16_SCREEN } from '../models/ad16-screen.model';

type DraftField = 'titleDraft' | 'durationDraft' | 'passingScoreDraft';

@Component({
  imports: [RouterLink, StudyIcon],
  selector: 'study-ad16-page',
  templateUrl: './ad16-page.html',
})
export class AD16Page {
  readonly definition = AD16_SCREEN;
  private readonly route = inject(ActivatedRoute);
  readonly quizId = this.route.snapshot.paramMap.get('quizId');

  titleDraft = '';
  durationDraft = '';
  passingScoreDraft = '';

  get isEditMode(): boolean {
    return this.quizId !== null;
  }

  updateDraft(field: DraftField, event: Event): void {
    if (this.isEditMode || !(event.target instanceof HTMLInputElement)) return;
    this[field] = event.target.value;
  }
}
