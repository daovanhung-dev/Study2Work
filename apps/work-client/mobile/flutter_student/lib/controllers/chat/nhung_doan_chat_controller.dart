import 'package:supabase_flutter/supabase_flutter.dart';

final supabase = Supabase.instance.client;

Future<List<Map<String, dynamic>>> getChats(int svId) async {
  final response = await supabase
      .from('doanchat')
      .select('doanhnghiep_id')
      .eq('sinhvien_id', svId);

  List<int> doanhnghiepIds = response.map((row) => row['doanhnghiep_id'] as int).toList();

  if (doanhnghiepIds.isEmpty) return [];

  final responseSv = await supabase
      .from('doanhnghiep')
      .select('id, hoten')
      .inFilter('id', doanhnghiepIds);

  List<Map<String, dynamic>> chats = responseSv.map((row) => {
    "id": row['id'],
    "hoten": row['hoten'],
  }).toList();

  return chats;
}
