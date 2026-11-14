import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: 'admin',
    loadChildren: () => import('./features/admin/admin.route').then((m) => m.adminRoutes),
  },
  {
    path: 'readiness',
    loadChildren: () => import('./features/system/system.route').then((m) => m.systemRoutes),
  },
  {
    path: '',
    loadChildren: () => import('./features/shared/shared.route').then((m) => m.sharedRoutes),
  },
  { path: '**', redirectTo: 'not-found' },
];
