import type {
  AdminContent,
  AdminCourse,
  AdminDiscussion,
  AdminLesson,
  AdminNotification,
  AdminQuiz,
  AdminQuizStatistics,
  AdminUserProfile,
} from './admin-api.models';
import { displayValue, formatDate } from './admin-screen-state';
import type { AdminScreenField, AdminScreenMetric, AdminScreenRow, AdminScreenSection } from '../../shared/ui/admin-screen.model';

export function renderUserFields(user: AdminUserProfile): readonly AdminScreenField[] {
  return [
    { label: 'Mã người dùng', value: displayValue(user.id) },
    { label: 'Họ và tên', value: user.full_name },
    { label: 'Email', value: user.email },
    { label: 'Số điện thoại', value: displayValue(user.phone) },
    { label: 'Ảnh đại diện', value: displayValue(user.avatar_url) },
    { label: 'Vai trò', value: user.role },
    { label: 'Trạng thái', value: user.status },
    { label: 'Ngày tạo', value: formatDate(user.created_at) },
    { label: 'Cập nhật gần nhất', value: formatDate(user.updated_at) },
  ];
}

export function renderUserRow(user: AdminUserProfile): AdminScreenRow {
  return {
    values: [
      displayValue(user.id),
      user.full_name,
      user.email,
      user.role,
      user.status,
      formatDate(user.created_at),
    ],
    route: `/admin/users/${encodeURIComponent(String(user.id))}`,
  };
}

export function renderCourseFields(course: AdminCourse | undefined): readonly AdminScreenField[] {
  if (!course) {
    return [];
  }
  return [
    { label: 'Mã khóa học', value: displayValue(course.id) },
    { label: 'Tên khóa học', value: course.title },
    { label: 'Mô tả', value: displayValue(course.description) },
    { label: 'Mô tả ngắn', value: '' },
    { label: 'Chủ khóa học', value: course.mentor.full_name },
    { label: 'Mã mentor', value: displayValue(course.mentor.id) },
    { label: 'Giá', value: course.price },
    { label: 'Trạng thái', value: course.status },
    { label: 'Ảnh đại diện', value: displayValue(course.thumbnail_url) },
  ];
}

export function renderCourseRow(course: AdminCourse): AdminScreenRow {
  return {
    values: [
      displayValue(course.id),
      course.title,
      displayValue(course.description),
      course.mentor.full_name,
      course.price,
      course.status,
    ],
    route: `/admin/courses/${encodeURIComponent(String(course.id))}`,
  };
}

export function renderContentRow(content: AdminContent): AdminScreenRow {
  return {
    values: [
      displayInt64(content.id),
      content.title,
      displayInt64(content.course_id),
      content.content_type,
      displayValue(content.order),
      content.status,
    ],
    ...(Number.isSafeInteger(content.id)
      ? { route: `/admin/content/${encodeURIComponent(String(content.id))}/review` }
      : {}),
  };
}

function displayInt64(value: number | null): string {
  if (value === null) {
    return '—';
  }
  return Number.isSafeInteger(value) ? String(value) : 'Không thể hiển thị chính xác';
}

export function renderContentFields(content: AdminContent): readonly AdminScreenField[] {
  return [
    { label: 'Mã nội dung', value: displayValue(content.id) },
    { label: 'Tiêu đề', value: content.title },
    { label: 'Loại nội dung', value: content.content_type },
    { label: 'Trạng thái', value: content.status },
    { label: 'Mã khóa học', value: displayValue(content.course_id) },
    { label: 'Mã nội dung cha', value: displayValue(content.parent_id) },
    { label: 'Thứ tự', value: displayValue(content.order) },
    { label: 'Payload', value: JSON.stringify(content.payload, null, 2) },
  ];
}

export function renderLessonRow(lesson: AdminLesson): AdminScreenRow {
  return {
    values: [
      displayValue(lesson.id),
      lesson.title,
      displayValue(lesson.course_id),
      displayValue(lesson.order),
      lesson.status,
    ],
    route: `/admin/lessons/${encodeURIComponent(String(lesson.id))}`,
  };
}

export function renderLessonFields(lesson: AdminLesson): readonly AdminScreenField[] {
  return [
    { label: 'Mã bài học', value: displayValue(lesson.id) },
    { label: 'Tiêu đề', value: lesson.title },
    { label: 'Nội dung', value: displayValue(lesson.content) },
    { label: 'Nội dung bài học', value: displayValue(lesson.content) },
    { label: 'Mã khóa học', value: displayValue(lesson.course_id) },
    { label: 'Trạng thái', value: lesson.status },
    { label: 'URL video', value: displayValue(lesson.video_url) },
    { label: 'Thứ tự hiển thị', value: displayValue(lesson.order) },
  ];
}

export function renderQuizRow(quiz: AdminQuiz): AdminScreenRow {
  return {
    values: [
      displayInt64(quiz.id),
      quiz.title,
      displayInt64(quiz.course_id),
      displayValue(quiz.duration_minutes),
      quiz.passing_score,
    ],
    ...(Number.isSafeInteger(quiz.id)
      ? { route: `/admin/quizzes/${encodeURIComponent(String(quiz.id))}/statistics` }
      : {}),
  };
}

export function renderQuizStatistics(stats: AdminQuizStatistics): readonly AdminScreenMetric[] {
  return [
    { label: 'Mã Quiz', value: displayInt64(stats.quiz_id) },
    { label: 'Lượt làm bài', value: displayInt64(stats.attempt_count) },
    { label: 'Lượt nộp bài', value: displayInt64(stats.submitted_attempt_count) },
    { label: 'Lượt đã chấm', value: displayInt64(stats.graded_attempt_count) },
    { label: 'Điểm trung bình', value: displayValue(stats.average_score) },
    { label: 'Lượt đạt', value: displayInt64(stats.passed_attempt_count) },
    { label: 'Tỷ lệ đạt (%)', value: displayValue(stats.pass_rate_percent) },
  ];
}

export function renderNotificationRow(notification: Pick<AdminNotification, 'id' | 'title' | 'content' | 'channels' | 'status' | 'created_at'>): AdminScreenRow {
  return {
    values: [
      displayInt64(notification.id),
      notification.title,
      notification.content,
      notification.channels.join(', '),
      notification.status,
      formatDate(notification.created_at),
    ],
    ...(Number.isSafeInteger(notification.id)
      ? { route: `/admin/notifications/${encodeURIComponent(String(notification.id))}` }
      : {}),
  };
}

export function renderNotificationStatusFields(notification: AdminNotification): readonly AdminScreenField[] {
  return [
    { label: 'Mã thông báo', value: displayInt64(notification.id) },
    { label: 'Tiêu đề', value: notification.title },
    { label: 'Nội dung', value: notification.content },
    { label: 'Kênh', value: notification.channels.join(', ') },
    { label: 'Trạng thái tổng hợp', value: notification.status },
    { label: 'Ngày tạo', value: formatDate(notification.created_at) },
  ];
}

export function renderDiscussionRow(discussion: AdminDiscussion): AdminScreenRow {
  return {
    values: [
      displayInt64(discussion.id),
      discussion.title,
      discussion.content,
      discussion.author.full_name,
      displayInt64(discussion.course_id),
      discussion.status,
    ],
    ...(Number.isSafeInteger(discussion.id)
      ? { route: `/admin/discussions/${encodeURIComponent(String(discussion.id))}/moderate` }
      : {}),
  };
}

export function renderDiscussionFields(discussion: AdminDiscussion): readonly AdminScreenField[] {
  return [
    { label: 'Mã thảo luận', value: displayInt64(discussion.id) },
    { label: 'Tiêu đề', value: displayValue(discussion.title) },
    { label: 'Nội dung', value: discussion.content },
    { label: 'Tác giả', value: discussion.author.full_name },
    { label: 'Mã tác giả', value: displayInt64(discussion.author.id) },
    { label: 'Mã khóa học', value: displayInt64(discussion.course_id) },
    { label: 'Trạng thái', value: discussion.status },
  ];
}

export function renderDiscussionComments(discussion: AdminDiscussion): readonly AdminScreenSection[] {
  return [
    {
      title: 'Bình luận trực tiếp',
      description: 'Các bình luận trực tiếp có trong response của API #98.',
      items: discussion.comments.map(
        (comment) => `${comment.author.full_name}: ${comment.content} (${formatDate(comment.created_at)})`,
      ),
    },
  ];
}
