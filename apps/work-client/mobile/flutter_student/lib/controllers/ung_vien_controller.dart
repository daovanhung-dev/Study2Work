import 'package:work_server/helper_db/neon_db.dart';

final NeonDatabase database = NeonDatabase.instance;

Future<Map<String, dynamic>> xemChiTiet(int id) async {
  final rows = await database.query(
    '''
    SELECT
      "id",
      "avt",
      "vitri",
      "hoten" AS "ten",
      "nganh" AS "cn",
      "kinhnghiem" AS "kn",
      "kynang" AS "skill",
      "hocvan" AS "hv",
      "luongmongmuon" AS "luong"
    FROM "Cv"
    WHERE "id" = \$1
    LIMIT 1
  ''',
    parameters: [id],
  );

  if (rows.isEmpty) return {};
  final row = rows.first;
  final skill = row['skill']?.toString() ?? '';

  return {
    'macv_ds': row['id'],
    'avt_ds': row['avt'],
    'vitri_ds': row['vitri'],
    'ten_ds': row['ten'],
    'cn_ds': row['cn'],
    'kn_ds': row['kn'],
    'skill_ds': skill
        .split(',')
        .map((item) => item.trim())
        .where((item) => item.isNotEmpty)
        .toList(),
    'hv_ds': row['hv'],
    'luong_ds': row['luong'],
  };
}
