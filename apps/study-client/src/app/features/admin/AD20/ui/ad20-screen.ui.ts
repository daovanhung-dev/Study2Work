import type { AdminScreenDefinition } from '../../../../shared/ui/admin-screen.model';

export const AD20_UI: Pick<AdminScreenDefinition, 'id' | 'title' | 'eyebrow' | 'description' | 'mode' | 'fields' | 'actions' | 'links'> = {
  "id": "AD20",
  "title": "Soạn thông báo hệ thống",
  "eyebrow": "Thông báo hệ thống",
  "description": "Soạn nội dung xem trước tại chỗ. Người nhận, kênh, lưu nháp và gửi vẫn khóa trong khi contract #93/#18 chưa thống nhất.",
  "mode": "compose",
  "fields": [
    "Người nhận",
    "Kênh gửi",
    "Tiêu đề",
    "Nội dung"
  ],
  "actions": [
    {
      "label": "Lưu bản nháp",
      "reason": "#93 không có request hoặc endpoint lưu nháp."
    },
    {
      "label": "Gửi thông báo",
      "reason": "Audience, permission, response và delivery contract chưa được xác nhận."
    }
  ],
  "links": [
    {
      "label": "Danh sách thông báo",
      "route": "/admin/notifications"
    }
  ]
};
