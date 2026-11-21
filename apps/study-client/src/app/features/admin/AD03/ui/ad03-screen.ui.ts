import type { AdminScreenDefinition } from '../../../../shared/ui/admin-screen.model';

export const AD03_UI: Pick<AdminScreenDefinition, 'id' | 'title' | 'eyebrow' | 'description' | 'mode' | 'fields' | 'links' | 'sections'> = {
  "id": "AD03",
  "title": "Hồ sơ chi tiết tài khoản",
  "eyebrow": "Quản trị người dùng",
  "description": "Xem thông tin định danh, vai trò và trạng thái tài khoản từ API quản trị.",
  "mode": "detail",
  "fields": [
    "Mã người dùng",
    "Họ và tên",
    "Email",
    "Vai trò",
    "Trạng thái"
  ],
  "links": [
    {
      "label": "Chỉnh sửa hồ sơ",
      "route": "/admin/users/:userId/edit"
    },
    {
      "label": "Thao tác tài khoản",
      "route": "/admin/users/:userId/actions"
    },
    {
      "label": "Danh sách người dùng",
      "route": "/admin/users"
    }
  ],
  "sections": [
    {
      "title": "Hoạt động gần đây",
      "description": "Không có API nhật ký kiểm toán trong contract hiện tại."
    }
  ]
};
