class DoanChat {
  final int? id;
  final int sinhvienId;
  final int doanhnghiepId;
  final DateTime? createdAt;

  DoanChat({
    this.id,
    required this.sinhvienId,
    required this.doanhnghiepId,
    this.createdAt,
  });

  /// Chuyển từ Map (dữ liệu lấy từ PostgreSQL) sang Object.
  factory DoanChat.fromMap(Map<String, dynamic> map) {
    return DoanChat(
      id: _toInt(map['id']),
      sinhvienId: _toInt(map['sinhvien_id']) ?? 0,
      doanhnghiepId: _toInt(map['doanhnghiep_id']) ?? 0,
      createdAt: _toDateTime(map['created_at']),
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

  /// Chuyển từ Object sang Map (để lưu vào PostgreSQL).
  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'sinhvien_id': sinhvienId,
      'doanhnghiep_id': doanhnghiepId,
      'created_at': createdAt?.toIso8601String(),
    };
  }

  /// Hàm copy để cập nhật một số trường
  DoanChat copyWith({
    int? id,
    int? sinhvienId,
    int? doanhnghiepId,
    DateTime? createdAt,
  }) {
    return DoanChat(
      id: id ?? this.id,
      sinhvienId: sinhvienId ?? this.sinhvienId,
      doanhnghiepId: doanhnghiepId ?? this.doanhnghiepId,
      createdAt: createdAt ?? this.createdAt,
    );
  }
}
