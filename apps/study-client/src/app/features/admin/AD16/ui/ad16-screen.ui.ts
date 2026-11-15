import type { AdminScreenDefinition } from '../../../../shared/ui/admin-screen.model';

export const AD16_UI: Pick<AdminScreenDefinition, 'id' | 'title' | 'eyebrow' | 'description' | 'mode' | 'fields' | 'links'> = {
  "id": "AD16",
  "title": "Tạo hoặc chỉnh sửa bài kiểm tra",
  "eyebrow": "Quản lý bài kiểm tra",
  "description": "Tạo bản nháp Quiz trong trang. Câu hỏi, dữ liệu nạp khi chỉnh sửa và thao tác lưu còn chờ contract được xác nhận.",
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
