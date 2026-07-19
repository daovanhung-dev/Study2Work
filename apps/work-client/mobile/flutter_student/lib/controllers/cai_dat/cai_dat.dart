import 'package:learn2earn/helper_db/sinh_vien/helper_db.dart';
final sqlite = SinhVienSQLiteHelper.instance;

Future<void> dangXuat() async{
  await sqlite.deleteSinhVien();
}