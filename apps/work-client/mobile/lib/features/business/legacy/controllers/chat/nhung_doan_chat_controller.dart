import 'package:work_server/helper_db/neon_db.dart';

final NeonDatabase database = NeonDatabase.instance;

Future<List<Map<String, dynamic>>> getChats(int dnId) async {
  final rows = await database.query(
    '''
    SELECT DISTINCT s."id", s."hoten"
    FROM "DoanChat" dc
    INNER JOIN "SinhVien" s ON s."id" = dc."sinhvien_id"
    WHERE dc."doanhnghiep_id" = \$1
    ORDER BY s."hoten"
  ''',
    parameters: [dnId],
  );

  return rows.map((row) => {'id': row['id'], 'hoten': row['hoten']}).toList();
}
