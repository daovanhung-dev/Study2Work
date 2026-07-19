import 'package:flutter/material.dart';
import 'package:learn2earn/helper_db/helper_widget.dart';
import 'package:learn2earn/controllers/trang_chu/quan_ly_job/quan_ly_job_ctrl.dart';
import 'package:learn2earn/views/trang_chu/tien_ich/Quan_ly_job/chi_tiet_Job.dart';
import 'package:learn2earn/views/trang_chu/main/dang_tin_tuyen_dung.dart';
class QuanLyJob extends StatefulWidget {
  const QuanLyJob({super.key});

  @override
  State<QuanLyJob> createState() => _QuanLyJobState();
}

class _QuanLyJobState extends State<QuanLyJob> {

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey[100],
      appBar: AppBar(
        backgroundColor: const Color(0xFF7ecbff),
        title: const Text("Quản lý Job", style: TextStyle(fontWeight: FontWeight.w600)),
        centerTitle: true,
      ),
      body: FutureBuilder(
        future: getJob(),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          } else if (snapshot.hasError) {
            return Center(child: Text("Lỗi: ${snapshot.error}"));
          } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
            return const Center(child: Text("Không có dữ liệu"));
          }

          final dsJobs = snapshot.data!;
          return ListView.builder(
            padding: const EdgeInsets.symmetric(vertical: 16, horizontal: 12),
            itemCount: dsJobs.length,
            itemBuilder: (context, i) {
              final job = dsJobs[i];
              int id_JD = job.id;
              return Card(
                margin: const EdgeInsets.only(bottom: 16),
                elevation: 4,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(16),
                ),
                child: Padding(
                  padding: const EdgeInsets.all(14),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      _titleLine(Icons.work_outline, job.tenViTri ?? "Không có tên"),
                      const SizedBox(height: 6),
                      _infoLine("Mã công việc", "${job.id}"),
                      _infoLine("Cấp bậc", job.capBac),
                      _infoLine("Nhiệm vụ", job.nhiemVu),
                      _infoLine("Trình độ", job.trinhDo),
                      _infoLine("Kinh nghiệm", job.kinhNghiem),
                      _infoLine("Mức lương", job.mucLuong),
                      _infoLine("Địa điểm", job.diaDiem),
                      _infoLine("Thời gian", job.thoiGian),
                      const SizedBox(height: 10),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                        children: [
                          _actionButton(Icons.visibility, "Chi tiết", Colors.blueAccent, () {
                            Navigator.push(context,MaterialPageRoute(builder: (context) => XemChiTietJD(id: id_JD),),);
                          }),
                          _actionButton(Icons.edit, "Sửa", Colors.orange, () {}),
                          _actionButton(Icons.delete, "Xóa", Colors.redAccent, () {}),
                        ],
                      ),
                    ],
                  ),
                ),
              );
            },
          );
        },
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          Navigator.push(context,MaterialPageRoute(builder: (context) => DangTinTuyenDung(),),);
        },
        backgroundColor: const Color(0xFF7ecbff),
        child: const Icon(Icons.add),
      ),
    );
  }

  Widget _titleLine(IconData icon, String text) {
    return Row(
      children: [
        Icon(icon, color: Colors.blueAccent),
        const SizedBox(width: 8),
        Expanded(
          child: Text(
            text,
            style: const TextStyle(
              fontWeight: FontWeight.w600,
              fontSize: 16,
              color: Colors.black87,
            ),
          ),
        ),
      ],
    );
  }

  Widget _infoLine(String label, String? value) {
    if (value == null || value.isEmpty) return const SizedBox.shrink();
    return Padding(
      padding: const EdgeInsets.only(bottom: 4),
      child: RichText(
        text: TextSpan(
          text: "$label: ",
          style: const TextStyle(color: Colors.black87, fontWeight: FontWeight.w500, fontSize: 13),
          children: [
            TextSpan(
              text: value,
              style: const TextStyle(color: Colors.black54, fontWeight: FontWeight.normal),
            ),
          ],
        ),
      ),
    );
  }

  Widget _actionButton(IconData icon, String label, Color color, VoidCallback onTap) {
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(10),
      child: Container(
        width: 90,
        height: 36,
        decoration: BoxDecoration(
          color: color.withOpacity(0.12),
          borderRadius: BorderRadius.circular(10),
          border: Border.all(color: color.withOpacity(0.3)),
        ),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(icon, size: 18, color: color),
            const SizedBox(width: 5),
            Text(label, style: TextStyle(fontSize: 13, color: color, fontWeight: FontWeight.w600)),
          ],
        ),
      ),
    );
  }
}
