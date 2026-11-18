import { HttpParams } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { defer, firstValueFrom, from, type Observable } from 'rxjs';

import { STUDY_SERVER_APIS } from '../../../../core/constant/api.constants';
import type { ApiEnvelope } from '../../../../core/http/api-envelope';
import { StudyApiService } from '../../../../core/http/study-api.service';
import type { PublicLesson, VerifiedCourseOverview } from '../models/ST-09-course-overview.models';

interface MembershipPage {
  readonly items: readonly { readonly courseId: number; readonly name: string }[];
  readonly page: number;
  readonly totalPages: number;
}

@Injectable({ providedIn: 'root' })
export class StudentCourseOverviewService {
  private readonly api = inject(StudyApiService);

  getOverview(courseId: string): Observable<VerifiedCourseOverview | null> {
    return defer(() => from(this.loadOverview(courseId)));
  }

  private async loadOverview(courseId: string): Promise<VerifiedCourseOverview | null> {
    const numericId = Number(courseId);
    if (!Number.isSafeInteger(numericId) || numericId < 1) {
      throw new Error('Không thể xác minh chính xác mã khóa học này.');
    }

    let course: MembershipPage['items'][number] | undefined;
    let page = 1;
    do {
      const response = await firstValueFrom(this.api.request<unknown>(STUDY_SERVER_APIS.API_020, {
        params: new HttpParams().set('status', 'ACTIVE').set('page', page),
      }));
      const membership = readMembershipPage(response);
      if (membership.page !== page) throw new Error('Phân trang khóa học không hợp lệ.');
      course = membership.items.find((item) => item.courseId === numericId);
      if (course) break;
      if (page >= membership.totalPages) return null;
      page += 1;
    } while (true);

    const progressResponse = await firstValueFrom(this.api.request<unknown>(STUDY_SERVER_APIS.API_037,
      { pathParams: { course_id: courseId } }));
    const progress = readCourseProgress(progressResponse, numericId);
    const curriculumResponse = await firstValueFrom(this.api.request<unknown>(STUDY_SERVER_APIS.API_009,
      { pathParams: { course_id: courseId } }));
    const publicLessons = readPublicLessons(curriculumResponse, numericId);
    return {
      courseId: numericId,
      name: course.name,
      ...progress,
      publicLessons,
    };
  }
}

function readMembershipPage(response: ApiEnvelope<unknown>): MembershipPage {
  const data = response.data;
  if (!isSuccessful(response) || !isRecord(data) || !Array.isArray(data['items']) || !isRecord(data['pagination'])) {
    throw new Error('Danh sách khóa học không hợp lệ.');
  }
  const pagination = data['pagination'];
  const page = pagination['page'];
  const totalPages = pagination['total_pages'];
  if (!Number.isInteger(page) || (page as number) < 1 ||
      !Number.isInteger(totalPages) || (totalPages as number) < 0) {
    throw new Error('Phân trang khóa học không hợp lệ.');
  }
  const items = data['items'].map((item: unknown) => {
    if (!isRecord(item) || !Number.isSafeInteger(item['course_id']) || (item['course_id'] as number) < 1 ||
        typeof item['name'] !== 'string' || typeof item['enrollment_status'] !== 'string') {
      throw new Error('Dữ liệu ghi danh không hợp lệ.');
    }
    if (item['enrollment_status'] !== 'ACTIVE') {
      throw new Error('Trạng thái ghi danh không khớp bộ lọc.');
    }
    return { courseId: item['course_id'] as number, name: item['name'] };
  });
  return { items, page: page as number, totalPages: totalPages as number };
}

function readCourseProgress(response: ApiEnvelope<unknown>, courseId: number) {
  const data = response.data;
  if (!isSuccessful(response) || !isRecord(data) || data['course_id'] !== courseId ||
      !isNonnegativeInteger(data['completed_lessons']) || !isNonnegativeInteger(data['total_lessons']) ||
      !Number.isInteger(data['progress_percent']) || (data['progress_percent'] as number) < 0 ||
      (data['progress_percent'] as number) > 100 || typeof data['has_content'] !== 'boolean' ||
      (data['completed_lessons'] as number) > (data['total_lessons'] as number)) {
    throw new Error('Dữ liệu tiến độ khóa học không hợp lệ.');
  }
  return {
    completedLessons: data['completed_lessons'] as number,
    totalLessons: data['total_lessons'] as number,
    progressPercent: data['progress_percent'] as number,
  };
}

function readPublicLessons(response: ApiEnvelope<unknown>, courseId: number): PublicLesson[] {
  const data = response.data;
  if (!isSuccessful(response) || !isRecord(data) || !Array.isArray(data['items'])) {
    throw new Error('Đề cương công khai không hợp lệ.');
  }
  const lessons: PublicLesson[] = data['items'].map((item: unknown) => {
    if (!isRecord(item) || !Number.isSafeInteger(item['id']) || (item['id'] as number) < 1 ||
        item['course_id'] !== courseId || typeof item['title'] !== 'string' ||
        !isNonnegativeInteger(item['order']) || item['status'] !== 'PUBLISHED') {
      throw new Error('Bài học trong đề cương không hợp lệ.');
    }
    return { id: item['id'] as number, title: item['title'], order: item['order'] as number };
  });
  return lessons.sort((first, second) => first.order - second.order || first.id - second.id);
}

function isSuccessful(response: ApiEnvelope<unknown>): boolean {
  return response.success === true && response.businessCode === 'DESIGN_RESOURCE_RETRIEVED';
}

function isNonnegativeInteger(value: unknown): value is number {
  return Number.isSafeInteger(value) && (value as number) >= 0;
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}
