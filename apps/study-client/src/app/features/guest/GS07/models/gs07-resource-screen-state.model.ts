export interface GS07ResourceDetail {
  readonly id: number;
  readonly name: string;
  readonly type: string;
  readonly url: string;
  readonly visibility: 'PUBLIC' | 'PRIVATE';
  readonly lesson_id: number | null;
}

export type GS07ResourceScreenState =
  | { readonly status: 'loading' }
  | { readonly status: 'invalid-resource' }
  | { readonly status: 'login-required' }
  | { readonly status: 'forbidden' }
  | { readonly status: 'not-found' }
  | { readonly status: 'error'; readonly message: string }
  | {
      readonly status: 'ready';
      readonly resource: GS07ResourceDetail;
      readonly safeUrl: string | null;
    };
