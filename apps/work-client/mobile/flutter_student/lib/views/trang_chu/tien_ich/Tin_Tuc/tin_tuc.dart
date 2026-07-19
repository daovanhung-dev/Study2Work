import 'package:flutter/material.dart';

class TinTucView extends StatelessWidget {
  const TinTucView({super.key});

  // Danh sách demo tin tức
  final List<Map<String, String>> _newsItems = const [
    {
      'title': 'Học bổng mùa thu 2025',
      'summary': 'Thông tin về các học bổng dành cho sinh viên ưu tú.',
      'image': 'assets/news1.png',
      'date': '10/11/2025',
    },
    {
      'title': 'Workshop kỹ năng phỏng vấn',
      'summary': 'Tham gia workshop để nâng cao kỹ năng phỏng vấn và CV.',
      'image': 'assets/news2.png',
      'date': '08/11/2025',
    },
    {
      'title': 'Cập nhật việc làm IT mới nhất',
      'summary': 'Danh sách các vị trí tuyển dụng IT hot nhất hiện nay.',
      'image': 'assets/news3.png',
      'date': '05/11/2025',
    },
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Tin tức & Thông báo'),
        backgroundColor: Colors.blue.shade400,
        elevation: 0,
      ),
      body: ListView.separated(
        padding: const EdgeInsets.all(12),
        itemCount: _newsItems.length,
        separatorBuilder: (_, __) => const SizedBox(height: 12),
        itemBuilder: (context, index) {
          final item = _newsItems[index];
          return _buildNewsCard(context, item);
        },
      ),
    );
  }

  Widget _buildNewsCard(BuildContext context, Map<String, String> item) {
    return Material(
      color: Colors.white,
      borderRadius: BorderRadius.circular(14),
      elevation: 3,
      child: InkWell(
        borderRadius: BorderRadius.circular(14),
        onTap: () {
          // TODO: Chuyển sang trang chi tiết tin tức
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('Mở tin: ${item['title']}')),
          );
        },
        child: Container(
          padding: const EdgeInsets.all(12),
          child: Row(
            children: [
              ClipRRect(
                borderRadius: BorderRadius.circular(10),
                child: Image.asset(
                  item['image']!,
                  width: 90,
                  height: 90,
                  fit: BoxFit.cover,
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      item['title']!,
                      style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                      maxLines: 2,
                      overflow: TextOverflow.ellipsis,
                    ),
                    const SizedBox(height: 6),
                    Text(
                      item['summary']!,
                      style: const TextStyle(fontSize: 13, color: Colors.black54),
                      maxLines: 3,
                      overflow: TextOverflow.ellipsis,
                    ),
                    const SizedBox(height: 6),
                    Text(
                      item['date']!,
                      style: const TextStyle(fontSize: 11, color: Colors.grey),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
