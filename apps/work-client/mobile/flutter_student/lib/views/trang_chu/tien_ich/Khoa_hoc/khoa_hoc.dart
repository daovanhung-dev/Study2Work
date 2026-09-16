import 'package:flutter/material.dart';
import 'package:work_server/theme/design_tokens.dart';

class KhoaHocView extends StatefulWidget {
  const KhoaHocView({super.key});

  @override
  State<KhoaHocView> createState() => _KhoaHocViewState();
}

class _KhoaHocViewState extends State<KhoaHocView> {
  // Demo dữ liệu khóa học
  final List<Map<String, dynamic>> _courses = [
    {
      'title': 'Flutter Cơ Bản',
      'description': 'Học cách tạo ứng dụng di động với Flutter từ đầu.',
      'progress': 0.5, // 50% hoàn thành
      'image': 'assets/flutter_course.png',
    },
    {
      'title': 'Python cho Sinh Viên',
      'description': 'Ngôn ngữ lập trình Python cơ bản cho sinh viên IT.',
      'progress': 0.2,
      'image': 'assets/python_course.png',
    },
    {
      'title': 'Thiết Kế UI/UX',
      'description': 'Thiết kế giao diện đẹp và trải nghiệm người dùng tốt.',
      'progress': 0.8,
      'image': 'assets/uiux_course.png',
    },
    {
      'title': 'Cơ Sở Dữ Liệu SQL',
      'description': 'Quản lý và truy vấn dữ liệu với SQL.',
      'progress': 0.0,
      'image': 'assets/sql_course.png',
    },
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Khóa học'),
        backgroundColor: AppColors.action,
        elevation: 0,
      ),
      body: Padding(
        padding: const EdgeInsets.all(12.0),
        child: ListView.separated(
          itemCount: _courses.length,
          separatorBuilder: (_, __) => const SizedBox(height: 12),
          itemBuilder: (context, index) {
            final course = _courses[index];
            return _buildCourseCard(course);
          },
        ),
      ),
    );
  }

  Widget _buildCourseCard(Map<String, dynamic> course) {
    final double progress = course['progress'] ?? 0.0;

    return Material(
      elevation: 2,
      borderRadius: BorderRadius.circular(14),
      color: AppColors.surface,
      child: InkWell(
        borderRadius: BorderRadius.circular(14),
        onTap: () {
          // Future enhancement: Xem chi tiết khóa học
        },
        child: Container(
          padding: const EdgeInsets.all(12),
          child: Row(
            children: [
              ClipRRect(
                borderRadius: BorderRadius.circular(10),
                child: Image.asset(
                  course['image'],
                  width: 70,
                  height: 70,
                  fit: BoxFit.cover,
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      course['title'] ?? 'Khóa học chưa xác định',
                      style: const TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 6),
                    Text(
                      course['description'] ?? '',
                      style: const TextStyle(
                        fontSize: 13,
                        color: AppColors.muted,
                      ),
                      maxLines: 2,
                      overflow: TextOverflow.ellipsis,
                    ),
                    const SizedBox(height: 8),
                    // Progress bar
                    ClipRRect(
                      borderRadius: BorderRadius.circular(6),
                      child: LinearProgressIndicator(
                        value: progress,
                        minHeight: 6,
                        backgroundColor: AppColors.border,
                        valueColor: AlwaysStoppedAnimation<Color>(
                          AppColors.action,
                        ),
                      ),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      'Tiến độ: ${(progress * 100).toInt()}%',
                      style: const TextStyle(
                        fontSize: 12,
                        color: AppColors.muted,
                      ),
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
