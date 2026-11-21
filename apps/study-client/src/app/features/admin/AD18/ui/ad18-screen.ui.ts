import type { AdminScreenDefinition } from '../../../../shared/ui/admin-screen.model';

export const AD18_UI: Pick<AdminScreenDefinition, 'id' | 'title' | 'eyebrow' | 'description' | 'mode' | 'actions' | 'links'> = {
  "id": "AD18",
  "title": "Xóa bài kiểm tra",
  "eyebrow": "Quản lý bài kiểm tra",
  "description": "Chưa thể xác nhận thao tác vì chưa có dữ liệu Quiz, lịch sử liên quan và chính sách xóa được phê duyệt.",
  "mode": "delete",
  "actions": [
    {
      "label": "Xác nhận xóa bài kiểm tra",
      "reason": "Chưa có phê duyệt chính sách, quyền và dữ liệu kiểm tra tác động.",
      "destructive": true
    }
  ],
  "links": [
    {
      "label": "Quay lại danh sách",
      "route": "/admin/quizzes"
    }
  ]
};
