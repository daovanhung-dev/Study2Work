import type { AdminScreenDefinition } from '../../../../shared/ui/admin-screen.model';

export const AD05_UI: Pick<AdminScreenDefinition, 'id' | 'title' | 'eyebrow' | 'description' | 'mode' | 'actions' | 'links'> = {
  "id": "AD05",
  "title": "Khóa, mở khóa hoặc xóa tài khoản",
  "eyebrow": "Quản trị người dùng",
  "description": "Các thao tác tài khoản chỉ có thể thực hiện khi chính sách trạng thái, phiên đăng nhập, xóa và kiểm toán được xác nhận.",
  "mode": "actions",
  "actions": [
    {
      "label": "Khóa tài khoản",
      "reason": "Chưa có trạng thái đích và quy tắc chuyển trạng thái được duyệt."
    },
    {
      "label": "Mở khóa tài khoản",
      "reason": "Chưa có trạng thái đích và quy tắc chuyển trạng thái được duyệt."
    },
    {
      "label": "Xóa tài khoản",
      "reason": "Chưa xác nhận chính sách xóa, ảnh hưởng phiên hoặc kiểm toán.",
      "destructive": true
    }
  ],
  "links": [
    {
      "label": "Quay lại hồ sơ",
      "route": "/admin/users/:userId"
    }
  ]
};
