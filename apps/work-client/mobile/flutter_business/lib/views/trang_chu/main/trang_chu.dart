import 'package:flutter/material.dart';
import 'package:learn2earn/views/cai_dat/setting.dart';
import 'package:learn2earn/views/trang_chu/main/thong_tin_chi_tiet.dart';
import 'package:learn2earn/views/trang_chu/main/xem_chi_tiet_view.dart';
import 'package:learn2earn/views/ung_vien/ung_vien.dart';
import '../../tro_chuyen/tro_chuyen.dart';
import 'thong_bao.dart';
import 'dang_tin_tuyen_dung.dart';
import 'xem_chi_tiet.dart';
import '../tien_ich/Quan_ly_job/quan_ly_job.dart';
import '../tien_ich/Chuong_trinh_thuc_te/chuongTrinhThucTap.dart';
import '../tien_ich/Lich_phong_van/lichPV.dart';
import '../tien_ich/Lien_ket_nha_truong/lien_ket_nha_truong.dart';
import '../tien_ich/Loc_cv/LocCV.dart';
import '../tien_ich/Thong_ke/thong_ke.dart';
import 'dang_tin_tuyen_dung.dart';
import '/controllers/trang_chu/hien_thi_danh_sach_top_cv.dart';
import 'xem_chi_tiet.dart';
import 'package:intl/intl.dart';
import 'package:learn2earn/helper_db/helper_db.dart';
import 'package:learn2earn/helper_db/helper_supabase.dart';
import 'package:learn2earn/views/trang_chu/tien_ich/Tim_kiem_nhan_su/timKiemNhanSu.dart';
import 'package:learn2earn/views/trang_chu/tien_ich/Thong_ke/thongKeBaoCao.dart';

final sqlite = HelperDB.instance;
final supabase = DNSupabase.instance;

class trangChu extends StatefulWidget {
  const trangChu({super.key});

  @override
  State<trangChu> createState() => _trangChuState();
}

class _trangChuState extends State<trangChu> {
  String? name = '';
  String? img = '';

  Widget _infoTag(IconData icon, String? text) {
    if (text == null || text.isEmpty) return const SizedBox.shrink();
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
      decoration: BoxDecoration(
        color: Colors.blueAccent.withOpacity(0.08),
        borderRadius: BorderRadius.circular(8),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, size: 12, color: Colors.blueAccent),
          const SizedBox(width: 4),
          Text(
            text,
            style: const TextStyle(fontSize: 11, color: Colors.black87),
          ),
        ],
      ),
    );
  }

  List<Map<String, dynamic>> ds_cv = [];

  @override
  void initState() {
    super.initState();
    loadTopCV();
    loadTT();
  }

  //load thong tin
  Future<void> loadTT() async {
    name = await sqlite.getNameDN();
    int id = await sqlite.getID();
    img = await supabase.getAVT(id);
  }

  // Hàm async để lấy dữ liệu
  Future<void> loadTopCV() async {
    List<Map<String, dynamic>> result = await getTopCV();
    setState(() {
      ds_cv = result; // cập nhật biến
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Color(0xFF7ecbff),
        leading: Padding(
          padding: EdgeInsets.all(8), // chỉnh khoảng cách nếu muốn
          child: GestureDetector(
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => const thongTinChiTiet(),
                ),
              );
            },
            child: CircleAvatar(
              radius: 22, // Độ lớn ảnh tròn
              backgroundColor: Colors.grey[200],
              backgroundImage: NetworkImage('$img'),
              onBackgroundImageError: (_, __) {
                debugPrint('❌ Lỗi tải ảnh avatar');
              },
            ),
          ),
        ),
        title: Text('$name'),
        actions: [
          IconButton(
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => const thongBao()),
              );
            },
            icon: Icon(Icons.notifications),
          ),
        ],
      ),

      body: SizedBox.expand(
        child: Stack(
          children: [
            // Background full màn hình
            Container(
              decoration: BoxDecoration(),
              child: Image.asset(
                "assets/bg_trangchu.jpg",
                fit: BoxFit.cover,
                width: double.infinity,
                height: double.infinity,
              ),
            ),

            Padding(
              padding: EdgeInsets.only(top: 10),
              child: SingleChildScrollView(
                child: Center(
                  child: Column(
                    children: [
                      //Dang tin tuyen dung
                      Container(
                        margin: const EdgeInsets.symmetric(
                          vertical: 10,
                          horizontal: 16,
                        ),
                        padding: const EdgeInsets.symmetric(
                          vertical: 12,
                          horizontal: 14,
                        ),
                        decoration: BoxDecoration(
                          color: Colors.white,
                          borderRadius: BorderRadius.circular(12),
                          boxShadow: [
                            BoxShadow(
                              color: Colors.black.withOpacity(0.05),
                              blurRadius: 6,
                              offset: const Offset(0, 2),
                            ),
                          ],
                        ),
                        child: Row(
                          crossAxisAlignment: CrossAxisAlignment.center,
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            // Cột tiêu đề
                            Expanded(
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: const [
                                  Text(
                                    "Đăng tin tuyển dụng",
                                    style: TextStyle(
                                      fontSize: 14,
                                      fontWeight: FontWeight.w600,
                                    ),
                                  ),
                                  SizedBox(height: 4),
                                  Text(
                                    "Tạo tin mới ngay hôm nay",
                                    style: TextStyle(
                                      fontSize: 12,
                                      color: Colors.black54,
                                    ),
                                    overflow: TextOverflow.ellipsis,
                                  ),
                                ],
                              ),
                            ),

                            const SizedBox(width: 10),

                            // Nút hành động nhỏ gọn
                            ElevatedButton.icon(
                              onPressed: () {
                                Navigator.push(
                                  context,
                                  MaterialPageRoute(
                                    builder: (context) => const DangTinTuyenDung(),
                                  ),
                                );
                              },
                              icon: const Icon(Icons.add, size: 16),
                              label: const Text("Tạo"),
                              style: ElevatedButton.styleFrom(
                                backgroundColor: Colors.blueAccent,
                                foregroundColor: Colors.white,
                                padding: const EdgeInsets.symmetric(
                                  horizontal: 10,
                                  vertical: 8,
                                ),
                                shape: RoundedRectangleBorder(
                                  borderRadius: BorderRadius.circular(8),
                                ),
                                textStyle: const TextStyle(
                                  fontSize: 13,
                                  fontWeight: FontWeight.w500,
                                ),
                                elevation: 0,
                              ),
                            ),
                          ],
                        ),
                      ),

                      //Danh sach tuyen dung
                      Container(
                        width: double.infinity,
                        height: 300,
                        margin: const EdgeInsets.symmetric(
                          vertical: 12,
                          horizontal: 16,
                        ),
                        padding: const EdgeInsets.all(16),
                        decoration: BoxDecoration(
                          color: Colors.white,
                          borderRadius: BorderRadius.circular(16),
                          boxShadow: [
                            BoxShadow(
                              color: Colors.black.withOpacity(0.05),
                              blurRadius: 8,
                              offset: const Offset(0, 3),
                            ),
                          ],
                        ),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            const Text(
                              "Danh sách tuyển dụng nổi bật",
                              style: TextStyle(
                                fontSize: 15,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                            const SizedBox(height: 10),

                            Expanded(
                              child: FutureBuilder<List<Map<String, dynamic>>>(
                                future: getTopCV(),
                                builder: (context, snapshot) {
                                  if (snapshot.connectionState ==
                                      ConnectionState.waiting) {
                                    return const Center(
                                      child: CircularProgressIndicator(),
                                    );
                                  } else if (snapshot.hasError) {
                                    return Center(
                                      child: Text("Lỗi: ${snapshot.error}"),
                                    );
                                  } else if (!snapshot.hasData ||
                                      snapshot.data!.isEmpty) {
                                    return const Center(
                                      child: Text("Không có dữ liệu"),
                                    );
                                  }

                                  final dsCv = snapshot.data!;
                                  return ListView.builder(
                                    itemCount: dsCv.length,
                                    itemBuilder: (context, i) {
                                      final cv = dsCv[i];
                                      return GestureDetector(
                                        onTap: () {
                                          Navigator.push(
                                            context,
                                            MaterialPageRoute(
                                              builder: (_) =>
                                                  XemChiTietView(id: cv['id']),
                                            ),
                                          );
                                        },
                                        child: Container(
                                          margin: const EdgeInsets.symmetric(
                                            vertical: 6,
                                          ),
                                          padding: const EdgeInsets.all(10),
                                          decoration: BoxDecoration(
                                            color: Colors.grey[50],
                                            borderRadius: BorderRadius.circular(
                                              12,
                                            ),
                                            border: Border.all(
                                              color: Colors.grey[300]!,
                                            ),
                                          ),
                                          child: Row(
                                            crossAxisAlignment:
                                                CrossAxisAlignment.start,
                                            children: [
                                              ClipRRect(
                                                borderRadius:
                                                    BorderRadius.circular(8),
                                                child: Image.network(
                                                  cv['avt'] ?? '',
                                                  width: 55,
                                                  height: 55,
                                                  fit: BoxFit.cover,
                                                  errorBuilder: (_, __, ___) =>
                                                      Container(
                                                        width: 55,
                                                        height: 55,
                                                        color: Colors.grey[300],
                                                        child: const Icon(
                                                          Icons.person,
                                                          color: Colors.grey,
                                                        ),
                                                      ),
                                                ),
                                              ),
                                              const SizedBox(width: 10),
                                              Expanded(
                                                child: Column(
                                                  crossAxisAlignment:
                                                      CrossAxisAlignment.start,
                                                  children: [
                                                    Text(
                                                      cv['vitri'] ??
                                                          'Vị trí chưa có',
                                                      style: const TextStyle(
                                                        fontSize: 14,
                                                        fontWeight:
                                                            FontWeight.bold,
                                                      ),
                                                      overflow:
                                                          TextOverflow.ellipsis,
                                                    ),
                                                    const SizedBox(height: 4),
                                                    Text(
                                                      cv['hoten'] ?? '',
                                                      style: const TextStyle(
                                                        fontSize: 13,
                                                        color: Colors.black87,
                                                      ),
                                                    ),
                                                    Text(
                                                      cv['nganh'] ?? '',
                                                      style: const TextStyle(
                                                        fontSize: 12,
                                                        color: Colors.black54,
                                                      ),
                                                    ),
                                                    const SizedBox(height: 6),
                                                    Wrap(
                                                      spacing: 8,
                                                      runSpacing: 6,
                                                      children: [
                                                        Container(
                                                          padding: EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                                                          constraints: BoxConstraints(maxWidth: 180),
                                                          decoration: BoxDecoration(
                                                            color: Colors.white,
                                                            borderRadius: BorderRadius.circular(12),
                                                            boxShadow: [
                                                              BoxShadow(
                                                                color: Colors.grey.withOpacity(0.3),
                                                                spreadRadius: 1,
                                                                blurRadius: 6,
                                                                offset: Offset(0, 3),
                                                              ),
                                                            ],
                                                            border: Border.all(color: Colors.grey.shade300),
                                                          ),
                                                          child: Row(
                                                            mainAxisSize: MainAxisSize.min,
                                                            children: [
                                                              Icon(Icons.mail, size: 18, color: Colors.blueAccent),
                                                              SizedBox(width: 6),
                                                              Flexible(
                                                                child: Text(
                                                                  cv['email'],
                                                                  overflow: TextOverflow.ellipsis,
                                                                  maxLines: 1,
                                                                  style: TextStyle(
                                                                    fontSize: 14,
                                                                    color: Colors.grey.shade800,
                                                                    fontWeight: FontWeight.w500,
                                                                  ),
                                                                ),
                                                              ),
                                                            ],
                                                          ),
                                                        ),
                                                        Container(
                                                          padding: EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                                                          constraints: BoxConstraints(maxWidth: 180),
                                                          decoration: BoxDecoration(
                                                            color: Colors.white,
                                                            borderRadius: BorderRadius.circular(12),
                                                            boxShadow: [
                                                              BoxShadow(
                                                                color: Colors.grey.withOpacity(0.3),
                                                                spreadRadius: 1,
                                                                blurRadius: 6,
                                                                offset: Offset(0, 3),
                                                              ),
                                                            ],
                                                            border: Border.all(color: Colors.grey.shade300),
                                                          ),
                                                          child: Row(
                                                            mainAxisSize: MainAxisSize.min,
                                                            children: [
                                                              Icon(Icons.phone, size: 18, color: Colors.green),
                                                              SizedBox(width: 6),
                                                              Flexible(
                                                                child: Text(
                                                                  cv['sdt'],
                                                                  overflow: TextOverflow.ellipsis,
                                                                  maxLines: 1,
                                                                  style: TextStyle(
                                                                    fontSize: 14,
                                                                    color: Colors.grey.shade800,
                                                                    fontWeight: FontWeight.w500,
                                                                  ),
                                                                ),
                                                              ),
                                                            ],
                                                          ),
                                                        ),
                                                        Container(
                                                          padding: EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                                                          constraints: BoxConstraints(maxWidth: 180),
                                                          decoration: BoxDecoration(
                                                            color: Colors.white,
                                                            borderRadius: BorderRadius.circular(12),
                                                            boxShadow: [
                                                              BoxShadow(
                                                                color: Colors.grey.withOpacity(0.3),
                                                                spreadRadius: 1,
                                                                blurRadius: 6,
                                                                offset: Offset(0, 3),
                                                              ),
                                                            ],
                                                            border: Border.all(color: Colors.grey.shade300),
                                                          ),
                                                          child: Row(
                                                            mainAxisSize: MainAxisSize.min,
                                                            children: [
                                                              Icon(Icons.location_on, size: 18, color: Colors.redAccent),
                                                              SizedBox(width: 6),
                                                              Flexible(
                                                                child: Text(
                                                                  cv['diachi'],
                                                                  overflow: TextOverflow.ellipsis,
                                                                  maxLines: 1,
                                                                  style: TextStyle(
                                                                    fontSize: 14,
                                                                    color: Colors.grey.shade800,
                                                                    fontWeight: FontWeight.w500,
                                                                  ),
                                                                ),
                                                              ),
                                                            ],
                                                          ),
                                                        ),
                                                        Container(
                                                          padding: EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                                                          constraints: BoxConstraints(maxWidth: 180),
                                                          decoration: BoxDecoration(
                                                            color: Colors.white,
                                                            borderRadius: BorderRadius.circular(12),
                                                            boxShadow: [
                                                              BoxShadow(
                                                                color: Colors.grey.withOpacity(0.3),
                                                                spreadRadius: 1,
                                                                blurRadius: 6,
                                                                offset: Offset(0, 3),
                                                              ),
                                                            ],
                                                            border: Border.all(color: Colors.grey.shade300),
                                                          ),
                                                          child: Row(
                                                            mainAxisSize: MainAxisSize.min,
                                                            children: [
                                                              Icon(Icons.work, size: 18, color: Colors.orange),
                                                              SizedBox(width: 6),
                                                              Flexible(
                                                                child: Text(
                                                                  cv['kinhnghiem'],
                                                                  overflow: TextOverflow.ellipsis,
                                                                  maxLines: 1,
                                                                  style: TextStyle(
                                                                    fontSize: 14,
                                                                    color: Colors.grey.shade800,
                                                                    fontWeight: FontWeight.w500,
                                                                  ),
                                                                ),
                                                              ),
                                                            ],
                                                          ),
                                                        ),
                                                      ],
                                                    )

                                                  ],
                                                ),
                                              ),
                                            ],
                                          ),
                                        ),
                                      );
                                    },
                                  );
                                },
                              ),
                            ),
                          ],
                        ),
                      ),

                      //Tien ich

                      Container(
                        width: double.infinity,
                        padding: const EdgeInsets.all(16),
                        margin: const EdgeInsets.symmetric(
                          vertical: 16,
                          horizontal: 20,
                        ),
                        decoration: BoxDecoration(
                          color: Colors.white,
                          borderRadius: BorderRadius.circular(16),
                          boxShadow: [
                            BoxShadow(
                              color: Colors.black.withOpacity(0.05),
                              blurRadius: 8,
                              offset: const Offset(0, 4),
                            ),
                          ],
                        ),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            const Text(
                              "Tiện ích",
                              style: TextStyle(
                                fontSize: 16,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                            const SizedBox(height: 12),
                            SizedBox(
                              height: 95,
                              child: ListView(
                                scrollDirection: Axis.horizontal,
                                children: [
                                  _buildTienIchItem(
                                    context,
                                    iconPath: "assets/job_tien_ich.png",
                                    title: "Quản lý Job",
                                    page: const QuanLyJob(),
                                  ),
                                  _buildTienIchItem(
                                    context,
                                    iconPath: "assets/tien_ich1.png",
                                    title: "Tìm kiếm nhân sự",
                                    page: const EmployeeSearchUI(),
                                  ),
                                  _buildTienIchItem(
                                    context,
                                    iconPath: "assets/tien_ich2.png",
                                    title: "Lịch phỏng vấn",
                                    page: const LichPV(),
                                  ),
                                  _buildTienIchItem(
                                    context,
                                    iconPath: "assets/loc_cv_tien_ich.png",
                                    title: "Quản lý nhân sự",
                                    page: const LocCV(),
                                  ),
                                  _buildTienIchItem(
                                    context,
                                    iconPath: "assets/internship_tien_ich.png",
                                    title: "Chương trình thực tập",
                                    page: const ChuongTrinhThucTapPage(),
                                  ),
                                  _buildTienIchItem(
                                    context,
                                    iconPath: "assets/school_tien_ich.png",
                                    title: "Liên kết với nhà trường",
                                    page: const lienKet(),
                                  ),
                                  _buildTienIchItem(
                                    context,
                                    iconPath: "assets/thong_ke_tien_ich.png",
                                    title: "Thống kê & báo cáo",
                                    page: const EmployeeReportUI(),
                                  ),
                                ],
                              ),
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}


Widget _buildTienIchItem(
  BuildContext context, {
  required String iconPath,
  required String title,
  required Widget page,
}) {
  return GestureDetector(
    onTap: () {
      Navigator.push(context, MaterialPageRoute(builder: (context) => page));
    },
    child: Container(
      width: 80,
      margin: const EdgeInsets.only(right: 14),
      decoration: BoxDecoration(
        color: const Color(0xFFdbf0fc),
        borderRadius: BorderRadius.circular(12),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.08),
            blurRadius: 5,
            offset: const Offset(0, 3),
          ),
        ],
      ),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Image.asset(iconPath, width: 36, height: 36),
          const SizedBox(height: 6),
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 4),
            child: Text(
              title,
              textAlign: TextAlign.center,
              style: const TextStyle(
                fontSize: 9,
                fontWeight: FontWeight.w600,
                height: 1.2,
              ),
            ),
          ),
        ],
      ),
    ),
  );
}
