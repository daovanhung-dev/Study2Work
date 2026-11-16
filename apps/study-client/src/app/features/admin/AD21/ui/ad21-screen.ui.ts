import type { AdminScreenDefinition } from '../../../../shared/ui/admin-screen.model';

export const AD21_UI: Pick<AdminScreenDefinition, 'id' | 'title' | 'eyebrow' | 'description' | 'mode' | 'fields' | 'links'> = {
  "id": "AD21",
  "title": "Kiểm soát và giám sát trạng thái thông báo",
  "eyebrow": "Thông báo hệ thống",
  "description": "Trạng thái tổng hợp notification. API hiện tại không trả người nhận hoặc tiến độ theo từng kênh.",
  "mode": "status",
  "fields": [
    "Tiêu đề",
    "Nội dung",
    "Trạng thái tổng hợp"
  ],
  "links": [
    {
      "label": "Danh sách thông báo",
      "route": "/admin/notifications"
    }
  ]
};
