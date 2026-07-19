import 'package:learn2earn/models/DNSupabase.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import 'package:learn2earn/helper_db/helper_db.dart';
import 'package:learn2earn/models/JD.dart';
import 'package:learn2earn/models/NganhNghe.dart';
import 'package:learn2earn/models/ung_vien.dart';
import 'package:learn2earn/models/CV.dart';

final HelperDB dbHelper = HelperDB.instance;

class DNSupabase {
  static final DNSupabase instance = DNSupabase._internal();

  factory DNSupabase() {
    return instance;
  }

  DNSupabase._internal();

  final SupabaseClient client = Supabase.instance.client;

  Future<bool> ktDangNhap(String gmail, String matKhau) async {
    final response = await client
        .from('doanhnghiep')
        .select()
        .eq('email', '$gmail')
        .eq('matkhau', '$matKhau')
        .single();

    if (response.isNotEmpty)
      return true;
    else
      return false;
  }

  Future<Map<String, dynamic>> getDN(String email) async {
    final response = await client
        .from('doanhnghiep')
        .select()
        .eq('email', '$email')
        .single();
    print("hello3");
    return response;
  }

  //lay
  Future<List<Nganh>> getNganh() async {
    final response = await client.from('bannganh').select('nganh');
    List<Nganh> Nganh_nghe = response.map((e) => Nganh.fromMap(e)).toList();

    return Nganh_nghe;
  }

  //lay anh
  Future<String> getAVT(int id) async {
    final response = await client
        .from('doanhnghiep')
        .select('avt')
        .eq('id', '$id')
        .single();
    return response['avt'] as String;
  }

  Future<List<Map<String, dynamic>>> layUngVien() async {
    final response = await client
        .from('ungvien')
        .select('sinhvien_id')
        .eq('doanhnghiep_id', await dbHelper.getID());

    if (response.isEmpty) return [];

    // Lấy danh sách id sinh viên
    final List<int> sinhvienIds = response
        .map<int>((row) => row['sinhvien_id'] as int)
        .toList();

    // Truy vấn toàn bộ CV có id trong danh sách
    final response2 = await client
        .from('cv')
        .select()
        .inFilter('id', sinhvienIds);

    return List<Map<String, dynamic>>.from(response2);
  }

  Future<List<String>> layTrangThai() async {
    final response = await client
        .from('ungvien')
        .select('trangthai')
        .eq('doanhnghiep_id', await dbHelper.getID());

    List<String> trangThai = [];
    for (var i = 0; i < response.length; i++) {
      trangThai.add(response[i]['trangthai']);
    }
    return trangThai;
  }

  //========================================JD============================================================
  //Nhap dữ liệu cho JD
  Future<void> insertJD(Map<String, dynamic> data) async {
    final response = await client.from('jd').insert(data);
    print(response);
  }

  //Lấy dữ liệu từ JD
  Future<JD> getJD(int maJD) async {
    final response = await client
        .from('jd')
        .select()
        .eq('id', '$maJD')
        .single();
    return JD.fromMap(response);
  }

  //============ung tuyen===================

  Future<List<CV>> getCV() async {
    final response = await client
        .from('ungvien')
        .select()
        .eq('doanhnghiep_id', await dbHelper.getID());

    List<CV> ungVien = [];
    for (var i = 0; i < response.length; i++) {
      final response2 = await client
          .from('cv')
          .select()
          .eq('id', response[i]['sinhvien_id'])
          .single();
      CV cv = CV.fromMap(response2);
      ungVien.add(cv);
    }
    return ungVien;
  }

  Future<List<UngVien>> getUngVien() async {
    final response = await client
        .from('ungvien')
        .select()
        .eq('doanhnghiep_id', await dbHelper.getID());
    List<UngVien> ungVien = [];
    for (var i = 0; i < response.length; i++) {
      ungVien.add(UngVien.fromMap(response[i]));
    }
    return ungVien;
  }

  Future<void> ungTuyen(int sinhvien_id) async {
    await client
        .from('ungvien')
        .update({'trangthai': 'Đã ứng tuyển'})
        .eq('sinhvien_id', sinhvien_id);
  }

  Future<void> delCV(int sinhvien_id) async{
    await client.from('ungvien').delete().eq('sinhvien_id', sinhvien_id);
  }
  //doan chat
  Future<void> insertDoanChat(Map<String, dynamic> data) async {
    await client.from('doanchat').insert(data);
  }

  //chat
  Future<void> guiTinNhan(
    int sinhvienId,
    int doanhnghiepId,
    String noidung,
  ) async {
    await client.from('chat').insert({
      'sinhvien_id': sinhvienId,
      'doanhnghiep_id': doanhnghiepId,
      'nguoigui': doanhnghiepId,
      'nguoinhan': sinhvienId,
      'noidung': noidung,
      'ngaygui': DateTime.now().toIso8601String(), // nên thêm timestamp
    });
  }
}
