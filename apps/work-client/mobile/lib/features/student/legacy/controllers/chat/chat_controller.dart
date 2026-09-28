import 'dart:async';

import 'package:study2work_mobile/core/data/neon/neon_client.dart';
import 'package:study2work_mobile/shared/chat/message_polling.dart';

export 'package:study2work_mobile/shared/chat/message_polling.dart'
    show startMessagePollingWithLoader;

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
      sinhvienId.toString(),
      doanhnghiepId.toString(),
      sinhvienId,
      doanhnghiepId,
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
