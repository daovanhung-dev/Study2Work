import 'package:flutter/material.dart';

class HoTroSinhVienView extends StatelessWidget {
  const HoTroSinhVienView({super.key});

  // Danh sách tiện ích hỗ trợ
  final List<Map<String, dynamic>> _supportItems = const [
    {'icon': Icons.question_answer_rounded, 'title': 'FAQ', 'description': 'Câu hỏi thường gặp'},
    {'icon': Icons.chat_bubble_outline, 'title': 'Chat Hỗ Trợ', 'description': 'Trao đổi trực tiếp với trợ lý'},
    {'icon': Icons.book_outlined, 'title': 'Tài Liệu Học Tập', 'description': 'Sách, bài giảng, slides'},
    {'icon': Icons.contact_phone_outlined, 'title': 'Liên Hệ', 'description': 'Thông tin liên hệ hỗ trợ'},
    {'icon': Icons.info_outline, 'title': 'Hướng Dẫn Sử Dụng', 'description': 'Cách sử dụng ứng dụng'},
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Hỗ trợ sinh viên'),
        backgroundColor: Colors.blue.shade400,
        elevation: 0,
      ),
      body: Padding(
        padding: const EdgeInsets.all(12.0),
        child: GridView.builder(
          itemCount: _supportItems.length,
          gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
            crossAxisCount: 2,
            childAspectRatio: 1.1,
            crossAxisSpacing: 12,
            mainAxisSpacing: 12,
          ),
          itemBuilder: (context, index) {
            final item = _supportItems[index];
            return _buildSupportCard(context, item);
          },
        ),
      ),
    );
  }

  Widget _buildSupportCard(BuildContext context, Map<String, dynamic> item) {
    return Material(
      color: Colors.white,
      borderRadius: BorderRadius.circular(14),
      elevation: 3,
      child: InkWell(
        borderRadius: BorderRadius.circular(14),
        onTap: () {
          // TODO: Xử lý chuyển sang chức năng chi tiết
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('Mở chức năng: ${item['title']}')),
          );
        },
        child: Container(
          padding: const EdgeInsets.all(14),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(item['icon'], size: 38, color: Colors.blue.shade400),
              const SizedBox(height: 12),
              Text(
                item['title'],
                style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 6),
              Text(
                item['description'],
                style: const TextStyle(fontSize: 13, color: Colors.black54),
                textAlign: TextAlign.center,
              ),
            ],
          ),
        ),
      ),
    );
  }
}
