import type { AdminScreenDefinition } from '../../../../shared/ui/admin-screen.model';

export const AD17_UI: Pick<AdminScreenDefinition, 'id' | 'title' | 'eyebrow' | 'description' | 'mode' | 'metrics' | 'links'> = {
  "id": "AD17",
  "title": "Thống kê bài kiểm tra",
  "eyebrow": "Quản lý bài kiểm tra",
  "description": "Đọc projection thống kê từ API #91 hiện tại. Contract catalog và DTO local còn khác nhau; ý nghĩa metric chưa được phê duyệt.",
  "mode": "statistics",
  "metrics": [
    "Lượt làm bài",
    "Lượt nộp bài",
    "Lượt đã chấm",
    "Điểm trung bình",
    "Lượt đạt",
    "Tỷ lệ đạt (%)"
  ],
  "links": [
    {
      "label": "Danh sách bài kiểm tra",
      "route": "/admin/quizzes"
    }
  ]
};
