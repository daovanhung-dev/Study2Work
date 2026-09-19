# Import/File map — WMB_HOME_DASHBOARD

## Source evidence

| File | Vai trò |
|---|---|
| `lib/views/trang_chu/main/trang_chu.dart` | Source evidence for WMB_HOME_DASHBOARD. |
| `lib/views/trang_chu/main/thong_bao.dart` | Source evidence for WMB_HOME_DASHBOARD. |
| `lib/views/trang_chu/main/thong_tin_chi_tiet.dart` | Source evidence for WMB_HOME_DASHBOARD. |
| `lib/views/trang_chu/main/xem_chi_tiet.dart` | Source evidence for WMB_HOME_DASHBOARD. |
| `lib/views/trang_chu/main/xem_chi_tiet_view.dart` | Source evidence for WMB_HOME_DASHBOARD. |
| `lib/controllers/trang_chu/xem_chi_tiet.dart` | Source evidence for WMB_HOME_DASHBOARD. |
| `lib/controllers/trang_chu/hien_thi_danh_sach_top_cv.dart` | Source evidence for WMB_HOME_DASHBOARD. |

## View/function mapping

| View | Function | Source |
|---|---|---|
| `TrangChu` | WMB_HOME_DASHBOARD-FN01 | `lib/views/trang_chu/main/trang_chu.dart` |
| `ThongBao` | WMB_HOME_DASHBOARD-FN02 | `lib/views/trang_chu/main/thong_bao.dart` |
| `ThongTinChiTiet` | WMB_HOME_DASHBOARD-FN03 | `lib/views/trang_chu/main/thong_tin_chi_tiet.dart` |
| `XemChiTiet` | WMB_HOME_DASHBOARD-FN04 | `lib/views/trang_chu/main/xem_chi_tiet.dart` |
| `XemChiTietView` | WMB_HOME_DASHBOARD-FN05 | `lib/views/trang_chu/main/xem_chi_tiet_view.dart` |

## Dependency direction

```text
View → controller/helper → NeonDatabase hoặc SQLite helper
View → model
View → MaterialPageRoute/local state
AI path → AIService → external Gemini chỉ khi exact source gọi
```

Không tạo Work HTTP API contract mới. Tên helper có Supabase chỉ là compatibility naming khi implementation current là Neon; không ghi credential literal.

