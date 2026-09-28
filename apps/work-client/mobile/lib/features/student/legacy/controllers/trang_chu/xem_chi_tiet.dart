import 'package:study2work_mobile/core/data/neon/neon_client.dart';
import 'package:study2work_mobile/features/student/legacy/models/sinh_vien/jd.dart';

class XemChiTietController {
  final NeonDatabase database = NeonDatabase.instance;

  Future<List<JD>> getAllJD() async {
    final rows = await database.query(
      'SELECT * FROM "JD" ORDER BY "ngay_tao" DESC NULLS LAST, "id" DESC',
    );
    return rows.map(JD.fromMap).toList();
  }

  Future<JD> xemChiTiet(int id) async {
    final rows = await database.query(
      'SELECT * FROM "JD" WHERE "id" = \$1 LIMIT 1',
      parameters: [id],
    );
    if (rows.isEmpty) throw StateError('Không tìm thấy JD với id: $id');
    return JD.fromMap(rows.first);
  }

  Future<List<JD>> getJDByNganh(String nganh) async {
    final rows = await database.query(
      'SELECT * FROM "JD" WHERE "nganh" = \$1 ORDER BY "ngay_tao" DESC NULLS LAST',
      parameters: [nganh],
    );
    return rows.map(JD.fromMap).toList();
  }

  Future<List<JD>> getJDByDoanhNghiep(int doanhNghiepID) async {
    final rows = await database.query(
      'SELECT * FROM "JD" WHERE "doanhnghiep_id" = \$1 ORDER BY "ngay_tao" DESC NULLS LAST',
      parameters: [doanhNghiepID],
    );
    return rows.map(JD.fromMap).toList();
  }

  Future<void> updateJD(JD jd) async {
    await database.execute(
      '''
      UPDATE "JD" SET
        "doanhnghiep_id" = \$1, "ten_cong_ty" = \$2, "nganh" = \$3,
        "ten_vi_tri" = \$4, "cap_bac" = \$5, "bao_cao_cho" = \$6,
        "nhiem_vu" = \$7, "trinh_do" = \$8, "kinh_nghiem" = \$9,
        "ky_nang" = \$10, "ky_nang_mem" = \$11, "uu_tien" = \$12,
        "muc_luong" = \$13, "phuc_loi" = \$14, "moi_truong" = \$15,
        "dia_diem" = \$16, "thoi_gian" = \$17, "han_nop" = \$18,
        "cach_ung_tuyen" = \$19, "mo_ta" = \$20, "avt" = \$21
      WHERE "id" = \$22
    ''',
      parameters: [
        jd.doanhNghiepID,
        jd.tenCongTy,
        jd.nganh,
        jd.tenViTri,
        jd.capBac,
        jd.baoCaoCho,
        jd.nhiemVu,
        jd.trinhDo,
        jd.kinhNghiem,
        jd.kyNang,
        jd.kyNangMem,
        jd.uuTien,
        jd.mucLuong,
        jd.phucLoi,
        jd.moiTruong,
        jd.diaDiem,
        jd.thoiGian,
        jd.hanNop,
        jd.cachUngTuyen,
        jd.moTa,
        jd.avt,
        jd.id,
      ],
    );
  }

  Future<void> deleteJD(int id) async {
    await database.execute(
      'DELETE FROM "JD" WHERE "id" = \$1',
      parameters: [id],
    );
  }
}
