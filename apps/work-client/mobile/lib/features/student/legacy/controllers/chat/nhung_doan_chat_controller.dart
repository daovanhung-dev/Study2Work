import 'package:work_server/helper_db/neon_db.dart';

final NeonDatabase database = NeonDatabase.instance;

Future<List<Map<String, dynamic>>> getChats(int svId) async {
  final rows = await database.query(
    '''
    SELECT DISTINCT d."id", d."hoten"
    FROM "DoanChat" dc
    INNER JOIN "DoanhNghiep" d ON d."id" = dc."doanhnghiep_id"
    WHERE dc."sinhvien_id" = \$1
    ORDER BY d."hoten"
  ''',
    parameters: [svId],
  );

  return rows.map((row) => {'id': row['id'], 'hoten': row['hoten']}).toList();
}
