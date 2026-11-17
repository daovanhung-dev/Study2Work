import { Component, OnInit, inject } from '@angular/core';

import { StudentApiService, type ApiId, type NotificationRecord, type StudentPage } from '../../data/student-api.service';
import { StudentApiState } from '../../data/student-api-state';

@Component({
  selector: 'study-st26-page',
  styleUrls: ['./st26-page.css', './st26-visual.css', '../../../../shared/ui/student-static-screen.css', '../../data/student-api-view.css'],
  templateUrl: './st26-page.html',
})
export class ST26Page implements OnInit {
  private readonly api = inject(StudentApiService);
  readonly notifications = new StudentApiState<StudentPage<NotificationRecord>>();
  readonly mutation = new StudentApiState<StudentPage<NotificationRecord>>();
  activeFilter: 'all' | 'unread' = 'all';

  ngOnInit(): void {
    this.reloadNotifications();
  }

  reloadNotifications(): void {
    const options = this.activeFilter === 'unread' ? { unreadOnly: true, page: 1 } : { page: 1 };
    this.notifications.load(this.api.getNotifications(options));
  }

  setFilter(filter: 'all' | 'unread'): void {
    if (filter === this.activeFilter || this.filtersDisabled) return;
    this.activeFilter = filter;
    this.reloadNotifications();
  }

  get filtersDisabled(): boolean {
    return this.notifications.status() === 'loading' || this.mutation.status() === 'loading';
  }

  markRead(notificationId: ApiId): void {
    if (this.mutation.status() === 'loading') return;
    this.mutation.load(this.api.markNotificationRead(String(notificationId)), () => this.reloadNotifications());
  }

  markAllRead(): void {
    if (this.mutation.status() === 'loading') return;
    this.mutation.load(this.api.markAllNotificationsRead(), () => this.reloadNotifications());
  }
}
