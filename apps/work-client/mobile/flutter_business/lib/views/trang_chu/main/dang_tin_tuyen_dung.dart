import 'package:flutter/material.dart';
import 'package:learn2earn/models/JD.dart';
import 'package:learn2earn/helper_db/helper_supabase.dart';
import 'package:learn2earn/helper_db/helper_db.dart';
import 'package:supabase_flutter/supabase_flutter.dart';

final SupabaseClient client = Supabase.instance.client;
final DNSupabase DN = DNSupabase.instance;
final HelperDB dbHelper = HelperDB.instance;

class DangTinTuyenDung extends StatefulWidget {
  const DangTinTuyenDung({super.key});

  @override
  State<DangTinTuyenDung> createState() => _DangTinTuyenDungState();
}

class _DangTinTuyenDungState extends State<DangTinTuyenDung> {
  final _tenViTriController = TextEditingController();
  final _phongBanController = TextEditingController();
  final _capBacController = TextEditingController();
  final _baoCaoChoController = TextEditingController();
  final _nhiemVuController = TextEditingController();
  final _trinhDoController = TextEditingController();
  final _kinhNghiemController = TextEditingController();
  final _kyNangController = TextEditingController();
  final _kyNangMemController = TextEditingController();
  final _uuTienController = TextEditingController();
  final _mucLuongController = TextEditingController();
  final _phucLoiController = TextEditingController();
  final _moiTruongController = TextEditingController();
  final _diaDiemController = TextEditingController();
  final _thoiGianController = TextEditingController();
  final _hanNopController = TextEditingController();
  final _cachUngTuyenController = TextEditingController();
  final _moTaController = TextEditingController();
  int id_DN = 0;

  @override
  void initState() {
    super.initState();
    _loadID();
  }

  Future<void> _loadID() async {
    int id = await dbHelper.getID();
    setState(() {
      id_DN = id;
    });
  }

  List<String> _splitText(String text) =>
      text.split(',').map((e) => e.trim()).where((e) => e.isNotEmpty).toList();

  Widget _buildSectionTitle(String title) => Padding(
    padding: const EdgeInsets.symmetric(vertical: 12),
    child: Row(
      children: [
        Icon(Icons.folder_open, color: Colors.blueAccent),
        SizedBox(width: 6),
        Text(title,
            style: TextStyle(
                fontSize: 16,
                fontWeight: FontWeight.bold,
                color: Colors.blueAccent)),
      ],
    ),
  );

  Widget _buildTextField(TextEditingController controller, String hint,
      {int maxLines = 1}) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 6),
      child: TextField(
        controller: controller,
        maxLines: maxLines,
        decoration: InputDecoration(
          hintText: hint,
          hintStyle: TextStyle(color: Colors.grey[500]),
          filled: true,
          fillColor: Colors.white,
          contentPadding: EdgeInsets.symmetric(horizontal: 16, vertical: 12),
          enabledBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(20),
            borderSide:
            BorderSide(color: Colors.blueAccent.shade100, width: 1.5),
          ),
          focusedBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(20),
            borderSide: BorderSide(color: Colors.blueAccent, width: 2),
          ),
        ),
      ),
    );
  }

  Widget _buildButton(String text, Color bg, Color fg, VoidCallback onTap) {
    return Expanded(
      child: ElevatedButton(
        onPressed: onTap,
        style: ElevatedButton.styleFrom(
            backgroundColor: bg,
            foregroundColor: fg,
            minimumSize: Size(double.infinity, 50),
            shape:
            RoundedRectangleBorder(borderRadius: BorderRadius.circular(25)),
            elevation: 3),
        child: Text(text, style: TextStyle(fontSize: 16)),
      ),
    );
  }

  bool _validateInput() {
    if (_tenViTriController.text.isEmpty ||
        _phongBanController.text.isEmpty ||
        _capBacController.text.isEmpty ||
        _baoCaoChoController.text.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Vui lòng điền đầy đủ thông tin chung.")),
      );
      return false;
    }
    if (_nhiemVuController.text.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Vui lòng nhập nhiệm vụ chính.")),
      );
      return false;
    }
    if (_trinhDoController.text.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Vui lòng nhập trình độ học vấn.")),
      );
      return false;
    }
    if (_diaDiemController.text.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Vui lòng nhập địa điểm làm việc.")),
      );
      return false;
    }
    return true;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey[100],
      appBar: AppBar(
        title: Text("Đăng Tin Tuyển Dụng"),
        backgroundColor: Colors.blueAccent,
        elevation: 0,
      ),
      body: SingleChildScrollView(
        padding: EdgeInsets.symmetric(horizontal: 16, vertical: 10),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            _buildSectionTitle("Thông tin chung"),
            _buildTextField(_tenViTriController, "Tên vị trí"),
            _buildTextField(_phongBanController, "Phòng ban"),
            _buildTextField(_capBacController, "Cấp bậc"),
            _buildTextField(_baoCaoChoController, "Báo cáo cho"),

            _buildSectionTitle("Mô tả công việc"),
            _buildTextField(_nhiemVuController,
                "Nhiệm vụ chính (ngăn cách bởi dấu ,)", maxLines: 3),

            _buildSectionTitle("Yêu cầu công việc"),
            _buildTextField(_trinhDoController, "Trình độ học vấn"),
            _buildTextField(_kinhNghiemController, "Kinh nghiệm"),
            _buildTextField(_kyNangController,
                "Kỹ năng chuyên môn (ngăn cách bởi dấu ,)", maxLines: 2),
            _buildTextField(_kyNangMemController,
                "Kỹ năng mềm (ngăn cách bởi dấu ,)", maxLines: 2),
            _buildTextField(_uuTienController,
                "Ưu tiên (ngăn cách bởi dấu ,)", maxLines: 2),

            _buildSectionTitle("Quyền lợi"),
            _buildTextField(_mucLuongController, "Mức lương"),
            _buildTextField(_phucLoiController,
                "Phúc lợi (ngăn cách bởi dấu ,)", maxLines: 2),
            _buildTextField(_moiTruongController, "Môi trường làm việc"),

            _buildSectionTitle("Thông tin khác"),
            _buildTextField(_diaDiemController, "Địa điểm"),
            _buildTextField(_thoiGianController, "Thời gian làm việc"),
            _buildTextField(_hanNopController, "Hạn nộp (YYYY-MM-DD)"),
            _buildTextField(_cachUngTuyenController, "Cách ứng tuyển"),
            _buildTextField(_moTaController, "Mô tả", maxLines: 4),

            SizedBox(height: 20),
            Row(
              children: [
                _buildButton(
                    "Hủy", Colors.grey[300]!, Colors.black, () => Navigator.pop(context)),
                SizedBox(width: 15),
                _buildButton("Lưu", Colors.blueAccent, Colors.white, () async {
                  // 1. Kiểm tra các trường bắt buộc
                  final requiredFields = {
                    "Tên vị trí": _tenViTriController.text,
                    "Phòng ban": _phongBanController.text,
                    "Cấp bậc": _capBacController.text,
                    "Báo cáo cho": _baoCaoChoController.text,
                    "Nhiệm vụ chính": _nhiemVuController.text,
                    "Trình độ": _trinhDoController.text,
                    "Địa điểm": _diaDiemController.text,
                  };

                  for (var entry in requiredFields.entries) {
                    if (entry.value.trim().isEmpty) {
                      ScaffoldMessenger.of(context).showSnackBar(
                        SnackBar(content: Text("Vui lòng nhập ${entry.key}")),
                      );
                      return;
                    }
                  }

                  // 2. Kiểm tra số cho mức lương
                  if (_mucLuongController.text.isNotEmpty &&
                      double.tryParse(_mucLuongController.text) == null) {
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(content: Text("Mức lương phải là số hợp lệ")),
                    );
                    return;
                  }

                  // 3. Kiểm tra định dạng ngày cho hạn nộp
                  if (_hanNopController.text.isNotEmpty) {
                    try {
                      DateTime.parse(_hanNopController.text);
                    } catch (e) {
                      ScaffoldMessenger.of(context).showSnackBar(
                        SnackBar(content: Text("Hạn nộp phải theo định dạng YYYY-MM-DD")),
                      );
                      return;
                    }
                  }

                  print("Bấm Lưu Rồi");

                  // 4. Tạo object JD
                  final JD jd = JD.fromMap({
                    "doanhnghiep_id": id_DN,
                    "ten_vi_tri": _tenViTriController.text,
                    "phong_ban": _phongBanController.text,
                    "cap_bac": _capBacController.text,
                    "bao_cao_cho": _baoCaoChoController.text,
                    "nhiem_vu": _splitText(_nhiemVuController.text),
                    "trinh_do": _trinhDoController.text,
                    "kinh_nghiem": _kinhNghiemController.text,
                    "ky_nang": _splitText(_kyNangController.text),
                    "ky_nang_mem": _splitText(_kyNangMemController.text),
                    "uu_tien": _splitText(_uuTienController.text),
                    "muc_luong": _mucLuongController.text,
                    "phuc_loi": _splitText(_phucLoiController.text),
                    "moi_truong": _moiTruongController.text,
                    "dia_diem": _diaDiemController.text,
                    "thoi_gian": _thoiGianController.text,
                    "han_nop": _hanNopController.text,
                    "cach_ung_tuyen": _cachUngTuyenController.text,
                    "mo_ta": _moTaController.text,
                  });

                  // 5. Gửi dữ liệu lên Supabase
                  final response = await client.from('jd').insert({
                    "doanhnghiep_id": id_DN,
                    "ten_vi_tri": _tenViTriController.text,
                    "phong_ban": _phongBanController.text,
                    "cap_bac": _capBacController.text,
                    "bao_cao_cho": _baoCaoChoController.text,
                    "nhiem_vu": _splitText(_nhiemVuController.text),
                    "trinh_do": _trinhDoController.text,
                    "kinh_nghiem": _kinhNghiemController.text,
                    "ky_nang": _splitText(_kyNangController.text),
                    "ky_nang_mem": _splitText(_kyNangMemController.text),
                    "uu_tien": _splitText(_uuTienController.text),
                    "muc_luong": _mucLuongController.text,
                    "phuc_loi": _splitText(_phucLoiController.text),
                    "moi_truong": _moiTruongController.text,
                    "dia_diem": _diaDiemController.text,
                    "thoi_gian": _thoiGianController.text,
                    "han_nop": _hanNopController.text,
                    "cach_ung_tuyen": _cachUngTuyenController.text,
                    "mo_ta": _moTaController.text,
                  });

                  print("Dữ liệu đăng tin: $jd");
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(content: Text("Đăng tin thành công!")),
                  );
                  //Navigator.pop(context);
                }),
              ],
            ),
            SizedBox(height: 30),
          ],
        ),
      ),
    );
  }
}
