import 'package:study2work_mobile/features/business/legacy/helper_db/helper_db.dart';

final sqlite = HelperDB.instance;
Future<void> dangXuat() async {
  await sqlite.clearDoanhNghiep();
}
