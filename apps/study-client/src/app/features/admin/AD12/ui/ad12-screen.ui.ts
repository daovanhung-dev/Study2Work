import type { AdminScreenDefinition } from '../../../../shared/ui/admin-screen.model';

export const AD12_UI: Pick<AdminScreenDefinition, 'id' | 'title' | 'eyebrow' | 'description' | 'mode' | 'columns' | 'filters'> = {
  "id": "AD12",
  "title": "Danh sách bài học hệ thống",
  "eyebrow": "Quản lý bài học",
  "description": "Danh sách bài học từ API quản trị #82. API hiện không có phân trang, tìm kiếm hoặc loại nội dung.",
  "mode": "list",
  "columns": [
    "Mã bài học",
    "Tiêu đề",
    "ID khóa học",
    "Thứ tự",
    "Trạng thái"
  ]
};
