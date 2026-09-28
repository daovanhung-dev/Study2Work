import 'package:study2work_mobile/features/student/legacy/helper_db/out_meta/helper_db_error.dart';
import 'package:study2work_mobile/features/student/legacy/helper_db/out_meta/helper_supabase_error.dart';

/// Compatibility data facade used while Student legacy screens are migrated.
///
/// Presentation code depends on this application boundary instead of
/// importing a database helper directly. The underlying schema and SQL remain
/// unchanged until the corresponding vertical slice gets a typed repository.
final class StudentLegacyData {
  StudentLegacyData._();

  static final sqlite = HelperDB.instance;
  static final neon = DNSupabase.instance;
}
