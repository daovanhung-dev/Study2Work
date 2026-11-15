import type { AdminScreenDefinition } from '../../../../shared/ui/admin-screen.model';

export const AD15_UI: Pick<AdminScreenDefinition, 'id' | 'title' | 'eyebrow' | 'description' | 'mode' | 'columns' | 'links' | 'filters'> = {
  "id": "AD15",
  "title": "Danh sách bài kiểm tra",
  "eyebrow": "Quản lý bài kiểm tra",
  "description": "Danh sách metadata bài kiểm tra theo API #87. Tìm kiếm và số câu hỏi thực tế không có trong response.",
  "mode": "list",
  "columns": [
    "Mã bài kiểm tra",
    "Tên bài kiểm tra",
    "Mã khóa học",
    "Thời lượng (phút)",
    "Điểm đạt"
  ],
  "links": [
    {
      "label": "Tạo bài kiểm tra",
      "route": "/admin/quizzes/new"
    }
  ],
  "filters": [
    { "key": "course", "label": "Mã khóa học", "type": "text", "placeholder": "ID khóa học (int64)" },
    { "key": "status", "label": "Trạng thái", "type": "text", "placeholder": "Nhập trạng thái chính xác" }
  ]
};
