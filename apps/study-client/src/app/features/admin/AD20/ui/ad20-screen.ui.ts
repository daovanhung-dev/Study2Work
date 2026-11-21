import type { AdminScreenDefinition } from '../../../../shared/ui/admin-screen.model';

export const AD20_UI: Pick<AdminScreenDefinition, 'id' | 'title' | 'eyebrow' | 'description' | 'mode' | 'fields' | 'actions' | 'links'> = {
  "id": "AD20",
  "title": "Soạn thông báo hệ thống",
  "eyebrow": "Thông báo hệ thống",
  "description": "Chọn từng người nhận, kênh gửi và nội dung. Study Server xác nhận yêu cầu đã được xếp hàng; trạng thái gửi được theo dõi riêng.",
  "mode": "compose",
  "fields": [
    "Người nhận",
    "Kênh gửi",
    "Tiêu đề",
    "Nội dung"
  ],
  "actions": [
    {
      "label": "Gửi thông báo",
      "reason": "Gửi recipients tường minh tới #93 và chuyển tới SH-07 khi server xác nhận QUEUED."
    }
  ],
  "links": [
    {
      "label": "Danh sách thông báo",
      "route": "/admin/notifications"
    }
  ]
};
