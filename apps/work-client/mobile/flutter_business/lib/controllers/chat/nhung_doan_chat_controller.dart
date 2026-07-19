import 'package:supabase_flutter/supabase_flutter.dart';

final supabase = Supabase.instance.client;

Future<List<Map<String, dynamic>>> getChats(int dnId) async {
  final response = await supabase
      .from('doanchat')
      .select('sinhvien_id')
      .eq('doanhnghiep_id', dnId);

  List<int> studentIds = response.map((row) => row['sinhvien_id'] as int).toList();

  if (studentIds.isEmpty) return [];

  final responseSv = await supabase
      .from('sinhvien')
      .select('id, hoten')
      .inFilter('id', studentIds);

  List<Map<String, dynamic>> chats = responseSv.map((row) => {
    "id": row['id'],
    "hoten": row['hoten'],
  }).toList();

  return chats;
}
