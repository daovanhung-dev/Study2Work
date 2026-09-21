import 'package:study2work_mobile/core/data/sqlite/session_store.dart';
import 'package:study2work_mobile/features/business/legacy/helper_db/helper_db.dart';
import 'package:study2work_mobile/features/business/legacy/models/doanh_nghiep.dart';

/// SQLite adapter for the Business session database.
///
/// The table and database name stay owned by the existing helper so this
/// migration does not change the current local schema.
final class BusinessSessionStore implements SessionStore<DoanhNghiep> {
  BusinessSessionStore({HelperDB? database})
      : _database = database ?? HelperDB.instance;

  final HelperDB _database;

  @override
  Future<DoanhNghiep?> read() {
    return _database.getDoanhNghiep();
  }

  @override
  Future<void> save(DoanhNghiep value) {
    return _database.saveDoanhNghiep(value);
  }

  @override
  Future<void> clear() {
    return _database.clearDoanhNghiep();
  }
}
