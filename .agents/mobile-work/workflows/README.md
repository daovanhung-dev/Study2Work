# Mobile workflow

Trước edit: chọn đúng Flutter app, trace `view -> controller -> helper/model ->
Neon hoặc SQLite`, kiểm tra external HTTP call và platform impact. Giữ nguyên
package name `work_server`, public helper signature, model mapping và
MaterialPageRoute flow nếu task không yêu cầu đổi contract.

Sau edit, kiểm tra feature-specific `flutter analyze`/`flutter test`. Hai bộ
`neon_test.dart` xác minh URL/row/model normalization và chat polling; hai bộ
`neon_connection_test.dart` chỉ chạy khi truyền `--dart-define=RUN_NEON_SMOKE=true`.
Không chạy smoke mạng mặc định và không log credential/row nhạy cảm.
