# SH-02 — Data Flow & State

## 1. Model
```ts
interface Chapter { id: string; title: string; lessonCount: number; }
interface CourseDetail {
  id: string; title: string; topic: string; level: string;
  description: string; durationMinutes: number | null;
  lessonsCount: number; chapters: Chapter[]; isEnrolled: boolean;
}
type FetchStatus = 'idle'|'loading'|'success'|'not-found'|'error';
type EnrollStatus = 'idle'|'submitting'|'success'|'error';
interface CourseDetailState {
  courseId: string; course: CourseDetail|null;
  fetchStatus: FetchStatus; enrollStatus: EnrollStatus;
  expandedChapterIds: string[]; errorMessage: string|null;
  isAuthenticated: boolean; requestSeq: number;
}
```

## 2. Sources and mappings
| Data | Source | Mapping | UI |
|---|---|---|---|
| `courseId` | router `:courseId` | decoded+validated | API-001 path; API-002 body |
| `isAuthenticated` | shared auth/session | boolean | `SH-02-EL-007` CTA |
| `title, description` | API-001 | strings; description default | `EL-003/005` |
| `topic, level` | API-001 | enum → Vietnamese labels, unknown fallback | `EL-004` |
| `duration_minutes` | API-001 | 540 → `9 giờ` | `EL-008` |
| `chapters[]` | API-001 | `lesson_count → lessonCount` | `EL-006` |
| `viewer.is_enrolled` | API-001 | null → false | `EL-007` |
| `enrollment_id` | API-002 | không cần hiển thị; không lưu PII | state only CTA |

## 3. Read flow
1. Router cấp courseId; validate theo BR-005.
2. Nếu không hợp lệ → `fetchStatus='not-found'` (không gọi API).
3. Nếu hợp lệ, set `fetchStatus='loading'`, clear old course, increase requestSeq, GET API-001.
4. 200: map DTO, set `fetchStatus='success'`, init `expandedChapterIds=[]`.
5. 404: `not-found`; network/5xx: `error`; stale response sau route change bỏ qua.

## 4. Write flow (Enroll)
1. User click CTA; lấy `courseId` từ current route và auth state.
2. Nếu anonymous → route login với returnUrl; không gửi API-002.
3. Nếu đã enrolled/submitting → không gửi POST.
4. Nếu authenticated + unenrolled, set `enrollStatus='submitting'`, disable CTA; POST API-002.
5. 201 hoặc 409 ALREADY_ENROLLED → `course.isEnrolled=true`, CTA `Đã đăng ký`.
6. 401 → redirect login; các lỗi khác → `enrollStatus='error'`, CTA cho retry thủ công.

## 5. Local state, concurrency và cleanup
- Accordion: toggle chapter ID trong `expandedChapterIds`; không thay đổi dữ liệu backend.
- Nếu `courseId` thay đổi trên cùng component: reset course/accordion/enroll status, ignore response của ID trước.
- Không ghi token vào DD hay browser local storage từ component; sử dụng shared auth layer.
- Cache: không cache màn detail trong demo; GET mỗi lần mount/route change.
- `fetchStatus='success'` mới cho CTA hoạt động.
