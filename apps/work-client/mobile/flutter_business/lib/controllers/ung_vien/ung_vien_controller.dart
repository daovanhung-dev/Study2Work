import 'package:learn2earn/helper_db/helper_db.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import 'package:learn2earn/helper_db/helper_supabase.dart';
import 'package:learn2earn/models/ung_vien.dart';
import 'package:learn2earn/models/CV.dart';
import 'package:learn2earn/models/chat.dart';

final dbHelper = HelperDB.instance;
final supabase = DNSupabase.instance;

class UngTuyenCtrl {
  Future<List<CV>> getCV() async {
    final response = await supabase.getCV();
    return response;
  }

  Future<void> ungTuyen(int sinhvien_id) async {
    await supabase.ungTuyen(sinhvien_id);

    //tao doan chat
    await supabase.insertDoanChat({
      'sinhvien_id': sinhvien_id,
      'doanhnghiep_id': await dbHelper.getID(),
    });
    final idDN = await dbHelper.getID();
    await supabase.guiTinNhan(sinhvien_id, idDN, "Bạn đã được công ty ứng tuyển!");

  }

  Future<void> delCV(int sinhvien_id) async{
    await supabase.delCV(sinhvien_id);
  }

  Future<List<String>> getTrangThai() async {
    final response = await supabase.getUngVien();

    // Nếu response là null, trả về danh sách rỗng
    if (response == null) return [];

    // Lấy danh sách trạng thái
    return response
        .map((e) => e.trangthai ?? 'chưa xác định') // đảm bảo không null
        .toList();
  }



}
