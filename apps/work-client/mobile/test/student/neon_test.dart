import 'package:flutter_test/flutter_test.dart';
import 'package:study2work_mobile/features/student/legacy/controllers/chat/chat_controller.dart';
import 'package:study2work_mobile/core/data/neon/neon_client.dart';
import 'package:study2work_mobile/features/student/legacy/models/sinh_vien/cv.dart';

void main() {
  test('normalizes Neon URL and PostgreSQL row values', () {
    const source =
        'postgresql://user:password@example.test/db?sslmode=require&channel_binding=require';
    final normalized = neonDriverUrl(source);
    final uri = Uri.parse(normalized);

    expect(uri.queryParameters['sslmode'], 'require');
    expect(uri.queryParameters['channel_binding'], isNull);
    expect(uri.queryParameters['max_connection_count'], '1');
    expect(uri.queryParameters['connect_timeout'], '20');

    final timestamp = DateTime.utc(2026, 1, 2, 3, 4, 5);
    final row = normalizeNeonRow({
      'id': BigInt.from(42),
      'created_at': timestamp,
      'nullable': null,
      'social': {'github': 'user'},
    });
    expect(row['id'], 42);
    expect(row['created_at'], timestamp);
    expect(row['nullable'], isNull);
    expect(row['social'], {'github': 'user'});

    final cv = CV.fromMap({
      'id': row['id'],
      'hoten': 'Student',
      'email': 'student@example.test',
      'ngaysinh': row['created_at'],
      'social': '{"github":"user"}',
    });
    expect(cv.id, 42);
    expect(cv.ngaysinh, timestamp);
    expect(cv.social?['github'], 'user');

    expect(
      () => neonDriverUrl(
        'postgresql://user:password@example.test/db?sslmode=disable',
      ),
      throwsArgumentError,
    );
  });

  test('polling emits only new ids and stops after cancellation', () async {
    var rows = <Map<String, dynamic>>[
      {'id': 1},
    ];
    final received = <int>[];
    final timer = startMessagePollingWithLoader(
      fetch: () async => List<Map<String, dynamic>>.of(rows),
      interval: const Duration(milliseconds: 10),
      onMessage: (row) => received.add(row['id'] as int),
    );

    await Future<void>.delayed(const Duration(milliseconds: 35));
    rows = [
      {'id': 1},
      {'id': 2},
      {'id': 2},
    ];
    await Future<void>.delayed(const Duration(milliseconds: 35));
    timer.cancel();
    rows.add({'id': 3});
    await Future<void>.delayed(const Duration(milliseconds: 25));

    expect(received, [2]);
  });
}
