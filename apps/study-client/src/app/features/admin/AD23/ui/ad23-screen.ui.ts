import type { AdminScreenDefinition } from '../../../../shared/ui/admin-screen.model';

export const AD23_UI: Pick<AdminScreenDefinition, 'id' | 'title' | 'eyebrow' | 'description' | 'mode' | 'actions' | 'links'> = {
  "id": "AD23",
  "title": "Điều tra và kiểm duyệt thảo luận",
  "eyebrow": "Kiểm duyệt cộng đồng",
  "description": "Đọc thảo luận và bình luận trực tiếp. API #98 không trả quan hệ hoặc metadata report.",
  "mode": "moderation",
  "actions": [
    {
      "label": "Ẩn thảo luận",
      "reason": "Chưa có API và policy được xác nhận."
    },
    {
      "label": "Cảnh cáo người dùng",
      "reason": "Chưa có API và policy được xác nhận."
    },
    {
      "label": "Xóa thảo luận",
      "reason": "Chưa xác định xóa mềm/vĩnh viễn hoặc kiểm toán.",
      "destructive": true
    }
  ],
  "links": [
    {
      "label": "Danh sách thảo luận được báo cáo",
      "route": "/admin/discussions/reported"
    }
  ]
};
