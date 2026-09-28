import 'package:flutter/foundation.dart';
import 'package:study2work_mobile/features/student/legacy/helper_db/sinh_vien/helper_db.dart';
import 'package:study2work_mobile/features/student/legacy/helper_db/sinh_vien/helper_supabase.dart';
import 'package:study2work_mobile/features/student/legacy/models/sinh_vien/sinh_vien.dart';

final sqlite = SinhVienSQLiteHelper.instance;
final neon = SinhVienSupabaseHelper();
SinhVien? student;

/// Hàm đăng nhập
/// Trả về true nếu thành công, false nếu thất bại
Future<bool> dangNhapDN(String email, String matKhau) async {
  try {
    // 1️⃣ Kiểm tra đăng nhập với Neon
    final loginSuccess = await neon.login(email, matKhau);
    if (!loginSuccess) return false;

    // 2️⃣ Lấy dữ liệu sinh viên từ Neon
    final svData = await neon.getByEmail(email);
    if (svData == null) return false;

    student = svData;

    // 3️⃣ Lưu SQLite (xóa cũ, insert mới)
    await sqlite.insertSinhVien(student!);

    // 4️⃣ Lấy lại từ SQLite để đảm bảo dữ liệu đồng bộ
    student = await sqlite.getSinhVien();
    debugPrint("Sinh viên lưu SQLite: ${student!.email}");

    // 5️⃣ Lấy danh sách ngành từ Neon và lưu SQLite
    final dsNganh = await neon.getNganh();
    if (dsNganh.isNotEmpty) {
      await sqlite.saveNganh(dsNganh);
      debugPrint("Danh sách ngành đã lưu SQLite: ${dsNganh.length} ngành");
    }

    return true;
  } catch (e, st) {
    debugPrint("Lỗi đăng nhập: $e");
    debugPrintStack(stackTrace: st);
    return false;
  }
}

/// Hàm kiểm tra đăng nhập tự động (nếu đã lưu SQLite)
Future<bool> autoLogin() async {
  try {
    final savedUser = await sqlite.getSinhVien();
    if (savedUser.email != null && savedUser.matkhau != null) {
      final ok = await neon.login(savedUser.email!, savedUser.matkhau!);
      if (ok) {
        student = savedUser;
        debugPrint("Tự động đăng nhập thành công: ${student!.email}");
        return true;
      }
    }
    return false;
  } catch (e, st) {
    debugPrint("Lỗi autoLogin: $e");
    debugPrintStack(stackTrace: st);
    return false;
  }
}
