import { Component } from '@angular/core';
import { Router, RouterLink, RouterOutlet } from '@angular/router';

import { StudyIcon } from '../../shared/ui/study-icon';

@Component({
  imports: [RouterLink, RouterOutlet, StudyIcon],
  selector: 'study-admin-layout',
  styleUrl: './admin-layout.css',
  templateUrl: './admin-layout.html',
})
export class AdminLayout {
  constructor(readonly router: Router) {}

  get isUsersRoute(): boolean {
    return this.router.url.startsWith('/admin/users');
  }

  get isAdminHome(): boolean {
    return this.router.url === '/admin' || this.router.url === '/admin/';
  }
}
