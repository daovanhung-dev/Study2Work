import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import 'package:study2work_mobile/app/config/app_config.dart';
import 'package:study2work_mobile/features/auth/presentation/role_login_page.dart';
import 'package:study2work_mobile/features/business/presentation/business_shell_page.dart';
import 'package:study2work_mobile/features/student/presentation/student_shell_page.dart';

import 'auth_navigation_state.dart';

GoRouter createAppRouter(AppConfig config) {
  final authState = AuthNavigationState.instance;

  return GoRouter(
    initialLocation: '/login',
    refreshListenable: authState,
    redirect: (context, state) {
      final isRolePath =
          state.matchedLocation == '/student' ||
          state.matchedLocation == '/business';
      if (!authState.isAuthenticated && isRolePath) {
        return '/login';
      }
      if (authState.isAuthenticated && state.matchedLocation == '/login') {
        return config.rolePath;
      }
      if (state.matchedLocation == '/student' && config.isBusiness) {
        return '/business';
      }
      if (state.matchedLocation == '/business' && config.isStudent) {
        return '/student';
      }
      return null;
    },
    routes: [
      GoRoute(
        path: '/login',
        name: 'login',
        builder: (context, state) => const RoleLoginPage(),
      ),
      GoRoute(
        path: '/student',
        name: 'student-home',
        builder: (context, state) => const StudentShellPage(),
      ),
      GoRoute(
        path: '/business',
        name: 'business-home',
        builder: (context, state) => const BusinessShellPage(),
      ),
      GoRoute(
        path: '/not-found',
        name: 'not-found',
        builder: (context, state) => const Scaffold(
          body: Center(child: Text('Không tìm thấy trang')),
        ),
      ),
    ],
    errorBuilder: (context, state) => const Scaffold(
      body: Center(child: Text('Không tìm thấy trang')),
    ),
  );
}
