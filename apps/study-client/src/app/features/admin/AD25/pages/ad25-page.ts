import { Component, signal } from '@angular/core';
import { RouterLink } from '@angular/router';

import { StudyIcon } from '../../../../shared/ui/study-icon';
import { AD25_SCREEN } from '../models/ad25-screen.model';

@Component({
  imports: [RouterLink, StudyIcon],
  selector: 'study-ad25-page',
  templateUrl: './ad25-page.html',
})
export class AD25Page {
  readonly definition = AD25_SCREEN;
  readonly selectedFormat = signal<'csv' | 'xlsx' | 'pdf'>('csv');
  readonly selectedScopes = signal({ course: true, learner: true, impact: false });
  readonly selectedPeriod = signal<'week' | 'month' | 'custom'>('month');

  setFormat(value: 'csv' | 'xlsx' | 'pdf'): void {
    this.selectedFormat.set(value);
  }

  setScope(scope: 'course' | 'learner' | 'impact', checked: boolean): void {
    this.selectedScopes.update((current) => ({ ...current, [scope]: checked }));
  }

  setPeriod(value: 'week' | 'month' | 'custom'): void {
    this.selectedPeriod.set(value);
  }
}
