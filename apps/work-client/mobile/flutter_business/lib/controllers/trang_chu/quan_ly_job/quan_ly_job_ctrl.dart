import 'package:supabase_flutter/supabase_flutter.dart';
import 'package:learn2earn/models/JD.dart';
import 'package:learn2earn/helper_db/helper_db.dart';
final supabase = Supabase.instance.client;
final HelperDB dbHelper = HelperDB.instance;

Future<List<JD>> getJob() async {
  final int doanhnghiep_id = await dbHelper.getID();
  final response = await supabase
      .from('jd')
      .select('id, ten_vi_tri, cap_bac, nhiem_vu, trinh_do, kinh_nghiem, muc_luong, dia_diem, thoi_gian')
  .eq('doanhnghiep_id', '$doanhnghiep_id');

  // Ép kiểu response sang List<dynamic>
  final List<dynamic> data = response;

  // Chuyển List<Map> → List<JD>
  List<JD> jobs = data.map((e) => JD.fromMap(e)).toList();

  return jobs;
}


