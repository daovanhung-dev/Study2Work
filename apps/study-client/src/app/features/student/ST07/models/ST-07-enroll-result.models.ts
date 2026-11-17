/** ST-07 DD 03-data-flow / 04-api-integration: unavailable is not empty or success. */
export interface StudentEnrollResultState {
  readonly kind: 'blocked' | 'missing-context';
  readonly title: string;
  readonly message: string;
}
