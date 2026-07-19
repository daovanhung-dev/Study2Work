import 'package:supabase_flutter/supabase_flutter.dart';
import '../lay_ten.dart';
import 'package:supabase/supabase.dart' hide RealtimeClient;

final supabase = Supabase.instance.client;

/// Lấy lịch sử chat giữa SV và DN
Future<List<Map<String, dynamic>>> getChat(
    int sinhvienId,
    int doanhnghiepId,
    ) async {
  final response = await supabase
      .from('chat')
      .select('id, nguoigui, nguoinhan, noidung, ngaygui, trangthai')
      .eq('sinhvien_id', sinhvienId)
      .eq('doanhnghiep_id', doanhnghiepId)
      .order('ngaygui', ascending: true);

  final data = response as List;
  return data.map((row) => {
    "id": row['id'],
    "nguoigui": row['nguoigui'],
    "nguoinhan": row['nguoinhan'],
    "noidung": row['noidung'],
    "ngaygui": row['ngaygui'],
    "trangthai": row['trangthai'],
  }).toList();
}

/// Gửi tin nhắn mới
Future<void> guiTinNhan(
    int sinhvienId,
    int doanhnghiepId,
    String noidung,
    ) async {


  await supabase.from('chat').insert({
    'sinhvien_id': sinhvienId,
    'doanhnghiep_id': doanhnghiepId,
    'nguoigui': sinhvienId,
    'nguoinhan': doanhnghiepId,
    'noidung': noidung,
    'ngaygui': DateTime.now().toIso8601String(), // nên thêm timestamp
  });
}

/// Đăng ký lắng nghe tin nhắn realtime
RealtimeChannel subscribeMessages(Function(Map<String, dynamic>) onMessage) {
  final channel = supabase.channel('public:chat').onPostgresChanges(
    event: PostgresChangeEvent.insert,
    schema: 'public',
    table: 'chat',
    callback: (payload) {
      // debug
      print('Realtime payload: ${payload.newRecord}');
      onMessage(payload.newRecord);
    },
  ).subscribe();
  return channel;
}
