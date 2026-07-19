import 'package:supabase_flutter/supabase_flutter.dart';
import 'package:learn2earn/models/sinh_vien/CV.dart';
import 'package:learn2earn/helper_db/sinh_vien/helper_db.dart';
import 'package:learn2earn/helper_db/sinh_vien/helper_supabase.dart';
final supabase = SinhVienSupabaseHelper();
final dbHelper = SinhVienSQLiteHelper.instance;

class CVCtrl {
  /// 🔹 Lấy CV theo id
  Future<CV?> getCVById() async {
    int id = await dbHelper.getID();
    final cv = await supabase.getCVById(id);
    return cv;
  }

  Future<void> Update(CV cv) async{
    supabase.updateCV(cv);
  }
}


