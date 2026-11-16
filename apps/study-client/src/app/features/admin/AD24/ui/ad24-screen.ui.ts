import type { AdminScreenDefinition } from '../../../../shared/ui/admin-screen.model';

export const AD24_UI: Pick<AdminScreenDefinition, 'id' | 'title' | 'eyebrow' | 'description' | 'mode' | 'actions'> = {
  "id": "AD24",
  "title": "Báo cáo tác động cộng đồng",
  "eyebrow": "Báo cáo",
  "description": "Bộ lọc và vùng báo cáo đang chờ API #101/#102 cùng công thức, phạm vi ngày và phân khúc được xác nhận.",
  "mode": "report",
  "actions": [
    {
      "label": "Áp dụng bộ lọc",
      "reason": "API #101/#102 chưa có route hoặc contract thực thi."
    },
    {
      "label": "Đặt lại",
      "reason": "Chưa có ngày mặc định hoặc bộ giá trị phân khúc được xác nhận."
    },
    {
      "label": "Làm mới truy vấn",
      "reason": "Không có endpoint báo cáo để gọi."
    },
    {
      "label": "Xuất báo cáo (AD-25)",
      "reason": "Handoff filter và contract #103/#18 chưa được thống nhất."
    }
  ]
};
