import 'package:work_server/helper_db/helper_db.dart';
import 'package:work_server/helper_db/neon_db.dart';
import 'package:work_server/models/cv.dart';
import 'package:work_server/models/jd.dart';
import 'package:work_server/models/nganh_nghe.dart';
import 'package:work_server/models/ung_vien.dart';

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

  Future<List<String>> layTrangThai() async {
    final companyId = await dbHelper.getID();
    final rows = await database.query(
      'SELECT "trangthai" FROM "UngVien" WHERE "doanhnghiep_id" = \$1 ORDER BY "created_at" DESC',
      parameters: [companyId],
    );
    return rows.map((row) => row['trangthai']?.toString() ?? '').toList();
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
    final values = columns.map((column) => _jdValue(data[column])).toList();
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

  dynamic _jdValue(dynamic value) {
    if (value is Iterable) return value.join(', ');
    return value;
  }

  Future<JD> getJD(int maJD) async {
    final rows = await database.query(
      'SELECT * FROM "JD" WHERE "id" = \$1 LIMIT 1',
      parameters: [maJD],
    );
    if (rows.isEmpty) throw StateError('Không tìm thấy JD.');
    return JD.fromMap(rows.first);
  }

  Future<List<CV>> getCV() async {
    final companyId = await dbHelper.getID();
    final rows = await database.query(
      '''
      SELECT c.*
      FROM "UngVien" u
      INNER JOIN "Cv" c ON c."sinhvien_id" = u."sinhvien_id"
      WHERE u."doanhnghiep_id" = \$1
      ORDER BY u."created_at" DESC
    ''',
      parameters: [companyId],
    );
    return rows.map(CV.fromMap).toList();
  }

  Future<List<UngVien>> getUngVien() async {
    final companyId = await dbHelper.getID();
    final rows = await database.query(
      'SELECT * FROM "UngVien" WHERE "doanhnghiep_id" = \$1 ORDER BY "created_at" DESC',
      parameters: [companyId],
    );
    return rows.map(UngVien.fromMap).toList();
  }

  Future<void> ungTuyen(int sinhvienId) async {
    final companyId = await dbHelper.getID();
    await database.execute(
      'UPDATE "UngVien" SET "trangthai" = \$1 WHERE "sinhvien_id" = \$2 AND "doanhnghiep_id" = \$3',
      parameters: ['Đã ứng tuyển', sinhvienId, companyId],
    );
  }

  Future<void> delCV(int sinhvienId) async {
    final companyId = await dbHelper.getID();
    await database.execute(
      'DELETE FROM "UngVien" WHERE "sinhvien_id" = \$1 AND "doanhnghiep_id" = \$2',
      parameters: [sinhvienId, companyId],
    );
  }

  Future<void> insertDoanChat(Map<String, dynamic> data) async {
    await database.execute(
      'INSERT INTO "DoanChat" ("sinhvien_id", "doanhnghiep_id") VALUES (\$1, \$2)',
      parameters: [data['sinhvien_id'], data['doanhnghiep_id']],
    );
  }

  Future<void> guiTinNhan(
    int sinhvienId,
    int doanhnghiepId,
    String noidung,
  ) async {
    await database.execute(
      '''
      INSERT INTO "Chat" ("sinhvien_id", "doanhnghiep_id", "nguoigui", "nguoinhan", "noidung", "ngaygui")
      VALUES (\$1, \$2, \$3, \$4, \$5, \$6)
    ''',
      parameters: [
        sinhvienId,
        doanhnghiepId,
        doanhnghiepId,
        sinhvienId,
        noidung,
        DateTime.now().toUtc(),
      ],
    );
  }
}
