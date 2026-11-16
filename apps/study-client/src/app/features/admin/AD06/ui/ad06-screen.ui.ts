import type { AdminScreenDefinition } from '../../../../shared/ui/admin-screen.model';

export const AD06_UI: Pick<AdminScreenDefinition, 'id' | 'title' | 'eyebrow' | 'description' | 'mode' | 'columns' | 'filters'> = {
  "id": "AD06",
  "title": "Quản lý danh mục khóa học",
  "eyebrow": "Quản lý khóa học",
  "description": "Danh sách khóa học theo API quản trị #73. Bộ lọc và thao tác khác vẫn khóa khi hợp đồng sản phẩm chưa được xác nhận.",
  "mode": "list",
  "columns": [
    "Mã định danh",
    "Tên khóa học",
    "Giảng viên hướng dẫn",
    "Học phí",
    "Trạng thái"
  ],
  "filters": [
    { "key": "status", "label": "Trạng thái", "type": "text", "placeholder": "Nhập trạng thái chính xác" },
    { "key": "mentor", "label": "Mã mentor", "type": "number", "placeholder": "ID mentor" }
  ]
};
