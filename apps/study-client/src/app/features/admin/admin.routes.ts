import { Routes } from '@angular/router';

import { AdminLayout } from '../../layouts/admin/admin-layout';
import { AD01Page } from './AD01/pages/ad01-page';
import { AD02Page } from './AD02/pages/ad02-page';
import { AD03Page } from './AD03/pages/ad03-page';
import { AD04Page } from './AD04/pages/ad04-page';
import { AD05Page } from './AD05/pages/ad05-page';
import { AD06Page } from './AD06/pages/ad06-page';
import { AD07Page } from './AD07/pages/ad07-page';
import { AD08Page } from './AD08/pages/ad08-page';
import { AD09Page } from './AD09/pages/ad09-page';
import { AD10Page } from './AD10/pages/ad10-page';
import { AD11Page } from './AD11/pages/ad11-page';
import { AD12Page } from './AD12/pages/ad12-page';
import { AD13Page } from './AD13/pages/ad13-page';
import { AD14Page } from './AD14/pages/ad14-page';
import { AD15Page } from './AD15/pages/ad15-page';
import { AD16Page } from './AD16/pages/ad16-page';
import { AD17Page } from './AD17/pages/ad17-page';
import { AD18Page } from './AD18/pages/ad18-page';
import { AD19Page } from './AD19/pages/ad19-page';
import { AD20Page } from './AD20/pages/ad20-page';
import { AD21Page } from './AD21/pages/ad21-page';
import { AD22Page } from './AD22/pages/ad22-page';
import { AD23Page } from './AD23/pages/ad23-page';
import { AD24Page } from './AD24/pages/ad24-page';
import { AD25Page } from './AD25/pages/ad25-page';

export const adminRoutes: Routes = [
  {
    path: '',
    component: AdminLayout,
    children: [
      { path: '', pathMatch: 'full', component: AD01Page },
      { path: 'users/:userId/edit', component: AD04Page },
      { path: 'users/:userId/actions', component: AD05Page },
      { path: 'users/:userId', component: AD03Page },
      { path: 'users', component: AD02Page },
      { path: 'courses/:courseId/edit', component: AD08Page },
      { path: 'courses/:courseId/actions', component: AD09Page },
      { path: 'courses/:courseId', component: AD07Page },
      { path: 'courses', component: AD06Page },
      { path: 'content/:contentId/review', component: AD11Page },
      { path: 'content/pending', component: AD10Page },
      { path: 'lessons/:lessonId/edit', component: AD14Page },
      { path: 'lessons/:lessonId', component: AD13Page },
      { path: 'lessons', component: AD12Page },
      { path: 'quizzes/new', component: AD16Page },
      { path: 'quizzes/:quizId/edit', component: AD16Page },
      { path: 'quizzes/:quizId/statistics', component: AD17Page },
      { path: 'quizzes/:quizId/delete', component: AD18Page },
      { path: 'quizzes', component: AD15Page },
      { path: 'notifications/new', component: AD20Page },
      { path: 'notifications/:notificationId', component: AD21Page },
      { path: 'notifications', component: AD19Page },
      { path: 'discussions/reported', component: AD22Page },
      { path: 'discussions/:discussionId/moderate', component: AD23Page },
      { path: 'reports/community-impact', component: AD24Page },
      { path: 'reports/export', component: AD25Page },
    ],
  },
];
