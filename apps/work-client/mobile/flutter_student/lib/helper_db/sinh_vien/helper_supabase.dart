import 'package:supabase_flutter/supabase_flutter.dart';
import 'package:learn2earn/models/sinh_vien/sinh_vien.dart';
import 'package:learn2earn/models/sinh_vien/NganhNghe.dart';
import 'package:learn2earn/models/sinh_vien/doan_chat.dart';
import 'package:learn2earn/models/sinh_vien/JD.dart';
import 'package:learn2earn/models/sinh_vien/ung_vien.dart';
import 'package:learn2earn/models/sinh_vien/CV.dart';

class SinhVienSupabaseHelper {
  final SupabaseClient client = Supabase.instance.client;
  final String tableName = 'sinhvien';

  // 🟢 Lấy toàn bộ danh sách sinh viên
  Future<List<SinhVien>> getAll() async {
    final response = await client.from(tableName).select();

    // Nếu response là List, map sang List<SinhVien>
    final data = response as List<dynamic>;
    return data.map((e) => SinhVien.fromMap(e)).toList();
  }

  // 🟢 Thêm sinh viên mới
  Future<void> insert(SinhVien sv) async {
    await client.from(tableName).insert(sv.toMap());
  }

  // 🟡 Cập nhật thông tin sinh viên
  Future<void> update(SinhVien sv) async {
    if (sv.id == null) return;
    await client.from(tableName).update(sv.toMap()).eq('id', sv.id!);
  }

  // 🔴 Xóa sinh viên theo id
  Future<void> delete(int id) async {
    await client.from(tableName).delete().eq('id', id);
  }

  // 🔍 Tìm sinh viên theo email
  Future<SinhVien?> getByEmail(String email) async {
    final response = await client
        .from(tableName)
        .select()
        .eq('email', email)
        .maybeSingle();

    if (response == null) return null;
    return SinhVien.fromMap(response);
  }

  // 🔐 Kiểm tra đăng nhập (email + mật khẩu)
  Future<bool> login(String email, String matkhau) async {
    final response = await client
        .from(tableName)
        .select()
        .eq('email', email)
        .eq('matkhau', matkhau)
        .maybeSingle();

    if (response == null) return false;
    return true;
  }

  //lay cach nganh( phuc vu chuc nang tim kiem)
  Future<List<Nganh>> getNganh() async {
    final response = await client.from('bannganh').select('nganh');
    return response.map((e) => Nganh.fromMap(e)).toList();
  }

  //lay doan chat
  Future<List<DoanChat>> getDoanChat(int id) async {
    final response = await client
        .from('doanchat')
        .select()
        .eq('sinhvien_id', id);
    return response.map((e) => DoanChat.fromMap(e)).toList();
  }

  //lay doanh nghiep
  Future<String> getNameDN(int DN_id) async {
    final response = await client
        .from('doanhnghiep')
        .select('hoten')
        .eq('id', DN_id)
        .single();
    return response['hoten'];
  }

  //==============================================================================
  //Job
  //lay JD
  Future<List<JD>> getTopJD() async {
    // Lấy toàn bộ danh sách jd_id trong bảng topJD
    final topJDResponse = await client.from('topJD').select('jd_id');

    // Nếu không có dữ liệu thì trả về danh sách rỗng
    if (topJDResponse.isEmpty) return [];

    // Lấy danh sách các id
    final List<int> jdIds = topJDResponse
        .map<int>((row) => row['jd_id'] as int)
        .toList();

    // Truy vấn toàn bộ JD có id trong danh sách jdIds
    final jdResponse = await client.from('jd').select().inFilter('id', jdIds);

    // Chuyển sang danh sách model JD
    final jobs = jdResponse.map<JD>((e) => JD.fromMap(e)).toList();

    return jobs;
  }

  Future<JD> getJD(int id) async {
    final response = await client.from('jd').select().eq('id', id).single();
    return JD.fromMap(response);
  }

  Future<List<JD>> getAllJD() async {
    final data = await client.from('jd').select();
    return (data as List).map((e) => JD.fromMap(e)).toList();
  }

  //lay jd bang
  Future<int> getIdDnByIdJd(int idJD) async {
    final response = await client
        .from('jd')
        .select('doanhnghiep_id')
        .eq('id', idJD)
        .single();
    return response['doanhnghiep_id'] as int;
  }

  //================================================================================
  //ung vien
  /// 🟢 Thêm một bản ghi ứng viên mới
  Future<bool> insertUngVien(UngVien uv) async {
    try {
      // 1️⃣ Kiểm tra xem sinh viên đã ứng tuyển vào JD này chưa
      final kt = await client
          .from('ungvien')
          .select('id')
          .eq('jd_id', uv.jdId!)
          .eq('sinhvien_id', uv.sinhvienId!)
          .maybeSingle(); // Trả về null nếu không có dòng nào khớp

      // 2️⃣ Nếu đã có, trả về false (đã ứng tuyển rồi)
      if (kt != null) {
        return false;
      }

      // 3️⃣ Nếu chưa có, thêm mới vào bảng
      await client.from('ungvien').insert({
        'sinhvien_id': uv.sinhvienId,
        'doanhnghiep_id': uv.doanhnghiepId,
        'trangthai': uv.trangthai ?? 'chưa ứng tuyển',
        'jd_id': uv.jdId,
      });

      return true; // thành công
    } catch (e) {
      throw Exception('Lỗi khi thêm ứng viên: $e');
    }
  }

  //================================================================================
  //cv
  Future<CV?> getCVById(int id) async {
    try {
      final response = await client
          .from('cv')
          .select('*')
          .eq('id', id)
          .maybeSingle();

      if (response == null) return null;
      return CV.fromMap(response);
    } catch (e) {
      throw Exception('Lỗi khi lấy CV theo ID: $e');
    }
  }

  Future<void> updateCV(CV cv) async
  {
    await client.from('cv').update(cv.toMap()).eq('id', cv.id!);
  }
}
