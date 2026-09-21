import 'package:study2work_mobile/core/data/neon/neon_client.dart';

final NeonDatabase database = NeonDatabase.instance;

Future<Map<String, dynamic>> xemChiTiet(int id) async {
  final rows = await database.query(
    '''
    SELECT "id", "avt", "hoten", "ngaysinh", "gioitinh", "email", "sdt",
           "diachi", "vitri", "nganh", "muctieunghiep", "hocvan",
           "kinhnghiem", "kynang", "ngoaingu", "chungchi", "duan",
           "giaithuong", "hoatdong", "social", "portfolio", "luongmongmuon"
    FROM "Cv"
    WHERE "id" = \$1
    LIMIT 1
  ''',
    parameters: [id],
  );
  return rows.isEmpty ? <String, dynamic>{} : rows.first;
}
