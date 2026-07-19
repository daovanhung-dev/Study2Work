import 'package:flutter/material.dart';

class QuenMatKhau extends StatefulWidget {
  const QuenMatKhau({super.key});

  @override
  State<QuenMatKhau> createState() => _QuenMatKhauState();
}

class _QuenMatKhauState extends State<QuenMatKhau> {
  final TextEditingController _emailCtrl = TextEditingController();
  final TextEditingController _msvCtrl = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Stack(
        children: [
          // Nền hình
          Positioned.fill(
            child: Image.asset(
              "assets/bg_login.png",
              fit: BoxFit.cover,
            ),
          ),

          // Lớp phủ mờ gradient nhẹ
          Positioned.fill(
            child: Container(
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  colors: [
                    Colors.white.withOpacity(0.4),
                    Colors.white.withOpacity(0.8)
                  ],
                  begin: Alignment.topCenter,
                  end: Alignment.bottomCenter,
                ),
              ),
            ),
          ),

          // Nội dung chính
          SafeArea(
            child: Center(
              child: SingleChildScrollView(
                padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 40),
                child: Container(
                  padding:
                  const EdgeInsets.symmetric(horizontal: 20, vertical: 30),
                  decoration: BoxDecoration(
                    color: Colors.white.withOpacity(0.9),
                    borderRadius: BorderRadius.circular(20),
                    boxShadow: [
                      BoxShadow(
                        color: Colors.black.withOpacity(0.15),
                        blurRadius: 10,
                        offset: const Offset(0, 4),
                      ),
                    ],
                  ),
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      const Text(
                        "Quên mật khẩu",
                        style: TextStyle(
                          fontSize: 24,
                          fontWeight: FontWeight.bold,
                          color: Colors.blueAccent,
                        ),
                      ),
                      const SizedBox(height: 25),

                      // Email
                      TextField(
                        controller: _emailCtrl,
                        decoration: const InputDecoration(
                          labelText: "Email",
                          hintText: "Nhập email của bạn",
                          prefixIcon: Icon(Icons.email_outlined),
                          border: OutlineInputBorder(),
                        ),
                      ),
                      const SizedBox(height: 20),

                      // Mã sinh viên
                      TextField(
                        controller: _msvCtrl,
                        decoration: const InputDecoration(
                          labelText: "Mã Sinh Viên",
                          hintText: "Nhập mã sinh viên",
                          prefixIcon: Icon(Icons.badge_outlined),
                          border: OutlineInputBorder(),
                        ),
                      ),
                      const SizedBox(height: 30),

                      // Nút gửi
                      SizedBox(
                        width: double.infinity,
                        height: 48,
                        child: ElevatedButton.icon(
                          onPressed: () {
                            // TODO: thêm logic gửi mail reset
                            ScaffoldMessenger.of(context).showSnackBar(
                              const SnackBar(
                                content:
                                Text("Yêu cầu đặt lại mật khẩu đã được gửi!"),
                                duration: Duration(seconds: 2),
                              ),
                            );
                          },
                          icon: const Icon(Icons.send),
                          label: const Text(
                            "Gửi yêu cầu",
                            style: TextStyle(fontSize: 16),
                          ),
                          style: ElevatedButton.styleFrom(
                            backgroundColor: Colors.blueAccent,
                            foregroundColor: Colors.white,
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(12),
                            ),
                          ),
                        ),
                      ),

                      const SizedBox(height: 15),

                      // Nút quay lại
                      TextButton.icon(
                        onPressed: () => Navigator.pop(context),
                        icon: const Icon(Icons.arrow_back_ios_new_rounded,
                            size: 18),
                        label: const Text("Quay lại đăng nhập"),
                        style: TextButton.styleFrom(
                          foregroundColor: Colors.blueAccent,
                        ),
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
}
