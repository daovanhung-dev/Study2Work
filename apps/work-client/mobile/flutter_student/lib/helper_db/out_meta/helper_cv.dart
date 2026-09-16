import 'dart:convert';

import 'package:work_server/helper_db/neon_db.dart';
import 'package:work_server/models/outmeta/cv.dart';

class CVHelperDB {
  final NeonDatabase database = NeonDatabase.instance;

  Future<CV?> insertCV(CV cv) async {
    try {
      final rows = await database.query(r'''
        INSERT INTO "Cv" (
          "avt", "hoten", "ngaysinh", "gioitinh", "email", "sdt", "diachi",
          "vitri", "nganh", "muctieunghiep", "hocvan", "kinhnghiem", "kynang",
          "ngoaingu", "chungchi", "duan", "giaithuong", "hoatdong", "social",
          "portfolio", "luongmongmuon", "created_at", "sinhvien_id"
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12,
                  $13, $14, $15, $16, $17, $18, $19, $20, $21, $22, $23)
        RETURNING *
      ''', parameters: _insertParameters(cv));
      return rows.isEmpty ? null : CV.fromMap(rows.first);
    } catch (_) {
      return null;
    }
  }

  Future<List<CV>> getAllCV() async {
    try {
      final rows = await database.query(
        'SELECT * FROM "Cv" ORDER BY "created_at" DESC NULLS LAST',
      );
      return rows.map(CV.fromMap).toList();
    } catch (_) {
      return [];
    }
  }

  Future<CV?> getCVById(int id) async {
    try {
      final rows = await database.query(
        r'SELECT * FROM "Cv" WHERE "id" = $1 LIMIT 1',
        parameters: [id],
      );
      return rows.isEmpty ? null : CV.fromMap(rows.first);
    } catch (_) {
      return null;
    }
  }

  Future<bool> updateCV(CV cv) async {
    if (cv.id == null) return false;
    try {
      final affected = await database.execute(
        r'''
        UPDATE "Cv" SET
          "avt" = $1, "hoten" = $2, "ngaysinh" = $3, "gioitinh" = $4,
          "email" = $5, "sdt" = $6, "diachi" = $7, "vitri" = $8,
          "nganh" = $9, "muctieunghiep" = $10, "hocvan" = $11,
          "kinhnghiem" = $12, "kynang" = $13, "ngoaingu" = $14,
          "chungchi" = $15, "duan" = $16, "giaithuong" = $17,
          "hoatdong" = $18, "social" = $19, "portfolio" = $20,
          "luongmongmuon" = $21
        WHERE "id" = $22
      ''',
        parameters: [..._updateParameters(cv), cv.id],
      );
      return affected > 0;
    } catch (_) {
      return false;
    }
  }

  Future<bool> deleteCV(int id) async {
    try {
      return await database.execute(
            r'DELETE FROM "Cv" WHERE "id" = $1',
            parameters: [id],
          ) >
          0;
    } catch (_) {
      return false;
    }
  }

  Future<List<CV>> searchCV(String keyword) async {
    try {
      final pattern = '%$keyword%';
      final rows = await database.query(
        r'''
        SELECT * FROM "Cv"
        WHERE "hoten" ILIKE $1 OR "nganh" ILIKE $2
        ORDER BY "created_at" DESC NULLS LAST
      ''',
        parameters: [pattern, pattern],
      );
      return rows.map(CV.fromMap).toList();
    } catch (_) {
      return [];
    }
  }

  Future<List<String>> getNganh() async {
    final rows = await database.query(
      'SELECT "nganh" FROM bannganh ORDER BY "nganh"',
    );
    return rows.map((row) => row['nganh']?.toString() ?? '').toList();
  }

  List<Object?> _insertParameters(CV cv) {
    return [
      cv.avt,
      cv.hoten,
      cv.ngaysinh,
      cv.gioitinh,
      cv.email,
      cv.sdt,
      cv.diachi,
      cv.vitri,
      cv.nganh,
      cv.muctieunghiep,
      cv.hocvan,
      cv.kinhnghiem,
      cv.kynang,
      cv.ngoaingu,
      cv.chungchi,
      cv.duan,
      cv.giaithuong,
      cv.hoatdong,
      cv.social == null ? null : jsonEncode(cv.social),
      cv.portfolio,
      cv.luongmongmuon,
      cv.createdAt,
      null,
    ];
  }

  List<Object?> _updateParameters(CV cv) {
    return [
      cv.avt,
      cv.hoten,
      cv.ngaysinh,
      cv.gioitinh,
      cv.email,
      cv.sdt,
      cv.diachi,
      cv.vitri,
      cv.nganh,
      cv.muctieunghiep,
      cv.hocvan,
      cv.kinhnghiem,
      cv.kynang,
      cv.ngoaingu,
      cv.chungchi,
      cv.duan,
      cv.giaithuong,
      cv.hoatdong,
      cv.social == null ? null : jsonEncode(cv.social),
      cv.portfolio,
      cv.luongmongmuon,
    ];
  }
}
