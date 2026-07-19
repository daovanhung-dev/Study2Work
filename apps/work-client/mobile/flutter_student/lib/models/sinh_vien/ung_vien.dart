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
      id: json['id'],
      createdAt: json['created_at'] != null ? DateTime.parse(json['created_at']) : null,
      sinhvienId: json['sinhvien_id'],
      doanhnghiepId: json['doanhnghiep_id'],
      jdId: json['jd_id'],
      trangthai: json['trangthai'],
    );
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