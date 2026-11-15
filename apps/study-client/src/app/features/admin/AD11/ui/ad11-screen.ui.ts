import type { AdminScreenDefinition } from '../../../../shared/ui/admin-screen.model';

export const AD11_UI: Pick<AdminScreenDefinition, 'id' | 'title' | 'eyebrow' | 'description' | 'mode' | 'links'> = {
  "id": "AD11",
  "title": "Thẩm định và phê duyệt nội dung bài giảng",
  "eyebrow": "Kiểm duyệt nội dung",
  "description": "Xem trước nội dung, đối chiếu thông tin và mở quyết định khi policy kiểm duyệt được xác nhận.",
  "mode": "review",
  "links": [
    {
      "label": "Quay lại hàng chờ",
      "route": "/admin/content/pending"
    }
  ]
};
