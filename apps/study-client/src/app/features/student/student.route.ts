import { Routes } from '@angular/router';
import { StudentLayout } from '../../layouts/student/student-layout';

export const studentRoutes: Routes = [
  {
    path: '',
    component: StudentLayout,
    children: [
      {
        path: 'profile/edit',
        data: { section: 'profile' },
        loadComponent: () =>
          import('./ST03/pages/ST-03-profile-edit-page').then((m) => m.StudentProfileEditPage),
      },
      {
        path: 'profile',
        data: { section: 'profile' },
        loadComponent: () =>
          import('./ST02/pages/ST-02-profile-page').then((m) => m.StudentProfilePage),
      },
      {
        path: 'enroll/result/:courseId',
        data: { section: 'checkout' },
        loadComponent: () =>
          import('./ST07/pages/ST-07-enroll-result-page').then((m) => m.StudentEnrollResultPage),
      },
      {
        path: 'enroll/:courseId',
        data: { section: 'checkout' },
        loadComponent: () =>
          import('./ST04/pages/ST-04-enroll-check-page').then((m) => m.StudentEnrollCheckPage),
      },
      {
        path: 'checkout/:courseId',
        data: { section: 'checkout' },
        loadComponent: () =>
          import('./ST05/pages/ST-05-order-check-page').then((m) => m.StudentOrderCheckPage),
      },
      {
        path: 'pay/:orderId',
        data: { section: 'checkout' },
        loadComponent: () =>
          import('./ST06/pages/ST-06-payment-page').then((m) => m.StudentPaymentPage),
      },
      {
        path: 'courses/:courseId',
        data: { section: 'myCourses' },
        loadComponent: () =>
          import('./ST09/pages/ST-09-course-overview-page').then(
            (m) => m.StudentCourseOverviewPage,
          ),
      },
      {
        path: 'courses',
        data: { section: 'myCourses' },
        loadComponent: () =>
          import('./ST08/pages/ST-08-courses-page').then((m) => m.StudentCoursesPage),
      },
      {
        path: 'lessons/:lessonId/start',
        data: { section: 'myCourses' },
        loadComponent: () =>
          import('./ST10/pages/ST-10-lesson-access-page').then((m) => m.StudentLessonAccessPage),
      },
      {
        path: '',
        pathMatch: 'full',
        data: { section: 'overview' },
        loadComponent: () =>
          import('./ST01/pages/ST-01-overview-page').then((m) => m.StudentOverviewPage),
      },
    ],
  },
];
