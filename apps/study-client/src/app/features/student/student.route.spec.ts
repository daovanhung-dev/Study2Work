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
    expect(enrollmentRoute?.data).toEqual({ apiIds: [8, 15], shell: 'custom' });
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
});
