import { Component, inject } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { ActivatedRoute, NavigationEnd, Router, RouterOutlet } from '@angular/router';
import { filter } from 'rxjs';

type StudentShellMode = 'legacy' | 'portal' | 'exam' | 'blank';

@Component({
  imports: [RouterOutlet],
  selector: 'study-student-layout',
  styleUrl: './student-layout.css',
  templateUrl: './student-layout.html',
})
export class StudentLayout {
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);

  shellMode: StudentShellMode = 'legacy';

  constructor() {
    this.router.events
      .pipe(
        filter((event): event is NavigationEnd => event instanceof NavigationEnd),
        takeUntilDestroyed(),
      )
      .subscribe(() => this.setShellMode());
  }

  setShellMode(): void {
    const shell = this.route.firstChild?.snapshot.data['shell'];
    this.shellMode = shell === 'portal' || shell === 'exam' || shell === 'blank' ? shell : 'legacy';
  }
}
