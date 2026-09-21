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
      id: _toInt(map['id']),
      createdAt: _toDateTime(map['created_at']),
      sinhvienId: _toInt(map['sinhvien_id']),
      doanhnghiepId: _toInt(map['doanhnghiep_id']),
      trangthai: map['trangthai']?.toString(),
    );
  }

  static int? _toInt(dynamic value) {
    if (value == null) return null;
    if (value is int) return value;
    return int.tryParse(value.toString());
  }

  static DateTime? _toDateTime(dynamic value) {
    if (value is DateTime) return value;
    if (value == null) return null;
    return DateTime.tryParse(value.toString());
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
