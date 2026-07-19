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

  /// Chuyển từ Map (dữ liệu lấy từ Supabase) sang Object
  factory Chat.fromMap(Map<String, dynamic> map) {
    return Chat(
      id: map['id'] as int?,
      sinhvienId: map['sinhvien_id'] as int?,
      doanhnghiepId: map['doanhnghiep_id'] as int?,
      nguoiGui: map['nguoigui'] as String?,
      nguoiNhan: map['nguoinhan'] as String?,
      noiDung: map['noidung'] as String?,
      ngayGui: map['ngaygui'] != null ? DateTime.parse(map['ngaygui']) : null,
      trangThai: map['trangthai'] as bool?,
    );

  }

  /// Chuyển từ Object sang Map (để insert/update vào Supabase)
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
