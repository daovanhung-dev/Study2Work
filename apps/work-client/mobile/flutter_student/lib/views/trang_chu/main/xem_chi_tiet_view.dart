import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'package:learn2earn/controllers/trang_chu/xem_chi_tiet.dart';
import 'package:learn2earn/controllers/UngTuyenCtrl.dart';
import 'package:learn2earn/models/sinh_vien/JD.dart';

final xemChiTietCtrl = XemChiTietController();
final ungTuyenCtrl = UngTuyenCtrl();

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
      backgroundColor: const Color(0xFFF4F7FB),
      appBar: AppBar(
        elevation: 0,
        backgroundColor: const Color(0xFF0052CC),
        title: const Text(
          "Chi tiết công việc",
          style: TextStyle(fontWeight: FontWeight.bold),
        ),
        centerTitle: true,
      ),
      body: SafeArea(
        child: FutureBuilder<JD>(
          future: xemChiTietCtrl.xemChiTiet(widget.id),
          builder: (context, snapshot) {
            if (snapshot.connectionState == ConnectionState.waiting) {
              return const Center(child: CircularProgressIndicator());
            }
            if (snapshot.hasError) {
              return Center(child: Text("Lỗi: ${snapshot.error}"));
            }
            if (!snapshot.hasData) {
              return const Center(child: Text("Không tìm thấy dữ liệu"));
            }

            final jd = snapshot.data!;
            final maxWidth = MediaQuery.of(context).size.width < 460
                ? MediaQuery.of(context).size.width - 32
                : 420.0;

            return SingleChildScrollView(
              padding: const EdgeInsets.all(16),
              child: Align(
                alignment: Alignment.topCenter,
                child: ConstrainedBox(
                  constraints: BoxConstraints(maxWidth: maxWidth),
                  child: Container(
                    padding: const EdgeInsets.all(20),
                    decoration: BoxDecoration(
                      color: Colors.white,
                      borderRadius: BorderRadius.circular(24),
                      boxShadow: [
                        BoxShadow(
                          color: Colors.black.withOpacity(0.06),
                          blurRadius: 10,
                          offset: const Offset(0, 5),
                        ),
                      ],
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        // ===================== HEADER =====================
                        Row(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            ClipRRect(
                              borderRadius: BorderRadius.circular(16),
                              child: Image.network(
                                jd.avt,
                                width: 80,
                                height: 80,
                                fit: BoxFit.cover,
                                errorBuilder: (_, __, ___) => Container(
                                  width: 80,
                                  height: 80,
                                  color: Colors.grey[300],
                                  child: const Icon(Icons.business,
                                      color: Colors.grey),
                                ),
                              ),
                            ),
                            const SizedBox(width: 12),
                            Expanded(
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Text(
                                    jd.tenViTri,
                                    style: const TextStyle(
                                      fontSize: 20,
                                      fontWeight: FontWeight.bold,
                                      color: Color(0xFF0052CC),
                                    ),
                                  ),
                                  const SizedBox(height: 4),
                                  Text(jd.tenCongTy,
                                      style: const TextStyle(
                                          fontSize: 15,
                                          fontWeight: FontWeight.w500)),
                                  const SizedBox(height: 4),
                                  Text(jd.diaDiem,
                                      style: const TextStyle(
                                          fontSize: 13,
                                          color: Colors.black54)),
                                ],
                              ),
                            ),
                          ],
                        ),

                        const SizedBox(height: 16),
                        const Divider(),

                        // ===================== TAG INFO =====================
                        Wrap(
                          spacing: 10,
                          runSpacing: 10,
                          children: [
                            _infoTag(Icons.school, jd.trinhDo, Colors.orange),
                            _infoTag(Icons.star, jd.capBac, Colors.purple),
                            _infoTag(Icons.timer, jd.thoiGian, Colors.green),
                            _infoTag(Icons.monetization_on, jd.mucLuong,
                                Colors.blue),
                            _infoTag(Icons.calendar_today,
                                _formatDate(jd.hanNop), Colors.red),
                          ],
                        ),

                        const SizedBox(height: 20),
                        const Divider(),

                        // ===================== FULL DETAILS =====================
                        _sectionTitle("THÔNG TIN CHI TIẾT"),
                        _buildRich("ID công việc", jd.id.toString()),
                        _buildRich("ID doanh nghiệp",
                            jd.doanhNghiepID?.toString() ?? "Chưa có"),
                        _buildRich("Tên công ty", jd.tenCongTy),
                        _buildRich("Ngành nghề", jd.nganh),
                        _buildRich("Tên vị trí", jd.tenViTri),
                        _buildRich("Cấp bậc", jd.capBac),
                        _buildRich("Báo cáo cho", jd.baoCaoCho),
                        _buildRich("Trình độ yêu cầu", jd.trinhDo),
                        _buildRich("Kinh nghiệm", jd.kinhNghiem),
                        _buildRich("Kỹ năng chuyên môn", jd.kyNang),
                        _buildRich("Kỹ năng mềm", jd.kyNangMem),
                        _buildRich("Ưu tiên", jd.uuTien),
                        _buildRich("Mức lương", jd.mucLuong),
                        _buildRich("Phúc lợi", jd.phucLoi),
                        _buildRich("Môi trường làm việc", jd.moiTruong),
                        _buildRich("Địa điểm", jd.diaDiem),
                        _buildRich("Thời gian làm việc", jd.thoiGian),
                        _buildRich("Hạn nộp hồ sơ", _formatDate(jd.hanNop)),
                        _buildRich("Cách ứng tuyển", jd.cachUngTuyen),
                        _buildRich("Mô tả công việc", jd.moTa),

                        const SizedBox(height: 26),

                        // ===================== APPLY BUTTON =====================
                        Center(
                          child: ElevatedButton.icon(
                            onPressed: () async {
                              bool kt = await ungTuyenCtrl.ungTuyen(jd.id);
                              if (kt) {
                                _showSnack(context, 'Ứng tuyển thành công!',
                                    Colors.blue);
                              } else {
                                _showSnack(context,
                                    'Bạn đã ứng tuyển vị trí này rồi!',
                                    Colors.redAccent);
                              }
                            },
                            style: ElevatedButton.styleFrom(
                              backgroundColor: const Color(0xFF0052CC),
                              padding: const EdgeInsets.symmetric(
                                  horizontal: 30, vertical: 12),
                              shape: RoundedRectangleBorder(
                                  borderRadius: BorderRadius.circular(30)),
                              shadowColor:
                              Colors.blueAccent.withOpacity(0.35),
                              elevation: 6,
                            ),
                            icon: const Icon(Icons.send, color: Colors.white),
                            label: const Text(
                              "Ứng tuyển ngay",
                              style: TextStyle(
                                color: Colors.white,
                                fontWeight: FontWeight.bold,
                                fontSize: 15,
                              ),
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              ),
            );
          },
        ),
      ),
    );
  }

  // ===================== WIDGET HELPER =====================

  void _showSnack(BuildContext context, String msg, Color color) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(
          msg,
          style: const TextStyle(color: Colors.white),
        ),
        backgroundColor: color,
        behavior: SnackBarBehavior.floating,
        margin: const EdgeInsets.all(16),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
        duration: const Duration(seconds: 2),
      ),
    );
  }

  String _formatDate(String dateStr) {
    if (dateStr.isEmpty) return "Chưa có";
    try {
      return DateFormat('dd/MM/yyyy').format(DateTime.parse(dateStr));
    } catch (_) {
      return dateStr;
    }
  }

  Widget _sectionTitle(String title) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8),
      child: Text(
        title,
        style: const TextStyle(
          fontSize: 17,
          fontWeight: FontWeight.bold,
          color: Color(0xFF0052CC),
        ),
      ),
    );
  }

  Widget _buildRich(String label, String? value) {
    final text = value?.isNotEmpty == true ? value! : "Chưa có";
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4),
      child: Text.rich(
        TextSpan(
          children: [
            TextSpan(
              text: "$label: ",
              style: const TextStyle(
                  fontWeight: FontWeight.bold, color: Colors.black),
            ),
            TextSpan(text: text),
          ],
        ),
        style: const TextStyle(fontSize: 14, color: Colors.black87),
      ),
    );
  }

  Widget _infoTag(IconData icon, String text, Color color) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
      decoration: BoxDecoration(
        color: color.withOpacity(0.12),
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: color.withOpacity(0.25)),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, size: 18, color: color),
          const SizedBox(width: 6),
          Flexible(
            child: Text(
              text.isNotEmpty ? text : "Chưa có",
              style: const TextStyle(
                fontSize: 13,
                fontWeight: FontWeight.w500,
                color: Colors.black87,
              ),
              maxLines: 1,
              overflow: TextOverflow.ellipsis,
            ),
          ),
        ],
      ),
    );
  }
}
