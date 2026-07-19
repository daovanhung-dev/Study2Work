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

  /// Chuyển từ Map (dữ liệu lấy từ Supabase/PostgreSQL) sang Object
  factory DoanChat.fromMap(Map<String, dynamic> map) {
    return DoanChat(
      id: map['id'] as int?,
      sinhvienId: map['sinhvien_id'] as int,
      doanhnghiepId: map['doanhnghiep_id'] as int,
      createdAt: map['created_at'] != null
          ? DateTime.parse(map['created_at'])
          : null,
    );
  }

  /// Chuyển từ Object sang Map (để insert/update vào Supabase)
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
