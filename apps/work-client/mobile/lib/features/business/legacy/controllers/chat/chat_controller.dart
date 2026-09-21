import 'dart:async';

import 'package:work_server/helper_db/neon_db.dart';

final NeonDatabase database = NeonDatabase.instance;

Future<List<Map<String, dynamic>>> getChat(
  int sinhvienId,
  int doanhnghiepId,
) async {
  return database.query(
    '''
    SELECT "id", "nguoigui", "nguoinhan", "noidung", "ngaygui", "trangthai",
           "sinhvien_id", "doanhnghiep_id"
    FROM "Chat"
    WHERE "sinhvien_id" = \$1 AND "doanhnghiep_id" = \$2
    ORDER BY "ngaygui" ASC NULLS LAST, "id" ASC
  ''',
    parameters: [sinhvienId, doanhnghiepId],
  );
}

Future<void> guiTinNhan(
  int sinhvienId,
  int doanhnghiepId,
  String noidung,
) async {
  await database.execute(
    '''
    INSERT INTO "Chat" (
      "sinhvien_id", "doanhnghiep_id", "nguoigui", "nguoinhan", "noidung", "ngaygui"
    ) VALUES (\$1, \$2, \$3, \$4, \$5, \$6)
  ''',
    parameters: [
      sinhvienId,
      doanhnghiepId,
      doanhnghiepId.toString(),
      sinhvienId.toString(),
      noidung,
      DateTime.now().toUtc(),
    ],
  );
}

Timer startMessagePolling({
  required int sinhvienId,
  required int doanhnghiepId,
  required void Function(Map<String, dynamic>) onMessage,
  Duration interval = const Duration(seconds: 3),
}) {
  return startMessagePollingWithLoader(
    fetch: () => getChat(sinhvienId, doanhnghiepId),
    onMessage: onMessage,
    interval: interval,
  );
}

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
