class DoanhNghiep {
  final int id;
  final String hoTen;
  final String email;
  final String matKhau;
  final String diaChi;
  final String soDienThoai;

  DoanhNghiep({
    required this.id,
    required this.hoTen,
    required this.email,
    required this.matKhau,
    required this.diaChi,
    required this.soDienThoai,
  });

  /// Chuyển từ Map (SQLite) → Object
  factory DoanhNghiep.fromMap(Map<String, dynamic> map) {
    return DoanhNghiep(
      id: map['id'] ?? 0,
      hoTen: map['hoten'] ?? '',
      email: map['email'] ?? '',
      matKhau: map['matkhau'] ?? '',
      diaChi: map['diachi'] ?? '',
      soDienThoai: map['sodienthoai']?.toString() ?? '',
    );
  }

  /// Chuyển từ Object → Map (để lưu vào SQLite)
  Map<String, dynamic> toMap() {
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
    return 'DoanhNghiep(id: $id, hoTen: $hoTen, email: $email, matKhau: $matKhau, diaChi: $diaChi, soDienThoai: $soDienThoai)';
  }
}
