import { Component, OnInit, inject } from '@angular/core';

import { StudentApiService, type AchievementRecord } from '../../data/student-api.service';
import { StudentApiState } from '../../data/student-api-state';

@Component({
  selector: 'study-st22-page',
  styleUrls: ['./st22-page.css', '../../../../shared/ui/student-static-screen.css', '../../data/student-api-view.css'],
  templateUrl: './st22-page.html',
})
export class ST22Page implements OnInit {
  private readonly api = inject(StudentApiService);
  readonly achievements = new StudentApiState<{ items: AchievementRecord[] }>();

  ngOnInit(): void {
    this.achievements.load(this.api.getAchievements());
  }
}
