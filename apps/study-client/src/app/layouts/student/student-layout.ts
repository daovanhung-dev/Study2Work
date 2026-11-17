import { ChangeDetectionStrategy, Component, OnInit, inject, signal } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { ActivatedRoute, NavigationEnd, Router, RouterLink, RouterOutlet } from '@angular/router';
import { filter } from 'rxjs';

type StudentSection = 'overview' | 'checkout' | 'myCourses' | 'profile';
type StudentShellMode = 'legacy' | 'portal' | 'exam' | 'blank';

@Component({
  selector: 'study-student-layout',
  imports: [RouterLink, RouterOutlet],
  templateUrl: './student-layout.html',
  styleUrl: './student-layout.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class StudentLayout implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);

  shellMode: StudentShellMode = 'legacy';
  readonly section = signal<StudentSection | null>(null);
  readonly currentYear = new Date().getFullYear();
  mobileNavOpen = false;

  constructor() {
    this.router.events
      .pipe(
        filter((event): event is NavigationEnd => event instanceof NavigationEnd),
        takeUntilDestroyed(),
      )
      .subscribe(() => this.updateRouteState());
  }

  ngOnInit(): void {
    this.updateRouteState();
  }

  closeMenu(): void {
    this.mobileNavOpen = false;
  }

  setShellMode(): void {
    const shell = this.route.firstChild?.snapshot.data['shell'];
    this.shellMode = shell === 'portal' || shell === 'exam' || shell === 'blank' ? shell : 'legacy';
  }

  private updateRouteState(): void {
    this.setShellMode();
    const section = this.route.firstChild?.snapshot.data['section'];
    this.section.set(
      section === 'overview' ||
        section === 'checkout' ||
        section === 'myCourses' ||
        section === 'profile'
        ? section
        : null,
    );
  }
}
