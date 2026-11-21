import { Routes } from '@angular/router';

import { SharedLayout } from '../../layouts/shared/shared-layout';
import { SH01Page } from './SH01/pages/sh01-page';
import { SH02Page } from './SH02/pages/sh02-page';
import { SH03Page } from './SH03/pages/sh03-page';
import { SH04Page } from './SH04/pages/sh04-page';
import { SH05Page } from './SH05/pages/sh05-page';
import { SH06Page } from './SH06/pages/sh06-page';
import { SH07Page } from './SH07/pages/sh07-page';

export const sharedRoutes: Routes = [
  {
    path: '',
    component: SharedLayout,
    children: [
      {
        path: 'forbidden',
        component: SH05Page,
      },
      {
        path: 'not-found',
        component: SH06Page,
      },
      {
        path: 'operations/:operationId',
        component: SH07Page,
      },
      {
        path: '',
        pathMatch: 'full',
        component: SH01Page,
      },
      {
        path: 'login',
        component: SH02Page,
        data: { screenId: 'SH-02', apiIds: [3, 4] },
      },
      {
        path: 'register/verification',
        component: SH04Page,
      },
      {
        path: 'register',
        component: SH03Page,
      },
    ],
  },
];
