export interface NotFoundViewModel {
  readonly source: 'route' | 'resource' | 'error';
  readonly title: string;
  readonly description: string;
  /** Router misses are UI state, not an HTTP response from the API. */
  readonly statusLabel: string;
}
