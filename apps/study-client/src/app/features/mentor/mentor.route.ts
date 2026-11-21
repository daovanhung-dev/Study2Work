import { Routes } from '@angular/router';

import { MentorLayout } from '../../layouts/mentor/mentor-layout';
import { ME01Page } from './ME01/pages/me01-page';
import { ME02Page } from './ME02/pages/me02-page';
import { ME03Page } from './ME03/pages/me03-page';
import { blockME04DepartureDuringWrite, ME04Page } from './ME04/pages/me04-page';
import { ME05Page } from './ME05/pages/me05-page';
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
      { path: '', pathMatch: 'full', component: ME01Page, data: { screenId: 'ME-01', apiIds: [46, 54, 58] } },
      { path: 'courses', component: ME02Page, data: { screenId: 'ME-02', apiIds: [46] } },
      { path: 'courses/:courseId/lectures/new', component: ME04Page, canDeactivate: [blockME04DepartureDuringWrite], data: { screenId: 'ME-04', apiIds: [34, 46, 47] } },
      { path: 'lectures/:lectureId', component: ME05Page, data: { screenId: 'ME-05', apiIds: [48] } },
      { path: 'courses/:courseId/content', component: ME06Page, data: { screenId: 'ME-06', apiIds: [49] } },
      { path: 'courses/:courseId/content/new', component: ME07Page, data: { screenId: 'ME-07', apiIds: [49, 50, 51] } },
      { path: 'courses/:courseId/content/:contentId', component: ME07Page, data: { screenId: 'ME-07', apiIds: [49, 50, 51] } },
      { path: 'content/:contentId/actions', component: ME08Page, data: { screenId: 'ME-08', apiIds: [49, 52, 53] } },
      { path: 'submissions', component: ME09Page, data: { screenId: 'ME-09', apiIds: [54] } },
      { path: 'submissions/:submissionId', component: ME10Page, data: { screenId: 'ME-10', apiIds: [55, 56, 57] } },
      { path: 'support', component: ME11Page, data: { screenId: 'ME-11', apiIds: [58] } },
      { path: 'support/:requestId', component: ME12Page, data: { screenId: 'ME-12', apiIds: [59, 60, 61] } },
      { path: 'notifications/new/recipients', component: ME13Page, data: { screenId: 'ME-13', apiIds: [46, 62] } },
      { path: 'notifications/new', component: ME14Page, data: { screenId: 'ME-14', apiIds: [62, 63] } },
      { path: 'notifications/:notificationId/status', component: ME15Page, data: { screenId: 'ME-15', apiIds: [64] } },
      { path: 'courses/:courseId/students/:studentId/progress', component: ME17Page, data: { screenId: 'ME-17', apiIds: [67] } },
      { path: 'courses/:courseId/progress', component: ME16Page, data: { screenId: 'ME-16', apiIds: [65] } },
      { path: 'courses/:courseId/analytics', component: ME18Page, data: { screenId: 'ME-18', apiIds: [66] } },
      { path: 'courses/:courseId', component: ME03Page, data: { screenId: 'ME-03', apiIds: [46, 49, 65] } },
    ],
  },
];
