import 'package:learn2earn/models/sinh_vien/JD.dart';
import 'package:learn2earn/helper_db/sinh_vien/helper_supabase.dart';
import 'package:learn2earn/helper_db/sinh_vien/helper_db.dart';

class TrangChuCtrl {
  final _supbase = SinhVienSupabaseHelper();
  final _sqlite = SinhVienSQLiteHelper.instance;

  List<JD> _jobs = [];

  //phuong thuc
  Future<List<JD>> get_Top_JD() async {
    final jd = await _supbase.getTopJD();
    return jd;
  }

  Future<String> getNameSV() async{
    final sv = await _sqlite.getSinhVien();
    String name =  sv.hoten ?? 'Lỗi hiển thị tên';
    return name ;
  }

  Future<String> getImgSV() async {
    final sv = await _sqlite.getSinhVien();
    String img = sv.avt ?? 'Lỗi hiển thị ảnh';
    return img;
  }
}
