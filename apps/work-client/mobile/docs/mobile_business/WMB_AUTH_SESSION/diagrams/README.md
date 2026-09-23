# Diagrams — WMB_AUTH_SESSION

```mermaid
flowchart LR
  A[Doanh nghiệp] --> V[Xác thực và phiên doanh nghiệp]
  V --> C[Current view/controller]
  C --> D[Neon credential lookup qua helper]
  C --> O[Current UI result/side effect]
```

Sơ đồ mô tả current behavior, không phải target architecture.

