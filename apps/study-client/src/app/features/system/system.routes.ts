import { Routes } from '@angular/router';

import { SystemLayout } from '../../layouts/system/system-layout';
import { SystemReadinessPage } from './pages/system-readiness-page';

export const systemRoutes: Routes = [
  {
    path: '',
    component: SystemLayout,
    children: [
      {
        path: '',
        pathMatch: 'full',
        component: SystemReadinessPage,
      },
    ],
  },
];
