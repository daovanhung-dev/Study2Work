class UngVien {
  int? id;
  DateTime? createdAt;
  int? sinhvienId;
  int? doanhnghiepId;
  int? jdId;
  String? trangthai;

  UngVien({
    this.id,
    this.createdAt,
    this.sinhvienId,
    this.doanhnghiepId,
    this.jdId,
    this.trangthai = 'chưa ứng tuyển',
  });

  // Chuyển từ JSON sang object
  factory UngVien.fromJson(Map<String, dynamic> json) {
    return UngVien(
      id: _toInt(json['id']),
      createdAt: _toDateTime(json['created_at']),
      sinhvienId: _toInt(json['sinhvien_id']),
      doanhnghiepId: _toInt(json['doanhnghiep_id']),
      jdId: _toInt(json['jd_id']),
      trangthai: json['trangthai']?.toString(),
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

  // Chuyển object sang JSON
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'created_at': createdAt?.toIso8601String(),
      'sinhvien_id': sinhvienId,
      'doanhnghiep_id': doanhnghiepId,
      'jd_id': jdId,
      'trangthai': trangthai,
    };
  }
}
