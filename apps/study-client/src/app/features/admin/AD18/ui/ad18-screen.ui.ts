import type { AdminScreenDefinition } from '../../../../shared/ui/admin-screen.model';

export const AD18_UI: Pick<AdminScreenDefinition, 'id' | 'title' | 'eyebrow' | 'description' | 'mode' | 'actions' | 'links'> = {
  "id": "AD18",
  "title": "Xóa bài kiểm tra",
  "eyebrow": "Quản lý bài kiểm tra",
  "description": "Xem trạng thái cổng xác nhận. Màn hình chưa có dữ liệu đọc để đối chiếu Quiz hoặc lịch sử tác động.",
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
