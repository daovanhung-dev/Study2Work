import 'package:supabase_flutter/supabase_flutter.dart';
import 'package:learn2earn/models/sinh_vien/JD.dart';

/// ✅ Controller dành cho chức năng xem chi tiết JD
/// Tách riêng để dễ bảo trì và test
class XemChiTietController {
  final SupabaseClient client = Supabase.instance.client;
  final String tableName = 'jd';

  /// 🟢 Lấy toàn bộ danh sách JD
  Future<List<JD>> getAllJD() async {
    final response = await client.from(tableName).select();

    if (response == null || response.isEmpty) {
      return [];
    }

    // Ép kiểu sang List<JD>
    return (response as List<dynamic>).map((e) => JD.fromMap(e)).toList();
  }

  /// 🔍 Lấy chi tiết một JD theo ID
  Future<JD> xemChiTiet(int id) async {
    final response = await client
        .from(tableName)
        .select()
        .eq('id', id)
        .maybeSingle(); // maybeSingle() → null nếu không có

    if (response == null) {
      throw Exception('Không tìm thấy JD với id: $id');
    }

    return JD.fromMap(response);
  }

  /// 🧩 Lấy danh sách JD theo ngành
  Future<List<JD>> getJDByNganh(String nganh) async {
    final response =
    await client.from(tableName).select().eq('nganh', nganh);

    if (response == null || response.isEmpty) {
      return [];
    }

    return (response as List<dynamic>).map((e) => JD.fromMap(e)).toList();
  }

  /// 🧩 Lấy danh sách JD theo doanh nghiệp ID
  Future<List<JD>> getJDByDoanhNghiep(int doanhNghiepID) async {
    final response = await client
        .from(tableName)
        .select()
        .eq('doanh_nghiep_id', doanhNghiepID);

    if (response == null || response.isEmpty) {
      return [];
    }

    return (response as List<dynamic>).map((e) => JD.fromMap(e)).toList();
  }

  /// 🟡 Cập nhật JD (dành cho admin hoặc doanh nghiệp)
  Future<void> updateJD(JD jd) async {
    await client.from(tableName).update(jd.toMap()).eq('id', jd.id);
  }

  /// 🔴 Xóa JD theo ID (dành cho admin)
  Future<void> deleteJD(int id) async {
    await client.from(tableName).delete().eq('id', id);
  }
}
