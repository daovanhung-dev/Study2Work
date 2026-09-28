import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'package:study2work_mobile/app/config/app_config.dart';
import 'package:study2work_mobile/core/data/gemini/gemini_client.dart';
import 'package:study2work_mobile/core/data/neon/neon_client.dart';
import 'package:study2work_mobile/core/data/sqlite/session_store.dart';
import 'package:study2work_mobile/features/auth/domain/auth_repository.dart';
import 'package:study2work_mobile/features/business/auth/data/business_auth_repository.dart';
import 'package:study2work_mobile/features/business/auth/data/business_session_store.dart';
import 'package:study2work_mobile/features/business/chat/data/business_chat_repository.dart';
import 'package:study2work_mobile/features/business/legacy/models/doanh_nghiep.dart';
import 'package:study2work_mobile/features/chat/domain/chat_repository.dart';
import 'package:study2work_mobile/features/student/auth/data/student_auth_repository.dart';
import 'package:study2work_mobile/features/student/auth/data/student_session_store.dart';
import 'package:study2work_mobile/features/student/chat/data/student_chat_repository.dart';
import 'package:study2work_mobile/features/student/legacy/models/sinh_vien/sinh_vien.dart';

final appConfigProvider = Provider<AppConfig>((ref) {
  return AppConfig.fromFlavor(appFlavor);
});

final neonClientProvider = Provider<NeonClient>((ref) {
  ref.onDispose(() {
    NeonDatabase.instance.close();
  });
  return NeonDatabase.instance;
});

final geminiClientProvider = Provider<GeminiClient>((ref) {
  return AIService();
});

final studentSessionStoreProvider = Provider<SessionStore<SinhVien>>((ref) {
  return StudentSessionStore();
});

final businessSessionStoreProvider = Provider<SessionStore<DoanhNghiep>>((ref) {
  return BusinessSessionStore();
});

final authRepositoryProvider = Provider<AuthRepository>((ref) {
  final config = ref.watch(appConfigProvider);
  return config.isStudent
      ? StudentAuthRepository()
      : BusinessAuthRepository();
});

final chatRepositoryProvider = Provider<ChatRepository>((ref) {
  final config = ref.watch(appConfigProvider);
  return config.isStudent
      ? StudentChatRepository()
      : BusinessChatRepository();
});
