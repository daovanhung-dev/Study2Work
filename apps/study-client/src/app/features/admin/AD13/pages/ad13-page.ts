import { Component, inject } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';

import { AD13ApiService } from '../data-access/ad13-api.service';
import { StudyIcon } from '../../../../shared/ui/study-icon';
import { adminRouteState, loadedFields } from '../../admin-screen-state';
import { renderLessonFields } from '../../admin-screen-renderers';
import type { AdminScreenField } from '../../../../shared/ui/admin-screen.model';

@Component({
  imports: [RouterLink, StudyIcon],
  selector: 'study-ad13-page',
  styleUrl: './ad13-page.css',
  templateUrl: './ad13-page.html',
})
export class AD13Page {
  private readonly route = inject(ActivatedRoute);
  private readonly api = inject(AD13ApiService);
  readonly viewState = adminRouteState(
    this.route,
    'lessonId',
    (lessonId) => this.api.getLesson(lessonId),
    (lesson) => loadedFields(renderLessonFields(lesson)),
  );

  get lessonFields(): readonly AdminScreenField[] {
    const values = new Map((this.viewState().fields ?? []).map((field) => [field.label, field.value]));
    return [
      { label: 'Tiêu đề bài học', value: values.get('Tiêu đề') ?? '—' },
      { label: 'Mã định danh bài học', value: values.get('Mã bài học') ?? '—' },
      { label: 'Khóa học trực thuộc', value: values.get('Mã khóa học') ?? '—' },
      { label: 'Thứ tự trong chương', value: values.get('Thứ tự hiển thị') ?? '—' },
      { label: 'Trạng thái phát hành', value: values.get('Trạng thái') ?? '—' },
      { label: 'URL video (metadata)', value: values.get('URL video') ?? '—' },
    ];
  }

  get lessonContent(): string {
    return this.viewState().fields?.find((field) => field.label === 'Nội dung bài học')?.value ?? '—';
  }
}
