class DoanChat {
  final int id;
  final int sinhVienId;
  final int doanhNghiepId;
  final DateTime? createdAt;

  DoanChat({
    required this.id,
    required this.sinhVienId,
    required this.doanhNghiepId,
    this.createdAt,
  });

  // 🧩 Tạo instance từ Map (JSON -> Object)
  factory DoanChat.fromMap(Map<String, dynamic> map) {
    return DoanChat(
      id: _toInt(map['id']) ?? 0,
      sinhVienId: _toInt(map['sinhvien_id']) ?? 0,
      doanhNghiepId: _toInt(map['doanhnghiep_id']) ?? 0,
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

  // 🔁 Chuyển Object -> Map (để insert/update)
  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'sinhvien_id': sinhVienId,
      'doanhnghiep_id': doanhNghiepId,
      'created_at': createdAt?.toIso8601String(),
    };
  }

  // ✨ Hỗ trợ copy nhanh
  DoanChat copyWith({
    int? id,
    int? sinhVienId,
    int? doanhNghiepId,
    DateTime? createdAt,
  }) {
    return DoanChat(
      id: id ?? this.id,
      sinhVienId: sinhVienId ?? this.sinhVienId,
      doanhNghiepId: doanhNghiepId ?? this.doanhNghiepId,
      createdAt: createdAt ?? this.createdAt,
    );
  }
}
