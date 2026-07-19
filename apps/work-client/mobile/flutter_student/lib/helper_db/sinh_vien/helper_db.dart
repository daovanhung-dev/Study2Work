import 'dart:async';
import 'package:sqflite/sqflite.dart';
import 'package:path/path.dart';
import 'package:learn2earn/models/sinh_vien/sinh_vien.dart';
import 'package:learn2earn/models/sinh_vien/NganhNghe.dart';

class SinhVienSQLiteHelper {
  static final SinhVienSQLiteHelper instance = SinhVienSQLiteHelper._init();
  static Database? _database;

  SinhVienSQLiteHelper._init();

  Future<Database> get database async {
    if (_database != null) return _database!;
    _database = await _initDB('sinhvien.db');
    return _database!;
  }

  // 🏗️ Tạo database
  Future<Database> _initDB(String filePath) async {
    final dbPath = await getDatabasesPath();
    final path = join(dbPath, filePath);

    return await openDatabase(path, version: 1, onCreate: _createDB);
  }

  // 📦 Tạo bảng sinhvien
  Future<void> _createDB(Database db, int version) async {
    await db.execute('''
    CREATE TABLE sinhvien (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  hoten TEXT,
  email TEXT,
  matkhau TEXT,
  chuyennganh TEXT,
  avt TEXT
);

  ''');

    await db.execute('''
    CREATE TABLE bannganh (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      nganh TEXT NULL
    )
  ''');
  }

  Future<int> insertSinhVien(SinhVien sv) async {
    final db = await instance.database;

    // Xóa hết dữ liệu cũ
    await db.delete('sinhvien');

    print('🟢 Đã xóa dữ liệu cũ, thêm sinh viên mới');
    // Thêm sinh viên mới
    return await db.insert(
      'sinhvien',
      sv.toMap(),
    );
  }


  // 🟡 Cập nhật sinh viên
  Future<int> updateSinhVien(SinhVien sv) async {
    final db = await instance.database;
    if (sv.id == null) return 0;
    return await db.update(
      'sinhvien',
      sv.toMap(),
      where: 'id = ?',
      whereArgs: [sv.id],
    );
  }

  // 🔴 Xóa sinh viên
  Future<int> deleteSinhVien() async {
    final db = await instance.database;
    return await db.delete('sinhvien');
  }

  // 📋 Lấy sinh viên
  Future<SinhVien> getSinhVien() async {
    final db = await instance.database;
    final result = await db.query('sinhvien');
    if (result.isNotEmpty) {
      return SinhVien.fromMap(result.first);
    }
    return SinhVien();
  }

  // 🔍 Lấy 1 sinh viên theo email
  Future<SinhVien?> getByEmail(String email) async {
    final db = await instance.database;
    final result = await db.query(
      'sinhvien',
      where: 'email = ?',
      whereArgs: [email],
    );
    if (result.isNotEmpty) {
      return SinhVien.fromMap(result.first);
    }
    return null;
  }

  // 🔐 Kiểm tra đăng nhập (email + mật khẩu)
  Future<SinhVien?> login(String email, String matkhau) async {
    final db = await instance.database;
    final result = await db.query(
      'sinhvien',
      where: 'email = ? AND matkhau = ?',
      whereArgs: [email, matkhau],
    );
    if (result.isNotEmpty) {
      return SinhVien.fromMap(result.first);
    }
    return null;
  }

  //kiem tra da dang nhap chua
  Future<Map<String, dynamic>?> getDangNhap() async {
    final db = await instance.database;
    final result = await db.query(
      'sinhvien',
      columns: ['Email', 'MatKhau'],
      limit: 1,
    );

    if (result.isEmpty) return null;
    return result.first;
  }

  // 🧹 Đóng kết nối DB
  Future close() async {
    final db = await instance.database;
    db.close();
  }

  //luu ds nganh nghe
  Future<void> saveNganh(List<Nganh> dsNganh) async {
    final db = await instance.database;
    final batch = db.batch(); // dùng batch để tăng tốc độ ghi

    for (var nganh in dsNganh) {
      batch.insert(
        'bannganh',
        nganh.toMap(),
        conflictAlgorithm: ConflictAlgorithm.replace,
      );
    }

    await batch.commit(noResult: true);
  }

  //get id
  Future<int> getID() async {
    final db = await instance.database;
    final result = await db.query(
      'sinhvien',
      columns: ['id'],
      limit: 1,
    );

    if (result.isNotEmpty) {
      return result.first['id'] as int;
    } else {
      return 0; // hoặc 0 nếu bạn muốn mặc định
    }
  }
  /// 🔑 Kiểm tra xem đã đăng nhập chưa
  /// Nếu bảng 'sinhvien' có dữ liệu, trả về true
  Future<bool> isLoggedIn() async {
    final db = await instance.database;
    final result = await db.query(
      'sinhvien',
      columns: ['id'], // chỉ cần kiểm tra có row hay không
      limit: 1,
    );

    return result.isNotEmpty;
  }
  /// Lưu email + mật khẩu vào SQLite (overwrite sinh viên hiện tại)
  Future<void> saveDangNhap(String email, String matkhau) async {
    final sv = SinhVien(
      hoten: null,
      email: email,
      matkhau: matkhau,
      chuyennganh: null,
      avt: null,
    );
    await insertSinhVien(sv);
  }
}
