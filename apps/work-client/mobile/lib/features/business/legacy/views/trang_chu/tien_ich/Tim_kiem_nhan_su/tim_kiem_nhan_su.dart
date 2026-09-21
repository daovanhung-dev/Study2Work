import 'package:flutter/material.dart';
import 'package:study2work_mobile/app/theme/design_tokens.dart';
import 'package:study2work_mobile/features/business/legacy/controllers/trang_chu/timkiemctrl.dart';
import 'package:study2work_mobile/features/business/legacy/helper_db/helper_widget.dart';

class EmployeeSearchUI extends StatefulWidget {
  const EmployeeSearchUI({super.key});

  @override
  State<EmployeeSearchUI> createState() => _EmployeeSearchUIState();
}

class _EmployeeSearchUIState extends State<EmployeeSearchUI> {
  TextEditingController chuyenNganh = TextEditingController();
  List<String> nganhOptions = ['IT', 'Kế Toán'];
  String? selected;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('🔍 Tìm kiếm nhân sự'),
        backgroundColor: AppColors.primary,
      ),
      body: Stack(
        children: [
          Positioned.fill(
            child: Image.asset('assets/business/bg_trangchu.jpg', fit: BoxFit.cover),
          ),
          SingleChildScrollView(
            padding: const EdgeInsets.all(16),
            child: Container(
              width: 320,
              height: 700,
              padding: const EdgeInsets.symmetric(vertical: 20, horizontal: 20),
              margin: const EdgeInsets.symmetric(vertical: 20),
              decoration: BoxDecoration(
                color: AppColors.surface,
                borderRadius: BorderRadius.circular(20),
                boxShadow: [
                  BoxShadow(
                    color: AppColors.navy.withValues(alpha: 0.1),
                    spreadRadius: 5,
                    blurRadius: 7,
                    offset: const Offset(0, 3),
                  ),
                ],
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  helperTextField(
                    controller: chuyenNganh,
                    label: 'Tìm kiếm nhanh',
                  ),
                  SizedBox(height: 10),
                  helperDropdown(
                    value: selected,
                    items: nganhOptions,
                    label: "Chuyên Ngành",
                    onChanged: (value) {
                      setState(() {
                        selected = value;
                      });
                    },
                  ),
                  SizedBox(height: 10),
                  ElevatedButton(
                    onPressed: () {
                      timKiem(chuyenNganh.text);
                    },
                    child: Text('Tìm kiếm'),
                  ),

                  const SizedBox(height: 20),
                  Text(
                    selected == null
                        ? 'Chưa chọn ngành'
                        : 'Ngành đã chọn: $selected',
                    style: const TextStyle(fontSize: 16),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
