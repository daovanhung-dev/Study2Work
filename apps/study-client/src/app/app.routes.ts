import { inject } from '@angular/core';
import { Router, Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    loadChildren: () => import('./features/shared/shared.route').then((m) => m.sharedRoutes),
  },
  {
    path: 'courses',
    loadChildren: () => import('./features/guest/guest.route').then((m) => m.guestRoutes),
  },
  {
    path: 'resources/:resourceId',
    loadChildren: () =>
      import('./features/guest/guest.route').then((m) => m.guestResourceRoutes),
  },
  {
    path: 'student',
    loadChildren: () => import('./features/student/student.route').then((m) => m.studentRoutes),
  },
  {
    path: 'mentor',
    loadChildren: () => import('./features/mentor/mentor.route').then((m) => m.mentorRoutes),
  },
  {
    path: 'admin',
    loadChildren: () => import('./features/admin/admin.routes').then((m) => m.adminRoutes),
  },
  {
    path: '**',
    redirectTo: () => inject(Router).createUrlTree(['/not-found']),
  },
];
