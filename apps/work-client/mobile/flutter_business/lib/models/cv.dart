// lib/models/cv.dart
import 'dart:convert';

class CV {
  final int? id;
  final String? avt;
  final String hoten; // not null in DB
  final DateTime? ngaysinh;
  final String? gioitinh;
  final String email; // not null in DB
  final String? sdt;
  final String? diachi;
  final String? vitri;
  final String? nganh;
  final String? muctieunghiep;
  final String? hocvan;
  final String? kinhnghiem;
  final String? kynang;
  final String? ngoaingu;
  final String? chungchi;
  final String? duan;
  final String? giaithuong;
  final String? hoatdong;
  final Map<String, dynamic>? social; // jsonb
  final String? portfolio;
  final String? luongmongmuon;
  final DateTime? createdAt;

  const CV({
    this.id,
    this.avt,
    required this.hoten,
    this.ngaysinh,
    this.gioitinh,
    required this.email,
    this.sdt,
    this.diachi,
    this.vitri,
    this.nganh,
    this.muctieunghiep,
    this.hocvan,
    this.kinhnghiem,
    this.kynang,
    this.ngoaingu,
    this.chungchi,
    this.duan,
    this.giaithuong,
    this.hoatdong,
    this.social,
    this.portfolio,
    this.luongmongmuon,
    this.createdAt,
  });

  CV copyWith({
    int? id,
    String? avt,
    String? hoten,
    DateTime? ngaysinh,
    String? gioitinh,
    String? email,
    String? sdt,
    String? diachi,
    String? vitri,
    String? nganh,
    String? muctieunghiep,
    String? hocvan,
    String? kinhnghiem,
    String? kynang,
    String? ngoaingu,
    String? chungchi,
    String? duan,
    String? giaithuong,
    String? hoatdong,
    Map<String, dynamic>? social,
    String? portfolio,
    String? luongmongmuon,
    DateTime? createdAt,
  }) {
    return CV(
      id: id ?? this.id,
      avt: avt ?? this.avt,
      hoten: hoten ?? this.hoten,
      ngaysinh: ngaysinh ?? this.ngaysinh,
      gioitinh: gioitinh ?? this.gioitinh,
      email: email ?? this.email,
      sdt: sdt ?? this.sdt,
      diachi: diachi ?? this.diachi,
      vitri: vitri ?? this.vitri,
      nganh: nganh ?? this.nganh,
      muctieunghiep: muctieunghiep ?? this.muctieunghiep,
      hocvan: hocvan ?? this.hocvan,
      kinhnghiem: kinhnghiem ?? this.kinhnghiem,
      kynang: kynang ?? this.kynang,
      ngoaingu: ngoaingu ?? this.ngoaingu,
      chungchi: chungchi ?? this.chungchi,
      duan: duan ?? this.duan,
      giaithuong: giaithuong ?? this.giaithuong,
      hoatdong: hoatdong ?? this.hoatdong,
      social: social ?? this.social,
      portfolio: portfolio ?? this.portfolio,
      luongmongmuon: luongmongmuon ?? this.luongmongmuon,
      createdAt: createdAt ?? this.createdAt,
    );
  }

  /// Chuyển từ Map (ví dụ từ JSON response hoặc row DB) sang model
  factory CV.fromMap(Map<String, dynamic> map) {
    // social có thể là Map hoặc JSON string từ DB driver
    Map<String, dynamic>? parseSocial(dynamic v) {
      if (v == null) return null;
      if (v is Map<String, dynamic>) return v;
      if (v is String) {
        try {
          final decoded = json.decode(v);
          if (decoded is Map<String, dynamic>) return decoded;
        } catch (_) {}
      }
      return null;
    }

    DateTime? parseDate(dynamic v) {
      if (v == null) return null;
      if (v is DateTime) return v;
      if (v is String) {
        try {
          return DateTime.parse(v);
        } catch (_) {
          return null;
        }
      }
      return null;
    }

    return CV(
      id: map['id'] is int ? map['id'] as int : (map['id'] is String ? int.tryParse(map['id']) : null),
      avt: map['avt'] as String?,
      hoten: (map['hoten'] ?? '') as String,
      ngaysinh: parseDate(map['ngaysinh']),
      gioitinh: map['gioitinh'] as String?,
      email: (map['email'] ?? '') as String,
      sdt: map['sdt'] as String?,
      diachi: map['diachi'] as String?,
      vitri: map['vitri'] as String?,
      nganh: map['nganh'] as String?,
      muctieunghiep: map['muctieunghiep'] as String?,
      hocvan: map['hocvan'] as String?,
      kinhnghiem: map['kinhnghiem'] as String?,
      kynang: map['kynang'] as String?,
      ngoaingu: map['ngoaingu'] as String?,
      chungchi: map['chungchi'] as String?,
      duan: map['duan'] as String?,
      giaithuong: map['giaithuong'] as String?,
      hoatdong: map['hoatdong'] as String?,
      social: parseSocial(map['social']),
      portfolio: map['portfolio'] as String?,
      luongmongmuon: map['luongmongmuon'] as String?,
      createdAt: parseDate(map['created_at'] ?? map['createdAt']),
    );
  }

  /// Chuyển model thành Map để gửi lên API / lưu DB
  Map<String, dynamic> toMap() {
    return {
      if (id != null) 'id': id,
      'avt': avt,
      'hoten': hoten,
      'ngaysinh': ngaysinh?.toIso8601String(),
      'gioitinh': gioitinh,
      'email': email,
      'sdt': sdt,
      'diachi': diachi,
      'vitri': vitri,
      'nganh': nganh,
      'muctieunghiep': muctieunghiep,
      'hocvan': hocvan,
      'kinhnghiem': kinhnghiem,
      'kynang': kynang,
      'ngoaingu': ngoaingu,
      'chungchi': chungchi,
      'duan': duan,
      'giaithuong': giaithuong,
      'hoatdong': hoatdong,
      'social': social == null ? null : json.encode(social), // encode để DB jsonb chấp nhận string nếu cần
      'portfolio': portfolio,
      'luongmongmuon': luongmongmuon,
      'created_at': createdAt?.toIso8601String(),
    };
  }

  String toJson() => json.encode(toMap());

  factory CV.fromJson(String source) {
    final Map<String, dynamic> map = json.decode(source);
    return CV.fromMap(map);
  }

  @override
  String toString() {
    return 'CV(id: $id, hoten: $hoten, email: $email, vitri: $vitri, nganh: $nganh)';
  }

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;
    return other is CV && other.id == id;
  }

  @override
  int get hashCode => id.hashCode;
}
