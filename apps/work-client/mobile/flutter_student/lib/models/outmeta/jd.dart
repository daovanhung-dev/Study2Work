class JD {
  final int id;
  final String tenViTri;
  final String capBac;
  final String baoCaoCho;
  final String nhiemVu;
  final String trinhDo;
  final String kinhNghiem;
  final String kyNang;
  final String kyNangMem;
  final String uuTien;
  final String mucLuong;
  final String phucLoi;
  final String moiTruong;
  final String diaDiem;
  final String thoiGian;
  final String hanNop;
  final String cachUngTuyen;
  final String moTa;

  JD({
    required this.id,
    required this.tenViTri,
    required this.capBac,
    required this.baoCaoCho,
    required this.nhiemVu,
    required this.trinhDo,
    required this.kinhNghiem,
    required this.kyNang,
    required this.kyNangMem,
    required this.uuTien,
    required this.mucLuong,
    required this.phucLoi,
    required this.moiTruong,
    required this.diaDiem,
    required this.thoiGian,
    required this.hanNop,
    required this.cachUngTuyen,
    required this.moTa,
  });

  // Convert từ Object -> Map (SQLite / Supabase)
  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'ten_vi_tri': tenViTri,
      'cap_bac': capBac,
      'bao_cao_cho': baoCaoCho,
      'nhiem_vu': nhiemVu,
      'trinh_do': trinhDo,
      'kinh_nghiem': kinhNghiem,
      'ky_nang': kyNang,
      'ky_nang_mem': kyNangMem,
      'uu_tien': uuTien,
      'muc_luong': mucLuong,
      'phuc_loi': phucLoi,
      'moi_truong': moiTruong,
      'dia_diem': diaDiem,
      'thoi_gian': thoiGian,
      'han_nop': hanNop,
      'cach_ung_tuyen': cachUngTuyen,
      'mo_ta': moTa,
    };
  }

  // Convert từ Map -> Object
  factory JD.fromMap(Map<String, dynamic> map) {
    // Hàm helper để parse int an toàn
    int parseIntSafe(dynamic value, [int defaultValue = 0]) {
      if (value == null) return defaultValue;
      if (value is int) return value;
      return int.tryParse(value.toString()) ?? defaultValue;
    }

    return JD(
      id: parseIntSafe(map['id']), // id mặc định 0 nếu null hoặc parse fail
      tenViTri: map['ten_vi_tri']?.toString() ?? '',
      capBac: map['cap_bac']?.toString() ?? '',
      baoCaoCho: map['bao_cao_cho']?.toString() ?? '',
      nhiemVu: map['nhiem_vu']?.toString() ?? '',
      trinhDo: map['trinh_do']?.toString() ?? '',
      kinhNghiem: map['kinh_nghiem']?.toString() ?? '',
      kyNang: map['ky_nang']?.toString() ?? '',
      kyNangMem: map['ky_nang_mem']?.toString() ?? '',
      uuTien: map['uu_tien']?.toString() ?? '',
      mucLuong: map['muc_luong']?.toString() ?? '',
      phucLoi: map['phuc_loi']?.toString() ?? '',
      moiTruong: map['moi_truong']?.toString() ?? '',
      diaDiem: map['dia_diem']?.toString() ?? '',
      thoiGian: map['thoi_gian']?.toString() ?? '',
      hanNop: map['han_nop']?.toString() ?? '',
      cachUngTuyen: map['cach_ung_tuyen']?.toString() ?? '',
      moTa: map['mo_ta']?.toString() ?? '',
    );
  }

}
