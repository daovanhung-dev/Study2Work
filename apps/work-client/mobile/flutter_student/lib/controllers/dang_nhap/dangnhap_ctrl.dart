import 'package:flutter/foundation.dart';
import 'package:learn2earn/helper_db/sinh_vien/helper_db.dart';
import 'package:learn2earn/helper_db/sinh_vien/helper_supabase.dart';
import 'package:learn2earn/models/sinh_vien/sinh_vien.dart';
import 'package:learn2earn/models/outmeta/NganhNghe.dart';

final Sqlite = SinhVienSQLiteHelper.instance;
final Supabase = SinhVienSupabaseHelper();
SinhVien? SV;

/// Hàm đăng nhập
/// Trả về true nếu thành công, false nếu thất bại
Future<bool> dangNhapDN(String email, String matKhau) async {
  try {
    // 1️⃣ Kiểm tra đăng nhập với Supabase
    final loginSuccess = await Supabase.login(email, matKhau);
    if (!loginSuccess) return false;

    // 2️⃣ Lấy dữ liệu sinh viên từ Supabase
    final svData = await Supabase.getByEmail(email);
    if (svData == null) return false;

    SV = svData;

    // 3️⃣ Lưu SQLite (xóa cũ, insert mới)
    await Sqlite.insertSinhVien(SV!);

    // 4️⃣ Lấy lại từ SQLite để đảm bảo dữ liệu đồng bộ
    SV = await Sqlite.getSinhVien();
    debugPrint("Sinh viên lưu SQLite: ${SV!.email}");

    // 5️⃣ Lấy danh sách ngành từ Supabase và lưu SQLite
    final dsNganh = await Supabase.getNganh();
    if (dsNganh.isNotEmpty) {
      await Sqlite.saveNganh(dsNganh);
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
    final savedUser = await Sqlite.getSinhVien();
    if (savedUser.email != null && savedUser.matkhau != null) {
      final ok = await Supabase.login(savedUser.email!, savedUser.matkhau!);
      if (ok) {
        SV = savedUser;
        debugPrint("Tự động đăng nhập thành công: ${SV!.email}");
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
