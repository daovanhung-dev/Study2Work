
class DoanhNghiep {
  final String maDN;
  final String tenDN;
  final String email;
  final String matKhau;
  final String diaChi;
  final String soDienThoai;

  DoanhNghiep({
    required this.maDN,
    required this.tenDN,
    required this.email,
    required this.matKhau,
    required this.diaChi,
    required this.soDienThoai,
  });

  // Convert từ Map (SQLite) -> Object
  factory DoanhNghiep.fromMap(Map<String, dynamic> map) {
    return DoanhNghiep(
      maDN: map['MaDN'],
      tenDN: map['TenDN'],
      email: map['Email'],
      matKhau: map['MatKhau'],
      diaChi: map['DiaChi'],
      soDienThoai: map['SoDienThoai'],
    );
  }

  // Convert từ Object -> Map (SQLite)
  Map<String, dynamic> toMap() {
    return {
      'MaDN': maDN,
      'TenDN': tenDN,
      'Email': email,
      'MatKhau': matKhau,
      'DiaChi': diaChi,
      'SoDienThoai': soDienThoai,
    };
  }

  factory DoanhNghiep.fromJson(Map<String, dynamic> json) {
    return DoanhNghiep(
      maDN: json['MaDN'],
      tenDN: json['TenDN'],
      email: json['Email'],
      matKhau: json['MatKhau'],
      diaChi: json['DiaChi'],
      soDienThoai: json['SoDienThoai'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'MaDN': maDN,
      'TenDN': tenDN,
      'Email': email,
      'MatKhau': matKhau,
      'DiaChi': diaChi,
      'SoDienThoai': soDienThoai,
    };
  }
}


