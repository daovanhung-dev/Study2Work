import 'package:work_server/helper_db/helper_db.dart';
final sqlite = HelperDB.instance;
Future<void> dangXuat() async{
  await sqlite.clearDoanhNghiep();
}