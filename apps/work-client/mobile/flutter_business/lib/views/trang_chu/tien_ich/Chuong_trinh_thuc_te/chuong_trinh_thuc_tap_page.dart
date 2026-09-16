import 'package:flutter/material.dart';

// [MODEL TỪ PHẦN TRÊN]
class ThucTapProgram {
  final String hoTen;
  final String nganhHoc;
  final String truong;
  final String viTri;
  final String thoiGian;
  final String nguoiHuongDan;

  ThucTapProgram({
    required this.hoTen,
    required this.nganhHoc,
    required this.truong,
    required this.viTri,
    required this.thoiGian,
    required this.nguoiHuongDan,
  });
}

class ChuongTrinhThucTapPage extends StatefulWidget {
  const ChuongTrinhThucTapPage({super.key});

  @override
  State<ChuongTrinhThucTapPage> createState() => _ChuongTrinhThucTapPageState();
}

class _ChuongTrinhThucTapPageState extends State<ChuongTrinhThucTapPage> {
  // DANH SÁCH LƯU TRỮ CHƯƠNG TRÌNH THỰC TẬP
  final List<ThucTapProgram> _programList = [];

  // Callback để nhận dữ liệu từ Form con
  void _addProgram(ThucTapProgram program) {
    setState(() {
      _programList.add(program);
    });

    // Cuộn xuống cuối để thấy item mới (nếu đang ở cuối danh sách)
    // Cần phải có ScrollController để làm việc này
  }

  void _deleteProgram(int index) {
    setState(() {
      _programList.removeAt(index);
    });
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text("Đã xóa chương trình thực tập thành công!"), backgroundColor: Colors.redAccent),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("CHƯƠNG TRÌNH THỰC TẬP", style: TextStyle(fontWeight: FontWeight.bold, color: Colors.white)),
        centerTitle: true,
        backgroundColor: Colors.green,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // FORM NHẬP LIỆU
            const Text(
                '📝 THÊM CHƯƠNG TRÌNH MỚI',
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.green)
            ),
            const Divider(color: Colors.green),

            // Truyền hàm _addProgram vào Form để nó gọi lại khi lưu thành công
            ChuongTrinhThucTapForm(onSave: _addProgram),

            const SizedBox(height: 30),

            // HIỂN THỊ DANH SÁCH ĐÃ LƯU
            const Text(
                '📋 DANH SÁCH CHƯƠNG TRÌNH ĐÃ LƯU',
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.green)
            ),
            const Divider(color: Colors.green),

            _programList.isEmpty
                ? const Center(
              child: Padding(
                padding: EdgeInsets.only(top: 20),
                child: Text(
                  'Chưa có chương trình thực tập nào được lưu.',
                  style: TextStyle(fontStyle: FontStyle.italic, color: Colors.grey),
                ),
              ),
            )
                : ListView.builder(
              shrinkWrap: true, // Quan trọng khi nằm trong SingleChildScrollView
              physics: const NeverScrollableScrollPhysics(), // Vô hiệu hóa cuộn của ListView
              itemCount: _programList.length,
              itemBuilder: (context, index) {
                return _buildProgramCard(_programList[index], index);
              },
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildProgramCard(ThucTapProgram program, int index) {
    return Card(
      elevation: 4,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      margin: const EdgeInsets.only(bottom: 15),
      child: ListTile(
        contentPadding: const EdgeInsets.all(15),
        leading: const Icon(Icons.badge, size: 40, color: Colors.green),
        title: Text(
            program.hoTen,
            style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16, color: Colors.indigo)
        ),
        subtitle: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const SizedBox(height: 4),
            Text('🎓 ${program.truong} - ${program.nganhHoc}'),
            Text('💼 Vị trí: ${program.viTri}'),
            Text('🕒 Thời gian: ${program.thoiGian}', style: const TextStyle(fontWeight: FontWeight.w500)),
            Text('👨‍🏫 HD: ${program.nguoiHuongDan}'),
          ],
        ),
        trailing: IconButton(
          icon: const Icon(Icons.delete_forever, color: Colors.redAccent),
          onPressed: () => _deleteProgram(index),
        ),
      ),
    );
  }
}

// 3. Widget Form Nhập Liệu (Tách ra để chuyên nghiệp hơn)

class ChuongTrinhThucTapForm extends StatefulWidget {
  final Function(ThucTapProgram) onSave; // Biến Callback

  const ChuongTrinhThucTapForm({super.key, required this.onSave});

  @override
  State<ChuongTrinhThucTapForm> createState() => _ChuongTrinhThucTapFormState();
}

class _ChuongTrinhThucTapFormState extends State<ChuongTrinhThucTapForm> {
  final _formKey = GlobalKey<FormState>();
  final TextEditingController _hoTenController = TextEditingController();
  final TextEditingController _nganhHocController = TextEditingController();
  final TextEditingController _truongController = TextEditingController();
  final TextEditingController _nguoiHuongDanController = TextEditingController();

  String? _viTriThucTap;
  String? _thoiGianThucTap;

  final List<String> _viTriOptions = ['Mobile App (Flutter/React Native)', 'Backend (NodeJS/Java)', 'Frontend (React/Vue)', 'Tester/QA', 'Designer/UX'];
  final List<String> _thoiGianOptions = ['3 tháng (Bán thời gian)', '6 tháng (Toàn thời gian)', 'Theo yêu cầu của trường'];

  @override
  void dispose() {
    _hoTenController.dispose();
    _nganhHocController.dispose();
    _truongController.dispose();
    _nguoiHuongDanController.dispose();
    super.dispose();
  }

  void _luuChuongTrinh() {
    if (_formKey.currentState!.validate()) {
      // Dữ liệu hợp lệ, tạo đối tượng Model
      final program = ThucTapProgram(
        hoTen: _hoTenController.text.trim(),
        nganhHoc: _nganhHocController.text.trim(),
        truong: _truongController.text.trim(),
        viTri: _viTriThucTap!,
        thoiGian: _thoiGianThucTap!,
        nguoiHuongDan: _nguoiHuongDanController.text.trim(),
      );

      // GỌI CALLBACK ĐỂ TRUYỀN DỮ LIỆU LÊN WIDGET CHA (ChuongTrinhThucTapPage)
      widget.onSave(program);

      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text("Lưu thành công chương trình thực tập của: ${program.hoTen}!"),
          backgroundColor: Colors.green,
        ),
      );

      // Reset Form sau khi lưu
      _formKey.currentState?.reset();
      _hoTenController.clear();
      _nganhHocController.clear();
      _truongController.clear();
      _nguoiHuongDanController.clear();
      setState(() {
        _viTriThucTap = null;
        _thoiGianThucTap = null;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Form(
      key: _formKey,
      child: Column(
        children: [
          _buildTextField("Họ và tên", _hoTenController, Icons.person),
          _buildTextField("Ngành học", _nganhHocController, Icons.class_),
          _buildTextField("Trường học", _truongController, Icons.school),

          _buildDropdownField(
            'Vị trí thực tập',
            Icons.work,
            _viTriThucTap,
            _viTriOptions,
                (v) => setState(() => _viTriThucTap = v),
          ),

          _buildDropdownField(
            'Thời gian thực tập',
            Icons.schedule,
            _thoiGianThucTap,
            _thoiGianOptions,
                (v) => setState(() => _thoiGianThucTap = v),
          ),

          _buildTextField("Người hướng dẫn", _nguoiHuongDanController, Icons.person_pin),

          const SizedBox(height: 20),
          ElevatedButton.icon(
            icon: const Icon(Icons.save),
            label: const Text("LƯU CHƯƠNG TRÌNH", style: TextStyle(fontSize: 16)),
            style: ElevatedButton.styleFrom(
              backgroundColor: Colors.green,
              foregroundColor: Colors.white,
              minimumSize: const Size(double.infinity, 55),
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
              elevation: 5,
            ),
            onPressed: _luuChuongTrinh,
          ),
          const SizedBox(height: 10),
        ],
      ),
    );
  }

  Widget _buildTextField(String label, TextEditingController controller, IconData icon) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 16),
      child: TextFormField(
        controller: controller,
        decoration: InputDecoration(
          labelText: label,
          prefixIcon: Icon(icon, color: Colors.green.shade600),
          border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
          filled: true,
          fillColor: Colors.green.shade50.withOpacity(0.5),
        ),
        validator: (value) => (value == null || value.isEmpty) ? "Vui lòng nhập $label" : null,
      ),
    );
  }

  Widget _buildDropdownField(String label, IconData icon, String? value, List<String> items, Function(String?) onChanged) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 16),
      child: DropdownButtonFormField<String>(
        value: value,
        decoration: InputDecoration(
          labelText: label,
          prefixIcon: Icon(icon, color: Colors.green.shade600),
          border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
          filled: true,
          fillColor: Colors.green.shade50.withOpacity(0.5),
        ),
        hint: Text("Chọn $label"),
        items: items.map((String item) {
          return DropdownMenuItem(
            value: item,
            child: Text(item),
          );
        }).toList(),
        onChanged: onChanged,
        validator: (v) => v == null ? "Vui lòng chọn $label" : null,
      ),
    );
  }
}