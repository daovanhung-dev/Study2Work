import 'package:supabase_flutter/supabase_flutter.dart';

final supabase = Supabase.instance.client;

Future<Map<String, dynamic>> xemChiTiet(int id) async {
  final response = await supabase
      .from('cv')
      .select('''
        id,
        avt,
        hoten,
        ngaysinh,
        gioitinh,
        email,
        sdt,
        diachi,
        vitri,
        nganh,
        muctieunghiep,
        hocvan,
        kinhnghiem,
        kynang,
        ngoaingu,
        chungchi,
        duan,
        giaithuong,
        hoatdong,
        social,
        portfolio,
        luongmongmuon
      ''')
      .eq('id', id)
      .maybeSingle();

  if (response == null) {
    return {}; // không tìm thấy dữ liệu
  }

  return {
    'id': response['id'] ?? 0,
    'avt': response['avt'] ?? "",
    'hoten': response['hoten'] ?? "",
    'ngaysinh': response['ngaysinh'] ?? "",
    'gioitinh': response['gioitinh'] ?? "",
    'email': response['email'] ?? "",
    'sdt': response['sdt'] ?? "",
    'diachi': response['diachi'] ?? "",
    'vitri': response['vitri'] ?? "",
    'nganh': response['nganh'] ?? "",
    'muctieunghiep': response['muctieunghiep'] ?? "",
    'hocvan': response['hocvan'] ?? "",
    'kinhnghiem': response['kinhnghiem'] ?? "",
    'kynang': response['kynang'] ?? "",
    'ngoaingu': response['ngoaingu'] ?? "",
    'chungchi': response['chungchi'] ?? "",
    'duan': response['duan'] ?? "",
    'giaithuong': response['giaithuong'] ?? "",
    'hoatdong': response['hoatdong'] ?? "",
    'social': response['social'] ?? "",
    'portfolio': response['portfolio'] ?? "",
    'luongmongmuon': response['luongmongmuon'] ?? "",
  };
}
