import 'package:flutter/material.dart';
import 'package:work_server/theme/design_tokens.dart';
import '../trang_chu/main/thong_bao.dart';
import 'package:work_server/controllers/cai_dat/cai_dat.dart';
import 'package:work_server/views/dang_nhap/dang_nhap.dart';

class Setting extends StatefulWidget {
  const Setting({super.key});

  @override
  State<Setting> createState() => _SettingState();
}

class _SettingState extends State<Setting> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      extendBodyBehindAppBar: true,
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0,
        leading: Padding(
          padding: const EdgeInsets.all(8.0),
          child: CircleAvatar(
            backgroundColor: AppColors.surface,
            backgroundImage: const AssetImage("assets/logo.jpg"),
          ),
        ),
        title: const Text(
          "Cài đặt",
          style: TextStyle(
            fontWeight: FontWeight.bold,
            color: AppColors.surface,
            fontSize: 22,
            shadows: [
              Shadow(
                offset: Offset(0, 1),
                blurRadius: 2,
                color: AppColors.muted,
              ),
            ],
          ),
        ),
        actions: [
          IconButton(
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => const ThongBao()),
              );
            },
            icon: const Icon(Icons.notifications, color: AppColors.surface),
          ),
        ],
      ),
      body: Stack(
        children: [
          // Nền mơ màng
          Positioned.fill(
            child: Image.asset("assets/bg_trangchu.jpg", fit: BoxFit.cover),
          ),
          Container(color: AppColors.navy.withValues(alpha: 0.2)), // overlay nền
          SafeArea(
            child: Center(
              child: SingleChildScrollView(
                child: Container(
                  width: 360,
                  padding: const EdgeInsets.all(20),
                  decoration: BoxDecoration(
                    color: AppColors.surface.withValues(alpha: 0.85),
                    borderRadius: BorderRadius.circular(25),
                    border: Border.all(
                      color: AppColors.surface.withValues(alpha: 0.3),
                    ),
                    boxShadow: [
                      BoxShadow(
                        color: AppColors.navy.withValues(alpha: 0.1),
                        blurRadius: 20,
                        offset: const Offset(0, 10),
                      ),
                    ],
                  ),
                  child: Column(
                    children: [
                      const Text(
                        "Tài khoản",
                        style: TextStyle(
                          fontSize: 24,
                          fontWeight: FontWeight.bold,
                          color: AppColors.navy,
                          shadows: [
                            Shadow(
                              offset: Offset(0, 1),
                              blurRadius: 2,
                              color: AppColors.border,
                            ),
                          ],
                        ),
                      ),
                      const SizedBox(height: 25),
                      _buildButton(Icons.person, "Thông tin cá nhân"),
                      _buildButton(Icons.lock, "Đổi mật khẩu"),
                      _buildButton(Icons.notifications, "Thông báo"),
                      _buildButton(Icons.palette, "Giao diện"),
                      _buildButton(Icons.language, "Ngôn ngữ"),
                      _buildButton(Icons.security, "Quyền riêng tư"),
                      _buildButton(Icons.help_outline, "Trợ giúp"),
                      _buildButton(Icons.info_outline, "Phiên bản"),
                      _buildButton(Icons.star, "Đánh giá"),
                      _buildButton(
                        Icons.logout,
                        "Đăng xuất",
                        color: AppColors.danger,
                        onTap: () async {
                          dangXuat();
                          ScaffoldMessenger.of(context).showSnackBar(
                            const SnackBar(
                              content: Text('Bạn đã đăng xuất thành công!'),
                              backgroundColor: AppColors.action,
                              duration: Duration(seconds: 2),
                            ),
                          );
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (context) => const DangNhap(),
                            ),
                          );
                        },
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildButton(
    IconData icon,
    String label, {
    Color? color,
    VoidCallback? onTap,
  }) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        margin: const EdgeInsets.symmetric(vertical: 10),
        padding: const EdgeInsets.symmetric(vertical: 14, horizontal: 18),
        decoration: BoxDecoration(
          color: color != null
              ? color.withValues(alpha: 0.12)
              : AppColors.action.withValues(alpha: 0.15),
          borderRadius: BorderRadius.circular(18),
          border: Border.all(
            color: color != null
                ? color.withValues(alpha: 0.3)
                : AppColors.action.withValues(alpha: 0.3),
          ),
          boxShadow: [
            BoxShadow(
              color: AppColors.navy.withValues(alpha: 0.03),
              blurRadius: 5,
              offset: const Offset(0, 3),
            ),
          ],
        ),
        child: Row(
          children: [
            Icon(icon, color: color ?? AppColors.action, size: 22),
            const SizedBox(width: 16),
            Text(
              label,
              style: const TextStyle(
                fontSize: 16,
                fontWeight: FontWeight.w600,
                color: AppColors.navy,
              ),
            ),
            const Spacer(),
            const Icon(
              Icons.arrow_forward_ios,
              size: 16,
              color: AppColors.muted,
            ),
          ],
        ),
      ),
    );
  }
}
