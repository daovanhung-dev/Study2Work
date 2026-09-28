import 'package:study2work_mobile/features/business/legacy/helper_db/helper_db.dart';
import 'package:study2work_mobile/features/business/legacy/helper_db/helper_supabase.dart';

/// Compatibility data facade used while Business legacy screens are migrated.
///
/// Presentation code depends on this application boundary instead of
/// importing a database helper directly. The underlying schema and SQL remain
/// unchanged until the corresponding vertical slice gets a typed repository.
final class BusinessLegacyData {
  BusinessLegacyData._();

  static final sqlite = HelperDB.instance;
  static final neon = DNSupabase.instance;
}
