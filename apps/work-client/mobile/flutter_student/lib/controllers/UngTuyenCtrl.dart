import 'package:learn2earn/models/sinh_vien/ung_vien.dart';
import 'package:learn2earn/helper_db/sinh_vien/helper_supabase.dart';
import 'package:learn2earn/helper_db/sinh_vien/helper_db.dart';
import 'package:learn2earn/models/sinh_vien/ung_vien.dart';

class UngTuyenCtrl{
  final SinhVienSupabaseHelper _helper = SinhVienSupabaseHelper();
  final SinhVienSQLiteHelper _helperSV = SinhVienSQLiteHelper.instance;

  Future<bool> ungTuyen(int idJD) async {

    int idSV = await _helperSV.getID();
    int idDN = await _helper.getIdDnByIdJd(idJD);
    UngVien uv = UngVien(
      sinhvienId: idSV,
      doanhnghiepId: idDN,
      jdId: idJD,
    );
    final kt = await _helper.insertUngVien(uv);
    return kt;
  }
}