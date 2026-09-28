import 'package:flutter_test/flutter_test.dart';

import 'package:study2work_mobile/app/config/app_config.dart';
import 'package:study2work_mobile/shared/models/chat_message.dart';

void main() {
  test('maps Android flavors to role-specific app configuration', () {
    final student = AppConfig.fromFlavor('student');
    final business = AppConfig.fromFlavor('business');

    expect(student.isStudent, isTrue);
    expect(student.rolePath, '/student');
    expect(student.sqliteDatabaseName, 'sinhvien.db');
    expect(student.applicationId, 'com.s2w.work.students');

    expect(business.isBusiness, isTrue);
    expect(business.rolePath, '/business');
    expect(business.sqliteDatabaseName, 'doanhnghiep.db');
    expect(business.applicationId, 'com.s2w.work.business');
  });

  test('keeps chat row normalization in the shared model', () {
    final message = ChatMessage.fromMap({
      'id': 42,
      'nguoigui': '7',
      'nguoinhan': 8,
      'noidung': 'hello',
      'ngaygui': '2026-01-02T03:04:05.000Z',
      'trangthai': 'sent',
    });

    expect(message.id, 42);
    expect(message.senderId, 7);
    expect(message.receiverId, 8);
    expect(message.content, 'hello');
    expect(message.status, 'sent');
    expect(message.sentAt, DateTime.utc(2026, 1, 2, 3, 4, 5));
  });
}
