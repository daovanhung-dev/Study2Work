# Diagrams — WMS_CV_MANAGEMENT

```mermaid
flowchart LR
  A[Sinh viên] --> V[Quản lý CV sinh viên]
  V --> C[Current view/controller]
  C --> D[Cached student id từ SQLite]
  C --> O[Current UI result/side effect]
```

Sơ đồ mô tả current behavior, không phải target architecture.

