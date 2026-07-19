import 'package:flutter/material.dart';

class QuenMatKhauView extends StatefulWidget {
  const QuenMatKhauView({super.key});

  @override
  State<QuenMatKhauView> createState() => _QuenMatKhauViewState();
}

class _QuenMatKhauViewState extends State<QuenMatKhauView> {
  final TextEditingController _emailController = TextEditingController();
  bool _isSent = false;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFE6F3FF),
      body: SafeArea(
        child: Center(
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 24.0, vertical: 40),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const Icon(Icons.lock_reset_rounded,
                    color: Color(0xFF2196F3), size: 90),
                const SizedBox(height: 20),
                const Text(
                  "Quên mật khẩu?",
                  style: TextStyle(
                      fontSize: 26,
                      fontWeight: FontWeight.bold,
                      color: Color(0xFF1565C0)),
                ),
                const SizedBox(height: 10),
                const Text(
                  "Nhập email để nhận liên kết khôi phục mật khẩu",
                  textAlign: TextAlign.center,
                  style: TextStyle(fontSize: 16, color: Colors.black54),
                ),
                const SizedBox(height: 30),
                Container(
                  decoration: BoxDecoration(
                    color: Colors.white,
                    borderRadius: BorderRadius.circular(16),
                    boxShadow: [
                      BoxShadow(
                        color: Colors.blue.withOpacity(0.1),
                        blurRadius: 10,
                        offset: const Offset(0, 5),
                      ),
                    ],
                  ),
                  child: TextField(
                    controller: _emailController,
                    decoration: const InputDecoration(
                      hintText: "Nhập email của bạn",
                      prefixIcon: Icon(Icons.email_outlined, color: Colors.blue),
                      border: InputBorder.none,
                      contentPadding:
                      EdgeInsets.symmetric(horizontal: 20, vertical: 16),
                    ),
                  ),
                ),
                const SizedBox(height: 30),
                ElevatedButton(
                  onPressed: () {
                    setState(() => _isSent = true);
                  },
                  style: ElevatedButton.styleFrom(
                    backgroundColor: const Color(0xFF64B5F6),
                    foregroundColor: Colors.white,
                    shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(12)),
                    minimumSize: const Size(double.infinity, 55),
                  ),
                  child: const Text(
                    "GỬI LIÊN KẾT KHÔI PHỤC",
                    style:
                    TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                  ),
                ),
                const SizedBox(height: 25),
                if (_isSent)
                  Container(
                    padding: const EdgeInsets.all(16),
                    decoration: BoxDecoration(
                      color: Colors.lightBlue.shade50,
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: const Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Icon(Icons.check_circle, color: Colors.green),
                        SizedBox(width: 8),
                        Flexible(
                          child: Text(
                            "Liên kết khôi phục đã được gửi tới email của bạn!",
                            style: TextStyle(
                                fontSize: 15, color: Colors.black87),
                            textAlign: TextAlign.center,
                          ),
                        ),
                      ],
                    ),
                  ),
                const Spacer(),
                TextButton(
                  onPressed: () {
                    Navigator.pop(context);
                  },
                  child: const Text(
                    "← Quay lại đăng nhập",
                    style: TextStyle(
                      color: Color(0xFF1565C0),
                      fontSize: 15,
                      fontWeight: FontWeight.w500,
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
