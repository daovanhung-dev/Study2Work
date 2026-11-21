import { Component, DestroyRef, computed, inject, signal } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { ActivatedRoute, RouterLink } from '@angular/router';

import { StudyIcon } from '../../../../shared/ui/study-icon';
import { AD18_SCREEN } from '../models/ad18-screen.model';

@Component({
  imports: [RouterLink, StudyIcon],
  selector: 'study-ad18-page',
  styleUrl: './ad18-page.css',
  templateUrl: './ad18-page.html',
})
export class AD18Page {
  readonly definition = AD18_SCREEN;
  private readonly route = inject(ActivatedRoute);
  private readonly destroyRef = inject(DestroyRef);
  readonly quizId = signal(this.route.snapshot.paramMap.get('quizId') ?? '—');
  readonly isQuizIdValid = computed(() => isPositiveSignedInt64(this.quizId()));

  constructor() {
    this.route.paramMap
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe((params) => this.quizId.set(params.get('quizId') ?? '—'));
  }
}

function isPositiveSignedInt64(value: string): boolean {
  const match = /^[0-9]+$/.exec(value);
  if (match?.[0] !== value || value.length > 19 || !/[1-9]/.test(value)) {
    return false;
  }

  const max = '9223372036854775807';
  return value.length < max.length || (value.length === max.length && value <= max);
}
