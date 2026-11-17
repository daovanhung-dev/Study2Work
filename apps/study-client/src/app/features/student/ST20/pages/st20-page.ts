import { Component, OnInit, inject } from '@angular/core';

import { StudentApiService, type AchievementRecord } from '../../data/student-api.service';
import { StudentApiState } from '../../data/student-api-state';

@Component({
  selector: 'study-st20-page',
  styleUrls: ['../../../../shared/ui/student-static-screen.css', '../../data/student-api-view.css'],
  templateUrl: './st20-page.html',
})
export class ST20Page implements OnInit {
  private readonly api = inject(StudentApiService);
  readonly progress = new StudentApiState<Record<string, unknown>>();
  readonly achievements = new StudentApiState<{ items: AchievementRecord[] }>();

  ngOnInit(): void {
    this.progress.load(this.api.getMyProgress());
    this.achievements.load(this.api.getAchievements());
  }
}
