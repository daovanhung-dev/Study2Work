import type { AdminScreenDefinition } from '../../../../shared/ui/admin-screen.model';

export const AD16_UI: Pick<AdminScreenDefinition, 'id' | 'title' | 'eyebrow' | 'description' | 'mode' | 'fields' | 'links'> = {
  "id": "AD16",
  "title": "Tạo hoặc chỉnh sửa bài kiểm tra",
  "eyebrow": "Quản lý bài kiểm tra",
  "description": "Tạo Quiz từ cấu hình và câu hỏi theo current backend source; chế độ chỉnh sửa chờ API detail và contract #89.",
  "mode": "builder",
  "fields": [
    "Tên bài kiểm tra",
    "Khóa học áp dụng",
    "Thời lượng",
    "Điểm đạt yêu cầu"
  ],
  "links": [
    {
      "label": "Danh sách bài kiểm tra",
      "route": "/admin/quizzes"
    }
  ]
};
