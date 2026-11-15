import type { AdminScreenDefinition } from '../../../../shared/ui/admin-screen.model';

export const AD09_UI: Pick<AdminScreenDefinition, 'id' | 'title' | 'eyebrow' | 'description' | 'mode' | 'actions' | 'links'> = {
  "id": "AD09",
  "title": "Thao tác khóa học",
  "eyebrow": "Quản lý khóa học",
  "description": "Trạng thái và thao tác xóa khóa học cần theo đúng quy tắc chuyển trạng thái và phụ thuộc đã duyệt.",
  "mode": "actions",
  "actions": [
    {
      "label": "Cập nhật trạng thái",
      "reason": "Chưa có enum và transition policy được xác nhận."
    },
    {
      "label": "Đánh dấu xóa",
      "reason": "Chưa xác nhận dependency và lifecycle của khóa học.",
      "destructive": true
    }
  ],
  "links": [
    {
      "label": "Quay lại chi tiết",
      "route": "/admin/courses/:courseId"
    }
  ]
};
