import { Component, inject } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';

import { AD07ApiService } from '../data-access/ad07-api.service';
import { StudyIcon } from '../../../../shared/ui/study-icon';
import { adminRouteState, loadedFields } from '../../admin-screen-state';
import { renderCourseFields } from '../../admin-screen-renderers';
import type { AdminScreenField } from '../../../../shared/ui/admin-screen.model';

@Component({
  imports: [RouterLink, StudyIcon],
  selector: 'study-ad07-page',
  styleUrl: './ad07-page.css',
  templateUrl: './ad07-page.html',
})
export class AD07Page {
  private readonly route = inject(ActivatedRoute);
  private readonly api = inject(AD07ApiService);
  readonly viewState = adminRouteState(
    this.route,
    'courseId',
    (courseId) => this.api.getCourse(courseId),
    (page) => page.items[0]
      ? loadedFields(renderCourseFields(page.items[0]))
      : { status: 'error', message: 'API #74 không trả khóa học cho mã đã yêu cầu.' },
  );

  get courseFields(): readonly AdminScreenField[] {
    const values = new Map((this.viewState().fields ?? []).map((field) => [field.label, field.value]));
    return [
      { label: 'Tên khóa học', value: values.get('Tên khóa học') ?? '—' },
      { label: 'Mã khóa học', value: values.get('Mã khóa học') ?? '—' },
      { label: 'Giảng viên phụ trách', value: values.get('Chủ khóa học') ?? '—' },
      { label: 'Học phí', value: values.get('Giá') ?? '—' },
      { label: 'Trạng thái phát hành', value: values.get('Trạng thái') ?? '—' },
      { label: 'URL ảnh bìa', value: values.get('Ảnh đại diện') ?? '—' },
    ];
  }

  get description(): string {
    return this.viewState().fields?.find((field) => field.label === 'Mô tả')?.value ?? '—';
  }
}
