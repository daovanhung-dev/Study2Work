import type { AdminScreenDefinition } from '../../../../shared/ui/admin-screen.model';

export const AD14_UI: Pick<AdminScreenDefinition, 'id' | 'title' | 'eyebrow' | 'description' | 'mode' | 'fields' | 'links'> = {
  "id": "AD14",
  "title": "Chỉnh sửa bài học",
  "eyebrow": "Quản lý bài học",
  "description": "Nạp Lesson từ API #83 và giữ thay đổi biên tập trong bộ nhớ trang. Cập nhật, đổi trạng thái và xóa vẫn chờ contract được xác nhận.",
  "mode": "edit",
  "fields": [
    "Tiêu đề",
    "Nội dung bài học",
    "Course ID",
    "URL video",
    "Thứ tự hiển thị",
    "Trạng thái"
  ],
  "links": [
    {
      "label": "Quay lại chi tiết",
      "route": "/admin/lessons/:lessonId"
    }
  ]
};
