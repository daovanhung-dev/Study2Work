export interface PublicLesson {
  readonly id: number;
  readonly title: string;
  readonly order: number;
}

export interface VerifiedCourseOverview {
  readonly courseId: number;
  readonly name: string;
  readonly completedLessons: number;
  readonly totalLessons: number;
  readonly progressPercent: number;
  readonly publicLessons: readonly PublicLesson[];
}

export type StudentCourseOverviewState =
  | { readonly kind: 'missing-context' | 'loading' | 'not-enrolled' | 'blocked'; readonly title: string; readonly message: string }
  | { readonly kind: 'ready'; readonly data: VerifiedCourseOverview };
