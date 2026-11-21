import { Component, Input, inject, signal } from '@angular/core';
import { Router, RouterLink, RouterLinkActive } from '@angular/router';

import { StudyIcon } from '../../../../shared/ui/study-icon';

@Component({
  imports: [RouterLink, RouterLinkActive, StudyIcon],
  selector: 'study-guest-site-layout',
  styleUrl: './guest-site-layout.css',
  templateUrl: './guest-site-layout.html',
})
export class GuestSiteLayout {
  @Input() showSearch = false;

  private readonly router = inject(Router);
  readonly searchQuery = signal('');

  onSearchInput(event: Event): void {
    this.searchQuery.set((event.currentTarget as HTMLInputElement).value);
  }

  submitSearch(event: Event): void {
    event.preventDefault();
    const query = this.searchQuery().trim();
    if (!query) return;

    void this.router.navigate(['/courses/search'], { queryParams: { q: query } });
  }
}
