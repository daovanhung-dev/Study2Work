import { Routes } from '@angular/router';

import { SharedLayout } from '../../layouts/shared/shared-layout';

export const sharedRoutes: Routes = [
  {
    path: '',
    component: SharedLayout,
    children: [
      {
        path: '',
        pathMatch: 'full',
        loadComponent: () => import('./SH01/pages/SH-01-landing-page').then((m) => m.GuestLandingPage),
      },
      {
        path: 'login',
        loadComponent: () => import('./SH02/pages/SH-02-login-page').then((m) => m.LoginPage),
      },
      {
        path: 'register/verification',
        loadComponent: () => import('./SH04/pages/SH-04-verification-page').then((m) => m.VerificationPage),
      },
      {
        path: 'register',
        loadComponent: () => import('./SH03/pages/SH-03-register-page').then((m) => m.RegisterPage),
      },
      {
        path: 'forbidden',
        loadComponent: () => import('./SH05/pages/SH-05-forbidden-page').then((m) => m.SystemForbiddenPage),
      },
      {
        path: 'not-found',
        loadComponent: () => import('./SH06/pages/SH-06-not-found-page').then((m) => m.SystemNotFoundPage),
      },
      {
        path: 'operations/:operationId',
        loadComponent: () => import('./SH07/pages/SH-07-operations-page').then((m) => m.SystemOperationsPage),
      },
    ],
  },
];
