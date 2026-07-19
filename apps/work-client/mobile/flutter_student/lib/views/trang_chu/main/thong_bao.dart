import 'package:flutter/material.dart';
import 'package:intl/intl.dart';

class thongBao extends StatefulWidget {
  const thongBao({super.key});

  @override
  State<thongBao> createState() => _thongBaoState();
}

class _thongBaoState extends State<thongBao> with SingleTickerProviderStateMixin {
  final List<Map<String, dynamic>> ds_thongbao = [
    {
      "id_tb": "001",
      "tieu_de": "Lịch phỏng vấn",
      "noi_dung": "Bạn có lịch phỏng vấn vị trí Flutter Dev vào 9h sáng mai.",
      "thoi_gian": "2025-09-30 14:30",
      "trang_thai": false,
      "loai": "phongvan",
      "avt_tb": "assets/avt.jpg",
    },
    {
      "id_tb": "002",
      "tieu_de": "Cập nhật hồ sơ",
      "noi_dung": "Hồ sơ của bạn đã được duyệt thành công.",
      "thoi_gian": "2025-09-29 10:15",
      "trang_thai": true,
      "loai": "hoso",
      "avt_tb": "assets/avt.jpg",
    },
    {
      "id_tb": "003",
      "tieu_de": "Tin tuyển dụng mới",
      "noi_dung": "Công ty ABC vừa đăng tuyển vị trí Backend Developer.",
      "thoi_gian": "2025-09-28 09:00",
      "trang_thai": false,
      "loai": "tuyendung",
      "avt_tb": "assets/avt.jpg",
    },
    {
      "id_tb": "004",
      "tieu_de": "Nhắc nhở",
      "noi_dung": "Bạn chưa hoàn thành cập nhật kỹ năng trong hồ sơ.",
      "thoi_gian": "2025-09-27 20:45",
      "trang_thai": false,
      "loai": "nhacnho",
      "avt_tb": "assets/avt.jpg",
    },
    {
      "id_tb": "005",
      "tieu_de": "Thông báo hệ thống",
      "noi_dung": "Hệ thống sẽ bảo trì vào lúc 23h hôm nay.",
      "thoi_gian": "2025-09-26 18:00",
      "trang_thai": true,
      "loai": "hethong",
      "avt_tb": "assets/avt.jpg",
    },
  ];

  late AnimationController _controller;
  late Animation<double> _fadeAnimation;

  @override
  void initState() {
    super.initState();
    _controller =
        AnimationController(vsync: this, duration: const Duration(seconds: 1));
    _fadeAnimation = CurvedAnimation(parent: _controller, curve: Curves.easeIn);
    _controller.forward();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  Color _getColorByType(String loai) {
    switch (loai) {
      case "phongvan":
        return Colors.blueAccent;
      case "hoso":
        return Colors.green;
      case "tuyendung":
        return Colors.orange;
      case "nhacnho":
        return Colors.redAccent;
      case "hethong":
        return Colors.deepPurple;
      default:
        return Colors.grey;
    }
  }

  IconData _getIconByType(String loai) {
    switch (loai) {
      case "phongvan":
        return Icons.event_available;
      case "hoso":
        return Icons.check_circle;
      case "tuyendung":
        return Icons.work;
      case "nhacnho":
        return Icons.alarm;
      case "hethong":
        return Icons.system_update;
      default:
        return Icons.notifications;
    }
  }

  String _formatTime(String time) {
    final DateTime date = DateTime.parse(time);
    return DateFormat('dd/MM/yyyy • HH:mm').format(date);
  }

  void _xemChiTiet(Map<String, dynamic> thongBao) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        shape:
        RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
        title: Row(
          children: [
            Icon(_getIconByType(thongBao['loai']),
                color: _getColorByType(thongBao['loai'])),
            const SizedBox(width: 10),
            Expanded(
              child: Text(
                thongBao['tieu_de'],
                style:
                const TextStyle(fontWeight: FontWeight.bold, fontSize: 18),
              ),
            ),
          ],
        ),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(thongBao['noi_dung']),
            const SizedBox(height: 10),
            Text(
              "Thời gian: ${_formatTime(thongBao['thoi_gian'])}",
              style: const TextStyle(color: Colors.grey, fontSize: 12),
            ),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text("Đóng",
                style: TextStyle(color: Color(0xFF7ecbff))),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        elevation: 0,
        backgroundColor: const Color(0xFF7ecbff),
        title: const Text(
          "Thông báo",
          style: TextStyle(color: Colors.white),
        ),
        centerTitle: true,
      ),
      body: Stack(
        children: [
          Positioned.fill(
            child: Image.asset(
              "assets/bg_trangchu.jpg",
              fit: BoxFit.cover,
            ),
          ),
          FadeTransition(
            opacity: _fadeAnimation,
            child: ListView.builder(
              padding: const EdgeInsets.all(16),
              itemCount: ds_thongbao.length,
              itemBuilder: (context, index) {
                final tb = ds_thongbao[index];
                final color = _getColorByType(tb['loai']);
                final icon = _getIconByType(tb['loai']);
                final daDoc = tb['trang_thai'] == true;

                return AnimatedContainer(
                  duration: const Duration(milliseconds: 400),
                  curve: Curves.easeInOut,
                  margin: const EdgeInsets.symmetric(vertical: 8),
                  decoration: BoxDecoration(
                    color: daDoc ? Colors.white.withOpacity(0.9) : Colors.blue.shade50,
                    borderRadius: BorderRadius.circular(20),
                    boxShadow: [
                      BoxShadow(
                        color: color.withOpacity(0.3),
                        blurRadius: 10,
                        offset: const Offset(0, 4),
                      ),
                    ],
                    border: Border.all(color: color.withOpacity(0.4), width: 1),
                  ),
                  child: ListTile(
                    contentPadding: const EdgeInsets.all(12),
                    leading: CircleAvatar(
                      radius: 25,
                      backgroundColor: color.withOpacity(0.2),
                      child: Icon(icon, color: color),
                    ),
                    title: Text(
                      tb['tieu_de'],
                      style: TextStyle(
                        fontWeight: FontWeight.bold,
                        color: color,
                        fontSize: 16,
                      ),
                    ),
                    subtitle: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(tb['noi_dung'],
                            style: const TextStyle(fontSize: 13)),
                        const SizedBox(height: 6),
                        Text(
                          _formatTime(tb['thoi_gian']),
                          style:
                          const TextStyle(fontSize: 11, color: Colors.grey),
                        ),
                        const SizedBox(height: 6),
                        Container(
                          padding: const EdgeInsets.symmetric(
                              horizontal: 8, vertical: 4),
                          decoration: BoxDecoration(
                            color: daDoc
                                ? Colors.green.withOpacity(0.2)
                                : Colors.redAccent.withOpacity(0.2),
                            borderRadius: BorderRadius.circular(10),
                          ),
                          child: Text(
                            daDoc ? "Đã đọc" : "Chưa đọc",
                            style: TextStyle(
                              color: daDoc ? Colors.green : Colors.redAccent,
                              fontSize: 12,
                              fontWeight: FontWeight.w500,
                            ),
                          ),
                        ),
                      ],
                    ),
                    trailing: ElevatedButton.icon(
                      onPressed: () => _xemChiTiet(tb),
                      icon: const Icon(Icons.arrow_forward_ios_rounded, size: 14),
                      label: const Text("Chi tiết", style: TextStyle(fontSize: 12)),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: color.withOpacity(0.8),
                        foregroundColor: Colors.white,
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(12),
                        ),
                        padding: const EdgeInsets.symmetric(
                            horizontal: 10, vertical: 8),
                        elevation: 3,
                      ),
                    ),
                  ),
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}
