export interface VerifiedLessonAccess {
  readonly lessonId: number;
  readonly courseId: number;
  readonly title: string;
}

export type StudentLessonAccessState =
  | { readonly kind: 'missing-context' | 'checking' | 'denied' | 'not-found' | 'blocked'; readonly title: string; readonly message: string }
  | { readonly kind: 'allowed'; readonly title: string; readonly message: string; readonly lesson: VerifiedLessonAccess };
