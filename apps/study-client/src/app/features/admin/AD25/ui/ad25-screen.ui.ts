import type { AdminScreenDefinition } from '../../../../shared/ui/admin-screen.model';

export const AD25_UI: Pick<AdminScreenDefinition, 'id' | 'title' | 'eyebrow' | 'description' | 'mode' | 'fields' | 'links'> = {
  "id": "AD25",
  "title": "Trích xuất dữ liệu và theo dõi tiến trình xuất báo cáo",
  "eyebrow": "Báo cáo",
  "description": "Chỉ tạo tác vụ và tải artifact khi operation, trạng thái, lưu trữ và liên kết tải xuống có contract được xác nhận.",
  "mode": "export",
  "fields": [
    "Loại báo cáo",
    "Định dạng",
    "Khoảng thời gian",
    "Phân khúc"
  ],
  "links": [
    {
      "label": "Quay lại báo cáo tác động",
      "route": "/admin/reports/community-impact"
    }
  ]
};
