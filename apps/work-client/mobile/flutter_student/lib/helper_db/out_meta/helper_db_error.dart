import 'package:sqflite/sqflite.dart';
import 'package:path/path.dart';
import 'package:learn2earn/models/outmeta/doanh_nghiep.dart';
import 'package:learn2earn/models/outmeta/NganhNghe.dart';

class HelperDB {
  // 🔹 Singleton pattern (chỉ có 1 instance duy nhất)
  static final HelperDB instance = HelperDB._init();
  static Database? _database;

  HelperDB._init();

  // 🔹 Getter database: chỉ mở khi cần, tái sử dụng nếu đã mở
  Future<Database> get database async {
    if (_database != null) return _database!;
    _database = await _initDB('doanhnghiep.db');
    return _database!;
  }

  // 🔹 Khởi tạo DB
  Future<Database> _initDB(String filePath) async {
    final dbPath = await getDatabasesPath();
    final path = join(dbPath, filePath);

    return await openDatabase(path, version: 1, onCreate: _createDB);
  }

  // 🔹 Tạo bảng (vì chỉ lưu 1 dòng nên không cần id tự tăng)
  Future<void> _createDB(Database db, int version) async {
    await db.execute('''
    CREATE TABLE doanhnghiep (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      hoten TEXT,
      email TEXT,
      matkhau TEXT,
      diachi TEXT,
      sodienthoai INTEGER
    )
  ''');

    await db.execute('''
    CREATE TABLE bannganh (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      nganh TEXT NULL
    )
  ''');
  }

  // ============================================================
  // 🧠 Dưới đây là các hàm CRUD được tối ưu cho bảng 1 hàng duy nhất
  // ============================================================

  /// 🟢 Ghi đè hoặc tạo mới doanh nghiệp (chỉ giữ 1 hàng duy nhất)
  Future<void> saveDoanhNghiep(DoanhNghiep dn) async {
    final db = await instance.database;
    await db.insert(
      'doanhnghiep',
      dn.toMap(),
      conflictAlgorithm: ConflictAlgorithm.replace, // ghi đè dữ liệu cũ
    );
    print("Đã lưu doanh nghiệp");
    print(dn.toMap());
  }

  //save nganh
  Future<void> saveNganh(List<Nganh> Nganh_nghe) async {
    final db = await instance.database;
    for (var nganh in Nganh_nghe) {
      await db.insert(
        'bannganh',
        nganh.toMap(),
        conflictAlgorithm: ConflictAlgorithm.replace,
      );
    }
  }

  //lay chuyen nganh
  Future<List<String>> getNganh() async {
    final db = await instance.database;
    final result = await db.query('bannganh');
    return result.map((e) => e['nganh'] as String).toList();
  }

  /// 🟢 Lấy thông tin doanh nghiệp (dòng duy nhất)
  Future<DoanhNghiep?> getDoanhNghiep() async {
    final db = await instance.database;
    final result = await db.query('doanhnghiep', limit: 1);
    return result.isNotEmpty ? DoanhNghiep.fromMap(result.first) : null;
  }

  // Lấy tên người đăng nhập đầu tiên trong bảng doanhnghiep
  Future<String?> getNameDN() async {
    final db = await instance.database;
    final result = await db.query('doanhnghiep', columns: ['hoten'], limit: 1);

    if (result.isNotEmpty) {
      return result.first['hoten'] as String;
    } else {
      return null; // nếu chưa có ai đăng nhập
    }
  }

  /// 🟢 Lấy riêng Email & Mật khẩu (nếu cần)
  Future<Map<String, dynamic>?> getDangNhap() async {
    final db = await instance.database;
    final result = await db.query(
      'doanhnghiep',
      columns: ['Email', 'MatKhau'],
      limit: 1,
    );

    if (result.isEmpty) return null;
    return result.first;
  }

  Future<int> getID() async {
    final db = await instance.database;
    final result = await db.query('doanhnghiep', columns: ['id'], limit: 1);
    return result.first['id'] as int;
  }

  /// 🟢 Xoá toàn bộ dữ liệu (reset bảng)
  Future<void> clearDoanhNghiep() async {
    final db = await instance.database;
    await db.delete('doanhnghiep');
  }

  /// 🟢 Đóng kết nối DB (khi app tắt)
  Future<void> close() async {
    final db = _database;
    if (db != null) {
      await db.close();
      _database = null;
    }
  }
}
