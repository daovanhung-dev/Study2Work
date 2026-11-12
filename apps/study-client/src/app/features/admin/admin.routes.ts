import { Routes } from '@angular/router';

import { AdminLayout } from '../../layouts/admin/admin-layout';
import { AD01Page } from './AD01/pages/ad01-page';
import { AD02Page } from './AD02/pages/ad02-page';

export const adminRoutes: Routes = [
  {
    path: '',
    component: AdminLayout,
    children: [
      {
        path: '',
        pathMatch: 'full',
        component: AD01Page,
      },
      {
        path: 'users',
        component: AD02Page,
      },
    ],
  },
];
