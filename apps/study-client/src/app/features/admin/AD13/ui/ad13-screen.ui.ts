import type { AdminScreenDefinition } from '../../../../shared/ui/admin-screen.model';

export const AD13_UI: Pick<AdminScreenDefinition, 'id' | 'title' | 'eyebrow' | 'description' | 'mode' | 'fields' | 'links'> = {
  "id": "AD13",
  "title": "Chi tiết bài học",
  "eyebrow": "Quản lý bài học",
  "description": "Thông tin bài học theo projection hiện tại. Chỉ số phụ thuộc, thao tác media và realtime chưa có contract.",
  "mode": "detail",
  "fields": [
    "Mã bài học",
    "Tiêu đề",
    "Nội dung",
    "Mã khóa học",
    "Trạng thái"
  ],
  "links": [
    {
      "label": "Chỉnh sửa bài học",
      "route": "/admin/lessons/:lessonId/edit"
    },
    {
      "label": "Danh sách bài học",
      "route": "/admin/lessons"
    }
  ]
};
