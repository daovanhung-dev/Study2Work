import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';

class EmployeeReportUI extends StatelessWidget {
  const EmployeeReportUI({super.key});

  @override
  Widget build(BuildContext context) {
    // ✅ Dữ liệu có kiểu rõ ràng
    final List<Map<String, double>> data = [
      {'IT': 22.0},
      {'Kế Toán': 14.0},
      {'Kinh Doanh': 18.0},
      {'Nhân Sự': 8.0},
    ];

    final labels = data.map((e) => e.keys.first).toList();
    final values = data.map((e) => e.values.first).toList();

    final total = values.reduce((a, b) => a + b);

    final maxDept = data.reduce((a, b) =>
    a.values.first > b.values.first ? a : b);
    final minDept = data.reduce((a, b) =>
    a.values.first < b.values.first ? a : b);

    return Scaffold(
      appBar: AppBar(
        title: const Text('📊 Thống kê & Báo cáo nhân sự'),
        backgroundColor: Colors.indigo,
      ),
      body: Stack(
        children: [
          // 🌄 ẢNH NỀN
          Positioned.fill(
            child: Image.asset(
              'assets/bg_trangchu.jpg', // đổi đúng tên ảnh bạn lưu
              fit: BoxFit.cover,
            ),
          ),

          // 🌟 NỘI DUNG CHÍNH
          Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text(
                  'Biểu đồ nhân sự theo phòng ban',
                  style: TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                    color: Colors.black, // chữ sáng hơn để nổi trên nền
                  ),
                ),
                const SizedBox(height: 25),

                // ====== BIỂU ĐỒ CỘT ======
                Expanded(
                  child: Card(
                    color: Colors.white.withOpacity(0.9), // hơi trong suốt
                    elevation: 4,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(16),
                    ),
                    child: Padding(
                      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 20),
                      child: BarChart(
                        BarChartData(
                          maxY: 30,
                          gridData: FlGridData(show: true, drawVerticalLine: false),
                          borderData: FlBorderData(show: false),
                          alignment: BarChartAlignment.spaceAround,
                          titlesData: FlTitlesData(
                            leftTitles: AxisTitles(
                              sideTitles: SideTitles(
                                showTitles: true,
                                reservedSize: 40,
                                getTitlesWidget: (value, meta) => Text(
                                  value.toInt().toString(),
                                  style: const TextStyle(fontSize: 12),
                                ),
                              ),
                            ),
                            bottomTitles: AxisTitles(
                              sideTitles: SideTitles(
                                showTitles: true,
                                getTitlesWidget: (x, _) => Text(
                                  labels[x.toInt()],
                                  style: const TextStyle(
                                      fontWeight: FontWeight.bold, fontSize: 13),
                                ),
                              ),
                            ),
                            rightTitles: const AxisTitles(
                                sideTitles: SideTitles(showTitles: false)),
                            topTitles: const AxisTitles(
                                sideTitles: SideTitles(showTitles: false)),
                          ),
                          barGroups: List.generate(labels.length, (index) {
                            return BarChartGroupData(
                              x: index,
                              barRods: [
                                BarChartRodData(
                                  toY: values[index],
                                  color: Colors.indigo,
                                  width: 25,
                                  borderRadius: BorderRadius.circular(8),
                                ),
                              ],
                            );
                          }),
                        ),
                      ),
                    ),
                  ),
                ),

                const SizedBox(height: 25),

                // ====== THỐNG KÊ TỔNG ======
                Card(
                  color: Colors.white.withOpacity(0.9),
                  elevation: 3,
                  shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12)),
                  child: Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 18),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text('Tổng kết nhân sự:',
                            style: TextStyle(
                                fontWeight: FontWeight.bold, fontSize: 16)),
                        const SizedBox(height: 8),
                        Text('• Tổng số nhân viên: ${total.toInt()}'),
                        Text('• Phòng ban có nhiều nhân viên nhất: ${maxDept.keys.first}'),
                        Text('• Phòng ban ít nhân viên nhất: ${minDept.keys.first}'),
                      ],
                    ),
                  ),
                ),

                const SizedBox(height: 16),

                // ====== NÚT LÀM MỚI ======
                Center(
                  child: ElevatedButton.icon(
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.indigo,
                      padding: const EdgeInsets.symmetric(horizontal: 40, vertical: 14),
                      shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(10)),
                    ),
                    onPressed: () {
                      ScaffoldMessenger.of(context).showSnackBar(
                        const SnackBar(
                          content: Text('🔄 Dữ liệu báo cáo được làm mới!'),
                          backgroundColor: Colors.green,
                        ),
                      );
                    },
                    icon: const Icon(Icons.refresh, color: Colors.white),
                    label: const Text(
                      'Làm mới báo cáo',
                      style: TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.bold,
                        color: Colors.white,
                      ),
                    ),
                  ),
                ),

                const SizedBox(height: 10),
                const Center(
                  child: Text(
                    'Nguồn dữ liệu: Demo nội bộ (có thể thay bằng API)',
                    style: TextStyle(color: Colors.white70, fontSize: 13),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
