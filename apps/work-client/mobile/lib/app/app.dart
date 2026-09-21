import 'package:flutter/material.dart';

import 'package:study2work_mobile/app/config/app_config.dart';
import 'package:study2work_mobile/app/router/app_router.dart';
import 'package:study2work_mobile/app/theme/app_theme.dart';

class Study2WorkApp extends StatelessWidget {
  const Study2WorkApp({required this.config, super.key});

  final AppConfig config;

  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      debugShowCheckedModeBanner: false,
      title: config.displayName,
      theme: AppTheme.light(),
      routerConfig: createAppRouter(config),
    );
  }
}
