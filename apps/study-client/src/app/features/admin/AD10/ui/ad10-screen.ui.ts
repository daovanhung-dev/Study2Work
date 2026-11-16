import type { AdminScreenDefinition } from '../../../../shared/ui/admin-screen.model';

export const AD10_UI: Pick<AdminScreenDefinition, 'id' | 'title' | 'eyebrow' | 'description' | 'mode' | 'columns' | 'filters'> = {
  "id": "AD10",
  "title": "Nội dung chờ kiểm duyệt",
  "eyebrow": "Kiểm duyệt nội dung",
  "description": "Danh sách Content đang chờ kiểm duyệt, với bộ lọc type và mã khóa học theo API #78.",
  "mode": "list",
  "columns": [
    "Mã nội dung",
    "Tiêu đề",
    "Mã khóa học",
    "Loại nội dung",
    "Thứ tự",
    "Trạng thái"
  ],
  "filters": [
    { "key": "type", "label": "Loại nội dung", "type": "text", "placeholder": "Giá trị type chính xác" },
    { "key": "course", "label": "Mã khóa học", "type": "text", "placeholder": "ID khóa học (int64)" }
  ]
};
