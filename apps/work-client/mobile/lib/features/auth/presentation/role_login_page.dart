import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'package:study2work_mobile/features/business/legacy/views/dang_nhap/dang_nhap.dart'
    as business_login;
import 'package:study2work_mobile/features/student/legacy/views/dang_nhap/dang_nhap.dart'
    as student_login;
import 'package:study2work_mobile/shared/providers/app_providers.dart';

class RoleLoginPage extends ConsumerWidget {
  const RoleLoginPage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final config = ref.watch(appConfigProvider);
    final authRepository = ref.watch(authRepositoryProvider);
    return config.isStudent
        ? student_login.DangNhap(authRepository: authRepository)
        : business_login.DangNhap(authRepository: authRepository);
  }
}
