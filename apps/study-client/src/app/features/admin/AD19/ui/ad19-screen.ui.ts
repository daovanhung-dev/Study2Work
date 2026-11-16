import type { AdminScreenDefinition } from '../../../../shared/ui/admin-screen.model';

export const AD19_UI: Pick<AdminScreenDefinition, 'id' | 'title' | 'eyebrow' | 'description' | 'mode' | 'columns' | 'links' | 'filters'> = {
  "id": "AD19",
  "title": "Danh sách thông báo",
  "eyebrow": "Thông báo hệ thống",
  "description": "Danh sách thông báo có delivery theo API #92. Bộ lọc dùng trạng thái và kênh raw của source.",
  "mode": "list",
  "columns": [
    "Mã thông báo",
    "Tiêu đề",
    "Nội dung",
    "Kênh",
    "Trạng thái",
    "Ngày tạo"
  ],
  "links": [
    {
      "label": "Soạn thông báo",
      "route": "/admin/notifications/new"
    }
  ],
  "filters": [
    { "key": "status", "label": "Trạng thái", "type": "text", "placeholder": "FAILED, QUEUED hoặc SENT" },
    { "key": "channel", "label": "Kênh", "type": "text", "placeholder": "EMAIL hoặc PUSH" }
  ]
};
