import 'package:flutter_test/flutter_test.dart';
import 'package:study2work_mobile/core/data/neon/neon_client.dart';

void main() {
  const runSmoke = bool.fromEnvironment('RUN_NEON_SMOKE');

  test('Neon driver smoke test executes SELECT 1', () async {
    final database = NeonDatabase.instance;
    await database.initialize();
    await database.close();
  }, skip: runSmoke ? false : 'Pass --dart-define=RUN_NEON_SMOKE=true to run.');
}
