/** ST-01 DD 03-data-flow / 04-api-integration: unavailable is not empty or success. */
export interface StudentOverviewState {
  readonly kind: 'blocked';
  readonly title: string;
  readonly message: string;
}
