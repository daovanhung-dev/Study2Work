import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'package:learn2earn/controllers/trang_chu/quan_ly_CV/quan_ly_job_CV.dart';
import 'package:learn2earn/models/sinh_vien/CV.dart';

class QuanLyCVView extends StatefulWidget {
  const QuanLyCVView({super.key});

  @override
  State<QuanLyCVView> createState() => _QuanLyCVViewState();
}

class _QuanLyCVViewState extends State<QuanLyCVView> {
  final CVCtrl _ctrl = CVCtrl();
  CV? _cv;
  bool _loading = true;
  bool _editing = false;

  // Controllers cho các trường thông tin
  final _hotenCtrl = TextEditingController();
  final _emailCtrl = TextEditingController();
  final _sdtCtrl = TextEditingController();
  final _diachiCtrl = TextEditingController();
  final _gioitinhCtrl = TextEditingController();
  final _vitriCtrl = TextEditingController();
  final _nganhCtrl = TextEditingController();
  final _muctieuCtrl = TextEditingController();
  final _hocvanCtrl = TextEditingController();
  final _kinhnghiemCtrl = TextEditingController();
  final _kynangCtrl = TextEditingController();
  final _ngoainguCtrl = TextEditingController();
  final _chungchiCtrl = TextEditingController();
  final _duanCtrl = TextEditingController();
  final _giaithuongCtrl = TextEditingController();
  final _hoatdongCtrl = TextEditingController();
  final _portfolioCtrl = TextEditingController();
  final _luongmongmuonCtrl = TextEditingController();

  @override
  void initState() {
    super.initState();
    _loadCV();
  }

  Future<void> _loadCV() async {
    final cv = await _ctrl.getCVById(); // giả định CV id=1
    if (!mounted) return;
    setState(() {
      _cv = cv;
      _loading = false;
    });
    if (cv != null) {
      _hotenCtrl.text = cv.hoten;
      _emailCtrl.text = cv.email;
      _sdtCtrl.text = cv.sdt ?? '';
      _diachiCtrl.text = cv.diachi ?? '';
      _gioitinhCtrl.text = cv.gioitinh ?? '';
      _vitriCtrl.text = cv.vitri ?? '';
      _nganhCtrl.text = cv.nganh ?? '';
      _muctieuCtrl.text = cv.muctieunghiep ?? '';
      _hocvanCtrl.text = cv.hocvan ?? '';
      _kinhnghiemCtrl.text = cv.kinhnghiem ?? '';
      _kynangCtrl.text = cv.kynang ?? '';
      _ngoainguCtrl.text = cv.ngoaingu ?? '';
      _chungchiCtrl.text = cv.chungchi ?? '';
      _duanCtrl.text = cv.duan ?? '';
      _giaithuongCtrl.text = cv.giaithuong ?? '';
      _hoatdongCtrl.text = cv.hoatdong ?? '';
      _portfolioCtrl.text = cv.portfolio ?? '';
      _luongmongmuonCtrl.text = cv.luongmongmuon ?? '';
    }
  }

  void _toggleEdit() async {
    if (_editing) {
      await _updateCV();
    } else {
      setState(() => _editing = true);
    }
  }

  Future<void> _updateCV() async {
    if (_cv == null) return;

    final updated = _cv!.copyWith(
      hoten: _hotenCtrl.text.trim(),
      email: _emailCtrl.text.trim(),
      sdt: _sdtCtrl.text.trim(),
      diachi: _diachiCtrl.text.trim(),
      gioitinh: _gioitinhCtrl.text.trim(),
      vitri: _vitriCtrl.text.trim(),
      nganh: _nganhCtrl.text.trim(),
      muctieunghiep: _muctieuCtrl.text.trim(),
      hocvan: _hocvanCtrl.text.trim(),
      kinhnghiem: _kinhnghiemCtrl.text.trim(),
      kynang: _kynangCtrl.text.trim(),
      ngoaingu: _ngoainguCtrl.text.trim(),
      chungchi: _chungchiCtrl.text.trim(),
      duan: _duanCtrl.text.trim(),
      giaithuong: _giaithuongCtrl.text.trim(),
      hoatdong: _hoatdongCtrl.text.trim(),
      portfolio: _portfolioCtrl.text.trim(),
      luongmongmuon: _luongmongmuonCtrl.text.trim(),
    );

    try {
      await _ctrl.Update(updated);
      if (!mounted) return;

      setState(() {
        _cv = updated;
        _editing = false;
      });

      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('✅ Cập nhật CV thành công!'),
          backgroundColor: Colors.green,
        ),
      );
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('❌ Lỗi khi cập nhật: $e'),
          backgroundColor: Colors.red,
        ),
      );
    }
  }

  Widget _buildTextField(String label, TextEditingController controller, {bool enabled = true}) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 6),
      child: TextField(
        controller: controller,
        enabled: enabled,
        maxLines: null,
        decoration: InputDecoration(
          labelText: label,
          border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
          filled: true,
          fillColor: enabled ? Colors.white : Colors.blue.shade50,
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.blue.shade50,
      appBar: AppBar(
        title: const Text('Quản lý CV', style: TextStyle(fontWeight: FontWeight.bold)),
        backgroundColor: Colors.blue.shade400,
        centerTitle: true,
      ),
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : _cv == null
          ? _buildEmptyCVView()
          : _buildCVDetailView(),
      floatingActionButton: _cv == null
          ? FloatingActionButton(
        backgroundColor: Colors.blue,
        onPressed: () {},
        child: const Icon(Icons.add),
      )
          : FloatingActionButton(
        backgroundColor: _editing ? Colors.green : Colors.blue,
        onPressed: _toggleEdit,
        child: Icon(_editing ? Icons.save : Icons.edit),
      ),
    );
  }

  Widget _buildEmptyCVView() {
    return const Center(
      child: Text('Bạn chưa có CV nào!', style: TextStyle(fontSize: 20)),
    );
  }

  Widget _buildCVDetailView() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Card(
        elevation: 6,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
        child: Padding(
          padding: const EdgeInsets.all(20),
          child: Column(
            children: [
              CircleAvatar(
                radius: 45,
                backgroundImage: _cv!.avt != null
                    ? NetworkImage(_cv!.avt!)
                    : const AssetImage('assets/images/default_avatar.png') as ImageProvider,
              ),
              const SizedBox(height: 10),
              Text(_cv!.hoten, style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
              const Divider(height: 30, thickness: 1.5),
              _buildTextField('Họ và tên', _hotenCtrl, enabled: _editing),
              _buildTextField('Email', _emailCtrl, enabled: _editing),
              _buildTextField('Số điện thoại', _sdtCtrl, enabled: _editing),
              _buildTextField('Giới tính', _gioitinhCtrl, enabled: _editing),
              _buildTextField('Địa chỉ', _diachiCtrl, enabled: _editing),
              _buildTextField('Vị trí mong muốn', _vitriCtrl, enabled: _editing),
              _buildTextField('Ngành nghề', _nganhCtrl, enabled: _editing),
              _buildTextField('Mục tiêu nghề nghiệp', _muctieuCtrl, enabled: _editing),
              _buildTextField('Học vấn', _hocvanCtrl, enabled: _editing),
              _buildTextField('Kinh nghiệm', _kinhnghiemCtrl, enabled: _editing),
              _buildTextField('Kỹ năng', _kynangCtrl, enabled: _editing),
              _buildTextField('Ngoại ngữ', _ngoainguCtrl, enabled: _editing),
              _buildTextField('Chứng chỉ', _chungchiCtrl, enabled: _editing),
              _buildTextField('Dự án', _duanCtrl, enabled: _editing),
              _buildTextField('Giải thưởng', _giaithuongCtrl, enabled: _editing),
              _buildTextField('Hoạt động', _hoatdongCtrl, enabled: _editing),
              _buildTextField('Portfolio', _portfolioCtrl, enabled: _editing),
              _buildTextField('Lương mong muốn', _luongmongmuonCtrl, enabled: _editing),
              const SizedBox(height: 30),
            ],
          ),
        ),
      ),
    );
  }
}
