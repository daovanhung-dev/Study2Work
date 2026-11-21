import type { AdminScreenApiBoundary } from '../../../../shared/ui/admin-screen.model';

export const AD24_API_BOUNDARY: AdminScreenApiBoundary = {
  "apiReferences": [
    "#101",
    "#102"
  ],
  "sourceState": "api-absent",
  "sourceNote": "AD-24 route/page và Admin session gate có trong Study Client; API #101/#102 vẫn UNWIRED và không có Study Server route/query/model/test. Không gửi report request; date/segment, KPI, chart và export tiếp tục bị khóa."
};
