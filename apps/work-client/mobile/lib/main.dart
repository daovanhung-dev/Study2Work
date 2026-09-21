import 'dart:io' show Platform;

import 'package:flutter/foundation.dart' show kIsWeb;
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:sqflite_common_ffi/sqflite_ffi.dart';

import 'package:study2work_mobile/app/app.dart';
import 'package:study2work_mobile/app/config/app_config.dart';
import 'package:study2work_mobile/shared/providers/app_providers.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  final config = AppConfig.fromFlavor(appFlavor);
  if (config.isBusiness &&
      !kIsWeb &&
      !Platform.isAndroid &&
      !Platform.isIOS) {
    sqfliteFfiInit();
    databaseFactory = databaseFactoryFfi;
  }

  runApp(
    ProviderScope(
      overrides: [appConfigProvider.overrideWithValue(config)],
      child: Study2WorkApp(config: config),
    ),
  );
}
