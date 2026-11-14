/** ST-10 DD 03-data-flow / 04-api-integration: unavailable is not empty or success. */
export interface StudentLessonAccessState {
  readonly kind: 'blocked' | 'missing-context';
  readonly title: string;
  readonly message: string;
}
