import 'package:supabase_flutter/supabase_flutter.dart';

final supabase = Supabase.instance.client;
Future<List<Map<String, dynamic>>> getTopCV() async {
  List<Map<String,dynamic>> ds = [];
  try {
    // Lấy danh sách id từ topcv
    final idsResponse = await supabase.from('topcv').select('id');

    final List<int> idList = idsResponse.map<int>((row) => row['id'] as int).toList();

    if (idList.isEmpty) return ds; // trả về danh sách rỗng

    // Query tất cả CV theo idList
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
          kynang
        ''')
        .inFilter('id', idList);

    // Thêm dữ liệu vào ds
    for (var row in response) {
      ds.add({
        'id': row['id'],
        'avt': row['avt'],
        'vitri': row['vitri'],
        'hoten': row['hoten'],
        'ngaysinh': row['ngaysinh'],
        'gioitinh': row['gioitinh'],
        'email': row['email'],
        'sdt': row['sdt'],
        'diachi': row['diachi'],
        'nganh': row['nganh'],
        'muctieunghiep': row['muctieunghiep'],
        'hocvan': row['hocvan'],
        'kinhnghiem': row['kinhnghiem'],
        'kynang': row['kynang'],
      });
    }
  } catch (e) {
    print("Lỗi khi lấy dữ liệu CV: $e");
  }

  return ds; // ✅ trả về danh sách CV
}
