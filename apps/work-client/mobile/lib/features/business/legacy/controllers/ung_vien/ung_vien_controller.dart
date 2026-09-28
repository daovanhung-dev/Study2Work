import 'package:study2work_mobile/features/business/legacy/helper_db/helper_db.dart';
import 'package:study2work_mobile/features/business/legacy/helper_db/helper_supabase.dart';
import 'package:study2work_mobile/features/business/legacy/models/cv.dart';

final dbHelper = HelperDB.instance;
final supabase = DNSupabase.instance;

class UngTuyenCtrl {
  Future<List<CV>> getCV() async {
    final response = await supabase.getCV();
    return response;
  }

  Future<void> ungTuyen(int sinhvienId) async {
    await supabase.ungTuyen(sinhvienId);

    //tao doan chat
    await supabase.insertDoanChat({
      'sinhvien_id': sinhvienId,
      'doanhnghiep_id': await dbHelper.getID(),
    });
    final idDN = await dbHelper.getID();
    await supabase.guiTinNhan(
      sinhvienId,
      idDN,
      "Bạn đã được công ty ứng tuyển!",
    );
  }

  Future<void> delCV(int sinhvienId) async {
    await supabase.delCV(sinhvienId);
  }

  Future<List<String>> getTrangThai() async {
    final response = await supabase.getUngVien();

    // Lấy danh sách trạng thái
    return response
        .map((e) => e.trangthai ?? 'chưa xác định') // đảm bảo không null
        .toList();
  }
}
