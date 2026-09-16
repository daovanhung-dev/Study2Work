import 'package:work_server/helper_db/helper_db.dart';
import 'package:work_server/helper_db/neon_db.dart';
import 'package:work_server/models/jd.dart';

final HelperDB dbHelper = HelperDB.instance;
final NeonDatabase database = NeonDatabase.instance;

Future<List<JD>> getJob() async {
  final doanhnghiepId = await dbHelper.getID();
  final rows = await database.query(
    '''
    SELECT "id", "ten_vi_tri", "cap_bac", "nhiem_vu", "trinh_do",
           "kinh_nghiem", "muc_luong", "dia_diem", "thoi_gian"
    FROM "JD"
    WHERE "doanhnghiep_id" = \$1
    ORDER BY "ngay_tao" DESC NULLS LAST, "id" DESC
  ''',
    parameters: [doanhnghiepId],
  );
  return rows.map(JD.fromMap).toList();
}
