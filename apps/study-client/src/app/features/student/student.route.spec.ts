import { describe, expect, it } from 'vitest';

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
import { studentRoutes } from './student.route';

describe('studentRoutes', () => {
  it('maps the Student overview to its assigned APIs without inventing dashboard values', () => {
    const layoutRoute = studentRoutes.find((route) => route.component === StudentLayout);
    const overviewRoute = layoutRoute?.children?.find((route) => route.path === '');

    expect(overviewRoute?.component).toBe(ST01Page);
    expect(overviewRoute?.data).toEqual({ apiIds: [20, 21, 38, 43], shell: 'custom' });
  });

  it('maps ST-02 to the Student profile API without enabling a request', () => {
    const layoutRoute = studentRoutes.find((route) => route.component === StudentLayout);
    const profileRoute = layoutRoute?.children?.find((route) => route.path === 'profile');

    expect(profileRoute?.component).toBe(ST02Page);
    expect(profileRoute?.data).toEqual({ apiIds: [4], shell: 'custom' });
  });

  it('maps ST-03 to profile APIs while preserving its closed UI gate', () => {
    const layoutRoute = studentRoutes.find((route) => route.component === StudentLayout);
    const profileEditRoute = layoutRoute?.children?.find((route) => route.path === 'profile/edit');

    expect(profileEditRoute?.component).toBe(ST03Page);
    expect(profileEditRoute?.data).toEqual({ apiIds: [4, 13, 14], shell: 'custom' });
  });

  it('maps ST-04 to course and enrollment APIs without inferring enrollment state', () => {
    const layoutRoute = studentRoutes.find((route) => route.component === StudentLayout);
    const enrollmentRoute = layoutRoute?.children?.find(
      (route) => route.path === 'enroll/:courseId',
    );

    expect(enrollmentRoute?.component).toBe(ST04Page);
    expect(enrollmentRoute?.data).toEqual({ apiIds: [8, 15, 19, 20], shell: 'custom' });
  });

  it('maps ST-05 to course and order APIs while keeping order creation gated', () => {
    const layoutRoute = studentRoutes.find((route) => route.component === StudentLayout);
    const checkoutRoute = layoutRoute?.children?.find(
      (route) => route.path === 'checkout/:courseId',
    );

    expect(checkoutRoute?.component).toBe(ST05Page);
    expect(checkoutRoute?.data).toEqual({ apiIds: [8, 16], shell: 'custom' });
  });

  it('maps ST-06 to payment and operation APIs while keeping payment initiation gated', () => {
    const layoutRoute = studentRoutes.find((route) => route.component === StudentLayout);
    const paymentRoute = layoutRoute?.children?.find((route) => route.path === 'pay/:orderId');

    expect(paymentRoute?.component).toBe(ST06Page);
    expect(paymentRoute?.data).toEqual({ apiIds: [17, 18], shell: 'custom' });
  });

  it('maps the Student enrollment result to its assigned APIs without claiming enrollment', () => {
    const layoutRoute = studentRoutes.find((route) => route.component === StudentLayout);
    const resultRoute = layoutRoute?.children?.find(
      (route) => route.path === 'enroll/result/:courseId',
    );

    expect(resultRoute?.component).toBe(ST07Page);
    expect(resultRoute?.data).toEqual({ apiIds: [18, 19, 20], shell: 'custom' });
  });

  it('maps ST-08 and ST-09 to course and progress APIs without private API calls', () => {
    const layoutRoute = studentRoutes.find((route) => route.component === StudentLayout);
    const coursesRoute = layoutRoute?.children?.find((route) => route.path === 'courses');
    const courseRoute = layoutRoute?.children?.find((route) => route.path === 'courses/:courseId');

    expect(coursesRoute?.component).toBe(ST08Page);
    expect(coursesRoute?.data).toEqual({ apiIds: [20, 21], shell: 'custom' });
    expect(courseRoute?.component).toBe(ST09Page);
    expect(courseRoute?.data).toEqual({ apiIds: [9, 20, 37], shell: 'custom' });
  });

  it('maps the lesson entitlement transition to APIs #22–#24 and keeps media locked', () => {
    const layoutRoute = studentRoutes.find((route) => route.component === StudentLayout);
    const startRoute = layoutRoute?.children?.find(
      (route) => route.path === 'lessons/:lessonId/start',
    );

    expect(startRoute?.component).toBe(ST10Page);
    expect(startRoute?.data).toEqual({ apiIds: [22, 23, 24], shell: 'custom' });
  });

  it('registers all 26 Student screens with their page, API, and shell metadata', () => {
    const layoutRoute = studentRoutes.find((route) => route.component === StudentLayout);
    const children = layoutRoute?.children ?? [];
    const screens = [
      { path: '', page: ST01Page, apiIds: [20, 21, 38, 43], shell: 'custom' },
      { path: 'profile', page: ST02Page, apiIds: [4], shell: 'custom' },
      { path: 'profile/edit', page: ST03Page, apiIds: [4, 13, 14], shell: 'custom' },
      { path: 'enroll/:courseId', page: ST04Page, apiIds: [8, 15, 19, 20], shell: 'custom' },
      { path: 'checkout/:courseId', page: ST05Page, apiIds: [8, 16], shell: 'custom' },
      { path: 'pay/:orderId', page: ST06Page, apiIds: [17, 18], shell: 'custom' },
      { path: 'enroll/result/:courseId', page: ST07Page, apiIds: [18, 19, 20], shell: 'custom' },
      { path: 'courses', page: ST08Page, apiIds: [20, 21], shell: 'custom' },
      { path: 'courses/:courseId', page: ST09Page, apiIds: [9, 20, 37], shell: 'custom' },
      { path: 'lessons/:lessonId/start', page: ST10Page, apiIds: [22, 23, 24], shell: 'custom' },
      { path: 'lessons/:lessonId', page: ST11Page, apiIds: [24, 25, 26, 27], shell: 'portal' },
      { path: 'lessons/:lessonId/resources', page: ST12Page, apiIds: [12, 26], shell: 'portal' },
      { path: 'quizzes/:quizId', page: ST13Page, apiIds: [28, 29], shell: 'portal' },
      { path: 'quizzes/:quizId/attempts/:attemptId', page: ST14Page, apiIds: [28, 29, 30], shell: 'exam' },
      { path: 'attempts/:attemptId/submit', page: ST15Page, apiIds: [30, 31], shell: 'exam' },
      { path: 'attempts/:attemptId/result', page: ST16Page, apiIds: [32], shell: 'portal' },
      { path: 'assignments/:assignmentId', page: ST17Page, apiIds: [33], shell: 'portal' },
      { path: 'assignments/:assignmentId/submit', page: ST18Page, apiIds: [33, 34, 35], shell: 'portal' },
      { path: 'submissions/:submissionId', page: ST19Page, apiIds: [36], shell: 'portal' },
      { path: 'progress', page: ST20Page, apiIds: [21, 38], shell: 'portal' },
      { path: 'progress/:courseId', page: ST21Page, apiIds: [37], shell: 'blank' },
      { path: 'achievements', page: ST22Page, apiIds: [38], shell: 'portal' },
      { path: 'discussions', page: ST23Page, apiIds: [39], shell: 'blank' },
      { path: 'discussions/new', page: ST24Page, apiIds: [20, 39, 40], shell: 'portal' },
      { path: 'discussions/:discussionId', page: ST25Page, apiIds: [41, 42], shell: 'portal' },
      { path: 'notifications', page: ST26Page, apiIds: [43, 44, 45], shell: 'portal' },
    ];

    expect(children).toHaveLength(screens.length);
    for (const screen of screens) {
      const matches = children.filter((route) => route.path === screen.path);
      expect(matches).toHaveLength(1);
      expect(matches[0]?.component).toBe(screen.page);
      expect(matches[0]?.data).toEqual({ apiIds: screen.apiIds, shell: screen.shell });
    }
  });
});
