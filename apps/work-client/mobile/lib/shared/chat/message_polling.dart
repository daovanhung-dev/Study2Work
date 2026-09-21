import 'dart:async';

Timer startMessagePollingWithLoader({
  required Future<List<Map<String, dynamic>>> Function() fetch,
  required void Function(Map<String, dynamic>) onMessage,
  Duration interval = const Duration(seconds: 3),
}) {
  final seenIds = <int>{};
  var initialized = false;
  var running = false;

  Future<void> poll() async {
    if (running) return;
    running = true;
    try {
      final rows = await fetch();
      for (final row in rows) {
        final id = int.tryParse(row['id']?.toString() ?? '');
        if (id == null) continue;
        if (!initialized) {
          seenIds.add(id);
        } else if (seenIds.add(id)) {
          onMessage(row);
        }
      }
      initialized = true;
    } finally {
      running = false;
    }
  }

  final timer = Timer.periodic(interval, (_) => poll());
  unawaited(poll());
  return timer;
}
