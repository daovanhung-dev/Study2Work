/** ST-08 DD 03-data-flow / 04-api-integration: unavailable is not empty or success. */
export interface StudentCoursesState {
  readonly kind: 'blocked';
  readonly title: string;
  readonly message: string;
}
