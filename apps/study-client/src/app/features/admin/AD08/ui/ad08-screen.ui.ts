import type { AdminScreenDefinition } from '../../../../shared/ui/admin-screen.model';

export const AD08_UI: Pick<AdminScreenDefinition, 'id' | 'title' | 'eyebrow' | 'description' | 'mode' | 'fields' | 'links'> = {
  "id": "AD08",
  "title": "Chỉnh sửa khóa học",
  "eyebrow": "Quản lý khóa học",
  "description": "Nạp projection khóa học và cho phép xem bản nháp cục bộ. Thao tác cập nhật và upload thumbnail vẫn chờ contract được xác nhận.",
  "mode": "edit",
  "fields": [
    "Tiêu đề",
    "Mô tả",
    "Học phí",
    "Thumbnail URL",
    "Mentor",
    "Trạng thái"
  ],
  "links": [
    {
      "label": "Quay lại chi tiết",
      "route": "/admin/courses/:courseId"
    }
  ]
};
