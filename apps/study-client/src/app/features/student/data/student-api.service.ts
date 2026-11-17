import { HttpParams } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';

import { STUDY_SERVER_APIS } from '../../../core/constant/api.constants';
import type { ApiEnvelope } from '../../../core/http/api-envelope';
import { StudyApiService } from '../../../core/http/study-api.service';

export type ApiId = number | string;

export interface StudentPage<T> {
  items: T[];
  pagination: {
    page: number;
    size: number;
    total: number;
    total_pages: number;
  };
}

export interface LessonRecord {
  id: ApiId;
  course_id: ApiId;
  title: string;
  content?: string | null;
  video_url?: string | null;
  order: number;
  status: string;
}

export interface ResourceRecord {
  id: ApiId;
  name: string;
  type: string;
  url?: string | null;
  visibility?: string;
  lesson_id?: ApiId | null;
}

export interface QuizChoice {
  id: ApiId;
  text: string;
}

export interface QuizQuestion {
  id: ApiId;
  text: string;
  type: string;
  choices: QuizChoice[];
}

export interface QuizRecord {
  id: ApiId;
  course_id: ApiId;
  title: string;
  duration_minutes: number;
  passing_score: string;
  questions: QuizQuestion[];
}

export interface QuizAnswerRecord {
  question_id: ApiId;
  choice_ids?: ApiId[];
  text_answer?: string | null;
  correct?: boolean;
  score?: string | null;
}

export interface QuizAttemptRecord {
  id: ApiId;
  quiz_id: ApiId;
  status: string;
  started_at: string;
  submitted_at?: string | null;
  score?: string | null;
  answers: QuizAnswerRecord[];
}

export interface AssignmentRecord {
  id: ApiId;
  course_id: ApiId;
  title: string;
  description: string;
  due_at: string;
  max_score: string;
}

export interface UploadRecord {
  id: ApiId;
  name: string;
  url: string;
  content_type: string;
  size_bytes: number;
  status: string;
}

export interface SubmissionRecord {
  id: ApiId;
  assignment_id: ApiId;
  user_id: ApiId;
  content: string;
  files: UploadRecord[];
  status: string;
  submitted_at?: string;
  score?: string | null;
  feedback?: string | null;
}

export interface AchievementRecord {
  id: ApiId;
  code: string;
  title: string;
  awarded_at: string;
  course_id?: ApiId | null;
}

export interface DiscussionCommentRecord {
  id: ApiId;
  discussion_id: ApiId;
  content: string;
  author: { id: ApiId; full_name: string; avatar_url?: string | null };
  created_at: string;
}

export interface DiscussionRecord {
  id: ApiId;
  course_id: ApiId;
  title: string;
  content: string;
  author: { id: ApiId; full_name: string; avatar_url?: string | null };
  status?: string;
  comments: DiscussionCommentRecord[];
}

export interface NotificationRecord {
  id: ApiId;
  title: string;
  content: string;
  is_read?: boolean;
  status?: string;
  read_at?: string | null;
  created_at: string;
}

export interface LessonProgressRequest {
  position: number;
  percent: number;
  completed: boolean;
}

@Injectable({ providedIn: 'root' })
export class StudentApiService {
  private readonly api = inject(StudyApiService);

  getResource(resourceId: string): Observable<ApiEnvelope<ResourceRecord>> {
    return this.api.requestDeclared(STUDY_SERVER_APIS.API_012, {
      pathParams: { resource_id: resourceId },
    });
  }

  getMyProgress(): Observable<ApiEnvelope<Record<string, unknown>>> {
    return this.api.requestDeclared(STUDY_SERVER_APIS.API_021);
  }

  getLesson(lessonId: string): Observable<ApiEnvelope<LessonRecord>> {
    return this.api.requestDeclared(STUDY_SERVER_APIS.API_024, {
      pathParams: { lesson_id: lessonId },
    });
  }

  saveLessonProgress(
    lessonId: string,
    body: LessonProgressRequest,
  ): Observable<ApiEnvelope<LessonRecord>> {
    return this.api.requestDeclared(STUDY_SERVER_APIS.API_025, {
      pathParams: { lesson_id: lessonId },
      body,
    });
  }

  getLessonResources(lessonId: string): Observable<ApiEnvelope<ResourceRecord[]>> {
    return this.api.requestDeclared(STUDY_SERVER_APIS.API_026, {
      pathParams: { lesson_id: lessonId },
    });
  }

  getNextLesson(lessonId: string): Observable<ApiEnvelope<LessonRecord | null>> {
    return this.api.requestDeclared(STUDY_SERVER_APIS.API_027, {
      pathParams: { lesson_id: lessonId },
    });
  }

  getQuiz(quizId: string): Observable<ApiEnvelope<QuizRecord>> {
    return this.api.requestDeclared(STUDY_SERVER_APIS.API_028, {
      pathParams: { quiz_id: quizId },
    });
  }

  startAttempt(quizId: string): Observable<ApiEnvelope<QuizAttemptRecord>> {
    return this.api.requestDeclared(STUDY_SERVER_APIS.API_029, {
      pathParams: { quiz_id: quizId },
    });
  }

  saveAnswer(
    attemptId: string,
    questionId: ApiId,
    choiceIds: ApiId[],
  ): Observable<ApiEnvelope<QuizAttemptRecord>> {
    return this.api.requestDeclared(STUDY_SERVER_APIS.API_030, {
      pathParams: { attempt_id: attemptId },
      body: { question_id: questionId, 'answer(s)': JSON.stringify(choiceIds) },
    });
  }

  submitAttempt(attemptId: string): Observable<ApiEnvelope<QuizAttemptRecord>> {
    return this.api.requestDeclared(STUDY_SERVER_APIS.API_031, {
      pathParams: { attempt_id: attemptId },
    });
  }

  getAttemptResult(attemptId: string): Observable<ApiEnvelope<QuizAttemptRecord>> {
    return this.api.requestDeclared(STUDY_SERVER_APIS.API_032, {
      pathParams: { attempt_id: attemptId },
    });
  }

  getAssignment(assignmentId: string): Observable<ApiEnvelope<AssignmentRecord>> {
    return this.api.requestDeclared(STUDY_SERVER_APIS.API_033, {
      pathParams: { assignment_id: assignmentId },
    });
  }

  uploadSubmissionFile(file: File, courseId: ApiId): Observable<ApiEnvelope<UploadRecord>> {
    const body = new FormData();
    body.append('file', file, file.name);
    body.append('purpose', 'SUBMISSION');
    body.append('course_id', String(courseId));
    return this.api.requestDeclared(STUDY_SERVER_APIS.API_034, { body });
  }

  submitAssignment(
    assignmentId: string,
    text: string,
    fileIds: ApiId[],
  ): Observable<ApiEnvelope<SubmissionRecord>> {
    return this.api.requestDeclared(STUDY_SERVER_APIS.API_035, {
      pathParams: { assignment_id: assignmentId },
      body: { text, 'file refs': JSON.stringify(fileIds) },
    });
  }

  getSubmission(submissionId: string): Observable<ApiEnvelope<SubmissionRecord>> {
    return this.api.requestDeclared(STUDY_SERVER_APIS.API_036, {
      pathParams: { submission_id: submissionId },
    });
  }

  getCourseProgress(courseId: string): Observable<ApiEnvelope<Record<string, unknown>>> {
    return this.api.requestDeclared(STUDY_SERVER_APIS.API_037, {
      pathParams: { course_id: courseId },
    });
  }

  getAchievements(courseId?: string): Observable<ApiEnvelope<StudentPage<AchievementRecord>>> {
    const params = courseId ? new HttpParams().set('course_id', courseId) : undefined;
    return this.api.requestDeclared(STUDY_SERVER_APIS.API_038, { params });
  }

  getDiscussions(options: { courseId?: string; page?: number; sort?: string } = {}): Observable<ApiEnvelope<StudentPage<DiscussionRecord>>> {
    let params = new HttpParams();
    if (options.courseId) params = params.set('course_id', options.courseId);
    if (options.page !== undefined) params = params.set('page', options.page);
    if (options.sort) params = params.set('sort', options.sort);
    return this.api.requestDeclared(STUDY_SERVER_APIS.API_039, { params });
  }

  createDiscussion(body: { course_id: ApiId; title: string; content: string }): Observable<ApiEnvelope<DiscussionRecord>> {
    return this.api.requestDeclared(STUDY_SERVER_APIS.API_040, { body });
  }

  getDiscussion(discussionId: string): Observable<ApiEnvelope<StudentPage<DiscussionRecord>>> {
    return this.api.requestDeclared(STUDY_SERVER_APIS.API_042, {
      pathParams: { discussion_id: discussionId },
    });
  }

  addDiscussionComment(discussionId: string, content: string): Observable<ApiEnvelope<DiscussionRecord>> {
    return this.api.requestDeclared(STUDY_SERVER_APIS.API_041, {
      pathParams: { discussion_id: discussionId },
      body: { content },
    });
  }

  getNotifications(options: { unreadOnly?: boolean; page?: number } = {}): Observable<ApiEnvelope<StudentPage<NotificationRecord>>> {
    let params = new HttpParams();
    if (options.unreadOnly !== undefined) params = params.set('unread_only', options.unreadOnly);
    if (options.page !== undefined) params = params.set('page', options.page);
    return this.api.requestDeclared(STUDY_SERVER_APIS.API_043, { params });
  }

  markNotificationRead(notificationId: string): Observable<ApiEnvelope<StudentPage<NotificationRecord>>> {
    return this.api.requestDeclared(STUDY_SERVER_APIS.API_044, {
      pathParams: { notification_id: notificationId },
    });
  }

  markAllNotificationsRead(): Observable<ApiEnvelope<StudentPage<NotificationRecord>>> {
    return this.api.requestDeclared(STUDY_SERVER_APIS.API_045, { body: {} });
  }
}
