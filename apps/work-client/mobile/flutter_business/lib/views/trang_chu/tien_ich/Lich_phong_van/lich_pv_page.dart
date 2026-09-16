import 'package:flutter/material.dart';
import 'package:intl/intl.dart';

class LichPV extends StatefulWidget {
  const LichPV({super.key});

  @override
  State<LichPV> createState() => _LichPVState();
}

class _LichPVState extends State<LichPV> {
  // Thay đổi: Lưu trữ DateTime để có cả Ngày và Giờ
  final List<Map<String, dynamic>> _lichPVList = [];
  final DateFormat _dateFormat = DateFormat('EEEE, dd/MM/yyyy'); // VD: Thứ Hai, 10/06/2025
  final DateFormat _timeFormat = DateFormat('HH:mm'); // VD: 09:30

  // Hàm format TimeOfDay cũ được thay thế bằng format DateTime
  String _formatDateTime(DateTime dt) {
    // Format giờ: 09:30 sáng/chiều
    final timeStr = DateFormat('hh:mm').format(dt);
    final period = dt.hour >= 12 ? 'chiều' : 'sáng';
    return '$timeStr $period';
  }

  void _openForm({Map<String, dynamic>? data, int? index}) {
    final hoTenCtrl = TextEditingController(text: data?['hoTen'] ?? '');
    final sdtCtrl = TextEditingController(text: data?['sdt'] ?? '');
    final emailCtrl = TextEditingController(text: data?['email'] ?? '');
    final nguoiPVCtrl = TextEditingController(text: data?['nguoiPV'] ?? '');
    final ghiChuCtrl = TextEditingController(text: data?['ghiChu'] ?? '');

    // Khởi tạo DateTime: Nếu chỉnh sửa, lấy giá trị cũ; nếu thêm mới, lấy ngày/giờ hiện tại
    DateTime? thoiGianPV = data?['thoiGianPV'];
    if (thoiGianPV == null) {
      // Làm tròn đến nửa giờ gần nhất cho lịch mới
      final now = DateTime.now();
      thoiGianPV = now.add(Duration(minutes: 30 - now.minute % 30));
    }

    String hinhThuc = data?['hinhThuc'] ?? 'Online';

    // Controller chỉ để hiển thị Ngày/Giờ đã chọn
    final ngayGioPVCtrl = TextEditingController(
        text: data?['thoiGianPV'] != null ?
        '${_dateFormat.format(thoiGianPV!)} - ${_formatDateTime(thoiGianPV!)}' : ''
    );

    showDialog(
      context: context,
      builder: (context) {
        return StatefulBuilder(builder: (context, setStateDialog) {

          Future<void> _pickDateTime() async {
            // 1. Chọn ngày
            final pickedDate = await showDatePicker(
              context: context,
              initialDate: thoiGianPV ?? DateTime.now(),
              firstDate: DateTime.now().subtract(const Duration(days: 365)),
              lastDate: DateTime.now().add(const Duration(days: 365)),
            );

            if (pickedDate != null) {
              // 2. Chọn giờ (sau khi đã chọn ngày)
              final pickedTime = await showTimePicker(
                context: context,
                initialTime: TimeOfDay.fromDateTime(thoiGianPV ?? DateTime.now()),
              );

              if (pickedTime != null) {
                // Kết hợp Ngày và Giờ
                thoiGianPV = DateTime(
                  pickedDate.year,
                  pickedDate.month,
                  pickedDate.day,
                  pickedTime.hour,
                  pickedTime.minute,
                );

                ngayGioPVCtrl.text = '${_dateFormat.format(thoiGianPV!)} - ${_formatDateTime(thoiGianPV!)}';
                setStateDialog(() {});
              }
            }
          }

          void _onSave() {
            final hoTen = hoTenCtrl.text.trim();
            final sdt = sdtCtrl.text.trim();
            final email = emailCtrl.text.trim();
            final nguoiPV = nguoiPVCtrl.text.trim();
            final ghiChu = ghiChuCtrl.text.trim();

            if (hoTen.isEmpty || sdt.isEmpty || thoiGianPV == null) {
              ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text('Vui lòng nhập Họ tên, SĐT và chọn Ngày/Giờ PV.')));
              return;
            }

            if (email.isNotEmpty && !RegExp(r'^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$').hasMatch(email)) {
              ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text('Địa chỉ Email không hợp lệ.')));
              return;
            }

            final newData = <String, dynamic>{
              'hoTen': hoTen,
              'sdt': sdt,
              'email': email,
              'thoiGianPV': thoiGianPV, // Đã thay thế gioPV
              'nguoiPV': nguoiPV,
              'hinhThuc': hinhThuc,
              'ghiChu': ghiChu,
            };

            setState(() {
              if (index == null) {
                _lichPVList.add(newData);
              } else {
                _lichPVList[index] = newData;
              }
              // Sắp xếp lại danh sách theo thời gian phỏng vấn
              _lichPVList.sort((a, b) => (a['thoiGianPV'] as DateTime).compareTo(b['thoiGianPV'] as DateTime));
            });
            Navigator.of(context).pop();
          }

          return AlertDialog(
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
            title: Text(
              index == null ? 'Thêm lịch phỏng vấn' : 'Chỉnh sửa lịch phỏng vấn',
              style: const TextStyle(fontWeight: FontWeight.bold, color: Colors.indigo),
            ),
            content: SingleChildScrollView(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                mainAxisSize: MainAxisSize.min,
                children: [
                  // Các trường TextField cũ
                  _buildTextField(hoTenCtrl, 'Họ và tên', Icons.person),
                  _buildTextField(sdtCtrl, 'Số điện thoại', Icons.phone, keyboardType: TextInputType.phone),
                  _buildTextField(emailCtrl, 'Email (Gmail)', Icons.email, keyboardType: TextInputType.emailAddress),

                  const SizedBox(height: 12),
                  // Chọn Ngày/Giờ Phỏng vấn
                  Row(
                    children: [
                      Expanded(
                        child: _buildTextField(
                          ngayGioPVCtrl,
                          'Ngày & Giờ phỏng vấn',
                          Icons.date_range,
                          readOnly: true, // Chỉ hiển thị, không cho gõ tay
                          validator: (v) => v!.isEmpty ? 'Vui lòng chọn Ngày và Giờ' : null,
                        ),
                      ),
                      IconButton(
                        icon: const Icon(Icons.schedule, color: Colors.indigo, size: 30),
                        onPressed: _pickDateTime,
                      ),
                    ],
                  ),

                  const SizedBox(height: 12),
                  _buildTextField(nguoiPVCtrl, 'Người phỏng vấn', Icons.person_pin),

                  const SizedBox(height: 12),
                  // Dropdown cho Hình thức
                  DropdownButtonFormField<String>(
                    value: hinhThuc,
                    decoration: const InputDecoration(
                      labelText: 'Hình thức',
                      prefixIcon: Icon(Icons.videocam),
                      border: OutlineInputBorder(borderRadius: BorderRadius.all(Radius.circular(12))),
                      contentPadding: EdgeInsets.symmetric(vertical: 8, horizontal: 12),
                    ),
                    items: ['Online', 'Offline'].map((String value) {
                      return DropdownMenuItem<String>(
                        value: value,
                        child: Text(value),
                      );
                    }).toList(),
                    onChanged: (String? newValue) {
                      setStateDialog(() {
                        hinhThuc = newValue!;
                      });
                    },
                  ),

                  const SizedBox(height: 12),
                  _buildTextField(ghiChuCtrl, 'Ghi chú (tùy chọn)', Icons.note, maxLines: 2),
                ],
              ),
            ),
            actions: [
              TextButton(
                  onPressed: () => Navigator.of(context).pop(),
                  child: const Text('Hủy', style: TextStyle(color: Colors.red))),
              ElevatedButton.icon(
                onPressed: _onSave,
                icon: const Icon(Icons.save),
                label: Text(index == null ? 'Thêm' : 'Cập nhật'),
                style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.indigo,
                    foregroundColor: Colors.white,
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8))
                ),
              ),
            ],
          );
        });
      },
    );
  }

  Widget _buildTextField(TextEditingController controller, String label, IconData icon,
      {TextInputType keyboardType = TextInputType.text, bool readOnly = false, int maxLines = 1, String? Function(String?)? validator}) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 8.0),
      child: TextFormField(
        controller: controller,
        keyboardType: keyboardType,
        readOnly: readOnly,
        maxLines: maxLines,
        decoration: InputDecoration(
          labelText: label,
          prefixIcon: Icon(icon, color: Colors.indigo.shade400),
          border: const OutlineInputBorder(borderRadius: BorderRadius.all(Radius.circular(12))),
          contentPadding: const EdgeInsets.symmetric(vertical: 12, horizontal: 12),
        ),
        validator: validator,
      ),
    );
  }

  void _confirmDelete(int index) {
    // Logic xác nhận xóa giữ nguyên
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Xác nhận xóa'),
        content: Text('Bạn có chắc muốn xóa lịch phỏng vấn của ${_lichPVList[index]['hoTen']}?'),
        actions: [
          TextButton(onPressed: () => Navigator.of(context).pop(), child: const Text('Hủy')),
          ElevatedButton(
            onPressed: () {
              setState(() => _lichPVList.removeAt(index));
              Navigator.of(context).pop();
            },
            style: ElevatedButton.styleFrom(backgroundColor: Colors.red, foregroundColor: Colors.white),
            child: const Text('Xóa'),
          ),
        ],
      ),
    );
  }

  Widget _buildPVCard(Map<String, dynamic> item, int index) {
    final DateTime? thoiGianPV = item['thoiGianPV'];
    final ngayText = thoiGianPV != null ? _dateFormat.format(thoiGianPV) : 'Chưa chọn ngày';
    final gioText = thoiGianPV != null ? _formatDateTime(thoiGianPV) : 'Chưa chọn giờ';
    final hinhThuc = item['hinhThuc'] ?? 'Online';

    return Card(
      elevation: 6,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      margin: const EdgeInsets.symmetric(vertical: 10),
      child: ListTile(
        contentPadding: const EdgeInsets.all(16),
        // Leading là biểu tượng/màu sắc nổi bật cho thời gian
        leading: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(thoiGianPV != null ? _timeFormat.format(thoiGianPV) : '??:??',
                style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.green)),
            Text(thoiGianPV != null ? DateFormat('dd/MM').format(thoiGianPV) : '',
                style: const TextStyle(fontSize: 12, color: Colors.grey)),
          ],
        ),
        // Title là Họ tên
        title: Text(
          item['hoTen'] ?? 'Ứng viên không tên',
          style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.indigo),
        ),
        // Subtitle là Thông tin cơ bản và Người PV
        subtitle: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const SizedBox(height: 4),
            Text('📅 $ngayText'),
            Text('👤 Người PV: ${item['nguoiPV'] ?? 'Chưa xác định'}'),
            if ((item['email']?.toString() ?? '').isNotEmpty) Text('📧 ${item['email']}'),
            if ((item['sdt']?.toString() ?? '').isNotEmpty) Text('📞 ${item['sdt']}'),
            const SizedBox(height: 8),
            // Chip nổi bật Hình thức
            Chip(
              label: Text(hinhThuc, style: const TextStyle(fontWeight: FontWeight.bold)),
              avatar: Icon(hinhThuc == 'Online' ? Icons.laptop : Icons.business),
              backgroundColor: hinhThuc == 'Online' ? Colors.lightBlue.shade100 : Colors.orange.shade100,
            ),
            if ((item['ghiChu']?.toString() ?? '').isNotEmpty)
              Padding(
                padding: const EdgeInsets.only(top: 8.0),
                child: Text('🗒 Ghi chú: ${item['ghiChu']}', style: const TextStyle(fontStyle: FontStyle.italic)),
              ),
          ],
        ),
        // Trailing là các nút chỉnh sửa/xóa
        trailing: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            IconButton(
              icon: const Icon(Icons.edit, color: Colors.green),
              onPressed: () => _openForm(data: item, index: index),
            ),
            IconButton(
              icon: const Icon(Icons.delete, color: Colors.redAccent),
              onPressed: () => _confirmDelete(index),
            ),
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('🗓 LỊCH PHỎNG VẤN', style: TextStyle(fontWeight: FontWeight.bold, color: Colors.white)),
        centerTitle: true,
        backgroundColor: Colors.indigo,
        elevation: 0,
      ),
      body: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
        child: _lichPVList.isEmpty
            ? const Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(Icons.event_busy, size: 80, color: Colors.grey),
              SizedBox(height: 16),
              Text(
                'Chưa có lịch phỏng vấn nào.\nHãy nhấn "+" để bắt đầu thêm mới.',
                textAlign: TextAlign.center,
                style: TextStyle(fontSize: 16, color: Colors.grey),
              ),
            ],
          ),
        )
            : ListView.builder(
          itemCount: _lichPVList.length,
          itemBuilder: (context, i) => _buildPVCard(_lichPVList[i], i),
        ),
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () => _openForm(),
        label: const Text('Thêm lịch PV', style: TextStyle(fontWeight: FontWeight.bold)),
        icon: const Icon(Icons.add),
        backgroundColor: Colors.indigo,
        foregroundColor: Colors.white,
      ),
    );
  }
}