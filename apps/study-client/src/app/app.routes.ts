import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: 'admin',
    loadChildren: () => import('./features/admin/admin.routes').then((m) => m.adminRoutes),
  },
  {
    path: 'mentor',
    loadChildren: () => import('./features/mentor/mentor.route').then((m) => m.mentorRoutes),
  },
  {
    path: '',
    pathMatch: 'full',
    loadChildren: () => import('./features/system/system.routes').then((m) => m.systemRoutes),
  },
];
