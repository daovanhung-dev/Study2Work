import { Component, inject, signal } from '@angular/core';
import { Router } from '@angular/router';

import { StudyIcon } from '../../../../shared/ui/study-icon';

@Component({
  imports: [StudyIcon],
  selector: 'study-gs01-hero',
  styleUrl: './gs01-hero.css',
  templateUrl: './gs01-hero.html',
})
export class GS01Hero {
  private readonly router = inject(Router);
  readonly query = signal('');

  onInput(event: Event): void {
    this.query.set((event.currentTarget as HTMLInputElement).value);
  }

  submit(event: Event): void {
    event.preventDefault();
    const query = this.query().trim();
    if (!query) return;

    void this.router.navigate(['/courses/search'], { queryParams: { q: query } });
  }
}
