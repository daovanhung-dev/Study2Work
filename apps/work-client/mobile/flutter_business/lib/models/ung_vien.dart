class UngVien {
  final int? id;
  final DateTime? createdAt;
  final int? sinhvienId;
  final int? doanhnghiepId;
  final String? trangthai;

  UngVien({
    this.id,
    this.createdAt,
    this.sinhvienId,
    this.doanhnghiepId,
    this.trangthai,
  });

  // Chuyển từ Map (dữ liệu lấy từ DB hoặc API) sang Object
  factory UngVien.fromMap(Map<String, dynamic> map) {
    return UngVien(
      id: map['id'],
      createdAt: map['created_at'] != null
          ? DateTime.parse(map['created_at'])
          : null,
      sinhvienId: map['sinhvien_id'],
      doanhnghiepId: map['doanhnghiep_id'],
      trangthai: map['trangthai'],
    );
  }

  // Chuyển từ Object sang Map (để insert/update)
  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'created_at': createdAt?.toIso8601String(),
      'sinhvien_id': sinhvienId,
      'doanhnghiep_id': doanhnghiepId,
      'trangthai': trangthai,
    };
  }
}
