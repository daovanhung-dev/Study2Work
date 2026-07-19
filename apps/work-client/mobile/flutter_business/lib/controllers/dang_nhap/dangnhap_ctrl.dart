import 'package:learn2earn/helper_db/helper_supabase.dart';
import 'package:learn2earn/helper_db/helper_db.dart';
import 'package:learn2earn/models/doanh_nghiep.dart';
import 'package:learn2earn/models/DNSupabase.dart';
import 'package:flutter/foundation.dart';
import 'package:learn2earn/models/NganhNghe.dart';

final Sqlite = HelperDB.instance;
final Supabase = DNSupabase.instance;
DoanhNghiep? DN ;
DoanhNghiepSB? DN_SB;


Future<bool> dangNhapDN(String gmail, String matKhau) async {

  if (await Supabase.ktDangNhap(gmail, matKhau)==true) {
    final response = await Supabase.getDN(gmail);
    print("Dữ liệu nhận từ Supabase: $response");
    DN = DoanhNghiep.fromMap(response);
    await Sqlite.saveDoanhNghiep(DN!);
    //lay du lieu cac nganh
    final response2 = await Supabase.getNganh();

    await Sqlite.saveNganh(response2);

    
    return true;
  }
  return false;
}