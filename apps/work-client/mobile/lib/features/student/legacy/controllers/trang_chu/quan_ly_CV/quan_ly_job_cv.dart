import 'package:study2work_mobile/features/student/legacy/models/sinh_vien/cv.dart';
import 'package:study2work_mobile/features/student/legacy/helper_db/sinh_vien/helper_db.dart';
import 'package:study2work_mobile/features/student/legacy/helper_db/sinh_vien/helper_supabase.dart';

final supabase = SinhVienSupabaseHelper();
final dbHelper = SinhVienSQLiteHelper.instance;

class CVCtrl {
  /// 🔹 Lấy CV theo id
  Future<CV?> getCVById() async {
    int id = await dbHelper.getID();
    final cv = await supabase.getCVById(id);
    return cv;
  }

  Future<void> update(CV cv) async {
    supabase.updateCV(cv);
  }
}
