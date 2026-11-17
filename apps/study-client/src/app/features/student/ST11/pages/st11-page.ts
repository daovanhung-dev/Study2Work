import { Component, OnInit, inject } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

import { StudentApiService, type LessonRecord, type ResourceRecord } from '../../data/student-api.service';
import { StudentApiState } from '../../data/student-api-state';

@Component({
  selector: 'study-st11-page',
  styleUrls: ['./st11-page.css', '../../data/student-api-view.css'],
  templateUrl: './st11-page.html',
})
export class ST11Page implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);
  private readonly api = inject(StudentApiService);

  readonly lesson = new StudentApiState<LessonRecord>();
  readonly resources = new StudentApiState<ResourceRecord[]>();
  readonly nextLesson = new StudentApiState<LessonRecord | null>();
  readonly progress = new StudentApiState<LessonRecord>();
  lessonId = '';

  ngOnInit(): void {
    this.lessonId = this.route.snapshot.paramMap.get('lessonId') ?? '';
    if (!this.lessonId) return;
    this.lesson.load(this.api.getLesson(this.lessonId));
    this.resources.load(this.api.getLessonResources(this.lessonId));
  }

  saveProgress(event: Event, completed = false): void {
    const video = event.currentTarget;
    if (!(video instanceof HTMLVideoElement) || !this.lessonId) return;

    const position = Math.floor(video.currentTime);
    const duration = Number.isFinite(video.duration) && video.duration > 0 ? video.duration : 0;
    const percent = completed || duration === 0 ? (completed ? 100 : 0) : Math.min(100, Math.round((video.currentTime / duration) * 100));
    this.progress.load(
      this.api.saveLessonProgress(this.lessonId, { position, percent, completed }),
    );
  }

  loadNextLesson(): void {
    if (!this.lessonId) return;
    this.nextLesson.load(this.api.getNextLesson(this.lessonId), (lesson) => {
      if (lesson?.id !== undefined && lesson?.id !== null) {
        void this.router.navigate(['/student/lessons', lesson.id]);
      }
    });
  }
}
