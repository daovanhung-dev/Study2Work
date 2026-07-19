import 'package:learn2earn/helper_db/sinh_vien/helper_supabase.dart';
import 'package:learn2earn/models/sinh_vien/JD.dart';

class TimKiemCtrl {
  final helper = SinhVienSupabaseHelper();

  List<JD> jobs = [];
  List<JD> filtered = [];

  String diaDiem = "Tất cả";
  String loai = "Tất cả";
  String tuKhoa = "";

  // Lấy dữ liệu từ Supabase
  Future<void> loadJobs() async {
    jobs = await helper.getAllJD();
    filtered = List.from(jobs);
  }

  // Hàm lọc dữ liệu
  void filterJobs() {
    filtered = jobs.where((job) {
      final matchText = job.tenViTri.toLowerCase().contains(tuKhoa.toLowerCase()) ||
          job.tenCongTy.toLowerCase().contains(tuKhoa.toLowerCase());
      final matchDiaDiem = diaDiem == "Tất cả" || job.diaDiem == diaDiem;
      final matchLoai = loai == "Tất cả" || job.thoiGian == loai;
      return matchText && matchDiaDiem && matchLoai;
    }).toList();
  }
}
