import type { AdminScreenDefinition } from '../../../../shared/ui/admin-screen.model';

export const AD04_UI: Pick<AdminScreenDefinition, 'id' | 'title' | 'eyebrow' | 'description' | 'mode' | 'fields' | 'links'> = {
  "id": "AD04",
  "title": "Chỉnh sửa người dùng",
  "eyebrow": "Quản trị người dùng",
  "description": "Biểu mẫu hồ sơ người dùng. Trường và giá trị chỉ được gửi sau khi request body, quyền và mapping vai trò được duyệt.",
  "mode": "edit",
  "fields": [
    "Họ và tên",
    "Số điện thoại",
    "Ảnh đại diện",
    "Vai trò"
  ],
  "links": [
    {
      "label": "Quay lại hồ sơ",
      "route": "/admin/users/:userId"
    }
  ]
};
