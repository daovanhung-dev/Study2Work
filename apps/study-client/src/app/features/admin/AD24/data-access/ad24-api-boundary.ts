import type { AdminScreenApiBoundary } from '../../../../shared/ui/admin-screen.model';

export const AD24_API_BOUNDARY: AdminScreenApiBoundary = {
  "apiReferences": [
    "#101",
    "#102"
  ],
  "sourceState": "api-absent",
  "sourceNote": "Study Server hiện không có route, query, model hoặc test cho #101/#102; không có KPI, date filter hay segment có thể gọi. Export handoff sang #103/#18 cũng chưa rõ."
};
