import { Routes } from '@angular/router';

import { MentorLayout } from '../../layouts/mentor/mentor-layout';
import { ME06Page } from './ME06/pages/me06-page';
import { ME07Page } from './ME07/pages/me07-page';
import { ME08Page } from './ME08/pages/me08-page';
import { ME09Page } from './ME09/pages/me09-page';
import { ME10Page } from './ME10/pages/me10-page';
import { ME11Page } from './ME11/pages/me11-page';
import { ME12Page } from './ME12/pages/me12-page';
import { ME13Page } from './ME13/pages/me13-page';
import { ME14Page } from './ME14/pages/me14-page';
import { ME15Page } from './ME15/pages/me15-page';
import { ME16Page } from './ME16/pages/me16-page';
import { ME17Page } from './ME17/pages/me17-page';
import { ME18Page } from './ME18/pages/me18-page';

export const mentorRoutes: Routes = [
  {
    path: '',
    component: MentorLayout,
    children: [
      {
        path: 'courses/:courseId/content',
        component: ME06Page,
      },
      {
        path: 'courses/:courseId/content/new',
        component: ME07Page,
      },
      {
        path: 'courses/:courseId/content/:contentId',
        component: ME07Page,
      },
      {
        path: 'content/:contentId/actions',
        component: ME08Page,
      },
      {
        path: 'submissions',
        component: ME09Page,
      },
      {
        path: 'submissions/:submissionId',
        component: ME10Page,
      },
      {
        path: 'support',
        component: ME11Page,
      },
      {
        path: 'support/:requestId',
        component: ME12Page,
      },
      {
        path: 'notifications/recipients',
        component: ME13Page,
      },
      {
        path: 'notifications/create',
        component: ME14Page,
      },
      {
        path: 'notifications/status',
        component: ME15Page,
      },
      {
        path: 'notifications/:notificationId/status',
        component: ME15Page,
      },
      {
        path: 'courses/:courseId/progress',
        component: ME16Page,
      },
      {
        path: 'courses/:courseId/students/:studentId/progress',
        component: ME17Page,
      },
      {
        path: 'courses/:courseId/analytics',
        component: ME18Page,
      },
    ],
  },
];
