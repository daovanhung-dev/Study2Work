import { Routes } from '@angular/router';

import { GuestLayout } from '../../layouts/guest/guest-layout';
import { GS01Page } from './GS01/pages/gs01-page';
import { GS02Page } from './GS02/pages/gs02-page';
import { GS03Page } from './GS03/pages/gs03-page';
import { GS07Page } from './GS07/pages/gs07-page';

export const guestRoutes: Routes = [
  {
    path: '',
    component: GuestLayout,
    children: [
      { path: 'search', component: GS02Page },
      { path: ':courseId', component: GS03Page },
      { path: '', component: GS01Page },
    ],
  },
];

export const guestResourceRoutes: Routes = [
  {
    path: '',
    component: GuestLayout,
    children: [{ path: '', component: GS07Page }],
  },
];
