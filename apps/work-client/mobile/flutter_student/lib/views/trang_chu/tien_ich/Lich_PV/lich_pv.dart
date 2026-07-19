import 'package:flutter/material.dart';
import 'package:intl/intl.dart';

class LichPhongVanView extends StatefulWidget {
  const LichPhongVanView({super.key});

  @override
  State<LichPhongVanView> createState() => _LichPhongVanViewState();
}

class _LichPhongVanViewState extends State<LichPhongVanView> {
  // Demo dữ liệu phỏng vấn
  final List<Map<String, dynamic>> _interviews = [
    {
      'company': 'MaiATech',
      'position': 'Flutter Developer Intern',
      'date': DateTime.now().add(const Duration(days: 1, hours: 10)),
      'status': 'Sắp tới',
    },
    {
      'company': 'VNPay',
      'position': 'Backend Developer',
      'date': DateTime.now().subtract(const Duration(days: 1)),
      'status': 'Đã hoàn thành',
    },
    {
      'company': 'FPT Software',
      'position': 'Frontend Developer',
      'date': DateTime.now().add(const Duration(days: 3, hours: 14)),
      'status': 'Sắp tới',
    },
    {
      'company': 'Techcombank',
      'position': 'QA Tester',
      'date': DateTime.now().subtract(const Duration(days: 2)),
      'status': 'Đã hủy',
    },
  ];

  String _selectedFilter = 'Tất cả';
  final List<String> _filters = ['Tất cả', 'Sắp tới', 'Đã hoàn thành', 'Đã hủy'];

  @override
  Widget build(BuildContext context) {
    final filtered = _selectedFilter == 'Tất cả'
        ? _interviews
        : _interviews.where((e) => e['status'] == _selectedFilter).toList();

    return Scaffold(
      appBar: AppBar(
        title: const Text('Lịch Phỏng Vấn'),
        backgroundColor: Colors.blue.shade400,
        elevation: 0,
      ),
      body: Column(
        children: [
          _buildFilterChips(),
          Expanded(
            child: filtered.isEmpty
                ? const Center(child: Text('Không có lịch phỏng vấn nào', style: TextStyle(color: Colors.black54)))
                : ListView.separated(
              padding: const EdgeInsets.all(16),
              itemCount: filtered.length,
              separatorBuilder: (_, __) => const SizedBox(height: 12),
              itemBuilder: (context, index) {
                final item = filtered[index];
                return _buildInterviewCard(item);
              },
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildFilterChips() {
    return SingleChildScrollView(
      scrollDirection: Axis.horizontal,
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
      child: Row(
        children: _filters.map((filter) {
          final isSelected = _selectedFilter == filter;
          return Padding(
            padding: const EdgeInsets.symmetric(horizontal: 4),
            child: ChoiceChip(
              label: Text(filter),
              selected: isSelected,
              onSelected: (_) {
                setState(() {
                  _selectedFilter = filter;
                });
              },
              selectedColor: Colors.blue.shade400,
              backgroundColor: Colors.grey.shade200,
              labelStyle: TextStyle(color: isSelected ? Colors.white : Colors.black87, fontWeight: FontWeight.w600),
            ),
          );
        }).toList(),
      ),
    );
  }

  Widget _buildInterviewCard(Map<String, dynamic> item) {
    final date = item['date'] as DateTime;
    final formattedDate = DateFormat('EEE, dd/MM/yyyy – HH:mm').format(date);
    final status = item['status'] as String;

    Color statusColor;
    switch (status) {
      case 'Sắp tới':
        statusColor = Colors.green;
        break;
      case 'Đã hoàn thành':
        statusColor = Colors.blueGrey;
        break;
      case 'Đã hủy':
        statusColor = Colors.redAccent;
        break;
      default:
        statusColor = Colors.grey;
    }

    return Material(
      color: Colors.white,
      borderRadius: BorderRadius.circular(14),
      elevation: 2,
      child: InkWell(
        borderRadius: BorderRadius.circular(14),
        onTap: () {
          // TODO: Xem chi tiết phỏng vấn
        },
        child: Container(
          padding: const EdgeInsets.all(14),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  Expanded(
                    child: Text(
                      item['position'] ?? 'Vị trí chưa xác định',
                      style: const TextStyle(fontSize: 15, fontWeight: FontWeight.bold),
                      overflow: TextOverflow.ellipsis,
                    ),
                  ),
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                    decoration: BoxDecoration(color: statusColor.withOpacity(0.15), borderRadius: BorderRadius.circular(12)),
                    child: Text(
                      status,
                      style: TextStyle(color: statusColor, fontWeight: FontWeight.w600, fontSize: 12),
                    ),
                  )
                ],
              ),
              const SizedBox(height: 6),
              Text(item['company'] ?? 'Công ty chưa xác định', style: const TextStyle(color: Colors.black54)),
              const SizedBox(height: 6),
              Row(
                children: [
                  const Icon(Icons.calendar_today, size: 16, color: Colors.blueAccent),
                  const SizedBox(width: 6),
                  Text(formattedDate, style: const TextStyle(color: Colors.black87, fontSize: 13)),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}
