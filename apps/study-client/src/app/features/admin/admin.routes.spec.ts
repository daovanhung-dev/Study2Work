import { describe, expect, it } from 'vitest';

import { adminRoutes } from './admin.routes';

describe('adminRoutes', () => {
  const children = adminRoutes.find((route) => route.path === '')?.children ?? [];

  it('registers the requested AD-01 through AD-25 route surfaces', () => {
    const routeComponents = new Map(
      children.map((route) => [route.path, route.component?.name.replace(/^_/, '')]),
    );
    const expected = [
      ['', 'AD01Page'],
      ['users', 'AD02Page'],
      ['users/:userId', 'AD03Page'],
      ['users/:userId/edit', 'AD04Page'],
      ['users/:userId/actions', 'AD05Page'],
      ['courses', 'AD06Page'],
      ['courses/:courseId', 'AD07Page'],
      ['courses/:courseId/edit', 'AD08Page'],
      ['courses/:courseId/actions', 'AD09Page'],
      ['content/pending', 'AD10Page'],
      ['content/:contentId/review', 'AD11Page'],
      ['lessons', 'AD12Page'],
      ['lessons/:lessonId', 'AD13Page'],
      ['lessons/:lessonId/edit', 'AD14Page'],
      ['quizzes', 'AD15Page'],
      ['quizzes/new', 'AD16Page'],
      ['quizzes/:quizId/edit', 'AD16Page'],
      ['quizzes/:quizId/statistics', 'AD17Page'],
      ['quizzes/:quizId/delete', 'AD18Page'],
      ['notifications', 'AD19Page'],
      ['notifications/new', 'AD20Page'],
      ['notifications/:notificationId', 'AD21Page'],
      ['discussions/reported', 'AD22Page'],
      ['discussions/:discussionId/moderate', 'AD23Page'],
      ['reports/community-impact', 'AD24Page'],
      ['reports/export', 'AD25Page'],
    ] as const;

    expect(children).toHaveLength(expected.length);
    for (const [path, componentName] of expected) {
      expect(routeComponents.get(path)).toBe(componentName);
    }
  });
});

