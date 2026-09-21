/// Development-only direct Neon configuration.
///
/// This credential is intentionally kept here per the current prototype
/// requirement. It must not be shipped to production; see README.md.
// ignore: constant_identifier_names
const String NEON_POOLER_URL =
    'postgresql://neondb_owner:npg_KbI87qFogAHp@ep-noisy-fog-b3rlle00-pooler.c-4.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require';

/// Development-only Gemini configuration. Rotate this key before production.
// ignore: constant_identifier_names
const String GEMINI_API_KEY = 'AIzaSyDg8hutk_kLylLwDG2skoAeQmmxi_xXxlE';

enum AppFlavor { student, business }

AppFlavor appFlavorFromName(String? name) {
  return name == 'business' ? AppFlavor.business : AppFlavor.student;
}

class AppConfig {
  const AppConfig({required this.flavor});

  factory AppConfig.fromFlavor(String? name) {
    return AppConfig(flavor: appFlavorFromName(name));
  }

  final AppFlavor flavor;

  bool get isStudent => flavor == AppFlavor.student;
  bool get isBusiness => flavor == AppFlavor.business;

  String get displayName => isStudent ? 'S2WCV' : 'S2WHR';
  String get applicationId => isStudent
      ? 'com.s2w.work.students'
      : 'com.s2w.work.business';
  String get sqliteDatabaseName => isStudent ? 'sinhvien.db' : 'doanhnghiep.db';
  String get rolePath => isStudent ? '/student' : '/business';
  String get assetRoot => isStudent ? 'assets/student' : 'assets/business';

  String asset(String name) => '$assetRoot/$name';
}
