import 'package:supabase_flutter/supabase_flutter.dart';

final supabase = Supabase.instance.client;

Future<Map<String, dynamic>> xemChiTiet(int id) async {
  final response = await supabase
      .from('ungvien')
      .select('id, avt, vitri, ten, cn, kn, skill, hv, luong')
      .eq('id', id)
      .maybeSingle();

  if (response == null) {
    return {}; // không tìm thấy dữ liệu
  }

  return {
    'macv_ds': response['id'],
    'avt_ds': response['avt'],
    'vitri_ds': response['vitri'],
    'ten_ds': response['ten'],
    'cn_ds': response['cn'],
    'kn_ds': response['kn'],
    'skill_ds': List<String>.from(response['skill'] ?? []),
    'hv_ds': response['hv'],
    'luong_ds': response['luong'],
  };
}
