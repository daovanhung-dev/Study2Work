import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'package:work_server/theme/design_tokens.dart';
import 'package:work_server/controllers/trang_chu/xem_chi_tiet.dart';
import 'package:work_server/controllers/ung_tuyen_ctrl.dart';
import 'package:work_server/models/sinh_vien/jd.dart';

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
      backgroundColor: AppColors.background,
      appBar: AppBar(
        elevation: 0,
        backgroundColor: AppColors.primary,
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
                      color: AppColors.surface,
                      borderRadius: BorderRadius.circular(24),
                      boxShadow: [
                        BoxShadow(
                          color: AppColors.navy.withValues(alpha: 0.06),
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
                                  color: AppColors.border,
                                  child: const Icon(
                                    Icons.business,
                                    color: AppColors.muted,
                                  ),
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
                                      color: AppColors.primary,
                                    ),
                                  ),
                                  const SizedBox(height: 4),
                                  Text(
                                    jd.tenCongTy,
                                    style: const TextStyle(
                                      fontSize: 15,
                                      fontWeight: FontWeight.w500,
                                    ),
                                  ),
                                  const SizedBox(height: 4),
                                  Text(
                                    jd.diaDiem,
                                    style: const TextStyle(
                                      fontSize: 13,
                                      color: AppColors.muted,
                                    ),
                                  ),
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
                            _infoTag(Icons.school, jd.trinhDo, AppColors.warning),
                            _infoTag(Icons.star, jd.capBac, AppColors.info),
                            _infoTag(Icons.timer, jd.thoiGian, AppColors.success),
                            _infoTag(
                              Icons.monetization_on,
                              jd.mucLuong,
                              AppColors.action,
                            ),
                            _infoTag(
                              Icons.calendar_today,
                              _formatDate(jd.hanNop),
                              AppColors.danger,
                            ),
                          ],
                        ),

                        const SizedBox(height: 20),
                        const Divider(),

                        // ===================== FULL DETAILS =====================
                        _sectionTitle("THÔNG TIN CHI TIẾT"),
                        _buildRich("ID công việc", jd.id.toString()),
                        _buildRich(
                          "ID doanh nghiệp",
                          jd.doanhNghiepID?.toString() ?? "Chưa có",
                        ),
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
                              final kt = await ungTuyenCtrl.ungTuyen(jd.id);
                              if (!context.mounted) return;
                              if (kt) {
                                _showSnack(
                                  context,
                                  'Ứng tuyển thành công!',
                                  AppColors.action,
                                );
                              } else {
                                _showSnack(
                                  context,
                                  'Bạn đã ứng tuyển vị trí này rồi!',
                                  AppColors.danger,
                                );
                              }
                            },
                            style: ElevatedButton.styleFrom(
                              backgroundColor: AppColors.primary,
                              padding: const EdgeInsets.symmetric(
                                horizontal: 30,
                                vertical: 12,
                              ),
                              shape: RoundedRectangleBorder(
                                borderRadius: BorderRadius.circular(30),
                              ),
                              shadowColor: AppColors.action.withValues(
                                alpha: 0.35,
                              ),
                              elevation: 6,
                            ),
                            icon: const Icon(Icons.send, color: AppColors.surface),
                            label: const Text(
                              "Ứng tuyển ngay",
                              style: TextStyle(
                                color: AppColors.surface,
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
        content: Text(msg, style: const TextStyle(color: AppColors.surface)),
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
          color: AppColors.primary,
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
                fontWeight: FontWeight.bold,
                color: AppColors.navy,
              ),
            ),
            TextSpan(text: text),
          ],
        ),
        style: const TextStyle(fontSize: 14, color: AppColors.navy),
      ),
    );
  }

  Widget _infoTag(IconData icon, String text, Color color) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
      decoration: BoxDecoration(
        color: color.withValues(alpha: 0.12),
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: color.withValues(alpha: 0.25)),
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
                color: AppColors.navy,
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
