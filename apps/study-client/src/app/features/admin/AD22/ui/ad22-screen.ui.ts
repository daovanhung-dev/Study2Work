import type { AdminScreenDefinition } from '../../../../shared/ui/admin-screen.model';

export const AD22_UI: Pick<AdminScreenDefinition, 'id' | 'title' | 'eyebrow' | 'description' | 'mode' | 'columns' | 'filters'> = {
  "id": "AD22",
  "title": "Thảo luận được báo cáo",
  "eyebrow": "Kiểm duyệt cộng đồng",
  "description": "Hàng đợi thảo luận theo report còn mở hoặc đang xem xét. Mỗi discussion xuất hiện một lần.",
  "mode": "list",
  "columns": [
    "Mã thảo luận",
    "Tiêu đề từ nội dung",
    "Nội dung",
    "Tác giả",
    "Mã khóa học",
    "Trạng thái thảo luận"
  ],
  "filters": [
    { "key": "reason", "label": "Lý do báo cáo", "type": "text", "placeholder": "Giá trị chính xác" },
    { "key": "severity", "label": "Mức độ", "type": "text", "placeholder": "Giá trị chính xác" }
  ]
};
