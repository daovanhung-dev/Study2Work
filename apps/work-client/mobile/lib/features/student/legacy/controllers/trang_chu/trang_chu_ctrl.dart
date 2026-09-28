import 'package:study2work_mobile/features/student/legacy/models/sinh_vien/jd.dart';
import 'package:study2work_mobile/features/student/legacy/helper_db/sinh_vien/helper_supabase.dart';
import 'package:study2work_mobile/features/student/legacy/helper_db/sinh_vien/helper_db.dart';

class TrangChuCtrl {
  final _neon = SinhVienSupabaseHelper();
  final _sqlite = SinhVienSQLiteHelper.instance;

  //phuong thuc
  Future<List<JD>> getTopJd() async {
    final jd = await _neon.getTopJD();
    return jd;
  }

  Future<String> getNameSV() async {
    final sv = await _sqlite.getSinhVien();
    String name = sv.hoten ?? 'Lỗi hiển thị tên';
    return name;
  }

  Future<String> getImgSV() async {
    final sv = await _sqlite.getSinhVien();
    String img = sv.avt ?? 'Lỗi hiển thị ảnh';
    return img;
  }
}
