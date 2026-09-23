# Diagrams — WMB_HOME_DASHBOARD

```mermaid
flowchart LR
  A[Doanh nghiệp] --> V[Trang chủ và thông tin doanh nghiệp]
  V --> C[Current view/controller]
  C --> D[Dashboard đọc cache/CV projection và dữ liệu local presentation]
  C --> O[Current UI result/side effect]
```

Sơ đồ mô tả current behavior, không phải target architecture.

