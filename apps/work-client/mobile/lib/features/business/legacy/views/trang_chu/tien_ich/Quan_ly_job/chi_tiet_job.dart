import 'package:flutter/material.dart';
import 'package:work_server/theme/design_tokens.dart';
import 'package:work_server/helper_db/helper_supabase.dart';
import 'package:work_server/models/jd.dart';

final DNSupabase dn = DNSupabase.instance;

class XemChiTietJD extends StatefulWidget {
  const XemChiTietJD({super.key, required this.id});
  final int id;

  @override
  State<XemChiTietJD> createState() => _XemChiTietJDState();
}

class _XemChiTietJDState extends State<XemChiTietJD> {
  late int idJd;

  @override
  void initState() {
    super.initState();
    idJd = widget.id;
  }

  @override
  Widget build(BuildContext context) {
    final screenWidth = MediaQuery.of(context).size.width;

    return Scaffold(
      appBar: AppBar(
        backgroundColor: AppColors.action,
        title: const Text("Chi tiết JD"),
      ),
      body: Stack(
        children: [
          // Background
          Container(
            decoration: const BoxDecoration(
              image: DecorationImage(
                image: AssetImage("assets/bg_trangchu.jpg"),
                fit: BoxFit.cover,
              ),
            ),
          ),
          // Nội dung
          Center(
            child: SingleChildScrollView(
              padding: const EdgeInsets.all(12),
              child: Container(
                width: screenWidth * 0.95,
                padding: const EdgeInsets.all(20),
                decoration: BoxDecoration(
                  color: AppColors.surface.withValues(alpha: 0.95),
                  borderRadius: BorderRadius.circular(16),
                  boxShadow: [
                    BoxShadow(
                      color: AppColors.navy.withValues(alpha: 0.15),
                      blurRadius: 10,
                      offset: const Offset(0, 5),
                    ),
                  ],
                ),
                child: FutureBuilder<JD>(
                  future: dn.getJD(idJd),
                  builder: (context, snapshot) {
                    if (snapshot.connectionState == ConnectionState.waiting) {
                      return const Center(child: CircularProgressIndicator());
                    } else if (snapshot.hasError) {
                      return Center(child: Text('Lỗi: ${snapshot.error}'));
                    } else if (!snapshot.hasData) {
                      return const Center(child: Text('Không có dữ liệu'));
                    }

                    final data = snapshot.data!;

                    // Hàm tạo hàng thông tin dạng thẻ có icon + màu pastel
                    Widget infoRow(
                      String title,
                      String content, {
                      IconData? icon,
                      Color? bgColor,
                    }) {
                      return Container(
                        padding: const EdgeInsets.symmetric(
                          horizontal: 12,
                          vertical: 8,
                        ),
                        margin: const EdgeInsets.symmetric(vertical: 4),
                        decoration: BoxDecoration(
                          color: bgColor ?? AppColors.background,
                          borderRadius: BorderRadius.circular(12),
                          boxShadow: [
                            BoxShadow(
                              color: AppColors.navy.withValues(alpha: 0.05),
                              blurRadius: 5,
                              offset: const Offset(0, 2),
                            ),
                          ],
                        ),
                        child: Row(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            if (icon != null)
                              Padding(
                                padding: const EdgeInsets.only(right: 6),
                                child: Icon(
                                  icon,
                                  size: 20,
                                  color: AppColors.muted,
                                ),
                              ),
                            SizedBox(
                              width: 100,
                              child: Text(
                                "$title:",
                                style: TextStyle(
                                  fontWeight: FontWeight.bold,
                                  color: AppColors.navy,
                                ),
                              ),
                            ),
                            Expanded(
                              child: Text(
                                content.isNotEmpty
                                    ? content
                                    : "Không có dữ liệu",
                                style: const TextStyle(
                                  fontSize: 15,
                                  color: AppColors.navy,
                                ),
                              ),
                            ),
                          ],
                        ),
                      );
                    }

                    // Gradient tiêu đề
                    Widget gradientTitle(String text) {
                      return Center(
                        child: ShaderMask(
                          shaderCallback: (bounds) =>
                              const LinearGradient(
                                colors: [AppColors.action, AppColors.info],
                              ).createShader(
                                Rect.fromLTWH(
                                  0,
                                  0,
                                  bounds.width,
                                  bounds.height,
                                ),
                              ),
                          child: Text(
                            text,
                            style: const TextStyle(
                              fontSize: 24,
                              fontWeight: FontWeight.bold,
                              color: AppColors.surface,
                            ),
                            textAlign: TextAlign.center,
                          ),
                        ),
                      );
                    }

                    // Nhóm tiêu đề phụ
                    Widget sectionTitle(String text) {
                      return Padding(
                        padding: const EdgeInsets.symmetric(vertical: 8),
                        child: Text(
                          text,
                          style: const TextStyle(
                            fontSize: 18,
                            fontWeight: FontWeight.bold,
                            color: AppColors.navy,
                          ),
                        ),
                      );
                    }

                    return Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        // Tiêu đề JD
                        gradientTitle(data.tenViTri),
                        const SizedBox(height: 16),

                        // Thông tin cơ bản
                        infoRow(
                          "Cấp bậc",
                          data.capBac,
                          icon: Icons.star,
                          bgColor: AppColors.primarySoft,
                        ),
                        infoRow(
                          "Báo cáo cho",
                          data.baoCaoCho,
                          icon: Icons.group,
                          bgColor: AppColors.success.withValues(alpha: 0.08),
                        ),
                        infoRow(
                          "Địa điểm",
                          data.diaDiem,
                          icon: Icons.location_on,
                          bgColor: AppColors.warning.withValues(alpha: 0.08),
                        ),
                        infoRow(
                          "Thời gian",
                          data.thoiGian,
                          icon: Icons.calendar_today,
                          bgColor: AppColors.primarySoft,
                        ),
                        infoRow(
                          "Hạn nộp",
                          data.hanNop,
                          icon: Icons.schedule,
                          bgColor: AppColors.primarySoft,
                        ),
                        const SizedBox(height: 12),
                        Divider(color: AppColors.border),

                        // Chi tiết công việc
                        sectionTitle("Chi tiết công việc"),
                        infoRow("Nhiệm vụ", data.nhiemVu, icon: Icons.task),
                        infoRow("Trình độ", data.trinhDo, icon: Icons.school),
                        infoRow(
                          "Kinh nghiệm",
                          data.kinhNghiem,
                          icon: Icons.work,
                        ),
                        infoRow("Kỹ năng", data.kyNang, icon: Icons.build),
                        infoRow(
                          "Kỹ năng mềm",
                          data.kyNangMem,
                          icon: Icons.handshake,
                        ),
                        infoRow("Ưu tiên", data.uuTien, icon: Icons.thumb_up),
                        infoRow(
                          "Mức lương",
                          data.mucLuong,
                          icon: Icons.monetization_on,
                        ),
                        infoRow(
                          "Phúc lợi",
                          data.phucLoi,
                          icon: Icons.health_and_safety,
                        ),
                        infoRow(
                          "Môi trường",
                          data.moiTruong,
                          icon: Icons.nature,
                        ),
                        infoRow(
                          "Cách ứng tuyển",
                          data.cachUngTuyen,
                          icon: Icons.send,
                        ),
                        const SizedBox(height: 12),
                        Divider(color: AppColors.border),

                        // Mô tả công việc
                        sectionTitle("Mô tả công việc"),
                        Text(
                          data.moTa.isNotEmpty ? data.moTa : "Không có mô tả",
                          style: const TextStyle(
                            fontSize: 15,
                            color: AppColors.navy,
                            height: 1.4,
                          ),
                        ),
                      ],
                    );
                  },
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
