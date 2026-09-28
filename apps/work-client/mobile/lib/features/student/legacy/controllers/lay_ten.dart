import 'package:study2work_mobile/core/data/neon/neon_client.dart';

final NeonDatabase database = NeonDatabase.instance;

Future<Map<String, dynamic>?> getNameSV(int id) async {
  final rows = await database.query(
    'SELECT "hoten" FROM "SinhVien" WHERE "id" = \$1 LIMIT 1',
    parameters: [id],
  );
  return rows.isEmpty ? null : {'ten': rows.first['hoten']};
}

Future<Map<String, dynamic>?> getNameDN(int id) async {
  final rows = await database.query(
    'SELECT "hoten" FROM "DoanhNghiep" WHERE "id" = \$1 LIMIT 1',
    parameters: [id],
  );
  return rows.isEmpty ? null : {'hoten': rows.first['hoten']};
}
