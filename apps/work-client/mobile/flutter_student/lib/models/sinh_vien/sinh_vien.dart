class SinhVien {
  final int? id;
  final String? hoten;
  final String? email;
  final String? matkhau;
  final String? chuyennganh;
  final String? avt;


  SinhVien({
    this.id,
    this.hoten,
    this.email,
    this.matkhau,
    this.chuyennganh,
    this.avt,
  });

  // ✅ Chuyển từ Map (Supabase / JSON) sang đối tượng SinhVien
  factory SinhVien.fromMap(Map<String, dynamic> map) {
    return SinhVien(
      id: map['id'],
      hoten: map['hoten'],
      email: map['email'],
      matkhau: map['matkhau'],
      chuyennganh: map['chuyennganh'],
      avt: map['avt'],
    );
  }

  // ✅ Chuyển từ đối tượng SinhVien sang Map để insert/update
  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'hoten': hoten,
      'email': email,
      'matkhau': matkhau,
      'chuyennganh': chuyennganh,
      'avt': avt,
    };
  }

  // ✅ Sao chép đối tượng có chỉnh sửa (copyWith)
  SinhVien copyWith({
    int? id,
    String? hoten,
    String? email,
    String? matkhau,
    String? chuyennganh,
    String? avt,
  }) {
    return SinhVien(
      id: id ?? this.id,
      hoten: hoten ?? this.hoten,
      email: email ?? this.email,
      matkhau: matkhau ?? this.matkhau,
      chuyennganh: chuyennganh ?? this.chuyennganh,
      avt: avt ?? this.avt,
    );
  }
}
