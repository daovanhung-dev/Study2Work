class Chat {
  final int? id;
  final int? sinhvienId;
  final int? doanhnghiepId;
  final String? nguoiGui;
  final String? nguoiNhan;
  final String? noiDung;
  final DateTime? ngayGui;
  final bool? trangThai;

  Chat({
    this.id,
    this.sinhvienId,
    this.doanhnghiepId,
    this.nguoiGui,
    this.nguoiNhan,
    this.noiDung,
    this.ngayGui,
    this.trangThai,
  });

  /// Chuyển từ Map (dữ liệu lấy từ PostgreSQL) sang Object.
  factory Chat.fromMap(Map<String, dynamic> map) {
    return Chat(
      id: _toInt(map['id']),
      sinhvienId: _toInt(map['sinhvien_id']),
      doanhnghiepId: _toInt(map['doanhnghiep_id']),
      nguoiGui: map['nguoigui'] as String?,
      nguoiNhan: map['nguoinhan'] as String?,
      noiDung: map['noidung'] as String?,
      ngayGui: _toDateTime(map['ngaygui']),
      trangThai: map['trangthai'] as bool?,
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
      'nguoigui': nguoiGui,
      'nguoinhan': nguoiNhan,
      'noidung': noiDung,
      'ngaygui': ngayGui?.toIso8601String(),
      'trangthai': trangThai,
    };
  }

  /// Hàm copy để cập nhật một số trường
  Chat copyWith({
    int? id,
    int? sinhvienId,
    int? doanhnghiepId,
    String? nguoiGui,
    String? nguoiNhan,
    String? noiDung,
    DateTime? ngayGui,
    bool? trangThai,
  }) {
    return Chat(
      id: id ?? this.id,
      sinhvienId: sinhvienId ?? this.sinhvienId,
      doanhnghiepId: doanhnghiepId ?? this.doanhnghiepId,
      nguoiGui: nguoiGui ?? this.nguoiGui,
      nguoiNhan: nguoiNhan ?? this.nguoiNhan,
      noiDung: noiDung ?? this.noiDung,
      ngayGui: ngayGui ?? this.ngayGui,
      trangThai: trangThai ?? this.trangThai,
    );
  }
}
