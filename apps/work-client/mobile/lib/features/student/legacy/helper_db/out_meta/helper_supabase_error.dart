import 'package:study2work_mobile/core/data/neon/neon_client.dart';
import 'package:study2work_mobile/features/student/legacy/helper_db/out_meta/helper_db_error.dart';
import 'package:study2work_mobile/features/student/legacy/models/outmeta/jd.dart';
import 'package:study2work_mobile/features/student/legacy/models/outmeta/nganh_nghe.dart';

final HelperDB dbHelper = HelperDB.instance;

class DNSupabase {
  static final DNSupabase instance = DNSupabase._internal();

  factory DNSupabase() => instance;

  DNSupabase._internal();

  final NeonDatabase database = NeonDatabase.instance;

  Future<bool> ktDangNhap(String gmail, String matKhau) async {
    final rows = await database.query(
      'SELECT "id" FROM "DoanhNghiep" WHERE "email" = \$1 AND "matkhau" = \$2 LIMIT 1',
      parameters: [gmail, matKhau],
    );
    return rows.isNotEmpty;
  }

  Future<Map<String, dynamic>> getDN(String email) async {
    final rows = await database.query(
      'SELECT * FROM "DoanhNghiep" WHERE "email" = \$1 LIMIT 1',
      parameters: [email],
    );
    if (rows.isEmpty) throw StateError('Không tìm thấy doanh nghiệp.');
    return rows.first;
  }

  Future<List<Nganh>> getNganh() async {
    final rows = await database.query(
      'SELECT "nganh" FROM bannganh ORDER BY "nganh"',
    );
    return rows.map(Nganh.fromMap).toList();
  }

  Future<String> getAVT(int id) async {
    final rows = await database.query(
      'SELECT "avt" FROM "DoanhNghiep" WHERE "id" = \$1 LIMIT 1',
      parameters: [id],
    );
    if (rows.isEmpty) throw StateError('Không tìm thấy ảnh doanh nghiệp.');
    return rows.first['avt']?.toString() ?? '';
  }

  Future<List<Map<String, dynamic>>> layUngVien() async {
    final companyId = await dbHelper.getID();
    return database.query(
      '''
      SELECT c.*
      FROM "UngVien" u
      INNER JOIN "Cv" c ON c."sinhvien_id" = u."sinhvien_id"
      WHERE u."doanhnghiep_id" = \$1
      ORDER BY u."created_at" DESC
    ''',
      parameters: [companyId],
    );
  }

  Future<void> insertJD(Map<String, dynamic> data) async {
    final columns = <String>[
      'doanhnghiep_id',
      'ten_vi_tri',
      'phong_ban',
      'cap_bac',
      'bao_cao_cho',
      'nhiem_vu',
      'trinh_do',
      'kinh_nghiem',
      'ky_nang',
      'ky_nang_mem',
      'uu_tien',
      'muc_luong',
      'phuc_loi',
      'moi_truong',
      'dia_diem',
      'thoi_gian',
      'han_nop',
      'cach_ung_tuyen',
      'mo_ta',
      'ten_cong_ty',
      'nganh',
      'avt',
    ];
    final values = columns.map((column) {
      final value = data[column];
      return value is Iterable ? value.join(', ') : value;
    }).toList();
    final placeholders = List.generate(
      values.length,
      (index) => '\$${index + 1}',
    ).join(', ');
    final quotedColumns = columns.map((column) => '"$column"').join(', ');
    await database.execute(
      'INSERT INTO "JD" ($quotedColumns) VALUES ($placeholders)',
      parameters: values,
    );
  }

  Future<JD> getJD(int maJD) async {
    final rows = await database.query(
      'SELECT * FROM "JD" WHERE "id" = \$1 LIMIT 1',
      parameters: [maJD],
    );
    if (rows.isEmpty) throw StateError('Không tìm thấy JD.');
    return JD.fromMap(rows.first);
  }
}
