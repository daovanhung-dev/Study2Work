import type { AdminScreenDefinition } from '../../../../shared/ui/admin-screen.model';

export const AD07_UI: Pick<AdminScreenDefinition, 'id' | 'title' | 'eyebrow' | 'description' | 'mode' | 'fields' | 'links'> = {
  "id": "AD07",
  "title": "Chi tiết khóa học",
  "eyebrow": "Quản lý khóa học",
  "description": "Thông tin khóa học từ API quản trị. Số bài học, lượt đăng ký và chỉ số chất lượng không nằm trong projection hiện tại.",
  "mode": "detail",
  "fields": [
    "Mã khóa học",
    "Tên khóa học",
    "Mô tả",
    "Chủ khóa học",
    "Trạng thái"
  ],
  "links": [
    {
      "label": "Chỉnh sửa khóa học",
      "route": "/admin/courses/:courseId/edit"
    },
    {
      "label": "Thao tác khóa học",
      "route": "/admin/courses/:courseId/actions"
    },
    {
      "label": "Danh sách khóa học",
      "route": "/admin/courses"
    }
  ]
};
