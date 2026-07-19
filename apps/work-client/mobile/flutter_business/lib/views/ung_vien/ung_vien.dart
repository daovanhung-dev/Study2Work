import 'package:flutter/material.dart';
import '../trang_chu/main/xem_chi_tiet.dart';
import '../trang_chu/main/thong_bao.dart';
import 'package:learn2earn/helper_db/helper_supabase.dart';
import 'package:learn2earn/controllers/ung_vien/ung_vien_controller.dart';
import 'package:learn2earn/models/ung_vien.dart';
import 'package:learn2earn/models/CV.dart';
import 'package:learn2earn/views/trang_chu/main/xem_chi_tiet_view.dart';

final UngTuyenCtrl ctrl = UngTuyenCtrl();
DNSupabase DN = DNSupabase.instance;
List<String> trangThaiTemp = [];

class UngVien extends StatefulWidget {
  const UngVien({super.key});

  @override
  State<UngVien> createState() => _UngVienState();
}

class _UngVienState extends State<UngVien> {
  @override
  void initState() {
    super.initState();
    load();
  }

  void load() async {
    final response = await ctrl.getTrangThai();
    setState(() {
      trangThaiTemp = response;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF4F6F9),
      appBar: AppBar(
        elevation: 0,
        backgroundColor: const Color(0xFF7ecbff),
        surfaceTintColor: Colors.transparent,
        title: const Text(
          "Danh sách Ứng viên",
          style: TextStyle(
            fontSize: 19,
            fontWeight: FontWeight.bold,
            color: Color(0xFF1C2834),
          ),
        ),
        centerTitle: true,
        leading: Padding(
          padding: const EdgeInsets.all(6),
          child: CircleAvatar(
            backgroundImage: const AssetImage("assets/logo.jpg"),
            backgroundColor: Colors.grey.shade200,
          ),
        ),
        actions: [
          IconButton(
            icon: const Icon(
              Icons.notifications_none_rounded,
              color: Colors.white,
            ),
            onPressed: () => Navigator.push(
              context,
              MaterialPageRoute(builder: (_) => const thongBao()),
            ),
          ),
        ],
      ),
      body: FutureBuilder<List<CV>>(
        future: ctrl.getCV(),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          } else if (snapshot.hasError) {
            return Center(child: Text('Lỗi: ${snapshot.error}'));
          } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
            return const Center(
              child: Text(
                'Chưa có ứng viên nào.',
                style: TextStyle(fontSize: 16, color: Colors.black54),
              ),
            );
          }

          final ungvien = snapshot.data!;

          // Đảm bảo trangThaiTemp có đủ phần tử
          if (trangThaiTemp.length < ungvien.length) {
            trangThaiTemp = List.generate(
              ungvien.length,
              (index) => index < trangThaiTemp.length
                  ? trangThaiTemp[index]
                  : 'Không hiển thị',
            );
          }

          return ListView.builder(
            padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
            itemCount: ungvien.length,
            itemBuilder: (context, i) {
              final uv = ungvien[i];
              String trangThai = trangThaiTemp[i];
              return AnimatedContainer(
                duration: const Duration(milliseconds: 300),
                margin: const EdgeInsets.only(bottom: 14),
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(18),
                  boxShadow: [
                    BoxShadow(
                      color: Colors.black.withOpacity(0.05),
                      blurRadius: 8,
                      offset: const Offset(0, 3),
                    ),
                  ],
                ),
                child: Padding(
                  padding: const EdgeInsets.all(16),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        children: [
                          Hero(
                            tag: "uv_${uv.id ?? i}",
                            child: CircleAvatar(
                              radius: 30,
                              backgroundImage: AssetImage(
                                uv.avt ?? 'assets/default.jpg',
                              ),
                            ),
                          ),
                          const SizedBox(width: 14),
                          Expanded(
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text(
                                  uv.hoten ?? 'Chưa có họ tên',
                                  style: const TextStyle(
                                    fontSize: 16.5,
                                    fontWeight: FontWeight.w700,
                                    color: Color(0xFF1B2734),
                                  ),
                                ),
                                const SizedBox(height: 3),
                                Text(
                                  uv.vitri ?? 'Chưa có vị trí',
                                  style: const TextStyle(
                                    fontSize: 14,
                                    color: Color(0xFF3A8DFF),
                                    fontWeight: FontWeight.w500,
                                  ),
                                ),
                              ],
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 10),
                      buildInfo(Icons.school_outlined, uv.nganh ?? ''),
                      buildInfo(Icons.engineering_outlined, uv.kynang ?? ''),
                      buildInfo(
                        Icons.cast_for_education_outlined,
                        uv.hocvan ?? '',
                      ),
                      buildInfo(
                        Icons.payments_outlined,
                        uv.luongmongmuon ?? '',
                      ),
                      buildInfo(
                        _getTrangThaiIcon(trangThai),
                        'Trạng thái: $trangThai',
                      ),
                      const SizedBox(height: 16),
                      const Divider(height: 1, color: Color(0xFFE9EEF3)),
                      const SizedBox(height: 12),
                      Row(
                        children: [
                          // 🔹 Nếu trạng thái chưa ứng tuyển thì hiển thị nút Tuyển + Loại
                          if (trangThai.toLowerCase() != 'đã ứng tuyển' &&
                              trangThai.toLowerCase() != 'từ chối ứng tuyển') ...[
                            Expanded(
                              child: buildChipButton(
                                icon: Icons.check_circle_outline_rounded,
                                label: "Tuyển",
                                color: const Color(0xFF3A8DFF),
                                onTap: () async {
                                  await ctrl.ungTuyen(uv.id!);
                                  ScaffoldMessenger.of(context).showSnackBar(
                                    const SnackBar(
                                      content: Text('Đã Tuyển Dụng Thành Công!'),
                                      backgroundColor: Colors.blue,
                                    ),
                                  );
                                  final response = await ctrl.getTrangThai();
                                  setState(() {
                                    trangThaiTemp[i] = response[i];
                                  });
                                },
                              ),
                            ),
                            const SizedBox(width: 8),
                            Expanded(
                              child: buildChipButton(
                                icon: Icons.close_rounded,
                                label: "Loại",
                                color: Colors.redAccent.shade200,
                                onTap: () async {
                                  final confirm = await showDialog<bool>(
                                    context: context,
                                    builder: (context) => AlertDialog(
                                      title: const Text('Xác nhận'),
                                      content: const Text('Bạn có chắc muốn loại ứng viên này không?'),
                                      actions: [
                                        TextButton(
                                          onPressed: () => Navigator.pop(context, false),
                                          child: const Text('Hủy'),
                                        ),
                                        TextButton(
                                          onPressed: () => Navigator.pop(context, true),
                                          child: const Text('Đồng ý'),
                                        ),
                                      ],
                                    ),
                                  );

                                  if (confirm != true) return;

                                  // Xử lý xóa
                                  await ctrl.delCV(uv.id!);

                                  ScaffoldMessenger.of(context).showSnackBar(
                                    const SnackBar(
                                      content: Text('Đã Loại Thành Công!'),
                                      backgroundColor: Colors.blue,
                                      behavior: SnackBarBehavior.floating,
                                    ),
                                  );

                                  // 🔁 Gọi lại hàm load() để reset lại danh sách và trạng thái
                                  setState(() {
                                    trangThaiTemp.clear(); // Xóa cache tạm
                                  });
                                  load(); // Load lại danh sách từ server
                                },
                              ),
                            ),
                            
                            const SizedBox(width: 8),
                          ],

                          // 🔹 Nút Chi tiết luôn hiển thị
                          Expanded(
                            child: ElevatedButton.icon(
                              onPressed: () {
                                Navigator.push(
                                  context,
                                  MaterialPageRoute(
                                    builder: (_) => XemChiTietView(id: uv.id!),
                                  ),
                                );
                              },
                              style: ElevatedButton.styleFrom(
                                backgroundColor: const Color(0xFF3A8DFF),
                                elevation: 0,
                                shape: RoundedRectangleBorder(
                                  borderRadius: BorderRadius.circular(10),
                                ),
                                padding: const EdgeInsets.symmetric(vertical: 10),
                              ),
                              icon: const Icon(
                                Icons.info_outline_rounded,
                                color: Colors.white,
                                size: 18,
                              ),
                              label: const Text(
                                "Chi tiết",
                                style: TextStyle(
                                  color: Colors.white,
                                  fontSize: 13.5,
                                  fontWeight: FontWeight.w600,
                                ),
                              ),
                            ),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
              );
            },
          );
        },
      ),
    );
  }

  Widget buildInfo(IconData icon, String text) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 4),
      child: Row(
        children: [
          Icon(icon, size: 17, color: const Color(0xFF3A8DFF)),
          const SizedBox(width: 8),
          Expanded(
            child: Text(
              text,
              style: const TextStyle(
                fontSize: 13.5,
                color: Color(0xFF2C3E50),
                overflow: TextOverflow.ellipsis,
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget buildChipButton({
    required IconData icon,
    required String label,
    required Color color,
    required VoidCallback onTap,
  }) {
    return InkWell(
      borderRadius: BorderRadius.circular(50),
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
        decoration: BoxDecoration(
          color: color.withOpacity(0.1),
          borderRadius: BorderRadius.circular(50),
          border: Border.all(color: color.withOpacity(0.4)),
        ),
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(icon, color: color, size: 18),
            const SizedBox(width: 5),
            Text(
              label,
              style: TextStyle(
                color: color,
                fontWeight: FontWeight.w600,
                fontSize: 13.5,
              ),
            ),
          ],
        ),
      ),
    );
  }
}

IconData _getTrangThaiIcon(String trangThai) {
  switch (trangThai.toLowerCase()) {
    case 'đã ứng tuyển':
      return Icons.check_circle_outline;
    case 'từ chối ứng tuyển':
      return Icons.cancel_outlined;
    default:
      return Icons.hourglass_bottom;
  }
}
