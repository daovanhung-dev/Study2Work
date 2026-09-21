import 'package:postgres/postgres.dart';

import 'package:work_server/constants.dart';

/// Converts the Neon connection string to the subset understood by the Dart
/// driver. The source constant intentionally remains the exact value supplied
/// for the application configuration.
String neonDriverUrl(String connectionString) {
  final uri = Uri.parse(connectionString);
  final sslMode = uri.queryParameters['sslmode'];
  if (sslMode != 'require' &&
      sslMode != 'verify-ca' &&
      sslMode != 'verify-full') {
    throw ArgumentError('Neon connections must require SSL.');
  }
  final parameters = Map<String, String>.from(uri.queryParameters)
    ..remove('channel_binding')
    ..putIfAbsent('max_connection_count', () => '1')
    ..putIfAbsent('connect_timeout', () => '20');
  return uri.replace(queryParameters: parameters).toString();
}

Map<String, dynamic> normalizeNeonRow(Map<String, dynamic> row) {
  return row.map(
    (key, value) => MapEntry(key, value is BigInt ? value.toInt() : value),
  );
}

class NeonDatabase {
  NeonDatabase._();

  static final NeonDatabase instance = NeonDatabase._();

  Pool? _pool;

  Pool get _client => _pool ??= Pool.withUrl(neonDriverUrl(NEON_POOLER_URL));

  Future<void> initialize() async {
    await _client.execute('SELECT 1', ignoreRows: true);
  }

  Future<List<Map<String, dynamic>>> query(
    String sql, {
    List<Object?> parameters = const [],
  }) async {
    final result = await _client.execute(sql, parameters: parameters);
    return result
        .map((row) => normalizeNeonRow(row.toColumnMap()))
        .toList(growable: false);
  }

  Future<int> execute(String sql, {List<Object?> parameters = const []}) async {
    final result = await _client.execute(
      sql,
      parameters: parameters,
      ignoreRows: true,
    );
    return result.affectedRows;
  }

  Future<void> close() async {
    final pool = _pool;
    _pool = null;
    if (pool != null) await pool.close(force: true);
  }
}
