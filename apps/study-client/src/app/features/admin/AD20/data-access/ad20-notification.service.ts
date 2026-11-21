import { HttpParams } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';

import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import { AdminApiService } from '../../../../core/http/admin-api.service';
import type { AdminPage, AdminUserProfile } from '../../admin-api.models';

export interface AD20NotificationAcceptedData {
  readonly id: number;
  readonly title: string;
  readonly content: string;
  readonly channels: readonly ('EMAIL' | 'PUSH')[];
  readonly status: 'FAILED' | 'QUEUED' | 'SENT';
  readonly created_at: string;
}

@Injectable({ providedIn: 'root' })
export class AD20NotificationService {
  private readonly api = inject(AdminApiService);

  getRecipients(page: number) {
    return this.api.get<AdminPage<AdminUserProfile>>(STUDY_SERVER_APIS.API_068, {
      params: new HttpParams().set('page', String(page)),
    });
  }

  createNotification(request: {
    recipients: readonly number[];
    title: string;
    content: string;
    channels: readonly ('PUSH' | 'EMAIL')[];
  }) {
    return this.api.postWithResponse<AD20NotificationAcceptedData>(STUDY_SERVER_APIS.API_093, {
      body: request,
    });
  }
}
