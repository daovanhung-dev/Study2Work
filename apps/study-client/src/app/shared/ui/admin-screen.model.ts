export type AdminScreenMode =
  | 'list'
  | 'detail'
  | 'edit'
  | 'actions'
  | 'review'
  | 'builder'
  | 'statistics'
  | 'delete'
  | 'compose'
  | 'status'
  | 'moderation'
  | 'report'
  | 'export';

export type AdminScreenSourceState =
  'session-unavailable' | 'contract-blocked' | 'api-absent' | 'data-backed';

export interface AdminScreenFilter {
  readonly key: string;
  readonly label: string;
  readonly type: 'search' | 'text' | 'number';
  readonly placeholder?: string;
}

export interface AdminScreenRow {
  readonly values: readonly string[];
  readonly route?: string;
}

export interface AdminScreenField {
  readonly label: string;
  readonly value: string;
}

export interface AdminScreenMetric {
  readonly label: string;
  readonly value: string;
}

export interface AdminScreenSection {
  readonly title: string;
  readonly description?: string;
  readonly items: readonly string[];
}

export interface AdminScreenViewState {
  readonly status: 'loading' | 'error' | 'loaded';
  readonly message?: string;
  readonly httpStatus?: number;
  readonly retryable?: boolean;
  readonly rows?: readonly AdminScreenRow[];
  readonly fields?: readonly AdminScreenField[];
  readonly metrics?: readonly AdminScreenMetric[];
  readonly sections?: readonly AdminScreenSection[];
  readonly pagination?: {
    readonly page: number;
    readonly total: number;
    readonly totalPages: number;
    readonly size?: number;
  };
}

export interface AdminScreenApiBoundary {
  readonly apiReferences: readonly string[];
  readonly sourceState: AdminScreenSourceState;
  readonly sourceNote: string;
}

export interface AdminScreenLink {
  readonly label: string;
  readonly route: string;
}

export interface AdminScreenAction {
  readonly label: string;
  readonly reason: string;
  readonly destructive?: boolean;
}

export interface AdminScreenDefinition {
  readonly id: string;
  readonly title: string;
  readonly eyebrow: string;
  readonly description: string;
  readonly mode: AdminScreenMode;
  readonly apiReferences: readonly string[];
  readonly sourceState: AdminScreenSourceState;
  readonly sourceNote: string;
  readonly columns?: readonly string[];
  readonly fields?: readonly string[];
  readonly metrics?: readonly string[];
  readonly actions?: readonly AdminScreenAction[];
  readonly links?: readonly AdminScreenLink[];
  readonly sections?: readonly { readonly title: string; readonly description: string }[];
  readonly filters?: readonly AdminScreenFilter[];
}
