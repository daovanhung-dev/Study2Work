import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'thong_bao.dart';
import 'package:learn2earn/controllers/trang_chu/xem_chi_tiet.dart';

class XemChiTietView extends StatefulWidget {
  final int id;
  const XemChiTietView({super.key, required this.id});

  @override
  State<XemChiTietView> createState() => _XemChiTietViewState();
}

class _XemChiTietViewState extends State<XemChiTietView> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: const Color(0xFF7ecbff),
        title: const Text("Xem chi tiết"),
        actions: [
          IconButton(
            onPressed: () {
              Navigator.push(context,
                  MaterialPageRoute(builder: (context) => const thongBao()));
            },
            icon: const Icon(Icons.notifications),
          ),
        ],
      ),
      body: FutureBuilder<Map<String, dynamic>>(
        future: xemChiTiet(widget.id),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }
          if (snapshot.hasError) {
            return Center(child: Text("Lỗi: ${snapshot.error}"));
          }
          if (!snapshot.hasData || snapshot.data!.isEmpty) {
            return const Center(child: Text("Không tìm thấy dữ liệu"));
          }

          final dsCv = snapshot.data!;

          return Stack(
            children: [
              // Background mờ
              Container(
                decoration: BoxDecoration(
                  image: DecorationImage(
                    image: const AssetImage("assets/bg_trangchu.jpg"),
                    fit: BoxFit.cover,
                    colorFilter: ColorFilter.mode(
                        Colors.black.withOpacity(0.2), BlendMode.darken),
                  ),
                ),
              ),
              Center(
                child: SingleChildScrollView(
                  padding: const EdgeInsets.all(16),
                  child: Container(
                    width: 340,
                    decoration: BoxDecoration(
                      borderRadius: BorderRadius.circular(20),
                      gradient: LinearGradient(
                        colors: [Colors.white.withOpacity(0.95), Colors.white],
                        begin: Alignment.topLeft,
                        end: Alignment.bottomRight,
                      ),
                      boxShadow: [
                        BoxShadow(
                          color: Colors.black.withOpacity(0.25),
                          spreadRadius: 3,
                          blurRadius: 10,
                          offset: const Offset(0, 5),
                        ),
                      ],
                    ),
                    padding: const EdgeInsets.all(20),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        // Vị trí nổi bật
                        Center(
                          child: Text(
                            dsCv['vitri'] ?? '',
                            style: const TextStyle(
                              fontSize: 18,
                              fontWeight: FontWeight.bold,
                              color: Colors.blueAccent,
                            ),
                          ),
                        ),
                        const SizedBox(height: 16),
                        // Avatar + thông tin chính
                        Row(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            ClipRRect(
                              borderRadius: BorderRadius.circular(12),
                              child: Image.network(
                                dsCv['avt'],
                                width: 60,
                                height: 60,
                                fit: BoxFit.cover,
                                errorBuilder: (context, error, stackTrace) =>
                                    Container(
                                      width: 60,
                                      height: 60,
                                      color: Colors.grey[300],
                                      child: const Icon(Icons.person,
                                          color: Colors.grey),
                                    ),
                              ),
                            ),
                            const SizedBox(width: 12),
                            Expanded(
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  _buildRich("Họ tên", dsCv['hoten']),
                                  _buildRich(
                                      "Ngày sinh",
                                      dsCv['ngaysinh'] != null &&
                                          dsCv['ngaysinh'] != ""
                                          ? DateFormat('dd/MM/yyyy').format(
                                          DateTime.parse(dsCv['ngaysinh']))
                                          : "Chưa có"),
                                  _buildRich("Giới tính", dsCv['gioitinh']),
                                ],
                              ),
                            ),
                          ],
                        ),
                        const SizedBox(height: 16),
                        // Wrap thẻ thông tin nổi bật, scroll ngang nếu cần
                        SingleChildScrollView(
                          scrollDirection: Axis.horizontal,
                          child: Row(
                            children: [
                              _infoTagFull(Icons.email, dsCv['email'], Colors.blue.shade100),
                              const SizedBox(width: 8),
                              _infoTagFull(Icons.phone, dsCv['sdt'], Colors.green.shade100),
                              const SizedBox(width: 8),
                              _infoTagFull(Icons.location_on, dsCv['diachi'], Colors.red.shade100),
                              const SizedBox(width: 8),
                              _infoTagFull(Icons.work, dsCv['kinhnghiem'], Colors.orange.shade100),
                            ],
                          ),
                        ),
                        const SizedBox(height: 16),
                        // Thông tin chi tiết khác
                        _buildRich("Chuyên ngành", dsCv['nganh']),
                        _buildRich(
                            "Mục tiêu nghề nghiệp", dsCv['muctieunghiep']),
                        _buildRich("Học vấn", dsCv['hocvan']),
                        _buildRich("Kinh nghiệm", dsCv['kinhnghiem']),
                        _buildRich("Kỹ năng", dsCv['kynang']),
                        _buildRich("Ngoại ngữ", dsCv['ngoaingu']),
                        _buildRich("Chứng chỉ", dsCv['chungchi']),
                        _buildRich("Dự án", dsCv['duan']),
                        _buildRich("Giải thưởng", dsCv['giaithuong']),
                        _buildRich("Hoạt động", dsCv['hoatdong']),
                      ],
                    ),
                  ),
                ),
              ),
            ],
          );
        },
      ),
    );
  }

  // Helper RichText gọn
  Widget _buildRich(String label, String? value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 2),
      child: RichText(
        text: TextSpan(
          children: [
            TextSpan(
              text: "$label: ",
              style: const TextStyle(
                fontSize: 13,
                fontWeight: FontWeight.bold,
                color: Colors.black,
              ),
            ),
            TextSpan(
              text: value ?? "",
              style: const TextStyle(
                fontSize: 13,
                color: Colors.black87,
              ),
            ),
          ],
        ),
      ),
    );
  }

  // Widget thẻ thông tin nổi bật, không ellipsis
  Widget _infoTagFull(IconData icon, String? text, Color bgColor) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
      constraints: const BoxConstraints(minWidth: 100, maxWidth: 220),
      decoration: BoxDecoration(
        color: bgColor,
        borderRadius: BorderRadius.circular(14),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.15),
            blurRadius: 6,
            offset: const Offset(0, 3),
          ),
        ],
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, size: 20, color: Colors.black87),
          const SizedBox(width: 8),
          Flexible(
            child: Text(
              text ?? "",
              style: const TextStyle(
                fontSize: 14,
                fontWeight: FontWeight.w500,
                color: Colors.black87,
              ),
            ),
          ),
        ],
      ),
    );
  }
}
