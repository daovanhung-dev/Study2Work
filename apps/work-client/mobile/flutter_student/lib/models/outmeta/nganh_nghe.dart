class Nganh {
  final String tenNganh;

  Nganh({
    required this.tenNganh,
  });

  // Tạo từ Map (JSON)
  factory Nganh.fromMap(Map<String, dynamic> map) {
    return Nganh(
      tenNganh: map['Nganh'] ?? '',
    );
  }

  // Chuyển sang Map (JSON)
  Map<String, dynamic> toMap() {
    return {
      'Nganh': tenNganh,
    };
  }
}
