import { ChangeDetectionStrategy, Component, OnInit, inject, signal } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { ActivatedRoute, NavigationEnd, Router, RouterLink, RouterOutlet } from '@angular/router';
import { filter } from 'rxjs';

type StudentSection = 'overview' | 'checkout' | 'myCourses' | 'profile';

@Component({
  selector: 'study-student-layout',
  imports: [RouterLink, RouterOutlet],
  templateUrl: './student-layout.html',
  styleUrl: './student-layout.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class StudentLayout implements OnInit {
  private readonly route = inject(ActivatedRoute);
  readonly section = signal<StudentSection>('overview');
  readonly currentYear = new Date().getFullYear();
  mobileNavOpen = false;

  constructor() {
    inject(Router)
      .events.pipe(
        filter((event): event is NavigationEnd => event instanceof NavigationEnd),
        takeUntilDestroyed(),
      )
      .subscribe(() => this.updateSection());
  }

  ngOnInit(): void {
    this.updateSection();
  }

  closeMenu(): void {
    this.mobileNavOpen = false;
  }

  private updateSection(): void {
    const section = this.route.firstChild?.snapshot.data['section'];
    if (
      section === 'overview' ||
      section === 'checkout' ||
      section === 'myCourses' ||
      section === 'profile'
    ) {
      this.section.set(section);
    }
  }
}
