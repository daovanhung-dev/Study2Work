import 'package:supabase_flutter/supabase_flutter.dart';

final supabase = Supabase.instance.client;

Future<Map<String, dynamic>?> getNameSV(int id) async {
  final response = await supabase
      .from('sinhvien')
      .select('hoten')
      .eq('id', id);

  // Kiểm tra có dữ liệu hay không
  if (response.isNotEmpty) {
    return {
      "ten": response[0]['hoten'],
    };
  } else {
    return null; // hoặc {"ten": ""} nếu bạn muốn trả về mặc định
  }
}


Future<Map<String, dynamic>?> getNameDN(int id) async {
  final response = await supabase
      .from('doanhnghiep')
      .select('hoten')
      .eq('id', id);

  // Kiểm tra có dữ liệu hay không
  if (response.isNotEmpty) {
    return {
      "hoten": response[0]['hoten'],
    };
  } else {
    return null; // hoặc {"ten": ""} nếu bạn muốn trả về mặc định
  }
}


