// lib/services/cv_helper.dart
import 'package:supabase_flutter/supabase_flutter.dart';
import 'package:learn2earn/models/CV.dart';

class CVHelperDB {
  final SupabaseClient _client = Supabase.instance.client;
  final String table = 'cv';

  /// 🔹 Thêm 1 CV mới
  Future<CV?> insertCV(CV cv) async {
    try {
      final response = await _client
          .from(table)
          .insert(cv.toMap())
          .select()
          .single();
      return CV.fromMap(response);
    } catch (e) {
      print('❌ insertCV error: $e');
      return null;
    }
  }

  /// 🔹 Lấy tất cả CV
  Future<List<CV>> getAllCV() async {
    try {
      final data = await _client.from(table).select('*').order(
          'created_at', ascending: false);
      return (data as List).map((e) => CV.fromMap(e)).toList();
    } catch (e) {
      print('❌ getAllCV error: $e');
      return [];
    }
  }

  /// 🔹 Lấy CV theo ID
  Future<CV?> getCVById(int id) async {
    try {
      final data = await _client
          .from(table)
          .select()
          .eq('id', id)
          .maybeSingle();
      if (data == null) return null;
      return CV.fromMap(data);
    } catch (e) {
      print('❌ getCVById error: $e');
      return null;
    }
  }

  /// 🔹 Cập nhật CV
  Future<bool> updateCV(CV cv) async {
    if (cv.id == null) {
      print('⚠️ updateCV: CV chưa có id');
      return false;
    }
    try {
      await _client.from(table).update(cv.toMap()).eq('id', cv.id!);
      return true;
    } catch (e) {
      print('❌ updateCV error: $e');
      return false;
    }
  }

  /// 🔹 Xóa CV theo id
  Future<bool> deleteCV(int id) async {
    try {
      await _client.from(table).delete().eq('id', id);
      return true;
    } catch (e) {
      print('❌ deleteCV error: $e');
      return false;
    }
  }

  /// 🔹 Tìm kiếm CV theo tên hoặc ngành
  Future<List<CV>> searchCV(String keyword) async {
    try {
      final data = await _client
          .from(table)
          .select('*')
          .or('hoten.ilike.%$keyword%,nganh.ilike.%$keyword%')
          .order('created_at', ascending: false);

      return (data as List).map((e) => CV.fromMap(e)).toList();
    } catch (e) {
      print('❌ searchCV error: $e');
      return [];
    }
  }

  //lay chuyen nganh
  Future<List<String>> getNganh() async {
    final data = await _client
        .from('bannganh')
        .select('nganh');
    return (data as List).map((e) => e['nganh'] as String).toList();
  }
}