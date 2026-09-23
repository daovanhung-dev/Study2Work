# Import/File map — WMS_HOME_DASHBOARD

## Source evidence

| File | Vai trò |
|---|---|
| `lib/views/trang_chu/main/trang_chu.dart` | Source evidence for WMS_HOME_DASHBOARD. |
| `lib/views/trang_chu/main/thong_bao.dart` | Source evidence for WMS_HOME_DASHBOARD. |
| `lib/views/trang_chu/main/thong_tin_chi_tiet.dart` | Source evidence for WMS_HOME_DASHBOARD. |
| `lib/views/trang_chu/main/xem_chi_tiet.dart` | Source evidence for WMS_HOME_DASHBOARD. |
| `lib/controllers/trang_chu/trang_chu_ctrl.dart` | Source evidence for WMS_HOME_DASHBOARD. |
| `lib/controllers/trang_chu/xem_chi_tiet.dart` | Source evidence for WMS_HOME_DASHBOARD. |
| `lib/helper_db/sinh_vien/helper_supabase.dart` | Source evidence for WMS_HOME_DASHBOARD. |
| `lib/models/sinh_vien/jd.dart` | Source evidence for WMS_HOME_DASHBOARD. |

## View/function mapping

| View | Function | Source |
|---|---|---|
| `TrangChu` | WMS_HOME_DASHBOARD-FN01 | `lib/views/trang_chu/main/trang_chu.dart` |
| `ThongBao` | WMS_HOME_DASHBOARD-FN02 | `lib/views/trang_chu/main/thong_bao.dart` |
| `ThongTinChiTiet` | WMS_HOME_DASHBOARD-FN03 | `lib/views/trang_chu/main/thong_tin_chi_tiet.dart` |
| `XemChiTiet` | WMS_HOME_DASHBOARD-FN04 | `lib/views/trang_chu/main/xem_chi_tiet.dart` |
| `XemChiTietView` | Cross-feature dependency | `lib/views/trang_chu/main/xem_chi_tiet_view.dart` (inventory defined in WMS_JOB_SEARCH_APPLICATION) |

## Dependency direction

```text
View → controller/helper → NeonDatabase hoặc SQLite helper
View → model
View → MaterialPageRoute/local state
AI path → AIService → external Gemini chỉ khi exact source gọi
```

Không tạo Work HTTP API contract mới. Tên helper có Supabase chỉ là compatibility naming khi implementation current là Neon; không ghi credential literal.
