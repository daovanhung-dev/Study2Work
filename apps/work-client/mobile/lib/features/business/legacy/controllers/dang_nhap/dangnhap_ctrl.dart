import 'package:study2work_mobile/features/business/legacy/helper_db/helper_supabase.dart';
import 'package:study2work_mobile/features/business/legacy/helper_db/helper_db.dart';
import 'package:study2work_mobile/features/business/legacy/models/doanh_nghiep.dart';
import 'package:study2work_mobile/features/business/legacy/models/dn_supabase.dart';

final sqlite = HelperDB.instance;
final neon = DNSupabase.instance;
DoanhNghiep? dn;
DoanhNghiepSB? dnSb;

Future<bool> dangNhapDN(String gmail, String matKhau) async {
  if (await neon.ktDangNhap(gmail, matKhau) == true) {
    final response = await neon.getDN(gmail);
    dn = DoanhNghiep.fromMap(response);
    await sqlite.saveDoanhNghiep(dn!);
    //lay du lieu cac nganh
    final response2 = await neon.getNganh();

    await sqlite.saveNganh(response2);

    return true;
  }
  return false;
}

Future<bool> autoLogin() async {
  try {
    final savedUser = await sqlite.getDangNhap();
    final email = savedUser?['email']?.toString();
    final password = savedUser?['matkhau']?.toString();
    if (email == null || password == null) return false;

    final ok = await neon.ktDangNhap(email, password);
    if (!ok) return false;

    dn = await sqlite.getDoanhNghiep();
    return dn != null;
  } catch (_) {
    return false;
  }
}
