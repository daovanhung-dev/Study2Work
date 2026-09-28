import 'package:study2work_mobile/features/student/legacy/helper_db/sinh_vien/helper_db.dart';

final sqlite = SinhVienSQLiteHelper.instance;

Future<void> dangXuat() async {
  await sqlite.deleteSinhVien();
}
