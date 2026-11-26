import { Routes } from '@angular/router';

import { StudentLayout } from '../../layouts/student/student-layout';
import { ST02Page } from './ST02/pages/st02-page';
import { ST03Page } from './ST03/pages/st03-page';
import { ST04Page } from './ST04/pages/st04-page';
import { ST05Page } from './ST05/pages/st05-page';
import { ST06Page } from './ST06/pages/st06-page';
import { ST01Page } from './ST01/pages/st01-page';
import { ST07Page } from './ST07/pages/st07-page';
import { ST08Page } from './ST08/pages/st08-page';
import { ST09Page } from './ST09/pages/st09-page';
import { ST10Page } from './ST10/pages/st10-page';
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
        path: '',
        pathMatch: 'full',
        component: ST01Page,
        data: { apiIds: [20, 21, 38, 43], shell: 'custom' },
      },
      {
        path: 'profile',
        component: ST02Page,
        data: { apiIds: [4], shell: 'custom' },
      },
      {
        path: 'profile/edit',
        component: ST03Page,
        data: { apiIds: [4, 13, 14], shell: 'custom' },
      },
      {
        path: 'enroll/:courseId',
        component: ST04Page,
        data: { apiIds: [8, 15, 19, 20], shell: 'custom' },
      },
      {
        path: 'checkout/:courseId',
        component: ST05Page,
        data: { apiIds: [8, 16], shell: 'custom' },
      },
      {
        path: 'pay/:orderId',
        component: ST06Page,
        data: { apiIds: [17, 18], shell: 'custom' },
      },
      {
        path: 'enroll/result/:courseId',
        component: ST07Page,
        data: { apiIds: [18, 19, 20], shell: 'custom' },
      },
      {
        path: 'courses',
        component: ST08Page,
        data: { apiIds: [20, 21], shell: 'custom' },
      },
      {
        path: 'courses/:courseId',
        component: ST09Page,
        data: { apiIds: [9, 20, 37], shell: 'custom' },
      },
      {
        path: 'lessons/:lessonId/start',
        component: ST10Page,
        data: { apiIds: [22, 23, 24], shell: 'custom' },
      },
      {
        path: 'lessons/:lessonId/resources',
        component: ST12Page,
        data: { apiIds: [12, 26], shell: 'portal' },
      },
      {
        path: 'quizzes/:quizId/attempts/:attemptId',
        component: ST14Page,
        data: { apiIds: [28, 29, 30], shell: 'exam' },
      },
      {
        path: 'attempts/:attemptId/submit',
        component: ST15Page,
        data: { apiIds: [30, 31], shell: 'exam' },
      },
      {
        path: 'attempts/:attemptId/result',
        component: ST16Page,
        data: { apiIds: [32], shell: 'portal' },
      },
      {
        path: 'assignments/:assignmentId/submit',
        component: ST18Page,
        data: { apiIds: [33, 34, 35], shell: 'portal' },
      },
      {
        path: 'assignments/:assignmentId',
        component: ST17Page,
        data: { apiIds: [33], shell: 'portal' },
      },
      {
        path: 'submissions/:submissionId',
        component: ST19Page,
        data: { apiIds: [36], shell: 'portal' },
      },
      {
        path: 'progress/:courseId',
        component: ST21Page,
        data: { apiIds: [37], shell: 'portal' },
      },
      {
        path: 'progress',
        component: ST20Page,
        data: { apiIds: [21, 38], shell: 'portal' },
      },
      {
        path: 'achievements',
        component: ST22Page,
        data: { apiIds: [38], shell: 'portal' },
      },
      {
        path: 'discussions/new',
        component: ST24Page,
        data: { apiIds: [20, 39, 40], shell: 'portal' },
      },
      {
        path: 'discussions/:discussionId',
        component: ST25Page,
        data: { apiIds: [41, 42], shell: 'portal' },
      },
      {
        path: 'discussions',
        component: ST23Page,
        data: { apiIds: [39], shell: 'portal' },
      },
      {
        path: 'notifications',
        component: ST26Page,
        data: { apiIds: [43, 44, 45], shell: 'portal' },
      },
      {
        path: 'quizzes/:quizId',
        component: ST13Page,
        data: { apiIds: [28, 29], shell: 'portal' },
      },
      {
        path: 'lessons/:lessonId',
        component: ST11Page,
        data: { apiIds: [24, 25, 26, 27], shell: 'portal' },
      },
    ],
  },
];
