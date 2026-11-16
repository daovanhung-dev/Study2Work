import { Routes } from '@angular/router';

import { StudentLayout } from '../../layouts/student/student-layout';
import { ST11Page } from './ST11/pages/st11-page';
import { ST12Page } from './ST12/pages/st12-page';
import { ST13Page } from './ST13/pages/st13-page';
import { ST14Page } from './ST14/pages/st14-page';
import { ST15Page } from './ST15/pages/st15-page';
import { ST16Page } from './ST16/pages/st16-page';
import { ST17Page } from './ST17/pages/st17-page';
import { ST18Page } from './ST18/pages/st18-page';
import { ST19Page } from './ST19/pages/st19-page';
import { ST20Page } from './ST20/pages/st20-page';
import { ST21Page } from './ST21/pages/st21-page';
import { ST22Page } from './ST22/pages/st22-page';
import { ST23Page } from './ST23/pages/st23-page';
import { ST24Page } from './ST24/pages/st24-page';
import { ST25Page } from './ST25/pages/st25-page';
import { ST26Page } from './ST26/pages/st26-page';

export const studentRoutes: Routes = [
  {
    path: '',
    component: StudentLayout,
    children: [
      {
        path: 'lessons/:lessonId/resources',
        component: ST12Page,
        data: { shell: 'portal' },
      },
      {
        path: 'quizzes/:quizId/attempts/:attemptId',
        component: ST14Page,
        data: { shell: 'exam' },
      },
      {
        path: 'attempts/:attemptId/submit',
        component: ST15Page,
        data: { shell: 'exam' },
      },
      {
        path: 'attempts/:attemptId/result',
        component: ST16Page,
        data: { shell: 'portal' },
      },
      {
        path: 'assignments/:assignmentId/submit',
        component: ST18Page,
        data: { shell: 'portal' },
      },
      {
        path: 'assignments/:assignmentId',
        component: ST17Page,
        data: { shell: 'portal' },
      },
      {
        path: 'submissions/:submissionId',
        component: ST19Page,
        data: { shell: 'portal' },
      },
      {
        path: 'progress/:courseId',
        component: ST21Page,
        data: { shell: 'blank' },
      },
      {
        path: 'progress',
        component: ST20Page,
        data: { shell: 'portal' },
      },
      {
        path: 'achievements',
        component: ST22Page,
        data: { shell: 'portal' },
      },
      {
        path: 'discussions/new',
        component: ST24Page,
        data: { shell: 'portal' },
      },
      {
        path: 'discussions/:discussionId',
        component: ST25Page,
        data: { shell: 'portal' },
      },
      {
        path: 'discussions',
        component: ST23Page,
        data: { shell: 'blank' },
      },
      {
        path: 'notifications',
        component: ST26Page,
        data: { shell: 'portal' },
      },
      {
        path: 'quizzes/:quizId',
        component: ST13Page,
        data: { shell: 'portal' },
      },
      {
        path: 'lessons/:lessonId',
        component: ST11Page,
      },
    ],
  },
];
