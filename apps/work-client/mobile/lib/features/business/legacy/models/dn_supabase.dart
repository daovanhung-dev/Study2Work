class DoanhNghiepSB {
  final int id;
  final String hoTen;
  final String email;
  final String matKhau;
  final String diaChi;
  final String soDienThoai;

  DoanhNghiepSB({
    required this.id,
    required this.hoTen,
    required this.email,
    required this.matKhau,
    required this.diaChi,
    required this.soDienThoai,
  });

  /// Chuyển từ JSON Supabase → Object
  factory DoanhNghiepSB.fromJson(Map<String, dynamic> json) {
    return DoanhNghiepSB(
      id: json['id'] ?? 0,
      hoTen: json['hoten'] ?? '',
      email: json['email'] ?? '',
      matKhau: json['matkhau'] ?? '',
      diaChi: json['diachi'] ?? '',
      soDienThoai: json['sodienthoai']?.toString() ?? '',
    );
  }

  /// Chuyển từ Object → Map (để lưu xuống SQLite)
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'hoten': hoTen,
      'email': email,
      'matkhau': matKhau,
      'diachi': diaChi,
      'sodienthoai': soDienThoai,
    };
  }

  @override
  String toString() {
    return 'DoanhNghiepSB(id: $id, hoTen: $hoTen, email: $email, matKhau: $matKhau, diaChi: $diaChi, soDienThoai: $soDienThoai)';
  }
}
