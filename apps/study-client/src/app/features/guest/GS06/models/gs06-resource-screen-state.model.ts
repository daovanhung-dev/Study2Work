export interface GS06Resource {
  readonly id: number;
  readonly name: string;
  readonly type: string;
  readonly url: string;
  readonly visibility: 'PUBLIC';
  readonly lesson_id: number | null;
}

export type GS06ResourceScreenState =
  | { readonly status: 'loading' }
  | { readonly status: 'invalid-course' }
  | { readonly status: 'error' }
  | { readonly status: 'empty' }
  | { readonly status: 'ready'; readonly resources: readonly GS06Resource[] };
