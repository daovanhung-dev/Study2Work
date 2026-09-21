import 'package:study2work_mobile/core/data/sqlite/session_store.dart';
import 'package:study2work_mobile/features/student/legacy/helper_db/sinh_vien/helper_db.dart';
import 'package:study2work_mobile/features/student/legacy/models/sinh_vien/sinh_vien.dart';

/// SQLite adapter for the Student session database.
///
/// The table and database name stay owned by the existing helper so this
/// migration does not change the current local schema.
final class StudentSessionStore implements SessionStore<SinhVien> {
  StudentSessionStore({SinhVienSQLiteHelper? database})
      : _database = database ?? SinhVienSQLiteHelper.instance;

  final SinhVienSQLiteHelper _database;

  @override
  Future<SinhVien?> read() async {
    final session = await _database.getSinhVien();
    return session.email == null && session.matkhau == null ? null : session;
  }

  @override
  Future<void> save(SinhVien value) async {
    await _database.insertSinhVien(value);
  }

  @override
  Future<void> clear() async {
    await _database.deleteSinhVien();
  }
}
