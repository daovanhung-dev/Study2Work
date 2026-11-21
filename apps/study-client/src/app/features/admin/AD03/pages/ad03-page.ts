import { Component, inject } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';

import { AD03ApiService } from '../data-access/ad03-api.service';
import { StudyIcon } from '../../../../shared/ui/study-icon';
import { AD03_SCREEN } from '../models/ad03-screen.model';
import { adminRouteState, isSignedInt64RouteId, loadedFields } from '../../admin-screen-state';
import { renderUserFields } from '../../admin-screen-renderers';
import type { AdminScreenField } from '../../../../shared/ui/admin-screen.model';

@Component({
  imports: [RouterLink, StudyIcon],
  selector: 'study-ad03-page',
  styleUrl: './ad03-page.css',
  templateUrl: './ad03-page.html',
})
export class AD03Page {
  readonly definition = AD03_SCREEN;
  private readonly route = inject(ActivatedRoute);
  private readonly api = inject(AD03ApiService);
  readonly viewState = adminRouteState(
    this.route,
    'userId',
    (userId) => this.api.getUser(userId),
    (user) => loadedFields(renderUserFields(user)),
    isSignedInt64RouteId,
    'Mã người dùng phải là số nguyên signed 64-bit.',
    'DESIGN_RESOURCE_RETRIEVED',
  );

  get apiStateLabel(): string {
    switch (this.viewState().status) {
      case 'loading':
        return 'Đang tải';
      case 'loaded':
        return 'Đã tải';
      case 'error':
        return 'Lỗi tải';
    }
  }

  get identityFields(): readonly AdminScreenField[] {
    const values = new Map((this.viewState().fields ?? []).map((field) => [field.label, field.value]));
    return [
      { label: 'Họ và tên', value: values.get('Họ và tên') ?? '—' },
      { label: 'Địa chỉ Email', value: values.get('Email') ?? '—' },
      { label: 'Mã định danh người dùng', value: values.get('Mã người dùng') ?? '—' },
      { label: 'Số điện thoại', value: values.get('Số điện thoại') ?? '—' },
      { label: 'Vai trò hệ thống', value: values.get('Vai trò') ?? '—' },
      { label: 'Trạng thái tài khoản', value: values.get('Trạng thái') ?? '—' },
    ];
  }
}
