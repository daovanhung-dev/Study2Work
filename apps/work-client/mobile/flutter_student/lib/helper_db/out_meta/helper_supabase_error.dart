import 'package:learn2earn/models/outmeta/DNSupabase.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import 'package:learn2earn/helper_db/out_meta/helper_db_error.dart';
import 'package:learn2earn/models/outmeta/JD.dart';
import 'package:learn2earn/models/outmeta/NganhNghe.dart';

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

  //========================================JD============================================================
  //Nhap dữ liệu cho JD
  Future<void> insertJD(Map<String, dynamic> data) async {
    final response = await client.from('jd').insert(data);
    print(response);
  }

  //Lấy dữ liệu từ JD
  Future<JD> getJD(int maJD) async {
    final id = await dbHelper.getID();
    final response = await client
        .from('jd')
        .select()
        .eq('id', '$maJD')
        .single();
    return JD.fromMap(response);
  }
}
