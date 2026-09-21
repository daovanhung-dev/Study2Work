import 'package:flutter/material.dart';

abstract final class AppColors {
  static const primary = Color(0xFF1D4ED8);
  static const action = Color(0xFF2563EB);
  static const primarySoft = Color(0xFFEFF6FF);
  static const navy = Color(0xFF0F172A);
  static const background = Color(0xFFF8FAFC);
  static const surface = Color(0xFFFFFFFF);
  static const border = Color(0xFFE2E8F0);
  static const muted = Color(0xFF64748B);
  static const success = Color(0xFF16A34A);
  static const warning = Color(0xFFD97706);
  static const danger = Color(0xFFDC2626);
  static const info = Color(0xFF0284C7);
}

abstract final class AppSpacing {
  static const xs = 4.0;
  static const sm = 8.0;
  static const md = 12.0;
  static const lg = 16.0;
  static const xl = 24.0;
  static const xxl = 32.0;
  static const section = 40.0;
}

abstract final class AppRadii {
  static const control = 12.0;
  static const card = 16.0;
  static const hero = 24.0;
  static const pill = 999.0;
}
