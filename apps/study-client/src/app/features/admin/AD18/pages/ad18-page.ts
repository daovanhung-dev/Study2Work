import { Component, DestroyRef, inject, signal } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { ActivatedRoute, RouterLink } from '@angular/router';

import { StudyIcon } from '../../../../shared/ui/study-icon';
import { AD18_SCREEN } from '../models/ad18-screen.model';

@Component({
  imports: [RouterLink, StudyIcon],
  selector: 'study-ad18-page',
  templateUrl: './ad18-page.html',
})
export class AD18Page {
  readonly definition = AD18_SCREEN;
  private readonly route = inject(ActivatedRoute);
  private readonly destroyRef = inject(DestroyRef);
  readonly quizId = signal(this.route.snapshot.paramMap.get('quizId') ?? '—');

  constructor() {
    this.route.paramMap
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe((params) => this.quizId.set(params.get('quizId') ?? '—'));
  }
}
