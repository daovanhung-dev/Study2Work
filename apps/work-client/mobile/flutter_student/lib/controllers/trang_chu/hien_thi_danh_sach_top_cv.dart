import 'package:work_server/helper_db/neon_db.dart';

final NeonDatabase database = NeonDatabase.instance;

Future<List<Map<String, dynamic>>> getTopCV() async {
  try {
    final idsResponse = await database.query('SELECT "id" FROM "TopCV"');
    final ids = idsResponse.map((row) => row['id']).whereType<int>().toList();
    if (ids.isEmpty) return [];

    final placeholders = List.generate(
      ids.length,
      (index) => '\$${index + 1}',
    ).join(', ');
    return await database.query('''
      SELECT "id", "avt", "hoten", "ngaysinh", "gioitinh", "email", "sdt",
             "diachi", "vitri", "nganh", "muctieunghiep", "hocvan",
             "kinhnghiem", "kynang"
      FROM "Cv"
      WHERE "id" IN ($placeholders)
      ''', parameters: ids);
  } catch (_) {
    return [];
  }
}
