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
      id: map['id'] as int,
      sinhVienId: map['sinhvien_id'] as int,
      doanhNghiepId: map['doanhnghiep_id'] as int,
      createdAt:
      map['created_at'] != null ? DateTime.parse(map['created_at']) : null,
    );
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
