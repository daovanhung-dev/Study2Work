# Mobile tracked-file inventory

CONTEXT_STATUS: SOURCE_BACKED

Phạm vi: toàn bộ file được trả về bởi git ls-files apps/work-client/mobile tại source snapshot hiện tại (210 file). Loại trừ build/, .dart_tool/, cache và artefact sinh tự động.

Status: WIRED = có composition/import/route evidence; UNWIRED = implementation không có caller; PLACEHOLDER = UI skeleton; USED = asset có direct reference; DECLARED_NOT_REFERENCED = asset được khai báo nhưng không có direct reference; CONFIG = tooling/config; DOC_DISCREPANCY = tài liệu không khớp tracked source.

| App | Path | Kind | Purpose | Current status |
|---|---|---|---|---|
| Business | .gitignore | Config | Flutter project metadata or generated/local ignore rules. | CONFIG |
| Business | .metadata | Config | Flutter project metadata or generated/local ignore rules. | CONFIG |
| Business | README.md | Docs | Setup, features and security notes; README web-directory claim is not present in tracked source. | DOC_DISCREPANCY |
| Business | analysis_options.yaml | Config | Analyzer exclusions and Flutter lint configuration. | CONFIG |
| Business | android/.gitignore | Gradle | Android build, plugin, wrapper and JVM configuration. | CONFIG |
| Business | android/app/build.gradle.kts | Gradle | Android build, plugin, wrapper and JVM configuration. | CONFIG |
| Business | android/app/src/debug/AndroidManifest.xml | Android | Debug/profile INTERNET permission declaration. | CONFIG |
| Business | android/app/src/main/AndroidManifest.xml | Android | Launcher activity, app label and Flutter embedding metadata. | CONFIG |
| Business | android/app/src/main/kotlin/com/example/work_server/MainActivity.kt | Android | Minimal FlutterActivity host. | WIRED |
| Business | android/app/src/main/res/drawable-v21/launch_background.xml | AndroidAsset | Launcher icons, launch backgrounds and styles. | CONFIG |
| Business | android/app/src/main/res/drawable/launch_background.xml | AndroidAsset | Launcher icons, launch backgrounds and styles. | CONFIG |
| Business | android/app/src/main/res/mipmap-hdpi/ic_launcher.png | AndroidAsset | Launcher icons, launch backgrounds and styles. | CONFIG |
| Business | android/app/src/main/res/mipmap-mdpi/ic_launcher.png | AndroidAsset | Launcher icons, launch backgrounds and styles. | CONFIG |
| Business | android/app/src/main/res/mipmap-xhdpi/ic_launcher.png | AndroidAsset | Launcher icons, launch backgrounds and styles. | CONFIG |
| Business | android/app/src/main/res/mipmap-xxhdpi/ic_launcher.png | AndroidAsset | Launcher icons, launch backgrounds and styles. | CONFIG |
| Business | android/app/src/main/res/mipmap-xxxhdpi/ic_launcher.png | AndroidAsset | Launcher icons, launch backgrounds and styles. | CONFIG |
| Business | android/app/src/main/res/values-night/styles.xml | AndroidAsset | Launcher icons, launch backgrounds and styles. | CONFIG |
| Business | android/app/src/main/res/values/styles.xml | AndroidAsset | Launcher icons, launch backgrounds and styles. | CONFIG |
| Business | android/app/src/profile/AndroidManifest.xml | Android | Debug/profile INTERNET permission declaration. | CONFIG |
| Business | android/build.gradle.kts | Gradle | Android build, plugin, wrapper and JVM configuration. | CONFIG |
| Business | android/gradle.properties | Gradle | Android build, plugin, wrapper and JVM configuration. | CONFIG |
| Business | android/gradle/wrapper/gradle-wrapper.jar | Gradle | Android build, plugin, wrapper and JVM configuration. | CONFIG |
| Business | android/gradle/wrapper/gradle-wrapper.properties | Gradle | Android build, plugin, wrapper and JVM configuration. | CONFIG |
| Business | android/gradlew | Gradle | Android build, plugin, wrapper and JVM configuration. | CONFIG |
| Business | android/gradlew.bat | Gradle | Android build, plugin, wrapper and JVM configuration. | CONFIG |
| Business | android/settings.gradle.kts | Gradle | Android build, plugin, wrapper and JVM configuration. | CONFIG |
| Business | assets/avt.jpg | Asset | Bundled Flutter image/icon asset. | USED |
| Business | assets/bg_login.png | Asset | Bundled Flutter image/icon asset. | USED |
| Business | assets/bg_trangchu.jpg | Asset | Bundled Flutter image/icon asset. | USED |
| Business | assets/icon_login.png | Asset | Bundled Flutter image/icon asset. | DECLARED_NOT_REFERENCED |
| Business | assets/internship_tien_ich.png | Asset | Bundled Flutter image/icon asset. | USED |
| Business | assets/job_tien_ich.png | Asset | Bundled Flutter image/icon asset. | USED |
| Business | assets/loc_cv_tien_ich.png | Asset | Bundled Flutter image/icon asset. | USED |
| Business | assets/logo-nobr.png | Asset | Bundled Flutter image/icon asset. | USED |
| Business | assets/logo.jpg | Asset | Bundled Flutter image/icon asset. | USED |
| Business | assets/school_tien_ich.png | Asset | Bundled Flutter image/icon asset. | USED |
| Business | assets/thong_ke_tien_ich.png | Asset | Bundled Flutter image/icon asset. | USED |
| Business | assets/tien_ich1.png | Asset | Bundled Flutter image/icon asset. | USED |
| Business | assets/tien_ich2.png | Asset | Bundled Flutter image/icon asset. | USED |
| Business | devtools_options.yaml | Config | Flutter DevTools configuration. | CONFIG |
| Business | lib/constants.dart | Config | Prototype Neon/Gemini configuration symbols; secret literals omitted from context. | CONFIG |
| Business | lib/controllers/AI/ai_service.dart | Controller | Direct Gemini HTTP client. | SOURCE_BACKED |
| Business | lib/controllers/AI/view_test.dart | View/Test | Manual AI test screen without production route. | UNWIRED |
| Business | lib/controllers/cai_dat/cai_dat.dart | Controller | Logout and local session clearing. | WIRED |
| Business | lib/controllers/chat/chat_controller.dart | Controller | Chat query/send and three-second id-deduplicated polling. | WIRED |
| Business | lib/controllers/chat/nhung_doan_chat_controller.dart | Controller | Conversation-partner query from DoanChat. | WIRED |
| Business | lib/controllers/dang_nhap/dangnhap_ctrl.dart | Controller | Login orchestration between Neon and local SQLite. | WIRED |
| Business | lib/controllers/lay_ten.dart | Controller | Direct student/business name lookup; no active caller found. | UNWIRED |
| Business | lib/controllers/trang_chu/hien_thi_danh_sach_top_cv.dart | Controller | Home, top-CV, job-management, search or detail controller. | SOURCE_BACKED |
| Business | lib/controllers/trang_chu/quan_ly_job/quan_ly_job_ctrl.dart | Controller | Home, top-CV, job-management, search or detail controller. | SOURCE_BACKED |
| Business | lib/controllers/trang_chu/timkiemctrl.dart | Controller | Home, top-CV, job-management, search or detail controller. | SOURCE_BACKED |
| Business | lib/controllers/trang_chu/xem_chi_tiet.dart | Controller | CV detail projection query by candidate id. | SOURCE_BACKED |
| Business | lib/controllers/ung_vien/ung_vien_controller.dart | Controller | Application/candidate actions and side effects. | WIRED |
| Business | lib/dn.dart | Placeholder | Temporary empty StatefulWidget; outside active route graph. | PLACEHOLDER/UNWIRED |
| Business | lib/helper_db/helper_cv.dart | Helper | SQLite cache, Neon compatibility helpers, CV helpers or local UI builders. | SOURCE_BACKED |
| Business | lib/helper_db/helper_db.dart | Helper | SQLite cache, Neon compatibility helpers, CV helpers or local UI builders. | SOURCE_BACKED |
| Business | lib/helper_db/helper_supabase.dart | Helper | SQLite cache, Neon compatibility helpers, CV helpers or local UI builders. | SOURCE_BACKED |
| Business | lib/helper_db/helper_widget.dart | Helper | SQLite cache, Neon compatibility helpers, CV helpers or local UI builders. | SOURCE_BACKED |
| Business | lib/helper_db/neon_db.dart | DataBoundary | Neon singleton, SSL normalization, parameterized SQL and row normalization. | WIRED |
| Business | lib/main.dart | Entrypoint | MaterialApp bootstrap; starts at DangNhap. | WIRED |
| Business | lib/models/chat.dart | Model | Domain/compatibility models with DB row, JSON and date mapping. | SOURCE_BACKED |
| Business | lib/models/cv.dart | Model | Domain/compatibility models with DB row, JSON and date mapping. | SOURCE_BACKED |
| Business | lib/models/dn_supabase.dart | Model | Domain/compatibility models with DB row, JSON and date mapping. | SOURCE_BACKED |
| Business | lib/models/doanh_nghiep.dart | Model | Domain/compatibility models with DB row, JSON and date mapping. | SOURCE_BACKED |
| Business | lib/models/jd.dart | Model | Domain/compatibility models with DB row, JSON and date mapping. | SOURCE_BACKED |
| Business | lib/models/nganh_nghe.dart | Model | Domain/compatibility models with DB row, JSON and date mapping. | SOURCE_BACKED |
| Business | lib/models/ung_vien.dart | Model | Domain/compatibility models with DB row, JSON and date mapping. | SOURCE_BACKED |
| Business | lib/theme/app_components.dart | Theme | Local Cobalt tokens, Material 3 theme and reusable primitives. | WIRED |
| Business | lib/theme/app_theme.dart | Theme | Local Cobalt tokens, Material 3 theme and reusable primitives. | WIRED |
| Business | lib/theme/design_tokens.dart | Theme | Local Cobalt tokens, Material 3 theme and reusable primitives. | WIRED |
| Business | lib/views/cai_dat/setting.dart | View | Settings, notification navigation and logout. | WIRED |
| Business | lib/views/dang_nhap/dang_nhap.dart | View | Login, password-recovery and animated destination shell. | WIRED |
| Business | lib/views/dang_nhap/menu.dart | View | Login, password-recovery and animated destination shell. | WIRED |
| Business | lib/views/dang_nhap/quen_mat_khau.dart | View | Login, password-recovery and animated destination shell. | WIRED |
| Business | lib/views/kiem_tra_wifi.dart | View | Business connectivity screen not reached by current main route. | UNWIRED |
| Business | lib/views/trang_chu/main/dang_tin_tuyen_dung.dart | View | Home, notification, detail and job-posting surfaces. | SOURCE_BACKED |
| Business | lib/views/trang_chu/main/thong_bao.dart | View | Home, notification, detail and job-posting surfaces. | SOURCE_BACKED |
| Business | lib/views/trang_chu/main/thong_tin_chi_tiet.dart | View | Home, notification, detail and job-posting surfaces. | SOURCE_BACKED |
| Business | lib/views/trang_chu/main/trang_chu.dart | View | Home, notification, detail and job-posting surfaces. | SOURCE_BACKED |
| Business | lib/views/trang_chu/main/xem_chi_tiet.dart | View | Home, notification, detail and job-posting surfaces. | SOURCE_BACKED |
| Business | lib/views/trang_chu/main/xem_chi_tiet_view.dart | View | Home, notification, detail and job-posting surfaces. | SOURCE_BACKED |
| Business | lib/views/trang_chu/tien_ich/Chuong_trinh_thuc_te/chuong_trinh_thuc_tap.dart | View | Legacy internship screen retained beside the active page/form screen. | UNWIRED/LEGACY |
| Business | lib/views/trang_chu/tien_ich/Chuong_trinh_thuc_te/chuong_trinh_thuc_tap_page.dart | View | Internship-program listing and form screen. | WIRED |
| Business | lib/views/trang_chu/tien_ich/Lich_phong_van/lich_phong_van.dart | View | Student/business utility screens; active and legacy variants are documented per app. | SOURCE_BACKED |
| Business | lib/views/trang_chu/tien_ich/Lich_phong_van/lich_pv_page.dart | View | Student/business utility screens; active and legacy variants are documented per app. | SOURCE_BACKED |
| Business | lib/views/trang_chu/tien_ich/Lien_ket_nha_truong/lien_ket_nha_truong.dart | View | Student/business utility screens; active and legacy variants are documented per app. | SOURCE_BACKED |
| Business | lib/views/trang_chu/tien_ich/Loc_cv/loc_cv_filter.dart | View | Student/business utility screens; active and legacy variants are documented per app. | SOURCE_BACKED |
| Business | lib/views/trang_chu/tien_ich/Loc_cv/loc_cv_placeholder.dart | View | Student/business utility screens; active and legacy variants are documented per app. | SOURCE_BACKED |
| Business | lib/views/trang_chu/tien_ich/Quan_ly_job/chi_tiet_job.dart | View | Student/business utility screens; active and legacy variants are documented per app. | SOURCE_BACKED |
| Business | lib/views/trang_chu/tien_ich/Quan_ly_job/quan_ly_job.dart | View | Student/business utility screens; active and legacy variants are documented per app. | SOURCE_BACKED |
| Business | lib/views/trang_chu/tien_ich/Thong_ke/thong_ke.dart | View | Student/business utility screens; active and legacy variants are documented per app. | SOURCE_BACKED |
| Business | lib/views/trang_chu/tien_ich/Thong_ke/thong_ke_bao_cao.dart | View | Student/business utility screens; active and legacy variants are documented per app. | SOURCE_BACKED |
| Business | lib/views/trang_chu/tien_ich/Tim_kiem_nhan_su/tim_kiem_nhan_su.dart | View | Student/business utility screens; active and legacy variants are documented per app. | SOURCE_BACKED |
| Business | lib/views/tro_chuyen/chat.dart | View | Conversation list and polling chat screen. | WIRED |
| Business | lib/views/tro_chuyen/tro_chuyen.dart | View | Conversation list and polling chat screen. | WIRED |
| Business | lib/views/ung_vien/ung_vien.dart | View | Business candidate/application management screen. | WIRED |
| Business | pubspec.lock | Lockfile | Resolved Dart/Flutter dependency versions. | CONFIG |
| Business | pubspec.yaml | Package | Package identity, Dart SDK constraint, dependencies and asset declarations. | CONFIG |
| Business | test/neon_connection_test.dart | Test | Opt-in Neon SELECT 1 smoke test; skipped unless RUN_NEON_SMOKE=true. | DECLARED_NOT_RUNNABLE |
| Business | test/neon_test.dart | Test | URL/row/model normalization and polling cancellation tests. | SOURCE_BACKED |
| Student | .gitignore | Config | Flutter project metadata or generated/local ignore rules. | CONFIG |
| Student | .metadata | Config | Flutter project metadata or generated/local ignore rules. | CONFIG |
| Student | README.md | Docs | Setup, features and security notes; README web-directory claim is not present in tracked source. | DOC_DISCREPANCY |
| Student | analysis_options.yaml | Config | Analyzer exclusions and Flutter lint configuration. | CONFIG |
| Student | android/.gitignore | Gradle | Android build, plugin, wrapper and JVM configuration. | CONFIG |
| Student | android/app/build.gradle.kts | Gradle | Android build, plugin, wrapper and JVM configuration. | CONFIG |
| Student | android/app/src/debug/AndroidManifest.xml | Android | Debug/profile INTERNET permission declaration. | CONFIG |
| Student | android/app/src/main/AndroidManifest.xml | Android | Launcher activity, app label and Flutter embedding metadata. | CONFIG |
| Student | android/app/src/main/kotlin/com/example/work_server/MainActivity.kt | Android | Minimal FlutterActivity host. | WIRED |
| Student | android/app/src/main/res/drawable-v21/launch_background.xml | AndroidAsset | Launcher icons, launch backgrounds and styles. | CONFIG |
| Student | android/app/src/main/res/drawable/launch_background.xml | AndroidAsset | Launcher icons, launch backgrounds and styles. | CONFIG |
| Student | android/app/src/main/res/mipmap-hdpi/ic_launcher.png | AndroidAsset | Launcher icons, launch backgrounds and styles. | CONFIG |
| Student | android/app/src/main/res/mipmap-mdpi/ic_launcher.png | AndroidAsset | Launcher icons, launch backgrounds and styles. | CONFIG |
| Student | android/app/src/main/res/mipmap-xhdpi/ic_launcher.png | AndroidAsset | Launcher icons, launch backgrounds and styles. | CONFIG |
| Student | android/app/src/main/res/mipmap-xxhdpi/ic_launcher.png | AndroidAsset | Launcher icons, launch backgrounds and styles. | CONFIG |
| Student | android/app/src/main/res/mipmap-xxxhdpi/ic_launcher.png | AndroidAsset | Launcher icons, launch backgrounds and styles. | CONFIG |
| Student | android/app/src/main/res/values-night/styles.xml | AndroidAsset | Launcher icons, launch backgrounds and styles. | CONFIG |
| Student | android/app/src/main/res/values/styles.xml | AndroidAsset | Launcher icons, launch backgrounds and styles. | CONFIG |
| Student | android/app/src/profile/AndroidManifest.xml | Android | Debug/profile INTERNET permission declaration. | CONFIG |
| Student | android/build.gradle.kts | Gradle | Android build, plugin, wrapper and JVM configuration. | CONFIG |
| Student | android/gradle.properties | Gradle | Android build, plugin, wrapper and JVM configuration. | CONFIG |
| Student | android/gradle/wrapper/gradle-wrapper.jar | Gradle | Android build, plugin, wrapper and JVM configuration. | CONFIG |
| Student | android/gradle/wrapper/gradle-wrapper.properties | Gradle | Android build, plugin, wrapper and JVM configuration. | CONFIG |
| Student | android/gradlew | Gradle | Android build, plugin, wrapper and JVM configuration. | CONFIG |
| Student | android/gradlew.bat | Gradle | Android build, plugin, wrapper and JVM configuration. | CONFIG |
| Student | android/settings.gradle.kts | Gradle | Android build, plugin, wrapper and JVM configuration. | CONFIG |
| Student | assets/avt.jpg | Asset | Bundled Flutter image/icon asset. | USED |
| Student | assets/bg_login.png | Asset | Bundled Flutter image/icon asset. | DECLARED_NOT_REFERENCED |
| Student | assets/bg_trangchu.jpg | Asset | Bundled Flutter image/icon asset. | USED |
| Student | assets/calendar.png | Asset | Bundled Flutter image/icon asset. | USED |
| Student | assets/help-desk.png | Asset | Bundled Flutter image/icon asset. | USED |
| Student | assets/icon_login.png | Asset | Bundled Flutter image/icon asset. | DECLARED_NOT_REFERENCED |
| Student | assets/internship_tien_ich.png | Asset | Bundled Flutter image/icon asset. | DECLARED_NOT_REFERENCED |
| Student | assets/job_tien_ich.png | Asset | Bundled Flutter image/icon asset. | DECLARED_NOT_REFERENCED |
| Student | assets/loc_cv_tien_ich.png | Asset | Bundled Flutter image/icon asset. | DECLARED_NOT_REFERENCED |
| Student | assets/logo-nobr.png | Asset | Bundled Flutter image/icon asset. | USED |
| Student | assets/logo.jpg | Asset | Bundled Flutter image/icon asset. | USED |
| Student | assets/manager.png | Asset | Bundled Flutter image/icon asset. | USED |
| Student | assets/newspaper.png | Asset | Bundled Flutter image/icon asset. | USED |
| Student | assets/online-learning.png | Asset | Bundled Flutter image/icon asset. | USED |
| Student | assets/school_tien_ich.png | Asset | Bundled Flutter image/icon asset. | DECLARED_NOT_REFERENCED |
| Student | assets/thong_ke_tien_ich.png | Asset | Bundled Flutter image/icon asset. | DECLARED_NOT_REFERENCED |
| Student | assets/tien_ich1.png | Asset | Bundled Flutter image/icon asset. | USED |
| Student | devtools_options.yaml | Config | Flutter DevTools configuration. | CONFIG |
| Student | lib/constants.dart | Config | Prototype Neon/Gemini configuration symbols; secret literals omitted from context. | CONFIG |
| Student | lib/controllers/AI/ai_service.dart | Controller | Direct Gemini HTTP client. | SOURCE_BACKED |
| Student | lib/controllers/AI/view_test.dart | View/Test | Manual AI test screen without production route. | UNWIRED |
| Student | lib/controllers/cai_dat/cai_dat.dart | Controller | Logout and local session clearing. | WIRED |
| Student | lib/controllers/chat/chat_controller.dart | Controller | Chat query/send and three-second id-deduplicated polling. | WIRED |
| Student | lib/controllers/chat/nhung_doan_chat_controller.dart | Controller | Conversation-partner query from DoanChat. | WIRED |
| Student | lib/controllers/dang_nhap/dangnhap_ctrl.dart | Controller | Login orchestration between Neon and local SQLite. | WIRED |
| Student | lib/controllers/lay_ten.dart | Controller | Direct student/business name lookup; no active caller found. | UNWIRED |
| Student | lib/controllers/tim_kiem_job/tim_kiem_ctrl.dart | Controller | Student job loading and local filtering. | WIRED |
| Student | lib/controllers/trang_chu/hien_thi_danh_sach_top_cv.dart | Controller | Home, top-CV, job-management, search or detail controller. | SOURCE_BACKED |
| Student | lib/controllers/trang_chu/quan_ly_CV/quan_ly_job_cv.dart | Controller | Home, top-CV, job-management, search or detail controller. | SOURCE_BACKED |
| Student | lib/controllers/trang_chu/timkiemctrl.dart | Controller | Home, top-CV, job-management, search or detail controller. | SOURCE_BACKED |
| Student | lib/controllers/trang_chu/trang_chu_ctrl.dart | Controller | Home, top-CV, job-management, search or detail controller. | SOURCE_BACKED |
| Student | lib/controllers/trang_chu/xem_chi_tiet.dart | Controller | Home, top-CV, job-management, search or detail controller. | SOURCE_BACKED |
| Student | lib/controllers/ung_tuyen_ctrl.dart | Controller | Application/candidate actions and side effects. | WIRED |
| Student | lib/controllers/ung_vien_controller.dart | Controller | Candidate CV detail projection map; no active caller found. | UNWIRED |
| Student | lib/helper_db/neon_db.dart | DataBoundary | Neon singleton, SSL normalization, parameterized SQL and row normalization. | WIRED |
| Student | lib/helper_db/out_meta/helper_cv.dart | Helper | SQLite cache, Neon compatibility helpers, CV helpers or local UI builders. | SOURCE_BACKED |
| Student | lib/helper_db/out_meta/helper_db_error.dart | Helper | SQLite cache, Neon compatibility helpers, CV helpers or local UI builders. | SOURCE_BACKED |
| Student | lib/helper_db/out_meta/helper_supabase_error.dart | Helper | SQLite cache, Neon compatibility helpers, CV helpers or local UI builders. | SOURCE_BACKED |
| Student | lib/helper_db/out_meta/helper_widget.dart | Helper | SQLite cache, Neon compatibility helpers, CV helpers or local UI builders. | SOURCE_BACKED |
| Student | lib/helper_db/sinh_vien/helper_cv.dart | Helper | SQLite cache, Neon compatibility helpers, CV helpers or local UI builders. | SOURCE_BACKED |
| Student | lib/helper_db/sinh_vien/helper_db.dart | Helper | SQLite cache, Neon compatibility helpers, CV helpers or local UI builders. | SOURCE_BACKED |
| Student | lib/helper_db/sinh_vien/helper_supabase.dart | Helper | SQLite cache, Neon compatibility helpers, CV helpers or local UI builders. | SOURCE_BACKED |
| Student | lib/helper_db/sinh_vien/helper_widget.dart | Helper | SQLite cache, Neon compatibility helpers, CV helpers or local UI builders. | SOURCE_BACKED |
| Student | lib/main.dart | Entrypoint | MaterialApp bootstrap; starts at DangNhap. | WIRED |
| Student | lib/models/models.dart | Model | Legacy uppercase-key DoanhNghiep model; no active import found. | UNWIRED |
| Student | lib/models/outmeta/cv.dart | Model | Domain/compatibility models with DB row, JSON and date mapping. | SOURCE_BACKED |
| Student | lib/models/outmeta/dn_supabase.dart | Model | Legacy Supabase-named company model; no active import found. | UNWIRED |
| Student | lib/models/outmeta/doanh_nghiep.dart | Model | Domain/compatibility models with DB row, JSON and date mapping. | SOURCE_BACKED |
| Student | lib/models/outmeta/jd.dart | Model | Domain/compatibility models with DB row, JSON and date mapping. | SOURCE_BACKED |
| Student | lib/models/outmeta/nganh_nghe.dart | Model | Domain/compatibility models with DB row, JSON and date mapping. | SOURCE_BACKED |
| Student | lib/models/sinh_vien/chat.dart | Model | Domain/compatibility models with DB row, JSON and date mapping. | SOURCE_BACKED |
| Student | lib/models/sinh_vien/cv.dart | Model | Domain/compatibility models with DB row, JSON and date mapping. | SOURCE_BACKED |
| Student | lib/models/sinh_vien/doan_chat.dart | Model | Domain/compatibility models with DB row, JSON and date mapping. | SOURCE_BACKED |
| Student | lib/models/sinh_vien/jd.dart | Model | Domain/compatibility models with DB row, JSON and date mapping. | SOURCE_BACKED |
| Student | lib/models/sinh_vien/nganh_nghe.dart | Model | Domain/compatibility models with DB row, JSON and date mapping. | SOURCE_BACKED |
| Student | lib/models/sinh_vien/sinh_vien.dart | Model | Domain/compatibility models with DB row, JSON and date mapping. | SOURCE_BACKED |
| Student | lib/models/sinh_vien/ung_vien.dart | Model | Domain/compatibility models with DB row, JSON and date mapping. | SOURCE_BACKED |
| Student | lib/sv.dart | Placeholder | Temporary empty StatefulWidget; outside active route graph. | PLACEHOLDER/UNWIRED |
| Student | lib/theme/app_components.dart | Theme | Local Cobalt tokens, Material 3 theme and reusable primitives. | WIRED |
| Student | lib/theme/app_theme.dart | Theme | Local Cobalt tokens, Material 3 theme and reusable primitives. | WIRED |
| Student | lib/theme/design_tokens.dart | Theme | Local Cobalt tokens, Material 3 theme and reusable primitives. | WIRED |
| Student | lib/views/cai_dat/setting.dart | View | Settings, notification navigation and logout. | WIRED |
| Student | lib/views/dang_nhap/dang_nhap.dart | View | Login, password-recovery and animated destination shell. | WIRED |
| Student | lib/views/dang_nhap/menu.dart | View | Login, password-recovery and animated destination shell. | WIRED |
| Student | lib/views/dang_nhap/quen_mat_khau.dart | View | Login, password-recovery and animated destination shell. | WIRED |
| Student | lib/views/tim_kiem_cong_viec/tim_kiem_job.dart | View | Student job search/filter and detail/application navigation. | WIRED |
| Student | lib/views/trang_chu/main/dang_tin_tuyen_dung.dart | View | Home, notification, detail and job-posting surfaces. | SOURCE_BACKED |
| Student | lib/views/trang_chu/main/thong_bao.dart | View | Home, notification, detail and job-posting surfaces. | SOURCE_BACKED |
| Student | lib/views/trang_chu/main/thong_tin_chi_tiet.dart | View | Home, notification, detail and job-posting surfaces. | SOURCE_BACKED |
| Student | lib/views/trang_chu/main/trang_chu.dart | View | Home, notification, detail and job-posting surfaces. | SOURCE_BACKED |
| Student | lib/views/trang_chu/main/xem_chi_tiet.dart | View | Home, notification, detail and job-posting surfaces. | SOURCE_BACKED |
| Student | lib/views/trang_chu/main/xem_chi_tiet_view.dart | View | Home, notification, detail and job-posting surfaces. | SOURCE_BACKED |
| Student | lib/views/trang_chu/tien_ich/Hotro_SV/ho_tro_sv.dart | View | Student/business utility screens; active and legacy variants are documented per app. | SOURCE_BACKED |
| Student | lib/views/trang_chu/tien_ich/Khoa_hoc/khoa_hoc.dart | View | Student/business utility screens; active and legacy variants are documented per app. | SOURCE_BACKED |
| Student | lib/views/trang_chu/tien_ich/Lich_PV/lich_pv.dart | View | Student/business utility screens; active and legacy variants are documented per app. | SOURCE_BACKED |
| Student | lib/views/trang_chu/tien_ich/Quan_ly_CV/quan_ly_cv.dart | View | Student/business utility screens; active and legacy variants are documented per app. | SOURCE_BACKED |
| Student | lib/views/trang_chu/tien_ich/Tim_kiem_nhan_su/tim_kiem_nhan_su.dart | View | Student/business utility screens; active and legacy variants are documented per app. | SOURCE_BACKED |
| Student | lib/views/trang_chu/tien_ich/Tin_Tuc/tin_tuc.dart | View | Student/business utility screens; active and legacy variants are documented per app. | SOURCE_BACKED |
| Student | lib/views/tro_chuyen/chat.dart | View | Conversation list and polling chat screen. | WIRED |
| Student | lib/views/tro_chuyen/tro_chuyen.dart | View | Conversation list and polling chat screen. | WIRED |
| Student | pubspec.lock | Lockfile | Resolved Dart/Flutter dependency versions. | CONFIG |
| Student | pubspec.yaml | Package | Package identity, Dart SDK constraint, dependencies and asset declarations. | CONFIG |
| Student | test/neon_connection_test.dart | Test | Opt-in Neon SELECT 1 smoke test; skipped unless RUN_NEON_SMOKE=true. | DECLARED_NOT_RUNNABLE |
| Student | test/neon_test.dart | Test | URL/row/model normalization and polling cancellation tests. | SOURCE_BACKED |
