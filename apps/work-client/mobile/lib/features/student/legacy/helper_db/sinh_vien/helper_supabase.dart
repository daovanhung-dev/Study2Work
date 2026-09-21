import 'dart:convert';

import 'package:study2work_mobile/core/data/neon/neon_client.dart';
import 'package:study2work_mobile/features/student/legacy/models/sinh_vien/cv.dart';
import 'package:study2work_mobile/features/student/legacy/models/sinh_vien/jd.dart';
import 'package:study2work_mobile/features/student/legacy/models/sinh_vien/nganh_nghe.dart';
import 'package:study2work_mobile/features/student/legacy/models/sinh_vien/doan_chat.dart';
import 'package:study2work_mobile/features/student/legacy/models/sinh_vien/sinh_vien.dart';
import 'package:study2work_mobile/features/student/legacy/models/sinh_vien/ung_vien.dart';

class SinhVienSupabaseHelper {
  final NeonDatabase database = NeonDatabase.instance;

  Future<List<SinhVien>> getAll() async {
    final rows = await database.query('SELECT * FROM "SinhVien"');
    return rows.map(SinhVien.fromMap).toList();
  }

  Future<void> insert(SinhVien sv) async {
    await database.execute(
      'INSERT INTO "SinhVien" ("hoten", "email", "matkhau", "chuyennganh", "avt") VALUES (\$1, \$2, \$3, \$4, \$5)',
      parameters: [sv.hoten, sv.email, sv.matkhau, sv.chuyennganh, sv.avt],
    );
  }

  Future<void> update(SinhVien sv) async {
    if (sv.id == null) return;
    await database.execute(
      'UPDATE "SinhVien" SET "hoten" = \$1, "email" = \$2, "matkhau" = \$3, "chuyennganh" = \$4, "avt" = \$5 WHERE "id" = \$6',
      parameters: [
        sv.hoten,
        sv.email,
        sv.matkhau,
        sv.chuyennganh,
        sv.avt,
        sv.id,
      ],
    );
  }

  Future<void> delete(int id) async {
    await database.execute(
      'DELETE FROM "SinhVien" WHERE "id" = \$1',
      parameters: [id],
    );
  }

  Future<SinhVien?> getByEmail(String email) async {
    final rows = await database.query(
      'SELECT * FROM "SinhVien" WHERE "email" = \$1 LIMIT 1',
      parameters: [email],
    );
    return rows.isEmpty ? null : SinhVien.fromMap(rows.first);
  }

  Future<bool> login(String email, String matkhau) async {
    final rows = await database.query(
      'SELECT "id" FROM "SinhVien" WHERE "email" = \$1 AND "matkhau" = \$2 LIMIT 1',
      parameters: [email, matkhau],
    );
    return rows.isNotEmpty;
  }

  Future<List<Nganh>> getNganh() async {
    final rows = await database.query(
      'SELECT "nganh" FROM bannganh ORDER BY "nganh"',
    );
    return rows.map(Nganh.fromMap).toList();
  }

  Future<List<DoanChat>> getDoanChat(int id) async {
    final rows = await database.query(
      'SELECT * FROM "DoanChat" WHERE "sinhvien_id" = \$1 ORDER BY "created_at" DESC',
      parameters: [id],
    );
    return rows.map(DoanChat.fromMap).toList();
  }

  Future<String> getNameDN(int dnId) async {
    final rows = await database.query(
      'SELECT "hoten" FROM "DoanhNghiep" WHERE "id" = \$1 LIMIT 1',
      parameters: [dnId],
    );
    if (rows.isEmpty) throw StateError('Không tìm thấy doanh nghiệp.');
    return rows.first['hoten']?.toString() ?? '';
  }

  Future<List<JD>> getTopJD() async {
    final rows = await database.query('''
      SELECT j.*
      FROM "TopJD" t
      INNER JOIN "JD" j ON j."id" = t."jd_id"
      ORDER BY t."created_at" DESC
    ''');
    return rows.map(JD.fromMap).toList();
  }

  Future<JD> getJD(int id) async {
    final rows = await database.query(
      'SELECT * FROM "JD" WHERE "id" = \$1 LIMIT 1',
      parameters: [id],
    );
    if (rows.isEmpty) throw StateError('Không tìm thấy JD với id: $id');
    return JD.fromMap(rows.first);
  }

  Future<List<JD>> getAllJD() async {
    final rows = await database.query(
      'SELECT * FROM "JD" ORDER BY "ngay_tao" DESC NULLS LAST, "id" DESC',
    );
    return rows.map(JD.fromMap).toList();
  }

  Future<int> getIdDnByIdJd(int idJD) async {
    final rows = await database.query(
      'SELECT "doanhnghiep_id" FROM "JD" WHERE "id" = \$1 LIMIT 1',
      parameters: [idJD],
    );
    if (rows.isEmpty || rows.first['doanhnghiep_id'] == null) {
      throw StateError('JD chưa gán doanh nghiệp.');
    }
    return int.parse(rows.first['doanhnghiep_id'].toString());
  }

  Future<bool> insertUngVien(UngVien uv) async {
    if (uv.jdId == null || uv.sinhvienId == null) return false;

    final existing = await database.query(
      'SELECT "id" FROM "UngVien" WHERE "jd_id" = \$1 AND "sinhvien_id" = \$2 LIMIT 1',
      parameters: [uv.jdId, uv.sinhvienId],
    );
    if (existing.isNotEmpty) return false;

    await database.execute(
      'INSERT INTO "UngVien" ("sinhvien_id", "doanhnghiep_id", "trangthai", "jd_id") VALUES (\$1, \$2, \$3, \$4)',
      parameters: [
        uv.sinhvienId,
        uv.doanhnghiepId,
        uv.trangthai ?? 'chưa ứng tuyển',
        uv.jdId,
      ],
    );
    return true;
  }

  Future<CV?> getCVById(int id) async {
    final rows = await database.query(
      'SELECT * FROM "Cv" WHERE "id" = \$1 LIMIT 1',
      parameters: [id],
    );
    return rows.isEmpty ? null : CV.fromMap(rows.first);
  }

  Future<void> updateCV(CV cv) async {
    if (cv.id == null) return;
    final data = cv.toMap();
    await database.execute('''
      UPDATE "Cv" SET
        "avt" = \$1, "hoten" = \$2, "ngaysinh" = \$3, "gioitinh" = \$4,
        "email" = \$5, "sdt" = \$6, "diachi" = \$7, "vitri" = \$8,
        "nganh" = \$9, "muctieunghiep" = \$10, "hocvan" = \$11,
        "kinhnghiem" = \$12, "kynang" = \$13, "ngoaingu" = \$14,
        "chungchi" = \$15, "duan" = \$16, "giaithuong" = \$17,
        "hoatdong" = \$18, "social" = \$19, "portfolio" = \$20,
        "luongmongmuon" = \$21
      WHERE "id" = \$22
    ''', parameters: _cvParameters(data)..add(cv.id));
  }

  List<Object?> _cvParameters(Map<String, dynamic> data) {
    return [
      data['avt'],
      data['hoten'],
      data['ngaysinh'],
      data['gioitinh'],
      data['email'],
      data['sdt'],
      data['diachi'],
      data['vitri'],
      data['nganh'],
      data['muctieunghiep'],
      data['hocvan'],
      data['kinhnghiem'],
      data['kynang'],
      data['ngoaingu'],
      data['chungchi'],
      data['duan'],
      data['giaithuong'],
      data['hoatdong'],
      data['social'] is Map ? jsonEncode(data['social']) : data['social'],
      data['portfolio'],
      data['luongmongmuon'],
    ];
  }
}
