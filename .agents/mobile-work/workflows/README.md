# Mobile workflow

Trước mọi task, xác định `primary_task_type`, chạy
`scripts/select-worklogs.mjs --type <primary_task_type> --limit 3`, đọc các log
được chọn và ghi `PRIOR_WORKLOG_REVIEW` trước khi inspect sâu.

Trước edit: đọc `.agents/project/design.md`, chọn đúng flavor, trace `view -> controller -> helper/model ->
Neon hoặc SQLite`, kiểm tra external HTTP call và platform impact. Giữ nguyên
package name `study2work_mobile`, public helper signature, model mapping và
MaterialPageRoute flow nếu task không yêu cầu đổi contract.

Với authoring/review Mobile module DD, dùng workflow `docs-dd-mobile` và skill
`create-dd-from-bd-mobile` từ `.agents/context-manifest.json`. Đọc BD/BRD,
references/INDEX, template và source evidence trước khi viết; không chuyển DD
Mobile thành API DD hoặc runtime implementation.

Sau edit, kiểm tra feature-specific `flutter analyze`/`flutter test`. Hai bộ
`neon_test.dart` xác minh URL/row/model normalization và chat polling; hai bộ
`neon_connection_test.dart` chỉ chạy khi truyền `--dart-define=RUN_NEON_SMOKE=true`.
Không chạy smoke mạng mặc định và không log credential/row nhạy cảm.

Build matrix cho Android dùng cùng root project:

```bash
flutter build apk --flavor student
flutter build apk --flavor business
flutter build appbundle --flavor student
flutter build appbundle --flavor business
```

Với UI-only change, kiểm tra Android/iOS portrait, keyboard/IME, scroll,
loading/empty/error, snackbar/dialog, text overflow, semantic labels và touch
target tối thiểu 44px. Không biến state cục bộ của static screen thành
persistence/backend behavior.

Mọi task phải dùng `.agents/worklog/TEMPLATE.md`, ghi source trace và status
verification trước khi cập nhật context; sau đó chạy context validator.

## Context inventory workflow

Khi source mobile thay đổi:

1. Đối chiếu `git ls-files apps/work-client/mobile` với
   [`file-inventory.md`](../file-inventory.md); không đưa `build/`, `.dart_tool/`
   hoặc cache vào inventory.
2. Cập nhật đúng role page và `data-flow.md` nếu route, helper, model, DB table,
   external call hoặc wiring thay đổi.
3. Giữ `EXPECTED_BEHAVIOR` tách khỏi `CURRENT_BEHAVIOR`; ghi discrepancy,
   unwired và placeholder bằng evidence từ source.
4. Chạy `git diff --check` và `node scripts/validate-agent-context.mjs`.
   Nếu Flutter/Dart/Node không có trong môi trường, ghi
   `DECLARED_NOT_RUNNABLE`, không đánh dấu `VERIFIED`.
